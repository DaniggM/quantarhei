# -*- coding: utf-8 -*-
import unittest

"""
*******************************************************************************


    Tests of the quantarhei.spectroscopy.abs package


*******************************************************************************
"""
import numpy
#import h5py
import tempfile

from quantarhei.spectroscopy.abs2 import AbsSpectrumBase #, AbsSpectrumDifference
from quantarhei import FrequencyAxis
from quantarhei import energy_units
#from quantarhei import convert

from quantarhei import AbsSpectrum, AbsSpectrumCalculator
from quantarhei import Molecule, CorrelationFunction, TimeAxis
#from quantarhei import Aggregate

class TestAbs(unittest.TestCase):
    """Tests for the abs package
    
    
    """
    
    def setUp(self,verbose=False):
        
        abss = AbsSpectrumBase()
        with energy_units("1/cm"):
            f = FrequencyAxis(10000.0,2000, 1.0)
            a = self._spectral_shape(f, [1.0, 11000.0, 100.0])
            abss.axis = f
            abss.data = a
        self.abss = abss
        self.axis = abss.axis
        
        
        
        
        time = TimeAxis(0.0,1000,1.0)
        with energy_units("1/cm"):
            mol1 = Molecule(elenergies=[0.0, 10000.0])
            params = dict(ftype="OverdampedBrownian", reorg=20, cortime=30,
                          T=300)
            mol1.set_dipole(0,1,[0.0, 1.0, 0.0])
            cf = CorrelationFunction(time, params)
            mol1.set_transition_environment((0,1),cf)
            
            self.mol1 = mol1
            
            abs_calc = AbsSpectrumCalculator(time, system=mol1)
            abs_calc.bootstrap(rwa=10000)
            
        abs1 = abs_calc.calculate()
        
        self.abs1 = abs1
        
        
    def _spectral_shape(self, f, par):
        a = par[0]
        fd = par[1]
        sig = par[2]
        with energy_units("1/cm"):
            return a*numpy.exp(-((f.data-fd)/sig)**2)
        
    def _opt_spectral_shape(self, par):
        f = self.axis
        a = AbsSpectrumBase(axis=f,data=self._spectral_shape(f, par))
        return a
        
            
    def test_abs_spectrum_saveablity(self):
        """Testing if AbsSpectrum is saveble
        
        """
        abs1 = self.abs1
        
        #drv = "core"
        #bcs = False
        
        with tempfile.TemporaryFile() as f:
        #with h5py.File('tempfile.hdf5', 
        #               driver=drv, 
        #               backing_store=bcs) as f:
    
            abs1.save(f) #, test=True)
            f.seek(0)
            abs2 = AbsSpectrum()
            abs2 = abs2.load(f) #, test=True)
            
        numpy.testing.assert_array_equal(abs1.data, abs2.data)


    # def test_abs_difference_equal_zero(self):
    #     """Testing calculation of zero difference between abs spectra
        
    #     """
        
    #     #
    #     #  Test difference = 0
    #     # 
    #     par = [1.0, 11000.0, 100.0]
    #     with energy_units("1/cm"):
    #         f2 = self._spectral_shape(self.abss.axis, par) 
        
    #         abss2 = AbsSpectrumBase(axis=self.abss.axis, data=f2)
    #         ad = AbsSpectrumDifference(target=self.abss, optfce=abss2, 
    #                                bounds=(10100.0, 11900.0))
    #     d = ad.difference()
        
    #     self.assertAlmostEqual(d, 0.0)
        
        
        
    # def test_abs_difference_formula(self):
    #     """Testing formula for calculation of difference between abs spectra
        
    #     """

    #     #
    #     #  Test difference formula
    #     #
    #     par = [1.0, 10900.0, 100.0]
    #     with energy_units("1/cm"):
    #         f2 = self._spectral_shape(self.abss.axis, par) 
        
    #         abss2 = AbsSpectrumBase(axis=self.abss.axis, data=f2)
    #         ad = AbsSpectrumDifference(target=self.abss, optfce=abss2, 
    #                                bounds=(10100.0, 11900.0))
    #     d = ad.difference()  
          
    #     #with energy_units("1/cm"):   
    #     if True:
    #         target = self.abss.data[ad.nl:ad.nu]
    #         secabs = abss2.data[ad.nl:ad.nu]
    #         x = self.abss.axis.data[ad.nl:ad.nu]
    #         d2 = 1000.0*numpy.sum(numpy.abs((target-secabs)**2/
    #                                (x[len(x)-1]-x[0])))
        
    #     self.assertAlmostEqual(d, d2)        
        
#    def test_minimize(self):
#        """Testing difference minimization using scipy.optimize package
#        
#        """
#        with energy_units("1/cm"):
#            ad = AbsSpectrumDifference(target=self.abss, 
#                                   optfce=self._opt_spectral_shape, 
#                                   bounds=(10100.0, 11900.0))
#        
#        method = "Nelder-Mead"
#        ini = [0.5, 10900, 80.0]
#        p = ad.minimize(ini, method=method)
#        
#        numpy.testing.assert_array_almost_equal(p, [1.0, 11000.0, 100.0])


    def test_of_molecular_absorption(self):
        """(AbsSpectrum) Testing absorption spectrum of a molecule
        
        """
        mol1 = self.mol1
        time = mol1.get_transition_environment((0,1)).axis
                      
        with energy_units("1/cm"):
            # data for comparison
            x = self.abs1.axis.data
            y = self.abs1.data/3.0
        
                                               
        abs_calc = AbsSpectrumCalculator(time, system=mol1)
        
        # FIXME: RWA does not work correctly yet
        with energy_units("1/cm"):
            abs_calc.bootstrap(rwa=10000)
        
        prop = mol1.get_ReducedDensityMatrixPropagator(time, 
                                                relaxation_theory="stR",
                                                time_dependent=True)
        #prop.setDtRefinement(10)
        
        abs_calc.set_propagator(prop)
        abs1 = abs_calc.calculate(from_dynamics=True)   
        
        with energy_units("1/cm"):
            x1 = abs1.axis.data
            y1 = abs1.data 
        
        diff = numpy.max(numpy.abs(y1-y))
        rdiff = diff/numpy.max(numpy.abs(y))
        
        self.assertTrue(rdiff < 0.01)
        
        _plot_ = False
        if _plot_:
            import matplotlib.pyplot as plt
            plt.plot(x,y,"-b")
            plt.plot(x1,y1,"--r")
            plt.show() 
        
        

if __name__ == '__main__':
    unittest.main()        
        