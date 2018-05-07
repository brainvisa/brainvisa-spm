# -*- coding: utf-8 -*-
from brainvisa.processes import *
import json

all_available_types = sorted([t.name for t in getAllDiskItemTypes()])
all_available_formats = sorted([t.name for t in getAllFormats()])

userLevel = 0
name = "Manage Subject group"

signature = Signature(
    'group', ReadDiskItem('Subject Group', 'JSON file'),
    'diskitem_type', OpenChoice(),
    'diskitem_format', OpenChoice(),
    'subjects_to_add', ListOf(ReadDiskItem(all_available_types[0], all_available_formats[0])),
    'subjects_to_remove', ListOf(ReadDiskItem(all_available_types[0], all_available_formats[0])),
)


def initialization(self):
    self.setOptional("subjects_to_add", "subjects_to_remove")
    self.signature['diskitem_type'].setChoices(*all_available_types)
    self.signature['diskitem_format'].setChoices(*all_available_formats)

    self.addLink(None, 'diskitem_type', self.updateSignatureAboutTypeAndFormat)
    self.addLink(None, 'diskitem_format', self.updateSignatureAboutTypeAndFormat)

    self.diskitem_type = "4D Volume"
    self.diskitem_format = "NIFTI-1 image"


def updateSignatureAboutTypeAndFormat(self, proc):
    if self.diskitem_type in all_available_types and self.diskitem_format in all_available_formats:
        self.signature["subjects_to_add"] = ListOf(ReadDiskItem(self.diskitem_type, self.diskitem_format))
        self.signature["subjects_to_remove"] = ListOf(ReadDiskItem(self.diskitem_type, self.diskitem_format))
        self.setOptional("subjects_to_add", "subjects_to_remove")
        self.changeSignature(self.signature)
    else:
        pass  # OpenChoice causes problems during writing


def execution(self, context):
    f = open(self.group.fullPath(), 'r')
    data = json.load(f)
    f.close()

    first_subject_dict = data["group_list"][0]
    attr_needed = first_subject_dict.keys()

    if self.subjects_to_remove:
        data = self.removeOldSubjects(context, data, attr_needed)

    if self.subjects_to_add:
        data = self.addNewSubjects(context, data, attr_needed)

    f = open(self.group.fullPath(), 'w')
    data = json.dump(data, f, indent=1)
    f.close()


def removeOldSubjects(self, context, data, attr_needed):
    for diskitem in self.subjects_to_remove:
        diskitem_attr = diskitem.hierarchyAttributes()
        subject_dict = {}
        for attr in attr_needed:
            try:
                subject_dict[attr] = diskitem_attr[attr]
            except KeyError, e:
                context.error("subject has not all needed attributes")
                raise KeyError(e)
            except Exception as e:
                context.error(e)
        try:
            data["group_list"].remove(subject_dict)
        except ValueError, e:
            context.error("old subject not found")
        except Exception as e:
            context.error(e)

        return data


def addNewSubjects(self, context, data, attr_needed):
    for diskitem in self.subjects_to_add:
        diskitem_attr = diskitem.hierarchyAttributes()
        subject_dict = {}
        for attr in attr_needed:
            try:
                subject_dict[attr] = diskitem_attr[attr]
            except KeyError, e:
                context.error("subject has not all needed attributes")
                raise KeyError(e)
            except Exception as e:
                context.error(e)

        if not subject_dict in data["group_list"]:
            data["group_list"].append(subject_dict)
        else:
            context.warning("New subject already exist in group")

        return data
