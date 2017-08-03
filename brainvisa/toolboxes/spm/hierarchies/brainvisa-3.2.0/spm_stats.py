include( 'base' )
# TODO : add covariate, fwhm and other parameters

spm_files = (
    '{analysis}', SetType('SPM workspace directory'), SetContent(
        'SPM', SetType('SPM design specification'),
        'spm_{date}', SetType('SPM graphical report'),
        'spm{contrast_type}_{contrast_index}_{basename}_labelled', SetType('SPM labelled filtered image'),
        'spm{contrast_type}_{contrast_index}_{basename}_translation', SetType('SPM labelled filtered image translation'),
        'spm{contrast_type}_{contrast_index}_{basename}', SetType('SPM filtered image'),
    ),
)
#'analyzes/spm_stats/'
spm_stats = (
    '{factorial_design}', SetContent(
        '{first_group}_compare_to_{second_group}',
            SetContent(*spm_files),
        '{group_name}',
            SetContent(*spm_files)
    ),
)

insert( 'analyzes', 'spm_stats', SetContent(*spm_stats))