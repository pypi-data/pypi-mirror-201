"""Cryo science calibration task."""
from collections import defaultdict

import numpy as np
from astropy.io import fits
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.tasks.science_base import CalibrationCollection
from dkist_processing_cryonirsp.tasks.science_base import ScienceCalibrationBase


class SPScienceCalibration(ScienceCalibrationBase):
    """Task class for SP Cryo science calibration of polarized and non-polarized data."""

    def process_frames(self, calibrations: CalibrationCollection):
        """
        Completely calibrate all science frames.

        - Apply all dark, gain, geometric corrections
        - Demodulate if needed
        - Apply telescope correction, if needed
        - Write calibrated arrays
        """
        for exp_time in self.constants.observe_exposure_times:
            for map_scan in range(1, self.constants.num_map_scans + 1):
                for scan_step in range(1, self.constants.num_scan_steps + 1):
                    for meas_num in range(1, self.constants.num_meas + 1):
                        beam_storage = dict()
                        header_storage = dict()
                        for beam in range(1, self.constants.num_beams + 1):
                            apm_str = f"{exp_time = }, {map_scan = }, {scan_step = }, {meas_num = } and {beam = }"
                            with self.apm_processing_step(f"Basic corrections for {apm_str}"):
                                if self.constants.correct_for_polarization:
                                    logger.info(
                                        f"Processing polarimetric observe frames from {apm_str}"
                                    )
                                    result = self.process_polarimetric_modstates(
                                        beam=beam,
                                        meas_num=meas_num,
                                        scan_step=scan_step,
                                        map_scan=map_scan,
                                        exp_time=exp_time,
                                        calibrations=calibrations,
                                    )
                                    intermediate_array, intermediate_header = result

                                else:
                                    logger.info(
                                        f"Processing Stokes-I observe frames from {apm_str}"
                                    )
                                    # Note: this assumes only a single frame per measurement and modstate == 1
                                    result = self.correct_single_frame(
                                        beam=beam,
                                        modstate=1,
                                        meas_num=meas_num,
                                        scan_step=scan_step,
                                        map_scan=map_scan,
                                        exp_time=exp_time,
                                        calibrations=calibrations,
                                    )
                                    intermediate_array, intermediate_header = result
                                    intermediate_header = self._compute_date_keys(
                                        intermediate_header
                                    )
                                    # Add a "stokes" dimension so later loops work as expected
                                    intermediate_array = intermediate_array[:, :, None]

                                # At this point we have a 3D stokes stack of basic corrected arrays
                                # Now we need to apply geo and spectral corrections to each array in the stack
                                fully_corrected_array = np.zeros_like(intermediate_array)

                                num_states = intermediate_array.shape[-1]
                                # Do the geo correction
                                for i in range(num_states):
                                    geo_corrected_array = next(
                                        self.corrections_correct_geometry(
                                            intermediate_array[:, :, i],
                                            calibrations.state_offset[CryonirspTag.beam(beam)],
                                            calibrations.angle[CryonirspTag.beam(beam)],
                                        )
                                    )
                                    # Now correct the spectral curvature
                                    spectral_corrected_array = next(
                                        self.corrections_remove_spec_geometry(
                                            geo_corrected_array,
                                            calibrations.spec_shift[CryonirspTag.beam(beam)],
                                        )
                                    )
                                    # Insert the result into the fully corrected array stack
                                    fully_corrected_array[:, :, i] = spectral_corrected_array

                                beam_storage[CryonirspTag.beam(beam)] = fully_corrected_array
                                header_storage[CryonirspTag.beam(beam)] = intermediate_header

                        with self.apm_processing_step("Combining beams"):
                            logger.info("Combining beams")
                            combined = self.combine_beams(beam_storage, header_storage)

                        if self.constants.correct_for_polarization:
                            with self.apm_processing_step("Correcting telescope polarization"):
                                logger.info("Correcting telescope polarization")
                                calibrated = self.telescope_polarization_correction(combined)
                        else:
                            calibrated = combined

                        if self.constants.correct_for_polarization:
                            calibrated = self.remove_crosstalk(calibrated)

                        # Save the final output file
                        with self.apm_writing_step("Writing calibrated array"):
                            logger.info("Writing calibrated array")
                            self.write_calibrated_array(
                                calibrated, map_scan=map_scan, meas_num=meas_num
                            )

    def combine_beams(self, array_dict: dict, header_dict: dict) -> CryonirspL0FitsAccess:
        """
        Average all beams together.

        Also complain if the inputs are strange.
        """
        headers = list(header_dict.values())
        if len(headers) == 0:
            raise ValueError("No headers provided")
        for h in headers[1:]:
            if fits.HeaderDiff(headers[0], h):
                raise ValueError("Headers are different! This should NEVER happen!")

        array_list = []
        for beam in range(1, self.constants.num_beams + 1):
            array_list.append(array_dict[CryonirspTag.beam(beam)])

        avg_array = average_numpy_arrays(array_list)

        hdu = fits.ImageHDU(data=avg_array, header=headers[0])
        obj = CryonirspL0FitsAccess(hdu=hdu, auto_squeeze=False)

        return obj

    @staticmethod
    def remove_crosstalk(fits_obj: CryonirspL0FitsAccess) -> CryonirspL0FitsAccess:
        """Remove the continuum from QUV (remove cross-talk)."""
        array_stack = fits_obj.data
        array_header = fits_obj.header
        for i in range(1, 4):
            array_stack[:, :, i] = (
                array_stack[:, :, i]
                - np.nanmedian(array_stack[:, :, i] / array_stack[:, :, 0], axis=1)[:, None]
                * array_stack[:, :, 0]
            )
        hdu = fits.ImageHDU(data=array_stack, header=array_header)
        obj = CryonirspL0FitsAccess(hdu=hdu, auto_squeeze=False)
        return obj
