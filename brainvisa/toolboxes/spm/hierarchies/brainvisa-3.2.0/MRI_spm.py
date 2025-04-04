include( 'base' )
#===============================================================================
# Not subject specific
#===============================================================================
#'templates/t1mri/'
templates = (
    't1mri', SetContent(
        '{template}_{step}_TPM_HDW_DARTEL', SetType('TPM HDW DARTEL template'),
        '{template}_TPM', SetType('TPM template'),
        'Template_{step}_{template}_GS', SetType('Geodesic shooting template')
    ),
)
insertFirst('', 'templates', SetContent(*templates))

#'analyzes/DARTEL/{processing}/DARTEL_{template}/'
DARTEL_directory = (
    '<template>_{step}_HDW_DARTEL', SetType('TPM HDW DARTEL created template'),
)
insert('analyzes/DARTEL/{processing}',
            'DARTEL_{template}',
            SetType('DARTEL analysis directory'),
            SetContent(*DARTEL_directory))

subject_groups = (
    '{modality}_group', SetContent(
        '{group_name}_group', SetType('Subject Group')
    ),
)
insertFirst('', 'subject_groups', SetContent(*subject_groups))

covariates = (
    'spm_covariate', SetContent(
        '{covariate_table}_table', SetType('Covariate table for SPM')
    )
)
insertFirst('', 'covariates', SetContent(*covariates))

#===============================================================================
# subject specific
#===============================================================================

#{center}/{subject}/{processing}/{acquisition}/{analysis}_LDW_to_{template}
LDW_directory = (
#using TPM
  #-T1 MRI probability map native space->
  '<subject>_grey_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'grey',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_white_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'white',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_csf_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'csf',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_skull_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'skull',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_scalp_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'scalp',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_background_proba_native',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'none',
                    'transformation', 'none',
                    'modulation', 'none',
                    'warping_method', 'none'),
  #<--
  '<subject>_PVE',
        SetType('T1 MRI partial volume estimation'),
        SetWeakAttr('transformation', 'none',
                    'warping_method', 'none'),
  '<subject>_estimate_raw_volumes',
        SetType('Estimate T1 MRI raw volumes'),
  '<subject>_bias_corrected',
        SetType('T1 MRI Bias corrected'),
        SetWeakAttr('transformation', 'none',
                    'warping_method', 'none',
                    'space', 't1mri'),
  '<subject>_bias_field', SetType('T1 MRI Bias field'),
  #-T1 MRI probability map DARTEL imported with rigid transform->
  '<subject>_grey_proba_rigid_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'grey',
		    'transformation', 'rigid',
                    'modulation', 'none',
                    'warping_method', 'none'),
  '<subject>_white_proba_rigid_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'white',
              'transformation', 'rigid',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_csf_proba_rigid_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'csf',
              'transformation', 'rigid',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_skull_proba_rigid_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'skull',
              'transformation', 'rigid',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_scalp_proba_rigid_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'scalp',
              'transformation', 'rigid',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_background_proba_rigid_registered',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'none',
                    'transformation', 'rigid',
                    'modulation', 'none',
                    'warping_method', 'none'),
  #<--
  '<subject>_PVE_rigid_registered',
        SetType('T1 MRI Partial Volume Estimation'),
        SetWeakAttr('transformation', 'rigid',
                    'warping_method', 'none'),
  #-T1 MRI probability map DARTEL imported with affine transform (VBM toolbox)->
  '<subject>_grey_proba_affine_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'grey',
              'transformation', 'affine',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_white_proba_affine_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'white',
              'transformation', 'affine',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_csf_proba_affine_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'csf',
              'transformation', 'affine',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_skull_proba_affine_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'skull',
              'transformation', 'affine',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_scalp_proba_affine_registered',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'scalp',
              'transformation', 'affine',
              'modulation', 'none',
              'warping_method', 'none'),
  '<subject>_background_proba_affine_registered',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'none',
                    'transformation', 'affine',
                    'modulation', 'none',
                    'warping_method', 'none'),
  #<--
  '<subject>_PVE_affine_registered',
        SetType('T1 MRI Partial Volume Estimation'),
        SetWeakAttr('transformation', 'affine',
                    'warping_method', 'none'),
  '<subject>_bias_corrected_using_affine_registered',
        SetType('T1 MRI Bias corrected'),
        SetWeakAttr('transformation', 'affine',
                    'warping_method', 'none',
                    'space', 'mni'),
)

HDW_directory = (
  '<subject>_jacobian_warped',
        SetType('Jacobian determinant'),
)
#{center}/{subject}/{processing}/{acquisition}/{analysis}_LDW_to_{template} ==> warping_method : low-dimensional
#{center}/{subject}/{processing}/{acquisition}/{analysis}_HDW_to_{template} ==> warping_method : high-dimensional
def createHierarchyTreeDependingOnNormalization(warping_method):
  return (
  #Warped on template, LDW(ex: TPM)/or/HDW(ex : DARTEL) depending on warping_method (low-dimensional/or/high-dimensional)
    #-T1 MRI probability map warped on LDW/or/HDW template with non-linear only modulation->
  '<subject>_grey_proba_warped_with_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'grey',
              'modulation', 'non-linear only',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_white_proba_warped_with_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'white',
              'modulation', 'non-linear only',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_csf_proba_warped_with_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'csf',
              'modulation', 'non-linear only',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_skull_proba_warped_with_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'skull',
              'modulation', 'non-linear only',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_scalp_proba_warped_with_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'scalp',
              'modulation', 'non-linear only',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_background_proba_warped_with_non_linear_modulation',
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', 'none',
                    'modulation', 'non-linear only',
                    'warping_method', warping_method,
                    'transformation', 'none'),
  #<--
  #-T1 MRI probability map warped on TPM/or/DARTEL template with affine and non-linear modulation->
  '<subject>_grey_proba_warped_with_affine_and_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'grey',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_white_proba_warped_with_affine_and_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'white',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_csf_proba_warped_with_affine_and_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'csf',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_skull_proba_warped_with_affine_and_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'skull',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_scalp_proba_warped_with_affine_and_non_linear_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'scalp',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_background_proba_warped_with_affine_and_non_linear_modulation',
  SetType('T1 MRI tissue probability map'),
  SetWeakAttr('tissue_class', 'none',
              'modulation', 'affine and non-linear',
              'warping_method', warping_method,
              'transformation', 'none'),
  #<--
  #-T1 MRI probability map warped on TPM/or/DARTEL without modulation->
  '<subject>_grey_proba_warped_without_modulation', #TODO : check if without_modulation is useless
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'grey',
                    'warping_method', warping_method,
                    'modulation', 'none',
                    'transformation', 'none'),
  '<subject>_white_proba_warped_without_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'white',
                    'warping_method', warping_method,
                    'modulation', 'none',
                    'transformation', 'none'),
  '<subject>_csf_proba_warped_without_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'csf',
                    'warping_method', warping_method,
                    'modulation', 'none',
                    'transformation', 'none'),
  '<subject>_skull_proba_warped_without_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'skull',
                    'warping_method', warping_method,
                    'modulation', 'none',
                    'transformation', 'none'),
  '<subject>_scalp_proba_warped_without_modulation',
	SetType('T1 MRI tissue probability map'),
	SetWeakAttr('tissue_class', 'scalp',
                    'warping_method', warping_method,
                    'modulation', 'none',
                    'transformation', 'none'),
  '<subject>_background_proba_warped_without_modulation',
  SetType('T1 MRI tissue probability map'),
  SetWeakAttr('tissue_class', 'none',
              'warping_method', warping_method,
              'modulation', 'none',
              'transformation', 'none'),
  #<--
  '<subject>_PVE_warped_without_modulation',
  SetType('T1 MRI Partial Volume Estimation'),
  SetWeakAttr('warping_method', warping_method,
              'transformation', 'none'),
  '<subject>_bias_corrected_using_warped_without_modulation',
  SetType('T1 MRI Bias corrected'),
  SetWeakAttr('transformation', 'none',
              'warping_method', warping_method,
              'space', 'mni'),
  'y_<subject>_forward_deformation_field',
  SetType('SPM deformation field'),
  SetWeakAttr('direction', 'forward',
              'warping_method', warping_method,
              'orientation', 'acquisition_to_mni'),
  'iy_<subject>_inverse_deformation_field',
  SetType('SPM deformation field'),
  SetWeakAttr('direction', 'inverse',
              'warping_method', warping_method,
              'orientation', 'acquisition_to_mni'),
  )

HDW_DARTEL = (
    '<subject>_HDW_DARTEL_flow_field', SetType('HDW DARTEL flow field'),
)

def cat_tissue_outputs(tissue_prefix, tissue_class):
    return (
        'p%s<subject>' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'none',
                    'modulation', 'none',
                    'transformation', 'none'),
        'wp%s<subject>' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'high-dimensional',
                    'modulation', 'none',
                    'transformation', 'none'),
        'mwp%s<subject>' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'high-dimensional',
                    'modulation', 'affine and non-linear',
                    'transformation', 'none'),
        'm0wp%s<subject>' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'high-dimensional',
                    'modulation', 'non-linear only',
                    'transformation', 'none'),

        'rp%s<subject>_rigid' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'none',
                    'modulation', 'none',
                    'transformation', 'rigid'),
        'rp%s<subject>_affine' % tissue_prefix,
        SetType('T1 MRI tissue probability map'),
        SetWeakAttr('tissue_class', tissue_class,
                    'warping_method', 'none',
                    'modulation', 'none',
                    'transformation', 'affine'),
    )

CAT12_directory = (
    cat_tissue_outputs('1', 'grey') +
    cat_tissue_outputs('2', 'white') +
    cat_tissue_outputs('3', 'csf') +
    cat_tissue_outputs('4', 'skull') +
    cat_tissue_outputs('5', 'scalp') +
    cat_tissue_outputs('6', 'none') +
    cat_tissue_outputs('7', 'wmh') +

    ('y_<subject>',
        SetType('SPM deformation field'),
        SetWeakAttr('direction', 'forward',
                    'warping_method', 'none',
                    'orientation', 'acquisition_to_mni'),
    'iy_<subject>',
        SetType('SPM deformation field'),
        SetWeakAttr('direction', 'inverse',
                    'warping_method', 'none',
                    'orientation', 'acquisition_to_mni'),
    't_<subject>_{transformation}_reorient',
        SetType('SPM transformation'),
        SetWeakAttr('direction', 'forward'),
    'it_<subject>_{transformation}_reorient',
        SetType('SPM transformation'),
        SetWeakAttr('direction', 'inverse'),

    'wj_<subject>',
        SetType('Jacobian determinant'),
        SetWeakAttr('space', 't1mri'),

    'm<subject>',
        SetType('T1 MRI Bias corrected'),
        SetWeakAttr('transformation', 'none',
                    'warping_method', 'none',
                    'space', 't1mri'),
        SetPriorityOffset(-1),
    'wm<subject>',
        SetType('T1 MRI Bias corrected'),
        SetWeakAttr('transformation', 'none',
                    'warping_method', 'high-dimensional',
                    'space', 't1mri'),
        SetPriorityOffset(-1),
        # SetWeakAttr('processing', 'cat12Segment'),
    )
)
cat12_analysis_directory = (
    '{analysis}', SetContent(
        'mri', SetContent(*CAT12_directory)
    )
    # SetDefaultAttributeValue('analysis', 'default'),
)

shoot_analysis_directory = (
    '{analysis}_using_{template}GS', SetContent(
        'v_{prefix}<subject>_Template',
        SetType('Velocity field'),

        'y_{prefix}<subject>_Template',
        SetType('SPM deformation field'),
        SetWeakAttr('direction', 'forward',
                    'warping_method', 'high-dimensional'),

        'j_{prefix}<subject>_Template',
        SetType('Jacobian determinant'),
    )
)

#{center}/{subject}/{processing}/{acquisition}
analysis_directory = (
    '{analysis}_LDW_from_t1mri_to_{template}', SetContent(
        *(LDW_directory + createHierarchyTreeDependingOnNormalization(warping_method='low-dimensional'))),
    '{analysis}_HDW_from_t1mri_to_{template}', SetContent(
        *(HDW_directory + createHierarchyTreeDependingOnNormalization(warping_method='high-dimensional'))),
    '{analysis}_HDW_DARTEL_from_t1mri_to_{template}', SetContent(*HDW_DARTEL),
    # '{analysis}_from_t1mri_to_TPM',
    #   SetContent(*CAT12_directory),
    #   SetDefaultAttributeValue('analysis', 'default'),
    #   SetWeakAttr('template', 'TPM',
    #               'spm_hierarchy', 'yes'),
)

long_spm_registration = (
    '{analysis}',
        SetDefaultAttributeValue('analysis', 'default_analysis'),
        SetContent(
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_bias_corrected',
                SetType('T1 MRI Bias corrected'),
                SetWeakAttr('space', 'average',
                            'transformation', 'none',
                            'warping_method', 'none'),
            'iy_<subject>_{acquisition}_to_avg_<acquisition_sequence>_inverse_deformation_field',
                SetType('SPM deformation field'),
                SetWeakAttr('orientation', 'acquisition_to_average',
                            'direction', 'inverse'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_white_proba',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'white',
                            'space', 'average',
                            'transformation', 'none',
                            'modulation', 'none',
                            'warping_method', 'none'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_grey_proba',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'grey',
                            'space', 'average',
                            'transformation', 'none',
                            'modulation', 'none',
                            'warping_method', 'none'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_csf_proba',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'csf',
                            'space', 'average',
                            'transformation', 'none',
                            'modulation', 'none',
                            'warping_method', 'none'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_brain_mask',
                SetType('T1 Brain Mask'),
                SetWeakAttr('space', 'average',
                            ),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_grey_mask',
                SetType('T1 MRI tissue probability mask'),
                SetWeakAttr('space', 'average',
                            'tissue_class', 'grey'),

            # SPM12 pairwise/serial
            '<subject>_avg_<acquisition_sequence>_t1mri',
                SetType('T1 MRI mid-point average'),
                SetWeakAttr('space', 'average',
                            'modality', 't1mri'),
            '<subject>_avg_<acquisition_sequence>_flairmri',
                SetType('FLAIR MRI mid-point average'),
                SetWeakAttr('space', 'average',
                            'modality', 'flairmri'),

            'j_<subject>_avg_<acquisition_sequence>_to_{acquisition}',
                SetType('Jacobian determinant'),
                SetWeakAttr('space', 'average'),
            'jd_<subject>_{baseline}_{followup}',
                SetType('Jacobian rate'),
                SetWeakAttr('space', 'average'),
            'dv_<subject>_avg_<acquisition_sequence>_to_{acquisition}',
                SetType('Divergence map'),
                SetWeakAttr('space', 'average'),
            'dv_<subject>_{baseline}_{followup}',
                SetType('Divergence rate'),
                SetWeakAttr('space', 'average'),
            'y_<subject>_{acquisition}_to_avg_<acquisition_sequence>',
                SetType('SPM deformation field'),
                SetWeakAttr('orientation', 'acquisition_to_average',
                            'direction', 'forward',
                            'warping_method', 'none'),
            # Native space
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_grey_proba',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'grey',
                            'space', 'halfway',
                            'transformation', 'none',
                            'modulation', 'none',
                            'warping_method', 'none',
                            'acquisition', 'average'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_white_proba',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'white',
                            'space', 'halfway',
                            'transformation', 'none',
                            'modulation', 'none',
                            'warping_method', 'none',
                            'acquisition', 'average'),
            # DARTEL imported
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_grey_proba_rigid_registered',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'grey',
                            'transformation', 'rigid',
                            'modulation', 'none',
                            'warping_method', 'none',
                            'acquisition', 'average'),
            '<subject>_{acquisition}_to_avg_<acquisition_sequence>_white_proba_rigid_registered',
                SetType('T1 MRI tissue probability map'),
                SetWeakAttr('tissue_class', 'white',
                            'transformation', 'rigid',
                            'modulation', 'none',
                            'warping_method', 'none',
                            'acquisition', 'average'),
    )
)

insert('{center}/{subject}/longitudinal_preprocessings/spm12Serial', 'avg_{acquisition_sequence}',
       SetContent(*long_spm_registration),
       SetWeakAttr('processing', 'spm12Serial'))
insert('{center}/{subject}/longitudinal_preprocessings/spm12Pairwise', 'avg_{acquisition_sequence}',
       SetContent(*long_spm_registration),
       SetWeakAttr('processing', 'spm12Pairwise'))
insert('{center}/{subject}/spm/cat12Segment', '{acquisition}',
       SetContent(*cat12_analysis_directory),
       SetWeakAttr('processing', 'cat12Segment'))
insert('{center}/{subject}/spm/spm12Segment', '{acquisition}',
       SetContent(*analysis_directory),
       SetWeakAttr('processing', 'spm12Segment'))
insert('{center}/{subject}/spm/spm8VBMSegmentation', '{acquisition}',
       SetContent(*analysis_directory),
       SetWeakAttr('processing', 'spm8VBMSegmentation'))
insert('{center}/{subject}/spm/spm8NewSegment', '{acquisition}',
       SetContent(*analysis_directory),
       SetWeakAttr('processing', 'spm8NewSegment'))
insert('{center}/{subject}/spm/spm12Shoot', '{acquisition}',
       SetContent(*shoot_analysis_directory),
       SetWeakAttr('processing', 'spm12Shoot'))

# Should not be here ?
insert('{center}/{subject}/nuclear_imaging/{processing}', '{acquisition}',
       SetContent('t1mri',
                  SetContent('{analysis}_from_{segmentation_method}',
                             SetContent("t1mri_space",
                                        SetContent('<subject>_intracranial_labels',
                                                   SetType('T1 MRI intracranial labels'),
                                                   SetWeakAttr('space', 't1mri'),
                                                   '<subject>_intracranial_labels', SetType('T1 MRI intracranial labels translation'), SetWeakAttr('space', 't1mri'),
                                                   )))))
