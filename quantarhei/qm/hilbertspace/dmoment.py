# -*- coding: utf-8 -*-

from .operators import SelfAdjointOperator
from ...core.managers import BasisManaged

import numpy
#import scipy


class TransitionDipoleMoment(SelfAdjointOperator, BasisManaged):
    
    def __init__(self, dim=None, data=None):
        
        if not ((dim is None) and (data is None)):        
            # Set the currently used basis
            cb = self.manager.get_current_basis()
            self.set_current_basis(cb)
            # unless it is the basis outside any context
            if cb != 0:
                self.manager.register_with_basis(cb,self) 
    
            self._data = data
            self.dim = self._data.shape[0] 
            
            if not self.check_selfadjoint():
                raise Exception("The data of this operator have"
                +" to be represented by 3 selfadjoint matrices") 
         
 
    def check_selfadjoint(self):
        a = numpy.allclose(numpy.transpose(numpy.conj(self._data[:,:,0])), 
         self._data[:,:,0])        
        b = numpy.allclose(numpy.transpose(numpy.conj(self._data[:,:,1])), 
         self._data[:,:,1])
        c = numpy.allclose(numpy.transpose(numpy.conj(self._data[:,:,2])), 
         self._data[:,:,2])
        return (a and b) and c   
        
    def transform(self,SS,inv=None):
        """
        This function transforms the Operator into a different basis, using
        a given transformation matrix.
        """
        if inv is None:
            S1 = numpy.linalg.inv(SS)
        else:
            S1 = inv
        #S1 = scipy.linalg.inv(SS)
        for i in range(3):
            self._data[:,:,i] = numpy.dot(S1,numpy.dot(self._data[:,:,i],SS))
        
          
    def dipole_strength(self, from_state=None, to_state=None, transition=None):
        """Calculates transition dipole strength between two states
        
        Current usage is:
        
        ds = dip.dipole_strength(transition=(0,1))
        
        deprecated use is
        
        ds = dip.dipole_strength(from_state=0, to_state=1)
        
        """
        # FIXME: it should be possibe to call just dipole_strength((0,1))
        if to_state is None:
            fstate = transition[0]
            tstate = transition[1]
        else:
            fstate = from_state
            tstate = to_state
        d = numpy.zeros(3,dtype=numpy.float64)        
        for i in range(3):        
            d[i] = self.data[fstate,tstate,i]
        return numpy.dot(d,d)
    
    def get_compoment_data(self, n):
        """Returns a component data of the transition dipole moment operator
        
        """
        return self.data[:,:,n]
    
    def get_component(self, n):
        """Returns a component of the transition dipole moment operator
        
        """
        return SelfAdjointOperator(dim=self.dim, data=self.data[:,:,n])
    
    def get_dipole_length_operator(self):
        """Returns operator composed of the dipole strengths
        
        """
        d = numpy.zeros(3,dtype=numpy.float64)   
        dat = numpy.zeros((self.dim, self.dim), dtype=numpy.float64)
        for k in range(self.dim):
            for l in range(self.dim):
                for i in range(3):        
                    d[i] = self.data[k,l,i]
                dat[k,l] = numpy.sqrt(numpy.dot(d,d))
                
        return SelfAdjointOperator(data=dat)
    
    
