#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import string
import re
import testiLuokka


# And then, how to see other instances?
t = testiLuokka.tl("joko", "/home/tommi/omat/python/snmpinfo/snmp_kyselyt/")

# This prints only the named instance
t.tulosta()

# print "turha kutsu? <------------------------> ?"
# Ei kutsuta t�t� toistamiseen, ajaa vanhojen p��lle...
# TODO: fix vain yhden koneen tiedot n�kyv�t!
# t.teeLista("snmp_kyselyt")

t.nimea("Lala")

# Tarkoitus on tulostaa X ensimm�ist� listalta...
# t.tulostaX(3)
t.koneNimi()
print "Our machine is ", t.machineNameInd(0), " on a " , t.systemLocationInd(0), "."


t.machineNameInd(1)
# t.machineNameInd(2)
t.contactNameInd(0)

print "Katsotaan listaa -> ", t.tulosta()
#t.tulostaKaikki()



print "End of testy.py class."
