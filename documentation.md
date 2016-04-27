# USGS Geologic Hazards Science Center GIS Server Documentation
## http://earthquake.usgs.gov/arcgis/rest/services

The USGS Geologic Hazards Science Center (GHSC) in Golden, CO maintains a GIS server with services pertaining to various geologic hazard disciplines including earthquakes and landslides.  This document provides an overview of the structure of this server and also outlines the GIS data it contains.

There are 4 folders for varying geologic hazards in the home area on the GIS server. http://earthquake.usgs.gov/arcgis/rest/services
They are eq (earthquakes), gm (geomagnetism), haz (earthquake hazards), and ls (landlsides).  Each directory contains services with data that pertain to each discipline.  Services for each discipline are outlined below.

### Earthquakes (*eq* folder)
There are currently GIS services for 3 projects within the earthquake team.  These projects are **Slab Models for Subduction Zones**, **Tweet Earthquake Dispatch (TED)**, and **ShakeMap**. <br> <br>


GIS Services for the **Slab Models for Subduction Zones** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/data/slab/<br>


Slab Depth Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_depth/MapServer <br>
This service contains linear contours showing subduction zone depth values around the world

Slab Dip Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_dip/MapServer <br>
This service contains linear contours showing subduction zone dip values around the world

Slab Strike Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_strike/MapServer <br>
This service contains linear contours showing subduction zone strike values around the world

Slab Grid Points: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_grid/MapServer <br>
This service contains a grid of points showing subduction zone depth, dip, and strike values around the world <br><br>


GIS Services for the **Tweet Earthquake Dispatch (TED)** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/earthquakes/ted/ <br>

TED Napa Tweets: http://earthquake.usgs.gov/arcgis/rest/services/eq/ted_NapaTweets/MapServer <br>
This service contains tweets corresponding to the August 24, 2014 M6.0 Napa earthquake.  The service is a sample of the data harvested by the TED project.

TED Napa Heatmap: http://earthquake.usgs.gov/arcgis/rest/services/eq/ted_NapaHeatmap/MapServer <br>
This service contains a tweet density heatmap corresponding to the August 24, 2014 M6.0 Napa earthquake. <br><br>

