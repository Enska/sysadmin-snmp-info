#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Original class author: Petteri Klemola
# Used, modified and published with permission for this use.
#
# Author: Tommi Ruuth
#

import sys
import datetime
import random
import struct
import dircache
# Omat luokat:
# import dbHandler
# import utils
# SNMP-luokka, joka parseaa snmp-tuloksia
import snmpParseri

class Render:
   # Luokka joka rakentelee itseään kutsumalla nettisivun

    def __init__(self, url):
        # @params: Base URL for this page
        self.cssPrefix = ""
	# print "Debug:Render:__init__: url -> %s" % url
	self.setBaseUrl(url)

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
        # self.cssClass('Maintainer: enskaätmedusapistetutkapistefi | %s' % self.url(self.baseUrl0,'Footer part'), 'footer')
	self.cssClass('Maintainer: enskaätmedusapistetutkapistefi | %s' % self.url(self.getBaseUrl(),'Footer part'), 'footer')
	# self.cssClass('Maintainer: enskaätmedusapistetutkapistefi | %s' % self.url('testi','Footer part'), 'footer')
	print "getBaseUrl: %s" % self.getBaseUrl()
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
        # returns cotextroot
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
      # self.jep = 'http://localhost/tommi/index.py'
      Render.__init__(self, jep)
      # Create basic page

   def doPage(self) :
      self.header()
      self.cssClass('Header for this page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p> sivuParseri.py::teePerusSivu::doPage method test. </p>"
      self.cssClass('Machine list page | %s ' %self.inUrl('kone', 'All the machines'), 'tilasto')
      self.cssClass('Test underpage | %s ' %self.inUrl('config', 'Config / settings'), 'tilasto')
      self.footer()

class prepData(Render) :

   def __init__(self, ds):
      # Prepare data for use
      # Read files, create lists
      self.kojeet = self.listFiles("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      self.resFiles = self.listFiles(ds)

      # Create one big hash-list of machineinformation
      # self.bigList = snmpParseri.Parser(self.kojeet)
      # print "prepData::__init__ tester"

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
      try:
	 snmpfilut1 = dircache.listdir(dirr)
	 snmpfilut1 = snmpfilut1[:]  # jotta voidaan muokata listaa
	 snmpfilut2 = []
	 for fil in snmpfilut1:
	    withdir = dirr + '/' + fil
	    snmpfilut2.insert(snmpfilut1.index(fil), dirr + '/' + fil)
      except IOError, err:
 	 print 'Couldnt open the snmp-results-file-directory (%r).' % ('dirr',), err

      return snmpfilut2

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
	Error("vika")
      self.header()
      print "<p> sivuParseri.py::teeServerSivu::doPage method test. </p>"
      self.bStart()
      print "%s" % server
      self.bEnd()
      self.addAllServerInfo(self, server)
      self.cssClass('Server page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      self.cssClass('Test underpage | %s ' %self.inUrl('kone', 'Kaikki koneet'), 'tilasto')
      self.footer()

   def addAllServerInfo(self, lis, name):
      # Called with the name the LIST and index of the machine we want to see on page
      machineList = self.bigList
      target = name
      ind = machineList.machineIdInd(name)
      self.cssStart('tilasto')
      self.lB()
      self.tableStart()
      self.addTableRow("Machine location:", machineList.machineLocationInd(ind) )
      self.addTableRow("Mchine contact:", machineList.machineContactInd(ind) )
      nlh = {}
      nlh = machineList.machineNetworkInd(ind)
      for e in (nlh) :
	 self.addTableRow("Network adapter %s :" %e, nlh[e])
      self.addTableRow("Memory:", machineList.machineMemoryInd(ind) )
      self.addTableRow("System date:", machineList.machineSystemDateInd(ind) )
      self.addTableRow("Uptime:", machineList.machineUptimeInd(ind) )
      self.tableEnd()

class doMachineList(Render) :
   # This class creates a page, which we show to user.

   def __init__(self,koneet):
      # Basic init-method. This is used on creation.
      Render.__init__(self,koneet)

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
      # self.header()
      # koneet = self.koneet
      self.cssStart('tilasto')
      self.lB()
      print machineList.machineLocationInd(ind)
      self.lB()
      print machineList.machineContactInd(ind)
      self.lB()
      # print "Debug: addBasicInfo() params:", machineName, ind
      #print machineName.machineNameInd(ind)
      #print self.objDiv()
      # print "param: ", machineName," ind -> ", ind
      #print machineName.machineLocationInd(ind)
      # print "lalalal"
      #print self.objDiv()
      #print machineName.machineContactInd(ind)
      #print self.objDiv()
      #print machineName.machineNetworkInd(ind)
      #print self.objDiv()
      # print machineName.printAll(ind)
      # print " </p>"

   def addAllInfo(self, machineList, ind):
      # Called with the name the LIST and index of the machine we want to see on page
      self.cssStart('tilasto')
      self.lB()
      print machineList.machineLocationInd(ind)
      self.lB()
      print machineList.machineContactInd(ind)
      self.lB()
      nlh = {}
      nlh = machineList.machineNetworkInd(ind)
      for e in (nlh) :
	 print nlh[e]
	 self.lB()
      self.lB()
      print machineList.machineMemoryInd(ind)
      self.lB()
      print machineList.machineSystemDateInd(ind)
      self.lB()
      print machineList.machineUptimeInd(ind)


   def lueFilut(self, hakemisto):
      # Lukee hakemistossa olevien tiedostojen nimet ja polut talteen
      filukkeet = hakemisto
      # print "Debug: lueFilut() -> parametri: hakemisto -> ", hakemisto
      try:
	 snmpfilut1 = dircache.listdir(hakemisto)
	 snmpfilut1 = snmpfilut1[:]  # jotta voidaan muokata listaa
	 # print "Debug: lueFilut() -> dircache -> tulos2: ", snmpfilut1
	 snmpfilut2 = []
	 for fil in snmpfilut1:
	    withdir = hakemisto + '/' + fil
	    # print "Debug: koko -> ",withdir
	    snmpfilut2.insert(snmpfilut1.index(fil), hakemisto + '/' + fil)
	 # print "Debug: lueFilut() -> dircache -> tulos3: ", snmpfilut2
      except IOError, err:
 	 print 'Couldnt open the snmp-results-file-directory (%r).' % ('hakemisto',), err

      return snmpfilut2
      #return self.lista


class doConfigPage(Render) :

   def __init__(self, jep):
      Render.__init__(self, jep)

   def doPage(self, something) :
      self.header()
      print "<p> Config-page to handle settings of clients. </p>"
      self.cssClass('Config-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      self.footer()

class Error(Render):

    def __init__(self, text):
        self.text = text
        Render.__init__(self, jotain)
        self.prefix = [
            'Ongelmia jäsennyksessä',
            'Kärpänen',
            'Järjestelmä huumeessa',
            'Suoritus kohtasi seuraavan virhetilanteen',
            'Fehler',
            'Kone on tätä mieltä',
            'Saisit puolestani jatkaa, mutta',
            'Voi vittu',
            'Nyt ei oikein näytä sujuvan, ehkä sun kannatais mennä muualle'
            ]

    def doPage(self):
        self.header()
        self.cssClass("<b>%s:</b> %s" % (random.choice(self.prefix), self.text), 'virhe')
        self.footer()
