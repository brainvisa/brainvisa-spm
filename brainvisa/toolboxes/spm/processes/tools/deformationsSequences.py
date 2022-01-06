import os

from brainvisa.processes import Signature
from brainvisa.processes import ReadDiskItem, WriteDiskItem, ListOf
from brainvisa.processes import getAllFormats

name = "Apply multiple deformations"
userLevel = 1

signature = Signature(
    'input_images', ListOf(ReadDiskItem('4D Volume', 'aims readable volume formats')),
    'deformation_1', ReadDiskItem('Any Type', getAllFormats()),
    'deformation_2', ReadDiskItem('Any Type', getAllFormats()),
    'deformation_3', ReadDiskItem('Any Type', getAllFormats()),
    
    'output_images', ListOf(WriteDiskItem('4D Volume', 'aims writable volume formats'))
)


def initialization(self):
    self.setOptional('deformation_2', 'deformation_3')


def execution(self, context):

    if len(self.input_images) != len(self.output_images):
        raise ValueError('Input and output parameters must have the same length.')
    
    deformation_list = [getattr(self, f'deformation_{i+1}') for i in range(3)]
    deformation_list = [d for d in deformation_list if d]
    
    input_tmp = [im.fullPath() for im in self.input_images]
    output_tmp = [context.temporary('NIFTI-1 image') for _ in self.input_images]

    for deformation in deformation_list[:-1]:
        self.apply_deformation(context, input_tmp, output_tmp, deformation)
        input_tmp = output_tmp
        
    self.apply_deformation(context, input_tmp, self.output_images,
                           deformation_list[-1])
    

def is_deformation_field(deformation_path):
    deformation_file = os.path.basename(deformation_path)
    return (
        deformation_file.endswith('.nii.gz')
        or deformation_file.endswith('.nii')
    ) and deformation_file.startswith('y_')


def apply_deformation(self, context, input_file, output_file, deformation):
    if str(deformation.type) == 'SPM deformation field' or is_deformation_field(deformation.fullPath()):
        context.runProcess('SPM12deformations_generic',
                           input_images=input_file,
                           deformation_type='deformation_field',
                           deformation_field=deformation.fullPath(),
                           output_destination='Source directories',
                           custom_outputs=True,
                           images_deformed=output_file)

    elif deformation.fullPath().endswith('_sn.mat'):
        context.runProcess('SPM12deformations_generic',
                           input_images=input_file,
                           deformation_type='spatial_normalisation_param',
                           spatial_normalisation_params=deformation.fullPath(),
                           custom_outputs=True,
                           images_deformed=output_file)

    elif str(deformation.type) == 'SPM transformation' or deformation.fullPath().endswith('.mat'):
        context.runProcess('SPM12Reorient_generic',
                           images_to_reorient=input_file,
                           reorient_by='saved_matrix',
                           saved_matrix=deformation.fullPath(),
                           custom_outputs=True,
                           images_reoriented=output_file)
