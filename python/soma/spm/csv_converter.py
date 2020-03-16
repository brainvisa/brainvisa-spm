# -*- coding: utf-8 -*-
from __future__ import print_function

from __future__ import absolute_import
import os
import json
import csv
import copy
from six.moves import range

def convert( const_pydict, output_path, const_key_titles=[""], verbose=False ):
  pydict = copy.deepcopy(const_pydict)
  key_titles = copy.deepcopy(const_key_titles)
  
  pydict, key_titles = separateHeadersAndDatas( pydict, key_titles )
  key_titles = checkPyDictCompliance( pydict, key_titles )

  #If the folder which contains the output file doesn't exist
  #CSV write can't create the folder
  output_dir = output_path[:output_path.rindex('/')]
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  generic_dict = createGenericDict( pydict, {} )
  if verbose:
    print("*****JSON dict representing the generic model *****")
    print(json.dumps( generic_dict, sort_keys=True, indent=4, separators=(',', ': ')))

  #Warning!! if the output file already exists it will be erased
  c = csv.writer(open(output_path, "w"), delimiter=';')
  rows = createRowHeaderList( key_titles, generic_dict, {})
  rows = createRowSeparator( rows )
  for k in sorted(rows.keys()):
    c.writerow( rows[k] )
  subject_rows = createRowDataList( generic_dict, pydict, {} )
  for k in sorted(subject_rows.keys()):
    c.writerow( subject_rows[k] )


def separateHeadersAndDatas( pydict, key_titles ):
  key_titles.append( ' || ' )
  new_dict = {}
  for current_key in pydict.keys():
    new_key = current_key + '; || '
    new_dict[ new_key ] = pydict[ current_key ]
  return new_dict, key_titles

def checkPyDictCompliance( pydict, key_titles ):
  """this method check if all keys contains the good number of words as key_titles"""
  words_number = len( key_titles )
  for key in pydict.keys():
    current_words_number = key.count( ';' ) + 1
    if current_words_number != words_number:
      print('ERROR : number of header words mismatch with key_titles')
      return [ " -- " ] * words_number
  return key_titles

def createGenericDict (  dictionary_list, subtree={} ):
  """dictionary_list could be two different objects:
    (-) list of dictionary, one dictionary per subject
    [Subject01_dict, Subject02_dict, ... ]
    (-) a dictionary which the first keys are the subject names
    {Subject01 : ...,Subject02 : ..., } """

  if not isinstance( dictionary_list, list):
    if  isinstance( dictionary_list, dict):
      dictionary = dictionary_list
      dictionary_list = []
      for subject in dictionary.keys():
        dictionary_list.append(dictionary[subject])
    else:
      print("""ERROR the argument "dictionary_list" has not a good value""")

  children_name_list = []
  #create list with all names available
  for d in dictionary_list:
    children_name_list = list( set( children_name_list + list(d.keys()) ) )
  #create list of subtree which contains the specific node
  for c in children_name_list:
    branch_list = []
    for d in dictionary_list:
      if c in list(d.keys()):
        if isinstance( d[c], dict ):
          branch_list.append( d[c] )

    if len( branch_list ) != 0:
      subtree[c] = {}
      subtree[c] = createGenericDict( branch_list, subtree[c] )
    else:
      subtree[c] = ''

  return subtree


def howMuchLeaves( dict_node, index=0):
  """The purpose of this process is to determine how many Leaves are derived from a node """
  if isinstance(dict_node, dict):
    for k in dict_node.keys():
      if isinstance( dict_node[k], dict ):
        index = howMuchLeaves( dict_node[k], index )
      else:
        index = index + 1
    return index
  else:
    return 0

def createRowHeaderList(  key_titles, generic_dict, rows, index=1, begin_length=0):
  """The purpose of this process is to create the rows of the CSV header,
  one list item corresponding to one cell in csv """
  if not index in list(rows.keys()):
    rows[index] = []
    if index == 1:
      rows[index].extend( key_titles )
    else:
      rows[index].extend( ['  --  '] * ( len( key_titles ) - 1 ) )
      rows[index].append( ' || ' )
  #if the tree has some branch more longuer than others we have to fill the blank
  if len(rows[index]) < begin_length:
    for r in range(begin_length - len(rows[index]) ):
      rows[index].append('  --  ')

  #the keys of python dict is aleatory, so we have to sort
  for k in sorted(generic_dict.keys() ):
    begin_length = len( rows[index] )
    rows[index].append(k)
    num_of_leaves = howMuchLeaves(generic_dict[k])
    for i in range(num_of_leaves-1):
      rows[index].append('  --  ')
    if isinstance(generic_dict[k], dict):
      createRowHeaderList( key_titles, generic_dict[k], rows, index+1,begin_length )

  if index == 1:
    #to verify if the rows have the same length
    length = len( rows[ list(rows.keys())[0] ] )
    for k in rows.keys():
      if len( rows[k] ) < length:
        for r in range(length-len(rows[k])):
          rows[k].append('  --  ')
    return rows

def createRowSeparator( rows ):
  last_row_index = max( rows.keys() )
  rows[ last_row_index + 1 ] = list()
  for item in rows[ last_row_index ]:
    if item == ' || ':
      rows[ last_row_index + 1 ].append( ' # ' )
    else:
      rows[ last_row_index + 1 ].append( ' == ' )
  return rows

def createRowDataList(  generic_dict, pydict, rows ):
  """The purpose of this process is to create one list per subject,
  which contains its data"""
  subject_rows = {}
  for exam_name in  pydict.keys():
    subject_rows[exam_name] = []
    for subject_id_item in exam_name.split(';'):
      subject_rows[exam_name].append(preventAutomaticNumberConversionInCSVReader(subject_id_item))

    subject_dict =  pydict[exam_name]
    subject_rows = IterationOnEachSubject( generic_dict, subject_dict, subject_rows, exam_name )

  return subject_rows

def preventAutomaticNumberConversionInCSVReader(subject_id_item):
  try:
    float(subject_id_item)
    return str( "'" + subject_id_item )
  except:
    return subject_id_item

def IterationOnEachSubject( generic_dict, subject_dict, subject_rows, exam_name):
  """The purpose of this process is to complete the Subject list so that it meets the header fields"""
  for k in sorted( generic_dict.keys() ):
    if k in list(subject_dict.keys()):
      if isinstance(subject_dict[k], dict):
        IterationOnEachSubject(generic_dict[k], subject_dict[k], subject_rows, exam_name)
      else:
        cell_value = convertToNumberIfPossible(subject_dict[k])
        subject_rows[exam_name].append(cell_value)
    else:
      num_of_leaves = howMuchLeaves(generic_dict[k])
      #if num_of_leaves == 0, we have to fill the blank by one '  --  '
      #this case appears when one(several) leaf/(leaves) doesn't exist in one(several) file(s)
      for i in range(num_of_leaves-1):
        subject_rows[exam_name].append('  --  ')
      subject_rows[exam_name].append('  --  ')
  return subject_rows

def convertToNumberIfPossible(cell_value):
  if isinstance(cell_value, str) and cell_value != '':
    cell_value = cell_value.replace(',','.')
    if cell_value.isdigit():
      return int(cell_value)
    elif '-' in cell_value:
      abs_cell_value = cell_value.replace('-','')
      if abs_cell_value.isdigit():
        return int(abs_cell_value) * -1
      else:
        try:
          return float(cell_value)
        except ValueError:
          return "'" + cell_value
    else:
      try:
        return float(cell_value)
      except ValueError:
        return "'" + cell_value
  else:
    return cell_value

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def reverse(path, delimiter=';'):
  """This method aims is to restore python dictionary from the CSV file
  created by convert"""
  pydict = {}

  f = open(path,'r')
  row = {}
  ind = 0
  for line in f:
    if ind == 0:
      tmp_line_splitted = line.split(delimiter)
      if ' || ' in tmp_line_splitted:
        nb_of_word_in_key = tmp_line_splitted.index( ' || ' )
      else:
        nb_of_word_in_key = 1
    line = deleteCharUsingForNewLine(line)
    line = deleteCharUsingAsHeaderSeparator(line)
    line_splitted = line.split(delimiter)
    if set( line_splitted ) != set( [ '' ] ):
      row[ind] = line_splitted
      ind += 1
  del ind

  header_dict = {}
  data_dict = {}
  ind_header = 0
  for key in sorted(row.keys()):
    #the first case of CSV could be anything
    row_name_list = []
    for it in range( nb_of_word_in_key ):
      if not '--' in row[key][0]:
        row_name_list.append( row[key][0] )
      del row[key][0]
    row_name = ';'.join( row_name_list )
    row_name = deleteQuoteFromNumberConversionPrevention(row_name)

    row_data = row[key]

    if key != 0 and row_name and not '--' in row_name:
      data_dict.update( {row_name:row_data} )
    else:
      if key == 0:
        row_keys_list = row_name_list
      header_dict.update( {str(ind_header):row_data} )
      ind_header += 1
  for row_name in data_dict.keys():
    pydict[row_name] = createPyDictBranch( header_dict, data_dict[row_name])

  cleanDict(pydict)

  return pydict, row_keys_list

def deleteCharUsingForNewLine(line):
  line = line.replace('\r','')
  line = line.replace('\n','')
  return line

def deleteCharUsingAsHeaderSeparator(line):
  line = line.replace(' || ;','')
  line = line.replace(' == ','')
  line = line.replace(' # ','')
  return line

def deleteQuoteFromNumberConversionPrevention(row_name):
  return row_name.replace("'","")

def createPyDictBranch( header_dict, data_dict):
  """This method aims is to restore the python dictionary for each row data"""
  branch_dict = {}
  for ind in range(len(data_dict)):
    tmp_list = []
    first_title=False
    for key in list(reversed(sorted(header_dict.keys()))):
      tmp_ind = ind
      if '  --  ' in header_dict[key][ind] and first_title:
        while '  --  ' in header_dict[key][tmp_ind]:
          tmp_ind -= 1
      else:
        first_title=True
      if not '  --  ' in header_dict[key][tmp_ind] :
        tmp_list.append( header_dict[key][tmp_ind] )

    tmp_list.reverse()
    k = tmp_list.pop()
    tmp_dict = {k:data_dict[ind]}
    size_list = len(tmp_list)
    for i in range(size_list):
      k = tmp_list.pop()
      d = {k:tmp_dict}
      tmp_dict = d.copy()

    branch_dict = mergeDict( branch_dict, tmp_dict )

  return branch_dict

def mergeDict( d1, d2, d2_erase_d1=False ):
  """This method allow to merge two python dictionaries
  without erase the deep keys, contrary to classical "update" method"""
  dict_merged = {}
  key_list = []
  key_list.extend( list(d1.keys()) )
  key_list.extend( list(d2.keys()) )
  key_list = list( set( key_list ) )
  for key in key_list:
    if isinstance( key, str ):
      new_key = key.replace( '\n', '' )
    else:
      new_key = key
    if key in list(d1.keys()) and key in list(d2.keys()):
      if isinstance( d1[key], dict ) and isinstance( d2[key], dict ):
        dict_merged[new_key] = mergeDict( d1[key], d2[key], d2_erase_d1 )
      else:
        # If same data are merged, neither d1 value nor d2 value was wrote
        if d2_erase_d1:
          dict_merged[new_key] = d2[key]
        else:
          dict_merged[new_key] = '** data merged **'
    elif key in list(d1.keys()) and not key in list(d2.keys()):
      dict_merged[new_key] = d1[key]
    elif not key in list(d1.keys()) and key in list(d2.keys()):
      dict_merged[new_key] = d2[key]
  return dict_merged

def cleanDict(pydict):
  """This method is used to delete part af python dictionary_list
  if it's empty or only full with '  --  ' or '  --  \n'"""
  for key in pydict.keys():
    if isinstance(pydict[key], dict):
      if pydict[key]:#Testing if pydict[key] is not empty
        cleanDict(pydict[key])
        if not pydict[key]:#Testing if pydict[key] is empty
          del pydict[key]
      else:
        del pydict[key]
    elif '  --  ' in pydict[key]:
      del pydict[key]


