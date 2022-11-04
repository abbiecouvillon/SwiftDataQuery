import astropy
import argparse
from astropy.coordinates import SkyCoord
from swifttools.swift_too import Data, TOO
from swifttools.swift_too import ObsQuery
from pandas import *
'''
READ BEFORE RUNNING
When running this code, put it in the same folder as the csv youre readong from.
run from console the following line:

python3 SNQuery.py snlist.csv ~/Downloads

Where snlist.csv should be the name of the csv and ~/Downloads is the folder that you want all the downloads to go to.
'''

# Use command line to grab arguments from the user
parser = argparse.ArgumentParser(description='automate file grab')
parser.add_argument('csvfile', metavar='csvfile',
                    type=str, nargs=1, help='csv file to read supernovae from')
parser.add_argument('outputdir', metavar='outputdir',
                    type=str, nargs=1, help='directory where you want to download the data to')
args = parser.parse_args()
data = read_csv(args.csvfile[0])
output = args.outputdir[0]
print(output)
SN = data['SNname'].tolist()
too = TOO()


def query(SNname): #query needs to have a download of uvot and auxil data with a range of 8 arcminutes
    coords = astropy.coordinates.get_icrs_coordinates(SNname)
    oq = ObsQuery(skycoord=coords, radius=8/60)
    print(oq)
    for k in range(len(oq)):
        data = Data(obsid=oq[k].obsid, uvot=True, auxil=True, outdir=output+'/'+SNname+'/'+oq[k].obsid,clobber=True)
        print(output+'/'+SNname+'/'+oq[k].obsid)

print(SN)
for k in range(len(SN)-1):
    if str(SN[k]) != 'nan':
        print("Currently processing", SN[k])
        query(SN[k])
    else:
        print('SN field empty. Skipping.')