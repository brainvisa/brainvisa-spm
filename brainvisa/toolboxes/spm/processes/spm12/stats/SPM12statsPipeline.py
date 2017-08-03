# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software"s author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user"s attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software"s suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.

from brainvisa.processes import *
from soma.spm import csv_converter
from brainvisa.data.neuroHierarchy import databases

userLevel = 2
name = "Stats pipeline (SPM12) (WIP...)"

volume_choice_section = "Volume choice"
factoriel_design_section = "Factoriel design"
contrast_manager_section = "Contrast manager"
result_section = "Result report"
show_output_section = "Output Results"

#------------------------------------------------------------------------------
top_type_list = ["T1 MRI tissue probability map"]
images_type = sorted([t.name for t in getAllDiskItemTypes()])
for top_type in top_type_list:
    images_type.insert(0, images_type.pop(images_type.index(top_type)))
#------------------------------------------------------------------------------

signature = Signature(
    "factorial_design_type",
        Choice("One sample T-Test",
               "Two sample T-Test",
               "Paired T-Test"),
    "analysis_name", String(),
    #volume_choice_section
    "files_type",
        OpenChoice(
            *images_type,
            section=volume_choice_section),
    "group",
        ReadDiskItem(
            "Subject Group",
            "JSON file",
            section=volume_choice_section),
    "file_reference",
        ReadDiskItem(
            "4D Volume",
            ["NIFTI-1 image", "SPM image", "MINC image"],
            section=volume_choice_section),
    "group_images",
        ListOf(
            ReadDiskItem(
                "4D Volume",
                "NIFTI-1 image"),
            section=volume_choice_section),
    "group_2",
        ReadDiskItem(
            "Subject Group",
            "JSON file",
            section=volume_choice_section),
    "group_2_images",
        ListOf(
            ReadDiskItem(
                "4D Volume",
                "NIFTI-1 image"),
            section=volume_choice_section),
    #factoriel_design_section
    "covariate_table",
        ReadDiskItem(
            "Covariate table for SPM",
            "CSV file",
            section=factoriel_design_section),
    "nuisance_covariate_list", ListOf(Choice(), section=factoriel_design_section),
    "interest_covariate_list", ListOf(Choice(), section=factoriel_design_section),
    "threshold_masking",
        Choice(
            "Neither",
            "Absolute",
            "Relative",
            section=factoriel_design_section),
    "threshold_value", Float(section=factoriel_design_section),
    "implicit_mask", Boolean(section=factoriel_design_section),
    "explicit_mask",
        ReadDiskItem(
            "explicit mask for SPM analysis",
            ["NIFTI-1 image", "SPM image", "MINC image"],
            section=factoriel_design_section),
    #contrast_manager_section
    "contrast", Boolean(section=contrast_manager_section),
    "contrast_name", String(section=contrast_manager_section),
    "contrast_type", Choice(("Neither", 0),
                            ("positive", 1),
                            ("negative", -1),
                            section=contrast_manager_section),
    "contrast_vector", ListOf(Float(), section=contrast_manager_section),
    #result_section
    'print_result', Choice("none",
                           "PostScript (PS)",
                           "Encapsulated PostScript (EPS)",
                           "Portable Document Format (PDF)",
                           "JPEG image",
                           "PNG image",
                           "TIFF image",
                           "MATLAB figure",
                           #"CSV file",
                           #"NIDM (Neuroimaging Data Model)",
                           section=result_section),
    "add_section_overlay", Boolean(section=result_section),
    "section_image",
        ReadDiskItem(
            "anatomical Template",
            ["NIFTI-1 image", "SPM image", "MINC image"],
            section=result_section),
    "add_render_overlay", Boolean(section=result_section),
    "render_image", ReadDiskItem("SPM Render", "Matlab file", section=result_section),
    "render_style", Choice(("New", "1"), ("Old", "NaN"), section=result_section),
    "brightness",
        Choice(
            ("Neither", 1),
            ("slightly", 0.75),
            ("more", 0.5),
            ("lots", 0.25),
            section=result_section),
    "p_value_type", Choice("FDR", "FWE", "Neither", section=result_section),
    "p_value", Float(section=result_section),
    "min_cluster_size", Integer(section=result_section),
    #show_output_section
    "spm_workspace_directory", #to hide
        WriteDiskItem(
            "SPM workspace directory",
            "Directory",
            section=show_output_section),
    "spm_mat",
        WriteDiskItem(
          "SPM design specification",
          "Matlab file",
          section=show_output_section),
    "spm_report",
        WriteDiskItem(
            "SPM graphical report",
            "PS file",
            section=show_output_section),
    "filtered_image",
        WriteDiskItem(
            "SPM filtered image",
            ["NIFTI-1 image", "SPM image", "MINC image"],
            section=show_output_section),
)
#------------------------------------------------------------------------------

def initialization(self):
    self.setDisable("filtered_image")  # TODO : make link in python module
    #Modify signature
    self.setOptional("group", "file_reference", "group_2")
    self.setOptional("covariate_table","nuisance_covariate_list")
    self.setOptional("interest_covariate_list", "explicit_mask")
    self.setOptional("spm_report", "filtered_image")
    #self.setHidden("spm_workspace_directory")
    #Update Signature
    self.addLink(None, "factorial_design_type", self.updateSignatureAboutFactorialDesignSelection)
    self.addLink(None, "files_type", self.updateFileReference)
    self.addLink(None, "group", self.updateFileReference)
    self.addLink(None, "covariate_table", self.updateSignatureAboutCovariate)
    self.addLink(None, 'threshold_masking', self.updateSignatureAboutThresholdMasking )
    self.addLink(None, "add_section_overlay", self.updateSignatureAboutSection)
    self.addLink(None, "add_render_overlay", self.updateSignatureAboutRender)
    self.addLink(None, "render_style", self.updateSignatureAboutRender)
    #make diskitem links
    self.linkParameters("group_images",
                        ("group", "file_reference", "files_type"),
                        self.updateGroupImages)
    self.linkParameters("group_2_images",
                        ("group_2", "file_reference", "files_type"),
                        self.updateGroup2Images)
    self.linkParameters("spm_mat",
                        ("group", "group_2", "factorial_design_type", "analysis_name"),
                        self.updateSPMMat)
    self.linkParameters("spm_workspace_directory", "spm_mat")
    #Create execution tree
    analysis_serial_node = SerialExecutionNode(name, parameterized=self)
    self.addProcessesToExecutionNode(analysis_serial_node)
    # Attach the execution tree to the process
    self.setExecutionNode(analysis_serial_node)

    #update node selection
    self.addLink(None, "factorial_design_type", self.updateFactorialDesignSelection)

    #Initialize signature fields
    self.threshold_masking = "Neither"
    self.contrast_name = "contrast"
    self.print_result = "PostScript (PS)"
    self.p_value_type = "Neither"
    self.p_value = 0.001
    self.min_cluster_size = 0
    self.add_section_overlay = False
    self.add_render_overlay = False

def updateSignatureAboutFactorialDesignSelection(self, proc):
    if self.factorial_design_type == "One sample T-Test":
        self.setEnable("group", "file_reference", mandatory=False)
        self.setEnable("group_images", mandatory=True)
        self.setDisable("group_2", "group_2_images")
    elif self.factorial_design_type in ["Two sample T-Test", "Paired T-Test"]:
        self.setEnable("group", "file_reference", "group_2", mandatory=False)
        self.setEnable("group_images", "group_2_images", mandatory=True)
    else:
        raise RuntimeError("Unvalid factorial_design_type")
    self.changeSignature(self.signature)
#==============================================================================
# Extract File from group
#==============================================================================
def updateFileReference(self, proc):
    if self.group is not None:
        f = open(self.group.fullPath(), "r")
        group_dict_list = json.load(f)
        f.close()
        required_attr = group_dict_list["group_list"][0]
    else:
        required_attr = {}
    self.signature["file_reference"] = ReadDiskItem(
        self.files_type,
        ["NIFTI-1 image", "SPM image", "MINC image"],
        requiredAttributes=required_attr,
        section=volume_choice_section)
    self.setOptional("file_reference")
    self.changeSignature(self.signature)

def updateGroupImages(self, proc, dummy):
    if not None in [self.file_reference, self.group]:
        reference_attr = self.file_reference.hierarchyAttributes()
        f = open(self.group.fullPath(), "r")
        group_dict_list = json.load(f)
        f.close()
        first_attr_dict = group_dict_list["group_list"][0]
        for attr in first_attr_dict:
            if attr in reference_attr.keys():
                del reference_attr[attr]
            else:
                context.warning("%s attribute not found" % attr)

        return findDiskitemListFromGroup(self.group, self.files_type, reference_attr)

def updateGroup2Images(self, proc, dummy):
    if not None in [self.file_reference, self.group_2]:
        reference_attr = self.file_reference.hierarchyAttributes()
        f = open(self.group_2.fullPath(), "r")
        group_dict_list = json.load(f)
        f.close()
        first_attr_dict = group_dict_list["group_list"][0]
        for attr in first_attr_dict:
            if attr in reference_attr.keys():
                del reference_attr[attr]
            else:
                context.warning("%s attribute not found" % attr)

        return findDiskitemListFromGroup(self.group_2, self.files_type, reference_attr)

def findDiskitemListFromGroup(group_diskitem, type_to_find, common_attribute_dict ):
    db = databases.database( group_diskitem.hierarchyAttributes()[ "_database" ] )
    diskitem_list = []
    d = common_attribute_dict.copy()
    f = open(group_diskitem.fullPath(), "r")
    group_dict_list = json.load(f)
    f.close()
    for attr_dict in group_dict_list["group_list"]:
        tmp_dict = attr_dict.copy()
        tmp_dict.update( d )
        tmp_diskitem_list = list( db.findDiskItems( tmp_dict, _type=type_to_find ) )
        if tmp_diskitem_list and len(tmp_diskitem_list) == 1:
          diskitem_list.append( tmp_diskitem_list[0] )
        else:
            diskitem_list.append('')
            print("None or several diskitems found for type '%s' with these attributes:"%type_to_find)
            print(json.dumps( tmp_dict, indent=1))
    return diskitem_list
#==============================================================================
#
#==============================================================================
def updateSPMMat(self, proc, dummy):
    def makeDiskItem(attr):
        attr["analysis"] = self.analysis_name
        attr["factorial_design"] = self.factorial_design_type.replace(" ", "").replace("-", "")
        return self.signature["spm_mat"].findValue(attr)

    if self.group is not None and self.analysis_name:
        attr = {"_database":self.group.hierarchyAttributes()["_database"]}
        if self.factorial_design_type == "One sample T-Test":
            attr.update({"group_name":self.group.hierarchyAttributes()["group_name"]})
        elif self.factorial_design_type in ["Two sample T-Test", "Paired T-Test"]:
            if self.group_2 is not None:
                attr.update({"first_group_name":self.group.hierarchyAttributes()["group_name"]})
                attr.update({"second_group_name":self.group_2.hierarchyAttributes()["group_name"]})
            else:
                pass
        else:
            raise ValueError("Invalid factorial_design_type")
        return makeDiskItem(attr)

def updateSignatureAboutCovariate(self, proc):
    covariate_dict, row_keys_list = csv_converter.reverse(self.covariate_table.fullPath())
    nuisance_covariate_list = []
    for subject_covariate_dict in covariate_dict.values():
        nuisance_covariate_list = list(set( nuisance_covariate_list + subject_covariate_dict.keys()))
    nuisance_covariate_list.sort()
    self.signature["nuisance_covariate_list"] = ListOf(Choice(*nuisance_covariate_list), section=factoriel_design_section)
    interest_covariate_list_user_level = self.signature["interest_covariate_list"].userLevel
    self.signature["interest_covariate_list"] = ListOf(Choice(*nuisance_covariate_list), section=factoriel_design_section)
    self.signature["interest_covariate_list"].userLevel = interest_covariate_list_user_level
    self.setOptional("nuisance_covariate_list", "interest_covariate_list")
    self.changeSignature(self.signature)

def updateSignatureAboutThresholdMasking( self, proc ):
    if self.threshold_masking == "Neither":
        self.setDisable('threshold_value')
    else:
        self.setEnable('threshold_value')
    self.changeSignature( self.signature )

def updateSignatureAboutSection(self, proc):
    if self.add_section_overlay:
        self.setEnable("section_image")
    else:
        self.setDisable("section_image")
    self.changeSignature(self.signature)

def updateSignatureAboutRender(self, proc):
    if self.add_render_overlay:
        self.setEnable("render_image", "render_style")
        if self.render_style == "1":
            self.setEnable("brightness")
        elif self.render_style == "NaN":
            self.setDisable("brightness")
        else:
            raise ValueError("Unvalid render_style")
    else:
        self.setDisable("render_image", "render_style", "brightness")
    self.changeSignature(self.signature)
#==============================================================================
#
#==============================================================================
def addProcessesToExecutionNode(self, analysis_serial_node):

    factorial_design_selection_node = SelectionExecutionNode(
        """Factorial design""",
        optional=True,
        selected=True,
        parameterized=self)
    self.addOneSampleTTestProcess(factorial_design_selection_node)
    self.addTwoSampleTTestProcess(factorial_design_selection_node)
    self.addPairedTTestProcess(factorial_design_selection_node)

    analysis_serial_node.addChild("factorial_design_node", factorial_design_selection_node)

    addDesignMatrixProcess(analysis_serial_node)
    addDesignExploreFilesAndFactorsProcess(analysis_serial_node)
    addModelEstimationProcess(analysis_serial_node)
    addContrastProcess(analysis_serial_node)
    addResultsReportProcess(analysis_serial_node)
    addIdentifyAndLabelProcess(analysis_serial_node)

def addOneSampleTTestProcess(self, node):
    node.addChild(
        "one_sample_T_test",
        ProcessExecutionNode(
            "SPM12oneSampleTTest_generic",
            selected=True))
    node.addDoubleLink("one_sample_T_test.images", "group_images")
    node.addDoubleLink("one_sample_T_test.threshold_masking", "threshold_masking")
    node.addDoubleLink("one_sample_T_test.threshold_value", "threshold_value")
    node.addDoubleLink("one_sample_T_test.implicit_mask", "implicit_mask")
    node.addDoubleLink("one_sample_T_test.explicit_mask", "explicit_mask")
    node.addDoubleLink("one_sample_T_test.covariate_table", "covariate_table")
    node.addDoubleLink("one_sample_T_test.nuisance_covariate_list", "nuisance_covariate_list")
    node.addDoubleLink("one_sample_T_test.interest_covariate_list", "interest_covariate_list")
    node.addDoubleLink("one_sample_T_test.spm_workspace_directory", "spm_workspace_directory")
    node.addDoubleLink("one_sample_T_test.one_sample_T_test_mat_file", "spm_mat")
    node.one_sample_T_test._selectionChange.add(self.updateOneSampleTTestChoice)

def updateOneSampleTTestChoice(self, node):
    if node.isSelected():
        self.factorial_design_type = "One sample T-Test"

def addTwoSampleTTestProcess(self, node):
    node.addChild(
        "two_sample_T_test",
        ProcessExecutionNode(
            "SPM12twoSampleTTest_generic",
            selected=False))
    node.addDoubleLink("two_sample_T_test.group_1_images", "group_images")
    node.addDoubleLink("two_sample_T_test.group_2_images", "group_2_images")
    node.addDoubleLink("two_sample_T_test.threshold_masking", "threshold_masking")
    node.addDoubleLink("two_sample_T_test.threshold_value", "threshold_value")
    node.addDoubleLink("two_sample_T_test.implicit_mask", "implicit_mask")
    node.addDoubleLink("two_sample_T_test.explicit_mask", "explicit_mask")
    node.addDoubleLink("two_sample_T_test.covariate_table", "covariate_table")
    node.addDoubleLink("two_sample_T_test.covariate_list", "nuisance_covariate_list")
    node.addDoubleLink("two_sample_T_test.spm_workspace_directory", "spm_workspace_directory")
    node.addDoubleLink("two_sample_T_test.two_sample_T_test_mat_file", "spm_mat")
    node.two_sample_T_test._selectionChange.add(self.updateTwoSampleTTestChoice)

def updateTwoSampleTTestChoice(self, node):
    if node.isSelected():
        self.factorial_design_type = "Two sample T-Test"

def addPairedTTestProcess(self, node):
    node.addChild(
        "paired_T_Test",
        ProcessExecutionNode(
            "SPM12pairedTTest_generic",
          selected=False))
    node.addDoubleLink("paired_T_Test.group_1_images", "group_images")
    node.addDoubleLink("paired_T_Test.group_2_images", "group_2_images")
    node.addDoubleLink("paired_T_Test.threshold_masking", "threshold_masking")
    node.addDoubleLink("paired_T_Test.threshold_value", "threshold_value")
    node.addDoubleLink("paired_T_Test.implicit_mask", "implicit_mask")
    node.addDoubleLink("paired_T_Test.explicit_mask", "explicit_mask")
    node.addDoubleLink("paired_T_Test.covariate_table", "covariate_table")
    node.addDoubleLink("paired_T_Test.covariate_list", "nuisance_covariate_list")
    node.addDoubleLink("paired_T_Test.spm_workspace_directory", "spm_workspace_directory")
    node.addDoubleLink("paired_T_Test.paired_T_test_mat_file", "spm_mat")
    node.paired_T_Test._selectionChange.add(self.updatePairedTTestChoice)

def updatePairedTTestChoice(self, node):
    if node.isSelected():
        self.factorial_design_type = "Paired T-Test"

def addDesignMatrixProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "design_mat",
        ProcessExecutionNode(
            "SPM12modelReview_generic",
            optional=True,
            selected=True)
    )
    analysis_serial_node.addDoubleLink("design_mat.basic_model_mat_file", "spm_mat")
    analysis_serial_node.addDoubleLink("design_mat.print_result", "print_result")

def addDesignExploreFilesAndFactorsProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "files_and_factors",
        ProcessExecutionNode(
            "SPM12modelReview_generic",
            optional=True,
            selected=True)
    )
    analysis_serial_node.files_and_factors.display = "Files & Factors"
    analysis_serial_node.addDoubleLink("files_and_factors.basic_model_mat_file", "spm_mat")
    analysis_serial_node.addDoubleLink("files_and_factors.print_result", "print_result")


def addModelEstimationProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "est",
        ProcessExecutionNode(
            "SPM12modelEstimation_generic",
            optional=True,
            selected=True)
    )
    analysis_serial_node.addDoubleLink("spm_mat", "est.basic_model_mat_file")

def addContrastProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "contrast_SPM",
        ProcessExecutionNode(
            "SPM12contrastManager_generic",
            optional=True,
            selected=True)
    )
    analysis_serial_node.addDoubleLink("spm_mat", "contrast_SPM.contrast_mat_file")
    analysis_serial_node.addDoubleLink("contrast_vector", "contrast_SPM.T_contrast_0_weights_vector")
    analysis_serial_node.addDoubleLink("contrast_name", "contrast_SPM.T_contrast_0_name")

def addResultsReportProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "results_report_SPM",
        ProcessExecutionNode(
            "SPM12resultsReport_generic",
            optional=True,
            selected=True))
    analysis_serial_node.results_report_SPM.contrast_number = 1
    analysis_serial_node.addDoubleLink("spm_mat", "results_report_SPM.results_report_mat_file")
    analysis_serial_node.addDoubleLink("print_result", "results_report_SPM.print_result")
    analysis_serial_node.addDoubleLink("add_section_overlay", "results_report_SPM.add_section_overlay")
    analysis_serial_node.addDoubleLink("section_image", "results_report_SPM.section_image")
    analysis_serial_node.addDoubleLink("add_render_overlay", "results_report_SPM.add_render_overlay")
    analysis_serial_node.addDoubleLink("render_image", "results_report_SPM.render_image")
    analysis_serial_node.addDoubleLink("render_style", "results_report_SPM.render_style")
    analysis_serial_node.addDoubleLink("brightness", "results_report_SPM.brightness")
    analysis_serial_node.addDoubleLink("p_value_type", "results_report_SPM.contrast_0_threshold_type")
    analysis_serial_node.addDoubleLink("p_value", "results_report_SPM.contrast_0_threshold")
    analysis_serial_node.addDoubleLink("min_cluster_size", "results_report_SPM.contrast_0_extent")
    analysis_serial_node.addDoubleLink("filtered_image", "results_report_SPM.filtered_image")
    analysis_serial_node.addDoubleLink("spm_report", "results_report_SPM.results_report")

def addIdentifyAndLabelProcess(analysis_serial_node):
    analysis_serial_node.addChild(
        "label_filtered_images",
        ProcessExecutionNode(
            "labelFilteredImages",
            optional=True,
            selected=False))
    analysis_serial_node.addDoubleLink("label_filtered_images.results_report_mat_file",
                                       "results_report_SPM.results_report_mat_file")
    analysis_serial_node.addDoubleLink("label_filtered_images.write_filtered_images",
                                       "results_report_SPM.write_filtered_images")
    analysis_serial_node.addLink("label_filtered_images.write_filtered_images_basename",
                                 "results_report_SPM.write_filtered_images_basename")
#==============================================================================
#
#==============================================================================
def updateFactorialDesignSelection(self, enabled, names, parameterized):
    if self.factorial_design_type == "One sample T-Test":
        parameterized[0].executionNode().factorial_design_node.one_sample_T_test.setSelected( True )
    elif self.factorial_design_type == "Two sample T-Test":
        parameterized[0].executionNode().factorial_design_node.two_sample_T_test.setSelected( True )
    elif self.factorial_design_type == "Paired T-Test":
        parameterized[0].executionNode().factorial_design_node.paired_T_Test.setSelected( True )
    else:
        raise Exception("Unvalid factorial_design_type")