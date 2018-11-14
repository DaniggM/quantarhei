"""

    Autogenerated by ghenerate script, part of Quantarhei
    http://github.com/tmancal74/quantarhei
    Tomas Mancal, tmancal74@gmai.com

    Generated on: 2018-11-12 14:35:11

    Edit the functions below to give them desired functionality.
    In present version of `ghenerate`, no edits or replacements
    are perfomed in the feature file text.

"""
import numpy

from behave import given
from behave import when
from behave import then

import quantarhei as qr

#
# Given ...
#
@given('that I have an aggregate of three molecules with no dephasing set')
def step_given_1(context):
    """

        Given that I have an aggregate of three molecules with no dephasing set

    """
    agg = qr.TestAggregate("trimer-2")
    
    with qr.energy_units("1/cm"):
        agg.set_resonance_coupling(0,1, 100.0)
    agg.build()
    
    context.agg = agg


#
# When ...
#
@when('I ask the aggregate to return PureDephasing object')
def step_when_2(context):
    """

        When I ask the aggregate to return PureDephasing object

    """
    agg = context.agg
    
    pd = agg.get_PureDephasing()
    
    context.pd = pd


#
# Then ...
#
@then('I get an empty PureDephasing object')
def step_then_3(context):
    """

        Then I get an empty PureDephasing object

    """
    pd = context.pd
    
    agg = context.agg
    Ntot = agg.Ntot
    
    comp = numpy.zeros((Ntot,Ntot), dtype=qr.REAL)

    numpy.testing.assert_allclose(comp, pd.data)


#
# Given ...
#
@given('that I have an aggregate of three molecules with dephasing rates set')
def step_given_4(context):
    """

        Given that I have an aggregate of three molecules with dephasing rates set

    """
    agg = qr.TestAggregate("trimer-2")
    
    for mol in agg.monomers:
        mol.set_transition_width((0,1), 1.0/100.0)

    with qr.energy_units("1/cm"):
        agg.set_resonance_coupling(0,1, 100.0)
        
    agg.build()
    
    context.agg = agg


#
# Then ...
#
@then('I get a PureDephasing object with some rates')
def step_then_5(context):
    """

        Then I get a PureDephasing object with some rates

    """
    pd = context.pd
    
    agg = context.agg
    Ntot = agg.Ntot
    
    comp = numpy.zeros((Ntot,Ntot), dtype=qr.REAL)
    a1 = numpy.array(comp.shape)
    a2 = numpy.array(pd.data.shape)

    numpy.testing.assert_allclose(a1, a2)    


#
# Given ...
#
@given('that I have an aggregate of two identical molecules with dephasing rates set')
def step_given_6(context):
    """

        Given that I have an aggregate of two identical molecules with dephasing rates set

    """
    agg = qr.TestAggregate("homodimer-2")
    
    for mol in agg.monomers:
        mol.set_transition_width((0,1), 1.0/100.0)

    with qr.energy_units("1/cm"):
        agg.set_resonance_coupling(0,1, 100.0)
        
    agg.build()
    
    context.agg = agg

#
# Then ...
#
@then('I get a PureDephasing object with electronic dephasing rates equal to zero')
def step_then_7(context):
    """

        Then I get a PureDephasing object with electronic dephasing rates equal to zero

    """
    pd = context.pd
    
    a1 = pd.data
    a2 = numpy.zeros(pd.data.shape, dtype=qr.REAL)
    a2[:,:] = a1
    a2[1,2] = 0.0
    a2[2,1] = 0.0
    
    numpy.testing.assert_allclose(a1, a2)

#
# Given ...
#
@given('that I have an aggregate of two molecules with nuclear mode each and with electronic dephasing rates set')
def step_given_8(context):
    """

        Given that I have an aggregate of two molecules with nuclear mode each and with electronic dephasing rates set

    """
    agg = qr.TestAggregate("dimer-2-vib")
    
    for mol in agg.monomers:
        mol.set_transition_width((0,1), 1.0/100.0)

    with qr.energy_units("1/cm"):
        agg.set_resonance_coupling(0,1, 100.0)
        
    agg.build()
    
    context.agg = agg
