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
   # Eri html osat, joista tehdaan itse sivu. Nama koootaan yhteen joko tavallisena
   # html:na tai esim. php:na...
   html_dir = "/home/tommi/omat/python/snmpinfo/html"
   # Testausta varten
   # SNMPv2-MIB::sysName.0 = STRING: byakhee
   # SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...
   # Muuttujia
   # Testaamiseen
   # snmpt = ['SNMPv2-MIB::sysName.0 = STRING: byakhee', 'SNMPv2-MIB::sysLocation.0 = STRING: Kulkee ties missa...']

   snmpt = []
   ##########################
   # Moduulit
   def snmp_vastaus(snmp_tulos) :
      # Kutsutaan yhdella snmp-kyselyn tulosrivilla
      # Palauttaa takaisin snmp-muuttujan nimen ja tuloksen
      osa = re.search('^(.*)::(.*) = (.*): (.*)', snmp_tulos)
      return osa.group(2), osa.group(4)


#      kone = tulosparit['sysName.0']

   def koneNimi(lista):
      # Hakee koneen nimen ja palauttaa sen
      return lista.get('sysName.0', 'Arvoa ei ollut')

   def koneKontakti(lista):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      return lista.get('sysContact.0', 'Arvoa ei ollut')

   def koneSijainti(lista):
      # Hakee koneen sijainnin ja palauttaa sen
      return lista.get('sysLocation.0', 'Arvoa ei ollut')

   def koneVerkko(lista):
      # Hakee koneen eri verkkoliittymät ja palauttaa ne
      return lista.get('sysContact.0', 'Arvoa ei ollut')

   def koneIpt(lista):
      # Hakee koneen ipt (poislukien localhost) ja palauttaa sen
      return lista.get('sysContact.0', 'Arvoa ei ollut')

   def koneMuisti(lista):
      # Hakee koneen fyysisen muistin määrän ja palauttaa sen
      # pitää hakea oikea muuttuja ->  HOST-RESOURCES-MIB::hrStorageDescr.1 = STRING: Physical memory
      # Ja tämä avulla oikea lukuarvo -> HOST-RESOURCES-MIB::hrStorageSize.1 = INTEGER: 2062168
      return lista.get('.0', 'Arvoa ei ollut')

   def koneJoku1(lista):
      # Hakee koneen nimen ja palauttaa sen
      return lista.get('sysContact.0', 'Arvoa ei ollut')

   def koneJoku2(lista):
      # Hakee koneen nimen ja palauttaa sen
      return lista.get('sysContact.0', 'Arvoa ei ollut')


   ###########################
   #  MAIN
   try:
      filu = open('snmp_kyselyt/byakhee.system.txt', 'r')
   except IOError, err:
      print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % ('snmp_kyselyt/byakhee.system.txt',), err
      #return []
   le = int(0)
   type(le)
   testi = {}
   for li in  filu.readlines() :
      # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
      # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
      # snmpt.append(snmp_vastaus(li))
      avain, arvo = snmp_vastaus(li)
      testi[avain] = arvo
   filu.close()

   # print testi
   print koneNimi(testi), koneKontakti(testi), koneSijainti(testi)

