#######################################################################################################
##################### This file will load clinical goals for evaluation purposes. #####################
####### The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work ########
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

from connect import *

def addClinicalGoal(es, roi, goal, criteria, primary_acceptance, param_value=None, absolute=False,
                    secondary_acceptance=None, priority=2147483647):
    clinicalGoal = es.AddClinicalGoal()
    clinicalGoal.StructureName=roi
    clinicalGoal.GoalType=goal
    clinicalGoal.GoalCriteria=criteria
    clinicalGoal.UseAbsoluteVolume = absolute
    clinicalGoal.ParameterValue=param_value
    clinicalGoal.AcceptanceLevel=primary_acceptance
    clinicalGoal.Priority=priority
    
    if secondary_acceptance is not None:
        clinicalGoal.SecondaryAcceptanceLevel = secondary_acceptance
    
    return clinicalGoal