"""Helper to manage raw input data."""
from collections.abc import Generator

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspRampFitsAccess


class InputFrameMixin:
    """Mixin for methods that support easy loading of input frames."""

    def input_frame_fits_access_generator(
        self,
        time_obs: str,
    ) -> Generator[CryonirspRampFitsAccess, None, None]:
        """
        Return a fits access generator of raw input frames based on time-obs.

        A single time-obs should correspond to a single ramp.
        """
        tags = [CryonirspTag.input(), CryonirspTag.frame(), CryonirspTag.time_obs(time_obs)]

        frame_generator = self.fits_data_read_fits_access(tags, cls=CryonirspRampFitsAccess)
        return frame_generator
