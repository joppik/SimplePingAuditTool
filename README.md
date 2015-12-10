# SimplePingAuditTool

writen in Python

Ping networks and write output to sqlite3 and flat file

script to audit live hosts in a network by VLAN and collect results

script reads control.txt file for VLAN and subnet information, eg 
300 192.168.1.0/24
400 192.168.10.0/24

and then writes output to sqlite3 database and scratch file. A summmary file is also created to show "UP" hosts

script calls "fping -C 1 -q <IP>"

