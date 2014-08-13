#!/usr/bin/python

#######
# this is a script to get the currently joined Access Points, and other useful info from a WLC.
# Replace the RO_String below, with your SNMP RO community.
# Originally created on July 18 2013 by Mike Albano
# Severely modified on Aug 8 2014 by Daniel Klopp
########

import os, sys, commands

# Define your snmp RO String
RO_string =''
# Define your WLC's by IP:
WLC_List = ['1']

# Minor exception handling
try:
  open('/tmp/wlc_aps', 'w')
except:
  print sys.stderr, "Couldn't open file"
  sys.exit(1)

# Define the output files
outfile1 = open("/tmp/wlc_aps", "w")

def get_ap_data(WLC):
    # use net-snmp to get entire 'bsnAPTable'. Check the AIRESPACE-WIRELESS-MIB.my for what column heading definitions.
    get_aps = commands.getoutput('snmptable -Cf SEP -CB -CH -v2c -Os -c %s %s WLSX-WLAN-MIB::wlsxWlanAPTable' % (RO_string, WLC))

# turn get_aps_clean into a list
    results = get_aps.splitlines()

# loop through the list and print the items we are interested in
# if you'd like additional info in your files, modify the 'writtenlines' variable below
    for interesting in results:
        # turn each field of the list into a value. Note we need to specify
        # our own seperator (SEP) b/c white-space is not consistent enough (ie if spaces exist in field values)
        values = interesting.split("SEP")
        # decide what we are interested in writing to the file (check AIRESPACE mib for all available options)
        writtenlines = 'ip=' +values[0] + ' name=' + values[1] + ' groupname=' + values[2] + ' model=' + values[3] + ' mac=' + values[10] + ' uptime=' + values[11]+ ' location=' + values[12] + ' building=' + values[13] + ' serial=' + values[4]
	#writtenlines = " ".join(values)
        # remove the " character from the output
        writtenlines_clean = writtenlines.replace("\"", "")
        #writtenlines_clean = writtenlines###writtenlines.replace("\"", "")
        # Uncomment the following line, if you also want the script to print everything to stdout
        print writtenlines_clean
        # Write the file, including newlines
        outfile1.write(writtenlines_clean + '\n')
        #outfile1.write("\n".join(writtenlines_clean))

# Loop through the list of WLC's and call the main function for each.
for i in WLC_List:
    get_ap_data(i)
        
# close the file
outfile1.close()

