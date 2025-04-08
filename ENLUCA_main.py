#######################################################################################################
######### This file will run automatic plan optimization for LA-NSCLC with input beam angles. #########
####### The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work ########
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

from connect import *
from tkinter import *
from tkinter import Tk, Label, Button, Frame, X, simpledialog
from tkinter import ttk
from ENLUCA_struct_gui import structure_lists, structure_gui, dict_unpack
from ENLUCA_beam_gui import beam_gui
from ENLUCA_func_defs import *


try:
    db = get_current("PatientDB")
    patient = get_current("Patient")
    case = get_current("Case")
    patient_model = case.PatientModel
    examination = get_current("Examination")
    structure_set = patient_model.StructureSets[examination.Name]
except:
    print('Pasient/case/CT er ikke lastet. Skriptet stoppes.')
    exit()

ui = get_current('ui')
ui.TitleBar.Navigation.MenuItem['Plan design'].Button.Click()

ctv_list, gtv_list, oar_list = structure_lists(patient_model)
struct_dict = structure_gui(ctv_list, gtv_list, oar_list)
ctv, ctvp, ctvn, ictv_gtv, gtvp, boost, gtvn, nodeboost, body, lungs, heart, esophagus, spinal, chestwall, mediastinum, trachea, bronchi, aorta, plexus, expanded = dict_unpack(
    struct_dict)
ba1, ba2, ba3 = beam_gui()

# Add expanded CTV for dose restriction:
if not expanded:
    with CompositeAction(f'Expand (ICTV_expanded, Image set: Legeinntegning 20%)'):
        retval_0 = case.PatientModel.CreateRoi(Name="ICTV_expanded", Color="Cyan", Type="Ctv", TissueName=None,
                                               RbeCellTypeName=None, RoiMaterial=None)
        retval_0.SetMarginExpression(SourceRoiName=ctv,
                                     MarginSettings={'Type': "Expand", 'Superior': 2, 'Inferior': 2, 'Anterior': 2,
                                                     'Posterior': 2, 'Right': 2, 'Left': 2})
        retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# If no ICTVp-IGTVp donut exists, create one using ROI algebra
if not ictv_gtv:
    with CompositeAction('ROI algebra (ICTVp-IGTVp, Image set: Legeinntegning 20%)'):
        retval_0 = case.PatientModel.CreateRoi(Name="ictvp_igtvp", Color="Pink", Type="Ctv", TissueName=None,
                                               RbeCellTypeName=None, RoiMaterial=None)
        retval_0.SetAlgebraExpression(ExpressionA={'Operation': "Union", 'SourceRoiNames': [ctvp],
                                                   'MarginSettings': {'Type': "Expand", 'Superior': 0, 'Inferior': 0,
                                                                      'Anterior': 0, 'Posterior': 0, 'Right': 0,
                                                                      'Left': 0}},
                                      ExpressionB={'Operation': "Union", 'SourceRoiNames': [gtvp],
                                                   'MarginSettings': {'Type': "Expand", 'Superior': 0, 'Inferior': 0,
                                                                      'Anterior': 0, 'Posterior': 0, 'Right': 0,
                                                                      'Left': 0}}, ResultOperation="Subtraction",
                                      ResultMarginSettings={'Type': "Expand", 'Superior': 0, 'Inferior': 0,
                                                            'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0})
        retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Contours", Resolution=0.025)

# ----------------------- Add treatment plan -------------------------

# Create a simple tkinter window
root = Tk()
root.withdraw()  # Hide the main window

# Show an input dialog
plan_name = simpledialog.askstring("Input Required", "Please enter the name of the plan:")

if not plan_name:
    messagebox.showwarning("Warning", "No input provided.")

MAX_PLAN_NAME_LENGTH = 16  # Adjust this limit based on what the system allows

# Ensure plan name does not exceed the maximum length
if plan_name and len(plan_name) > MAX_PLAN_NAME_LENGTH:
    plan_name = plan_name[:MAX_PLAN_NAME_LENGTH]  # Truncate to fit

new_plan = case.AddNewPlan(PlanName=plan_name, ExaminationName=examination.Name)
patient.Save()
new_plan.SetCurrent()

new_bs = new_plan.AddNewBeamSet(Name=plan_name, ExaminationName=examination.Name, MachineName="PB360_OSU",
                                Modality="Protons", TreatmentTechnique="ProtonPencilBeamScanning",
                                PatientPosition="HeadFirstSupine", NumberOfFractions=33, RbeModelName="Constant 1.1")
new_bs.SetDefaultDoseGrid(VoxelSize={'x': 0.3, 'y': 0.3, 'z': 0.3})

ctv_center = structure_set.RoiGeometries[ctv].GetCenterOfRoi()
iso_data = new_bs.CreateDefaultIsocenterData(Position=ctv_center)
if ba1:
    beam_1 = new_bs.CreatePBSIonBeam(SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=6,
                                     IsocenterData=iso_data, Name="Beam 1", GantryAngle=ba1)
if ba2:
    beam_2 = new_bs.CreatePBSIonBeam(SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=6,
                                     IsocenterData=iso_data, Name="Beam 2", GantryAngle=ba2)
if ba3:
    beam_3 = new_bs.CreatePBSIonBeam(SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=6,
                                     IsocenterData=iso_data, Name="Beam 3", GantryAngle=ba3)

await_user_input(
    'Ready to start optimization? Check beam angles, range shifter, air gap, optimization algorithm (Monte Carlo 10000 ions/spot), dose algorithm (Monte Carlo 0.5% uncert.). Resume script execution.')

patient.Save()

ui.TitleBar.Navigation.MenuItem['Plan optimization'].Button.Click()
plan = get_current("Plan")
beam_set = get_current("BeamSet")

obj_num = 0
const_num = 0

po = plan.PlanOptimizations[0]
# es=evaluation setup, abbrieviated to avoid length names
es=plan.TreatmentCourse.EvaluationSetup



# CTV optimization functions
if ctv:
    ctv_minDose, const_num = minDose(po, roi=ctv, dose=6500, o_num=obj_num, c_num=const_num, constraint=True)
    ctv_minDVH, const_num = minDVH(po, roi=ctv, dose=6500, volume=100, o_num=obj_num, c_num=const_num, constraint=True, robust=True)
    ctv_dose_fall_off, obj_num = fall_off(po, roi=ctv, o_num=obj_num, c_num=const_num, high_dose=9500, low_dose=6600, distance=0.4, weight=100)
    ctv_maxDose, const_num = maxDose(po, roi=ctv, dose=11500, o_num=obj_num, c_num=const_num, constraint=True)
    ctv_v100, obj_num = maxDVH(po, roi=ctv, dose=10000, volume=30, o_num=obj_num, c_num=const_num, absoluteVolume=True, weight=100)
    ctv_v105, obj_num = maxDVH(po, roi=ctv, dose=10500, volume=5, o_num=obj_num, c_num=const_num, absoluteVolume=True, weight=100)
    
    # Add clinical goals
    es.AddClinicalGoal(RoiName=ctv, GoalCriteria="AtLeast", GoalType="AverageDose", PrimaryAcceptanceLevel=6270,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=ctv, GoalCriteria="AtMost", GoalType="AbsoluteVolumeAtDose", ParameterValue=10000, PrimaryAcceptanceLevel=30,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=ctv, GoalCriteria="AtMost", GoalType="AbsoluteVolumeAtDose", ParameterValue=10500, PrimaryAcceptanceLevel=5,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=ctv, GoalCriteria="AtLeast", GoalType="VolumeAtDose", ParameterValue=6270, PrimaryAcceptanceLevel=1,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=ctv, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=0.03, PrimaryAcceptanceLevel=11500,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if expanded:
    expanded_maxDose, obj_num = maxDose(po, roi=expanded, dose=7400, o_num=obj_num, c_num=const_num,
                               weight=1500, robust=True)
    expanded_fall_off, obj_num = fall_off(po, roi=expanded, o_num=obj_num, c_num=const_num, high_dose=9500, low_dose=6270, distance=1, weight=1000)

if ictv_gtv:
    ictv_gtv_maxDose, obj_num = maxDose(po, roi=ictv_gtv, dose=8000, o_num=obj_num, c_num=const_num,
                               weight=1500, robust=False)
    ictv_gtv_median, obj_num = maxDVH(po, roi=ictv_gtv, dose=7500, volume=50, o_num=obj_num, c_num=const_num,
                             weight=1500)

if body:
    body_maxDose, obj_num = maxDose(po, roi=body, dose=11500, o_num=obj_num, c_num=const_num, weight=1500)
    body_fall_off, obj_num = fall_off(po, roi=body, o_num=obj_num, c_num=const_num, high_dose=6600, low_dose=0, distance=2)

if spinal:
    spinal_maxDose, const_num = maxDose(po, roi=spinal, dose=4400, o_num=obj_num, c_num=const_num, constraint=True)
    spinal_PRV, obj_num = maxDose(po, roi=spinal, dose=5000, o_num=obj_num, c_num=const_num, weight=100, robust=True)
    
    es.AddClinicalGoal(RoiName=spinal, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=0.05, PrimaryAcceptanceLevel=5000,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if heart:
    heart_maxDose, obj_num = maxDose(po, roi=heart, dose=7400, o_num=obj_num, c_num=const_num, weight=1500)
    heart_meanDose, obj_num = maxEUD(po, roi=heart, dose=500, o_num=obj_num, c_num=const_num, weight=1500)
    heart_fall_off, obj_num = fall_off(po, roi=heart, o_num=obj_num, c_num=const_num, high_dose=6600, low_dose=0, distance=1)
    
    es.AddClinicalGoal(RoiName=heart, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=heart, GoalCriteria="AtMost", GoalType="AverageDose", PrimaryAcceptanceLevel=500,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=heart, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=2500, PrimaryAcceptanceLevel=0.50,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=heart, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=4000, PrimaryAcceptanceLevel=0.30,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=heart, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=5000, PrimaryAcceptanceLevel=0.20,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if esophagus:
    esophagus_maxDose, obj_num = maxDose(po, roi=esophagus, dose=6900, o_num=obj_num, c_num=const_num, weight=5000, robust=False)
    esophagus_PRV, obj_num = maxDose(po, roi=esophagus, dose=7400, o_num=obj_num, c_num=const_num, weight=5000, robust=True)
    
    es.AddClinicalGoal(RoiName=esophagus, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7000,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=esophagus, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=3500, PrimaryAcceptanceLevel=0.40,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)


if chestwall:
    chestwall_maxDose, const_num = maxDose(po, roi=chestwall, dose=7300, o_num=obj_num, c_num=const_num, constraint=True)
    es.AddClinicalGoal(RoiName=chestwall, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if mediastinum:
    mediastinum_maxDose, const_num = maxDose(po, roi=mediastinum, dose=7200, o_num=obj_num, c_num=const_num, constraint=True)
    es.AddClinicalGoal(RoiName=mediastinum, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if trachea:
    trachea_maxDose, obj_num = maxDose(po, roi=trachea, dose=7300, o_num=obj_num, c_num=const_num, weight=1500, robust=False)
    trachea_PRV, obj_num = maxDose(po, roi=trachea, dose=7800, o_num=obj_num, c_num=const_num, weight=1500, robust=True)
    
    es.AddClinicalGoal(RoiName=trachea, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if bronchi:
    bronchi_maxDose, obj_num = maxDose(po, roi=bronchi, dose=7300, o_num=obj_num, c_num=const_num, weight=5000, robust=False)
    bronchi_PRV, obj_num = maxDose(po, roi=bronchi, dose=7800, o_num=obj_num, c_num=const_num, weight=5000, robust=True)
    es.AddClinicalGoal(RoiName=bronchi, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if aorta:
    aorta_maxDose, obj_num = maxDose(po, roi=aorta, dose=7300, o_num=obj_num, c_num=const_num, weight=5000)
    es.AddClinicalGoal(RoiName=aorta, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if plexus:
    plexus_maxDose, obj_num = maxDose(po, roi=plexus, dose=7400, o_num=obj_num, c_num=const_num, weight=1500)
    es.AddClinicalGoal(RoiName=plexus, GoalCriteria="AtMost", GoalType="DoseAtAbsoluteVolume", ParameterValue=1, PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if lungs:
    lungs_20gy, obj_num = maxDVH(po, roi=lungs, dose=2000, volume=35, o_num=obj_num, c_num=const_num, weight=1500)
    lungs_5gy, obj_num = maxDVH(po, roi=lungs, dose=500, volume=60, o_num=obj_num, c_num=const_num, weight=1500)
    lungs_maxEUD, obj_num = maxEUD(po, roi=lungs, dose=2000, o_num=obj_num, c_num=const_num, weight=1500)
    lungs_fall_off, obj_num = fall_off(po, roi=lungs, o_num=obj_num, c_num=const_num, high_dose=6600, low_dose=0, distance=1)
    
    es.AddClinicalGoal(RoiName=lungs, GoalCriteria="AtMost", GoalType="AverageDose", PrimaryAcceptanceLevel=2000,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=lungs, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=500, PrimaryAcceptanceLevel=0.55,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
    es.AddClinicalGoal(RoiName=lungs, GoalCriteria="AtMost", GoalType="VolumeAtDose", ParameterValue=2000, PrimaryAcceptanceLevel=0.35,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if boost:
    boost_targetEUD, obj_num = targetEUD(po, roi=boost, dose=9300, o_num=obj_num, c_num=const_num, weight=100,robust=True)
    boost_min, obj_num = minDose(po, roi=boost, dose=9300, o_num=obj_num, c_num=const_num, weight=1000, robust=True)
    boost_max, obj_num = maxDose(po, boost, 10000, obj_num, const_num, weight=500)
    
    es.AddClinicalGoal(RoiName=boost, GoalCriteria="AtMost", GoalType="AverageDose", PrimaryAcceptanceLevel=9500,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if nodeboost:
    nodeboost_targetEUD, obj_num = targetEUD(po, roi=nodeboost, dose=7400, o_num=obj_num, c_num=const_num, weight=1000)
    nodeboost_maxDose, obj_num = maxDose(po, roi=nodeboost, dose=8000, o_num=obj_num, c_num=const_num, weight=1000)
    nodeboost_minDose, obj_num = minDose(po, roi=nodeboost, dose=7200, o_num=obj_num, c_num=const_num, weight=1000)
    
    es.AddClinicalGoal(RoiName=nodeboost, GoalCriteria="AtMost", GoalType="AverageDose", PrimaryAcceptanceLevel=7400,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)

if gtvn:
    es.AddClinicalGoal(RoiName=gtvn, GoalCriteria="AtLeast", GoalType="AverageDose", PrimaryAcceptanceLevel=6600,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
if gtvp:
    es.AddClinicalGoal(RoiName=gtvp, GoalCriteria="AtLeast", GoalType="AverageDose", PrimaryAcceptanceLevel=6600,
                                      IsComparativeGoal=False, BeamSet=beam_set, Priority=2147483647, AssociateToPlan=False)
# Set optimization and robustness parameters and start optimization
# 100 steps, 0.50 cm robustness margin, 3.5% density uncertainty
optimization_parameters(po, iter=100, tolerance=1e-8, spot_weight=40, pos_uncert=0.5, dens_uncert=0.035)
po.RunOptimization()

# ---------------------------- Optimize plan - continuous until good ---------------------------
total_dose = plan.TreatmentCourse.TotalDose
end_opt = 0

# Decreasing mean doses to lungs-igtv and heart:
if lungs:
    lungs_dose_1 = total_dose.GetDoseStatistic(RoiName=lungs, DoseType="Average")
    if (lungs_dose_1 * 0.7 + 10) < 1500:
        edit_objective(lungs_maxEUD, lungs_dose_1 * 0.7 + 10, weight=400)
    else:
        edit_objective(lungs_maxEUD, 1500, 400)

if heart:
    heart_dose_1 = total_dose.GetDoseStatistic(RoiName=heart, DoseType="Average")
    edit_objective(heart_meanDose, heart_dose_1 * 0.7, 10)

# Ensuring boost dose is not above the set levels:
if boost:
    target_boost_eud = 9500
    if nodeboost:
        target_node_eud = 7400

    current_iter = 0
    max_iter = 5

    boost_average = total_dose.GetDoseStatistic(RoiName=boost, DoseType="Average")
    if nodeboost:
        nodeboost_average = total_dose.GetDoseStatistic(RoiName=nodeboost, DoseType="Average")
    else:
        nodeboost_average = 0
    while (boost_average > 9450.0 or nodeboost_average > 7350.0) and (current_iter < max_iter):
        if boost:
            boost_average = total_dose.GetDoseStatistic(RoiName=boost, DoseType="Average")

            if boost_average > 9450:
                if (boost_average - target_boost_eud) < 100:
                    edit_objective(boost_targetEUD, target_boost_eud - 50)
                    target_boost_eud -= 50
                else:
                    edit_objective(boost_targetEUD, target_boost_eud - 100)
                    target_boost_eud -= 100

        if nodeboost:
            nodeboost_average = total_dose.GetDoseStatistic(RoiName=nodeboost, DoseType="Average")
            if nodeboost_average > 7350:
                if (nodeboost_average - target_node_eud) < 100:
                    edit_objective(nodeboost_targetEUD, target_node_eud - 50)
                    target_node_eud -= 50
                else:
                    edit_objective(nodeboost_targetEUD, target_node_eud - 100)
                    target_node_eud -= 100
        current_iter += 1

        po.RunOptimization()

        boost_average = total_dose.GetDoseStatistic(RoiName=boost, DoseType="Average")
        if nodeboost:
            nodeboost_average = total_dose.GetDoseStatistic(RoiName=nodeboost, DoseType="Average")

# Set final optimization and robustness parameters and start optimization
# 200 steps, 0.50 cm robustness margin, 3.5% density uncertainty
optimization_parameters(po, iter=200, tolerance=1e-9)
po.RunOptimization()

# Compute final dose, this locks in the dose/ plan and ends optimization
beam_set.AccurateDoseAlgorithm.MCStatisticalUncertaintyForFinalDose = 0.005
beam_set.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False)

robusteval = beam_set.CreateRadiationSetScenarioGroup(Name="5mm/3.5%", UseIsotropicPositionUncertainty=False,
                                                      PositionUncertaintySuperior=0.5, PositionUncertaintyInferior=0.5,
                                                      PositionUncertaintyPosterior=0.5,
                                                      PositionUncertaintyAnterior=0.5, PositionUncertaintyLeft=0.5,
                                                      PositionUncertaintyRight=0.5,
                                                      PositionUncertaintyFormation="AxesAndDiagonalEndPoints",
                                                      PositionUncertaintyList=None, DensityUncertaintyPercent=3.5,
                                                      NumberOfDensityDiscretizationPoints=3,
                                                      ShallAddScenariosOnPlanningExamination=True,
                                                      NamesOfNonPlanningExaminations=[],
                                                      ComputeScenarioDosesAfterGroupCreation=True,
                                                      IncludeZeroPositionUncertainty=False)

patient.Save()