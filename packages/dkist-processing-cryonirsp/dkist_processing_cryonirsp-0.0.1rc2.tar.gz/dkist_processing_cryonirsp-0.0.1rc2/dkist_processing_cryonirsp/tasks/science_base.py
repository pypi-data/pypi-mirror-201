"""Cryonirsp science calibration task."""
from abc import abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_pac.optics.telescope import Telescope
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


@dataclass
class CalibrationCollection:
    """Dataclass to hold all calibration objects and allow for easy, property-based access."""

    dark: dict
    solar_gain: dict
    angle: dict | None
    state_offset: dict | None
    spec_shift: dict | None
    demod_matrices: dict | None


class ScienceCalibrationBase(CryonirspTaskBase):
    """
    Task class for Cryonirsp science calibration of polarized and non-polarized data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    def collect_calibration_objects(self) -> CalibrationCollection:
        """
        Collect *all* calibration for all modstates, and exposure times.

        Doing this once here prevents lots of reads as we reduce the science data.
        """
        dark_dict = defaultdict(dict)
        solar_dict = dict()
        angle_dict = dict() if self.constants.arm_id == "SP" else None
        state_offset_dict = dict() if self.constants.arm_id == "SP" else None
        spec_shift_dict = dict() if self.constants.arm_id == "SP" else None
        demod_dict = dict() if self.constants.correct_for_polarization else None

        for beam in range(1, self.constants.num_beams + 1):
            # Load the dark arrays
            for exp_time in self.constants.observe_exposure_times:
                try:
                    dark_array = self.intermediate_frame_load_dark_array(
                        beam=beam, exposure_time=exp_time
                    )
                except StopIteration:
                    raise ValueError(f"No matching dark found for {exp_time = } s")
                dark_dict[CryonirspTag.beam(beam)][
                    CryonirspTag.exposure_time(exp_time)
                ] = dark_array

            # Load the gain arrays
            solar_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_solar_gain_array(
                beam=beam,
            )

            if self.constants.arm_id == "SP":
                # Load the angle arrays
                angle_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_angle(beam=beam)
                # Load the state offsets
                state_offset_dict[
                    CryonirspTag.beam(beam)
                ] = self.intermediate_frame_load_state_offset(beam=beam)
                # Load the spectral shifts
                spec_shift_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_spec_shift(
                    beam=beam
                )

            # Load the demod matrices
            if self.constants.correct_for_polarization:
                demod_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_demod_matrices(
                    beam=beam
                )

        return CalibrationCollection(
            dark=dark_dict,
            solar_gain=solar_dict,
            angle=angle_dict,
            state_offset=state_offset_dict,
            spec_shift=spec_shift_dict,
            demod_matrices=demod_dict,
        )

    @abstractmethod
    def process_frames(self, calibrations: CalibrationCollection):
        """Abstract method to be implemented in subclass."""
        pass

    record_provenance = True

    def run(self):
        """
        Run Cryonirsp science calibration.

        - Collect all calibration objects
        - Process all frames
        - Record quality metrics


        Returns
        -------
        None

        """
        with self.apm_task_step("Loading calibration objects"):
            calibrations = self.collect_calibration_objects()

        with self.apm_task_step(
            f"Processing Science Frames for "
            f"{self.constants.num_map_scans} map scans and "
            f"{self.constants.num_scan_steps} scan steps"
        ):
            self.process_frames(calibrations=calibrations)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_science_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_observe(),
                ],
            )

            self.quality_store_task_type_counts(
                task_type=TaskName.observe.value, total_frames=no_of_raw_science_frames
            )

    def process_polarimetric_modstates(
        self,
        beam: int,
        meas_num: int,
        scan_step: int,
        map_scan: int,
        exp_time: float,
        calibrations: CalibrationCollection,
    ) -> tuple[np.ndarray, fits.Header]:
        """
        Process a single polarimetric array as much as is possible.

        This includes basic corrections and demodulation.
        """
        # Create the 3D stack of corrected modulated arrays
        array_shape = calibrations.dark[CryonirspTag.beam(1)][
            CryonirspTag.exposure_time(exp_time)
        ].shape
        array_stack = np.zeros(array_shape + (self.constants.num_modstates,))
        header_stack = []

        with self.apm_processing_step(f"Correcting {self.constants.num_modstates} modstates"):
            for modstate in range(1, self.constants.num_modstates + 1):
                # Correct the arrays
                corrected_array, corrected_header = self.correct_single_frame(
                    beam=beam,
                    modstate=modstate,
                    meas_num=meas_num,
                    scan_step=scan_step,
                    map_scan=map_scan,
                    exp_time=exp_time,
                    calibrations=calibrations,
                )
                # Add this result to the 3D stack
                array_stack[:, :, modstate - 1] = corrected_array
                header_stack.append(corrected_header)

        with self.apm_processing_step("Applying instrument polarization correction"):
            logger.info("Applying instrument polarization correction")
            intermediate_array = self.polarization_correction(
                array_stack, calibrations.demod_matrices[CryonirspTag.beam(beam)]
            )
            intermediate_header = self._compute_date_keys(header_stack)

        return intermediate_array, intermediate_header

    def write_calibrated_array(
        self,
        calibrated_object: CryonirspL0FitsAccess,
        map_scan: int,
        meas_num: int,
    ) -> None:
        """
        Write out calibrated science frames.

        For polarized data, write out calibrated science frames for all 4 Stokes parameters.
        For non-polarized data, write out calibrated science frames for Stokes I only.

        Parameters
        ----------
        calibrated_object
            Corrected frames object

        map_scan
            The current map scan. Needed because it's not a header key

        meas_num
            The current measurement number
        """
        if self.constants.correct_for_polarization:
            stokes_targets = self.constants.stokes_params
        else:
            stokes_targets = self.constants.stokes_I_list
        for i, stokes_param in enumerate(stokes_targets):
            final_data = self._re_dummy_data(calibrated_object.data[:, :, i])
            final_header = self._update_calibrated_header(
                calibrated_object.header, map_scan=map_scan
            )
            self.write_cal_array(
                data=final_data,
                header=final_header,
                stokes=stokes_param,
                meas_num=meas_num,
                scan_step=calibrated_object.scan_step,
                map_scan=map_scan,
            )

    def correct_single_frame(
        self,
        beam: int,
        modstate: int,
        meas_num: int,
        scan_step: int,
        map_scan: int,
        exp_time: float,
        calibrations: CalibrationCollection,
    ) -> tuple[np.ndarray, fits.Header]:
        """
        Apply basic corrections to a single frame.

        Generally the algorithm is:
            1. Dark correct the array
            2. Solar Gain correct the array
            3. Geo correct the array
            4. Spectral correct array

        Parameters
        ----------
        modstate
            The modulator state for this single step
        scan_step
            The slit step for this single step
        map_scan
            The current map scan
        exp_time
            The exposure time for this single step
        calibrations
            Collection of all calibration objects

        Returns
        -------
            Corrected array, header
        """
        # Extract calibrations
        dark_array = calibrations.dark[CryonirspTag.beam(beam)][
            CryonirspTag.exposure_time(exp_time)
        ]
        gain_array = calibrations.solar_gain[CryonirspTag.beam(beam)]

        # Grab the input observe frame(s)
        observe_object_list = list(
            self.linearized_frame_observe_fits_access_generator(
                beam=beam,
                map_scan=map_scan,
                scan_step=scan_step,
                meas_num=meas_num,
                modstate=modstate,
                exposure_time=exp_time,
            )
        )
        # There can be more than 1 frame if there are sub-repeats
        observe_fits_access = sorted(
            [item for item in observe_object_list],
            key=lambda x: x.time_obs,
        )
        observe_arrays = [item.data for item in observe_fits_access]
        observe_headers = [item.header for item in observe_fits_access]

        # Average over sub-repeats, if there are any
        avg_observe_array = average_numpy_arrays(observe_arrays)
        # Get the header for this frame
        observe_header = observe_headers[0]

        # Dark correction
        dark_corrected_array = next(subtract_array_from_arrays(avg_observe_array, dark_array))

        # TODO: Unclear how much this helps, so leaving it out for now...
        # TODO: Do not remove this code until we have confirmed with the cryo team
        # Bad pixel correction
        # bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
        # bad_pixel_corrected_array = self.corrections_correct_bad_pixels(
        #     dark_corrected_array, bad_pixel_map
        # )

        # Gain correction
        # gain_corrected_array = next(divide_arrays_by_array(bad_pixel_corrected_array, gain_array))
        gain_corrected_array = next(divide_arrays_by_array(dark_corrected_array, gain_array))

        return gain_corrected_array, observe_header

    @staticmethod
    def polarization_correction(array_stack: np.ndarray, demod_matrices: np.ndarray) -> np.ndarray:
        """
        Apply a polarization correction to an array by multiplying the array stack by the demod matrices.

        Parameters
        ----------
        array_stack : np.ndarray
            (x, y, M) stack of corrected arrays with M modulation states

        demod_matrices : np.ndarray
            (x, y, 4, M) stack of demodulation matrices with 4 stokes planes and M modulation states


        Returns
        -------
        np.ndarray
            (x, y, 4) ndarray with the planes being IQUV
        """
        demodulated_array = np.sum(demod_matrices * array_stack[:, :, None, :], axis=3)
        return demodulated_array

    def telescope_polarization_correction(
        self,
        inst_demod_obj: CryonirspL0FitsAccess,
    ) -> CryonirspL0FitsAccess:
        """
        Apply a telescope polarization correction.

        Parameters
        ----------
        inst_demod_obj
            A demodulated, beam averaged frame

        Returns
        -------
        FitsAccess object with telescope corrections applied
        """
        tm = Telescope.from_fits_access(inst_demod_obj)
        mueller_matrix = tm.generate_inverse_telescope_model(M12=True)
        inst_demod_obj.data = self.polarization_correction(inst_demod_obj.data, mueller_matrix)
        return inst_demod_obj

    @staticmethod
    def _compute_date_keys(headers: Iterable[fits.Header] | fits.Header) -> fits.Header:
        """
        Generate correct DATE-??? header keys from a set of input headers.

        Keys are computed thusly:
        * DATE-BEG - The (Spec-0122) DATE-OBS of the earliest input header
        * DATE-END - The (Spec-0122) DATE-OBS of the latest input header, plus the FPA exposure time

        Returns
        -------
        fits.Header
            A copy of the earliest header, but with correct DATE-??? keys
        """
        if isinstance(headers, fits.Header) or isinstance(
            headers, fits.hdu.compressed.CompImageHeader
        ):
            headers = [headers]

        sorted_obj_list = sorted(
            [CryonirspL0FitsAccess.from_header(h) for h in headers], key=lambda x: Time(x.time_obs)
        )
        date_beg = sorted_obj_list[0].time_obs
        exp_time = TimeDelta(sorted_obj_list[-1].fpa_exposure_time_ms / 1000.0, format="sec")
        date_end = (Time(sorted_obj_list[-1].time_obs) + exp_time).isot

        header = sorted_obj_list[0].header
        header["DATE-BEG"] = date_beg
        header["DATE-END"] = date_end

        return header

    def _re_dummy_data(self, data: np.ndarray):
        """
        Add the dummy dimension that we have been secretly squeezing out during processing.

        The dummy dimension is required because its corresponding WCS axis contains important information.

        Parameters
        ----------
        data : np.ndarray
            Corrected data
        """
        logger.info(f"Adding dummy WCS dimension to array with shape {data.shape}")
        return data[None, :, :]

    def _update_calibrated_header(self, header: fits.Header, map_scan: int) -> fits.Header:
        """
        Update calibrated headers with any information gleaned during science calibration.

        Right now all this does is put map scan values in the header.

        Parameters
        ----------
        header
            The header to update

        map_scan
            Current map scan

        Returns
        -------
        fits.Header
        """
        # Correct the headers for the number of map_scans due to potential observation aborts
        header["CNNMAPS"] = self.constants.num_map_scans
        header["CNMAP"] = map_scan

        return header

    def write_cal_array(
        self,
        data: np.ndarray,
        header: fits.Header,
        stokes: str,
        meas_num: int,
        scan_step: int,
        map_scan: int,
    ) -> None:
        """
        Write out calibrated array.

        Parameters
        ----------
        data : np.ndarray
            calibrated data to write out

        header : fits.Header
            calibrated header to write out

        stokes : str
            Stokes parameter of this step. 'I', 'Q', 'U', or 'V'

        meas_num: int
            The current measurement number

        scan_step : int
            The slit step for this step

        map_scan : int
            The current map scan


        Returns
        -------
        None
        """
        tags = [
            CryonirspTag.calibrated(),
            CryonirspTag.frame(),
            CryonirspTag.stokes(stokes),
            CryonirspTag.meas_num(meas_num),
            CryonirspTag.scan_step(scan_step),
            CryonirspTag.map_scan(map_scan),
        ]
        hdul = fits.HDUList([fits.PrimaryHDU(), fits.CompImageHDU(header=header, data=data)])
        self.fits_data_write(hdu_list=hdul, tags=tags)

        filename = next(self.read(tags=tags))
        logger.info(f"Wrote intermediate file for {tags = } to {filename}")
