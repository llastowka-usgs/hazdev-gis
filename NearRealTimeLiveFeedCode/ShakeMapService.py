#Greg Smoczyk USGS 05/01/2017
#This script processes events for the monthly significant event ShakeMap GIS feed. The script is run on our GIS servers every 15 minutes through a scheduled Windows task.
#arcpy is an Esri module for processing geospatial data via Python using ArcGIS software
import arcpy
from arcpy import env
import argparse
from pprint import pprint
import sys
import os
import os.path
import urllib
import urllib2
import json
import subprocess
import zipfile
import time
import shutil
import glob
#requests is a Python module to handle http requests more seamlessly
import requests
import re
import time, datetime, traceback, string
from array import array
import xml.dom.minidom as DOM
from xml.dom.minidom import parse, parseString
#arcpy.sa denotes the use of the Spatial Analyst toolbox for ArcGIS
from arcpy.sa import *
from datetime import datetime,timedelta
start = time.time()
arcpy.CheckOutExtension("Spatial")
#Set up MXD directory and file names
MXDLocation = r"path\\to\\MXDdirectory"
connectionFile = r"path\\to\\ConnectionFile"
mxdname = "monthly.mxd"
contourmxdname = "monthly_contours.mxd"
newdir = "path\\to\\data\\directory"

#URL for JSON feed that we use to get ShakeMap data
FEEDURL = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson'
#Code from Libcomcat to retrieve ShakeMap data for significant Earthquakes
def getEvents(magnitude=1.0,significance=0,product='shakemap',lastUpdate=2678000):
    """
    Return a list of earthquake event urls that meet the conditions set above.
    Inputs:

     * magnitude: Event magnitude (OR condition with significance)
     * significance: Event significance (integer score assembled from weighting magnitude, PAGER alert level, Max MMI, etc.)
     * lastUpdateDelta: Only retrieve events that have been updated in the past lastUpdate minutes.
     * product: Only retrieve events that have this product type associated with them.
    """
    fh = urllib2.urlopen(FEEDURL)
    data = fh.read()
    fh.close()
    jdict = json.loads(data)
    eventurls = []
    tnow = datetime.utcnow()
    for event in jdict['features']:
        eurl = event['properties']['detail']
        emag = event['properties']['mag']
        esig = event['properties']['sig']
        etypes = event['properties']['types'].split(',')[1:-1]
        eupdate = datetime.utcfromtimestamp(event['properties']['updated']/1000)
        hasproduct = product in etypes
        if not hasproduct:
            continue
        if eupdate < tnow - timedelta(seconds=60*lastUpdate):
            continue
        eventurls.append(eurl)
    return eventurls

if __name__ == '__main__':
    eventurls = getEvents(significance=500)
    update = 0
    for eventurl in eventurls:
        #The events are being looped over at this point, code below gets the JSON file and saves it
        t = eventurl.split("detail/")[1]
        net = t[:2]          
        eventid = t.split(".geojson")[0][2:]
        newdir = "path\\to\\data\\directory"
        req = requests.get(eventurl)
        jsonf = req.text
        fileloc = newdir + "\\" + net + eventid + ".json"
        f = open(fileloc,'w')
        print >>f,jsonf
        f.close()

        #Code below parses the JSON file, gets URL for shapefiles, then saves them to a directory
        with open(fileloc) as data_file: 
                data = json.load(data_file)
                #Code below gets shapefile
                shapeurl = data["properties"]["products"]["shakemap"][0]["contents"]["download/shape.zip"]["url"]             
                open(newdir + '\shape.zip', 'wb').write(urllib.urlopen(shapeurl).read())
                with zipfile.ZipFile(newdir + '\shape.zip', "r") as z:
                    z.extractall(newdir)
                    z.close()
                os.remove(newdir + '\shape.zip')
                version = data["properties"]["products"]["shakemap"][0]["properties"]["version"]
                eventdate = data["properties"]["products"]["origin"][0]["properties"]["eventtime"]
                stationurl = data["properties"]["products"]["shakemap"][0]["contents"]["download/stationlist.json"]["url"]
                open(newdir + '\\' + net + eventid + 'stations.json', 'wb').write(urllib.urlopen(stationurl).read())
                with open(newdir + '\\' + net + eventid + 'stations.json') as stations:
                    s = json.load(stations)
                    nu = 0
                    if len(s["features"]) > 0:
                        f = open(newdir + "\\" + net + eventid + "stations.csv",'w')
                        f.writelines("StationCode, latitude, longitude, regressiondist_km, intensity, Channel1Code, PGV_cm_sec1, PGA_percentG1, PSA0_3sec_percentG1, PSA1_0sec_percentG1, PSA3_0sec_percentG1, Channel2Code, PGV_cm_sec2, PGA_percentG2, PSA0_3sec_percentG2, PSA1_0sec_percentG2, PSA3_0sec_percentG2, Channel3Code, PGV_cm_sec3, PGA_percentG3, PSA0_3sec_percentG3, PSA1_0sec_percentG3, PSA3_0sec_percentG3, netcode, eventid\n")
                        #Row below is inserted so that the merge creates text fields rather than floating point fields.  There are values of 'None' dispersed throughout the station data which cause the merge to choke without this....
                        f.writelines("something, 0, 0, 1000, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, something, us77777gms\n")
                        while nu < len(s["features"]):
                            f.write(str(s["features"][nu]["id"]))
                            f.write(", ")
                            f.write(str(s["features"][nu]["geometry"]["coordinates"][1]))
                            f.write(", ")
                            f.write(str(s["features"][nu]["geometry"]["coordinates"][0]))
                            f.write(", ")
                            f.write(str(s["features"][nu]["properties"]["distance"]))
                            f.write(", ")
                            f.write(str(s["features"][nu]["properties"]["intensity"]))
                            f.write(", ")
                            loop = 0
                            while loop <=  len(s["features"][nu]["properties"]["channels"]) - 1  and loop < 3:
                                if len(s["features"][nu]["properties"]["channels"]) - 1 == 0:
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 0:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 1:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 2:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 3:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 4:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 5:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][4]["value"]))
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(",")
                                if len(s["features"][nu]["properties"]["channels"]) - 1 == 1:
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 0:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 1:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 2:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 3:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 4:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 5:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][4]["value"]))
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(",")
                                if len(s["features"][nu]["properties"]["channels"]) - 1 >= 2:
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 0:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(", ")
                                        f.write(" None")
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 1:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 2:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 3:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 4:
                                        pgv = " None"
                                        pga = " None"
                                        psa03 = " None"
                                        psa10 = " None"
                                        psa30 = " None"
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pgv":
                                            pgv = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "pga":
                                            pga = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa03":
                                            psa03 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa10":
                                            psa10 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])

                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"])
                                        if str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["name"]) == "psa30":
                                            psa30 = str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"])
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(pgv)
                                        f.write(", ")
                                        f.write(pga)
                                        f.write(", ")
                                        f.write(psa03)
                                        f.write(", ")
                                        f.write(psa10)
                                        f.write(", ")
                                        f.write(psa30)
                                        f.write(",")
                                    if len(s["features"][nu]["properties"]["channels"][loop]["amplitudes"]) == 5:
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["name"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][1]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][0]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][2]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][3]["value"]))
                                        f.write(", ")
                                        f.write(str(s["features"][nu]["properties"]["channels"][loop]["amplitudes"][4]["value"]))
                                        f.write(",")
                                loop = loop + 1
                            if str(s["features"][nu]["id"])[:5] == 'DYFI.' or str(s["features"][nu]["id"])[:5] == 'CIIM.' or str(s["features"][nu]["id"])[:9] == 'INTENSITY.' or str(s["features"][nu]["id"])[:4] == 'MMI.':
                                f.write("0")
                                f.write(", ")
                            else:
                                f.write("1")
                                f.write(", ")
                            f.write(net + eventid)
                            f.write("\n")
                            nu = nu + 1
                        f.close()

                if os.path.isfile(newdir + "\\mi.lyr"):
                    mmi = "mi"
                else:
                    mmi = "mmi"

                eventtime = float(str(data["properties"]["time"])[:-3])

                daysold = round((((time.time() - eventtime)/ 60)/60)/24, 2)
                print daysold
                print net + eventid
                if arcpy.Exists(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "mmicontours") == False:
                    
                    print "New Event- " + net + eventid + " -Being Added!"
                    update = 1
                    rasterdir = newdir
                    shapedir = newdir
                    kmldir = newdir
                    GDBdir = newdir + "\\ShakeMapTemp.gdb"
                    if mmi == "mi":
                        mmilayername = MXDLocation + "\\mi.lyr"
                    else:
                        mmilayername = MXDLocation + "\\mmi.lyr"
                    kmllayername = MXDLocation + "\\intensitykml.lyr"
                    rastermmi = "\\mi.fit"
                    sr = arcpy.SpatialReference(3785)
                    geo = arcpy.SpatialReference(4326)
                    arcpy.CopyFeatures_management(newdir + "\\" + mmi + ".shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "mmicontours")
                    arcpy.CopyFeatures_management(newdir + "\\pga.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgacontours")
                    arcpy.CopyFeatures_management(newdir + "\\pgv.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgvcontours")
                    arcpy.CopyFeatures_management(newdir + "\\psa03.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa03contours")
                    arcpy.CopyFeatures_management(newdir + "\\psa10.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa10contours")
                    arcpy.CopyFeatures_management(newdir + "\\psa30.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa30contours")

                    #print os.path.isfile(newdir + "\\" + net + eventid + "stations.csv")
                    if os.path.isfile(newdir + "\\" + net + eventid + "stations.csv") == True:
                        arcpy.MakeXYEventLayer_management(newdir + '\\' + net + eventid + 'stations.csv', "longitude", "latitude", net + eventid + "stations", geo)
                        arcpy.CopyFeatures_management(net + eventid + "stations", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "stations")

                    eventname = net + eventid
                    workspace = r"E:\GIS\eq\ShakeMap"
                    mmiFC = rasterdir + "\\" + rastermmi

                    #Following code added to save time if the eventid and version are the same as the last update
                    #Add and populate eventid, version, and eventage fields to MMI FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "version", "'" + version + "'", "PYTHON_9.3")
                    print version
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                    #Add and populate eventid and version fields to PGA FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "version", "'" + version + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                    #Add and populate eventid and version fields to PGV FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "version", "'" + version + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                    #Add and populate eventid and version fields to PSA03 FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "version", "'" + version + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                    #Add and populate eventid and version fields to PSA10 FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "version", "'" + version + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                    #Add and populate eventid and version fields to PSA30 FC
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "version", "'" + version + "'", "PYTHON_9.3")
                    arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                env.workspace = newdir + "\\ShakeMapTemp.gdb\\"
                
                w = "*" + net + eventid + "mmicontours*"        

                sr = arcpy.SpatialReference(3785)
                geo = arcpy.SpatialReference(4326)           
                fea = arcpy.ListFeatureClasses(w)
                for fc in fea:
                    n = fc[:10]
                    with arcpy.da.SearchCursor(fc, "version") as cursor:
                        li = []
                        for row in cursor:
                            li.append(row[0])
                            if max(li) <> int(version):
                                print "Event: " + net + eventid + " Version Update!"
                                update = 1

                                with arcpy.da.SearchCursor(fc, "eventdate", where_clause="OBJECTID = 1") as cur:
                                    for r in cur:
                                        eventdate = r[0]
                                
                                #Remove files for events that have updates available
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "stations")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "mmicontours")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgacontours")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgvcontours")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa03contours")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa10contours")
                                arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa30contours")
                                rasterdir = newdir
                                shapedir = newdir
                                kmldir = newdir
                                GDBdir = newdir + "\\ShakeMapTemp.gdb"
                                if mmi == "mi":
                                    mmilayername = MXDLocation + "\\mi.lyr"
                                else:
                                    mmilayername = MXDLocation + "\\mmi.lyr"
        
                                kmllayername = MXDLocation + "\\intensitykml.lyr"
                                rastermmi = "\\mi.fit"

                                if os.path.isfile(newdir + "\\" + net + eventid + "stations.csv") == True:
                                    arcpy.MakeXYEventLayer_management(newdir + '\\' + net + eventid + 'stations.csv', "longitude", "latitude", net + eventid + "stations", geo)
                                    arcpy.CopyFeatures_management(net + eventid + "stations", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "stations")

                                arcpy.CopyFeatures_management(newdir + "\\" + mmi + ".shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "mmicontours")
                                arcpy.CopyFeatures_management(newdir + "\\pga.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgacontours")
                                arcpy.CopyFeatures_management(newdir + "\\pgv.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "pgvcontours")
                                arcpy.CopyFeatures_management(newdir + "\\psa03.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa03contours")
                                arcpy.CopyFeatures_management(newdir + "\\psa10.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa10contours")
                                arcpy.CopyFeatures_management(newdir + "\\psa30.shp", newdir + "\\ShakeMapTemp.gdb\\" + net + eventid + "psa30contours")

                                #Define spatial references to be used in this script 
                                sr = arcpy.SpatialReference(3785)
                                geo = arcpy.SpatialReference(4326)
                                eventname = net + eventid
                                workspace = r"E:\GIS\eq\ShakeMap"
                                mmiFC = rasterdir + "\\" + rastermmi       

                                #This also added to save time if the eventid and version are the same as the last update
                                #Add and populate eventid, version, and eventage fields to MMI FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "version", "'" + version + "'" , "PYTHON_9.3")
                                print version
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "mmicontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "mmicontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                                #Add and populate eventid and version fields to PGA FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "version", "'" + version + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgacontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgacontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                                #Add and populate eventid and version fields to PGV FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "version", "'" + version + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "pgvcontours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                                #Add and populate eventid and version fields to PSA03 FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "version", "'" + version + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa03contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa03contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                                #Add and populate eventid and version fields to PSA10 FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "version", "'" + version + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa10contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa10contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

                                #Add and populate eventid and version fields to PSA30 FC
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "eventid", "'" + eventname + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "version", "SHORT", "", "", "", "version", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "version", "'" + version + "'", "PYTHON_9.3")
                                arcpy.AddField_management(GDBdir + "\\" + eventname + "psa30contours", "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.CalculateField_management(GDBdir + "\\" + eventname + "psa30contours", "eventdate", "'" + eventdate + "'" , "PYTHON_9.3")

        data_file.close()
    
    #If event is more than 1 month old, delete it
    env.workspace = newdir + "\\ShakeMapTemp.gdb\\"
    micont = arcpy.ListFeatureClasses("*mmicontours*")
    for fc in micont:
        n = fc[:10]
        with arcpy.da.SearchCursor(fc, "eventdate") as cursor:
            li = []
            for row in cursor:
                li.append(row[0])

        d = datetime.now()
        t = (d - datetime(int(max(li)[:4]), int(max(li)[5:7]), int(max(li)[8:10]), int(max(li)[11:13]), int(max(li)[14:16]), int(max(li)[17:19]))).total_seconds()
        daysold = ((t/60)/60)/24
        if daysold > 29.97:
            update = 1
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "mmicontours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "pgacontours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "pgvcontours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "psa03contours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "psa10contours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "psa30contours")
            arcpy.Delete_management(newdir + "\\ShakeMapTemp.gdb\\" + n + "stations")
            print "Event: " + n + " Deleted!"

    GDBdirnew = newdir + "\\ShakeMap.gdb"
    if update == 1:
        micont = arcpy.ListFeatureClasses("*mmicontours*")
        pgacont = arcpy.ListFeatureClasses("*pgacontours*")
        pgvcont = arcpy.ListFeatureClasses("*pgvcontours*")
        psa03cont = arcpy.ListFeatureClasses("*psa03contours*")
        psa10cont = arcpy.ListFeatureClasses("*psa10contours*")
        psa30cont = arcpy.ListFeatureClasses("*psa30contours*")
        stations = arcpy.ListFeatureClasses("*stations*")
        arcpy.Delete_management(GDBdirnew + "\\mi")
        arcpy.Merge_management(micont, GDBdirnew + "\\mi")
        arcpy.AddSpatialIndex_management("Path\\to\\TempShakeMapGDB\\mi")
        print "MI Spatial Index Recreated"
        
        #Code below updates PARAMVALUE field null values with VALUE field data because some regions don't have consistent field names(Alaska, Washington) 
        lst = arcpy.ListFields("Path\to\TempShakeMapGDB\mi")
        for f in lst:
            if f.name == "VALUE":
                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\mi", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                            row[0] = row[1]
                            cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\mi", "VALUE")


        arcpy.Delete_management(GDBdirnew + "\\pga")
        arcpy.Merge_management(pgacont, GDBdirnew + "\\pga")
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\pga")
        print "PGA Spatial Index Recreated"

        lst = arcpy.ListFields("\Path\to\TempShakeMapGDB\\pga")
        for f in lst:
            if f.name == "VALUE":
                
                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\pga", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                            row[0] = row[1]
                            cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\pga", "VALUE")

        arcpy.Delete_management(GDBdirnew + "\\pgv")
        arcpy.Merge_management(pgvcont, GDBdirnew + "\\pgv")
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\pgv")
        print "PGV Spatial Index Recreated" 

        lst = arcpy.ListFields("\Path\to\TempShakeMapGDB\pgv")
        for f in lst:
            if f.name == "VALUE":

                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\pgv", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                                row[0] = row[1]
                                cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\pgv", "VALUE")

        arcpy.Delete_management(GDBdirnew + "\\psa03")
        arcpy.Merge_management(psa03cont, GDBdirnew + "\\psa03")
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\psa03")
        print "PSA03 Spatial Index Recreated"

        lst = arcpy.ListFields("\Path\to\TempShakeMapGDB\psa03")
        for f in lst:
            if f.name == "VALUE": 

                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\psa03", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                            row[0] = row[1]
                            cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\psa03", "VALUE")

        arcpy.Delete_management(GDBdirnew + "\\psa10")
        arcpy.Merge_management(psa10cont, GDBdirnew + "\\psa10")
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\psa10")
        print "PSA10 Spatial Index Recreated"

        lst = arcpy.ListFields("\Path\to\TempShakeMapGDB\psa10")
        for f in lst:
            if f.name == "VALUE":

                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\psa10", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                            row[0] = row[1]
                            cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\psa10", "VALUE")

        arcpy.Delete_management(GDBdirnew + "\\psa30")
        arcpy.Merge_management(psa30cont, GDBdirnew + "\\psa30")
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\psa30")
        print "PSA30 Spatial Index Recreated"

        lst = arcpy.ListFields("\Path\to\TempShakeMapGDB\psa30")
        for f in lst:
            if f.name == "VALUE":

                with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\psa30", ["PARAMVALUE", "VALUE"]) as cursor:
                    for row in cursor:
                        if row[0] == None:
                            row[0] = row[1]
                            cursor.updateRow(row)
                arcpy.DeleteField_management("\Path\to\TempShakeMapGDB\psa30", "VALUE")




        arcpy.Delete_management(GDBdirnew + "\\stations")
        arcpy.Merge_management(stations, GDBdirnew + "\\stations")
        with arcpy.da.UpdateCursor("\Path\to\TempShakeMapGDB\stations", ["StationCode"]) as cursor:
            for row in cursor:
                if row[0] == 'something':
                    cursor.deleteRow()
        arcpy.AddSpatialIndex_management("\Path\to\TempShakeMapGDB\stations")
        print "Stations Spatial Index Recreated"

        servename = "hostname:6080"
        shakeserviceURL = "http://" + servename + "/arcgis/rest/services/ShakeMap/MapServer"
        shaker = requests.get(shakeserviceURL, auth=('<user>', '<password>'))
        shakeexists = shaker.status_code
        print shakeexists
        if shakeexists == 200:
            print "Previous Service Exists"
            gtUrl = "http://" + servename + "/arcgis/admin/generateToken"
            gtValues = {'username' : '<user>',
            'password' : '<password>',
            'client' : 'ip',
            'ip' : '<GIS Server IP>',
            'f' : 'json' }
            gtData = urllib.urlencode(gtValues)
            gtRequest = urllib2.Request(gtUrl, gtData)
            gtResponse = urllib2.urlopen(gtRequest)
            gtJson = json.load(gtResponse)
            token = gtJson['token']
            payload = {'token': token, 'f': 'json'}
            shakeurlstop = shakeserviceURL + "/stop"
            print shakeurlstop + "token=" + token + "&f=json"
            requests.post(shakeurlstop + "token=" + token + "&f=json")

            #Moves updated GDB to "Live" GDB for GIS Service
            for files in os.listdir("\Path\to\TempShakeMapGDB"):
                if files[-5:].lower() != '.lock':
                    shutil.copy2(os.path.join("\Path\to\TempShakeMapGDB", files), os.path.join("\Path\to\LiveShakeMapGDB", files))
            print "Data Migrated to Live Feed"
  
            shakeurlstart = shakeserviceURL + "/start"
            print shakeurlstart + "token=" + token + "&f=json"
            requests.post(shakeurlstart + "token=" + token + "&f=json")
            print "ShakeMap Service Restarted"

#Remove all processed files
jfiles = glob.glob("Path\\to\\DataDir\\*.json")
for f in jfiles:
    os.remove(f)
    print f + " Removed!"
cfiles = glob.glob("Path\\to\\DataDir\\*.csv")
for f in cfiles:
    os.remove(f)
    print f + " Removed!"
print "Processing time:" + str(((time.time() - start)/60))
