#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import string
import re
import glob

class tl:

   def __init__(self, nimi, lahdeHakemisto):
      self.nimi = nimi
      #self.nimi = self.teeLista(lahdeHakemisto)
      # self.lista = listaNimi
      self.kokolista =  {}
      self.kokolista = self.teeLista(lahdeHakemisto)
      # print self.kokolista('sysName.0', 'Arvoa ei ollut')
      #print self.kokolista['sysName.0']

   def tulosta(self):
      print "Minun nimeni on", self.nimi

   def nimea(self, parempiNimi):
      self.nimi = parempiNimi

   def teeLista(self, lahdeHakemisto):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi
      filut = glob.glob('%s/*' %lahdeHakemisto)
      for filuke in filut :
         self.lista = {}
	 try:
	    print "Debug: avataan ->", filuke
            filu = open(filuke, 'r')
            for li in filu.readlines() :
   	 # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
   	 # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
   	 # snmpt.append(snmp_vastaus(li))
   	        avain, arvo = self.snmpVastaus(li)
   	        self.lista[avain] = arvo
            filu.close()
         except IOError, err:
            print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % ('snmp_kyselyt/byakhee.system.txt',), err

      #self.kokolista = self.lista
      return self.lista

   def snmpVastaus(self, snmpRivi) :
      # Kutsutaan yhdella snmp-kyselyn tulosrivilla
      # Palauttaa takaisin snmp-muuttujan nimen ja tuloksen
      osa = re.search('^(.*)::(.*) = (.*): (.*)', snmpRivi)
      return osa.group(2), osa.group(4)
      # kone = tulosparit['sysName.0']

   def koneNimi(self):
      # Hakee koneen nimen ja palauttaa sen
      #return self.lista('sysName.0', 'Arvoa ei ollut')
      # print self.kokolista['sysName.0', 'Arvoa ei ollut']
      print self.kokolista['sysName.0']


   def tulostaX(self, X):
      cou=1
      # TODO Vähän paremmin tämä... Ei jaksa miettiä...
      while cou < X :
	 for i in self.kokolista:
	  # range(X)
	     print "Alkio ", cou, ": ", i, " -> ", self.kokolista[i]
	     cou= cou + 1

   def tulostaKaikki(self):
       # Tulostaa koko listan...
       # EI palauta mitään
       cou=1
       for i in self.kokolista :
	  print "Alkio ", cou, ": ", i, " -> ", self.kokolista[i]
	  cou= cou + 1