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
	 # Go trough all snmp-result files on sourceDirectory -dir
	 self.bigList[cou] = self.doOneMachineList(sourceFile)
	 # print "Debug: one result (",cou,"): ", self.bigList[cou], "\n"
         cou = cou + 1


   ##########################
   # perusfunktiot

   def doOneMachineList(self, snmpInfoFile):
      # This one reads the file trough. Collect everything from it and
      # returns it as a dict-list for the caller.
      #
      # FIX: Do a check that the file is really a txt-file.
      #
      # print "Debug: dirikka ->", lahdeTiedosto
      try:
	 filu = open(snmpInfoFile, 'r')
	 # Do file-check here, before readeing the content
	 self.lista = {}
         for livi in filu.readlines() :
	     # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
	     # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
	     # snmpt.append(snmp_vastaus(li))
	     string.strip(livi)
	     #string.lstrip(livi)
	     # livi.splitlines()
	     # print "Debug snmpParseri.py -> livi ->", livi, "<-"
	     avain, arvo = self.snmpVastaus(livi)
	     self.lista[avain] = arvo
         filu.close()
      except IOError, err:
	 print 'Couldnt open snmp-datafile directory: (%r).' % (snmpInfoFile), err
	 #return []

      return self.lista

   def teeLista(self, lahdeTiedosto):
      # Tama funktio tekee listan tuloksista jota sitten käpistellään
      # Luetaan tiedostot dict-listoiksi
      # print "Debug: dirikka ->", lahdeTiedosto
      self.lista = {}
      print 'Debug: We want to open a file'

      try:
	 filu = open(lahdeTiedosto, 'r')
         for livi in filu.readlines() :
	     # Kaydaan kaikki tulosrivit lapi tiedostosta ja laitetaan tulokset talteen
	     # testi-dict :iin. Avaimeksi aina snmp-muuttuja ja arvoksi snmp-kyselyn tulos
	     # snmpt.append(snmp_vastaus(li))
	     # print "Debug snmpParseri.py -> livi -> ", livi
	     avain, arvo = self.snmpVastaus(livi)
	     self.lista[avain] = arvo
	     filu.close()
      except IOError, err:
	 print 'snmp-tulostiedostoa (%r) ei pystytty avaamaan.' % (lahdeTiedosto,), err
	 #return []

      return self.lista

   def snmpVastaus(self,snmptulos) :
      # Params: one line of the snmpwalk result.
      # Action: Strip of the snmpwalk stuff like MIB information and some chars.
      # As a result return the human readable name of the MIB and its content
      # FIX: Sometimes the results dont contain "sss::sss:sss" lines
      # FIX: Check if there anything at all to search at snmptulos variable -> done
      #
      #
      finimi = ""
      finres = ""
      # Old default handler
      # osa = re.search('^(.*)::(.*) = (.*): (.*)', snmptulos)
      #
      if snmptulos == '' :
	 # Empty result?
	 # print "Debug: Something ir horribly wrong, return this"
	 # print "Debug: snmptulos -> ", snmptulos
	 return "problem", "result empty"
      #########################################
      # New way
      osa = re.search('^(.*) = (.*)', snmptulos)
      # print "Debug: reg-expr results osa 0:", osa.group(0)
      # print "Debug: reg-expr results osa 1:", osa.group(1)
      # print "Debug: reg-expr results osa 2:", osa.group(2)
      # print "Debug: reg-expr results osa 3:", osa.group(3)
      # Then lets see if there is some content for the MIB
      # If not, then this is empty result, remove just the "=" char
      # else do as usual, remove " = TYPE:" part
      nimi = re.search('^(.*)::(.*)', osa.group(1))
      # print "Debug: reg-expr results nimi 1:", nimi.group(1)
      # print "Debug: reg-expr results nimi 2:", nimi.group(2)
      finimi = nimi.group(2)
      # ('INTEGER' | 'OID' | 'STRING')
      # if ((":") in osa.group(2)):
      # Problem for if-statement:
      # IF variable is not set, we cannot check if there is content or not, gives error:
      # AttributeError: 'NoneType' object has no attribute 'group'
      # So how to check if there is content? -> count
      if ( (str.count(osa.group(2), ":")) >= 1 ):
	 # If there is something to find, lets check.
	 # No sense setting these as list for search:
	 # STRING|OID|INTEGER|Gauge32|Counter32|IpAddress|Timeticks
	 cont = re.search('(.*): (.*)$', osa.group(2))
	 # print "Debug: search testi. Var -> ", osa.group(2), " Pointer ->", cont
	 # print "Debug: reg-expr results cont 0:", cont.group(0)
	 # print "Debug: reg-expr results cont 1:", cont.group(1)
	 # print "Debug: reg-expr results cont 2:", cont.group(2)
	 # We need to check, if there is anything at cont.group(2)
	 if ( (str.count(cont.group(2), '')) >= 1 ) :
	    # Ok, wefound something as a final result.
	    # print "Debug: (if cont != ) reg-expr results cont 1:", cont.group(1)
	    # print "Debug: (if cont != ) reg-expr results cont 2:", cont.group(2)
	    finres = cont.group(2)
	 else :
	    # NO RESULT, value of the OID was is empty (zero lenght)
	    # print "Debug: reg-expr results are null for cont 1:", cont
	    # print "Debug: reg-expr results for cont 2:", cont.group(2)
	    # finres = osa.group(2)
	    finres = "None results for this OID"
      else :
	 finres = "No results for this OID."
      # Old default return
      # return osa.group(2), osa.group(4)
      # return nimi.group(2), cont.group(2)
      # print "---------------------"
      return finimi, finres

   def snmpReply(self,snmptulos) :
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
      # inter='sysName.0'
      # return self.bigList[ind].get('sysName.0', ('Variable ' + inter + ' didnt exist in snmp results. '))
      return self.bigList[ind].get('sysName.0', 'NOPE')

   def machineIdInd(self, name):
      # Checks trough the list and returns the index of succesful find. Otherwise returns -1
      resu = -1
      look = name
      for k in self.bigList:
	if ( self.machineNameInd(k) == name):
	    resu = k
      return resu

   def koneKontakti(self):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      inter='sysContact.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def machineContactInd(self,ind):
      # Hakee koneen kontaktitiedot ja palauttaa sen
      inter='sysContact.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def koneSijainti(self):
      # Hakee koneen sijainnin ja palauttaa sen
      inter='sysLocation.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def machineLocationInd(self,ind):
      # Hakee koneen sijainnin ja palauttaa sen
      inter='sysLocation.0'
      # print "Debug: ind -> ", ind," value -> ", self.bigList[ind].get(inter)
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   # These are handled by the snmp-index number.
   # NOTE: how about ipV6 interfaces?
   def machineNetworkInd(self, ind):
      # Asks all the network interfaces from the method, then return this as a list
      # TODO
      # Loop the multiple network connections.
      # CHANGE -> Returns a list of network interfaces. Caller must take care the
      # divide between these.
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
      # return lele
      return nw

   def koneIpt(self):
      # Hakee koneen ipt (poislukien localhost) ja palauttaa sen
      return self.kokolista.get('sysContact.0', 'Arvoa ei ollut')

   # TODO: list of ALL memorys (phys and virtual)
   def machineMemoryInd(self,ind):
      # Return the index for the memory of the machine
      # TODO: Check if this one differs on Solaris vs. Linux
      # One possible variable -> HOST-RESOURCES-MIB::hrStorageSize.1 = INTEGER: 2062168
      inter='hrMemorySize.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def machineUptimeInd(self,ind):
      # Return the uptime for this machine (this should always be present)
      # TODO: Check also that this info is collected from machine
      inter='hrSystemUptime.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def machineSystemDateInd(self, ind):
      # Return the machine systemdate (this is the fixed datem not UTC)
      inter='hrSystemDate.0'
      return self.bigList[ind].get(inter, ('Variable ' + inter + ' didnt exist in snmp results. '))

   def vastaus(self, hakemisto):
      return "jokin string"

   def printAll(self, ind):
       # print the whole list, dont return anything.
       # ONLY for testing!
       cou=1
       for i in self.bigList[ind] :
	  print "Koneindeksi:", ind, " -> avain:", i, " ->  arvo:", self.bigList[ind].get(i, 'none')
	  cou= cou + 1