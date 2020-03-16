# -*- coding: utf-8 -*-
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
from __future__ import absolute_import
from __future__ import print_function
from brainvisa.processes import *
from soma.spm import csv_converter

all_available_types = sorted([ t.name for t in getAllDiskItemTypes() ])
all_available_formats = sorted([ t.name for t in getAllFormats() ])

userLevel = 0
name = "Create/update covariate table"

signature = Signature(
  'diskitem_type', OpenChoice(),
  'diskitem_format', OpenChoice(),
  'subjects', ListOf(ReadDiskItem(all_available_types[0], all_available_formats[0])),
  'field_needed', ListOf(OpenChoice()),
  'covariate_table', WriteDiskItem( 'Covariate table for SPM', 'CSV file'),
  'doing_if_exists', Choice("delete old", "keep old"),
  'unique_database', Boolean(),
)

def initialization(self):
  self.signature[ 'diskitem_type' ].setChoices(*all_available_types)
  self.signature[ 'diskitem_format' ].setChoices(*all_available_formats)

  self.addLink(None, 'diskitem_type', self.updateSignatureAboutTypeAndFormat)
  self.addLink(None, 'diskitem_format', self.updateSignatureAboutTypeAndFormat)
  self.addLink(None, 'subjects', self.updateSignatureAboutFieldNeeded)

  self.diskitem_type = "4D Volume"
  self.diskitem_format = "NIFTI-1 image"
  self.doing_if_exists = "keep old"

def updateSignatureAboutTypeAndFormat(self, proc):
  print((self.diskitem_type, self.diskitem_format))
  if self.diskitem_type in all_available_types and self.diskitem_format in all_available_formats:
    self.signature["subjects"] = ListOf(ReadDiskItem(self.diskitem_type, self.diskitem_format))
    self.changeSignature(self.signature)
  else:
    pass#OpenChoice causes problems during writing

def updateSignatureAboutFieldNeeded(self, proc):
  if self.subjects:
    self.signature[ 'field_needed' ] = ListOf(Choice(*list(self.subjects[0].hierarchyAttributes().keys())))
    self.changeSignature(self.signature)
  else:
    pass

def execution( self, context ):
  if not self.unique_database or self.onlyOneDatabaseUsed():
    if os.path.exists(self.covariate_table.fullPath()):
      csv_dict, csv_row_header = csv_converter.reverse( self.covariate_table.fullPath() )
      covariate_list = list(csv_dict[list(csv_dict.keys())[0]].keys())
      if sorted(csv_row_header) != sorted(self.field_needed):
        raise ValueError("old and new field_need are different")
      else:
        pass
    else:
      csv_dict = {}
      covariate_list = ['covariate']

    old_subject_id_list = list(csv_dict.keys())
    new_subject_id_list = []
    for diskitem in self.subjects:
      subject_id_list = []
      for field in self.field_needed:
        subject_id_list.append(diskitem.hierarchyAttributes()[field])
      subject_id = ';'.join(subject_id_list)
      new_subject_id_list.append(subject_id)
      if not subject_id in list(csv_dict.keys()):
        csv_dict[subject_id] = {}
        for covariate in covariate_list:
          csv_dict[subject_id][covariate] = ''
      else:
        pass
    if self.doing_if_exists == "delete old":
      old_subject_id_list = list(set(old_subject_id_list)-set(new_subject_id_list))
      for old_subject_id in old_subject_id_list:
        del csv_dict[old_subject_id]
    elif self.doing_if_exists == "keep old":
      pass#do nothing
    else:
      raise ValueError("Unvalid doing_if_exists choice")

    csv_converter.convert(csv_dict, self.covariate_table.fullPath(), self.field_needed)
  else:
    context.error("All subjects must come from same database")

def onlyOneDatabaseUsed(self):
  database_list = []
  for diskitem in self.subjects:
    database_list.append(diskitem.hierarchyAttributes()['_database'])

  database_number = len(set(database_list))
  if database_number == 1:
    return True
  else:
    return False