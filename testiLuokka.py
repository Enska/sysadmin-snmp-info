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

      # ao. kutsu tehtävä ehkä loopissa, nyt luetaan hakemiston tiedot monta kertaa
      self.kokolista = self.teeLista(lahdeHakemisto)

      # print self.kokolista('sysName.0', 'Arvoa ei ollut')
      #print self.kokolista['sysName.0']

   def tulosta(self):
      print "testiLuokka -> tulosta -> Minun nimeni on", self.nimi
      # print "...."

   def nimea(self, parempiNimi):
      self.nimi = parempiNimi

   def teeLista(self, lahdeHakemisto):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi
      #
      # ONGELMA: Mutta edelleen vain viimeisimmän filukkeen tiedot jäävät talteen
      # -> eli tehtävä oma skalaari itse filumuuttujia varten? (tjms.)
      #
      #
      filut = glob.glob('%s/*' %lahdeHakemisto)
      # print "Debug: testiLuokka -> teeLista -> filut : ", filut
      self.konelista = {}
      ind = 0
      fil = 0

      # mainlist to hold all the results. List of hash-lists!
      self.filuLista = {}

      # Lets go through every file waht we have on result-dir
      for filuke in filut :

	 # Results are collected on this list
         self.lista = {}
	 try:
	    # print "Debug: testiLuokka -> teeLista -> filuke   : ", filuke
            filu = open(filuke, 'r')
            for li in filu.readlines() :
   	 # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
   	 # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
   	 # snmpt.append(snmp_vastaus(li))
	        # print "Debug: testiLuokka -> teeLista -> li : ", li

		# parse from the resultline the humanreadable key and its value
   	        avain, arvo = self.snmpVastaus(li)
   	        self.lista[avain] = arvo
            filu.close()

	    # Lets add the newly created snmp-results list to the mainlist
	    # Mainlist holds all the machines
	    self.filuLista[fil] = self.lista
	    fil = fil + 1
         except IOError, err:
            print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % ('snmp_kyselyt/byakhee.system.txt',), err

	#self.konelista[ind] = lista
	#ind = ind + 1
	#print "Debug: ", konelista

      #self.kokolista = self.lista
      return self.lista

   def snmpVastaus(self, snmpRivi) :
      # Kutsutaan yhdella snmp-kyselyn tulosrivilla
      # Palauttaa takaisin snmp-muuttujan nimen ja tuloksen
      osa = re.search('^(.*)::(.*) = (.*): (.*)', snmpRivi)
      return osa.group(2), osa.group(4)
      # kone = tulosparit['sysName.0']

   def koneNimi(self):
      # Is machineName good enough for ID? Is it unique enough?
      # machineName + IP ? Do we need uniq id?
      # Hakee koneen nimen ja palauttaa sen
      #return self.lista('sysName.0', 'Arvoa ei ollut')
      # print self.kokolista['sysName.0', 'Arvoa ei ollut']
      print self.kokolista['sysName.0']

   def machineNameInd(self,ind):
      # Gets machine name from the index "ind" and returns that machines name
      # print "machineName -> ", self.filuLista[ind]['sysName.0']
      print self.filuLista[ind]['sysName.0']

   def contactName(self):
      # Gets the system contact name and returns it
      print self.kokolista['sysContact.0']

   def contactNameInd(self,ind):
      # Gets the system contact name and returns it
      print self.filuLista[ind]['sysContact.0']


   def systemLocationInd(self,ind):
      # @param: self and index for machine
      # prints the result
      print "location -> ", self.filuLista[ind]['sysLocation.0']

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