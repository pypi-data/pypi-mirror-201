import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from dkist_fits_specifications import __version__ as spec_version
from dkist_header_validator import spec214_validator
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.write_l1 import CIWriteL1Frame
from dkist_processing_cryonirsp.tasks.write_l1 import SPWriteL1Frame
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb

# from dkist_processing_common.models.tags import Tag


@pytest.fixture(scope="function", params=[1, 4], ids=["stokes I only", "stokes IQUV"])
def write_ci_l1_task(
    recipe_run_id,
    calibrated_cryonirsp_dataset,
    init_cryonirsp_constants_db,
    request,
):
    num_of_stokes_params = request.param
    if num_of_stokes_params == 1:
        num_modstates = 1
    else:
        num_modstates = 2
    constants_db = CryonirspConstantsDb(
        AVERAGE_CADENCE=10,
        MINIMUM_CADENCE=10,
        MAXIMUM_CADENCE=10,
        VARIANCE_CADENCE=0,
        NUM_MAP_SCANS=1,
        NUM_SCAN_STEPS=2,
        # Needed so self.correct_for_polarization is set to the right value
        NUM_MODSTATES=num_modstates,
        ARM_ID="CI",
        AXIS_1_TYPE="HPLN-TAN",
        AXIS_2_TYPE="HPLT-TAN",
        AXIS_3_TYPE="AWAV",
    )

    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with CIWriteL1Frame(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            if num_of_stokes_params == 1:
                stokes_params = ["I"]
            else:
                stokes_params = ["I", "Q", "U", "V"]
            # Random data needed so skew and kurtosis don't barf
            hdu = fits.PrimaryHDU(
                data=np.random.random((128, 128, 1)) * 100.0, header=calibrated_cryonirsp_dataset
            )
            hdul = fits.HDUList([hdu])
            hdul[0].header["CTYPE1"] = "HPLN-TAN"
            hdul[0].header["CTYPE2"] = "HPLT-TAN"
            hdul[0].header["CTYPE3"] = "AWAV"
            for stokes_param in stokes_params:
                task.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        CryonirspTag.calibrated(),
                        CryonirspTag.frame(),
                        CryonirspTag.stokes(stokes_param),
                    ],
                )
            yield task, stokes_params
        except:
            raise
        finally:
            task.constants._purge()
            task.scratch.purge()


@pytest.fixture(scope="function", params=[1, 4], ids=["stokes I only", "stokes IQUV"])
def write_sp_l1_task(
    recipe_run_id,
    calibrated_cryonirsp_dataset,
    init_cryonirsp_constants_db,
    request,
):
    num_of_stokes_params = request.param
    if num_of_stokes_params == 1:
        num_modstates = 1
    else:
        num_modstates = 2
    constants_db = CryonirspConstantsDb(
        AVERAGE_CADENCE=10,
        MINIMUM_CADENCE=10,
        MAXIMUM_CADENCE=10,
        VARIANCE_CADENCE=0,
        NUM_MAP_SCANS=1,
        NUM_SCAN_STEPS=2,
        # Needed so self.correct_for_polarization is set to the right value
        NUM_MODSTATES=num_modstates,
        ARM_ID="SP",
    )

    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPWriteL1Frame(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            if num_of_stokes_params == 1:
                stokes_params = ["I"]
            else:
                stokes_params = ["I", "Q", "U", "V"]
            # Random data needed so skew and kurtosis don't barf
            hdu = fits.PrimaryHDU(
                data=np.random.random((128, 128, 1)) * 100.0, header=calibrated_cryonirsp_dataset
            )
            hdul = fits.HDUList([hdu])
            hdul[0].header["CTYPE1"] = "AWAV"
            hdul[0].header["CTYPE2"] = "HPLT-TAN"
            hdul[0].header["CTYPE3"] = "HPLN-TAN"
            for stokes_param in stokes_params:
                task.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        CryonirspTag.calibrated(),
                        CryonirspTag.frame(),
                        CryonirspTag.stokes(stokes_param),
                    ],
                )
            yield task, stokes_params
        except:
            raise
        finally:
            task.constants._purge()
            task.scratch.purge()


def test_write_ci_l1_frame(write_ci_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, stokes_params = write_ci_l1_task
    task()
    for stokes_param in stokes_params:
        files = list(
            task.read(
                tags=[
                    CryonirspTag.frame(),
                    CryonirspTag.output(),
                    CryonirspTag.stokes(stokes_param),
                ]
            )
        )
        assert len(files) == 1
        for file in files:
            assert file.exists
            assert spec214_validator.validate(file, extra=False)
            hdu_list = fits.open(file)
            header = hdu_list[1].header
            assert len(hdu_list) == 2  # Primary, CompImage
            assert type(hdu_list[0]) is fits.PrimaryHDU
            assert type(hdu_list[1]) is fits.CompImageHDU
            assert header["DTYPE1"] == "SPATIAL"
            assert header["DTYPE2"] == "SPATIAL"
            assert header["DTYPE3"] == "SPECTRAL"
            assert header["DAAXES"] == 2
            num_axes = 3
            if task.constants.num_map_scans > 1:
                num_axes += 1
                # Now test the scan number
                num_map_scans = task.constants.num_map_scans
                num_scan_steps = task.constants.num_scan_steps
                assert header[f"DNAXIS{num_axes}"] == num_map_scans * num_scan_steps
                current_scan_step = header["CNCURSCN"]
                current_map_scan = header["DSPSNUM"]
                # current scan step index = (current_map_scan - 1) * num_scan_steps + current_scan_step
                assert (
                    header[f"DINDEX{num_axes}"]
                    == (current_map_scan - 1) * num_scan_steps + current_scan_step
                )
            # Now test the stokes axes
            num_axes += 1
            if len(stokes_params) == 1:
                assert f"DNAXIS{num_axes}" not in header
                assert header["DNAXIS"] == 3
                assert header["DEAXES"] == 1
            else:
                assert header[f"DNAXIS{num_axes}"] == 4
                assert header["DNAXIS"] == 4
                assert header["DEAXES"] == 2
            assert header["INFO_URL"] == task.docs_base_url
            assert header["HEADVERS"] == spec_version
            assert (
                header["HEAD_URL"]
                == f"{task.docs_base_url}/projects/data-products/en/v{spec_version}"
            )
            calvers = task._get_version_from_module_name()
            assert header["CALVERS"] == calvers
            assert (
                header["CAL_URL"]
                == f"{task.docs_base_url}/projects/{task.constants.instrument.lower()}/en/v{calvers}/{task.workflow_name}.html"
            )
            calibrated_file = next(
                task.read(
                    tags=[
                        CryonirspTag.frame(),
                        CryonirspTag.calibrated(),
                        CryonirspTag.stokes(stokes_param),
                    ]
                )
            )
            cal_header = fits.open(calibrated_file)[0].header

            # Make sure we didn't overwrite pre-computed DATE-BEG and DATE-END keys
            assert header["DATE-BEG"] == cal_header["DATE-BEG"]
            assert header["DATE-END"] == cal_header["DATE-END"]
            date_avg = (
                (Time(header["DATE-END"], precision=6) - Time(header["DATE-BEG"], precision=6)) / 2
                + Time(header["DATE-BEG"], precision=6)
            ).isot
            assert header["DATE-AVG"] == date_avg
            assert isinstance(header["HLSVERS"], str)


def test_write_sp_l1_frame(write_sp_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, stokes_params = write_sp_l1_task
    task()
    for stokes_param in stokes_params:
        files = list(
            task.read(
                tags=[
                    CryonirspTag.frame(),
                    CryonirspTag.output(),
                    CryonirspTag.stokes(stokes_param),
                ]
            )
        )
        assert len(files) == 1
        for file in files:
            assert file.exists
            assert spec214_validator.validate(file, extra=False)
            hdu_list = fits.open(file)
            header = hdu_list[1].header
            assert len(hdu_list) == 2  # Primary, CompImage
            assert type(hdu_list[0]) is fits.PrimaryHDU
            assert type(hdu_list[1]) is fits.CompImageHDU
            assert header["DTYPE1"] == "SPECTRAL"
            assert header["DTYPE2"] == "SPATIAL"
            assert header["DTYPE3"] == "SPATIAL"
            assert header["DAAXES"] == 2
            if len(stokes_params) == 1:
                assert "DNAXIS4" not in header
                assert header["DNAXIS"] == 3
                assert header["DEAXES"] == 1
            else:
                assert header["DNAXIS4"] == 4
                assert header["DNAXIS"] == 4
                assert header["DEAXES"] == 2
            assert header["INFO_URL"] == task.docs_base_url
            assert header["HEADVERS"] == spec_version
            assert (
                header["HEAD_URL"]
                == f"{task.docs_base_url}/projects/data-products/en/v{spec_version}"
            )
            calvers = task._get_version_from_module_name()
            assert header["CALVERS"] == calvers
            assert (
                header["CAL_URL"]
                == f"{task.docs_base_url}/projects/{task.constants.instrument.lower()}/en/v{calvers}/{task.workflow_name}.html"
            )
            calibrated_file = next(
                task.read(
                    tags=[
                        CryonirspTag.frame(),
                        CryonirspTag.calibrated(),
                        CryonirspTag.stokes(stokes_param),
                    ]
                )
            )
            cal_header = fits.open(calibrated_file)[0].header

            # Make sure we didn't overwrite pre-computed DATE-BEG and DATE-END keys
            assert header["DATE-BEG"] == cal_header["DATE-BEG"]
            assert header["DATE-END"] == cal_header["DATE-END"]
            date_avg = (
                (Time(header["DATE-END"], precision=6) - Time(header["DATE-BEG"], precision=6)) / 2
                + Time(header["DATE-BEG"], precision=6)
            ).isot
            assert header["DATE-AVG"] == date_avg
            assert isinstance(header["HLSVERS"], str)
