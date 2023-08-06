# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.
import pytest

from responsibleai_tabular_automl.rai_automl import (
    _compute_and_upload_rai_insights_internal,
)
from azureml.core import Workspace, Run


class TestRAIAutoML:
    @pytest.mark.skip(
        "Skipping since it is not possible to "
        "run this test in build pipeline"
    )
    def test_compute_and_upload_rai_insights_internal_classification(self):
        ws = Workspace.get(
            "RAIPM2",
            subscription_id="fac34303-435d-4486-8c3f-7094d82a0b60",
            resource_group="RAIPM",
        )
        automl_run = ws.get_run(
            "AutoML_ee749e35-558a-4b95-9ddf-4ce55b4713df_2"
        )
        assert automl_run is not None
        rai_run = Run._start_logging(
            automl_run.experiment, snapshot_directory=None
        )
        _compute_and_upload_rai_insights_internal(rai_run, automl_run)

    @pytest.mark.skip(
        "Skipping since it is not possible to "
        "run this test in build pipeline"
    )
    def test_compute_and_upload_rai_insights_internal_regression(self):
        ws = Workspace.get(
            "RAIPM2",
            subscription_id="fac34303-435d-4486-8c3f-7094d82a0b60",
            resource_group="RAIPM",
        )
        automl_run = ws.get_run(
            "AutoML_ea3b2990-9602-4f4c-b5e6-3001fa903995_3"
        )
        assert automl_run is not None
        rai_run = Run._start_logging(
            automl_run.experiment, snapshot_directory=None
        )
        _compute_and_upload_rai_insights_internal(rai_run, automl_run)
