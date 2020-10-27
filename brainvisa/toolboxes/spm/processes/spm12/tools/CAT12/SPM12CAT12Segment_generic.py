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
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
from __future__ import absolute_import
from brainvisa.tools import spm_utils
from brainvisa.processes import *
import os
import shutil
from distutils.dir_util import copy_tree
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.tools.cat12 import EstimateAndWrite


configuration = Application().configuration


def validation():
    try:
        spm = SPM12Standalone(configuration.SPM.spm12_standalone_command,
                              configuration.SPM.spm12_standalone_mcr_path,
                              configuration.SPM.spm12_standalone_path)
    except Exception:
        spm = SPM12(configuration.SPM.spm12_path,
                    configuration.matlab.executable,
                    configuration.matlab.options)
    return spm


userLevel = 1
name = 'CAT12 - Segment - generic'
input_section = 'Inputs'
option_section = 'Initial options'
seg_options_section = 'Segmentations options'
spatial_options_section = 'Spatial registration options'
extended_section = 'Extended options'
surface_options = 'Surface options'
admin_options = 'Administration options'
output_section = 'Outputs'
grey_output = 'Grey matter'
white_output = 'White matter'
csf_output = 'CSF matter'
wmh_output = 'White matter intensity'
other_tissue_output = 'Other tissues (skull+scalp+background)'
pve_labels_output = 'PVE labels'
bias_output = 'Bias corrections'
other_output = "Other outputs"

signature = Signature(
    "t1mri", ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                          section=input_section),
    
    # --- Options ---
    "template", ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                             section=option_section),
    "affine_regularisation", Choice(('ICBM European brains', 'european'),
                                    ('ICBM East Asian brains', 'east_asian'),
                                    ('No regularisation', 'no_regularisation'),
                                    ('No affine registration', 'no_registration'),
                                    section=option_section),
    "inhomogeneity_correction", Choice('ultralight', 'light', 'medium', 'strong', 'heavy',
                                       section=option_section),  # detail more the choice text with values ?
    "processing_accuracy", Choice('average', 'high', 'ultra_high',
                                  section=option_section),
    
    # --- Extended options ---
    # - Segmentation options -
    "affine_preprocessing", Choice('none', 'light', 'full', 'default', 'rough',
                                   section=seg_options_section),
    "noise_correction", Choice('none', 'classic', 'light', 'medium',
                               section=seg_options_section),  # , 'strong'),
    # "initial_segmentation", Choice('SPM unified Segmentation', 'k-means AMAP'),
    "local_adaptative_segmentation", Choice('none', 'ultralight', 'light', 'medium', 'strong', 'heavy',
                                            section=seg_options_section),
    "skull_stripping", Choice(('none', 'none'),
                              ('SPM approach', 'spm'),
                              ('GCUT approach', 'gcut_medium'),
                              ('APRG approach', 'aprg'),
                              ('APRG approach V2', 'aprg_v2'),
                              ('APRG approach V2 wider', 'aprg_v2_wider'),
                              ('APRG approach V2 tighter', 'aprg_v2_tighter'),
                              section=seg_options_section),
    "clean_up", Choice('none', 'light', 'medium', 'strong', 'heavy',
                       section=seg_options_section),
    "wm_hyperintensities_correction", Choice(("no WMH correction", "no"),
                                             ("set WMH temporary as WM", "temporary"),
                                             #  ("set WMH as WM", "save"),
                                             section=seg_options_section),
    # "stroke_lesion_correction", Choice(),
    "optimal_resolution", Choice(('Optimal resolution', 'optimal'),
                                 ('Native resolution', 'native'),
                                 ('Best native resolution', 'best'),
                                 ('Fixed resolution', 'fixed'),
                                 section=seg_options_section),
    "optimal_resolution_value", ListOf(Float(),
                                       section=seg_options_section),
    
    # - Spatial registration -
    "spatial_registration_method", Choice('shooting', 'dartel',
                                          section=spatial_options_section),
    "spatial_registration_template", ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                                                  section=spatial_options_section),
    "shooting_method", Choice(("Default Shooting", 'default'),
                              ("Optimized Shooting - vox", 'opt_vox'),
                              ("Optimized Shooting - fast", 'opt_fast'),
                              ("Optimized Shooting - standard", 'opt_standard'),
                              ("Optimized Shooting - fine", 'opt_fine'),
                              ("Optimized Shooting - strong", 'opt_strong'),
                              ("Optimized Shooting - medium", 'opt_medium'),
                              ("Optimized Shooting - soft", 'opt_soft'),
                              section=spatial_options_section),
    
    "voxel_size", Float(section=extended_section),
    
    # - Surface otions - ?
    "surface_thickness_estimation", Boolean(section=surface_options),
    "voxel_size_thickness_est", Float(section=surface_options),
    "cortical_myelination_corr", Boolean(section=surface_options),
    "cortical_surf_creation", Float(section=surface_options),
    "parahipp_surf_creation", Float(section=surface_options),
    "closing_parahipp", Boolean(section=surface_options),
    
    # - Admin options -
    "create_report", Boolean(section=admin_options),
    "lazy_processing", Boolean(section=admin_options),
    "error_handling", Boolean(section=admin_options),
    "verbose", Choice('none', 'default', 'details',
                      section=admin_options),
    
    # --- Writing options ---
    # ROI process
    # ...
    # "ROI_process", Choice("No ROI processings", "Atlases",
    #                       section=output_section),
    
    "grey_native_space", Boolean(section=grey_output),
    "grey_normalized", Boolean(section=grey_output),
    "grey_modulated_normalized", Choice(("no", 'no'),
                                        ("affine + non-linear", 'affine_non_linear'),
                                        ("non-linear only", 'non_linear'),
                                        section=grey_output),
    "grey_dartel_export", Choice("no", "rigid", "affine", "both",
                                 section=grey_output),
    
    "white_native_space", Boolean(section=white_output),
    "white_normalized", Boolean(section=white_output),
    "white_modulated_normalized", Choice(("no", 'no'),
                                         ("affine + non-linear", 'affine_non_linear'),
                                         ("non-linear only", 'non_linear'),
                                         section=white_output),
    "white_dartel_export", Choice("no", "rigid", "affine", "both",
                                  section=white_output),
    
    "csf_native_space", Boolean(section=csf_output),
    "csf_normalized", Boolean(section=csf_output),
    "csf_modulated_normalized", Choice(("no", 'no'),
                                       ("affine + non-linear", 'affine_non_linear'),
                                       ("non-linear only", 'non_linear'),
                                       section=csf_output),
    "csf_dartel_export", Choice("no", "rigid", "affine", "both",
                                section=csf_output),
    
    # "wmh_native_space", Boolean(section=wmh_output),
    # "wmh_normalized", Boolean(section=wmh_output),
    # "wmh_modulated_normalized", Choice(("no", 'no'),
    #                                    ("affine + non-linear", 'affine_non_linear'),
    #                                    ("non-linear only", 'non_linear'),
    #                                    section=wmh_output),
    # "wmh_dartel_export", Choice("no", "rigid", "affine", "both",
    #                             section=wmh_output),
    
    # "sls_native_space", Boolean(),
    # "sls_normalized", Boolean(),
    # "sls_modulated_normalized", Choice("no", "affine + non-linear", "non-linear only"),
    # "sls_dartel_export", Choice("no", "rigid", "affine", "both"),
    
    "other_tissue_proba_map_native_space", Boolean(section=other_tissue_output),
    "other_tissue_proba_map_normalized", Boolean(section=other_tissue_output),
    "other_tissue_proba_map_modulated_normalized", Choice(("no", 'no'),
                                                          ("affine + non-linear", 'affine_non_linear'),
                                                          ("non-linear only", 'non_linear'),
                                                          section=other_tissue_output),
    "other_tissue_proba_map_dartel_export", Choice("no", "rigid", "affine", "both",
                                                   section=other_tissue_output),
    
    # "roi_evaluation_native_space", Boolean(),
    # "roi_evaluation_dartel_export", Choice("no", "rigid", "affine", "both"),
    
    "pve_labels_native_space", Boolean(section=pve_labels_output),
    "pve_labels_normalized", Boolean(section=pve_labels_output),
    "pve_labels_dartel_export", Choice("no", "rigid", "affine", "both",
                                       section=pve_labels_output),
    
    "bias_native_space", Boolean(section=bias_output),
    "bias_normalized", Boolean(section=bias_output),
    "bias_dartel_export", Choice("no", "rigid", "affine", "both",
                                 section=bias_output),
    
    "local_bias_native_space", Boolean(section=bias_output),
    "local_bias_normalized", Boolean(section=bias_output),
    "local_bias_dartel_export", Choice("no", "rigid", "affine", "both",
                                       section=bias_output),
    
    "jacobian_determinant", Boolean(section=other_output),
    'deformation_field_type', Choice("Neither", 'Inverse', 'Forward', 'Inverse + Forward',
                                     section=other_output),
    "registration_matrix", Boolean(section=other_output),
    
    "output_options", Choice(("Source directory", 'source'),
                             ("Custom output directory", 'custom'),
                             section=other_output),
    "output_directory", WriteDiskItem('Directory', 'Directory',
                                      section=other_output),
    "batch_location", WriteDiskItem('Matlab SPM script', 'Matlab script',
                                    section=other_output)
)


def initialization(self):
    self.setOptional('template', 'voxel_size', 'spatial_registration_template')
    
    self.addLink('batch_location', 't1mri', self.update_batch_path)
    self.addLink(None, 'surface_thickness_estimation', self.update_surface_selection)
    
    self.inhomogeneity_correction = 'medium'
    self.processing_accuracy = 'average'
    
    self.affine_preprocessing = 'default'
    self.noise_correction = 'medium'
    self.local_adaptative_segmentation = 'medium'
    self.skull_stripping = 'aprg'
    self.clean_up = 'medium'
    self.wm_hyperintensities_correction = 'temporary'
    self.addLink(None, 'optimal_resolution', self.update_optimal_resolution_choice)
    self.optimal_resolution = 'optimal'
    self.optimal_resolution_value = [1, 0.1]
    self.addLink(None, 'spatial_registration_method', self.update_registration_method)
    self.spatial_registration_method = 'shooting'
    self.shooting_method = 'opt_standard'
    self.voxel_size = 1.5
    
    self.voxel_size_thickness_est = 0.5
    self.cortical_myelination_corr = False
    self.cortical_surf_creation = 0.7
    self.parahipp_surf_creation = 0.1
    self.closing_parahipp = False
    
    self.create_report = True
    self.lazy_processing = False
    self.error_handling = True
    self.verbose = 'details'
    
    # self.ROI_process = 'No ROI processings'
    
    self.grey_native_space = False
    self.grey_normalized = False
    self.grey_modulated_normalized = 'affine_non_linear'
    self.grey_dartel_export = 'no'
    
    self.white_native_space = False
    self.white_normalized = False
    self.white_modulated_normalized = 'affine_non_linear'
    self.white_dartel_export = 'no'
    
    self.csf_native_space = False
    self.csf_normalized = False
    self.csf_modulated_normalized = 'no'
    self.csf_dartel_export = 'no'

    # self.wmh_native_space = False
    # self.wmh_normalized = False
    # self.wmh_modulated_normalized = 'no'
    # self.wmh_dartel_export = 'no'

    self.other_tissue_proba_map_native_space = False
    self.other_tissue_proba_map_normalized = False
    self.other_tissue_proba_map_modulated_normalized = 'no'
    self.other_tissue_proba_map_dartel_export = 'no'
    
    self.pve_labels_native_space = True
    self.pve_labels_normalized = False
    self.pve_labels_dartel_export = 'no'

    self.bias_native_space = False
    self.bias_normalized = True
    self.bias_dartel_export = 'no'

    self.local_bias_native_space = False
    self.local_bias_normalized = False
    self.local_bias_dartel_export = 'no'
    
    self.jacobian_determinant = False
    self.deformation_field_type = 'Neither'
    self.registration_matrix = False
    
    self.addLink(None, 'output_options', self.update_output_dir)


def update_batch_path(self, proc):
    if self.t1mri is not None:
        directory_path = os.path.dirname(self.t1mri.fullPath())
        return os.path.join(directory_path, 'cat12_segment_job.m')


def update_surface_selection(self, proc):
    if self.surface_thickness_estimation:
        self.setEnable("voxel_size_thickness_est", "cortical_myelination_corr",
                       "cortical_surf_creation", "parahipp_surf_creation",
                       "closing_parahipp",)
    else:
        self.setDisable("voxel_size_thickness_est", "cortical_myelination_corr",
                        "cortical_surf_creation", "parahipp_surf_creation",
                        "closing_parahipp",)
    self.changeSignature(self.signature)
        

def update_registration_method(self, proc):
    if self.spatial_registration_method == 'shooting':
        self.setEnable('shooting_method')
    elif self.spatial_registration_method == 'dartel':
        self.setDisable('shooting_method')
    self.changeSignature(self.signature)
        

def update_optimal_resolution_choice(self, proc):
    if self.optimal_resolution == 'native':
        self.setDisable('optimal_resolution_value')
    else:
        self.setEnable('optimal_resolution_value')
    self.changeSignature(self.signature)
        

def update_output_dir(self, proc):
    if self.output_options == 'source':
        self.setDisable('output_directory')
    else:
        self.setEnable('output_directory')
    self.changeSignature(self.signature)


def execution(self, context):
    estimate_and_write = EstimateAndWrite()
    
    estimate_and_write.volume_path_list = [self.t1mri.fullPath()]
    
    # Estimation options
    estimate_and_write.estimate_options.set_tissue_proba_map_path(self.template.fullPath())
    if self.affine_regularisation == 'european':
        estimate_and_write.estimate_options.set_affine_regularisation_EuropeanBrains()
    elif self.affine_regularisation == 'east_asian':
        estimate_and_write.estimate_options.set_affine_regularisation_AsianBrains()
    elif self.affine_regularisation == 'no_regularisation':
        estimate_and_write.estimate_options.unset_regularisation()
    elif self.affine_regularisation == 'no_registration':
        estimate_and_write.estimate_options.unset_affine_regularisation()
        
    getattr(estimate_and_write.estimate_options,
            'set_inhomogeneity_correction_%s' % self.inhomogeneity_correction)()
    getattr(estimate_and_write.estimate_options,
            'set_processing_%s' % self.processing_accuracy)()
    
    # Extended options
    getattr(estimate_and_write.extended_options,
            'set_APP_%s' % self.affine_preprocessing)()
    getattr(estimate_and_write.extended_options,
            'set_noise_corr_%s' % self.noise_correction)()
    getattr(estimate_and_write.extended_options,
            'set_LAS_str_%s' % self.local_adaptative_segmentation)()
    getattr(estimate_and_write.extended_options,
            'set_skull_stripping_%s' % self.skull_stripping)()
    getattr(estimate_and_write.extended_options,
            'set_clean_up_%s' % self.clean_up)()
    # getattr(estimate_and_write.extended_options,
    #         'set_wmh_correction_%s' % self.wm_hyperintensities_correction)()
    if self.optimal_resolution == 'native':
        estimate_and_write.extended_options.set_resampling_preproc_native()
    else:
        getattr(estimate_and_write.extended_options,
                'set_resampling_preproc_%s' % self.optimal_resolution)(self.optimal_resolution_value)
    # Spatial registration
    getattr(estimate_and_write.extended_options.spatial_registration,
            'set_registration_%s' % self.spatial_registration_method)()
    
    if self.spatial_registration_template:
        estimate_and_write.extended_options.spatial_registration.set_template(
            self.spatial_registration_template.fullPath()
        )
    else:
        estimate_and_write.extended_options.spatial_registration.set_template('')
        
    if self.spatial_registration_method == 'shooting':
        getattr(estimate_and_write.extended_options.spatial_registration,
                'set_shooting_method_%s' % self.shooting_method)()
    
    estimate_and_write.extended_options.set_voxel_size(self.voxel_size)
    
    # Surface options
    surf_options = estimate_and_write.extended_options.surface_options
    surf_options.set_voxel_size(self.voxel_size_thickness_est)
    surf_options.set_corr_myelination_choice(self.cortical_myelination_corr)
    surf_options.set_cortical_surf(self.cortical_surf_creation)
    surf_options.set_parahipp_surf(self.parahipp_surf_creation)
    surf_options.set_closing_parahipp_choice(self.closing_parahipp)
    
    if self.create_report:
        estimate_and_write.extended_options.set_report_volume()
    else:
        estimate_and_write.extended_options.unset_report()
    estimate_and_write.extended_options.set_lazy_choice(self.lazy_processing)
    estimate_and_write.extended_options.set_error_handling_choice(self.error_handling)
    getattr(estimate_and_write.extended_options, 'set_verbose_%s' % self.verbose)()
    
    # Writing options
    estimate_and_write.writing_options.surface_thickness = str(int(self.surface_thickness_estimation))
    # no ROI process by default
    estimate_and_write.writing_options.output_atlases.set_process_ROI_choice(False)
    
    for tissue in ['grey', 'white', 'csf']:  # , 'wmh']:
        getattr(estimate_and_write.writing_options,
                '%s' % tissue).set_native_choice(str(int(getattr(self, '%s_native_space' % tissue))))
        getattr(estimate_and_write.writing_options,
                '%s' % tissue).set_warped_choice(str(int(getattr(self, '%s_normalized' % tissue))))
        
        mod = getattr(estimate_and_write.writing_options,
                      '%s' % tissue)
        getattr(mod, 'set_modulated_%s' % getattr(self, '%s_modulated_normalized' % tissue))()
        
        dartel = getattr(estimate_and_write.writing_options,
                         '%s' % tissue)
        getattr(dartel, 'set_dartel_%s' % getattr(self, '%s_dartel_export' % tissue))()
    
    other_labels = getattr(estimate_and_write.writing_options,
                           'tpmc')
    other_labels.set_native_choice(str(int(self.other_tissue_proba_map_native_space)))
    other_labels.set_warped_choice(str(int(self.other_tissue_proba_map_normalized)))
    getattr(other_labels, 'set_modulated_%s' % self.other_tissue_proba_map_modulated_normalized)()
    getattr(other_labels, 'set_dartel_%s' % self.other_tissue_proba_map_dartel_export)()
    
    pve_labels = getattr(estimate_and_write.writing_options, 'label')
    pve_labels.set_native_choice(str(int(self.pve_labels_native_space)))
    pve_labels.set_warped_choice(str(int(self.pve_labels_normalized)))
    getattr(pve_labels, 'set_dartel_%s' % self.pve_labels_dartel_export)()
    
    bias = estimate_and_write.writing_options.bias
    bias.set_native_choice(str(int(self.bias_native_space)))
    bias.set_warped_choice(str(int(self.bias_normalized)))
    getattr(bias, 'set_dartel_%s' % self.bias_dartel_export)()
    
    local_bias = estimate_and_write.writing_options.las
    local_bias.set_native_choice(str(int(self.local_bias_native_space)))
    local_bias.set_warped_choice(str(int(self.local_bias_normalized)))
    getattr(local_bias, 'set_dartel_%s' % self.local_bias_dartel_export)()
    
    estimate_and_write.writing_options.set_jacobian(self.jacobian_determinant)
    estimate_and_write.writing_options.set_deformation_field_forward_choice('Forward' in self.deformation_field_type)
    estimate_and_write.writing_options.set_deformation_field_inverse_choice('Inverse' in self.deformation_field_type)
    estimate_and_write.writing_options.set_registration_matrix_choice(self.registration_matrix)
    
    context.write('<br>'.join(estimate_and_write.getStringListForBatch()))
    spm = validation()
    spm.addModuleToExecutionQueue(estimate_and_write)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
    
    if self.output_options != 'source':
        # Move outputs
        native_folder = os.path.dirname(self.t1mri.fullPath())
        output_folder = self.output_directory.fullPath()
        for folder in ['mri', 'report', 'label', 'surf']:
            src = os.path.join(native_folder, folder)
            dest = os.path.join(output_folder, folder)
            if os.path.exists(src):
                if not os.path.exists(dest):
                    os.makedirs(dest)
                copy_tree(src, dest)
                shutil.rmtree(src)
