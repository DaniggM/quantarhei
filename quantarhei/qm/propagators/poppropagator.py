# -*- coding: utf-8 -*-
import numpy
#from ...core.time import TimeAxis

class PopulationPropagator:
    """ Propagator for a population vector 
        
    The most important method of this class is the method `propagate`.
    It takes initial population vector and propagates it using the time values
    specified by TimaAxis.
    
    Parameters
    ----------
    
    timeaxis: TimeAxis
        The time interval on which we propagate.
        
    RateMatrix: float array of rank 2
        Rate matrix used to propagate the populations
        
        
    Examples
    --------
    
    """   
    
    def __init__(self, timeaxis, rate_matrix=None):

        self.timeAxis = timeaxis
        self.Nref = 1
        self.Nt = self.timeAxis.length
        self.dt = self.timeAxis.step
        
        if rate_matrix is not None:
            self.KK = rate_matrix
    
    def propagate(self, pini):
        """Propagates a given initional population vector
        
        """
        if not isinstance(pini, numpy.ndarray):
            pini = numpy.array(pini)
            
        return self._propagate_short_exp(pini)    
        
        
    def _propagate_short_exp(self,pini,L=4):
        """Propagation of the initial pop vector by short time expansion
        
        Propagates initial population vector by a give rate matrix with
        constant coefficients
        
        
        """
        Nt = self.timeAxis.length
        pops = numpy.zeros((Nt,pini.shape[0]))

        pops[0,:] = pini
        
        rho1 = pini
        rho2 = pini
        
        indx = 1
        for ii in self.timeAxis.data[1:self.Nt]:
                                   
            for jj in range(0, self.Nref):
                
                for ll in range(1,L+1):
                    
                    pref = (self.dt/ll) 
                    rho1 = pref*numpy.dot(self.KK.data,rho1)
                             
                    rho2 = rho2 + rho1
                rho1 = rho2    
                
            pops[indx,:] = rho2                        
            indx += 1             
            
        return pops
        
    
    def get_PropagationMatrix(self, timeaxis, corrections=-1):
        """Returns propagation matrix corresponding to the present propagator
        
        
        Examples
        --------
        
        >>> from quantarhei import TimeAxis
        >>> ta = TimeAxis(0.0, 1000, 1.0)
        >>> ts = TimeAxis(0.0, 10, 10.0)
        >>> KK = [[-1.0/100.0,  1.0/100.0],
        ...       [ 1.0/100.0, -1.0/100.0]]
        >>> prop = PopulationPropagator(ta, RateMatrix=numpy.array(KK))
        >>> U = prop.get_PropagationMatrix(ts)
        >>> print(U[:,:,0])
        [[ 1.  0.]
         [ 0.  1.]]
        
        
        """
        if timeaxis.is_subset_of(self.timeAxis):
            N = self.KK.shape[0]
            U = numpy.zeros((N,N,timeaxis.length), dtype=numpy.float64)
            
            # initial condition
            U0 = numpy.eye(N)
            
            # diagonalization of the rate matrix
            Kd, SS = numpy.linalg.eig(self.KK)
            S1 = numpy.linalg.inv(SS)

            
            # calculating exp(KK*step)
            expKd_step = numpy.dot(SS,numpy.dot(
                    numpy.diag(numpy.exp(Kd*timeaxis.step)),S1))

            #
            # If the starts of the time axes do not coincide, and the
            # shift is not a multiple of the submitted time axis step,
            # we have to calculate the evolution matrix also with
            # the difference of the starting times
            #
            if self.timeAxis.start != timeaxis.start:

                
                # get the distance of the starts in timeaxis.steps
                Ns = round((timeaxis.start - self.timeAxis.start)
                            /timeaxis.step)
                # if one can use timeaxis.step, make Ns steps 
                if (timeaxis.start == self.timeAxis.start + Ns*timeaxis.step):
                    for i in range(Ns):
                        U0 = numpy.dot(expKd_step,U0)
                # otherwise new exp(KK*dt) has to be calculated and applied
                else:
                    dt = timeaxis.start - self.timeAxis.start
                    expKd_dt = numpy.dot(SS,numpy.dot(
                            numpy.diag(numpy.exp(Kd*dt)),S1))
                    U0 = numpy.dot(expKd_dt,U0)
                    
            # initial condition at the start of the submitted timeaxis            
            U[:,:,0] = U0
 
            # application of the exp(KK*step) on initial condition
            for i in range(1,timeaxis.length):
                U[:,:,i] = numpy.dot(expKd_step,U[:,:,i-1])
                
                
            if corrections > -1:
            
                KKD = numpy.zeros(N, dtype=numpy.float64)
                KKT = numpy.zeros((N,N), dtype=numpy.float64)
                for i in range(N):
                    KKD[i] = -self.KK[i,i]
                KKT = self.KK+numpy.diag(KKD)

                
                # zero's order correction to the evolution matrix
                Uc0 = numpy.zeros((N,N,timeaxis.length), dtype=numpy.float64)
                for i in range(N):
                    Uc0[i,i,:] = numpy.exp(-KKD[i]*timeaxis.data) 
                    
                if corrections == 0:
                    return U, Uc0
                
                
                # first order correction
                Uc1 = numpy.zeros((N,N,timeaxis.length), dtype=numpy.float64)
                for i in range(N):
                    for j in range(N):
                        if i != j:
                            if KKD[i] == KKD[j]:
                                Uc1[i,j,:] = KKT[i,j]*timeaxis.data
                            else:
                                Uc1[i,j,:] = (
                                (KKT[i,j]/(KKD[i]-KKD[j]))
                                *(numpy.exp(-KKD[j]*timeaxis.data) 
                                - numpy.exp(-KKD[i]*timeaxis.data)))
                                
                if corrections == 1:
                    return U, Uc0, Uc1
                                
                # second order correction
                Uc2 = numpy.zeros((N,N,timeaxis.length), dtype=numpy.float64)
                for i in range(N):
                    for j in range(N):

                        for k in range(N):
                            
                            if (k != j):
                                if (i != j):
                                    # two parts of an expressions for i != i
                                    Uc2[i,j,:] += (
                                    (KKT[i,k]*KKT[k,j]/(KKD[k]-KKD[j]))
                                    *((numpy.exp(-KKD[j]*timeaxis.data) - 
                                       numpy.exp(-KKD[i]*timeaxis.data))
                                      /(KKD[i]-KKD[j]))
                                    )
                                    if (k != i):
                                        Uc2[i,j,:] -= (
                                        (KKT[i,k]*KKT[k,j]/(KKD[k]-KKD[j]))
                                        *((numpy.exp(-KKD[k]*timeaxis.data) -
                                           numpy.exp(-KKD[i]*timeaxis.data))
                                          /(KKD[i]-KKD[k]))
                                        )
                                else: 
                                    # whole expression for i = j
                                    Uc2[i,j,:] += (
                                    (KKT[i,k]*KKT[k,j]/(KKD[k]-KKD[j]))
                                    *(numpy.exp(-KKD[i]*timeaxis.data)
                                      *timeaxis.data
                                    -(numpy.exp(-KKD[k]*timeaxis.data)
                                     -numpy.exp(-KKD[i]*timeaxis.data))
                                     /(KKD[i]-KKD[k]))
                                    ) 
                                    pass
                                    
                if corrections >= 2:
                    return U, Uc0, Uc1, Uc2
                
            
            else:
                return U
            
        else:
            raise Exception("TimeAxis is not a subset of the internal"
                            +" TimeAxis of this propagator.")
            