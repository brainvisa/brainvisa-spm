# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.util.deformations.composition import Composition as Composition_virtual
from soma.spm.virtual_spm.util.deformations.composition import MatFileImported as MatFileImported_virtual
from soma.spm.virtual_spm.util.deformations.composition import DartelFlow as DartelFlow_virtual
from soma.spm.virtual_spm.util.deformations.composition import DeformationField as DeformationField_virtual
from soma.spm.virtual_spm.util.deformations.composition import IdentityFromImage as IdentityFromImage_virtual
from soma.spm.virtual_spm.util.deformations.composition import Identity as Identity_virtual
from soma.spm.virtual_spm.util.deformations.composition import Inverse as Inverse_virtual

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_container import SPMContainer

import abc
import numpy

class Deformation():
  __metaclass__ = abc.ABCMeta

class Composition(Composition_virtual, SPMContainer, Deformation):
  def __init__(self):
    SPMContainer.__init__(self, Deformation)
#===============================================================================
# 
#===============================================================================
class MatFileImported(MatFileImported_virtual, Deformation):
  def __init__(self):
    self.parameter_file_path = None
    self.voxel_size = ["NaN", "NaN", "NaN"]
    self.bounding_box = numpy.array([["NaN", "NaN", "NaN"],["NaN", "NaN", "NaN"]])
#===============================================================================
# 
#===============================================================================
class DartelFlow(DartelFlow_virtual, Deformation):
  def __init__(self):
    self.flow_field_path = None
    self.flow_direction = [1, 0]
    self.time_step = 6
#===============================================================================
# 
#===============================================================================
class DeformationField(DeformationField_virtual, Deformation):
  def __init__(self):
    self.deformation_field_path = None
#===============================================================================
# 
#===============================================================================
class IdentityFromImage(IdentityFromImage_virtual, Deformation):
  def __init__(self):
    self.reference_image_path = None
#===============================================================================
# 
#===============================================================================
class Identity(Identity_virtual, Deformation):
  def __init__(self):
    self.voxel_size = None
    self.bounding_box = None
#===============================================================================
# 
#===============================================================================
class Inverse(Inverse_virtual, Deformation):
  def __init__(self):
    self.composition = None
    self.reference_image_path = None
    
  @checkIfArgumentTypeIsAllowed(Composition, 1)
  def setDeformationComposition(self, composition):
    super(Inverse, self).setDeformationComposition(composition)