# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class PairedTTestDesign():
  def addScansPair(self, scans_list):
    scans_pair = ScansPair()
    scans_pair.setScans( scans_list )
    self.scans_pair_list.append(scans_pair)
    
  def clearScanPair(self):
    for scans_pair in self.scans_pair_list:
      del scans_pair
    self.scans_pair_list = []
      
  def enableGrandMeanScaling(self):
    """
    This option is only used for PET data.
    Selecting YES will specify 'grand mean scaling by factor' which could be eg. 'grand
    mean scaling by subject' if the factor is 'subject'.
    Since  differences  between  subjects  may  be due to gain and sensitivity effects,
    AnCova  by  subject  could  be  combined with "grand mean scaling by subject" to
    obtain  a  combination of between subject proportional scaling and within subject
    AnCova.
    """
    self.grand_mean_scaling = 1
    
  def disableGrandMeanScaling(self):
    """
    This option is only used for PET data.
    Selecting YES will specify 'grand mean scaling by factor' which could be eg. 'grand
    mean scaling by subject' if the factor is 'subject'.
    Since  differences  between  subjects  may  be due to gain and sensitivity effects,
    AnCova  by  subject  could  be  combined with "grand mean scaling by subject" to
    obtain  a  combination of between subject proportional scaling and within subject
    AnCova.
    """
    self.grand_mean_scaling = 0
    
  def enableANCOVA(self):
    """
    This option is only used for PET data.
    Selecting   YES  will  specify  'ANCOVA-by-factor'  regressors.  This  includes  eg.
    'Ancova  by  subject'  or  'Ancova  by  effect'.  These  options  allow  eg.  different
    subjects to have different relationships between local and global measurements.
    """
    self.ANCOVA = 1
    
  def disableANCOVA(self):
    """
    This option is only used for PET data.
    Selecting   YES  will  specify  'ANCOVA-by-factor'  regressors.  This  includes  eg.
    'Ancova  by  subject'  or  'Ancova  by  effect'.  These  options  allow  eg.  different
    subjects to have different relationships between local and global measurements.
    """
    self.ANCOVA = 0
    
  def getStringListForBatch( self ):
    if self.scans_pair_list:
      batch_list = []
      if len(self.scans_pair_list) == 1:
        batch_list = addBatchKeyWordInEachItem("des.pt.pair", self.scans_pair_list[0].getStringListForBatch())
      else:
        for scans_pair_index, scans_pair in enumerate(self.scans_pair_list):
          batch_list.extend(addBatchKeyWordInEachItem("des.pt.pair(%i)" % (scans_pair_index+1), scans_pair.getStringListForBatch()))
      batch_list.append("des.t2.gmsca = %i;" % self.grand_mean_scaling)
      batch_list.append("des.t2.ancova = %i;" % self.ANCOVA)
      return batch_list
    else:
      raise ValueError('PairedTTestDesign needs scans pair list')
    
class ScansPair():    
  def setScans(self, scans_list):
    if len(scans_list) == 2:
      self.scan_1 = scans_list[0]
      self.scan_2 = scans_list[1]
    else:
      raise ValueError('Scans pair must contain exactly 2 paths' )
  
  def getStringListForBatch( self ):
    batch_list = ["scans = {\n'%s,1'\n'%s,1'\n};" % (self.scan_1, self.scan_2)]
    return batch_list