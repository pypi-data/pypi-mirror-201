"""CryoNIRSP Linearity COrrection Task."""
import numpy as np
from astropy.io import fits
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from logging42 import logger
from numba import njit
from numba import prange

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspRampFitsAccess
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspLinearityTaskBase
from dkist_processing_cryonirsp.tasks.mixin.input_frame import InputFrameMixin


class LinearityCorrection(CryonirspLinearityTaskBase, FitsDataMixin, InputFrameMixin):
    """Task class for performing linearity correction on all input frames, regardless of task type."""

    @property
    def polyfit_coeffs(self):
        """Property to set/get the polyfit coefficients array for linearization."""
        if self._polyfit_coeffs is None:
            raise ValueError(
                "polyfit coefficients array has not been set. This should never happen."
            )
        return self._polyfit_coeffs

    @polyfit_coeffs.setter
    def polyfit_coeffs(self, array: np.ndarray) -> None:
        """Getter for the polyfit coefficients property."""
        self._polyfit_coeffs = array

    @property
    def linear_thresh(self):
        """Property to set/get the linear thresholds array for linearization."""
        if self._linear_thresh is None:
            raise ValueError("linear thresholds array has not been set. This should never happen.")
        return self._linear_thresh

    @linear_thresh.setter
    def linear_thresh(self, array: np.ndarray) -> None:
        """Getter for the linear thresholds property."""
        self._linear_thresh = array

    def pre_run(self):
        """Set the threshold and polyfit parameters for the current arm, SP or CI."""
        super().pre_run()
        self._set_linearity_params()

    def _set_linearity_params(self):
        if self.constants.arm_id == "CI":
            self.polyfit_coeffs = self.parameters.ci_polyfit
            self.linear_thresh = self.parameters.ci_thresholds
        elif self.constants.arm_id == "SP":
            self.polyfit_coeffs = self.parameters.sp_polyfit
            self.linear_thresh = self.parameters.sp_thresholds
        else:
            raise ValueError(f"Invalid arm_id: {self.constants.arm_id}")

    def run(self):
        """
        Run method for this task.

        Steps to be performed:
            - Gather all input frames
            - Iterate through frames
                - Perform linearity correction for this frame (algorithm is TBD)
                - Get list of all tags for this frame
                - Remove input tag and add linearity_corrected tag
                - Write linearity corrected frame with updated tag list
                - Delete original frame

        Returns
        -------
        None
        """
        # Note: We use date-obs to identify individual ramp sets here.
        # The ramp number is not a unique identifier when frames from different subtask
        # types are combined in a single scratch dir.
        # Alternatively, a tuple of (subtask type, ramp number) may be sufficient to identify
        # individual ramp sets. For now, we are using date-obs to mirror what Tom does in his codes.
        # Also, by using date-obs and then getting a fits access generator for all the frames that
        # match that date, we avoid having to check for the number of frames per ramp. Checking that
        # is problematic if datasets with different frames per ramp are combined in scratch as you can no
        # longer use a constant, but will have to read it from the header of the first frame. The assumption
        # here is that the fits access generator returns all the frames in a ramp with a desired date-obs.
        with self.apm_step("Gather input frames"):
            num_frames = len(self.constants.time_obs_list)
            frame_num = 0
            for time_obs in self.constants.time_obs_list:
                frame_num += 1
                logger.info(f"Processing frames from {time_obs}, frame {frame_num} of {num_frames}")
                self._perform_linearity_correction(time_obs=time_obs)
            logger.info(f"Processed {frame_num} frames")

    def _perform_linearity_correction(self, time_obs: str) -> None:
        """
        Create a linearity corrected fits object from a series of input frames (ramp).

        Parameters
        ----------
        time_obs
            The common timestamp for all frames in the series (ramp)

        Returns
        -------
        None

        """
        # Get the input frame objects for this ramp
        input_objects = self.input_frame_fits_access_generator(time_obs=time_obs)
        # Now sort them based on frame in ramp
        sorted_input_objects = sorted(input_objects, key=lambda x: x.curr_frame_in_ramp)
        output_array = self._reduce_ramp_set(
            sorted_input_objects,
            mode="LookUpTable",
            camera_readout_mode=self.constants.camera_readout_mode,
            lin_curve=self.polyfit_coeffs,
            thresholds=self.linear_thresh,
        )
        # Linearity correction is complete. Adjust the tags and write the output
        # Grab the last object for tags and the header
        last_object = sorted_input_objects[-1]
        # Get the list of all tags for this frame
        all_tags = list(self.scratch.tags(last_object.name))
        # Remove these tags, as they are no longer needed
        all_tags.remove(CryonirspTag.input())
        all_tags.remove(CryonirspTag.curr_frame_in_ramp(last_object.curr_frame_in_ramp))
        # Add the linearized tag
        all_tags.append(CryonirspTag.linearized())
        # Write a new fits output object using the header from the last object
        hdul = fits.HDUList([fits.PrimaryHDU(header=last_object.header, data=output_array)])
        # Save to scratch with updated tags
        self.fits_data_write(
            hdu_list=hdul,
            tags=all_tags,
        )

    # The methods below are derived versions of the same codes in Tom Schad's h2rg.py
    @staticmethod
    @njit(parallel=True)
    def _lin_correct(raw_data, linc):
        """Perform the linearity fit using NUMBA."""
        return raw_data / (
            linc[0] + raw_data * (linc[1] + raw_data * (linc[2] + raw_data * linc[3]))
        )

    @staticmethod
    @njit(parallel=True)
    def _get_slopes(exptimes, data, thres):
        """Compute the slopes using NUMBA."""
        dsh = data.shape
        nelem = dsh[0] * dsh[1]
        proc_ramp = np.zeros(nelem)
        rdata = data.reshape((nelem, dsh[2]))
        rthres = thres.ravel()
        for i in prange(nelem):
            yy = rdata[i, :]
            weights = np.sqrt(yy)
            weights[yy > rthres[i]] = 0.0
            if np.sum(weights > 0) >= 2:
                sumw = np.sum(weights)
                # xw, yw are weighted x and y means, scalars
                xw = np.dot(weights, exptimes) / sumw
                yw = np.dot(weights, yy) / sumw
                # xd and yd are demeaned x and y vectors
                xd = exptimes - xw
                yd = yy - yw
                # wxd is a temp var used to get the weights into the products below
                wxd = weights * xd
                proc_ramp[i] = np.dot(wxd, yd) / np.dot(wxd, xd)
        return proc_ramp.reshape((dsh[0], dsh[1]))

    def _reduce_ramp_set(
        self,
        ramp_objs: list[CryonirspRampFitsAccess],
        mode: str = None,
        camera_readout_mode: str = None,
        lin_curve: np.ndarray = None,
        thresholds: np.ndarray = None,
    ) -> np.ndarray:
        """
        Process a single ramp from a set of input frames.

        mode:  'LookUpTable','FastCDS','FitUpTheRamp' (ignored if data is line by line)
        returns processed frames and last header (for now)
        """
        ramp_hdrs = [item.header for item in ramp_objs]

        if mode != "LookUpTable":
            raise ValueError(f"Linearization mode {mode} is currently not supported.")

        if camera_readout_mode != "FastUpTheRamp":
            raise ValueError(
                f"Camera readout mode {camera_readout_mode} is currently not supported."
            )

        # drop first frame in FastUpTheRamp
        ramp_objs = ramp_objs[1:]
        ramp_hdrs = ramp_hdrs[1:]

        # Get exptimes and raw data
        exptimes = np.array([obj.fpa_exposure_time_ms for obj in ramp_objs])
        # Create a 3D stack of the ramp frames
        raw_data = np.zeros((ramp_objs[0].data.shape + (len(ramp_objs),)))
        for n, obj in enumerate(ramp_objs):
            raw_data[:, :, n] = obj.data

        # support for single hardware ROI
        # NB 1: Unless we parse for these keywords, have to use the headers here
        # NB 2: The threshold table is originally constructed for the full sensor size (2k x 2k)
        #       The code below extracts the portion of the thresholds that map to the actual
        #       data size from the camera
        hwroi1_origin_x = ramp_hdrs[0]["CAM__034"]
        hwroi1_origin_y = ramp_hdrs[0]["CAM__035"]
        hwroi1_size_x = ramp_hdrs[0]["CAM__036"]
        hwroi1_size_y = ramp_hdrs[0]["CAM__037"]
        # Extract the desired region of the thresh table
        thres_roi = thresholds[
            hwroi1_origin_y : (hwroi1_origin_y + hwroi1_size_y),
            hwroi1_origin_x : (hwroi1_origin_x + hwroi1_size_x),
        ]

        # correct the whole data first using the curve derived from the on Sun data
        linc = np.flip(lin_curve)
        raw_data = self._lin_correct(raw_data, linc)

        slopes = self._get_slopes(exptimes, raw_data, thres_roi)
        # Scale the slopes by the exposure time to convert to counts
        processed_frame = slopes * np.nanmax(exptimes)
        return processed_frame
