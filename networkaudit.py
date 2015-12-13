import subprocess
import ipaddress
import sqlite3
import time

thetime = time.strftime("%H:%M:%S")
datet = time.strftime("%d-%m-%Y")

# open control file and read VLAN and subnet information
file = open('control.txt')
for line in file:
	a, b = line.strip().split()
	vlanid = a
	net_addr = b
	net_add = unicode(net_addr)

# open and append summary file to store summary of output
	summary = "summary.txt"
        tabs = open(summary, 'a')

# Create the network
	ip_net = ipaddress.ip_network(net_add)

# Get all hosts on that network
	all_hosts = list(ip_net.hosts())

# create output file using vlan and time/date information
        ex = ("_vlan:"+vlanid+"-"+thetime+"_"+datet)
        filename = 'scratch%s.txt' % ex
        print "creating file called", filename, "containing output of scan"
	sfile = open(filename, 'w')

# loop over all IPs found in networks defined in control file
	for i in range(len(all_hosts)):
		thetime = time.strftime("%H:%M:%S")
		datet = time.strftime("%d-%m-%Y")
		timenow = str(thetime)
		datenow = str(datet)
		hostname = str(all_hosts[i])
		ping = subprocess.Popen(["fping", "-C", "1", "-q", hostname], stderr=subprocess.PIPE,  stdout=subprocess.PIPE)
		out, err = ping.communicate()
		if "-" not in err:
			d = err.strip()
			print  (d, timenow, datenow,   "up")
			sfile.write(d +" : "+ timenow +" : "+ datenow +  " : up\n")
		else:
			e = err.strip()		
			print (e, timenow, datenow,  "down")
			sfile.write(e +" : "+  timenow +" : "+ datenow +  " : down\n")

	sfile.close()
	print "closeing scratch file"

	print "moving output to sql database"

# connect to database
	conn = sqlite3.connect("database.db") 
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS tableofdata__ (vlan, ip, response_in_ms, state, time, date); ")

	category = "Sports"
	with open(filename, "r") as sports:
        	lines = sports.readlines()

	for line in lines:
    # Split the line on whitespace
        	data = line.split()
        	one = data[0]
        	two = data[1]
        	three = data[2]
        	four = data[3]
		five = data[4]
		six = data[5]
		seven = data[6]
		eight = data[7]
		nine = data[8]
    # Put this through to SQL using an INSERT statement...
        	cursor.execute("INSERT INTO tableofdata__ (vlan, ip, response_in_ms, state, time, date) VALUES(?, ?, ?, ?, ?, ?)", (vlanid, one, three, nine, five, seven))
	conn.commit()

	print "completed sucesfully"
	print "write to summary file"
        conn = sqlite3.connect("database.db") # or use :memory: to put it in RAM
        cursor = conn.cursor()
        t = (vlanid,)

        count = 0
        for row in cursor.execute("""SELECT ip,state FROM tableofdata__ WHERE state="up" AND vlan=?""", t):
                count +=1
        print "we have ", count, " nodes up in vlan ", vlanid
        strcount = str(count)
        strt = str(t)
        tabs.write("At "+ thetime + " on " + datet +" we had " + strcount + " nodes up in vlan " + vlanid + "\n")
        tabs.close()
        conn.commit()

else:
	print "all done"
