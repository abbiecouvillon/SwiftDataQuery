import astropy
import argparse
from astropy.coordinates import SkyCoord
from swifttools.swift_too import Data, TOO
from swifttools.swift_too import ObsQuery
from pandas import *


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
    for k in range(len(oq)):
        data = Data(obsid=oq[k].obsid, uvot=True, auxil=True, outdir=output+'/'+SNname+'/'+oq[0].obsid,clobber=True)

for k in range(len(SN)):
    if str(SN[k]) != 'nan':
        print("Currently processing", SN[k])
        query(SN[k])
    else:
        print('SN field empty. Skipping.')