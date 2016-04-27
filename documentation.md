# USGS Geologic Hazards Science Center GIS Server Documentation
## http://earthquake.usgs.gov/arcgis/rest/services

The USGS Geologic Hazards Science Center (GHSC) in Golden, CO maintains a GIS server with services pertaining to various geologic hazard disciplines including earthquakes and landslides.  This document provides an overview of the structure of this server and also outlines the GIS data it contains.

There are 4 folders for varying geologic hazards in the home area on the GIS server. http://earthquake.usgs.gov/arcgis/rest/services
They are eq (earthquakes), gm (geomagnetism), haz (earthquake hazards), and ls (landlsides).  Each directory contains services with data that pertain to each discipline.  Services for each discipline are outlined below.

### Earthquakes (*eq* folder)
There are currently GIS services for 3 projects within the earthquake team.  These projects are **Slab Models for Subduction Zones**, **Tweet Earthquake Dispatch (TED)**, and **ShakeMap**.

GIS Services for the **Slab Models for Subduction Zones** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/data/slab/

Slab Depth Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_depth/MapServer <br>
This service contains linear contours showing subduction zone depth values around the world

Slab Dip Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_dip/MapServer <br>
This service contains linear contours showing subduction zone dip values around the world

Slab Strike Contours: http://earthquake.usgs.gov/arcgis/rest/services/eq/slab_strike/MapServer <br>
This service contains linear contours showing subduction zone strike values around the world

