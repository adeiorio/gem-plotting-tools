#
#
# This macro takes the name of the chamber and all the scandates from the scandates list file and produces tables for the twelve parameter of the VFAT electronics
#
#

def getcolumn(filename, column, vfat):
    f=open(filename,"r")
    lines=f.readlines()
    values=[]
    if(vfat==-1):
        for line in lines:
            values.append(line.strip().split(' ')[column])
    else:
        values = "N.A."
        for line in lines:
            if(line.strip().split('\t')[0]==vfat):
                values = line.strip().split('\t')[column]
    f.close()
    #print values
    return values

import argparse
import os,commands
import sys
usage = 'python dacScanComparison.py python dacScanComparison.py /path/to/DACscans/ --sdlist scandatelist.txt --vfat all -o /path/for/the/results/'
parser = argparse.ArgumentParser(usage)
parser.add_argument('filepath', type=str, help="File path from which input information is read until the folder with the chamber name", metavar='filepath')
parser.add_argument('--vfat', dest='vfat', type=str, default = 'none', help='')
parser.add_argument('--sdlist', dest='sdlist', type=str, default = '', help='Names of the scandate file to analyse')
parser.add_argument('-o','--outpath', dest='outpath', type=str, default = './', help='Path on the folder where the summary table will be written')
parser.add_argument('--popup', dest='popup', default=False, action='store_true') 
args = parser.parse_args()

print("Analyzing: '%s'" %args.filepath)
print("scandatelistfile: '%s'" %args.sdlist)

chamber = getcolumn(args.sdlist,0,-1)[0]
scandates = getcolumn(args.sdlist,1,-1)
vfats = []

if args.vfat=="none":
    print("Please pass the name of the vfat(s) you want to analyse with the option --vfat")
    sys.exit()
elif args.vfat=="all":
    for x in range(0,24):
        vfats.append(str(x))
else:
    for vf in (args.vfat).split(","):
        vfats.append(vf)
#print vfats

parameters = ["BIAS_CFD_DAC_1", "BIAS_CFD_DAC_2", "BIAS_PRE_I_BIT", "BIAS_PRE_I_BLCC", "BIAS_PRE_I_BSF", "BIAS_PRE_VREF", "BIAS_SD_I_BDIFF", "BIAS_SD_I_BFCAS", "BIAS_SD_I_BSF", "BIAS_SH_I_BDIFF", "BIAS_SH_I_BFCAS", "HYST"]

for vfat in vfats:
    table = []
    table.append(parameters)
    outpath = args.outpath+"/"+str(chamber)
    if not(os.path.exists(outpath)):
        os.makedirs(outpath)
    outfile = outpath+"/SummaryTable_VFAT"+str(vfat)+".txt"
    of = open(outfile, "w")
    #print str(scandate)
    for scandate in scandates:
        par_path = args.filepath+"/"+str(chamber)+"/dacScans/"+str(scandate)+"/"
        scanparam = []
        for par in parameters:
            scanparam.append(getcolumn(par_path+"NominalValues-CFG_"+par+".txt", 1, vfat))
        table.append(scanparam)
    of.write("VFAT "+vfat+"\n")
    if(args.popup):
        print("DAC_PARAM\t"+"\t".join([str(scandate) for scandate in scandates]))
    of.write("DAC_PARAM\t"+"\t".join([str(scandate) for scandate in scandates])+"\n")
    if(args.popup):
        print('\n'.join(' '.join(map(str,sl)) for sl in zip(*table)))
    of.write('\n'.join('\t'.join(map(str,sl)) for sl in zip(*table)))
    of.close()
