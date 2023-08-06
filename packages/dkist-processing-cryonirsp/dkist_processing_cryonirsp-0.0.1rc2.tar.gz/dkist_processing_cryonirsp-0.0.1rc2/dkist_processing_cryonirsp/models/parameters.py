"""CryoNIRSP calibration pipeline parameters."""
from functools import cached_property
from typing import Any

import numpy as np
from dkist_processing_common.models.parameters import ParameterBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetParameterValue
from logging42 import logger


class CryonirspParameters(ParameterBase):
    """Put all CryoNIRSP parameters parsed from the input dataset document in a single property."""

    def __init__(
        self,
        input_dataset_parameters: dict[str, list[InputDatasetParameterValue]],
        wavelength: float | None = None,
    ):
        super().__init__(input_dataset_parameters)
        self._wavelength = wavelength

    @property
    def geo_upsample_factor(self) -> float:
        """Pixel precision (1/upsample_factor) to use during phase matching of beam/modulator images."""
        return self._find_most_recent_past_value("cryonirsp_geo_upsample_factor")

    @property
    def geo_max_shift(self) -> float:
        """Max allowed pixel shift when computing spectral curvature."""
        return self._find_most_recent_past_value("cryonirsp_geo_max_shift")

    @property
    def geo_poly_fit_order(self) -> int:
        """Order of polynomial used to fit spectral shift as a function of slit position."""
        return self._find_most_recent_past_value("cryonirsp_geo_poly_fit_order")

    @property
    def geo_gradient_displacement(self) -> int:
        """Number of pixels to shift by when computing gradient."""
        return self._find_most_recent_past_value("cryonirsp_geo_gradient_displacement")

    @property
    def geo_strip_spatial_length_divisor(self) -> int:
        """Divisor applied to the array spatial axis size to compute the strip length."""
        return self._find_most_recent_past_value("cryonirsp_geo_strip_spatial_length_divisor")

    @property
    def geo_strip_spectral_width_divisor(self) -> int:
        """Divisor applied to the array width to compute the vertical strip width."""
        return self._find_most_recent_past_value("cryonirsp_geo_strip_spectral_width_divisor")

    @property
    def geo_strip_spectral_offset_divisor(self) -> int:
        """Divisor applied to the array width to compute the vertical strip half-offset."""
        return self._find_most_recent_past_value("cryonirsp_geo_strip_spectral_offset_divisor")

    @property
    def solar_spectral_avg_window(self):
        """Pixel sigma of Gaussian kernel used to compute characteristic solar spectra."""
        return self._find_parameter_closest_wavelength("cryonirsp_solar_spectral_avg_window")

    @property
    def solar_zone_prominence(self):
        """Relative peak prominence threshold used to identify strong spectral features."""
        return self._find_parameter_closest_wavelength("cryonirsp_solar_zone_prominence")

    @property
    def solar_zone_width(self):
        """Pixel width used to search for strong spectral features."""
        return self._find_parameter_closest_wavelength("cryonirsp_solar_zone_width")

    @property
    def solar_zone_bg_order(self):
        """Order of polynomial fit used to remove continuum when identifying strong spectral features."""
        return self._find_parameter_closest_wavelength("cryonirsp_solar_zone_bg_order")

    @property
    def solar_zone_normalization_percentile(self):
        """Fraction of CDF to use for normalzing spectrum when search for strong features."""
        return self._find_parameter_closest_wavelength(
            "cryonirsp_solar_zone_normalization_percentile"
        )

    @property
    def solar_zone_rel_height(self):
        """Relative height at which to compute the width of strong spectral features."""
        return self._find_most_recent_past_value("cryonirsp_solar_zone_rel_height")

    @property
    def polcal_num_spectral_bins(self) -> int:
        """Return Number of demodulation matrices to compute across the entire FOV in the spectral dimension."""
        return self._find_most_recent_past_value("cryonirsp_polcal_num_spectral_bins")

    @property
    def polcal_num_spatial_bins(self) -> int:
        """Return Number of demodulation matrices to compute across the entire FOV in the spatial dimension."""
        return self._find_most_recent_past_value("cryonirsp_polcal_num_spatial_bins")

    @property
    def max_cs_step_time_sec(self):
        """Time window within which CS steps with identical GOS configurations are considered to be the same."""
        return self._find_most_recent_past_value("cryonirsp_max_cs_step_time_sec")

    @property
    def polcal_pac_fit_mode(self):
        """Name of set of fitting flags to use during PAC Calibration Unit parameter fits."""
        return self._find_most_recent_past_value("cryonirsp_polcal_pac_fit_mode")

    @property
    def polcal_pac_init_set(self):
        """Name of set of initial values for Calibration Unit parameter fit."""
        return self._find_most_recent_past_value("cryonirsp_polcal_pac_init_set")

    @property
    def beam_boundaries_smoothing_disk_size(self) -> int:
        """Return the size of the smoothing disk (in pixels) to be used in the beam boundaries computation."""
        return self._find_most_recent_past_value("cryonirsp_beam_boundaries_smoothing_disk_size")

    @property
    def beam_boundaries_upsample_factor(self) -> int:
        """Return the upsample factor to be used in the beam boundaries cross correlation computation."""
        return self._find_most_recent_past_value("cryonirsp_beam_boundaries_upsample_factor")

    @property
    def bad_pixel_map_median_filter_size(self) -> int:
        """Return the smoothing disk size to be used in the bad pixel map computation."""
        return self._find_most_recent_past_value("cryonirsp_bad_pixel_map_median_filter_size")

    @property
    def bad_pixel_map_threshold_factor(self) -> float:
        """Return the threshold multiplicative factor to be used in the bad pixel map computation."""
        return self._find_most_recent_past_value("cryonirsp_bad_pixel_map_threshold_factor")

    @property
    def bad_pixel_correction_median_filter_size(self) -> int:
        """Return the size of the median filter to be used for bad pixel correction."""
        return self._find_most_recent_past_value(
            "cryonirsp_bad_pixel_correction_median_filter_size"
        )

    @cached_property
    def ci_thresholds(self) -> np.ndarray:
        """Name of parameter associated with the CI linearization thresholds."""
        param_dict = self._find_most_recent_past_value("cryonirsp_ci_thresholds")
        return self._get_param_data_from_npy_file(param_dict)

    @cached_property
    def ci_polyfit(self) -> np.ndarray:
        """Name of parameter associated with the CI linearization polyfit coefficients."""
        param_dict = self._find_most_recent_past_value("cryonirsp_ci_polyfit")
        return self._get_param_data_from_npy_file(param_dict)

    @cached_property
    def sp_thresholds(self) -> np.ndarray:
        """Name of parameter associated with the SP linearization thresholds."""
        param_dict = self._find_most_recent_past_value("cryonirsp_sp_thresholds")
        return self._get_param_data_from_npy_file(param_dict)

    @cached_property
    def sp_polyfit(self) -> np.ndarray:
        """Name of parameter associated with the SP linearization polyfit coefficients."""
        param_dict = self._find_most_recent_past_value("cryonirsp_sp_polyfit")
        return self._get_param_data_from_npy_file(param_dict)

    def _find_parameter_closest_wavelength(self, parameter_name: str) -> Any:
        """
        Find the database value for a parameter that is closest to the requested wavelength.

        NOTE: If the requested wavelength is exactly between two database values, the value from the smaller wavelength
        will be returned
        """
        if self._wavelength is None:
            raise ValueError(
                f"Cannot get wavelength dependent parameter {parameter_name} without wavelength"
            )

        parameter_dict = self._find_most_recent_past_value(parameter_name)
        wavelengths = np.array(parameter_dict["wavelength"])
        values = parameter_dict["values"]
        idx = np.argmin(np.abs(wavelengths - self._wavelength))
        chosen_wave = wavelengths[idx]
        chosen_value = values[idx]
        logger.info(
            f"Choosing {parameter_name} = {chosen_value} from {chosen_wave = } (requested {self._wavelength})"
        )
        return chosen_value

    @staticmethod
    def _get_param_data_from_npy_file(param_dict: dict) -> np.ndarray:
        """Return the data associated with a parameter file saved in numpy format."""
        file_path = param_dict["param_path"]
        result = np.load(file_path)
        return result
