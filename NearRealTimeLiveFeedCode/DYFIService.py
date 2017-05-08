#Greg Smoczyk USGS 05/01/2017
#This script processes events for the monthly significant event DYFI GIS feed. The script is run on our GIS servers every 15 minutes through a scheduled Windows task.
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
import xml.etree.ElementTree as ET
#arcpy.sa denotes the use of the Spatial Analyst toolbox for ArcGIS
from arcpy.sa import *
from datetime import datetime,timedelta

start = time.time()

arcpy.CheckOutExtension("Spatial")
#Set up MXD directory and file names
MXDLocation = r"path\to\location"
#Reference location of DB connection file
connectionFile = r"path\to\location"
mxdname = "monthly.mxd"
contourmxdname = "monthly_contours.mxd"
newdir = "path\\to\\data\\directory"

update = 0

#Enable GDB file overwrite by default
arcpy.env.overwriteOutput = True

#URL for JSON feed that we use to get DYFI data
FEEDURL = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson'

#Code from Libcomcat to retrieve DYFI data for given Earthquakes, in this case "significant quakes" with DYFI responses
def getEvents(magnitude=1.0,significance=0,product='dyfi',lastUpdate=2678000):
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
        newdir = "path\to\data\dir"
        req = requests.get(eventurl)
        jsonf = req.text
        fileloc = newdir + "\\" + net + eventid + ".json"
        f = open(fileloc,'w')

        print >>f,jsonf
        f.close()
        # Code below parses the JSON file, gets URL for shapefiles, then saves them to a directory
        with open(fileloc) as data_file:
                update = 0
                data = json.load(data_file)
                eventtime = float(str(data["properties"]["time"])[:-3])
                eventresponses = data["properties"]["felt"]
                daysold = round((((time.time() - eventtime)/ 60)/60)/24, 2)

                edate = data["properties"]["products"]["dyfi"][0]["properties"]["eventtime"]
                edate = edate.replace('T', ' ')[:-5]
                #Checks to see if the number of responses for each event has changed. If it has, the update flag is set to 1
                env.workspace = newdir + "\\DYFITemp.gdb\\"
                w = "*" + net + eventid + "1kpoly*"        
                fea = arcpy.ListFeatureClasses(w)
                for fc in fea:
                    with arcpy.da.SearchCursor(fc, "eventresponses") as cursor:
                        li = []
                        for row in cursor:
                            li.append(row[0])
                            if max(li) != int(eventresponses):
                                update = 1
                #Code below updates events that already exist and have new responses
                #Note that 1km and 10km polygons are downloaded for all significant events
                #1km processing
                if arcpy.Exists(newdir + "\\DYFITemp.gdb\\" + net + eventid + "1kpoly") == True and update == 1:
                    print "Event: " + net + eventid + " Version Update!"
                    if "dyfi_geo_1km.geojson" not in str(data["properties"]["products"]["dyfi"][0]["contents"]):
                        print "No 1 km data for event " + net + eventid
                    else:
                        onekboxurl = data["properties"]["products"]["dyfi"][0]["contents"]["dyfi_geo_1km.geojson"]["url"]
                        open(newdir + '\\' + net + eventid + '1kbox.json', 'wb').write(urllib.urlopen(onekboxurl).read())
                        with open(newdir + '\\' + net + eventid + '1kbox.json') as onekbox:
                            onekb = json.load(onekbox)
                            f = 0
                            print "Event " + net + eventid + " contains " + str(len(onekb["features"])) + " 1k polygons"
                            if len(onekb["features"]) != 0:
                                arcpy.CreateFeatureclass_management("path//to//tempGDB//", net + eventid + "1kpoly", "POLYGON")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "boxresponses", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "cdi", "FLOAT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "distance", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventid", "TEXT", "10", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventresponses", "LONG", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventdate", "TEXT", "25", "", "", "", "NULLABLE", "REQUIRED")
                                while f < len(onekb["features"]):

                                    feature_info = [onekb["features"][f]["geometry"]["coordinates"][0]]
                                    for feature in feature_info:
                                        pnt1 = arcpy.Point(feature[0][0],feature[0][1])
                                        pnt2 = arcpy.Point(feature[1][0],feature[1][1])
                                        pnt3 = arcpy.Point(feature[2][0],feature[2][1])
                                        pnt4 = arcpy.Point(feature[3][0],feature[3][1])
                                        poly = arcpy.Polygon(arcpy.Array([pnt1,pnt2,pnt3,pnt4]))
                                    if len(onekb["features"]) != 0:
                                        cur = arcpy.da.InsertCursor("path//to//tempGDB//" + net + eventid + "1kpoly", ['boxresponses', 'cdi', 'distance', 'eventresponses', 'SHAPE@', 'eventid', 'eventdate'])

                                        res = int([onekb["features"][f]["properties"]["nresp"]][0])
                                        cdi = float([onekb["features"][f]["properties"]["cdi"]][0])
                                        dist = int([onekb["features"][f]["properties"]["dist"]][0])
                                        eid = net + eventid
                                        cur.insertRow([res, cdi, dist, eventresponses, poly, eid, edate])
                                        del cur
                                        f = f + 1
                    #10km processing
                    if "dyfi_geo_10km.geojson" not in str(data["properties"]["products"]["dyfi"][0]["contents"]):
                        print "No 10 km data for event " + net + eventid
                    else:
                        tenkboxurl = data["properties"]["products"]["dyfi"][0]["contents"]["dyfi_geo_10km.geojson"]["url"]
                        open(newdir + '\\' + net + eventid + '10kbox.json', 'wb').write(urllib.urlopen(tenkboxurl).read())

                        with open(newdir + '\\' + net + eventid + '10kbox.json') as tenkbox:
                            tenkb = json.load(tenkbox)
                            f = 0
                            print "Event " + net + eventid + " contains " + str(len(tenkb["features"])) + " 10k polygons"
                            if len(tenkb["features"]) != 0:
                                arcpy.CreateFeatureclass_management("path//to//tempGDB//", net + eventid + "10kpoly", "POLYGON")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "boxresponses", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "cdi", "FLOAT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "distance", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventid", "TEXT", "10", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventresponses", "LONG", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventdate", "TEXT", "25", "", "", "", "NULLABLE", "REQUIRED")
                                while f < len(tenkb["features"]):

                                    feature_info = [tenkb["features"][f]["geometry"]["coordinates"][0]]
                                    for feature in feature_info:
                                        pnt1 = arcpy.Point(feature[0][0],feature[0][1])
                                        pnt2 = arcpy.Point(feature[1][0],feature[1][1])
                                        pnt3 = arcpy.Point(feature[2][0],feature[2][1])
                                        pnt4 = arcpy.Point(feature[3][0],feature[3][1])
                                        poly = arcpy.Polygon(arcpy.Array([pnt1,pnt2,pnt3,pnt4]))

                                    if len(tenkb["features"]) != 0:
                                        cur = arcpy.da.InsertCursor("path//to//tempGDB//" + net + eventid + "10kpoly", ['boxresponses', 'cdi', 'distance', 'eventresponses', 'SHAPE@', 'eventid', 'eventdate'])

                                        res = int([onekb["features"][f]["properties"]["nresp"]][0])
                                        cdi = float([onekb["features"][f]["properties"]["cdi"]][0])
                                        dist = int([onekb["features"][f]["properties"]["dist"]][0])
                                        eid = net + eventid
                                        cur.insertRow([res, cdi, dist, eventresponses, poly, eid, edate])
                                        del cur
                                        f = f + 1

                ####Checks to see if there's a new event and if the .geojson file is available for that event
                #1km processing
                if arcpy.Exists("path\\to\\tempGDB\\" + net + eventid + "1kpoly") == False and "dyfi_geo_1km.geojson" in str(data["properties"]["products"]["dyfi"][0]["contents"]):     
                    update = 1                  
                    if "dyfi_geo_1km.geojson" not in str(data["properties"]["products"]["dyfi"][0]["contents"]):
                        print "No 1 km data for event " + net + eventid
                    else:
                        print "New Event- " + net + eventid + " -Being Added!"
                        onekboxurl = data["properties"]["products"]["dyfi"][0]["contents"]["dyfi_geo_1km.geojson"]["url"]
                        open(newdir + '\\' + net + eventid + '1kbox.json', 'wb').write(urllib.urlopen(onekboxurl).read())

                        with open(newdir + '\\' + net + eventid + '1kbox.json') as onekbox:
                            onekb = json.load(onekbox)
                            f = 0
                            print "Event " + net + eventid + " contains " + str(len(onekb["features"])) + " 1k polygons"
                            if len(onekb["features"]) != 0:
                                arcpy.CreateFeatureclass_management("path//to//tempGDB//", net + eventid + "1kpoly", "POLYGON")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "boxresponses", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "cdi", "FLOAT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "distance", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventid", "TEXT", "10", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventresponses", "LONG", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "1kpoly", "eventdate", "TEXT", "25", "", "", "", "NULLABLE", "REQUIRED")
                                while f < len(onekb["features"]):

                                    feature_info = [onekb["features"][f]["geometry"]["coordinates"][0]]
                                    for feature in feature_info:
                                        pnt1 = arcpy.Point(feature[0][0],feature[0][1])
                                        pnt2 = arcpy.Point(feature[1][0],feature[1][1])
                                        pnt3 = arcpy.Point(feature[2][0],feature[2][1])
                                        pnt4 = arcpy.Point(feature[3][0],feature[3][1])
                                        poly = arcpy.Polygon(arcpy.Array([pnt1,pnt2,pnt3,pnt4]))

                                    if len(onekb["features"]) != 0:
                                        cur = arcpy.da.InsertCursor("path//to//tempGDB//" + net + eventid + "1kpoly", ['boxresponses', 'cdi', 'distance', 'eventresponses', 'SHAPE@', 'eventid', 'eventdate'])

                                        res = int([onekb["features"][f]["properties"]["nresp"]][0])
                                        cdi = float([onekb["features"][f]["properties"]["cdi"]][0])
                                        dist = int([onekb["features"][f]["properties"]["dist"]][0])
                                        eid = net + eventid
                                        cur.insertRow([res, cdi, dist, eventresponses, poly, eid, edate])
                                        del cur
                                        f = f + 1

                    #10km processing
                    if "dyfi_geo_10km.geojson" not in str(data["properties"]["products"]["dyfi"][0]["contents"]):
                        print "No 10 km data for event " + net + eventid
                    else:
                        tenkboxurl = data["properties"]["products"]["dyfi"][0]["contents"]["dyfi_geo_10km.geojson"]["url"]
                        open(newdir + '\\' + net + eventid + '10kbox.json', 'wb').write(urllib.urlopen(tenkboxurl).read())

                        with open(newdir + '\\' + net + eventid + '10kbox.json') as tenkbox:
                            tenkb = json.load(tenkbox)
                            f = 0
                            print "Event " + net + eventid + " contains " + str(len(tenkb["features"])) + " 10k polygons"
                            if len(tenkb["features"]) != 0:
                                arcpy.CreateFeatureclass_management("path//to//tempGDB//", net + eventid + "10kpoly", "POLYGON")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "boxresponses", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "cdi", "FLOAT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "distance", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventid", "TEXT", "10", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventresponses", "LONG", "", "", "", "", "NULLABLE", "REQUIRED")
                                arcpy.AddField_management("path//to//tempGDB//" + net + eventid + "10kpoly", "eventdate", "TEXT", "25", "", "", "", "NULLABLE", "REQUIRED")
                                while f < len(tenkb["features"]):
                            
                                    feature_info = [tenkb["features"][f]["geometry"]["coordinates"][0]]
                                    for feature in feature_info:
                                        pnt1 = arcpy.Point(feature[0][0],feature[0][1])
                                        pnt2 = arcpy.Point(feature[1][0],feature[1][1])
                                        pnt3 = arcpy.Point(feature[2][0],feature[2][1])
                                        pnt4 = arcpy.Point(feature[3][0],feature[3][1])
                                        poly = arcpy.Polygon(arcpy.Array([pnt1,pnt2,pnt3,pnt4]))

                                    if len(tenkb["features"]) != 0:
                                        cur = arcpy.da.InsertCursor("path//to//tempGDB//" + net + eventid + "10kpoly", ['boxresponses', 'cdi', 'distance', 'eventresponses', 'SHAPE@', 'eventid', 'eventdate'])

                                        res = int([onekb["features"][f]["properties"]["nresp"]][0])
                                        cdi = float([onekb["features"][f]["properties"]["cdi"]][0])
                                        dist = int([onekb["features"][f]["properties"]["dist"]][0])
                                        eid = net + eventid
                                        cur.insertRow([res, cdi, dist, eventresponses, poly, eid, edate])
                                        del cur
                                        f = f + 1

#If event is more than 1 month old, delete it
env.workspace = newdir + "\\DYFITemp.gdb\\"
poly1 = arcpy.ListFeatureClasses("*1kpoly*")
for fc in poly1:
    n = fc
    with arcpy.da.SearchCursor(fc, "eventdate") as cursor:
        li = []
        for row in cursor:
            li.append(row[0])

    d = datetime.now()
    t = (d - datetime(int(max(li)[:4]), int(max(li)[5:7]), int(max(li)[8:10]), int(max(li)[11:13]), int(max(li)[14:16]), int(max(li)[17:19]))).total_seconds()
    daysold = ((t/60)/60)/24
    if daysold > 29.97:
        update = 1
        arcpy.Delete_management(newdir + "\\DYFITemp.gdb\\" + n)
        print "Event: " + n + " Data Deleted!"

poly10 = arcpy.ListFeatureClasses("*10kpoly*")
for fc in poly10:
    n = fc
    with arcpy.da.SearchCursor(fc, "eventdate") as cursor:
        li = []
        for row in cursor:
            li.append(row[0])

    d = datetime.now()
    t = (d - datetime(int(max(li)[:4]), int(max(li)[5:7]), int(max(li)[8:10]), int(max(li)[11:13]), int(max(li)[14:16]), int(max(li)[17:19]))).total_seconds()
    daysold = ((t/60)/60)/24
            
    if daysold > 29.97:
        update = 1
        arcpy.Delete_management(newdir + "\\DYFITemp.gdb\\" + n)
        print "Event: " + n + " Data Deleted!"

arcpy.env.workspace = "path//to//TempProdGDB//"

ls1 = arcpy.ListFeatureClasses("*1kpoly")
ls10 = arcpy.ListFeatureClasses("*10kpoly")

arcpy.Merge_management(ls1, "path//to//TempProdGDB//onekpoly")
arcpy.DefineProjection_management("path//to//TempProdGDB//onekpoly", 4326)
arcpy.AddSpatialIndex_management("path//to//TempProdGDB//onekpoly")

arcpy.Merge_management(ls10, "path//to//TempProdGDB//tenkpoly")
arcpy.DefineProjection_management("path//to//TempProdGDB//tenkpoly", 4326)
arcpy.AddSpatialIndex_management("path//to//TempProdGDB//tenkpoly")

#Migrates data to prod GDB
for files in os.listdir("path\\to\\TempProdGDB"):
    if files[-5:].lower() != '.lock':
        shutil.copy2(os.path.join("path\\to\\TempProdGDB", files), os.path.join("path\\to\\ProdGDB", files))
print "Data Migrated to Live Feed"

#Removes all .json files
jfiles = glob.glob("path\\to\\tempdir\\*.json")
for f in jfiles:
    os.remove(f)
    print f + " Removed!"

#Gets token from GIS server then restarts the service if updates have been made
servename = "hostname:6080"
dyfiserviceURL = "http://" + servename + "/arcgis/admin/services/dyfi.MapServer"
dyfir = requests.get(dyfiserviceURL, auth=('<user>', '<password>'))
dyfiexists = dyfir.status_code

print dyfiexists

if dyfiexists == 200:
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

    dyfiurlstop = dyfiserviceURL + "/stop"
    requests.post(dyfiurlstop + "?token=" + token + "&f=json")
    dyfiurlstart = dyfiserviceURL + "/start"
    requests.post(dyfiurlstart + "?token=" + token + "&f=json")
    print "DYFI Service Restarted"
