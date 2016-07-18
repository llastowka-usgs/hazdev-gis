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

GIS Service for the **ShakeMap** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/data/shakemap/ <br>

30 Day Significant Earthquake ShakeMap Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/sm_ShakeMap30DaySignificant/MapServer <br>
This service contains ShakeMap station, mi, pga, pgv, psa03, psa10, and psa30 data.  It is updated every 15 minutes with significant earthquake events from around the world. <br><br><br>

GIS Service for the **Earthquake Catalog**<br>

Earthquake Catalog Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/catalog_2015/MapServer <br>
This service contains earthquake catalog data from 1900 - 2015.  It is updated annually.<br><br><br>

### Earthquake Hazards (*haz* folder)
There are currently GIS services for 1 project within the earthquake team.  This project is for the **Quaternary Faults of the United States**.<br> <br>

GIS Services for the **Quaternary Faults of the United States** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/hazards/qfaults/<br>

Quaternary Faults: http://earthquake.usgs.gov/arcgis/rest/services/haz/qfaults/MapServer <br>
This service contains quaternary fault traces and fault areas for the United States.

Paleosites: http://earthquake.usgs.gov/arcgis/rest/services/haz/paleosites/MapServer <br>
This service contains some paleosite locations near faults in the United States.

2002 Hazard Faults: http://earthquake.usgs.gov/arcgis/rest/services/haz/hazfaults2002/MapServer <br>
This service contains traces for fault locations that were used to caclulate the 2002 National Seismic Hazards Mapping project data.

2008 Hazard Faults: http://earthquake.usgs.gov/arcgis/rest/services/haz/hazfaults2008/MapServer <br>
This service contains traces for fault locations that were used to caclulate the 2008 National Seismic Hazards Mapping project data.

2014 Hazard Faults: http://earthquake.usgs.gov/arcgis/rest/services/haz/hazfaults2014/MapServer <br>
This service contains traces for fault locations that were used to caclulate the 2014 National Seismic Hazards Mapping project data.<br><br><br>

### Landslides (*ls* folder)
There are currently GIS services for 1 project within the landslides team.  This project is for **Post-Fire Debris-FLow Hazards**.<br> <br>

GIS Services for the **Post-Fire Debris-Flow Hazards** Project <br>
For more information about the project itself please visit: http://landslides.usgs.gov/hazards/postfire_debrisflow/<br>

2013/2014 Post-Fire Debris Flow Combined Hazard Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014CombinedHazardBasins/MapServer <br>
This service contains basin polygons with "Combined Hazard" data for debris flow areas after fires during the years of 2013 and 2014.

2013/2014 Post-Fire Debris Flow Combined Hazard Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014CombinedHazardSegments/MapServer <br>
This service contains stream channel segments of "Combined Hazard" data for debris flow areas after fires during the years of 2013 and 2014.

2013/2014 Post-Fire Debris Flow Probability Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014ProbabilityBasins/MapServer <br>
This service contains basin polygons with "Probability" data for debris flow areas after fires during the years of 2013 and 2014.

2013/2014 Post-Fire Debris Flow Probability Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014ProbabilitySegments/MapServer <br>
This service contains stream channel segments of "Probability" data for debris flow areas after fires during the years of 2013 and 2014.

2013/2014 Post-Fire Debris Flow Volume Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014VolumeBasins/MapServer <br>
This service contains basin polygons with "Volume" data for debris flow areas after fires during the years of 2013 and 2014.

2013/2014 Post-Fire Debris Flow Volume Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2013_2014VolumeSegments/MapServer <br>
This service contains stream channel segments of "Volume" data for debris flow areas after fires during the years of 2013 and 2014.

2015 Post-Fire Debris Flow Combined Hazard Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015CombinedHazardBasins/MapServer <br>
This service contains basin polygons with "Combined Hazard" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flow Combined Hazard Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015CombinedHazardSegments/MapServer <br>
This service contains stream channel segments of "Combined Hazard" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flow Probability Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015ProbabilityBasins/MapServer <br>
This service contains basin polygons with "Probability" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flow Probability Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015ProbabilitySegments/MapServer <br>
This service contains stream channel segments of "Probability" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flow Volume Basins: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015VolumeBasins/MapServer <br>
This service contains basin polygons with "Volume" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flow Volume Segments: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015VolumeSegments/MapServer <br>
This service contains stream channel segments of "Volume" data for debris flow areas after fires during the year of 2015.<br><br><br>

### Geomagnetism (*gm* folder)
There are currently no GIS services for any Geomagnetism projects within the team.  More information on the USGS Geomagnetism program can be found at: http://geomag.usgs.gov/<br><br><br>


## Leveraging GIS Services
There are numerous ways to interact with and consume GIS data found in these services.  Please visit Esri's ArcGIS Server REST API documentation at: http://resources.arcgis.com/en/help/rest/apiref/ for more information.
