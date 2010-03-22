#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
#
# Author: Tommi Ruuth
#
# dataHandler.py class for fetchin (if with db) and saving data.
#
# if handling data from directory (files) we have to have the file type.
#
# if using db, then this class all is saved. caller must take care data integrity.
#


import dircache
import os.path
import re
import string
import sys

class fileHandler:
  # This class/method os for FILE-listing 
  
  def __init__(self, sourceDirectory, sourceFiles=None):
    # @param: The directry of the source-files
    # This one is mandatory. -> TODO: check the param
    self.sdir = sourceDirectory
    if (sourceFiles==None):
      # No file to read given, so we read ALL from sourceDirectory
      self.sourceFiles = self.listFiles(sourceDirectory)  
    else:
      # TODO: Lets check that file exists
      fil2 = []
      fil2.insert(0, sourceDirectory  + "/" + sourceFiles)
      self.sourceFiles = fil2
    self.bigList =  {}
    cou = 0
    print "sourcefiles -> %s" % sourceFiles

    for sourceFile in self.sourceFiles:
      self.bigList[cou] = self.getDataFromFile(sourceFile)
      print "Debug: one result (",cou,"): ", self.bigList[cou], "\n"
      cou = cou + 1
    

  def getDataFromFile(self, fileToRead):
    # This one reads the file trough. Collect everything from it and
    # returns it as a dict-list for the caller.
    #
    # FIX: Do a check that the file is really a txt-file.
    #x
    print "Debug: file to read -> %s <br> \n \n" % fileToRead
    self.lista = {}
    try:
      filu = open(fileToRead, 'r')
      # Do file-check here, before readeing the content
      
      for livi in filu.readlines() :
	if ( livi[:1] == '#' ) :
	  # Skip comment line
	  continue
	else :
	  # string.strip(livi)
	  livi.strip()
	  # TODO: Remove linebreak...
	  livi+=livi.replace("\n","")
	  # print "DEBUG: line -> -%s- \n" % livi
	  if livi.count('=') > 0:
	    self.sep='='
	  else :
	    self.sep=':'
	  key, value = self.fileLineSeparator(livi, self.sep)
	  print "Debug: key -> %s, values -> %s \n" % (key,value)
	  self.lista[key] = value
      filu.close()
    except IOError, err:
      self.lista[0] = 'Couldnt open datafile %s directory: (%r). <br>\n' % (fileToRead, err)
      # pass
      #print 'Couldnt open datafile %s directory: (%r). <br>\n' % (fileToRead, err)
            

    return self.lista


  def fileLineSeparator(self, dataLine, separator) :
    # Params: one line of the read result.
    # Action: split 
    finimi = ""
    finres = ""
    if dataLine == '' :
      return "problem", "Line is empty"

    # print "DEBUG: line -> \"%s\"" % dataLine
    parts = dataLine.split(separator)
    return parts[0], parts[1]

  def listFiles(self, dirr):
    # Read all the filenames and full paths to a list and returns this
    files2 = []
    if ( os.path.exists(dirr) == 1 ):
      try:
	files1 = dircache.listdir(dirr)
	# TODO: dircache is to be deprecated on ptyhon 2.6, this has to be changed...
	l = len(files1)
	# print "filut: %(1)s , len -> %(2)s <br>" % { '1':snmpfilut1, '2':l }
	if ( len(files1) > 0 ):
	  snmpfilut1 = files1[:] # jotta voidaan muokata listaa
	  for fil in files1:
	    withdir = dirr + '/' + fil
	    files2.insert(files1.index(fil), dirr + '/' + fil)
	else:
	  files2.insert(1, "No files to read at directory %s ." % dirr)
      except IOError, err:
	print 'Couldnt open the file-directory (%r).' % ('dirr',), err
    
    return files2



class dbHandler:
  # This method os for database-listing of data
  # ONLY present as reminder as maybe-to-be-implemented someday
  def __init__(self, dbconfig):
    # We want to have the config data from file (or something)
    print "Just testing"

