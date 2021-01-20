# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from brainvisa.processes import *
import json

userLevel = 0
name = 'Measure the offset from SPM realign'


signature = Signature(
    "spm_version", Choice("spm8", "spm12"),
    "realign_parameters",
        ReadDiskItem("PET dynamic SPM realign results", "Text file"),
    "box_size", ListOf(Integer()),
    "acquisition_data",
        WriteDiskItem("Any Type", "JSON file"),
)


def initialization(self):
    self.box_size = [50, 50, 50]


def execution(self, context):
    realign_offset_dict = {}
    f = open(self.realign_parameters.fullPath(), 'r')
    first_line = f.readline()
    if first_line:
        index = 0
        first_transfo = self.buildAimsTransfo(first_line)
        for line in f.readlines():
            index += 1
            transfo = self.buildAimsTransfo(line)
            print(transfo)
            offset = self.extractOffsetBetweenTwoTransformations(first_transfo, transfo)
            realign_offset_dict["t0 to t%i" % index] = offset
            context.write("Mean offset between t0 and t%i : <b>%s mm</b>" % (index, offset))
    else:
        context.warning("no SPM transformation found")

    if realign_offset_dict:
        f = open(self.acquisition_data.fullPath(), 'r')
        data = json.load(f)
        f.close()
    
        offset_dict_key = "dynamic offset (mm)"
        spm_version_dict_key = "%s realign" % self.spm_version
        if offset_dict_key in data:
            if spm_version_dict_key in data[offset_dict_key]:
                data[offset_dict_key][spm_version_dict_key][str(self.box_size)] = realign_offset_dict
            else:
                data[offset_dict_key][spm_version_dict_key] = {str(self.box_size): realign_offset_dict}
        else:
            data[offset_dict_key] = {spm_version_dict_key: {str(self.box_size): realign_offset_dict}}
    
        f = open(self.acquisition_data.fullPath(), 'w')
        json.dump(data, f, indent=2, sort_keys=True)
        f.close()


def buildAimsTransfo(self, spm_line):
    transfo_str_list = spm_line.split()
    if len(transfo_str_list) != 6:
        raise ValueError("Transformations in text file must have 6 parameters")
    else:
        transfo_float_list = [float(transfo_str) for transfo_str in transfo_str_list]
        trm_t = aims.AffineTransformation3d()
        trm_t.setTranslation([transfo_float_list[0],
                            transfo_float_list[1],
                            transfo_float_list[2]])
        trm_r = aims.AffineTransformation3d()
        trm_r.setRotationAffine(transfo_float_list[3],
                              transfo_float_list[4],
                              transfo_float_list[5])
        return trm_t * trm_r


def extractOffsetBetweenTwoTransformations(self, first_transfo, second_transfo):
    coord_list = [[0, 0, 0],
                  [0, 0, self.box_size[2]],
                  [0, self.box_size[1], 0],
                  [self.box_size[0], 0, 0],
                  [self.box_size[0], 0, self.box_size[2]],
                  [self.box_size[0], self.box_size[1], 0],
                  [0, self.box_size[1], self.box_size[2]],
                  [self.box_size[0], self.box_size[1], self.box_size[2]],
                  [self.box_size[0]//2, self.box_size[1]//2, self.box_size[2]//2],
                 ]
    norm_sum = 0
    for coord in coord_list:
        norm_sum += (first_transfo.transformPoint3d(coord) - second_transfo.transformPoint3d(coord)).norm()
    return norm_sum/len(coord_list)
