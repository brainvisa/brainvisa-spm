## -*- coding: utf-8 -*-
##  This software and supporting documentation are distributed by
##      Institut Federatif de Recherche 49
##      CEA/NeuroSpin, Batiment 145,
##      91191 Gif-sur-Yvette cedex
##      France
##
## This software is governed by the CeCILL license version 2 under
## French law and abiding by the rules of distribution of free software.
## You can  use, modify and/or redistribute the software under the
## terms of the CeCILL license version 2 as circulated by CEA, CNRS
## and INRIA at the following URL "http://www.cecill.info".
##
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software"s author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability.
##
## In this respect, the user"s attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software"s suitability as regards their
## requirements in conditions enabling the security of their systems and/or
## data to be ensured and,  more generally, to use and operate it in the
## same conditions as regards security.
##
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license version 2 and that you accept its terms.

from brainvisa.processes import *
from brainvisa.processing.qt4gui.neuroProcessesGUI import mainThreadActions
from soma import aims
import os

userLevel = 0
name = "Identify and label vois extracted from result report SPM12"

def validation():
    from nuclearImaging.LabelNameSetting import LabelNameSetting
from nuclearImaging.LabelNameSetting import LabelNameSetting
#------------------------------------------------------------------------------

signature = Signature(
    'results_report_mat_file', ReadDiskItem('Matlab SPM file', 'Matlab file'),
    'write_filtered_images', Choice(('Thresholded SPM', 'thresh'),
                                    ('All clusters (binary)', 'binary'),
                                    ('All clusters (n-ary)', 'n-ary')),
    'write_filtered_images_basename', String(),
    'size_of_seeds', Integer(),
    'anat_template' ,ReadDiskItem('anatomical Template', ['NIFTI-1 image', 'SPM image', 'MINC image']),
    "atlas_label_mask", ListOf(ReadDiskItem( "atlas label volume", "NIFTI-1 image")),
    "atlas_label_translation",  ListOf(ReadDiskItem( "atlas label volume translation", "JSON file")),
)

#------------------------------------------------------------------------------

def initialization(self):
  self.setOptional("atlas_label_mask","atlas_label_translation")
  self.linkParameters( "atlas_label_translation", "atlas_label_mask" )

  self.write_filtered_images_basename = "filtered_images"
  self.size_of_seeds = 10

def execution( self, context ):
    volumes_path_list = self.findVolumes()
    for volume_path in volumes_path_list:
        if self.write_filtered_images == "thresh":
            volume_bin = context.temporary( "NIFTI-1 image" ).fullPath()
            command = ["AimsThreshold",
                       "-i", volume_path,
                       "-m", "gt",
                       "-t", '0',
                       "-o", volume_bin,
                       "-b", '1',
                      ]
            context.system( *command )
            volume_bin_labelled = context.temporary( "NIFTI-1 image" ).fullPath()
            command = ["AimsConnectComp",
                       "-i", volume_bin,
                       "-s", "%s" % self.size_of_seeds,
                       "-o", volume_bin_labelled,
                      ]
            context.system( *command )
        elif self.write_filtered_images == "binary":
            volume_bin_labelled = context.temporary( "NIFTI-1 image" ).fullPath()
            command = ["AimsConnectComp",
                       "-i", volume_path,
                       "-s", "%s" % self.size_of_seeds,
                       "-o", volume_bin_labelled,
                      ]
            context.system( *command )
        else:
            volume_bin_labelled = volume_path

        tmp_graph = context.temporary( "Graph" )
        command = ["AimsClusterArg",
                   "-i", volume_bin_labelled,
                   "-o", tmp_graph.fullPath()
                  ]
        context.system( *command )

        list_index = self.findAllLabelIndex(volume_bin_labelled )
        list_int_index = map( int, list_index )
        list_int_index.remove(0)

        attr = self.results_report_mat_file.hierarchyAttributes()
        attr.update(self.extractAttrFromPath(volume_path))
        output_label_volume = WriteDiskItem("SPM labelled filtered image", "NIFTI-1 image").findValue(attr)
        output_label_volume_translation = WriteDiskItem("SPM labelled filtered image translation", "JSON file").findValue(attr)

        filename = os.path.basename(volume_path).split('.')[0]
        mainThreadActions().call(self.showInterface,
                                 context,
                                 tmp_graph.fullPath(),
                                 list_int_index,
                                 output_label_volume_translation.fullPath(),
                                 filename)
        try: 
            self.createLabelFromGraph( tmp_graph.fullPath(), output_label_volume.fullPath() )
        except:
            context.error("Extraction label failed, graph may be empty?")
            
def findVolumes(self):
    workspace_directory = os.path.dirname(self.results_report_mat_file.fullPath())
    filenames_in_directory = os.listdir(workspace_directory)
    volumes_path_list = []
    for filename in filenames_in_directory:
        if filename.endswith("%s.nii" % self.write_filtered_images_basename):
            volumes_path_list.append(os.path.join(workspace_directory, filename))
    return volumes_path_list

def extractAttrFromPath(self, path):
    basename = os.path.basename(path)
    basename = basename.replace("spm", '')
    basename_splitted = basename.split('_')
    return {"contrast_type":basename_splitted[0],
            "contrast_index":basename_splitted[1],
            "basename":self.write_filtered_images_basename}

def findAllLabelIndex( self, roi_path ):
  roi_aims = aims.read( roi_path )
  ndarray = roi_aims.arraydata()
  label_index = []
  for array in ndarray[0]:
    for row in array:
      label_index += list( set( row ) )
      label_index = list( set( label_index ) )
  return label_index

def showInterface( self, context, tmp_graph_path, list_index, output_dict_path, voi_name  ):
  translate_dict = loadTranslateDict(output_dict_path)
  if self.atlas_label_mask and self.atlas_label_translation and len(self.atlas_label_mask) == len(self.atlas_label_translation):
    atlas_dict = {}
    for atlas_volume_diskitem, atlas_translation_diskitem in zip(self.atlas_label_mask, self.atlas_label_translation):
      if atlas_volume_diskitem.hierarchyAttributes()["atlas"] == atlas_translation_diskitem.hierarchyAttributes()["atlas"]:
        atlas_label_name = atlas_volume_diskitem.hierarchyAttributes()["atlas"]
        atlas_translate_dict = loadTranslateDict(atlas_translation_diskitem.fullPath())
        atlas_dict[atlas_label_name] = {"atlas_path":atlas_volume_diskitem.fullPath() ,
                                        "atlas_translate_dict":atlas_translate_dict}
      else:
        raise Exception("Wrong Atlas pair, name are different")

    interface = LabelNameSetting(self.anat_template.fullPath(),
                                 tmp_graph_path,
                                 voi_name,
                                 list_index,
                                 output_dict_path,
                                 translate_dict,
                                 atlas_dict
                                )
  else:
    interface = LabelNameSetting( self.anat_template.fullPath(),
                                 tmp_graph_path,
                                 voi_name,
                                 list_index,
                                 output_dict_path,
                                 translate_dict)

  interface.show()
  r = interface.exec_()
  return r

def createLabelFromGraph( self, graph_path, label_path ):
  graph = aims.read( graph_path )
  for vertex in graph.vertices():
    vertex[ "bucket_label" ] = int( vertex[ "name" ] )
    vertex[ "Tmtktri_label" ] = int( vertex[ "name" ] )
  aims.GraphManip.buckets2Volume( graph )

  atts = [ x for x in graph.keys() \
    if isinstance( graph[x], aims.rc_ptr_AimsData_S16 ) ]
  if len( atts ) == 0:
    raise RuntimeError( _t_( "the ROI graph contains no voxel data" ) )
  elif len( atts ) > 1:
    raise RuntimeError( _t_( "the ROI graph contains several volumes. " \
      + "Select the extract_volume parameter as one in " ) + "( " \
      + ", ".join( atts ) + " )" )
  else:
    vol = graph[ atts[0] ]
  # handle bounding box which may have cropped the data
  bmin = graph[ "boundingbox_min" ]
  bmax = graph[ "boundingbox_max" ]
  if bmin[:3] != [ 0, 0, 0 ] \
    or bmax[:3] != [ vol.dimX(), vol.dimY(), vol.dimZ() ]:
    # needs expanding in a bigger volume
    vol2 = aims.Volume_S16( bmax[0]+1, bmax[1]+1, bmax[2]+1 )
    vol2.fill(-1)
    ar = vol2.arraydata()
    ar[ :, bmin[2]:bmax[2]+1, bmin[1]:bmax[1]+1, bmin[0]:bmax[0]+1 ] \
      = vol.volume().arraydata()

    for x,y in vol.header().items():
      vol2.header()[ x ] = y
    # add 1 to all voxels because the background is -1
#    vol2 += 1
    aims.write( vol2, label_path )
  else:
    # bounding box OK
    # add 1 to all voxels because the background is -1
    vol += 1
    aims.write( vol.get(), label_path )

def loadTranslateDict(translate_dict_path):
  if os.path.exists(translate_dict_path):
    translate_dict_file = open(translate_dict_path, "r")
    translate_dict = json.load(translate_dict_file)
    translate_dict_file.close()
    return translate_dict
  else:
    return {}