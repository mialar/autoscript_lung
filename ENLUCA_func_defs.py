#######################################################################################################
## This file will define objective/ constraint functions for use in scripting in RayStation v.2024b. ##
####### The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work ########
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

from connect import *


# Function for adding min dose to roi.
# Inputs: roi, minimum dose level, weight, if it is constraint (default False)
# if it is robust (default False), and if it uses RBE dose (default True).
# Output: objective/constraint name for editing
def minDose(po, roi, dose, o_num, c_num, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):

        objective = po.AddOptimizationFunction(FunctionType="MinDose", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding max dose to roi.
# Inputs: roi, maximum dose level, weight, if it is constraint (default False)
# if it is robust (default False), and if it uses RBE dose (default True).
# Output: objective/constraint name for editing
def maxDose(po, roi, dose, o_num, c_num, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="MaxDose", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding min DVH to ROI
# Inputs: roi, dose level, volume (percentage or absolute), absoluteVolume: true if absolute volume, default to False,
# weight, if it is constraint (default False)
# if it is robust (default False), and if it uses RBE dose (default True).
# Output: objective/constraint name for editing
def minDVH(po, roi, dose, volume, o_num, c_num, absoluteVolume=False, weight=1, constraint=False, robust=False,
           rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="MinDvh", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            if absoluteVolume == True:
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.AbsoluteVolume = volume
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.IsAbsoluteVolume = absoluteVolume
            else:
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.PercentVolume = volume

            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num

        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            if absoluteVolume == True:
                po.Constraints[c_num].DoseFunctionParameters.AbsoluteVolume = volume
                po.Constraints[c_num].DoseFunctionParameters.IsAbsoluteVolume = absoluteVolume
            else:
                po.Constraints[c_num].DoseFunctionParameters.PercentVolume = volume

            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding max DVH to ROI
# Inputs: roi, dose level, volume (percentage or absolute), absoluteVolume: true if absolute volume, default to False,
# weight, if it is constraint (default False)
# if it is robust (default False), and if it uses RBE dose (default True).
# Output: objective/constraint name for editing
def maxDVH(po, roi, dose, volume, o_num, c_num, absoluteVolume=False, weight=1, constraint=False, robust=False,
           rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="MaxDvh", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            if absoluteVolume == True:
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.AbsoluteVolume = volume
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.IsAbsoluteVolume = absoluteVolume
            else:
                po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.PercentVolume = volume

            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num-1].DoseFunctionParameters, o_num

        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            if absoluteVolume == True:
                po.Constraints[c_num].DoseFunctionParameters.AbsoluteVolume = volume
                po.Constraints[c_num].DoseFunctionParameters.IsAbsoluteVolume = absoluteVolume
            else:
                po.Constraints[c_num].DoseFunctionParameters.PercentVolume = volume

            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding min EUD to ROI
# Inputs: roi, dose level, value of the parameter A (default to 1) according to the EUD equation, values may range from -150 to 1.0,
# weight, if constraint or robust (both default False), and if it uses RBE dose (default True)
# !!! Include a change of the parameter A!!!
# Output: objective/constraint name for editing
def minEUD(po, roi, dose, o_num, c_num, A=1, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="MinEUD", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.EudParameterA = A
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            po.Constraints[c_num].DoseFunctionParameters.EudParameterA = A
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding max EUD to ROI
# Inputs: roi, dose level, weight, if constraint or robust (both default False), and if it uses RBE dose (default True)
# !!! Include a change of the parameter A!!!
# Output: objective/constraint name for editing
def maxEUD(po, roi, dose, o_num, c_num, A=1, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="MaxEUD", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.EudParameterA = A
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            po.Constraints[c_num].DoseFunctionParameters.EudParameterA = A
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding target EUD to ROI
# Inputs: roi, dose level, weight, if constraint or robust (both default False), and if it uses RBE dose (default True)
# !!! Include a change of the parameter A!!!
# Output: objective/constraint name for editing
def targetEUD(po, roi, dose, o_num, c_num, A=1, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="TargetEUD", RoiName=roi, IsConstraint=constraint,
                                               IsRobust=robust, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.DoseLevel = dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.EudParameterA = A
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.DoseLevel = dose
            po.Constraints[c_num].DoseFunctionParameters.EudParameterA = A
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for adding dose fall-off to ROI
# Inputs: roi, high and low dose levels (default 66 and 0 Gy, respectively), dose fall off distance (default 2 cm),
# weight (default 1), constraint and robust both default False, if it uses RBE dose (default True)
# Output: objective/constraint name for editing
def fall_off(po, roi, o_num, c_num, high_dose=66, low_dose=0, distance=2, weight=1, constraint=False, robust=False, rbe=True):
    with CompositeAction('Add optimization function'):
        objective = po.AddOptimizationFunction(FunctionType="DoseFallOff", RoiName=roi, IsConstraint=constraint,
                                               RestrictAllBeamsIndividually=False, RestrictToBeams=[], IsRobust=robust, RestrictToBeamSet=None, UseRbeDose=rbe)
        if constraint == False:
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.HighDoseLevel = high_dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.LowDoseLevel = low_dose
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.LowDoseDistance = distance
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.AdaptToTargetDoseLevels = True
            po.Objective.ConstituentFunctions[o_num].DoseFunctionParameters.Weight = weight
            o_num += 1
            return po.Objective.ConstituentFunctions[o_num - 1].DoseFunctionParameters, o_num
        else:
            po.Constraints[c_num].DoseFunctionParameters.HighDoseLevel = high_dose
            po.Constraints[c_num].DoseFunctionParameters.LowDoseLevel = low_dose
            po.Constraints[c_num].DoseFunctionParameters.LowDoseDistance = distance
            c_num += 1
            return po.Constraints[c_num - 1].DoseFunctionParameters, c_num


# Function for editing objective
def edit_objective(obj_name, dose, weight=1):
    with CompositeAction('Edit optimization function'):
        obj_name.DoseLevel = dose
        obj_name.Weight = weight


# Function for editing constraint
def edit_constraint(const_name, dose):
    with CompositeAction('Edit optimization function'):
        const_name.DoseLevel = dose


# Function for setting optimization parameters
# Inputs: max number of iterations, optimality tolerance (format of i.e., 1E-08), number of iterations before spot weight bounding,
# position uncertainties (same in all directions), density uncertainty
# Default parameters: 100 iterations, tolerance 1E-08, 40 iterations before spot weight bounding, position uncertainty of 0.5 cm,
# density uncertainty of 3.5%
def optimization_parameters(po, iter=100, tolerance=1E-08, spot_weight=40, pos_uncert=0.5, dens_uncert=0.035):
    opt_param = po.OptimizationParameters

    with CompositeAction('Set optimization parameters'):
        opt_param.Algorithm.MaxNumberOfIterations = iter
        opt_param.Algorithm.OptimalityTolerance = tolerance
        opt_param.PencilBeamScanningProperties.NumberOfIterationsBeforeSpotWeightBounding = spot_weight
        opt_param.SaveRobustnessParameters(PositionUncertaintyAnterior=pos_uncert,
                                           PositionUncertaintyPosterior=pos_uncert,
                                           PositionUncertaintySuperior=pos_uncert,
                                           PositionUncertaintyInferior=pos_uncert,
                                           PositionUncertaintyLeft=pos_uncert, PositionUncertaintyRight=pos_uncert,
                                           DensityUncertainty=dens_uncert, PositionUncertaintySetting="Universal",
                                           IndependentLeftRight=True, IndependentAnteriorPosterior=True,
                                           IndependentSuperiorInferior=True, ComputeExactScenarioDoses=False,
                                           NamesOfNonPlanningExaminations=[],
                                           PatientGeometryUncertaintyType="PerTreatmentCourse",
                                           PositionUncertaintyType="PerTreatmentCourse",
                                           TreatmentCourseScenariosFactor=1000)