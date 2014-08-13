#!/usr/bin/python

#######
# this is a script to get the currently joined Access Points, and other useful info from a WLC.
# Replace the RO_String below, with your SNMP RO community.
# Originally created on July 18 2013 by Mike Albano
# Severely modified on Aug 8 2014 by Daniel Klopp
########

import os, sys, commands
import getopt

RETCODE_INVALID_OPTION=7
RETCODE_SUCCESS=0

# Define your snmp RO String
RO_string =''
# Define your WLC's by IP:
WLC_List = ['']

# Minor exception handling
try:
  open('/tmp/wlc_aps', 'w')
except:
  print sys.stderr, "Couldn't open file"
  sys.exit(1)

# Define the output files
outfile1 = open("/tmp/wlc_aps", "w")

def print_help():
    SP="   "
    print(sys.argv[0] + " [OPTIONS]")
    print(SP + "-h | --help             " + "print this help")
    print(SP + "-v | --verbose          " + "print this help")
    print(SP + "-a | --addresses        " + "print this help")
    print(SP + "-m | --mib              " + "the mib object")
    print(SP + "-t | --mib-table        " + "mib table object")
    print(SP + "-c | --community-string " + "SNMP community string (password)")
    print(SP + "-f | --file             " + "Output file, use - for stdout, default /tmp/wlc_aps")
    print(SP + "-o | --objects          " + "print objects of table, default is print all, use numbers for each column")

def parse_opts():
    opt_dict={}
    opt_dict['verbose'] = false
    opt_dict['file'] = "/tmp/wlc_aps"
    opt_dict['objects'] = None
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hva:m:t:c:f:", ["help", "verbose", "addresses", "mib", "mib-table", "community-string", "file", "mib-table"])
    except getopt.GetoptError:
        print ("Invalid options")
        print_help()
        sys.exit(RETCODE_INVALID_OPTION)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit(RETCODE_SUCCESS)
        elif opt in ('-a','--addresses'):
            addresses=[]
            for address in arg.split(','):
                addresses.append(address)
            if not addresses:
                print("At least one WLC address is required")
                sys.exit(RETCODE_INVALID_OPTION)
            else:
                opt_dict['addresses'] = addresses
        elif opt in ('-m', '--mib'):
            opt_dict['mib']=arg
        elif opt in ('-t', '--mib-table'):
            opt_dict['mib-table'] = arg
        elif opt in ('-v', '--verbose'):
            opt_dict['verbose'] = true
        elif opt in ('-c', '--community-string'):
            opt_dict['password'] = arg
        elif opt in ('-f','--file'):
            opt_dict['output'] = arg
        elif opt in ('-o', '--objects'):
            opt_dict['objects'] = arg.split(',')
        else:
            print_help()
            sys.exit(RETCODE_INVALID_OPTION)




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

