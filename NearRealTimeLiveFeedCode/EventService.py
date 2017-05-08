#Greg Smoczyk USGS 5/1/2017
#This script processes events for the monthly significant event GIS feed. The script is run on our GIS servers every 15 minutes through a scheduled Windows task.
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
arcpy.env.overwriteOutput=True
start = time.time()
arcpy.CheckOutExtension("Spatial")

#Set up MXD directory and file names
MXDLocation = r"path\\to\\MXDdirectory"
connectionFile = r"path\\to\\DatabaseConnectionFile"
mxdname = "event.mxd"
contourmxdname = "event.mxd"
newdir = "path\\to\\data\\directory"

#URL for JSON feed that we use to get event data
FEEDURL = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson'
#Code from Libcomcat to retrieve event data for significant Earthquakes
def getEvents(magnitude=1.0,significance=0,product='origin',lastUpdate=2678000):
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
        # The events are being looped over at this point, code below gets the JSON file and saves it
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
        
        #### Code below parses the JSON file, gets URL for shapefiles, then saves them to a directory
        with open(fileloc) as data_file: 
                data = json.load(data_file)
                magnitude = data["properties"]["mag"]
                depth = data["properties"]["products"]["origin"][0]["properties"]["depth"]
                eventdate = data["properties"]["products"]["origin"][0]["properties"]["eventtime"]
                lat = data["properties"]["products"]["origin"][0]["properties"]["latitude"]
                lon = data["properties"]["products"]["origin"][0]["properties"]["longitude"]
                location = data["properties"]["place"]
                status = data["properties"]["status"]
                mmi = data["properties"]["mmi"]
                eventtime = float(str(data["properties"]["time"])[:-3])
                updatedtime = float(str(data["properties"]["updated"])[:-3])
                updateinterval = str(int(updatedtime - eventtime))
                daysold = round((((time.time() - eventtime)/ 60)/60)/24, 2)
                
                if arcpy.Exists(newdir + "\\EventTemp.gdb\\" + net + eventid) == False:
                    print "New Event- " + net + eventid + " -Being Added!"
                    update = 1
                    GDBdir = newdir + "\\EventTemp.gdb"
                    sr = arcpy.SpatialReference(3785)
                    geo = arcpy.SpatialReference(4326)
                    eventname = net + eventid
                    workspace = r"path\\to\\data\\directory"
                    arcpy.CreateFeatureclass_management(GDBdir, eventname, "POINT", "", "", "", geo)
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "latitude", "FLOAT", "", "", "", "latitude", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "longitude", "FLOAT", "", "", "", "longitude", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "magnitude", "FLOAT", "", "", "", "magnitude", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "depth", "FLOAT", "", "", "", "depth", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "mmi", "FLOAT", "", "", "", "mmi", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "location", "TEXT", "", "", 150, "location", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "status", "TEXT", "", "", 25, "status", "NULLABLE", "NON_REQUIRED")
                    arcpy.AddField_management(GDBdir + "\\" + eventname, "updateinterval", "long", "", "", "", "updateinterval", "NULLABLE", "NON_REQUIRED")
                    cursor = arcpy.da.InsertCursor(GDBdir + "\\" + eventname, ["SHAPE@", "eventid", "latitude", "longitude", "magnitude", "depth", "mmi", "eventdate", "location", "status", "updateinterval"])
                    point = arcpy.Point(lon, lat)
                    cursor.insertRow([point, eventname, lat, lon, magnitude, depth, mmi, eventdate, location, status, updateinterval])
                    del cursor

                #If an update has occurred to an existing feature class it will be remade below!
                arcpy.env.workspace = newdir + "\\EventTemp.gdb\\"
                GDBdir = newdir + "\\EventTemp.gdb"
                sr = arcpy.SpatialReference(3785)
                geo = arcpy.SpatialReference(4326)
                eventname = net + eventid
                ev = arcpy.ListFeatureClasses('*' + eventname + '*')
                for fc in ev:
                    with arcpy.da.SearchCursor(fc, "updateinterval") as cur:
                        li = []
                        for row in cur:
                            li.append(row[0])
                            if str(max(li)) <> updateinterval:
                                print "Event: " + eventname + " Version Update!"
                                update = 1                                
                                arcpy.CreateFeatureclass_management(GDBdir, eventname, "POINT", "", "", "", geo)
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "eventid", "TEXT", "", "", 50, "eventid", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "latitude", "FLOAT", "", "", "", "latitude", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "longitude", "FLOAT", "", "", "", "longitude", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "magnitude", "FLOAT", "", "", "", "magnitude", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "depth", "FLOAT", "", "", "", "depth", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "mmi", "FLOAT", "", "", "", "mmi", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "eventdate", "TEXT", "", "", 50, "eventdate", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "location", "TEXT", "", "", 150, "location", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "status", "TEXT", "", "", 25, "status", "NULLABLE", "NON_REQUIRED")
                                arcpy.AddField_management(GDBdir + "\\" + eventname, "updateinterval", "long", "", "", "", "updateinterval", "NULLABLE", "NON_REQUIRED")
                                cursor = arcpy.da.InsertCursor(GDBdir + "\\" + eventname, ["SHAPE@", "eventid", "latitude", "longitude", "magnitude", "depth", "mmi", "eventdate", "location", "status", "updateinterval"])
                                point = arcpy.Point(lon, lat)
                                cursor.insertRow([point, eventname, lat, lon, magnitude, depth, mmi, eventdate, location, status, updateinterval])
                    del cur

    #If event is more than 1 month old, delete it
    env.workspace = newdir + "\\EventTemp.gdb\\"
    ev = arcpy.ListFeatureClasses()
    for fc in ev:
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
            arcpy.Delete_management(newdir + "\\EventTemp.gdb\\" + n)
            print "Event: " + n + " Deleted!"
        del cursor

    GDBdirnew = newdir + "\\Event.gdb"
    if update == 1:
        events = arcpy.ListFeatureClasses()
        arcpy.Delete_management(GDBdirnew + "\\events")
        arcpy.Merge_management(events, GDBdirnew + "\\events")
        arcpy.AddSpatialIndex_management("path\\to\\TempEventGDB")


        #Moves updated GDB to "Live" GDB for GIS Service
        for files in os.listdir("path\\to\\TempEventGDB"):
            if files[-5:].lower() != '.lock':
                shutil.copy2(os.path.join("path\\to\\TempEventGDB", files), os.path.join("path\\to\\ProdEventGDB", files))
        print "Data Migrated to Live Feed"

jfiles = glob.glob("path\\to\\TempDir\\*.json")
for f in jfiles:
    os.remove(f)
    print f + " Removed!"

servename = "hostname:6080"
shakeserviceURL = "http://" + servename + "/arcgis/rest/services/event/MapServer"
adminserviceURL = "http://" + servename + "/arcgis/admin/services/event.MapServer"
shaker = requests.get(shakeserviceURL, auth=('<user>', '<password>'))
shakeexists = shaker.status_code
print shakeexists
if shakeexists == 200:
    print "Previous Service Exists"
    gtUrl = "http://" + servename + "/arcgis/admin/generateToken"
    gtValues = {'username' : '<user>',
    'password' : '<password>',
    'client' : 'ip',
    'ip' : '<server IP>',
    'f' : 'json' }
    gtData = urllib.urlencode(gtValues)
    gtRequest = urllib2.Request(gtUrl, gtData)
    gtResponse = urllib2.urlopen(gtRequest)
    gtJson = json.load(gtResponse)
    token = gtJson['token']
    payload = {'token': token, 'f': 'json'}
    shakeurlstop = adminserviceURL + "/stop"
    requests.post(shakeurlstop + "token=" + token + "&f=json")
    shakeurlstart = adminserviceURL + "/start"
    requests.post(shakeurlstart + "token=" + token + "&f=json")
    print "Event Service Restarted"
print "Processing time:" + str(((time.time() - start)/60))
