# -*- coding: utf-8 -*-

import six


def checkIfArgumentTypeIsStrOrUnicode(argument_index):
  def decorator(function):
    def checkArgumentType(*args, **kwargs):
      assert isinstance(args[argument_index], six.string_types),\
        "str or unicode allowed but argument %s is %s" % (argument_index, type(args[argument_index]))
      return function(*args, **kwargs)
    return checkArgumentType
  return decorator

def checkIfArgumentIsInAllowedList(allowed_argument_list, argument_index):
  def decorator(function):
    def checkArgumentType(*args, **kwargs):
      assert argument_index in allowed_argument_list,\
             "Unvalid choice : '%s' , only one of them are allowed : %s" % (args[argument_index], allowed_argument_list)
      return function(*args, **kwargs)
    return checkArgumentType
  return decorator

def checkIfArgumentTypeIsAllowed(type_allowed, argument_index):
  def decorator(function):
    def checkArgumentType(*args, **kwargs):
      assert isinstance(args[argument_index], type_allowed),\
             "%s allowed but argument %s is %s" % (type_allowed, argument_index, type(args[argument_index]))
      return function(*args, **kwargs)
    return checkArgumentType
  return decorator

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance
