"""Cryo spectral line parser."""
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.spectral_line import find_associated_line
from dkist_processing_common.parsers.unique_bud import UniqueBud

from dkist_processing_cryonirsp.models.spectral_line import CRYO_CI_SPECTRAL_LINES
from dkist_processing_cryonirsp.models.spectral_line import CRYO_SP_SPECTRAL_LINES
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


class SpectralLineBud(UniqueBud):
    """Get spectral line wavelengths from file metadata."""

    def __init__(self):
        super().__init__(constant_name=BudName.spectral_line.value, metadata_key="wavelength")

    def setter(self, fits_obj: CryonirspL0FitsAccess):
        """
        Given a list of SpectralLine objects, find the one that contains the wavelength of the frame within its range, and return its name for observe frames only.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        if fits_obj.arm_id == "SP":
            return find_associated_line(
                wavelength=fits_obj.wavelength, lines=CRYO_SP_SPECTRAL_LINES
            )
        if fits_obj.arm_id == "CI":
            return find_associated_line(
                wavelength=fits_obj.wavelength, lines=CRYO_CI_SPECTRAL_LINES
            )
