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

include( 'builtin' )
include( 'spm' )

FileType('Matlab SPM deformation file', 'Matlab SPM file')

FileType('DARTEL analysis directory', 'Directory')

FileType('SPM field', '3D Volume')
FileType('HDW DARTEL flow field', 'SPM field')
FileType('SPM deformation field', 'SPM field')
FileType('Velocity field', 'SPM field')
FileType('T1 MRI Bias field', 'SPM field')#Voir avec Morpho

FileType('TPM HDW DARTEL created template', 'TPM HDW DARTEL template')

FileType('Jacobian determinant', '3D Volume')
FileType('Jacobian rate', '3D Volume')

FileType('Estimate T1 MRI raw volumes', 'Text file')
FileType('T1 MRI partial volume estimation', '3D Volume')
FileType('T1 MRI tissue probability map', '3D Volume')
FileType('T1 MRI tissue probability mask', 'Label volume')
## SPM12 Long
FileType('T1 MRI mid-point average', 'Raw T1 MRI')
FileType('FLAIR MRI mid-point average', '3D Volume')
FileType('Divergence map', '3D Volume')
FileType('Divergence rate', '3D Volume')
##
FileType('T1 MRI intracranial labels', 'Label volume')
FileType('T1 MRI intracranial labels translation', 'Text file', 'JSON file')
FileType('SPM tissue volumes', 'CSV file')
FileType('PET dynamic SPM realign results', 'Text file')

FileType('Subject Group', 'Any Type', 'JSON file')
FileType('Covariate table for SPM', 'CSV file')
