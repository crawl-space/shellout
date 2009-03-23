#!/usr/bin/python

import shellout as so

print "============================================="
print
print so.ls.l.si("/")
print 
print "============================================="
print 
print so.svn.help()
print
print "============================================="
print
print so.ps.a.u.x()
print
print "============================================="
print
print so.ls.color["always"]("/")
print
print "============================================="
print
print so.grep("model name", "/proc/cpuinfo")
