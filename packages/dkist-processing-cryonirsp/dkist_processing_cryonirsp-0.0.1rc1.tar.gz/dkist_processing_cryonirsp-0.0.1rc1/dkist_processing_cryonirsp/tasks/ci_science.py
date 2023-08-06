"""Cryonirsp science calibration task."""
from astropy.io import fits
from logging42 import logger

from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.tasks.science_base import CalibrationCollection
from dkist_processing_cryonirsp.tasks.science_base import ScienceCalibrationBase


class CIScienceCalibration(ScienceCalibrationBase):
    """Task class for Cryonirsp CI science calibration of polarized and non-polarized data."""

    def process_frames(self, calibrations: CalibrationCollection):
        """
        Completely calibrate all science frames.

        - Apply dark and gain corrections
        - Demodulate if needed
        - Apply telescope correction, if needed
        - Write calibrated arrays
        """
        # Using variables here to avoid hard-coding anywhere below
        beam = 1
        modstate = 1
        for exp_time in self.constants.observe_exposure_times:
            for map_scan in range(1, self.constants.num_map_scans + 1):
                for scan_step in range(1, self.constants.num_scan_steps + 1):
                    for meas_num in range(1, self.constants.num_meas + 1):
                        # If the number of beams ever changes we can add a loop here...
                        apm_str = f"{exp_time = }, {map_scan = }, {scan_step = } and {meas_num = }"
                        with self.apm_processing_step(f"Basic corrections for {apm_str}"):
                            # Initialize array_stack and headers
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
                                # Note: this assumes only a single frame per measurement and modstate == 1
                                logger.info(f"Processing Stokes-I observe frames from {apm_str}")
                                result = self.correct_single_frame(
                                    beam=beam,
                                    modstate=modstate,
                                    meas_num=meas_num,
                                    scan_step=scan_step,
                                    map_scan=map_scan,
                                    exp_time=exp_time,
                                    calibrations=calibrations,
                                )
                                intermediate_array, intermediate_header = result
                                intermediate_header = self._compute_date_keys(intermediate_header)
                                # Add a "stokes" dimension so later loops work as expected
                                intermediate_array = intermediate_array[:, :, None]

                            # Create a FitsL0Access object for this frame
                            hdu = fits.ImageHDU(data=intermediate_array, header=intermediate_header)
                            calibrated = CryonirspL0FitsAccess(hdu=hdu, auto_squeeze=False)

                        if self.constants.correct_for_polarization:
                            with self.apm_processing_step("Correcting telescope polarization"):
                                logger.info("Correcting telescope polarization")
                                calibrated = self.telescope_polarization_correction(calibrated)

                        # Save the final output files
                        with self.apm_writing_step("Writing calibrated arrays"):
                            logger.info("Writing calibrated arrays")
                            self.write_calibrated_array(
                                calibrated, map_scan=map_scan, meas_num=meas_num
                            )
