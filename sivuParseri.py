#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Original class author: Petteri Klemola
# Used and modified with permission for this use.
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

    def __init__(self, koneet):
        turhake = koneet
        self.cssPrefix = ""
	# "home"-URL for this page
        self.baseUrl0 = 'http://23.fi/Luokka:TestiURL'
        self.baseUrl = '%s' % self.baseUrl0

    def header(self):
        print "Content-Type: text/html \n"
        print "<html>"
        print "<head>"
        print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-15\" />"
        print "<meta name=\"Authors\" content=\"Tommi Ruuth, Petteri Klemola\" />"
        # print "<link rel=\"stylesheet\" href=\"http://23.fi/pelit/pelit.css\" type=\"text/css\">"
        print "<link rel=\"stylesheet\" href=\"pelit.css\" type=\"text/css\">"
        print "</head>"
        print "<body>"
        print "<h2>Server info</h2>"
        print "<p>Servers as list</p>"
        # print "<h2>Koneet</h2>"
        # print "<h2>Työkalut</h2>"
        # print "<ul><li>%s</ul>" % self.inUrl('Linkki 1', 'Linkki 2')
        self.cssEnd()
        self.cssStart('sisalto')

    def footer(self):
        self.cssEnd()
        self.cssClass('Maintainer: enskaätmedusapistetutkapistefi | %s' % self.url(self.baseUrl0,'Linux-tekstit'), 'footer')
        print "</body>"
        print "</html>"

    def cssClass(self,text,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"+self.formatText(text)+"</div>"

    def cssStart(self,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"

    def cssEnd(self):
        print "</div>"

    def tableStart(self):
        print "<table border=\"1\" >"

    def tableClStart(self):
        print "<tr>"

    def tableClEnd(self):
        print "</tr>"

    def tableSStart(self):
        print "</div>"

    def tableSEnd(self):
        print "</div>"

    def tableEnd(self):
        print "</table>"

    def lB(self):
        print "<br />"

    def objDiv(self):
        print " : "

    def formatText(self, text):
        text = str(text)
        return text.replace('\r\n','<br />')

    def inUrl(self, url, text=None):
        return self.url(self.baseUrl+"/"+url, text)

    def url(self, url, text=None):
        if text is None:
            text = url
        return "<a href=\"%(url)s\">%(text)s</a>" % {'url':url,'text':text}

class TeeKoneLista(Render) :
   # This class creates a page, which we show to user.

   def __init__(self,koneet):
      # Basic init-method. This is used on creation.
      Render.__init__(self,koneet)
      #self.koneet = koneet
      self.header()

      # This seems to be useless at the moment
      # self.cssStart('tilasto')

      # Luetaan läpi hakemisto, jossa tulosfilut ovat ja käsitellään
      # snmpParseri luokalla halutut filukkeet.
      # TODO:
      # -tehtävä config luokka/parseri, joka otetaan mukaan import:lla?
      kojeet = self.lueFilut("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")

      # This one needs to be changed. We want to have as return a hash-list?
      # bigList =  {}
      #for ind in kojeet:
	 # tiedot = snmpParseri.Parser(ind)
	 # bigList[ind] = tiedot
	 # print "Kone tiedot:", tiedot.koneNimi(), tiedot.koneSijainti(), tiedot.koneVerkko(), self.lB()
	 # print "Kone tiedot:", bigList.koneNimiInd(ind), bigList.koneSijaintiInd(ind), bigList.koneVerkkoInd(ind)
	 #, self.lB()
      # Lets end this part, then create a table for results
      self.cssEnd()
      self.cssStart('kuvaus')


      bigList = snmpParseri.Parser(kojeet)
      # This is the way to call object-lists...

      print "<p> Here starts the resultlist."
      self.lB()
      self.lB()
      # Table's dont work at the moment, there is not need for these now
      # print self.tableStart(), self.tableClStart()

      cou = 0
      for i in kojeet:
	 # This actually creates the machinelist
	 # TODO: The list should be a list of links on underpages, which
	 # contain detailed information about the machine
         # print "Kone ",cou + 1,": ", bigList.machineNameInd(cou), bigList.machineLocationInd(cou)
	 print "machine no:", cou+1 ,". "
	 self.lB()
	 print "%s" % self.url(bigList.machineNameInd(cou))
	 self.lB()
	 # "%s</ul>" % self.inUrl('Linkki 1', 'Linkki 2')
	 self.addName(bigList.machineNameInd(cou))
	 # For ALL the information, use addAllInfo
	 self.addAllInfo(bigList, cou)
	 self.lB()
	 # For only the basics, use addBasicInfo
	 #self.addBasicInfo(bigList, cou)
	 self.lB()
	 cou = cou + 1

      print self.objDiv()
      print self.tableClEnd(), self.tableEnd()
      # print machineName.printAll(ind)
      print " </p>"
      # And this works
      # print "Debug: result: ", bigList.koneNimiInd(0)

      #print "Kone :", tiedot.koneNimi(), tiedot.koneSijainti(), tiedot.koneVerkko()
      #for i in tiedot:
      #   print i
      # print snmpParseri.perusTiedot(koneet)
      #oli = snmpParseri.testi(koneet)
      #print oli.parser(koneet)
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

   def render(self):
      # self.header()
      # koneet = self.koneet
      self.cssStart('tilasto')
      print "<p> kone 1 </p>"
      self.cssEnd()
      # self.footer()

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

    def render(self):
        self.header()
        self.cssClass("<b>%s:</b> %s" % (random.choice(self.prefix), self.text), 'virhe')
        self.footer()
