"""Cryo spectral line list."""
from dkist_processing_common.models.spectral_line import SpectralLine

CRYO_SP_SPECTRAL_LINES = [
    SpectralLine(name="Ca II", wavelength=854.000, wavemin=848.000, wavemax=860.000),
    SpectralLine(name="He I, Fe XIII", wavelength=1077.000, wavemin=1067.000, wavemax=1087.000),
    SpectralLine(name="S IX", wavelength=1252.000, wavemin=1238.500, wavemax=1265.500),
    SpectralLine(name="H Paschen-beta", wavelength=1282.000, wavemin=1268.000, wavemax=1296.000),
    SpectralLine(name="Si X", wavelength=1430.000, wavemin=1412.500, wavemax=1447.500),
    SpectralLine(name="Fe XII", wavelength=2218.000, wavemin=2196.500, wavemax=2239.500),
    SpectralLine(name="Mg VIII", wavelength=3028.000, wavemin=2993.000, wavemax=3063.000),
    SpectralLine(name="Si IX", wavelength=3934.000, wavemin=3872.000, wavemax=3996.000),
    SpectralLine(name="CO", wavelength=4651.000, wavemin=4565.500, wavemax=4736.500),
]

CRYO_CI_SPECTRAL_LINES = [
    SpectralLine(name="Continuum", wavelength=1049.500, wavemin=1049.000, wavemax=1050.000),
    SpectralLine(name="Fe XIII", wavelength=1074.700, wavemin=1074.200, wavemax=1075.200),
    SpectralLine(name="Fe XIII", wavelength=1079.800, wavemin=1079.300, wavemax=1080.300),
    SpectralLine(name="He I", wavelength=1083.000, wavemin=1082.500, wavemax=1083.500),
    SpectralLine(name="H Paschen-beta", wavelength=1281.800, wavemin=1281.300, wavemax=1282.300),
    SpectralLine(name="J Band", wavelength=1250.000, wavemin=1170.000, wavemax=1330.000),
    SpectralLine(name="Si X", wavelength=1430.000, wavemin=1427.500, wavemax=1432.500),
]
