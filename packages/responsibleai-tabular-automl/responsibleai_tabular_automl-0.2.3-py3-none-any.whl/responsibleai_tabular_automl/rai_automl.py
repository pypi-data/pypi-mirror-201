# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

"""Module for computing and uploading RAI insights for AutoML models."""

import subprocess
import os
import shutil
import time
from typing import Optional
import pandas as pd
import json
import numpy as np
import warnings

from ml_wrappers.model.predictions_wrapper import (
    PredictionsModelWrapperClassification,
    PredictionsModelWrapperRegression,
)

from azureml.core.runconfig import RunConfiguration
from azureml.core.run import Run
from responsibleai import RAIInsights
from responsibleai.serialization_utilities import serialize_json_safe
from pathlib import Path
from azureml.core import ScriptRunConfig

from ._loggerfactory import _LoggerFactory, track

_ai_logger = None
submit_locally_managed_run = False


def _get_logger():
    global _ai_logger
    if _ai_logger is None:
        _ai_logger = _LoggerFactory.get_logger(__file__)
    return _ai_logger


_get_logger()


@track(_get_logger)
def _compute_and_upload_rai_insights_internal(
    current_run: Run, automl_child_run: Run
):
    automl_child_run.download_files("outputs/rai")

    print("Generating RAI insights for AutoML child run")
    _ai_logger.info("Generating RAI insights for AutoML child run")

    metadata = None
    with open("outputs/rai/metadata.json", "r") as fp:
        metadata = json.load(fp)

    train = pd.read_parquet("outputs/rai/train.df.parquet")
    test = pd.read_parquet("outputs/rai/test.df.parquet")
    train_predictions = pd.read_parquet(
        "outputs/rai/predictions.npy.parquet"
    ).values
    test_predictions = pd.read_parquet(
        "outputs/rai/predictions_test.npy.parquet"
    ).values

    if metadata["task_type"] == "classification":
        train_prediction_probabilities = pd.read_parquet(
            "outputs/rai/prediction_probabilities.npy.parquet"
        ).values
        test_prediction_probabilities = pd.read_parquet(
            "outputs/rai/prediction_test_probabilities.npy.parquet"
        ).values
    else:
        train_prediction_probabilities = None
        test_prediction_probabilities = None

    target_column_name = metadata["target_column"]
    task_type = metadata["task_type"]
    classes = metadata["classes"]

    categorical_features = (
        metadata["feature_type_summary"]["Categorical"]
        + metadata["feature_type_summary"]["CategoricalHash"]
    )
    dropped_features = (
        metadata["feature_type_summary"]["Hashes"]
        + metadata["feature_type_summary"]["AllNan"]
        + metadata["feature_type_summary"]["Ignore"]
    )
    datetime_features = metadata["feature_type_summary"]["DateTime"]
    text_features = metadata["feature_type_summary"]["Text"]

    X_test = test.drop(columns=[target_column_name])
    X_train = train.drop(columns=[target_column_name])
    if len(dropped_features) > 0:
        X_test = X_test.drop(columns=dropped_features)
        X_train = X_train.drop(columns=dropped_features)
    all_data = pd.concat([X_test, X_train])
    model_predict_output = np.concatenate(
        (test_predictions, train_predictions)
    )

    if metadata["task_type"] == "classification":
        model_predict_proba_output = np.concatenate(
            (test_prediction_probabilities, train_prediction_probabilities)
        )
        model_wrapper = PredictionsModelWrapperClassification(
            all_data, model_predict_output, model_predict_proba_output
        )
    else:
        model_wrapper = PredictionsModelWrapperRegression(
            all_data, model_predict_output
        )

    train = train.drop(columns=dropped_features)
    test = test.drop(columns=dropped_features)
    if len(text_features) == 0 and len(datetime_features) == 0:
        _ai_logger.info("Generating RAI insights for {} samples.".format(
            len(test)))
        rai_insights = RAIInsights(
            model=model_wrapper,
            train=train,
            test=test,
            target_column=target_column_name,
            categorical_features=categorical_features,
            task_type=task_type,
            classes=classes,
        )
        rai_insights.explainer.add()
        rai_insights.error_analysis.add()
        rai_insights.compute()
        rai_insights.save("dashboard")
        current_run.upload_folder("dashboard", "dashboard")

        rai_data = rai_insights.get_data()
        rai_dict = serialize_json_safe(rai_data)
        ux_json_path = Path("ux_json")
        ux_json_path.mkdir(parents=True, exist_ok=True)
        json_filename = ux_json_path / "dashboard.json"
        with open(json_filename, "w") as json_file:
            json.dump(rai_dict, json_file)
        current_run.upload_folder("ux_json", "ux_json")
        automl_child_run.tag("model_rai", "True")
        print("Successfully generated and uploaded the RAI insights")
        _ai_logger.info("Successfully generated and uploaded the RAI insights")
    else:
        warnings.warn("Currently RAI is not supported for "
                      "text and datetime features")
        _ai_logger.info("Currently RAI is not supported for "
                        "text and datetime features")
    current_run.complete()


@track(_get_logger)
def _create_project_folder(
    automl_parent_run_id: str, automl_child_run_id: str
):
    project_folder = "./automl_experiment_submit_folder"

    os.makedirs(project_folder, exist_ok=True)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rai_script_path = os.path.join(dir_path, "automl_inference_run.py")
    shutil.copy(rai_script_path, project_folder)

    # shutil.copy("automl_inference_run.py", project_folder)

    script_file_name = os.path.join(project_folder, "automl_inference_run.py")

    # Open the sample script for modification
    with open(script_file_name, "r") as cefr:
        content = cefr.read()

    content = content.replace("<<automl_parent_run_id>>", automl_parent_run_id)

    content = content.replace("<<automl_child_run_id>>", automl_child_run_id)

    # Write sample file into your script folder.
    with open(script_file_name, "w") as cefw:
        cefw.write(content)

    return project_folder


@track(_get_logger)
def _create_run_configuration(automl_child_run_id, ws):
    automl_run = ws.get_run(automl_child_run_id)
    run_configuration = RunConfiguration()
    run_configuration.environment = automl_run.get_environment()
    run_configuration.target = "local"
    run_configuration.script = "automl_inference_run.py"
    return run_configuration


def call_with_output(command):
    success = False
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT
        ).decode()
        success = True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
    except Exception as e:
        # check_call can raise other exceptions, such as FileNotFoundError
        output = str(e)
    return (success, output)


@track(_get_logger)
def execute_automl_inference_script(automl_child_run_id, ws):
    automl_run = ws.get_run(automl_child_run_id)
    print("Generating predictions for AutoML model")
    _ai_logger.info("Generating predictions for AutoML model")

    command = ["pip", "list"]
    success, output = call_with_output(command)

    automl_run.download_file("outputs/mlflow-model/conda.yaml", "conda.yaml")
    automl_env_name = "automl_env_" + str(time.time())
    command = [
        "conda",
        "env",
        "create",
        "--name",
        automl_env_name,
        "--file",
        os.path.join("conda.yaml"),
    ]
    success, output = call_with_output(command)

    if not success:
        _ai_logger.info("Error creating conda environment")
        raise Exception(output)

    inference_script_name = (
        "./automl_experiment_submit_folder" + "/automl_inference_run.py"
    )
    command = [
        "conda",
        "run",
        "-n",
        automl_env_name,
        "python",
        inference_script_name,
    ]
    success, output = call_with_output(command)

    if not success:
        _ai_logger.info("Error running automl script in conda environment")
        raise Exception(output)

    command = [
        "conda",
        "env",
        "remove",
        "--name",
        automl_env_name,
        "-y"
    ]
    success, output = call_with_output(command)
    print("Successfully generated predictions for AutoML model")
    _ai_logger.info("Successfully generated predictions for AutoML model")


@track(_get_logger)
def compute_and_upload_rai_insights(
    automl_parent_run_id: Optional[str] = None,
    automl_child_run_id: Optional[str] = None
):
    print("The automl child run-id is: " + str(automl_child_run_id))
    print("The automl parent run-id is: " + str(automl_parent_run_id))

    rai_run = Run.get_context()
    print("The current run-id is: " + rai_run.id)

    if submit_locally_managed_run:
        _ai_logger.info("Submitting locally managed run to compute AutoML "
                        "artifacts.")
        project_folder = _create_project_folder(
            automl_parent_run_id, automl_child_run_id
        )
        run_configuration = _create_run_configuration(
            automl_child_run_id, rai_run.experiment.workspace
        )

        src = ScriptRunConfig(
            source_directory=project_folder, run_config=run_configuration
        )
        automl_inference_run = rai_run.experiment.submit(config=src)
        automl_inference_run.wait_for_completion()
    else:
        _ai_logger.info("Creating local conda environment to compute "
                        "AutoML artifacts.")
        # Create conda env from native commands and submit script
        project_folder = _create_project_folder(
            automl_parent_run_id, automl_child_run_id
        )

        execute_automl_inference_script(
            automl_child_run_id, rai_run.experiment.workspace
        )

    automl_run = rai_run.experiment.workspace.get_run(automl_child_run_id)
    _compute_and_upload_rai_insights_internal(rai_run, automl_run)


# compute_and_upload_rai_insights("<<parent_run_id>>", "<<child_run_id>>")
