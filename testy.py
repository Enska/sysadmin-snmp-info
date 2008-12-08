#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import string
import re
import testiLuokka

t = testiLuokka.tl("joko", "/home/tommi/omat/python/snmpinfo/snmp_kyselyt/")
t.tulosta()
t.teeLista("snmp_kyselyt")
t.nimea("Lala")
# Tarkoitus on tulostaa X ensimmäistä listalta...
# t.tulostaX(3)
t.koneNimi()
print "Katsotaan listaa -> ", t.tulosta()
t.tulostaKaikki()