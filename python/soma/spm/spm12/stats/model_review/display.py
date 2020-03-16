# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

from soma.spm.spm_batch_maker_utils import convertlistToSPMString


class Display(object):
  """Select graphical report"""
#==============================================================================
#
#==============================================================================
class DesignMatrix(Display):
    """Review Design Matrix."""
    def __init__(self):
        pass

    def getStringListForBatch(self):
        return ["display.matrix = 1;"]
#==============================================================================
#
#==============================================================================
class DesignOrthogonality(Display):
    """Review Design Orthogonality."""
    def __init__(self):
        pass

    def getStringListForBatch(self):
        return ["display.orth = 1;"]
#==============================================================================
#
#==============================================================================
class FilesAndFactors(Display):
    """Review Files & Factors. Only available for second-level models."""
    def __init__(self):
        pass

    def getStringListForBatch(self):
        return ["display.factors = 1;"]
#==============================================================================
#
#==============================================================================
class Covariates(Display):
    """Review Covariance Structure. Only available for second-level models."""
    def __init__(self):
        pass

    def getStringListForBatch(self):
        return ["display.covariates = 1;"]
#==============================================================================
#
#==============================================================================
class Condition(Display):
    """Review Condition. Only available for fMRI first-level models."""
    def __init__(self):
        self.session_indexes = None
        self.condition_indexes = None

    @checkIfArgumentTypeIsAllowed(list, 1)
    def setSessionIndexes(self, index_list):
        self.session_indexes = index_list

    @checkIfArgumentTypeIsAllowed(list, 1)
    def setConditionIndexes(self, index_list):
        self.condition_indexes = index_list

    def getStringListForBatch(self):
        if not None in [self.session_indexes, self.condition_indexes]:
            batch_list = []
            batch_list.append("display.sess = ;" % convertlistToSPMString(self.session_indexes))
            batch_list.append("display.cond = ;" % convertlistToSPMString(self.condition_indexes))
        return batch_list
#==============================================================================
#
#==============================================================================
class CovarianceStructure(Display):
    """Review Covariance Structure."""
    def __init__(self):
        pass

    def getStringListForBatch(self):
        return ["display.covariance = 1;"]
