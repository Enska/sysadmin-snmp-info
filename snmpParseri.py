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


# HOST-RESOURCES-MIB::hrStorageDescr.1 (muisti)
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
      return lista['sysDescr-0']

   ###########################
   #  MAIN
   filu = open('snmp_kyselyt/byakhee.system.txt', 'r')
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

   print testi



