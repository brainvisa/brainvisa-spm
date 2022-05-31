import numpy
import os
import shutil
from tempfile import mkdtemp

from brainvisa.processes import Application, Signature
from brainvisa.processes import ReadDiskItem, WriteDiskItem, Choice, Integer
from brainvisa.processes import ListOf, Float, Matrix
from brainvisa.processes import getAllFormats
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.util.deformations import Deformations
from soma.spm.spm12.util.deformations import composition
from soma.spm.spm12.util.deformations.output import SaveDeformation

configuration = Application().configuration

userLevel = 1
name = 'spm12 - Deformations : composition - generic'

deformations = 'Deformations parameters {}'
output = 'Output'

OUTPUT_SECTION = {
    'output_deformation': WriteDiskItem('4D Volume', getAllFormats(),
                                        section=output),
    'batch_location': WriteDiskItem('Matlab SPM script', 'Matlab script',
                                    section=output),
}

signature = Signature(
    'deformation_number', Integer(),
)
signature.update(OUTPUT_SECTION)


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


def deformation_type_choice(num):
    return Choice(
        ('None', ''),
        ('Dartel flow', 'dartel'),
        ('Deformation Field', 'deformation'),
        ('Identity (Reference Image)', 'identity_image'),
        ('Identity (Bounding Box and Voxel Size)', 'identity_shape'),
        ('Imported sn.mat', 'imported_mat'),
        # 'Inverse',
        # 'Composition',
        section=deformations.format(num)
    )


def dartel_params(num):
    return {
        f'flow_field_{num}': ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                                          section=deformations.format(num)),
        f'direction_{num}': Choice(('Forward', [0, 1]), ('Backward', [1, 0]),
                                   section=deformations.format(num)),
        f'time_step_{num}': Choice(*[(2**i, i) for i in range(10)],
                                   section=deformations.format(num)),
        f'dartel_template_{num}': ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                                               section=deformations.format(num))
    }


def deformation_params(num):
    return {
        f'deformation_field_{num}': ReadDiskItem('4D Volume', getAllFormats(),
                                                 section=deformations.format(num))
    }


def identity_image_params(num):
    return {
        f'base_image_{num}': ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                                          section=deformations.format(num))
    }


def identity_params(num):
    return {
        f'voxel_size_{num}': ListOf(Float(),
                                    section=deformations.format(num)),
        f'bounding_box_{num}': Matrix(length=2, width=3,
                                      section=deformations.format(num))
    }


def imported_mat_params(num):
    return {
        f'param_file_{num}': ReadDiskItem('Any Type', getAllFormats(),
                                          section=deformations.format(num)),
        f'voxel_size_{num}': ListOf(Float(),
                                    section=deformations.format(num)),
        f'bounding_box_{num}': Matrix(length=2, width=3,
                                      section=deformations.format(num))
    }


def initialization(self):
    self.addLink(None, 'deformation_number', self.update_deformation_number)
    self.deformation_number = 1
    self.addLink('batch_location', 'output_deformation', self.update_batch_path)
    

def update_batch_path(self, proc):
    if self.output_deformation:
        output_dir = os.path.dirname(self.output_deformation.fullPath())
        return os.path.join(output_dir, 'spm12_deformation_composition_job.m')
    else:
        return ''


def get_param_num(self, param_name: str) -> int:
    end_name = param_name.split('_')[-1]
    if end_name.isdigit():
        return int(end_name)
    return 0
        

def update_deformation_number(self, deformation_number):
    if deformation_number < 1:
        self.deformation_number = deformation_number = 1
    signature = self.signature
    n_defined = len([i for i in self.signature if i.startswith('deformation_type')])

    if deformation_number < n_defined:
        params_to_remove = [param for param in signature
                            if self.get_param_num(param) > deformation_number]
        for param in params_to_remove:
            del signature[param]

    elif deformation_number > n_defined:
        for output_param in OUTPUT_SECTION:
            del signature[output_param]
        for i in range(n_defined + 1, deformation_number + 1):
            signature[f'deformation_type_{i}'] = deformation_type_choice(i)
            self.addLink(None, f'deformation_type_{i}', lambda x, num=i: self.update_defo_type(num))
        signature.update(OUTPUT_SECTION)
        
    self.changeSignature(signature)
    

def update_defo_type(self, num):
    deformation_type = getattr(self, f'deformation_type_{num}')
    
    # Empty parameters of the deformation "num" to fill with good parameters
    defo_params = [param for param in self.signature
                   if self.get_param_num(param) == num
                   and not param.startswith('deformation_type_')]
    for param in defo_params:
        del self.signature[param]
    
    # Complete deformation "num" according to deformation_type
    if deformation_type == 'dartel':
        self.signature.update(dartel_params(num))
        setattr(self, f'direction_{num}', 'Backward')
        setattr(self, f'time_step_{num}', 64)
        self.setOptional(f'dartel_template_{num}')
    
    elif deformation_type == 'deformation':
        self.signature.update(deformation_params(num))
    
    elif deformation_type == 'identity_image':
        self.signature.update(identity_image_params(num))
        
    elif deformation_type == 'identity_shape':
        self.signature.update(identity_params(num))
        self.setOptional(f'voxel_size_{num}', f'bounding_box_{num}')
    
    elif deformation_type == 'imported_mat':
        self.signature.update(imported_mat_params(num))
        self.setOptional(f'voxel_size_{num}', f'bounding_box_{num}')
    
    self.changeSignature(self.signature)


def execution(self, context):

    temp_directory = context.temporary('Directory')
    deformations = Deformations()
    for i in range(1, self.deformation_number + 1):
        deformation_type = getattr(self, f'deformation_type_{i}')
        if deformation_type == 'dartel':
            deformation_element = composition.DartelFlow()
            deformation_element.flow_field_path = getattr(self, f'flow_field_{i}').fullPath()
            deformation_element.flow_direction = getattr(self, f'direction_{i}')
            deformation_element.time_step = getattr(self, f'time_step_{i}')
            deformation_element.setDartelTemplatePath(getattr(self, f'dartel_template_{i}').fullPath())

        elif deformation_type == 'deformation':
            deformation_element = composition.DeformationField()
            deformation_file = getattr(self, f'deformation_field_{i}').fullPath()
            if deformation_file.endswith('.gz'):
                src_gz = shutil.copy(deformation_file, temp_directory.fullPath())
                context.system('gunzip', src_gz)
                source = '.'.join(src_gz.split('.')[:-1])
            else:
                source = deformation_file
            deformation_element.deformation_field_path = source
                
        elif deformation_type == 'identity_image':
            deformation_element = composition.IdentityFromImage()
            deformation_element.reference_image_path = getattr(self, f'base_image_{i}').fullPath()
                
        elif deformation_type == 'identity_shape':
            deformation_element = composition.Identity()
            voxel_size = getattr(self, f'voxel_size_{i}')
            if voxel_size:
                deformation_element.voxel_size = voxel_size
            bounding_box = getattr(self, f'bounding_box_{i}')
            if bounding_box:
                deformation_element.bounding_box = numpy.array(bounding_box)

        elif deformation_type == 'imported_mat':
            deformation_element = composition.MatFileImported()
            deformation_element.parameter_file_path = getattr(self, f'param_file_{i}').fullPath()
            voxel_size = getattr(self, f'voxel_size_{i}')
            if voxel_size:
                deformation_element.voxel_size = voxel_size
            bounding_box = getattr(self, f'bounding_box_{i}')
            if bounding_box:
                deformation_element.bounding_box = numpy.array(bounding_box)
        
        deformations.appendDeformation(deformation_element)
    
    save_deformation = SaveDeformation()
    
    deformation_tmp = context.temporary('NIFTI-1 image')
    deformation_name = os.path.basename(deformation_tmp.fullPath())
    output_dir = os.path.dirname(deformation_tmp.fullPath())
    
    save_deformation.setDeformationName(deformation_name)
    save_deformation.setOutputDestinationToOutputDirectory(output_dir)
    save_deformation.setOutputDeformationPath(self.output_deformation.fullPath())

    deformations.appendOutput(save_deformation)

    spm = validation()
    spm.addModuleToExecutionQueue(deformations)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
