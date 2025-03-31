#######################################################################################################
##################### This file will load clinical goals for evaluation purposes. #####################
####### The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work ########
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

from connect import *

def addClinicalGoal(roi, goalCriteria, goalType, primaryAcceptanceLevel, 
                    secondaryAcceptanceLevel=None, parameterValue=0, isComparativeGoal=False,
                    beamSet=beamset, priority=2147483647, associateToPlan=False):
    clinicalGoal = plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=roi, GoalCriteria=goalCriteria, GoalType=goalType,
                                                         PrimaryAcceptanceLevel=primaryAcceptanceLevel, SecondaryAcceptanceLevel=secondaryAcceptanceLevel,
                                                         ParameterValue=parameterValue, IsComparativeGoal=isComparativeGoal, BeamSet=beamset, 
                                                         Priority=priority, AssociateToPlan=associateToPlan)
    return clinicalGoal

# Possible values for input for clinical goals:
