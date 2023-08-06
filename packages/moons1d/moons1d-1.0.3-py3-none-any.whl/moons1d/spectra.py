import numpy as np

from astropy.io import fits
from astropy import units as u
from astropy.convolution import Gaussian1DKernel, convolve
from astropy.constants import c
from astropy.units import Quantity
from astropy.stats import sigma_clip
from spectres import spectres

from synphot import SourceSpectrum, SpectralElement, units, ReddeningLaw
from synphot.models import Box1D, Empirical1D

from . import utils


class Spectra:
    """Spectra objects contain 1D arrays of numbers along a regularly
    spaced grid of wavelengths.

    The spectral pixel values and the wavelength, if any, are available
    as arrays that can be accessed via properties of the Spectrum object
    called  :attr:`flux` and  :attr:`wave`, respectively. In addition to these 1D arrays
    severals attributes are associated  that provide general information
    on the type of spectra.

    Attributes
    ----------
    flux : 1D array
        Fluxes for each spectral pixels
    wave : 1D array
        Wavelength for each spectral pixels
    meta : `dict`
        meta dictionary with keys:

        ``"nid"``
            Number identifier of an object instance (`int`)
        ``"sampling"``
            Number of pixels per element of spectral resolution (`float`).
        ``"resolution"``
            Spectral resolution (`float`)
        ``"dispersion"``
            Spectral dispersion(`float`).

    Methods
    -------
    Trim(wave_range):
        Trim spectrum to a given wavelength range

    Mean(wave_range):
        Return the mean value of the fluxes array inside a wavelength range

    ReSampleArr(wave_new):
        Resample ``flux``, ``errFlux`` and ``wave arrays`` to a new wavelength sampling


    """
    def __init__(self, nid):
        #self.nid = nid
        #self.header = ""
        self.meta = {}
        self.meta['nid'] = nid
        self.meta['header'] =""
        self.flux = 0.0  # in ergs/s/cm2/A
        self.wave = 0.0  # in Ang

    def Trim(self, wave_range):
        """
        Trim spectrum into a wavelength range.

        The function adds/updates :attr:`flux` and  :attr:`wave`.

        Parameters
        ----------
        wave_range : `list` [`float`]
            2 element list [min,max] wavelengths
        """
        wave_range = wave_range.to(self.wave.unit)
        pix_mask = (self.wave >= wave_range[0]) & (self.wave <= wave_range[1])
        self.wave = self.wave[pix_mask]
        self.flux = self.flux[pix_mask]
        if hasattr(self, "errflux"):
            self.errflux = self.errflux[pix_mask]

    def Mean(self, wave_range):
        """
        Return the mean value of the fluxes array inside a wavelength range

        Parameters
        ----------
        wave_range : `list` [`float`]
            2 element list [min,max] wavelengths

        Returns
        -------
        mean : float
           flux mean over the wave range

        """
        wave_range = wave_range.to(self.wave.unit)
        pix_mask = (self.wave > wave_range[0]) & (self.wave < wave_range[1])
        mean = np.mean(self.flux[pix_mask])
        return mean

    def LoadFromTxt(self, file, unitwave = u.angstrom, unitflux = (u.erg/u.s/u.cm**2/u.angstrom)):
        """ Load fluxes from file

        The function adds/updates :attr:`flux` and  :attr:`wave`.

        Parameters
        ----------
        file : `str`
            string with the filename
        unitwave : `astropy.unit`, optional
            wavelength unit. Default is Angstrom
        unitflux = `astropy.unit`, optional
            flux unit. Default is erg/s/cm**2/angstrom


        """
        self.wave, self.flux = np.loadtxt(file, unpack = True)
        self.wave = self.wave * unitwave
        self.flux = self.flux * unitflux

    def ReSampleArr(self, wave_new):
        """
        Resample the flux, errFlux and wave array to a new wavelength sampling
        using SpectRes package.

        The function adds/updates :attr:`flux`,  :attr:`erflux`, and :attr:`wave`.

        References
        ----------
          [1] SpectRes package description in https://arxiv.org/abs/1705.05165, https://github.com/ACCarnall/SpectRes/blob/master/docs/index.rst
        """
        self.wave = self.wave.to(wave_new.unit)

        if not hasattr(self, "errflux"):
            self.flux = spectres(wave_new.value, self.wave.value, self.flux.value) * self.flux.unit

        if hasattr(self, "errflux"):
            self.flux, self.errflux = spectres(wave_new.value, self.wave.value, self.flux.value, spec_errs=self.errflux.value) * self.errflux.unit
        self.wave = wave_new

    def Degrade_Resolution(self, FWHM_in, dispersion, FWHM_out):
        """
        Degrades spectral resolution using a Gaussian 1D Kernel
        """

        FWHM_dif = np.sqrt(FWHM_out**2 - FWHM_in**2)
        sigma = FWHM_dif/2.355/dispersion  # Sigma difference in pixels
        gauss_1D_kernel = Gaussian1DKernel(sigma.value)
        self.flux = convolve(self.flux, gauss_1D_kernel)
        if hasattr(self, "errflux"):
            self.errflux = convolve(self.errflux, gauss_1D_kernel)


class Template(Spectra):
    """
    Template objects are a sub-class of Spectra. In addition to the
    attributes of "Spectra", severals attributes are stored in :attr:`meta` containing general
    information on the type of template.

    Attributes
    ----------
    meta : `dict`
        meta dictionary with keys:

        ``"name"``
            Name of the template (`str`).
        ``"type_source"``
            type of the source (`str`). Two accepted values:

            - 'point-source'. Point sources with fluxes interpreted as erg/s/A/cm2.

            - 'extended': Extended sources with fluxes interpreted as a surface brigthness in erg/s/A/cm2/arcsec2.

        ``"mag"``
            Magnitude of the source (`float`)
        ``"type_mag"``
            Type of magntude, could be either "AB" or "Vega"
        ``"filter"``
            Filter name (`str`)

    Methods
    -------
    LoadTemplate_File():
        Load Template from Fits file or from a synphot.sourcepectrum object

    """

    def __init__(self, nid, type_source="point-source"):

        Spectra.__init__(self, "Template")

        self.meta['name'] = 'No name'
        self.meta['type'] = 'Template' #Type of spectrum: template, sky, atmospheric absorption etc..
        self.meta['type_source'] = type_source  # point-source or surface brigthness
        self.meta['z'] = 0.0
        self.meta['mag']= 0.0
        self.meta['type_mag'] = 'AB'
        self.meta['filter'] = 'AB'
        self.meta['sampling'] = 0.
        self.meta['dispersion'] = 0.
        self.meta['resolution'] = 0.

        self.flux = []
        self.wave = []


    def LoadTemplate_File(self, template, filter_syn, mag=19., mag_type='AB', E_BV=0.0 , Extinction_model='mwavg', redshift= None):
        """
        Load Template from Fits file or from a synphot.sourcepectrum object

        This function load a template from an file and computes the following normalisation:

        - Apply extinction law using an reddening law and an extinction parameter Av

        - Redshift the spectrum (conserving the flux)

        - Normalise the template to a given magnitude/filter

        The function adds/updates :attr:`flux` and  :attr:`wave`.

        Parameters
        ----------
        template : `str` or `synphot.SourceSpectrum`
            Name of the template file (path + name). See fits format in https://synphot.readthedocs.io/en/latest/synphot/overview.html#synphot-fits-format-overview
            or synphot.SourceSpectrum objects

        filter_syn : `synphot.SpectralElement`
            Bandpass of the filter for magnitude normalisation

        mag : float
            Magnitude

        mag_type : str
            Type of magnitude, either 'AB' or 'Vega'

        E_BV : float
            E(B-V) value for the extinction

        Extinction_model: str
            Name of the Extinction law. Possible values  are:

            - lmc30dor : LMC2 Supershell Rv = 2.76 Gordon et al. 2003

            - lmcavg : LMC Average Rv = 3.41 Gordon et al. 2003

            - mwavg : Milky Way Diffuse Rv = 3.1 Cardelli et al. 1989

            - mwdense : Milky Way Dense Rv = 5.0 Cardelli et al. 1989

            - mwrv21 : Milky Way CCM Rv = 2.1 Cardelli et al. 1989

            - mwrv40 : Milky Way CCM Rv = 4.0 Cardelli et al. 1989

            - smcbar: SMC Bar Rv = 2.74 Gordon et al. 2003

            - xgalsb: Starburst (attenuation law) Rv = 4.0 Calzetti et al. 2000

        redshift : float
            Redshift of the source spectrum

        Examples
        --------
        ** Exemple 1 : Template from file and flux normalisation with a Johnson_j filter**

        Create a spectrum from a template file and a filter bandpass, with AB mag = 21. and E_BV =0.1  Milky Way Diffuse Rv = 3.1  extinction law.

        >>> filter = 'johnson_j_003_syn.fits'

        >>> bp = SpectralElement.from_file(filter)

        >>> bp.name = 'Johnson_J'

        >>> template_file  ='input_stellar_template_conv.fits'

        >>> Star = Template(1, type_source ='point-source') # first argument is just an ID number

        >>> Star.LoadTemplate_File(template_file, bp, mag=21., mag_type='AB', E_BV = 0.1, Extinction_model='mwavg')


        ** Exemple 2 : Normalize flux to reference wavelength**

        Same as before, but with a normalisation at a specific wavelength.
        Create a narrow filter `bp` at the central wavelength.

        >>> wave_c = 1.22 * 1.0e4

        >>> bp = SpectralElement(Empirical1D, points=[wave_c - 1, wave_c, wave_c + 1], lookup_table=[1,1,1], keep_neg=True)

        >>> bp.name = 'J-band'

        Load the stellar template file as a point-source.

        >>> template_file  ='input_stellar_template_conv.fits'

        >>> Star = Template(1, type_source ='point-source') # first argument is just an ID number

        Normalized the template to mag=21 AB and apply extinction.

        >>> Star.LoadTemplate_File(template_file, bp, mag=21., mag_type='AB', E_BV = 0.1, Extinction_model='mwavg')


        **Exemple 3 : Flat F_lambda**

        >>> Cst_temp = SourceSpectrum(ConstFlux1D, amplitude=1.* units.FLAM )

        >>> Cst_temp.name = 'Flat F_lambda'

        >>> Source = Template(1, type_source ='point-source')

        >>> Source.LoadTemplate_File(Cst_temp,bp, mag=15.5, mag_type='AB', E_BV=0.0 , Extinction_model='mwavg', redshift=0.)


        """
        if isinstance(template, SourceSpectrum) :
            self.meta['sampling'] = 2.
            self.meta['resolution'] = 20000
            self.meta['dispersion'] = ( filter_syn.avgwave() / self.meta['resolution'] )/ self.meta['sampling']
            self.meta['name'] = template.name
            self.meta['type_mag']= mag_type
            self.wave =  np.arange(3000,18000, self.meta['dispersion'].value  ) * u.angstrom
            Source = template.taper(wavelengths=self.wave) # + em

        else :
            HDU = fits.open(str(template))
            self.flux = HDU[0].data
            self.header = HDU[0].header
            self.wave = self.header['CRVAL1'] + self.header['CDELT1'] * np.arange(0, self.header['NAXIS1'], 1)

            if self.header['TUNIT2'] == 'erg/s/cm2/A' :
                self.flux *=  units.FLAM
            elif self.header['TUNIT2'] == 'erg/s/cm2/Hz' :
                self.flux *= units.FNU
            else :
                self.flux *=  units.FLAM

            if self.header['TUNIT1'] in ['angstroms','Angstroms','ANGSTROMS','AA'] :
                self.wave *=  u.AA
            elif self.header['TUNIT1'] in ['MICRONS','Microns','microns'] :
                self.wave *=  u.um
            else :
                self.wave *=  u.AA

            Source = SourceSpectrum(Empirical1D, points = self.wave , lookup_table=self.flux, keep_neg=True)
            self.meta['header'] = HDU[0].header
            self.meta['resolution'] = self.meta['header']["R"]
            self.meta['sampling'] = self.meta['header']["Sampling"] * u.pix
            self.meta['dispersion'] = self.meta['header']["CDELT1"] * Source.waveset.unit / u.pix
            self.meta['name'] = self.meta['header']["MNAME"]

        if redshift is not None :
            Source.z_type = 'conserve_flux'
            Source.z = redshift
            self.wave = Source.waveset

        if E_BV is not None :
            Extinction_model = ReddeningLaw.from_extinction_model(Extinction_model).extinction_curve(E_BV)
            Source = Source * Extinction_model
            self.meta['EXT_FUNC'] = Extinction_model
            self.meta['name'] = E_BV
        if mag_type == 'AB':
            Source = Source.normalize(mag * u.ABmag, filter_syn, force=True)
        elif mag_type == 'Vega':
            vega = SourceSpectrum.from_vega()  # For unit conversion
            Source = Source.normalize(mag * units.VEGAMAG, filter_syn, vegaspec=vega, force=True)
        elif mag_type == 'AB_pivot':
            Source = Source.normalize(mag * u.ABmag, filter_syn, wavelengths = filter_syn.waverange,  force=True)
        elif mag_type == 'Vega_pivot':
            Source = Source.normalize(mag * u.ABmag, filter_syn, wavelengths = filter_syn.waverange, force=True)
        elif mag_type == 'None':
            Source = Source

        ergscm2A = u.erg / u.s / u.cm**2 / u.angstrom
        self.flux = np.array(Source(Source.waveset,flux_unit='flam')) * ergscm2A
        if self.meta['type_source'] == "extended":
            self.flux = self.flux / (1 * u.arcsec**2)

        self.meta['z'] = redshift
        self.meta['mag'] = mag
        self.meta['type_mag'] = mag_type
        self.meta['filter'] = filter_syn.name
        self.meta['type'] = 'Template'


    def VelocityDisp(self, FWHM_in, FWHM_out):
        """
        Increase the velocity dispersion of a stellar template
        """

        FWHM_dif = np.sqrt(FWHM_out**2 - FWHM_in**2)
        sigma = FWHM_dif/2.355/self.meta['dispersion']  # Sigma difference in pixels
        gauss_1D_kernel = Gaussian1DKernel(sigma.value)
        self.flux = convolve(self.flux, gauss_1D_kernel) * self.flux.unit

class Sky(Spectra):
    """
    Sky spectrum class. Sky objects are a sub-class of Spectra.

    Attributes
    ----------
    type: str
        Type of sky model. e.g "SKYCAL_local" for sky models from SkyCal
        ESO simulator
    flux: array
        Sky flux in ph/s/cm2/A/arcsec2
    errflux: arrays
        1 sigma variaion of the sky

    Methods
    -------
    LoadTemplate_File():
        Load Template from Fits file or from a synphot.sourcepectrum object
    """

    def __init__(self, nid):
        Spectra.__init__(self, "Sky")
        self.meta['type'] = 'Sky'

    def Load_ESOSkyCal_Template(self, airmass):
        """
        Load ESO sky spectra from librairy

        Parameters
        ----------
        airmass: float
            airmass of the observation

        Reference
        ---------
            [1] SkyCal, https://www.eso.org/observing/etc/bin/gen/form?INS.MODE=swspectr+INS.NAME=SKYCALC,  Noll et al. (2012, A&A 543, A92) and Jones et al. (2013, A&A 560, A91).
        """

        # in Vacuum
        self.meta['name'] = 'SKYCAL_local'
        self.model = ""

        # Search for closest templates in terms of airmass
        available_airmass = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
        airmass_index = np.argmin(np.abs(available_airmass - airmass))
        closest_airmass = available_airmass[airmass_index]

        self.model = (utils.install_dir + "/models/Skymodel/SkyTemplate_ESO_a"
                      + np.str(closest_airmass) + ".fits")

        try:
            fits.getdata(str(self.model))

        except FileNotFoundError:
            raise FileNotFoundError("FITS file not found or not valid.")

        HDU = fits.open(str(self.model))
        self.flux = HDU[0].data
        self.errflux = HDU[2].data
        self.header = HDU[0].header

        self.meta['header'] = HDU[0].header

        self.wave = self.meta['header']["CDELT1"] * np.arange(self.meta['header']["NAXIS1"])
        self.wave += self.meta['header']["CRVAL1"]

        #self.wave = self.header["CDELT1"] * np.arange(self.header["NAXIS1"])
        #self.wave += self.header["CRVAL1"]

        # Convert wavelength unit
        if self.meta['header']["TUNIT1"] in ["AA", "A", "ang", "Angstroms"]:
            self.wave = self.wave * u.angstrom

        if self.meta['header']["TUNIT1"] in ["nm", "nanometer"]:
            self.wave = self.wave * u.nm
            self.wave = self.wave.to(u.angstrom)
            self.meta['header']["TUNIT1"] = "Angstroms"

        if self.meta['header']["TUNIT1"] in ["micron"]:
            self.wave = self.wave * u.micron
            self.wave = self.wave.to(u.angstrom)
            self.meta['header']["TUNIT1"] = "Angstroms"

        self.meta['dispersion'] = self.meta['header']["CDELT1"] * u.angstrom / u.pix

        # Convert flux
        if self.meta['header']["TUNIT2"] == "ph/s/cm2/A/arcsec2":
            # assumes a surface brightness - flux in 1 arcsec2
            phscm2A = u.photon / u.s / u.cm**2 / u.angstrom / u.arcsec**2
            self.flux = self.flux * phscm2A
            self.errflux = self.errflux * phscm2A

    def CreateSkyMask(self, sigma=6.2):
        """
        Create a mask for strong sky lines using sigma-clipping
        """

        Mask_sky = sigma_clip(self.flux.value, sigma=sigma).mask
        self.Mask = Mask_sky


class Atm_abs(Spectra):
    """
    Atmospheric absorption spectra class

    Atm_abs objects are a sub-class of Spectra

    Attributes
    ----------
    type: str
        Type of sky model. e.g "SKYCAL_local" for sky models from SkyCal
        ESO simulator
    """

    def __init__(self, nid):
        Spectra.__init__(self, "Atm_abs")
        self.meta['type'] = 'Atm_abs'

    def Load_ESOSkyCal_Template(self, airmass):
        """
        Load ESO atmospheric absorption spectra from library
        """

        self.meta['name'] = "SKYCAL_local"
        self.model = ""

        # Search for closest templates in terms of airmass
        available_airmass = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
        airmass_index = np.argmin(np.abs(available_airmass - airmass))
        closest_airmass = available_airmass[airmass_index]

        self.model = (utils.install_dir + "/models/Skymodel/SkyTemplate_ESO_a"
                      + np.str(closest_airmass) + ".fits")

        try:
            fits.getdata(str(self.model))

        except FileNotFoundError:
            raise FileNotFoundError("FITS file not found or not valid.")

        HDU = fits.open(str(self.model))

        self.flux = HDU[1].data
        self.meta['header'] = HDU[1].header

        self.wave = self.meta['header']["CDELT1"] * np.arange(self.meta['header']["NAXIS1"])
        self.wave += self.meta['header']["CRVAL1"]

        # Convert wavelength unit
        if self.meta['header']["TUNIT1"] in ["AA", "A", "ang", "Angstroms"]:
            self.wave = self.wave * u.angstrom

        if self.meta['header']["TUNIT1"] in ["nm", "nanometer"]:
            self.wave = self.wave * u.nm
            self.wave = self.wave.to(u.angstrom)
            self.meta['header']["TUNIT1"] = "Angstroms"

        if self.meta['header']["TUNIT1"] in ["micron"]:
            self.wave = self.wave * u.micron
            self.wave = self.wave.to(u.angstrom)
            self.meta['header']["TUNIT1"] = "Angstroms"

        self.meta['dispersion'] = self.meta['header']["CDELT1"] * u.angstrom / u.pix

        if self.meta['header']["TUNIT2"] == "sky transmission fraction":
            self.flux = self.flux * u.dimensionless_unscaled


class SimSpectrum(Spectra):
    def __init__(self, nid):
        Spectra.__init__(self, "SimSpectrum")


class LSF(Spectra):
    def __init__(self, nid):
        Spectra.__init__(self, "PSF")
