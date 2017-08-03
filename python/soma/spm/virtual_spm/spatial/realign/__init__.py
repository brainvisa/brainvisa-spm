# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString
from soma.spm.spm_batch_maker_utils import moveSPMPath
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.virtual_spm.spatial.realign.estimation_options import EstimationOptions
from soma.spm.virtual_spm.spatial.realign.reslice_options import ResliceOptions


class Realign():
  """
  """


class EstimateAndReslice(Realign):
  """
  This  routine  realigns  a  time-series  of images acquired from the same subject using a least squares approach and a 6
  parameter  (rigid  body) spatial transformation.  The first image in the list specified by the user is used as a reference to
  which  all subsequent scans are realigned. The reference scan does not have to be the first chronologically and it may be
  wise to chose a "representative scan" in this role.
  The  aim  is primarily to remove movement artefact in fMRI and PET time-series (or more generally longitudinal studies) .
  The  headers  are  modified for each of the input images, such that. they reflect the relative orientations of the data. The
  details  of  the  transformation  are  displayed  in  the  results  window  as  plots  of  translation  and  rotation.  A set of
  realignment parameters are saved for each session, named rp_*.txt. After realignment, the images are resliced such that
  they  match  the  first  image selected voxel-for-voxel. The resliced images are named the same as the originals, except
  that they are prefixed by 'r'.
  """

  @checkIfArgumentTypeIsAllowed(list, 1)
  def addSessionPathList(self, session_path_list):
    """
    Select  scans  for  this  session.  In  the  coregistration step, the sessions are first
    realigned  to  each  other, by aligning the first scan from each session to the first
    scan  of the first session.  Then the images within each session are aligned to the
    first  image  of  the  session.  The  parameter  estimation  is  performed  this way
    because  it is assumed (rightly or not) that there may be systematic differences in
    the images between sessions.
    """
    self.session_path_list.append(session_path_list)

  @checkIfArgumentTypeIsAllowed(list, 1)
  def addSessionRealignedPathList(self, session_path_list):
    self.session_realigned_path_list.append(session_path_list)

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMeanOuputPath(self, mean_output_path):
    self.mean_output_path = mean_output_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def addSessionRealignmentParametersPath(self, realignment_parameters_path):
    self.realignment_parameters_path_list.append(realignment_parameters_path)

  @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)
  def replaceEstimationOptions(self, estimation_options):
    del self.estimation_options
    self.estimation_options = estimation_options

  @checkIfArgumentTypeIsAllowed(ResliceOptions, 1)
  def replaceResliceOptions(self, reslice_options):
    del self.reslice_options
    self.reslice_options = reslice_options

  def getStringListForBatch(self):
    if self.session_path_list:
      batch_list = []
      data_string_converted = '{\n'
      for path_list in self.session_path_list:
        data_string_converted += '{\n' + convertPathListToSPMBatchString(path_list) + '}\n'
      data_string_converted += '}'
      batch_list.append("spm.spatial.realign.estwrite.data = %s;" % data_string_converted)
      batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.realign.estwrite", self.estimation_options.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.realign.estwrite", self.reslice_options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("At least one session is required")

  def _moveSPMDefaultPathsIfNeeded(self):
    reslice_choices = self.reslice_options.getReslicedImagesChoices()
    prefix = self.reslice_options.getCurrentFilenamePrefix()
    for session_index, session_path in enumerate(self.session_path_list):
      if reslice_choices[0] == 0:
        pass
      elif reslice_choices[0] == 1:
        if self.session_realigned_path_list and len(self.session_realigned_path_list[session_index]) == len(session_path) - 1:
          tmp_list = session_path[1:-1]
          for input_path, output_path in zip(tmp_list, self.session_realigned_path_list[session_index]):
            moveSPMPath(input_path, output_path, prefix=prefix)
      elif reslice_choices[0] == 2:
        if self.session_realigned_path_list and len(self.session_realigned_path_list[session_index]) == len(session_path):
          for input_path, output_path in zip(session_path, self.session_realigned_path_list[session_index]):
            moveSPMPath(input_path, output_path, prefix=prefix)
      else:
        raise ValueError("Unvalid first resclices choices")

      if self.realignment_parameters_path_list:
        moveSPMPath(session_path[0], self.realignment_parameters_path_list[session_index], prefix="rp_", extension="txt")
      else:
        pass

    if reslice_choices[1] == 0:
      pass
    elif reslice_choices[1] == 1:
      if self.mean_output_path is not None:
        moveSPMPath(self.session_path_list[0][0], self.mean_output_path, prefix="mean")
      else:
        pass
    else:
      raise ValueError("Unvalid second resclices choices")

