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
        self.baseUrl0 = 'http://23.fi/Luokka:Linux'
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
        print "<h2>Laiteinfo sivu</h2>"
        print "<p>Koneet ja niiden tiedot.</p>"
        print "<h2>Koneet</h2>"
        print "<h2>Työkalut</h2>"
        print "<ul><li>%s</ul>" % self.inUrl('Linkki 1', 'Linkki 2')
        self.cssEnd()
        self.cssStart('sisalto')

    def footer(self):
        self.cssEnd()
        self.cssClass('Ylläpitäjä: enskaätmedusapistetutkapistefi | %s' % self.url(self.baseUrl0,'Linux-tekstit'), 'footer')
        print "</body>"
        print "</html>"

    def cssClass(self,text,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"+self.formatText(text)+"</div>"

    def cssStart(self,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"

    def cssEnd(self):
        print "</div>"

    def lB(self):
        print "<br>"

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

   def __init__(self,koneet):
      Render.__init__(self,koneet)
      #self.koneet = koneet
      self.header()
      self.cssStart('tilasto')

      # Luetaan läpi hakemisto, jossa tulosfilut ovat ja käsitellään
      # snmpParseri luokalla halutut filukkeet.
      # TODO:
      # -tehtävä config luokka/parseri, joka otetaan mukaan import:lla?
      kojeet = self.lueFilut("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      # print "Debug: kojeet: ", kojeet, self.lB()
      for ind in kojeet:
	 tiedot = snmpParseri.Parser(ind)
	 print "Kone tiedot:", tiedot.koneNimi(), tiedot.koneSijainti(), tiedot.koneVerkko(), self.lB()
      # Nyt käsitellään vain yksi tulostiedosto.
      #tiedot = snmpParseri.Parser(koneet)
      #print "Kone :", tiedot.koneNimi(), tiedot.koneSijainti(), tiedot.koneVerkko()
      #for i in tiedot:
      #   print i
      # print snmpParseri.perusTiedot(koneet)
      #oli = snmpParseri.testi(koneet)
      #print oli.parser(koneet)
      self.cssEnd()
      self.footer()

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
 	 print 'snmp-tuloshakemistoa (%r) ei pystytty avaamaan.' % ('hakemisto',), err

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
