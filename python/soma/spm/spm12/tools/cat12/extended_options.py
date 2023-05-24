from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import os


class RegistrationOptions(object):
    def __init__(self):
        self.type = 'shooting'
        self.template = ''
        self.method = '0.5'
    
    def set_registration_shooting(self):
        self.type = 'shooting'
    
    def set_registration_dartel(self):
        self.type = 'dartel'
    
    @checkIfArgumentTypeIsAllowed(str, 1)
    def set_template(self, template_path):
        if os.path.exists(template_path):
            self.template = template_path
        else:
            raise FileNotFoundError('Template file does not exist!')
    
    def set_shooting_method_default(self):
        self.method = '4'
    
    def set_shooting_method_opt_vox(self):
        self.method = '5'
    
    def set_shooting_method_opt_fast(self):
        self.method = 'eps'
    
    def set_shooting_method_opt_standard(self):
        self.method = '0.5'
    
    def set_shooting_method_opt_fine(self):
        self.method = '1.0'
    
    def set_shooting_method_opt_strong(self):
        self.method = '11'
    
    def set_shooting_method_opt_medium(self):
        self.method = '12'
    
    def set_shooting_method_opt_soft(self):
        self.method = '13'
    
    def getStringListForBatch(self):
        if self.template:
            batch_list = []
            if self.type == 'shooting':
                batch_list.append("shooting.shootingtpm = {'%s'};" % self.template)
                batch_list.append("shooting.regstr = %s;" % self.method)
            elif self.type == 'dartel':
                batch_list.append("dartel.darteltpm = {'%s'};" % self.template)
            return addBatchKeyWordInEachItem('registration', batch_list)
        else:
            raise Exception('A template is needed for RegistrationOptions')


class SurfaceOptions(object):
    def __init__(self):
        self.voxel_size = 0.5
        #self.corr_myelination = '0'
        self.cortical_surf = 0.7
        self.parahipp_surf = 0.1
        self.initial_closing_parahipp = '0'
    
    @checkIfArgumentTypeIsAllowed(float, 1)
    def set_voxel_size(self, size):
        self.voxel_size = size
    
    #def set_corr_myelination_choice(self, choice):
        #self.corr_myelination = str(int(choice))
    
    @checkIfArgumentTypeIsAllowed(float, 1)
    def set_cortical_surf(self, value):
        self.cortical_surf = value
        
    @checkIfArgumentTypeIsAllowed(float, 1)
    def set_parahipp_surf(self, value):
        self.parahipp_surf = value
    
    def set_closing_parahipp_choice(self, choice):
        self.initial_closing_parahipp = str(int(choice))
    
    def getStringListForBatch(self):
        batch_list = []
        batch_list.append('pbtres = %s;' % str(self.voxel_size))
        batch_list.append("pbtmethod = 'pbt2x';")
        batch_list.append('SRP = 22;')
        batch_list.append('reduce_mesh = 1;')
        batch_list.append('vdist = 2;')
        batch_list.append('scale_cortex = %s;' % str(self.cortical_surf))
        batch_list.append('add_parahipp = %s;' % str(self.parahipp_surf))
        batch_list.append('close_parahipp = %s;' % self.initial_closing_parahipp)
        #batch_list.append('pbtlas = %s;' % self.corr_myelination)
        return addBatchKeyWordInEachItem("surface", batch_list)


class ExtendedOptions(object):
    def __init__(self):
        # Segmentation options
        self.resampling_preproc_type = 'optimal'
        self.resampling_preproc_values = [1, 0.3] #[1, 0.1]CAT12.7
        self.COM_to_set_origin = "1"
        self.affine_preprocessing = "1070"
        self.noise_correction = "-Inf"
        self.initial_segmentation = "0"
        self.local_adaptative_seg = "0.5"
        self.skull_stripping = "2"
        self.clean_up = "0.5"
        self.wmh_correction = "2"
        # self.stroke_lesion_correction = "0"
        
        # Registration
        self.spatial_registration = RegistrationOptions()
        
        # Voxel size
        self.voxel_size = 1.5
        self.bounding_box = 12
        
        # Surface
        self.surface_options = SurfaceOptions()
        
        # Admin
        self.lazy_process = "0"
        self.error_handling = "1"
        self.verbose = "2"
        self.create_report = "2"
    
    # Use center-of-mass to set origin
    def unset_COM(self):
        self.center_to_set_origin = "0"
    
    def set_COM_default(self):
        self.center_to_set_origin = "1"
    
    def set_COM_noTPM(self):
        self.center_to_set_origin = "2"
    
    # Affine preprocessing
    def set_APP_default(self):
        self.affine_preprocessing = "1070"
    
    def set_APP_none(self):
        self.affine_preprocessing = "0"
        
    def set_APP_light(self):
        self.affine_preprocessing = "1"
        
    def set_APP_full(self):
        self.affine_preprocessing = "2"
        
    def set_APP_rough(self):
        self.affine_preprocessing = "1144"
        
    # def set_APP_animal(self):
    #     self.affine_preprocessing = "5"
    
    # Noise correction
    def set_noise_corr_medium(self):
        self.noise_correction = "-Inf"  # or 3?
        
    def set_noise_corr_none(self):
        self.noise_correction = "0"
        
    def set_noise_corr_classic(self):
        self.noise_correction = "1"
        
    def set_noise_corr_light(self):
        self.noise_correction = "2"
        
    # def set_noise_corr_strong(self):
    #     self.noise_correction = "4"
    
    # Initial segmentation
    def set_intial_seg_spm(self):
        self.initial_segmentation = '0'
        
    def set_intial_seg_kamap(self):
        self.initial_segmentation = '2'
        
    # Local adaptative segmentation
    def set_LAS_str_medium(self):
        self.local_adaptative_seg = "0.5"
        
    def set_LAS_str_none(self):
        self.local_adaptative_seg = "0"
        
    def set_LAS_str_ultralight(self):
        self.local_adaptative_seg = "eps"
        
    def set_LAS_str_light(self):
        self.local_adaptative_seg = "0.25"
        
    def set_LAS_str_strong(self):
        self.local_adaptative_seg = "0.75"
        
    def set_LAS_str_heavy(self):
        self.local_adaptative_seg = "1"
    
    # Skull stripping
    def set_skull_stripping_none(self):
        self.skull_stripping = "-1"
        
    def set_skull_stripping_spm(self):
        self.skull_stripping = "0"
        
    def set_skull_stripping_gcut_medium(self):
        self.skull_stripping = "0.5"
        
    def set_skull_stripping_aprg(self):
        self.skull_stripping = "2"
        
    def set_skull_stripping_aprg_v2(self):
        self.skull_stripping = "2.5"
        
    def set_skull_stripping_aprg_v2_wider(self):
        self.skull_stripping = "2.1"
        
    def set_skull_stripping_aprg_v2_tighter(self):
        self.skull_stripping = "2.9"
    
    # Clean up strenght
    def set_clean_up_none(self):
        self.clean_up = "0"
        
    def set_clean_up_light(self):
        self.clean_up = "0.25"
        
    def set_clean_up_medium(self):
        self.clean_up = "0.5"
        
    def set_clean_up_strong(self):
        self.clean_up = "0.75"
        
    def set_clean_up_heavy(self):
        self.clean_up = "1.0"
        
    # White matter hyperintensities correction
    def set_wmh_correction_no(self):
        self.wmh_correction = "0"
    
    def set_wmh_correction_temporary(self):
        self.wmh_correction = "1"
    
    def set_wmh_correction_save_as_wm(self):
        self.wmh_correction = "2"
    
    def set_wmh_correction_as_separate_class(self):
        self.wmh_correction = "3"
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def set_resampling_preproc_optimal(self, values):
        if len(values) == 2:
            self.resampling_preproc_type = 'optimal'
            val = '[%s]' % ' '.join(str(v) for v in values)
            self.resampling_preproc_values = val
        else:
            raise ValueError("Input 'values' have to be list of 2 elements!")
        
    def set_resampling_preproc_native(self):
        self.resampling_preproc_type = 'native'
        self.resampling_preproc_values = 'struct([])'
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def set_resampling_preproc_best(self, values):
        if len(values) == 2:
            self.resampling_preproc_type = 'best'
            val = '[%s]' % ' '.join(str(v) for v in values)
            self.resampling_preproc_values = val
        else:
            raise ValueError("Input 'values' have to be list of 2 elements!")
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def set_resampling_preproc_fixed(self, values):
        if len(values) == 2:
            self.resampling_preproc_type = 'fixed'
            val = '[%s]' % ' '.join(str(v) for v in values)
            self.resampling_preproc_values = val
        else:
            raise ValueError("Input 'values' have to be list of 2 elements!")
    
    # Spatial registration
    
    @checkIfArgumentTypeIsAllowed(float, 1)
    def set_voxel_size(self, size):
        self.voxel_size = size
       
    @checkIfArgumentTypeIsAllowed(float, 1)
    def set_bounding_box(self, size):
        self.bounding_box = size
    
    # Report
    def unset_report(self):
        self.create_report = "0"
    
    def set_report_volume(self):
        self.create_report = "1"
        
    def set_report_volume_surfaces(self):
        self.create_report = "2"
    
    def set_lazy_choice(self, choice):
        self.lazy_process = str(int(choice))
    
    def set_error_handling_choice(self, choice):
        self.error_handling = str(int(choice))
        
    def set_verbose_none(self):
        self.verbose = '0'
        
    def set_verbose_default(self):
        self.verbose = '1'
    
    def set_verbose_details(self):
        self.verbose = '2'
    
    def getStringListForBatch(self):
        batch_list = []
        batch_list.append("segmentation.restypes.%s = %s;" % (self.resampling_preproc_type,
                                                              self.resampling_preproc_values))
        batch_list.append("segmentation.setCOM = %s;" % self.COM_to_set_origin)
        batch_list.append("segmentation.APP = %s;" % self.affine_preprocessing)
        batch_list.append("segmentation.affmod = 0;")
        batch_list.append("segmentation.NCstr = %s;" % self.noise_correction)
        batch_list.append("segmentation.spm_kamap = %s;" % self.initial_segmentation)
        batch_list.append("segmentation.LASstr = %s;" % self.local_adaptative_seg)
        batch_list.append("segmentation.LASmyostr = 0;")
        batch_list.append("segmentation.gcutstr = %s;" % self.skull_stripping)
        batch_list.append("segmentation.cleanupstr = %s;" % self.clean_up)
        batch_list.append("segmentation.BVCstr = 0.5;")
        batch_list.append("segmentation.WMHC = %s;" % self.wmh_correction)
        batch_list.append("segmentation.SLC = 0;")
        batch_list.append("segmentation.mrf = 1;")
        batch_list.extend(self.spatial_registration.getStringListForBatch())
        batch_list.append("vox = %s;" % str(self.voxel_size))
        batch_list.append("bb = %s;" % str(self.bounding_box))
        batch_list.extend(self.surface_options.getStringListForBatch())
        batch_list.append("admin.experimental = 0;")
        batch_list.append("admin.new_release = 0;")
        batch_list.append("admin.lazy = %s;" % str(self.lazy_process))
        batch_list.append("admin.ignoreErrors = %s;" % str(self.error_handling))
        batch_list.append("admin.verb = %s;" % str(self.verbose))
        batch_list.append("admin.print = %s;" % str(self.create_report))
        return addBatchKeyWordInEachItem("extopts", batch_list)
