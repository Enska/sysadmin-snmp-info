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

   def __init__(self, nimi):
      # Jos annettaisiin parametrina hakemisto, josta tiedot luettaisiin
      # Ei tehdä vielä näin...
      self.nimi = nimi
      # Eri html osat, joista tehdaan itse sivu. Nama koootaan yhteen joko tavallisena
      # html:na tai esim. php:na...
      self.html_dir = "/home/tommi/omat/python/snmpinfo/html"
      # Testausta varten
      # SNMPv2-MIB::sysName.0 = STRING: byakhee
      # SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...
      # Muuttujia
      # Testaamiseen
      # snmpt = ['SNMPv2-MIB::sysName.0 = STRING: byakhee', 'SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...']
      self.kokolista =  {}
      self.kokolista = self.teeLista("lahdeHakemisto")


   ##########################
   # perusfunktiot

   def teeLista(self, lahdeHakemisto):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi

      try:
	 filu = open('snmp_kyselyt/byakhee.system.txt', 'r')
      except IOError, err:
	 print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % ('snmp_kyselyt/byakhee.system.txt',), err
	 #return []
      self.lista = {}
      for livi in filu.readlines() :
	 # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
	 # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
	 # snmpt.append(snmp_vastaus(li))
	 avain, arvo = self.snmpVastaus(livi)
	 self.lista[avain] = arvo
      filu.close()
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

   def koneKontakti(self):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      return self.kokolista.get('sysContact.0', 'Arvoa ei ollut')

   def koneSijainti(self):
      # Hakee koneen sijainnin ja palauttaa sen
      return self.kokolista.get('sysLocation.0', 'Arvoa ei ollut')

   def koneVerkko(self):
      # Hakee koneen eri verkkoliittymät ja palauttaa ne
      # TODO
      # Looppi usealla liittymälle
      return self.kokolista.get('sysContact.0', 'Arvoa ei ollut')

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


