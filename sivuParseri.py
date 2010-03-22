#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Original class author: Petteri Klemola
# Used, modified and published with permission for this use by Tommi Ruuth.
#
# Author: Tommi Ruuth
#

import sys
import datetime
import random
import struct
import dircache
import os.path
import re

# Maybe we need these too?
import pickle
# import cgi

# not needed here, form are handled on index-class
# import cgitb; cgitb.enable()
# Omat luokat:
# import dbHandler
# import utils
# SNMP-luokka, joka parseaa snmp-tuloksia
import snmpParseri
import dataHandler

class Render:
   # Luokka joka rakentelee itseään kutsumalla nettisivun

    def __init__(self, url):
        # @params: Base URL for this page
        self.cssPrefix = ""
	# print "Debug:Render:__init__: url -> %s" % url
	self.setBaseUrl(url)
	# Mandatory config information
	prepConfigs()

    def header(self):
        print "Content-Type: text/html \n"
        print "<html>"
        print "<head>"
        print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-15\" />"
        print "<meta name=\"Authors\" content=\"Tommi Ruuth, Petteri Klemola\" />"
        print "<link rel=\"stylesheet\" href=\"%s/pelit.css\" type=\"text/css\">" % self.getContextRoot()
        print "</head>"
        print "<body>"
        self.cssEnd()
        self.cssStart('sisalto')

    def footer(self):
        self.cssEnd()
	bsu = self.url(self.getBaseUrl(),'Frontpage')
	bso = self.inUrl('kone', 'All machines')
	bsi = self.inUrl('config', 'Handle machines')
	self.cssClass('%(1)s | %(2)s | %(3)s <br> Maintainer: enska AT medusapistetutkapistefi' % {'1':bsu, '2':bso, '3':bsi}, 'footer')
	# self.cssClass('Maintainer: enskaätmedusapistetutkapistefi | %s' % self.url('testi','Footer part'), 'footer')
        print "</body>"
        print "</html>"

    def cssClass(self,text,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"+self.formatText(text)+"</div>"

    def cssStart(self,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"

    def cssEnd(self):
        print "</div>"

    def tableStart(self):
	 print "<table border=\"0\" >"

    def tableEnd(self):
        print "</table>"

    def tableRowStart(self):
	 print "<tr>"

    def tableRowEnd(self):
	 print "</tr>"

    def tableCellStart(self):
	 print "<td>"

    def tableCellEnd(self):
	 print "</td>"

    def addTableRow(self, descr, cont):
	 self.tableRowStart()
	 self.tableCellStart()
	 print descr
	 self.tableCellEnd()
	 self.tableCellStart()
	 print cont
	 self.tableCellEnd()
	 self.tableRowEnd()

    def addListToTableRow(self, itemList):
      self.tableRowStart()
      lislen = 10
      if ( len(itemList) < lislen ):
	 for co in (itemList):
	    self.tableCellStart()
	    print co
	    self.tableCellEnd()
      else:
	 self.tableCellStart()
	 print "Ups, too long list of data, will not add it to the table here... (max. length %s )" % lislen
	 self.tableCellEnd()
      self.tableRowEnd()

    def tableSStart(self):
        print "</div>"

    def tableSEnd(self):
        print "</div>"

    def lB(self):
        print "<br />"

    def bStart(self):
        print "<b>"

    def bEnd(self):
        print "</b>"

    def objDiv(self):
        print " : "

    def formatText(self, text):
        text = str(text)
        return text.replace('\r\n','<br />')

    def setBaseUrl(self, bu):
	# @params: (str) URL
	# @return: none
	self.setContextRoot(bu)
	self.baseUrl = '%s' % bu

    def getBaseUrl(self):
	# @params: None
	# @return: (str) baseUrl
	return self.baseUrl

    def setContextRoot(self,bu):
        # sets contextRoot (no index-file on that path)
	cr = bu
	if (cr.endswith("index.py")):
	      cr = cr.rstrip('index.py')
	      cr = cr.rstrip("/")
	self.contextRoot = '%s' % cr

    def getContextRoot(self):
        # returns contextroot
	# @params: None
	# @return: (str) contextRoot
	return self.contextRoot


    def inUrl(self, url, text=None):
	# @params: URL, alias for it
        return self.url(self.baseUrl+"/"+url, text)

    def url(self, url, text=None):
        if text is None:
            text = url
        return "<a href=\"%(url)s\">%(text)s</a>" % {'url':url,'text':text}

class doBasicPage(Render) :

   def __init__(self, jep):
      # Set basics for the page
      Render.__init__(self, jep)

   def doPage(self) :
      self.header()
      self.cssClass('To-be-named-better-project | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p>Welcome to a to-be-named-better-project's frontpage. <br><br>This project intends to produce a small sys admin tool. Idea of the tool is to collect server/switch/snmp-enabled machine data and show it as nice web-page. The collecting of data is done with snmp-protocol and this is the only method that is supported.</p>"
      self.cssClass('Machine list page | %s ' % self.inUrl('kone', 'All the machines'), 'tilasto')
      self.cssClass('Test underpage | %s ' % self.inUrl('config', 'Config / settings'), 'tilasto')
      self.footer()

class prepConfigs(Render) :
   def __init__(self):
      # Read configurations from config-file. 
      # This file and its directory are fixed to here
      
      # NOTE: relative path
      self.confDir='etc'

      # Lets check that directory exists
      if ( os.path.exists(self.confDir)):
	# Read files, create list of filenames
	self.confFile = dataHandler.fileHandler(self.confDir, 'sai.cfg')
      else:
	# ERROR, this dir doesnt exist, create error message to be returned
	errmsg = ["ERROR: Directory ("+self.confDir+") doesnt exist..."] 
	self.confFile = errmsg
	
	
   def getAllConf(self):

      
      # Ok. Lets return what ever we got...
      return self.confFile



class prepData(Render) :
  # NOTE: This one will be moved to dataHandler.py class

   def __init__(self, ds):
      # Prepare data for use
      # Lets check that directory exists
      if ( os.path.exists(ds)):
	# Read files, create list of filenames
	self.resFiles = self.listFiles(ds)
      else:
	# ERROR, this dir doesnt exist, create error message to be returned
	errmsg = ["ERROR: Directory ("+ds+") doesnt exist..."] 
	self.resFiles = errmsg

   def listConfigData(self):
      # Read all the files for manipulating

      #resConfigList = jokuluokka.Parser(self.resFiles)
      return resList

   def listData(self):
      # Read all the files for manipulating
      # resFiles = self.listFiles(ds)
      resList = snmpParseri.Parser(self.resFiles)
      return resList

   def getFilesList(self):
      # return datalist
      return self.resFiles

   def listFiles(self, dirr):
      # Read all the filenames and full paths to a list and returns this
      snmpfilut2 = []
      if ( os.path.exists(dirr) == 1 ):
	 try:
	    snmpfilut1 = dircache.listdir(dirr)
	    # TODO: dircache is to be deprecated on ptyhon 2.6, this has to be changed...
	    l = len(snmpfilut1)
	    # print "filut: %(1)s , len -> %(2)s <br>" % { '1':snmpfilut1, '2':l }
	    if ( len(snmpfilut1) > 0 ):
	       snmpfilut1 = snmpfilut1[:] # jotta voidaan muokata listaa
	       for fil in snmpfilut1:
		  withdir = dirr + '/' + fil
		  snmpfilut2.insert(snmpfilut1.index(fil), dirr + '/' + fil)
	    else:
	       snmpfilut2.insert(1, "No files to read at directory %s ." % dirr)
	 except IOError, err:
	    print 'Couldnt open the file-directory (%r).' % ('dirr',), err

      return snmpfilut2


class saveData(Render) :
  # NOTE: This one will be moved to dataHandler.py class

   def __init__(self, ds):
      # Save data on the directory which is given as paremeter
      # Read files, create lists, then save or update file
      self.workDir = ds
      # Lets check that directory exists
      if ( os.path.exists(self.workDir)):
	# Yep, get files if there are any
	self.oldFilesList = prepData(self.workDir)
      else:
	# ERROR, this dir doesnt exist, print to screen
	print "ERROR: Directory (%s) doesnt exist (check your configs). " % self.workDir

   def listConfigData(self):
      # Read all the files for manipulating
      return resList

   def getConfigFiles(self):
      return oldFilesList

   def saveDataToFile(self, filesDir, values):
   # def saveDataToFile(self, oldFiles, values):
      # Normal command to save data. Check is it new or old.
      
      # Old way
      # oldFiles = self.oldFilesList
      
      self.filesDir = filesDir
      self.values = values
      workDir = self.workDir
      # gl = re.compile('$(values['name']).conf')
      gl = re.compile(values['name'])
      print "Debug: saveDataToFile: saving data (%s)" % values['name']
      # if ( len(filesDir) > 0 ):
      for kl in (filesDir):
	if ( gl.match(kl) ):
	  # Old value, update file (name is used for the filename)
	  print "lala, this file (%s) needs updating..." % kl
	else:
	  # new file, save it
	  # resFile = open(values["name"], "w")
	  resFile = open(os.path.join(filesDir, 'serverconfig-%s.conf' % values['name']), 'wb')
	  for lk in (values):
	    val = "%s:%s\n" % (lk, values[lk])
	    resFile.write(val)
	  resFile.close()


class tester(Render):
   def __init__(self):
      print "jaja"

   def retS(self, st):
      return st


class doServerPage(Render) :

   def __init__(self, URL):
      Render.__init__(self, URL)
      self.ds = prepData("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      self.bigList = snmpParseri.Parser(self.ds.getFilesList())

   def doPage(self, mach):
      #@params: name of server or instance
      #@return: None
      if (mach[0]):
	 server = mach[0]
      else:
	Error(self.getBaseUrl())

      self.header()
      self.cssClass('Header for this page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p> This is the server-info page for one server. You should be able to see all the information as a table on below. </p>"
      self.bStart()
      print "%s" % server
      self.bEnd()
      self.addAllServerInfo(self, server)
      self.cssClass('Test underpage | %s ' %self.inUrl('kone', 'Kaikki koneet'), 'tilasto')
      self.footer()

   def addAllServerInfo(self, lis, name):
      # Called with the name the LIST and index of the machine we want to see on page
      machineList = self.bigList
      target = name
      ind = machineList.machineIdInd(name)
      # Check the ind
      if ind < 0 :
	 # Error(self.getBaseUrl())
	 # self.cssClass('Error %s ' %self.inUrl('error', 'Error'), 'tilasto')
	 Error("ei suju").doPage("addAllServerInfo")
      else :
	 self.cssStart('tilasto')
	 self.lB()
	 self.tableStart()
	 self.addTableRow("Machine location:", machineList.machineLocationInd(ind) )
	 self.addTableRow("Machine contact:", machineList.machineContactInd(ind) )
	 nlh = {}
	 nlh = machineList.machineNetworkInd(ind)
	 for e in (nlh) :
	    self.addTableRow("Network adapter %s :" %e, nlh[e])
	 self.addTableRow("Memory:", machineList.machineMemoryInd(ind) )
	 self.addTableRow("System date:", machineList.machineSystemDateInd(ind) )
	 self.addTableRow("Uptime:", machineList.machineUptimeInd(ind) )
	 self.tableEnd()

class doMachineList(Render) :
   # This class/method creates a page, which we show to user.

   def __init__(self, koneet):
      # Basic init-method. This is used on creation.
      Render.__init__(self, koneet)

      # joku = tester()
      # print joku.retS("testiiii")
      # Read all the files for manipulating
      self.ds = prepData("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")

      # Create one big hash-list of machineinformation
      self.bigList = snmpParseri.Parser(self.ds.getFilesList())
      # This is the way to call object-lists...

   def doPage(self, jotain):
      # kojeet = self.dataFiles
      kojeet = self.ds.getFilesList()
      bigList = self.bigList
      self.header()
      self.cssClass('Machine / workstation / switch list | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      self.cssStart('sisalto')

      print "<p> All the machines we have got information about. </p>"

      cou = 0
      allmac = len(kojeet)
      contlist = []
      self.tableStart()
      self.tableRowStart()
      self.tableCellStart()
      print "Index"
      self.tableCellEnd()
      self.tableCellStart()
      print "Server name"
      self.tableCellEnd()
      self.tableRowEnd()
      for i in kojeet:
	 self.tableRowStart()
	 self.tableCellStart()
	 print cou + 1
	 self.tableCellEnd()
	 self.tableCellStart()
	 self.bStart()
	 mac = bigList.machineNameInd(cou)
	 print "%s" % self.inUrl("server/" + mac, mac)
	 self.bEnd()
	 # print "(machine no:", cou+1 ,")"
	 self.tableCellEnd()
	 self.tableRowEnd()
	 cou = cou + 1
      self.tableEnd()
      self.cssEnd()
      self.footer()

   def addName(self, machineName):
      print "<b>", machineName, "</b>"

   def addBasicInfo(self, machineList, ind):
      # Called with the name the LIST and index of the machine we want to see on page
      self.cssStart('tilasto')
      self.lB()
      print machineList.machineLocationInd(ind)
      self.lB()
      print machineList.machineContactInd(ind)
      self.lB()

class doConfigPage(Render) :

   def __init__(self, jep):
      Render.__init__(self, jep)
      self.ds = prepData("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      self.confFiles = prepData("mach_confs")
      # Create one big hash-list of machineinformation
      self.bigList = snmpParseri.Parser(self.ds.getFilesList())


   def doPage(self, something) :

      self.header()
      self.cssClass('Config-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')

      kojeet = self.ds.getFilesList()
      bigList = self.bigList
      cofiles = self.confFiles.getFilesList()
      confData = dataHandler.fileHandler("mach_confs")
      # print "confs -> %s" % cofiles
      for j in cofiles:
	print "confs -> %s <br>" % j

      print "data -> %s" % confData

      #for j in confData:
	#print "data -> %s <br>" % j

      cou = 0
      allmac = len(kojeet)
      contlist = []

      print "<form name=\"input\" action=\"%s\" method=\"post\">" % (self.baseUrl+"/update")
      print "Machine: <input type=\"text\" name=\"server\"/>"

      self.tableStart()

      # TODO: Instead of machines results, we want to use the info from server-configs.
      # THe new way. MiddleOfProgress
      machlist = ["Number", "Server name", "Select one"]
      self.addListToTableRow(machlist)
      #for i in cofiles:
	 #machlist[0] = cou + 1
	 #mac = bigList.machineNameInd(cou)
	 #machlist[1] = "<b> %s </b>" % self.inUrl("server/" + mac, mac)
	 ##machlist[2] = "<input type=\"radio\" name=\"mac\" value=\"mac\" />"
	 #self.addListToTableRow(machlist)
	 #cou = cou + 1
      print "<br> tadaa <br>"
      
      #
      # The old way
      machlist = ["Number", "Server name", "Select one"]
      self.addListToTableRow(machlist)
      for i in kojeet:
	 machlist[0] = cou + 1
	 mac = bigList.machineNameInd(cou)
	 machlist[1] = "<b> %s </b>" % self.inUrl("server/" + mac, mac)
	 machlist[2] = "<input type=\"radio\" name=\"mac\" value=\"mac\" />"
	 self.addListToTableRow(machlist)
	 cou = cou + 1
      self.tableEnd()
      # print "</input >"

      print "<input type=\"submit\" value=\"Modify\"/>";
      print "</form>"

      # testing the form page
      self.addMachineInfoForm("testi")

      self.footer()

   def addMachineInfoForm(self, mach):

      self.eds = prepData("/var/www/tommi/data")
      self.lili = self.eds.getFilesList()
      print "Machine config-files: <br>"
      for lin in self.lili:
	 print "%s <br> \n" % lin

      self.namelist = ['name', 'ip', 'dns', 'snmpver', 'snmpcomm', '1', '2', 'user', 'passu']

      self.emplist = {}
      self.emplist[self.namelist[0]] = "Describing name of the machine."
      self.emplist[self.namelist[1]] = "IP"
      self.emplist[self.namelist[2]] = "DNS name of the machine."
      self.emplist[self.namelist[3]] = "Version of snmp (v2 only)."
      self.emplist[self.namelist[4]] = "Snmp community pharse."
      self.emplist[self.namelist[5]] = "tba"
      self.emplist[self.namelist[6]] = "tba"
      self.emplist[self.namelist[7]] = "Your username for this page"
      self.emplist[self.namelist[8]] = "Your password to save data"

      # testing the function, to see that the form works and saves dataFiles
      # TODO: move the editing page on its own, either with old data or to have new data
      self.doMachineForm(self.emplist)
      # emplist["name", "ip", "phar", "snmpver"] = "koneen nimi", "koneen ip", "jotain", "jossain"
      # print "list %s::%s" % (emplist.get("name", "nooooooo"), emplist.get("ip", "nooooooo"))
      if (mach == "uusi") :
	 # This is a new machine, no data to fetch
	 print "New data..."
	 #print "list %s" % emplist
	 self.doMachineForm(emplist)

      else:
	 # This is an old machine, fetch data and show it to the user
	 self.lB()
	 print "Old data..."


   def doMachineForm(self, datalist):
      # Create form with the data we received
      # maybe this could be done with javascript or similar?
      dsli = datalist
      namelist = self.namelist
      self.lB()
      target = (self.baseUrl+"/savedata")
      # For testing, there is additional python class
      # target = "http://localhost/tommi/formHandler.py"
      print "<p>Give information for the new machine. This is send to %s </p>"  % target
      print "<form name=\"id=newdata\" action=\"%s\" method=\"post\">" % target
      self.tableStart()
      for nametin in (namelist):
	 self.a = [0,1,2]
	 self.a[0] = "%s :" % nametin
	 self.a[1] = "<input type=\"text\" name=\"%(1)s\" value=\"test-%(1)s\" />" % { '1':nametin }
	 self.a[2] = "%(2)s" % { '2':dsli.get(nametin, "Errrr") }
	 self.addListToTableRow(self.a)

      self.tableEnd()
      self.lB()
      self.lB()

      print "<input type=\"submit\" value=\"Save data\"/>";
      print "<input type=\"reset\" value=\"Cancel (clear data)\"/>";
      print "</form>"


class doSaveDataPage(Render) :

   def __init__(self, URL, dataFromForm):
      Render.__init__(self, URL)
      self.filledForm = dataFromForm
      self.valuesList = {}
      self.oldFiles = prepData("data")

      # print "Content-Type: text/html \n"
      # print "Deb: %s <br> \n" % dataFromForm


   def doPage(self, data):
      # TODO: handle data
      values = self.valuesList
      formData = self.filledForm
      oldFiles = self.oldFiles
      filesDir = 'mach_conf'
      self.resultFile = ''
      self.blaah = saveData("data")

      self.header()
      self.cssClass('Reply-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p>Data save has been tried, see results below.</p>"
      
      values['debug'] = 1 # Set to 0 to have dummy data
      values['hasData'] = 1 # Set to 1, we dont know if there is any data
      values['user'] = ""
      values['passu'] = ""
      values['name'] = ""
      values['ip'] = ""
      values['dns'] = ""
      values['snmpver'] = ""
      values['snmpcomm'] = ""
      values['1'] = ""
      values['2'] = ""
      # print "Debug: list: %s <br> \n" % formData

      if ( len(formData) > 0 ):
	 values['hasData'] = 0
	 for valname in (values):
	    # tt1 = formData.getfirst(valname, "ERR: got nothing from html-form")
	    # print "debug: form: getfirst: (name) %s -> (value) %s \n <br>" % (valname, tt1)
	    filledList = formData.getlist(valname)
	    for pl in (filledList):
	       if ( values[valname] == "" ):
		  values[valname] = pl
		  # print "Debug: values for-loop: %s <br><br> \n" % pl
	       else:
		  values[valname + pl] = pl

      else:
	 values['hasData'] = 1 # Set to 1, NO data
	 # print "ERROR: No html-form data reveived... <br> \n"

      if ( values['debug'] == 0 ):
	values['hasData'] = 0 # Set to 0, we want see some data for debug reasons
	values['user'] = "a1"
	values['passu'] = "a2"
	values['name'] = "a3"
	values['ip'] = "a4"
	values['dns'] = "a5"
	values['snmpver'] = "a6"
	values['snmpcomm'] = "a7"
	values['1'] = "a8"
	values['2'] = "a9"

      if (values['hasData'] == 0):
	 print "<p>Data from FORM to be saved. <br> \n"

	 # Check if it was old config (from the filename (not the best way...))
	 # succ = self.blaah.saveDataToFile(oldFiles, values)
	 succ = self.blaah.saveDataToFile(filesDir, values)
	 # resFile = open(values["name"], "w")
	 
	 # Working way
	 # resultFile = open(os.path.join('etc', 'filu1-%s' % values['name']), 'wb')
	 # for lk in (values):
	    # print " %s -> %s  <br> \n" % (lk, values[lk])
	    # val = "%s : %s \n" % (lk, values[lk])
	    # resultFile.write(val)
	
	 # resultFile.close()
	    
	    # Example code
	    # commentfile = open(os.path.join(indexdir,'comment-%s' % filename), 'wb')
	    # pickle.dump(comments, commentfile)
	    # commentfile.close()

	 print "</p>"

      else:
	 print "<p>ERROR: No data received from form... Nothing to save. </p> \n"


      self.footer()


class doDebugPage(Render) :

   def __init__(self, URL, messa):
      Render.__init__(self, URL)
      #mes = self.messa
      # self.ds = prepData("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      # self.bigList = snmpParseri.Parser(self.ds.getFilesList())

   def doPage(self, URL, messa):
      #@params: name of server or instance
      #@return: None
      self.header()
      self.cssClass('DEBUG-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p> This is Debug page. <br> It is shown because it is uncommented from the index-page.</p>"
      self.bStart()
      print "<p>"
      print "Debug context-root: "
      self.lB()
      print "%s" % self.getContextRoot()
      self.lB()
      self.lB()
      print "Debug URL: "
      self.lB()
      print "%s" % URL
      self.lB()
      self.lB()
      print "Debug message:"
      self.lB()
      print "%s" % messa
      print "</p>"
      self.bEnd()
      self.lB()
      self.footer()


class Error(Render):
   def __init__(self, text):
      self.text = text
      Render.__init__(self, text)
      self.prefix = [
            'Ongelmia jäsennyksessä',
            'Kärpänen',
            'Järjestelmä huumeessa',
            'Suoritus kohtasi seuraavan virhetilanteen',
            'Fehler',
            'Kone on tätä mieltä',
            'Saisit puolestani jatkaa, mutta',
            ]

   def doPage(self, message):
      self.header()
      self.cssClass("%s -> " % message, 'testi')
      # self.cssClass("%s -> <b>%s:</b> %s" % message, (random.choice(self.prefix), self.text), 'virhe')
      self.footer()
