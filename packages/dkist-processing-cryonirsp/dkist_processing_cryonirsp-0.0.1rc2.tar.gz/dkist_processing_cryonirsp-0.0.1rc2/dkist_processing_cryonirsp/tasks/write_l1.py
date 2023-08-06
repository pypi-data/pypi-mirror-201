"""Cryonirsp write L1 task."""
from abc import ABC
from typing import Literal

from astropy.io import fits
from dkist_processing_common.tasks import WriteL1Frame
from logging42 import logger

from dkist_processing_cryonirsp.models.constants import CryonirspConstants


class CryonirspWriteL1Frame(WriteL1Frame, ABC):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

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
        """Get Cryonirsp pipeline constants."""
        return CryonirspConstants

    def l1_filename(self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]):
        """
        Use a FITS header to derive its filename in the following format.

        instrument_datetime_wavelength__stokes_datasetid__measno_L1.fits.

        Example
        -------
        "CRYONIRSP_2020_03_13T00_00_00_000_01080000_Q_DATID_2_L1.fits"

        Parameters
        ----------
        header
            The input fits header
        stokes
            The stokes parameter

        Returns
        -------
        The L1 filename
        """
        instrument = header["INSTRUME"]
        wavelength = str(round(header["LINEWAV"] * 1000)).zfill(8)
        datetime = header["DATE-BEG"].replace("-", "_").replace(":", "_").replace(".", "_")
        meas_num = header["CNCMEAS"]
        return f"{instrument}_{datetime}_{wavelength}_{stokes}_{self.constants.dataset_id}_{meas_num}_L1.fits"

    @staticmethod
    def _calculate_date_end(header: fits.Header) -> str:
        """
        In VISP, the instrument specific DATE-END keyword is calculated during science calibration.

        Check that it exists.

        Parameters
        ----------
        header
            The input fits header
        """
        try:
            return header["DATE-END"]
        except KeyError:
            raise KeyError(
                f"The 'DATE-END' keyword was not found. "
                f"Was supposed to be inserted during science calibration."
            )


class CIWriteL1Frame(CryonirspWriteL1Frame):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        """
        Add the Cryonirsp specific dataset headers to L1 FITS files.

        Parameters
        ----------
        header : fits.Header
            calibrated data header

        stokes :
            stokes parameter

        Returns
        -------
        fits.Header
            calibrated header with correctly written l1 headers
        """
        # Correct the headers for the number of map_scans due to potential observation aborts
        header["CNNMAPS"] = self.constants.num_map_scans

        if stokes.upper() not in self.constants.stokes_params:
            raise ValueError("The stokes parameter must be one of I, Q, U, V")

        # Dynamically assign dataset axes based on CTYPEs in the L0 headers
        axis_types = [
            self.constants.axis_1_type,  # HPLN-TAN
            self.constants.axis_2_type,  # HPLT-TAN
            self.constants.axis_3_type,  # AWAV
        ]
        for i, axis_type in enumerate(axis_types, start=1):
            if axis_type == "HPLN-TAN":  # axis 1
                header[f"DNAXIS{i}"] = header[f"NAXIS{i}"]
                header[f"DTYPE{i}"] = "SPATIAL"
                header[f"DPNAME{i}"] = "spatial-x"
                header[f"DWNAME{i}"] = "helioprojective longitude"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
            elif axis_type == "HPLT-TAN":  # axis 2
                header[f"DNAXIS{i}"] = header[f"NAXIS{i}"]
                header[f"DTYPE{i}"] = "SPATIAL"
                header[f"DPNAME{i}"] = "spatial-y"
                header[f"DWNAME{i}"] = "helioprojective latitude"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
            elif axis_type == "AWAV":  # axis 3
                header[f"DNAXIS{i}"] = header[f"NAXIS{i}"]
                header[f"DTYPE{i}"] = "SPECTRAL"
                header[f"DPNAME{i}"] = "dispersion axis"
                header[f"DWNAME{i}"] = "wavelength"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
                header[f"DINDEX{i}"] = 1  # There is only one wavelength...
                # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
                header["WAVEMIN"] = header[f"CRVAL{i}"] - (
                    header[f"CRPIX{i}"] * header[f"CDELT{i}"]
                )
                header["WAVEMAX"] = header[f"CRVAL{i}"] + (
                    (header[f"NAXIS{i}"] - header[f"CRPIX{i}"]) * header[f"CDELT{i}"]
                )
            else:
                raise ValueError(
                    f"Unexpected axis type. Expected ['HPLN-TAN', 'HPLT-TAN', 'AWAV']. Got {axis_type}"
                )

        # Set the base number of dataset axes to 3
        num_axis = 3

        # ---Temporal---
        if self.constants.num_map_scans > 1:
            num_axis += 1
            # Total number of scan steps in the entire dataset:
            header[f"DNAXIS{num_axis}"] = (
                self.constants.num_scan_steps * self.constants.num_map_scans
            )
            header[f"DTYPE{num_axis}"] = "TEMPORAL"
            header[f"DPNAME{num_axis}"] = "time"
            header[f"DWNAME{num_axis}"] = "time"
            header[f"DUNIT{num_axis}"] = "s"
            # Temporal position in dataset
            current_scan_step = header["CNCURSCN"]
            current_map_scan = header["DSPSNUM"]
            header[f"DINDEX{num_axis}"] = (
                current_map_scan - 1
            ) * self.constants.num_scan_steps + current_scan_step

        # ---Stokes---
        if self.constants.correct_for_polarization:
            num_axis += 1
            header[f"DNAXIS{num_axis}"] = 4  # I, Q, U, V
            header[f"DTYPE{num_axis}"] = "STOKES"
            header[f"DPNAME{num_axis}"] = "polarization state"
            header[f"DWNAME{num_axis}"] = "polarization state"
            header[f"DUNIT{num_axis}"] = ""
            # Stokes position in dataset - stokes axis goes from 1-4
            header[f"DINDEX{num_axis}"] = self.constants.stokes_params.index(stokes.upper()) + 1

        else:
            logger.info("Spectrographic data detected. Not adding DNAXIS information.")

        header["DNAXIS"] = num_axis
        header["DAAXES"] = 2  # Spatial, spatial
        header["DEAXES"] = num_axis - 2  # Total - detector axes

        header["LEVEL"] = 1
        header["WAVEBAND"] = self.constants.spectral_line
        header["WAVEUNIT"] = -9  # nanometers
        header["WAVEREF"] = "Air"
        # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
        header["WAVEMIN"] = header["CRVAL1"] - (header["CRPIX1"] * header["CDELT1"])
        header["WAVEMAX"] = header["CRVAL1"] + (
            (header["NAXIS1"] - header["CRPIX1"]) * header["CDELT1"]
        )

        # Binning headers
        header["NBIN1"] = 1
        header["NBIN2"] = 1
        header["NBIN3"] = 1
        header["NBIN"] = header["NBIN1"] * header["NBIN2"] * header["NBIN3"]

        return header


class SPWriteL1Frame(CryonirspWriteL1Frame):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        """
        Add the Cryonirsp specific dataset headers to L1 FITS files.

        Parameters
        ----------
        header : fits.Header
            calibrated data header

        stokes :
            stokes parameter

        Returns
        -------
        fits.Header
            calibrated header with correctly written l1 headers
        """
        # Correct the headers for the number of map_scans due to potential observation aborts
        header["CNNMAPS"] = self.constants.num_map_scans

        if stokes.upper() not in self.constants.stokes_params:
            raise ValueError("The stokes parameter must be one of I, Q, U, V")

        # Dynamically assign dataset axes based on CTYPEs in the L0 headers
        axis_types = [
            self.constants.axis_1_type,  # AWAV
            self.constants.axis_2_type,  # HPLT-TAN
            self.constants.axis_3_type,  # HPLN-TAN
        ]
        for i, axis_type in enumerate(axis_types, start=1):
            if axis_type == "HPLT-TAN":
                header[f"DNAXIS{i}"] = header[f"NAXIS{i}"]
                header[f"DTYPE{i}"] = "SPATIAL"
                header[f"DPNAME{i}"] = "spatial along slit"
                header[f"DWNAME{i}"] = "helioprojective longitude"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
            elif axis_type == "AWAV":
                header[f"DNAXIS{i}"] = header[f"NAXIS{i}"]
                header[f"DTYPE{i}"] = "SPECTRAL"
                header[f"DPNAME{i}"] = "dispersion axis"
                header[f"DWNAME{i}"] = "wavelength"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
                # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
                header["WAVEMIN"] = header[f"CRVAL{i}"] - (
                    header[f"CRPIX{i}"] * header[f"CDELT{i}"]
                )
                header["WAVEMAX"] = header[f"CRVAL{i}"] + (
                    (header[f"NAXIS{i}"] - header[f"CRPIX{i}"]) * header[f"CDELT{i}"]
                )
            elif axis_type == "HPLN-TAN":
                header[f"DNAXIS{i}"] = self.constants.num_map_scans
                header[f"DTYPE{i}"] = "SPATIAL"
                header[f"DPNAME{i}"] = "map scan step number"
                header[f"DWNAME{i}"] = "helioprojective latitude"
                header[f"DUNIT{i}"] = header[f"CUNIT{i}"]
                # Current position in map scan step which counts from zero
                header[f"DINDEX{i}"] = header["CNCURSCN"] + 1
            else:
                raise ValueError(
                    f"Unexpected axis type. Expected ['HPLT-TAN', 'AWAV', 'HPLN-TAN']. Got {axis_type}"
                )

        # Set the base number of dataset axes to 3
        num_axis = 3

        # ---Temporal---
        if self.constants.num_map_scans > 1:
            num_axis += 1
            header[
                f"DNAXIS{num_axis}"
            ] = self.constants.num_scan_steps  # total number of scans in the dataset
            header[f"DTYPE{num_axis}"] = "TEMPORAL"
            header[f"DPNAME{num_axis}"] = "time"
            header[f"DWNAME{num_axis}"] = "time"
            header[f"DUNIT{num_axis}"] = "s"
            # Temporal position in dataset
            header[f"DINDEX{num_axis}"] = header["DSPSNUM"]  # Current scan number

        # ---Stokes---
        if self.constants.correct_for_polarization:
            num_axis += 1
            header[f"DNAXIS{num_axis}"] = 4  # I, Q, U, V
            header[f"DTYPE{num_axis}"] = "STOKES"
            header[f"DPNAME{num_axis}"] = "polarization state"
            header[f"DWNAME{num_axis}"] = "polarization state"
            header[f"DUNIT{num_axis}"] = ""
            # Stokes position in dataset - stokes axis goes from 1-4
            header[f"DINDEX{num_axis}"] = self.constants.stokes_params.index(stokes.upper()) + 1

        else:
            logger.info("Spectrographic data detected. Not adding DNAXIS information.")

        header["DNAXIS"] = num_axis
        header["DAAXES"] = 2  # Spectral, spatial
        header["DEAXES"] = num_axis - 2  # Total - detector axes

        header["LEVEL"] = 1
        header["WAVEBAND"] = self.constants.spectral_line
        header["WAVEUNIT"] = -9  # nanometers
        header["WAVEREF"] = "Air"
        # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
        header["WAVEMIN"] = header["CRVAL1"] - (header["CRPIX1"] * header["CDELT1"])
        header["WAVEMAX"] = header["CRVAL1"] + (
            (header["NAXIS1"] - header["CRPIX1"]) * header["CDELT1"]
        )

        # Binning headers
        header["NBIN1"] = 1
        header["NBIN2"] = 1
        header["NBIN3"] = 1
        header["NBIN"] = header["NBIN1"] * header["NBIN2"] * header["NBIN3"]

        return header
