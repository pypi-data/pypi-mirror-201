from dataclasses import asdict

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from hypothesis import example
from hypothesis import given
from hypothesis import HealthCheck
from hypothesis import settings
from hypothesis import strategies as st

from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb


@pytest.fixture(scope="function")
def basic_science_task_with_parameter_mixin(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db
):
    class Task(CryonirspTaskBase):
        def run(self):
            ...

    init_cryonirsp_constants_db(recipe_run_id, CryonirspConstantsDb())
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    )
    try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
        assign_input_dataset_doc_to_task(task, param_class())
        yield task, param_class()
    except:
        raise
    finally:
        task.scratch.purge()
        task.constants._purge()


def test_non_wave_parameters(basic_science_task_with_parameter_mixin):
    """
    Given: A Science task with the parameter mixin
    When: Accessing properties for parameters that do not depend on wavelength
    Then: The correct value is returned
    """
    task, expected = basic_science_task_with_parameter_mixin
    task_param_attr = task.parameters
    for pn, pv in asdict(expected).items():
        if type(pv) is not dict:  # Don't test wavelength dependent parameters
            assert getattr(task_param_attr, pn.replace("cryonirsp_", "")) == pv


@given(wave=st.floats(min_value=800.0, max_value=2000.0))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@example(wave=1082.7)
def test_wave_parameters(basic_science_task_with_parameter_mixin, wave):
    """
    Given: A Science task with the paramter mixin
    When: Accessing properties for parameters that depend on wavelength
    Then: The correct value is returned
    """
    task, expected = basic_science_task_with_parameter_mixin
    task_param_attr = task.parameters
    task_param_attr._wavelength = wave
    pwaves = np.array(expected.cryonirsp_solar_zone_normalization_percentile.wavelength)
    midpoints = 0.5 * (pwaves[1:] + pwaves[:-1])
    idx = np.sum(midpoints < wave)
    for pn, pv in asdict(expected).items():
        if type(pv) is dict and "wavelength" in pv:
            assert getattr(task_param_attr, pn.replace("cryonirsp_", "")) == pv["values"][idx]


def test_file_parameters(basic_science_task_with_parameter_mixin):
    """
    Given: A Science task with the parameter mixin
    When: Accessing properties for parameters that are based on files
    Then: The correct value is returned
    """
    task, expected = basic_science_task_with_parameter_mixin
    task_param_attr = task.parameters
    for pn, pv in asdict(expected).items():
        if type(pv) is dict and "parameter_value_id" in pv:  # Specifically test file parameters
            actual = getattr(task_param_attr, pn.replace("cryonirsp_", ""))
            expected = task.parameters._get_param_data_from_npy_file(pv["parameter_value"])
            assert np.array_equal(actual, expected)
