"""Cryonirsp quality metrics task."""
from dataclasses import dataclass
from dataclasses import field

import numpy as np
from astropy.time import Time
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks import QualityL0Metrics
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from logging42 import logger

from dkist_processing_cryonirsp.models.constants import CryonirspConstants
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


@dataclass
class _QualitySensitivityData:
    """Class for storage of Cryonirsp polarimetric sensitivity quality data."""

    datetimes: list[str] = field(default_factory=list)
    I_sensitivity: list[float] = field(default_factory=list)
    Q_sensitivity: list[float] = field(default_factory=list)
    U_sensitivity: list[float] = field(default_factory=list)
    V_sensitivity: list[float] = field(default_factory=list)


@dataclass
class _QualityTaskTypeData:
    """Class for storage of Cryonirsp quality task type data."""

    quality_task_type: str
    average_values: list[float] = field(default_factory=list)
    rms_values_across_frame: list[float] = field(default_factory=list)
    datetimes: list[str] = field(default_factory=list)

    @property
    def has_values(self) -> bool:
        return bool(self.average_values)


class CryonirspL0QualityMetrics(QualityL0Metrics):
    """
    Task class for collection of Cryonirsp L0 specific quality metrics.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def constants_model_class(self):
        """Class for Cryonirsp constants."""
        return CryonirspConstants

    def run(self) -> None:
        """Calculate L0 metrics for Cryonirsp data."""
        if not self.constants.correct_for_polarization:
            paths = self.read(tags=[CryonirspTag.linearized()])
            self.calculate_l0_metrics(paths=paths)
        else:
            for m in range(1, self.constants.num_modstates + 1):
                with self.apm_task_step(f"Working on modstate {m}"):
                    paths = self.read(tags=[CryonirspTag.linearized(), CryonirspTag.modstate(m)])
                    self.calculate_l0_metrics(paths=paths, modstate=m)


class CryonirspL1QualityMetrics(CryonirspTaskBase, QualityMixin):
    """
    Task class for collection of Cryonirsp L1 specific quality metrics.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def run(self) -> None:
        """
        For each spectral scan.

            - Gather stokes data
            - Find Stokes Q, U, and V RMS noise
            - Find the polarimetric sensitivity (smallest intensity signal measured)
            - Send metrics for storage

        """
        self.compute_sensitivity()
        self.compute_noise()

    def compute_sensitivity(self) -> None:
        """Compute RMS noise and sensitivity estimate for L1 Cryonirsp frames."""
        with self.apm_processing_step("Calculating polarization metrics"):
            all_datetimes = []
            all_I_sensitivity = []
            all_Q_sensitivity = []
            all_U_sensitivity = []
            all_V_sensitivity = []
            for map_scan in range(1, self.constants.num_map_scans + 1):
                polarization_data = _QualitySensitivityData()
                poldata_noise_list_list = [
                    polarization_data.I_sensitivity,
                    polarization_data.Q_sensitivity,
                    polarization_data.U_sensitivity,
                    polarization_data.V_sensitivity,
                ]
                for step in range(1, self.constants.num_scan_steps + 1):
                    # grab stokes I data
                    stokesI_frame = next(
                        self.fits_data_read_fits_access(
                            tags=[
                                # CryonirspTag.calibrated(),
                                CryonirspTag.output(),
                                CryonirspTag.frame(),
                                CryonirspTag.scan_step(step),
                                CryonirspTag.map_scan(map_scan),
                                CryonirspTag.stokes("I"),
                                # Grab only the first measurement
                                CryonirspTag.meas_num(1),
                            ],
                            cls=L1QualityFitsAccess,
                        )
                    )
                    stokesI_med = np.nanmedian(stokesI_frame.data)
                    # TODO: Band-Aid to fix problem where median is zero
                    if stokesI_med == 0:
                        stokesI_med = np.nanmean(stokesI_frame.data)
                    polarization_data.datetimes.append(Time(stokesI_frame.time_obs).mjd)

                    # grab other stokes data and find and store RMS noise
                    for stokes_param, data_list in zip(
                        ("I", "Q", "U", "V"), poldata_noise_list_list
                    ):
                        try:
                            stokes_frame = next(
                                self.fits_data_read_fits_access(
                                    tags=[
                                        CryonirspTag.output(),
                                        CryonirspTag.frame(),
                                        CryonirspTag.scan_step(step),
                                        CryonirspTag.map_scan(map_scan),
                                        CryonirspTag.stokes(stokes_param),
                                    ],
                                    cls=L1QualityFitsAccess,
                                )
                            )
                        except StopIteration:
                            # This stokes parameter doesn't exist. No big deal.
                            continue

                        # compute sensitivity for this Stokes parameter
                        data_list.append(np.std(stokes_frame.data) / stokesI_med)

                all_datetimes.append(Time(np.mean(polarization_data.datetimes), format="mjd").isot)
                for target, source in zip(
                    [all_I_sensitivity, all_Q_sensitivity, all_U_sensitivity, all_V_sensitivity],
                    poldata_noise_list_list,
                ):
                    if not source:
                        # Empty list means there are no data for this Stokes parameter
                        continue
                    target.append(np.mean(source))

        with self.apm_step("Sending lists for storage"):
            for stokes_index, stokes_noise in zip(
                ("I", "Q", "U", "V"),
                (all_I_sensitivity, all_Q_sensitivity, all_U_sensitivity, all_V_sensitivity),
            ):
                if not stokes_noise:
                    continue
                self.quality_store_sensitivity(
                    stokes=stokes_index, datetimes=all_datetimes, values=stokes_noise
                )

    def compute_noise(self):
        """Compute noise in data."""
        with self.apm_processing_step("Calculating L1 Cryonirsp noise metrics"):
            for stokes in ["I", "Q", "U", "V"]:
                tags = [CryonirspTag.output(), CryonirspTag.frame(), CryonirspTag.stokes(stokes)]
                if self.scratch.count_all(tags=tags) > 0:
                    frames = self.fits_data_read_fits_access(
                        tags=tags,
                        cls=L1QualityFitsAccess,
                    )
                    noise_values = []
                    datetimes = []
                    for frame in frames:
                        noise_values.append(self.avg_noise(frame.data))
                        datetimes.append(frame.time_obs)
                    self.quality_store_noise(
                        datetimes=datetimes, values=noise_values, stokes=stokes
                    )
