"""Cryonirsp make movie frames task."""
import numpy as np
from astropy.io import fits
from astropy.visualization import ZScaleInterval
from dkist_processing_common.models.fits_access import FitsAccessBase
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l1_fits_access import CryonirspL1FitsAccess
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class CIMakeCryonirspMovieFrames(CryonirspTaskBase):
    """
    Make CryoNIRSP movie frames and tag with CryonirspTag.movie_frame().

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
        Execute the task.

        For each stokes state.
            For each map map_scan
              - Each scan step is one frame in the movie
              - Each scan step has either a single Stokes-I frame or a set of IQUV frames
              - For Stokes-I, each frame is a "MOVIE_FRAME"
              - For IQUV, each frame is one quadrant of a composite "MOVIE_FRAME"
              - Write the "MOVIE_FRAME"

        Returns
        -------
        None
        """
        is_polarized = False
        stokes_states = ["I", "Q", "U", "V"]
        # Loop over the number of dsps repeats
        for map_scan in range(1, self.constants.num_map_scans + 1):
            meas_num = 1  # Use only the first measurement if there are multiple measurements.
            instrument_set = set()
            wavelength_set = set()
            time_obs = []
            # Each scan step corresponds to a single movie frame
            for scan_step in range(1, self.constants.num_scan_steps + 1):
                with self.apm_processing_step(
                    f"Making movie frame for {map_scan = } and {scan_step = }"
                ):
                    logger.info(f"Making movie frame for {map_scan = } and {scan_step = }")
                    # Loop over the stokes states to add them to the frame array
                    for stokes_state in stokes_states:
                        stokes_paths = list(
                            self.read(
                                tags=[
                                    CryonirspTag.frame(),
                                    CryonirspTag.output(),
                                    CryonirspTag.stokes(stokes_state),
                                ]
                            )
                        )
                        if len(stokes_paths) > 0:
                            calibrated_frame = next(
                                self.fits_data_read_fits_access(
                                    tags=[
                                        CryonirspTag.frame(),
                                        CryonirspTag.output(),
                                        CryonirspTag.stokes(stokes_state),
                                        CryonirspTag.meas_num(meas_num),
                                        CryonirspTag.map_scan(map_scan),
                                        CryonirspTag.scan_step(scan_step),
                                    ],
                                    cls=CryonirspL1FitsAccess,
                                )
                            )
                            stokes_frame_data = calibrated_frame.data
                            # Grab the relevant header info from the frame
                            instrument_set.add(calibrated_frame.instrument)
                            wavelength_set.add(calibrated_frame.wavelength)
                            time_obs.append(calibrated_frame.time_obs)

                            # Encode the data as a specific stokes state
                            if stokes_state == "I":
                                stokes_i_data = stokes_frame_data
                            if stokes_state == "Q":
                                is_polarized = True
                                stokes_q_data = stokes_frame_data
                            if stokes_state == "U":
                                is_polarized = True
                                stokes_u_data = stokes_frame_data
                            if stokes_state == "V":
                                is_polarized = True
                                stokes_v_data = stokes_frame_data

                    # Use the most recently read header as the base header because we need to be able to read it
                    # with CryonirspL1FitsAccess. We'll update the values we actually care about below.
                    header = fits.Header(calibrated_frame.header)

                    # Make sure only one instrument value was found
                    if len(instrument_set) != 1:
                        raise ValueError(
                            f"There should only be one instrument value in the headers. "
                            f"Found {len(instrument_set)}: {instrument_set=}"
                        )
                    header["INSTRUME"] = instrument_set.pop()
                    # The timestamp of a movie frame will be the time of the scan start
                    header["DATE-BEG"] = time_obs[0]
                    # Make sure only one wavelength value was found
                    if len(wavelength_set) != 1:
                        raise ValueError(
                            f"There should only be one wavelength value in the headers. "
                            f"Found {len(wavelength_set)}: {wavelength_set=}"
                        )
                    header["LINEWAV"] = wavelength_set.pop()
                    # Write the movie frame file to disk and tag it, normalizing across stokes intensities
                    if is_polarized:
                        i_norm = ZScaleInterval()(stokes_i_data)
                        q_norm = ZScaleInterval()(stokes_q_data)
                        u_norm = ZScaleInterval()(stokes_u_data)
                        v_norm = ZScaleInterval()(stokes_v_data)
                        movie_frame_data = np.concatenate(
                            (
                                np.concatenate((i_norm, q_norm), axis=1),
                                np.concatenate((u_norm, v_norm), axis=1),
                            ),
                            axis=0,
                        )
                    else:
                        movie_frame_data = stokes_i_data

                with self.apm_writing_step(
                    f"Writing movie frame for {map_scan = } and {scan_step = }"
                ):
                    logger.info(f"Writing movie frame for {map_scan = } and {scan_step = }")
                    self.fits_data_write(
                        hdu_list=fits.HDUList(
                            [fits.PrimaryHDU(header=header, data=np.asarray(movie_frame_data))]
                        ),
                        tags=[
                            CryonirspTag.map_scan(map_scan),
                            CryonirspTag.scan_step(scan_step),
                            CryonirspTag.movie_frame(),
                        ],
                    )
