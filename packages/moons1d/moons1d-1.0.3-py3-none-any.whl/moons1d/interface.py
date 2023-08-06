import numpy as np
from configobj import ConfigObj
#from astropy import units as u
#from astropy.constants import c
#from astropy.units import Quantity
from synphot import SpectralElement
from synphot.models import Empirical1D

import matplotlib.pyplot as plt

from . import utils
from . import simulator
from . import spectra
from . import catalogue

def get_filter(filter_name, mag_type, verbose = True):
    #Configure filter
    filter_path = utils.install_dir+ "/models/synphot/comp/nonhst/"
    if filter_name in ['bessel_j','bessel_h','bessel_k','cousins_r','cousins_i','johnson_u','johnson_b','johnson_v','johnson_r','johnson_i','johnson_j','johnson_k']:
        bp = SpectralElement.from_filter(filter_name)
    elif filter_name in ['2mass_j']:
        bp = SpectralElement.from_file(filter_path+'2mass_j_001_syn.fits')
    elif filter_name in ['2mass_h']:
        bp = SpectralElement.from_file(filter_path+'2mass_h_001_syn.fits')
    elif filter_name in ['2mass_ks']:
        bp = SpectralElement.from_file(filter_path+'2mass_ks_001_syn.fits')
    elif filter_name in ['sdss_u']:
        bp = SpectralElement.from_file(filter_path+'sdss_u_005_syn.fits')
    elif filter_name in ['sdss_r']:
        bp = SpectralElement.from_file(filter_path+'sdss_r_005_syn.fits')
    elif filter_name in ['sdss_g']:
        bp = SpectralElement.from_file(filter_path+'sdss_g_005_syn.fits')
    elif filter_name in ['sdss_i']:
        bp = SpectralElement.from_file(filter_path+'sdss_i_005_syn.fits')
    elif filter_name in ['sdss_z']:
        bp = SpectralElement.from_file(filter_path+'sdss_z_005_syn.fits')
    elif filter_name in ['I', 'J', 'H']:
        Photo_bands = [{'name':'I', 'wave_ref' : 0.797, 'vega_cst': 0.45 },{'name':'J', 'wave_ref' : 1.22, 'vega_cst': 0.91 },{'name':'H', 'wave_ref' : 1.63, 'vega_cst': 1.39 }]
        #Use ref AB wavelength for normalisation (no filter)
        wave_c = ref =[x for x in Photo_bands if x['name'] == filter_name][0]['wave_ref'] * 1.0e4
        bp = SpectralElement(Empirical1D, points=[wave_c - 10, wave_c, wave_c + 10], lookup_table=[1,1,1], keep_neg=True)
        if mag_type == 'Vega_pivot' :
            bp.vega_cst = ref =[x for x in Photo_bands if x['name'] == filter_name][0]['vega_cst']
    else :
         print('[ERROR]--- UNKWON FILTER')
         return
    bp.name = filter_name
    if verbose:
        print('[INFO] | FILTER PROPERTIES')
        print('[INFO] |--- Name %s ' % (bp.name))
        print('[INFO] |--- Lambda average: %s ' % (bp.avgwave()))
        print('[INFO] |--- Lambda width:(rectangular) %s ' % (bp.rectwidth()))
    return bp

def config_run(Obs_conf, atm_disp = True, verbose = True):
    MOONS_modes = ConfigObj(utils.install_dir
                                + "/models/Instrument/MOONS_mode.ini")

    if Obs_conf['band'] == 'All':
        print("Please simulate one band at time")
        return

    Simu = simulator.Simulation(MOONS_modes,Obs_conf)
    Simu.GenerateDispersionAxis(verbose = verbose)
    Simu.Generate_Telescope_Transmission(verbose = verbose)
    Simu.Generate_Instrument_Transmission(verbose = verbose)
    Simu.Generate_FibreLoss(atm_disp = atm_disp, verbose = verbose)
    Simu.Generate_Total_Transmission(verbose = verbose)

    sky_model = spectra.Sky(1)
    sky_model.Load_ESOSkyCal_Template(Simu.observation['airmass'])
    Simu.setSky(sky_model)

    atm_model = spectra.Atm_abs(1)
    atm_model.Load_ESOSkyCal_Template(Simu.observation['airmass'])
    Simu.setAtms_abs(atm_model)
    return Simu

def run_multi_obj(Simu, catalogue, template_path = 'Working_dir' , verbose = True , save_plots = True, save_fits = True, Output_path = 'Working_dir', ApLoss=True):

    #Configure template
    if template_path == 'Working_dir':
        template_path = utils.working_dir +'/'

    if template_path == 'Working_dir':
        template_path = utils.working_dir +'/'

    for target in catalogue.targets :
        filter = get_filter(target.mag_filter, target.mag_type, verbose = verbose)
        if 'vega_cst' in dir(filter):
            target.mag += filter.vega_cst
        if verbose:
            print('[INFO] | TEMPLATE PROPERTIES')
            print('[INFO] |--- Name %s ' % (target.template_fits))
            print(f'[INFO] |--- {target.type_source}')
            print(f'[INFO] |--- E(B-V)= {target.e_bv} {target.extinction_model}')
            print(f'[INFO] |--- Redshift {target.redshift}')

        source = spectra.Template(1, type_source = target.type_source)
        source.LoadTemplate_File(template_path+target.template_fits,filter, mag=target.mag, mag_type= target.mag_type,  redshift = target.redshift, Extinction_model = target.extinction_model , E_BV = target.e_bv)

        Simu.setTemplate(source)
        Simu.Match_resolution()
        Simu.ConvertFlux2Counts()
        Simu.sky.CreateSkyMask(sigma=3.2)

        if Simu.observation["observing_mode"] == 'STARE':
            Simu.Generate_Stare_Seq(verbose = verbose)
        if Simu.observation["observing_mode"] == 'NOD':
            Simu.Generate_Nod_Seq(verbose = verbose)
        if Simu.observation["observing_mode"] == 'XSWITCH':
            Simu.Generate_Xswitch_Seq(verbose = verbose)

        Simu.Calibrate_data(ApLoss = ApLoss)

        if verbose:
            print('[INFO] | SIGNAL TO NOISE RATIO ')
            print(f'[INFO] |--- [Max]={np.max(SNR)}')
            print(f'[INFO] |--- [@mid waveband]={SNR[int(len(SNR)/2)]}')

        if save_plots:
            plt.figure()
            plt.rcParams['figure.figsize'] = (14,10)
            fig, (ax1, ax2) = plt.subplots(2)
            fig.suptitle('Axes values are scaled individually by default')
            x = np.linspace(0, 2 * np.pi, 400)
            y = np.sin(x ** 2)

            ax1.plot(Simu.model.wave, Simu.model.Obs_calibrated,label='Simulated - Flux' )
            ax1.plot(Simu.template.wave, Simu.model.Error_calibrated, color ='green', label='Simulated - Error')
            ax1.plot(Simu.template.wave, Simu.template.flux, color ='red',label='Input template')
            ax1.legend()
            ax1.set( ylabel = "Flux [erg/s/A/cm2]")
            ax2.plot(Simu.model.wave,Simu.model.Reduced_frame /  Simu.model.Noise_frame)
            ax2.set(ylabel = "SNR", xlabel = "Wavelength [A]")
            plot_file = Output_path + target.name+ '_' + Simu.observation["band"] + '.pdf'
            plt.savefig(plot_file)
            plt.close(fig)
            if verbose:
                print('[INFO] |--- PLOT SAVED ')
                print(f'[INFO] |------ {plot_file}')

        if save_fits:
            fileout = Output_path + target.name+ '_' + Simu.observation["band"] + '.fits'
            Simu.setFileOut(fileout) # Output .fits file
            Simu.SavetoFits(verbose = False)

    return np.c_[Simu.template.wave.value,
                    Simu.template.flux.value,
                    Simu.model.Obs_calibrated.value,
                    Simu.model.Error_calibrated.value]

def run_1obj_1band(template_spec, type_source, mag, mag_type, filter, Obs_conf, redshift = 0.0, Extinction_model = "mwavg" , E_BV = 0.0, atm_disp = True, ApLoss=True, verbose=True, save_plots = False, save_fits = False, debug = False):
    """
    Top level interface function for MOONS1D.
    Run one template and band at the time.


    Parameters
    ----------
    template : `str` or `synphot.SourceSpectrum`
        Name of the template file (path + name). See fits format in https://synphot.readthedocs.io/en/latest/synphot/overview.html#synphot-fits-format-overview
            or synphot.SourceSpectrum objects

    type_source : str
        Type of source, either 'point_source' or 'extended'

    mag : float
        Magnitude to normalise the input spectrum

    mag_type : float
        Type of magnitude: Vega or AB

    filter : `synphot.SpectralElement`
        Filter over which the spectrum will be normalised to
        the magnitude set in mag (in Angstroms).

        observation: dict
            observation dictionary contains all the parameters linked to the observational setup (similar to the ones stored in an OB):

            ``"R_mode"``
                Mandatory key. The `R_mode` key stores the resolution mode of MOONS (`str`): either "LR" for the low resolution mode or "HR" for the high resolution mode.

            ``"observing_mode"``
                Mandatory key. Name of the observing template (`str`): either "STARE", "NOD", "XSWITCH"

            ``"band"``
                Mandatory key. The keyword ``band`` stores the band of the simulated observation (`str`). Valid options are "RI", "YJ", "H", "all"

            ``"OB_name"``
                Name of the OB (`str`). Default is 'TestOB'.

            ``"Atm_correction"``
                Wavelength at which the atmospheric diffraction correction is
                performed [microns] (`float`). Default is 1.2 microns.

            ``"NDIT"``
                Number of exposure in the simulated OB (`int`). Default is 6.

            ``"DIT"``
                Detector integration time of each NDIT [s] (`float`). Default is 600s.

            ``"seeing"``
                Seeing at the zenith at 5000A [arcsec] (`float`). Default is 0.8.

            ``"airmass"``
                Average airmass during observations[arcsec] (`float`). Default is 1.

            ``"temperature"``
                Temperature [C] (`float`). Default value is 11.5C.

            ``"humidity"``
                Humidity [%] (`float`). Default value is 14.5 per cent.

            ``"pressure"``
                Atmospheric Ppressure [mBar] (`float`). Default value is 743 mBar.

            ``"telescope"``
                Which telescope is the observation being carried out with (`str`).
                Defaults to VLT, though can also be set to ELT.

    verbose : bool (optional)
        Print information to terminal whilst in progress, default True.

    atm_disp : bool (optional)
        Simulate the atmospheric diffraction. Defaults is True.

    save_plots : bool (optinal)
        Save plots result plots (Fluxes and SNR). Default is False.

    save_fits : bool (optional)
        Save results in fits files. Default is False

    debug : bool (optional)
        Run, debugging mode. The return variable is a dicctionary of moons1d.simulation objects (one per band).

    Returns
    -------
    A dictionnary with the results in each band. The keywords are the name of each band.
    The results in each bands are stored in a 2d array with four column containing:

    - Column 0: wavelengths (Angstrom)

    - Column 1: input model fluxes (erg/s/cm^2/A)

    - Column 2: mock observed fluxes (erg/s/cm^2/A)

    - Column 3: mock observational errors (erg/s/cm^2/A)

    """

    source = spectra.Template(1, type_source = type_source)
    source.LoadTemplate_File(template_spec,filter, mag=mag, mag_type=mag_type,  redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV)

    MOONS_modes = ConfigObj(utils.install_dir
                                + "/models/Instrument/MOONS_mode.ini")

    if Obs_conf['band'] == 'All':
        print("Use function run_allands")
        return

    Simu = simulator.Simulation(MOONS_modes,Obs_conf)
    Simu.GenerateDispersionAxis(verbose=verbose)
    Simu.Generate_Telescope_Transmission(verbose=verbose)
    Simu.Generate_Instrument_Transmission(verbose=verbose)
    Simu.Generate_FibreLoss(atm_disp = atm_disp,verbose=verbose)
    Simu.Generate_Total_Transmission(verbose=verbose)

    sky_model = spectra.Sky(1)
    sky_model.Load_ESOSkyCal_Template(Simu.observation['airmass'])
    Simu.setSky(sky_model)

    atm_model = spectra.Atm_abs(1)
    atm_model.Load_ESOSkyCal_Template(Simu.observation['airmass'])
    Simu.setAtms_abs(atm_model)

    Simu.setTemplate(source)
    Simu.Match_resolution()
    Simu.ConvertFlux2Counts()
    Simu.sky.CreateSkyMask(sigma=3.2)

    if Obs_conf['observing_mode'] == 'STARE':
        Simu.Generate_Stare_Seq()
    if Obs_conf['observing_mode'] == 'NOD':
        Simu.Generate_Nod_Seq()
    if Obs_conf['observing_mode'] == 'XSWITCH':
        Simu.Generate_Xswitch_Seq()

    Simu.Calibrate_data(ApLoss=ApLoss)

    #Print max SNR and SNR at mid bandwidth
    SNR = Simu.model.Reduced_frame /  Simu.model.Noise_frame

    if verbose:
        print('[INFO] | SIGNAL TO NOISE RATIO ')
        print(f'[INFO] |--- [Max]={np.max(SNR)}')
        print(f'[INFO] |--- [@mid waveband]={SNR[int(len(SNR)/2)]}')
    if save_plots:
        plt.figure()
        plt.rcParams['figure.figsize'] = (14,10)
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('Axes values are scaled individually by default')
        x = np.linspace(0, 2 * np.pi, 400)
        y = np.sin(x ** 2)

        ax1.plot(Simu.model.wave, Simu.model.Obs_calibrated,label='Simulated - Flux' )
        ax1.plot(Simu.template.wave, Simu.model.Error_calibrated, color ='green', label='Simulated - Error')
        ax1.plot(Simu.template.wave, Simu.template.flux, color ='red',label='Input template')
        ax1.legend()
        ax1.set( ylabel = "Flux [erg/s/A/cm2]")
        ax2.plot(Simu.model.wave,Simu.model.Reduced_frame /  Simu.model.Noise_frame)
        ax2.set(ylabel = "SNR", xlabel = "Wavelength [A]")
        plot_file = utils.working_dir +'/'+ Obs_conf['OB_name']+ '_' + Obs_conf['band'] + '.pdf'
        plt.savefig(plot_file)
        if verbose:
            print('[INFO] |--- PLOT SAVED ')
            print(f'[INFO] |------ {plot_file}')

    if save_fits:
        fileout = utils.working_dir +'/'+ Obs_conf['OB_name']+ '_' + Obs_conf['band'] + '.fits'
        Simu.setFileOut(fileout) # Output .fits file
        Simu.SavetoFits()

    if not debug :
        return np.c_[Simu.template.wave.value,
                    Simu.template.flux.value,
                    Simu.model.Obs_calibrated.value,
                    Simu.model.Error_calibrated.value]
    if  debug :
        print('[INFO] |--- BEGUG MODE')
        return Simu

def run_1obj_allbands(template_spec, type_source, mag, mag_type, filter, Obs_conf,  redshift = 0.0, Extinction_model = "mwavg" , E_BV = 0.0,atm_disp = True,  ApLoss=True, verbose=True, save_plots = False, save_fits = False, debug = False):
    """
    Top level interface function for MOONS1D.
    Run one template at the time, but can compute all the MOONS bands at the same time

    Parameters
    ----------
    template : `str` or `synphot.SourceSpectrum`
        Name of the template file (path + name). See fits format in https://synphot.readthedocs.io/en/latest/synphot/overview.html#synphot-fits-format-overview
            or synphot.SourceSpectrum objects

    type_source : str
        Type of source, either 'point_source' or 'extended'

    mag : float
        Magnitude to normalise the input spectrum

    mag_type : float
        Type of magnitude: Vega or AB

    filter : `synphot.SpectralElement`
        Filter over which the spectrum will be normalised to
        the magnitude set in mag (in Angstroms).

        observation: dict
            observation dictionary contains all the parameters linked to the observational setup (similar to the ones stored in an OB):

            ``"R_mode"``
                Mandatory key. The `R_mode` key stores the resolution mode of MOONS (`str`): either "LR" for the low resolution mode or "HR" for the high resolution mode.

            ``"observing_mode"``
                Mandatory key. Name of the observing template (`str`): either "STARE", "NOD", "XSWITCH"

            ``"band"``
                Mandatory key. The keyword ``band`` stores the band of the simulated observation (`str`). Valid options are "RI", "YJ", "H", "all"

            ``"OB_name"``
                Name of the OB (`str`). Default is 'TestOB'.

            ``"Atm_correction"``
                Wavelength at which the atmospheric diffraction correction is
                performed [microns] (`float`). Default is 1.2 microns.

            ``"NDIT"``
                Number of exposure in the simulated OB (`int`). Default is 6.

            ``"DIT"``
                Detector integration time of each NDIT [s] (`float`). Default is 600s.

            ``"seeing"``
                Seeing at the zenith at 5000A [arcsec] (`float`). Default is 0.8.

            ``"airmass"``
                Average airmass during observations[arcsec] (`float`). Default is 1.

            ``"temperature"``
                Temperature [C] (`float`). Default value is 11.5C.

            ``"humidity"``
                Humidity [%] (`float`). Default value is 14.5 per cent.

            ``"pressure"``
                Atmospheric Ppressure [mBar] (`float`). Default value is 743 mBar.

            ``"telescope"``
                Which telescope is the observation being carried out with (`str`).
                Defaults to VLT, though can also be set to ELT.

    verbose : bool (optional)
        Print information to terminal whilst in progress, default True.

    atm_disp : bool (optional)
        Simulate the atmospheric diffraction. Defaults is True.

    save_plots : bool (optinal)
        Save plots result plots (Fluxes and SNR). Default is False.

    save_fits : bool (optional)
        Save results in fits files. Default is False

    debug : bool (optional)
        Run, debugging mode. The return variable is a dicctionary of moons1d.simulation objects (one per band).

    Returns
    -------
    A dictionnary with the results in each band. The keywords are the name of each band.
    The results in each bands are stored in a 2d array with four column containing:

    - Column 0: wavelengths (Angstrom)

    - Column 1: input model fluxes (erg/s/cm^2/A)

    - Column 2: mock observed fluxes (erg/s/cm^2/A)

    - Column 3: mock observational errors (erg/s/cm^2/A)

    """

    source = spectra.Template(1, type_source = type_source)
    source.LoadTemplate_File(template_spec,filter, mag=mag, mag_type= mag_type, redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV)

    MOONS_modes = ConfigObj(utils.install_dir
                                + "/models/Instrument/MOONS_mode.ini")

    bands =  MOONS_modes[Obs_conf['R_mode']].sections
    results = {}
    for band in bands:
        Obs_conf['band'] =  band
        print(f'################ {band} ###############')
        results[band] = run_1obj_1band(template_spec, type_source, mag, mag_type, filter, Obs_conf, atm_disp = atm_disp, ApLoss = ApLoss , verbose=verbose, save_plots = save_plots, save_fits = save_fits, debug = debug)

    return results


def run(template_fits, Obs_conf, mag, mag_type = "AB",  type_source = "point-source", filter_name = "J", redshift = 0.0, Extinction_model = "mwavg" , E_BV = 0.0,  atm_disp = True, ApLoss=True , template_path = 'Working_dir', verbose=True, save_plots = False, save_fits = False, debug = False):
    """
    Top level interface function for MOONS1D.
    Run one template at the time, but can compute all the MOONS bands at the same time

    Parameters
    ----------
    """

    bp = get_filter(filter_name,mag_type, verbose=verbose)
    if 'vega_cst' in dir(bp):
        mag += bp.vega_cst

    #Configure template
    if template_path == 'Working_dir':
        template_path = utils.working_dir +'/'
    #Source = spectra.Template(1, type_source = type_source) # first argument is just an ID number
    #Source.LoadTemplate_File(template_path+template_fits, bp, mag=mag, mag_type=mag_type, E_BV = E_BV, Extinction_model=Extinction_model, redshift = redshift )
    if verbose:
        print('[INFO] | TEMPLATE PROPERTIES')
        print('[INFO] |--- Name %s ' % (template_fits))
        print(f'[INFO] |--- {type_source}')
        print(f'[INFO] |--- E(B-V)= {E_BV} {Extinction_model}')
        print(f'[INFO] |--- Redshift {redshift}')

    if Obs_conf['band'] in ['All','all','ALL']:
        if isinstance(template_fits, str):
            results = run_1obj_allbands(template_path+template_fits, type_source, mag, mag_type, bp, Obs_conf, redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV, atm_disp = atm_disp, ApLoss = ApLoss, verbose=verbose, save_plots = save_plots, save_fits = save_fits, debug = debug)
        else:
            results = run_1obj_allbands(template_fits, type_source, mag, mag_type, bp, Obs_conf, redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV, atm_disp = atm_disp, ApLoss = ApLoss, verbose=verbose, save_plots = save_plots, save_fits = save_fits, debug = debug)
            
    else :
        if isinstance(template_fits, str):
            results = run_1obj_1band(template_path+template_fits, type_source, mag, mag_type, bp, Obs_conf, redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV, atm_disp = atm_disp, ApLoss = ApLoss, verbose=verbose, save_plots = save_plots, save_fits = save_fits, debug = debug)
        else:
            results = run_1obj_1band(template_fits, type_source, mag, mag_type, bp, Obs_conf, redshift = redshift, Extinction_model = Extinction_model , E_BV = E_BV, atm_disp = atm_disp, ApLoss = ApLoss, verbose=verbose, save_plots = save_plots, save_fits = save_fits, debug = debug)            
    return results
