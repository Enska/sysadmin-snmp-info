#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# ohjelma kasittelee snmp-kyselysta saatuja tietoja
#
# tiedot kerataan esim. kerran paivassa, cachetetaan se mita on kasitelty
# ja seurataan tietojen ikaa (seka on myos tarkastettava cachen ikaa).
# tulokset kuitenkin laitetaan eteenpain, kayttaja ei kayta pythonia
# tuloksien katseluun. -> sivut pitaa rakentaa osista... ks. cacti sivut
#
# kerataan kamat filuun (python vai cron?, mista hostit?)
# parsetaan talteen mielenkiintoiset (vaiko, ei edes haeta muita?)
# Laitetaan filuun, jota kaytetaan sivun tekoon
# -> staattinen sivu, mutta kerataako aina osista, vaiko tehdaanko suoraan
# yhdeksi sivuksi?

# Perusasiat
# SNMPv2-MIB::sysDescr.0
# DISMAN-EVENT-MIB::sysUpTimeInstance
# SNMPv2-MIB::sysContact.0
# SNMPv2-MIB::sysName.0
# SNMPv2-MIB::sysLocation.0

# HOST-RESOURCES-MIB::hrSystemUptime.0
# HOST-RESOURCES-MIB::hrSystemDate.0
# HOST-RESOURCES-MIB::hrSystemInitialLoadDevice.0
# HOST-RESOURCES-MIB::hrSystemInitialLoadParameters.0
# HOST-RESOURCES-MIB::hrSystemNumUsers.0 4


# HOST-RESOURCES-MIB::hrStorageDescr.1 (muisti)  Mutta saattavat vaihdella eri koneilla
# HOST-RESOURCES-MIB::hrStorageDescr.31 (levyt)
# HOST-RESOURCES-MIB::hrStorageDescr.32


# Muuttujia
# lahdefilut
# cache

import sys
import string
import re

class Parser:

   def __init__(self, sourceDirectory):
      # @param: The directry of the source-files
      # This one is mandatory. -> TODO: check the param
      self.nimi = sourceDirectory
      # print "Debug: snmpParseri -> __init__ -> nimi -> ", nimi
      # Eri html osat, joista tehdaan itse sivu. Nama koootaan yhteen joko tavallisena
      # html:na tai esim. php:na...
      self.html_dir = "/home/tommi/omat/python/snmpinfo/html"
      # Testausta varten
      # SNMPv2-MIB::sysName.0 = STRING: byakhee
      # SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...
      # Muuttujia
      # Testaamiseen
      # snmpt = ['SNMPv2-MIB::sysName.0 = STRING: byakhee', 'SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...']

      # This we shouldnt need, we returned list is allready a hash-list.
      self.bigList =  {}
      cou = 0

      for sourceFile in sourceDirectory:
	 # Actually nimi is a directory
	 self.bigList[cou] = self.doOneMachineList(sourceFile)
	 # print "Debug: one result (",cou,"): ", self.bigList[cou], "\n"
         cou = cou + 1


   ##########################
   # perusfunktiot

   def doOneMachineList(self, sourceDir):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi
      # print "Debug: dirikka ->", lahdeTiedosto
      try:
	 filu = open(sourceDir, 'r')
	 self.lista = {}
         for livi in filu.readlines() :
	     # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
	     # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
	     # snmpt.append(snmp_vastaus(li))
	     avain, arvo = self.snmpVastaus(livi)
	     self.lista[avain] = arvo
         filu.close()
      except IOError, err:
	 print 'snmp-t9ulostiedostoa (%r) ei pystytty avaamaan.' % (lahdeTiedosto,), err
	 #return []

      return self.lista



   def teeLista(self, lahdeTiedosto):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi
      # print "Debug: dirikka ->", lahdeTiedosto
      self.lista = {}

      try:
	 filu = open(lahdeTiedosto, 'r')
         for livi in filu.readlines() :
	     # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
	     # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
	     # snmpt.append(snmp_vastaus(li))
	     avain, arvo = self.snmpVastaus(livi)
	     self.lista[avain] = arvo
	     filu.close()
      except IOError, err:
	 print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % (lahdeTiedosto,), err
	 #return []

      return self.lista

   def snmpVastaus(self,snmptulos) :
      # Kutsutaan yhdella snmp-kyselyn tulosrivilla
      # Palauttaa takaisin snmp-muuttujan nimen ja tuloksen
      osa = re.search('^(.*)::(.*) = (.*): (.*)', snmptulos)
      return osa.group(2), osa.group(4)
      # kone = tulosparit['sysName.0']

   def koneNimi(self):
      # Hakee koneen nimen ja palauttaa sen
      return self.kokolista.get('sysName.0', 'Arvoa ei ollut')

   def machineNameInd(self,ind):
      # Hakee koneen nimen ja palauttaa sen
      return self.bigList[ind].get('sysName.0', 'Arvoa ei ollut')

   def koneKontakti(self):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      return self.kokolista.get('sysContact.0', 'Arvoa ei ollut')

   def machineContactInd(self,ind):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      return self.bigList[ind].get('sysContact.0', 'Arvoa ei ollut')

   def koneSijainti(self):
      # Hakee koneen sijainnin ja palauttaa sen
      return self.kokolista.get('sysLocation.0', 'Arvoa ei ollut')

   def machineLocationInd(self,ind):
      # Hakee koneen sijainnin ja palauttaa sen
      return self.bigList[ind].get('sysLocation.0', 'Arvoa ei ollut')

   # These are handled by the snmp-index number.
   def machineNetworkInd(self, ind):
      # Asks all the network interfaces from the method, then return this as a list
      # TODO
      # Loop the multiple network connections.
      #
      nw = {}
      coun = 1
      lele = ""
      # print "testi 2 ->", self.bigList[ind].get('ifIndex.1', "null hits!")
      ehk = 'ifIndex.' + str (coun)
      while ( ( self.bigList[ind].get(ehk, "0")) != "0") :
	 idf = 'ifDescr.' + str (coun)
	 ipa = 'ifPhysAddress.' + str (coun)
	 ias = 'ifAdminStatus.' + str (coun)
	 ios = 'ifOperStatus.' + str (coun)
	 # print "idf (", coun, ")-> ", self.bigList[ind].get(idf, "-1")
	 # print "ipa (", coun, ")-> ", self.bigList[ind].get(ipa, "-1")
	 # print "ias (", coun, ")-> ", self.bigList[ind].get(ias, "-1")
	 # print "ios (", coun, ")-> ", self.bigList[ind].get(ios, "-1")
	 # print "ehk (", coun, ")-> ", ehk, "Res -> ", self.bigList[ind].get(ehk, "0")
	 result = self.bigList[ind].get(idf, "zero") + " : " + self.bigList[ind].get(ipa, "zero") + " : " + self.bigList[ind].get(ias, "zero") + " : " + self.bigList[ind].get(ios, "zero")
	 # nw[coun] = self.bigList[ind].get('ehk', coun)
	 nw[coun] = result
	 coun = coun + 1
	 ehk = 'ifIndex.' + str (coun)

      # for i in (self.bigList[ind]):
	 # ehk = 'ifIndex.' + str (coun)
	 # print "ehk -> ", ehk
	 # if  ( ( self.bigList[ind].get(ehk, "0")) == "1" ) :
	    # nw[coun] = self.bigList[ind].get('ehk', coun)
	    # nw[coun] = self.bigList[ind].get('ifIndex.%s', coun)
	    # jep = self.bigList[ind].get('ehk', coun)
	    # print "Testi loytyi -> ",jep, "ja -> ", ehk
	    # coun = coun + 1
      for i in (nw) :
      # if (self.bigList[ind].get('ifIndex.%s', coun, 'jep')):
	 # lele = lele + str (self.bigList[ind].get('ifIndex.%s', nw[i]))
	 lele = lele + nw[i] + "\n"
	 coun = coun + 1
         # return "jejeje"
	 # self.bigList[ind].get('idIndex', 'Arvoa ei ollut')
      return lele

   def koneIpt(self):
      # Hakee koneen ipt (poislukien localhost) ja palauttaa sen
      return self.kokolista.get('sysContact.0', 'Arvoa ei ollut')

   def koneMuisti(self):
      # Hakee koneen fyysisen muistin määrän ja palauttaa sen
      # pitää hakea oikea muuttuja ->  HOST-RESOURCES-MIB::hrStorageDescr.1 = STRING: Physical memory
      # Ja tämä avulla oikea lukuarvo -> HOST-RESOURCES-MIB::hrStorageSize.1 = INTEGER: 2062168
      return self.kokolista.get('.0', 'Arvoa ei ollut')

   def koneJoku1(self):
      # Hakee koneen nimen ja palauttaa sen
      return self.lista.get('sysContact.0', 'Arvoa ei ollut')

   def koneJoku2(lista):
      # Hakee koneen nimen ja palauttaa sen
      return lista.get('sysContact.0', 'Arvoa ei ollut')

   def vastaus(self, hakemisto):
      return "jokin string"


   def printAll(self, ind):
       # print the whole list, dont return anything.
       # ONLY for testing!
       cou=1
       for i in self.bigList[ind] :
	  print "Koneindeksi:", ind, " -> avain:", i, " ->  arvo:", self.bigList[ind].get(i, 'none')
	  cou= cou + 1