from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, moveSPMPath, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode


class WritingVolumeAtlases(object):
    """[summary]

    Parameters
    ----------
    object : [type]
        [description]
    """
    def __init__(self):
        self._batch_prefix = "ROImenu.atlases"
        self.process_ROI = False
        self.neuromorphometrics = "1"
        self.lpba40 = "0"
        self.cobra = "1"
        self.hammers = "0"
        self.ibsr = "0"
        self.aal3 = "0"
        self.mori = "0"
        self.anatomy = "0"
        self.julichbrain = "0"
        self.schaefer_100_parsels = "0"
        self.schaefer_200_parsels = "0"
        self.schaefer_400_parsels = "0"
        self.schaefer_600_parsels = "0"
        self.own_atlas_path = None
        
    def set_process_ROI_choice(self, choice):
        self.process_ROI = bool(int(choice))
    
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def set_own_atlas_path(self, own_atlas_path):
        self.own_atlas_path = own_atlas_path
    
    def set_atlas_choice(self, atlas_name, choice):
        """Set the atlas value

        Parameters
        ----------
        atlas_name : str
            Atlas name, need correspond to one of the class parameters
        choice : bool
            Choice of using the atlas_name
        """
        if getattr(self, atlas_name):
            setattr(self, atlas_name, str(int(choice)))
        else:
            print('WARNING : %s is not a valid atlas' % atlas_name)
            
    def getStringListForBatch(self):
        batch_list = []
        if not self.process_ROI:
            batch_list.append("ROImenu.noROI = struct([])")
            return batch_list
        else:
            batch_list.append("neuromorphometrics = %s;" % self.neuromorphometrics)
            batch_list.append("lpba40 = %s;" % self.lpba40)
            batch_list.append("cobra = %s;" % self.cobra)
            batch_list.append("hammers = %s;" % self.hammers)
            batch_list.append("ibsr = %s;" % self.ibsr)
            batch_list.append("aal3 = %s;" % self.aal3)
            batch_list.append("mori = %s;" % self.mori)
            batch_list.append("anatomy = %s;" % self.anatomy)
            batch_list.append("julichbrain = %s;" % self.julichbrain)
            batch_list.append("Schaefer2018_100Parcels_17Networks_order = %s;" % self.schaefer_100_parsels)
            batch_list.append("Schaefer2018_200Parcels_17Networks_order = %s;" % self.schaefer_200_parsels)
            batch_list.append("Schaefer2018_400Parcels_17Networks_order = %s;" % self.schaefer_400_parsels)
            batch_list.append("Schaefer2018_600Parcels_17Networks_order = %s;" % self.schaefer_600_parsels)
            if self.own_atlas_path:
                batch_list.append("ownatlas = {%s};" % self.own_atlas_path)
            else:
                batch_list.append("ownatlas = {''};")
                
            return addBatchKeyWordInEachItem(self._batch_prefix, batch_list)


class WritingOutputs(object):
    def __init__(self, batch_prefix, values=["0", "0", "0", "0"]):
        self.native, self.warped, self.modulated, self.dartel = values
        self._batch_prefix = batch_prefix
        
    def set_native_choice(self, choice):
        self.native = choice
        
    def set_warped_choice(self, choice):
        self.warped = choice
    
    # Modulated    
    def set_modulated_no(self):
        self.modulated = '0'
        
    def set_modulated_affine_non_linear(self):
        self.modulated = '1'
        
    def set_modulated_non_linear(self):
        self.modulated = '2'
        
    def set_modulated_both(self):
        self.modulated = '3'
    
    # Dartel
    def set_dartel_no(self):
        self.dartel = '0'
    
    def set_dartel_rigid(self):
        self.dartel = '1'
    
    def set_dartel_affine(self):
        self.dartel = '2'
    
    def set_dartel_both(self):
        self.dartel = '3'
    
    def getStringListForBatch(self):
        if self._batch_prefix is not None:
            batch_list = []
            if self.native is not None:
                batch_list.append("native = %s;" % self.native)
            if self.warped is not None:
                batch_list.append("warped = %s;" % self.warped)
            if self.modulated is not None:
                batch_list.append("mod = %s;" % self.modulated)
            if self.dartel is not None:
                batch_list.append("dartel = %s;" % self.dartel)
            return addBatchKeyWordInEachItem(self._batch_prefix, batch_list)
        else:
            raise Exception("WritingOutputs class need batch_prefix")


class WritingOptions(object):
    """[summary]

    Parameters
    ----------
    object : [type]
        [description]
    """
    def __init__(self):
        self._batch_prefix = "output"
        self.surface_thickness = "0"
        self.jacobian_warped = "0"
        self.deformation_fields = ["0", "0"]
        self.registration_matrix = "0"
        
        self.output_atlases = WritingVolumeAtlases()
        self.grey = WritingOutputs("GM", ["0", "0", "1", "0"])
        self.white = WritingOutputs("WM", ["0", "0", "1", "0"])
        self.csf = WritingOutputs("CSF")
        # self.wmh = WritingOutputs("WMH")
        self.sl = WritingOutputs("SL")
        self.tpmc = WritingOutputs("TPMC")
        self.atlas = WritingOutputs("atlas", ["0", "0", None, "0"])
        self.label = WritingOutputs("label", ["1", "0", None, "0"])
        self.bias = WritingOutputs("bias", ["0", "1", None, "0"])
        self.las = WritingOutputs("las", ["0", "0", None, "0"])
        
        self.percent_position = WritingOutputs("pp", ["0", "0", None, "0"])
    
    def set_surface_no(self):
        self.surface_thickness = "0"
        
    def set_surface_yes(self):
        self.surface_thickness = "1"
        
    def set_surface_preview(self):
        self.surface_thickness = "5"
    
    @checkIfArgumentTypeIsAllowed(bool, 1)
    def set_jacobian(self, choice):
        self.jacobian_warped = str(int(choice))
    
    @checkIfArgumentTypeIsAllowed(bool, 1)
    def set_deformation_field_forward_choice(self, choice):
        self.deformation_fields[0] = str(int(choice))
        
    @checkIfArgumentTypeIsAllowed(bool, 1)
    def set_deformation_field_inverse_choice(self, choice):
        self.deformation_fields[1] = str(int(choice))
        
    @checkIfArgumentTypeIsAllowed(bool, 1)
    def set_registration_matrix_choice(self, choice):
        self.registration_matrix = str(int(choice))
        
    def getStringListForBatch(self):
        if self._batch_prefix is not None:
            batch_list = []
            batch_list.extend(self.output_atlases.getStringListForBatch())
            batch_list.extend(self.grey.getStringListForBatch())
            batch_list.extend(self.white.getStringListForBatch())
            batch_list.extend(self.csf.getStringListForBatch())
            # batch_list.extend(self.wmh.getStringListForBatch())
            batch_list.extend(self.sl.getStringListForBatch())
            batch_list.extend(self.tpmc.getStringListForBatch())
            batch_list.extend(self.atlas.getStringListForBatch())
            batch_list.extend(self.label.getStringListForBatch())
            batch_list.extend(self.bias.getStringListForBatch())
            batch_list.extend(self.las.getStringListForBatch())
            batch_list.extend(self.percent_position.getStringListForBatch())
            batch_list.append('surface = %s;' % self.surface_thickness)
            batch_list.append('surf_measures = 1;')
            batch_list.append('jacobianwarped = %s;' % self.jacobian_warped)
            batch_list.append('warps = [%s];' % ' '.join(self.deformation_fields))
            batch_list.append('rmat = %s;' % self.registration_matrix)
            return addBatchKeyWordInEachItem(self._batch_prefix, batch_list)
        else:
            raise Exception("WritingOptions class need batch_prefix")
