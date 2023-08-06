"""CryoNIRSP compute beam boundary task."""
import largestinteriorrectangle as lir
import numpy as np
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger
from skimage import filters
from skimage import img_as_ubyte
from skimage.morphology import disk
from skimage.registration import phase_cross_correlation

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class BeamBoundariesCalibration(CryonirspTaskBase):
    """
    Task class for calculation of the beam boundaries for later use during calibration.

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
        Compute the beam boundaries by analyzing a set of solar gain images.

        Steps:
        1. Compute the average gain image
        2. Correct any bad pixels
        3. Smooth the image using a median filter with radius 3
        4. Use a bimodal threshold filter to segment the image into illuminated and non-illuminated regions
        5. Compute the boundaries of the illuminated region
        6. Extract the illuminated portion of the image
        7. Split the beams using a 10% buffer region around the horizontal mid-point
        8. Find the horizontal shift between the two images
        9. Identify the boundaries of the overlap
        10. Save the boundaries as a fits file (json?)


        Returns
        -------
        None

        """
        # Step 1:
        with self.apm_task_step(f"Compute average solar gain image"):
            average_solar_gain_array = self._compute_average_gain_array()
        # Step 2:
        with self.apm_task_step(f"Retrieve bad pixel map"):
            bad_pixel_map = self.intermediate_frame_load_full_bad_pixel_map()
            corrected_solar_gain_array = self.corrections_correct_bad_pixels(
                average_solar_gain_array, bad_pixel_map
            )
        with self.apm_task_step(f"Find the illuminated portion of the image"):
            # Step 3:
            # Smooth the array to get good segmentation
            smoothed_solar_gain_array = self._smooth_gain_array(corrected_solar_gain_array)
            # Step 4:
            # Segment the array into illuminated and non-illuminated pixels
            segmented_array = self._segment_array(smoothed_solar_gain_array)
            # Step 5:
            # Define the boundaries of the illuminated region
            illuminated_boundaries = self._compute_illuminated_boundaries(segmented_array)
        with self.apm_task_step(f"Compute the beam boundaries of the illuminated region"):
            # Steps 6 - 9:
            boundaries = self._compute_beam_boundaries(
                smoothed_solar_gain_array, illuminated_boundaries
            )
        # Step 10:
        with self.apm_writing_step("Writing beam boundaries"):
            for beam, array in enumerate(boundaries, start=1):
                self.intermediate_frame_write_arrays(
                    array, task_tag=CryonirspTag.task_beam_boundaries(), beam=beam
                )

    def _compute_average_gain_array(self) -> np.ndarray:
        """
        Compute an average of uncorrected solar gain arrays.

        We are computing the overall illumination pattern for both beams simultaneously,
        so no dark correction is required and no beam splitting is used at this point.
        Solar gain images are used because they have larger flux than the lamp gain images
        and the lamp gain images do not have the same illumination pattern as the solar
        gain images.

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

    def _smooth_gain_array(self, array: np.ndarray) -> np.ndarray:
        """
        Smooth the input array with morphological filtering using a disk shape.

        The array is smoothed to help eliminate artifacts in the image segmentation step.

        Parameters
        ----------
        array
            The input array to be smoothed

        Returns
        -------
        The smoothed output array
        """
        # Normalize the array, as skimage.filters requires that it be [0-1]
        norm_gain = img_as_ubyte((array - array.min()) / (array.max() - array.min()))
        # Smooth the array
        disk_size = self.parameters.beam_boundaries_smoothing_disk_size
        norm_gain = filters.rank.median(norm_gain, disk(disk_size))
        return norm_gain

    @staticmethod
    def _segment_array(array: np.ndarray) -> np.ndarray:
        """
        Segment the array into illuminated (True) and non-illuminated (False) regions.

        Parameters
        ----------
        array
            The array to be segmented

        Returns
        -------
        The boolean segmented output array
        """
        thresh = filters.threshold_minimum(array)
        logger.info(f"Segmentation threshold = {thresh}")
        segmented_array = (array > thresh).astype(bool)
        return segmented_array

    @staticmethod
    def _compute_illuminated_boundaries(array: np.ndarray) -> list[int]:
        """
        Compute the inscribed rectangular extent of the illuminated portion of the array.

        Parameters
        ----------
        array
            The segmented boolean array over which the illuminated boundaries are to be computed

        Returns
        -------
        The illuminated region boundaries [v_min, v_max, h_min, h_max]
        """
        """"""
        # Find the inscribed rectangle
        rect = lir.lir(array)
        # Compute the new image bounds, the maximums are exclusive and can be used in slices
        v_min, v_max, h_min, h_max = rect[1], rect[1] + rect[3], rect[0], rect[0] + rect[2]
        # Make sure all pixels are 1s
        if not np.all(array[v_min:v_max, h_min:h_max]):
            raise RuntimeError("Unable to compute illuminated image boundaries")
        # We separate the beams using the illuminated portion. Make sure that the number of
        # horizontal pixels is even, adjusting an edge if needed
        # num_h_pix represents the number of pixels in the illuminated beam in the horizontal direction
        num_h_pix = h_max - h_min
        # if num_h_pix is odd, then adjust one of the edges
        if num_h_pix % 2 == 1:
            # num_h_min_edge is the number of pixels in the unilluminated edge region
            # on the left side (minimum index values) of the image
            num_h_min_edge = h_min - 1
            # num_h_max_edge is the number of pixels in the unilluminated edge region
            # on the right side (maximum index values) of the image
            num_h_max_edge = array.shape[1] - h_max
            # Adjust the edge that has the smaller unilluminated region
            if num_h_min_edge > num_h_max_edge:
                h_max -= 1
            else:
                h_min += 1
        logger.info(f"Illuminated boundaries: {v_min = }, {v_max = }, {h_min = }, {h_max = }")
        return [v_min, v_max, h_min, h_max]

    @staticmethod
    def _compute_split_boundary(illuminated_array: np.ndarray) -> list[int]:
        """
        Compute the split boundary for the illuminated region.

        The split boundary is a margin region in the middle of the illuminated region
        where the transition between the beams occurs and is not used for processing

        Parameters
        ----------
        illuminated_array
            The array containing the illuminated region of the image

        Returns
        -------
        list[region_start, region_end]
        """
        # We split the illuminated region in half to coarsely define the beams
        split = illuminated_array.shape[1] // 2
        # NB: Assume a 10% margin around the middle split
        margin = split // 10
        # These boundary values are relative to extracted illuminated_array
        split_boundary = [split - margin, split + margin]
        return split_boundary

    @staticmethod
    def _split_beams(array: np.ndarray, split_boundary: list[int]) -> tuple[np.ndarray, np.ndarray]:
        """
        Split the beams coarsely along the horizontal axis in preparation for alignment.

        Parameters
        ----------
        array
            The array to be split
        split_boundary
            The split boundary locations [left_max, right_min]

        Returns
        -------
        tuple containing the split beams
        """
        left_beam = array[:, : split_boundary[0]]
        right_beam = array[:, split_boundary[1] :]
        return left_beam, right_beam

    def _compute_shift(self, left_beam: np.ndarray, right_beam: np.ndarray) -> int:
        """
        Compute the horizontal shift between the two beams using a cross correlation.

        Parameters
        ----------
        left_beam
            The coarse left beam image
        right_beam
            The coarse right beam image

        Returns
        -------
        horizontal shift required to align the beams
        """
        upsample_factor = self.parameters.beam_boundaries_upsample_factor
        shifts, _, _ = phase_cross_correlation(
            left_beam, right_beam, upsample_factor=upsample_factor
        )
        logger.info(f"{shifts=}")
        # Round to ints, as the correlation produces floats:
        shifts = [round(shift) for shift in shifts]
        # Ignoring any vertical shift for now
        # Fine shifts along both axes are computed in the geometric calibration
        return shifts[1]

    @staticmethod
    def _compute_sp_beam_overlap_boundaries(
        illuminated_boundaries: list[int], split_boundary: list[int], shift: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Compute the final boundaries to be used when extracting beams from the original input images.

        Parameters
        ----------
        illuminated_boundaries
            The boundaries of the illuminated portion of the image (includes both beams)
        split_boundary
            The central region to be unused, where the split occurs
        shift
            The horizontal shift required to align the two beam images

        Returns
        -------
        (beam_1_boundaries, beam_2_boundaries), where each beam boundary is defined as:
        np.array([v_min, v_max, h_min, h_max]
        """
        # A negative shift means the right beam image shifts to the left relative to the left beam image,
        # or in the negative direction of the horizontal axis index
        # The values computed here are to be used relative to the *uncorrected* full-size input images
        # The split boundaries are relative to the extracted illuminated beam, not the original beam
        # NB: The upper bounds are exclusive, ready to be used in array slicing
        v_min, v_max, h_min, h_max = illuminated_boundaries
        if shift < 0:
            left_beam_h_min = h_min
            left_beam_h_max = h_min + split_boundary[0] + shift
            right_beam_h_min = h_min + split_boundary[1] - shift
            right_beam_h_max = h_max
        else:
            left_beam_h_min = h_min + shift
            left_beam_h_max = h_min + split_boundary[0]
            right_beam_h_min = h_min + split_boundary[1]
            right_beam_h_max = h_max - shift
        # For now, v_min and v_max are the same for both beams. This may change in the future.
        beam_1_boundaries = np.array([v_min, v_max, left_beam_h_min, left_beam_h_max], dtype=int)
        beam_2_boundaries = np.array([v_min, v_max, right_beam_h_min, right_beam_h_max], dtype=int)
        logger.info(f"{beam_1_boundaries = }")
        logger.info(f"{beam_2_boundaries = }")

        return beam_1_boundaries, beam_2_boundaries

    def _compute_beam_boundaries(
        self,
        smoothed_solar_gain_array: np.ndarray,
        illuminated_boundaries: list[int],
    ) -> list[np.ndarray]:
        """
        Compute the beam boundaries from the illuminated beam and save them as a file.

        Parameters
        ----------
        smoothed_solar_gain_array
            The smoothed solar gain array, ready for beam identification
        illuminated_boundaries
            The boundaries of the illuminated beam [v_min, v_max, h_min, h_max]

        Returns
        -------
        A list of beam boundary arrays, one for each beam

        """
        # The illuminated beam boundaries ARE the final beam boundaries for CI
        # Step 6:
        if self.constants.arm_id == "CI":
            beam_boundaries = np.array(illuminated_boundaries)
            return [beam_boundaries]

        # SP beams require additional processing
        # Step 6:
        # Extract the illuminated region from the solar gain array
        illuminated_array = smoothed_solar_gain_array[
            illuminated_boundaries[0] : illuminated_boundaries[1],
            illuminated_boundaries[2] : illuminated_boundaries[3],
        ]
        # Step 7:
        # Split the beams
        split_boundary = self._compute_split_boundary(illuminated_array)
        left_beam, right_beam = self._split_beams(illuminated_array, split_boundary)
        # Step 8:
        shift = self._compute_shift(left_beam, right_beam)
        # Step 9:
        beam_1_boundaries, beam_2_boundaries = self._compute_sp_beam_overlap_boundaries(
            illuminated_boundaries, split_boundary, shift
        )
        return [beam_1_boundaries, beam_2_boundaries]
