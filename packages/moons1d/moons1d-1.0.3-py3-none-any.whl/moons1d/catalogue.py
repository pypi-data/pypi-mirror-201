import numpy as np

from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii
import random

# Catalogue

class Catalogue:

    def __init__(self, id, survey_name, nTarget):
        self.id = id
        self.survey_name = survey_name
        self.targets = []

        for i in range(nTarget):
            new_target = Target(i)
            new_target.setname("%s_%s" % (survey_name, i))
            new_target.setOutFile("%s_%s.fits" % (survey_name, i))
            self.targets.append(new_target)

    def set_mag_distribution(self, mag_range, mag_band, mag_type,  target_type ="point-source", type_distribution ='uniform'):
        nTarget = len(self.targets)
        if type_distribution == 'uniform':
            mags = np.random.uniform(mag_range[0], mag_range[1], nTarget)

        if type_distribution == 'normal':
            mags = np.random.normal(mag_range[0], mag_range[1], nTarget)

        i=0
        for target in self.targets:
            target.setMag(mags[i], mag_type, mag_band)
            target.type_source = target_type
            i+=1
        return

    def set_redshift_distribution(self, redshift_range,  type_distribution='uniform'):
        nTarget = len(self.targets)
        if type_distribution == 'uniform':
            redshifts = np.random.uniform(redshift_range[0], redshift_range[1], nTarget)

        if type_distribution == 'normal':
            redshifts = np.random.normal(redshift_range[0], redshift_range[1], nTarget)

        i=0
        for target in self.targets:
            target.setRedshift(redshifts[i])
            i+=1
        return

    def set_extinction_distribution(self, E_BV_range, extinction_model='mwavg', type_distribution='uniform'):
        nTarget = len(self.targets)
        if type_distribution == 'uniform':
            E_BV = np.random.uniform(E_BV_range[0], E_BV_range[1], nTarget)

        if type_distribution == 'normal':
            E_BV = np.random.normal(E_BV_range[0], E_BV_range[1], nTarget)

        i=0
        for target in self.targets:
            target.setExtinction(E_BV[i], extinction_model)
            i+=1
        return

    def set_template_distribution(self, template_list):
        for target in self.targets:
            template = random.choice(template_list)
            target.setTemplate(template)
        return

def Save_Catalogue(catalogue, filename):

    data = []

    for target in catalogue:
        row = {"id": target.id, "name": target.name, "RA": target.RA,
               "DEC": target.DEC, "mag": target.mag,
               "mag_filter": target.mag_filter, "template": target.template,
               "type": target.type, "redshift": target.redshift,
               "survey_name": target.survey_name,
               "FileOutput": target.FileOutput}

        data.append(row)

    ascii.write(Table(data), filename, overwrite=True)
    return


class Target:

    def __init__(self, nid):
        self.id = nid
        self.name = ""
        self.RA = 0.0
        self.DEC = 0.0
        self.mag = 0
        self.mag_type = "AB_pivot"
        self.mag_band = "J"
        self.template_fits = ""
        self.type_source = ""  # Point-Source or Extended
        self.redshift = ""
        self.e_bv = 0
        self.extinction_model = ""
        self.FileOutput = ""

    def getinfo(self):
        return "%s: %s | %s (%s) | %s " % (self.id, self.name, self.redshift,
                                           self.mag, self.mag_filter,
                                           self.template)

    def setMag(self, mag, mag_type, mag_filter):
        self.mag = mag
        self.mag_type = mag_type
        self.mag_filter = mag_filter

    def setRedshift(self, redshift):
        self.redshift = redshift

    def setTemplate(self, template):
        self.template_fits = template

    def setname(self, name):
        self.name = name

    def setExtinction(self, e_bv, extinction_model):
        self.e_bv = e_bv
        self.extinction_model = extinction_model

    def setOutFile(self, FileOutput):
        self.FileOutput = FileOutput

    def getFileOutput(self):
        return self.FileOutput

    def getRedshift(self):
        return self.redshift

    def getMag(self):
        return self.mag
