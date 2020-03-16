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
from brainvisa.processes import *
from brainvisa.data.neuroHierarchy import databases

userLevel = 0
name = "Create Analysis"

signature = Signature(
  'database', Choice(),
  'analysis_name', String(),
  'analysis', WriteDiskItem('Analysis Dir', 'Directory'),
)

def initialization(self):
  databases = [dbs.directory for dbs in neuroConfig.dataPath if not dbs.builtin]
  self.signature['database'].setChoices( *databases )
  
  self.linkParameters('analysis', ('database', 'analysis_name'), self.updateAnalysis)

  self.database = databases[0]

def updateAnalysis(self, proc, dummy):
  if not self.analysis_name in [None, '']:
    d = {}
    d['_database'] = self.database
    d['analysis'] = self.analysis_name
    return self.signature['analysis'].findValue(d)
  
def execution( self, context ):
  #db = databases.database( self.database )
  os.makedirs(self.analysis.fullPath())
  #db.update()