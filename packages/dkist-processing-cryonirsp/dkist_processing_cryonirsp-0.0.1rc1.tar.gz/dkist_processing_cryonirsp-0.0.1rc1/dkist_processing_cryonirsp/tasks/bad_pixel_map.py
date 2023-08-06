"""Task class for bad pixel map computation."""
import numpy as np
import scipy.ndimage as spnd
from dkist_processing_math.statistics import average_numpy_arrays

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import CryonirspTaskName
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class BadPixelMapCalibration(CryonirspTaskBase):
    """
    Task class for calculation of the bad pixel map for later use during calibration.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def run(self):
        """
        Compute the bad pixel map by analyzing a set of solar gain images.

        Steps:
        1. Compute the average gain image
        2. Smooth the array with a median filter
        3. Calculate the difference between the smoothed and input arrays
        4. Threshold the difference array on both ends to determine good and bad pixels
        5. Save the bad pixel map as a fits file

        Returns
        -------
        None

        """
        # Step 1:
        with self.apm_task_step(f"Compute average uncorrected solar gain image"):
            average_solar_gain_array = self._compute_average_gain_array()
        with self.apm_task_step(f"Compute the bad pixel map"):
            # Step 2:
            filter_size = self.parameters.bad_pixel_map_median_filter_size
            # TODO: Distinguish between SP and CI here? May need two parameters
            # TODO: as a 2D kernel does not need to be as large as the 1D kernel length.
            # Filter only along the slit so as not to broaden the spectral lines.
            # Broadening the spectral lines causes them to leak into the difference
            # array calculated below and possibly get classified as bad pixels
            # Use constant mode and the median for cval, as this gives better
            # filtering ability and behavior at the edge pixels
            filtered_array = spnd.median_filter(
                average_solar_gain_array,
                size=(filter_size, 1),
                mode="constant",
                cval=np.median(average_solar_gain_array),
            )
            # Step 3:
            diff = filtered_array - average_solar_gain_array
            # Step 4:
            thresh = self.parameters.bad_pixel_map_threshold_factor
            bad_pixel_map = np.array((np.abs(diff) > thresh * diff.std()), dtype=int)
        # Step 5:
        with self.apm_writing_step("Writing bad pixel map"):
            self.intermediate_frame_write_arrays(
                bad_pixel_map, task=CryonirspTaskName.bad_pixel_map.value
            )

    def _compute_average_gain_array(self) -> np.ndarray:
        """
        Compute an average of uncorrected solar gain arrays.

        We are computing the overall illumination pattern for one (CI) or both (SP) beams
        simultaneously, so no dark correction is required and no beam splitting is used at
        this point. Solar gain images are used because of their higher flux levels and they
        more accurately represent the illuminated beam seen in solar images.

        Returns
        -------
        The average gain array
        """
        # Get the linearized solar gain arrays
        lin_corr_gain_arrays = self.linearized_frame_full_array_generator(
            tags=[
                CryonirspTag.task_solar_gain(),
                CryonirspTag.linearized(),
                CryonirspTag.frame(),
            ]
        )
        averaged_gain_data = average_numpy_arrays(lin_corr_gain_arrays)
        return averaged_gain_data
