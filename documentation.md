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
This service contains a tweet density heatmap corresponding to the August 24, 2014 M6.0 Napa earthquake. <br><br><br>

**-------Real-time GIS Service Feeds--------**

Web Map displaying the feeds below: http://usgs.maps.arcgis.com/home/webmap/viewer.html?webmap=5555eabe9d65418d8e0b5677b3fe59b5 <br><br>

30 Day Significant Event Feed GIS Service: http://earthquake.usgs.gov/arcgis/rest/services/eq/event_30DaySignificant/MapServer <br>
This service contains event specific data for significant earthquakes over the past 30 days.  It is updated every 15 minutes. <br><br>

GIS Service for the **ShakeMap** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/data/shakemap/ <br>

30 Day Significant Earthquake ShakeMap Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/sm_ShakeMap30DaySignificant/MapServer <br>
This service contains ShakeMap station, mi, pga, pgv, psa03, psa10, and psa30 data.  It is updated every 15 minutes with significant earthquake events from around the world. <br><br>

GIS Service for the **DYFI?** Project <br>
For more information about the project itself please visit: http://earthquake.usgs.gov/data/dyfi/ <br>

30 Day Significant Earthquake Did You Feel It? Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/dyfi_30DaySignificant/MapServer <br>
This service contains aggregated DYFI? responses for events within the last 30 days.  The responses are geographically aggregated into 1km and 10km boxes.  It is updated every 15 minutes in real-time. <br>

Note: Documentation and Python code outlining the process of deploying these near real-time services on a local GIS server can be found in the "NearRealTimeLiveFeedCode" folder of this Github repository.

**------------------------------------------** <br>

GIS Service for the **USGS Earthquake Catalog**<br>

Earthquake Catalog Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/catalog_2015/MapServer <br>
This service contains earthquake catalog data from 1900 - 2015.  It is updated annually.<br><br>

Earthquake Catalog Feed (Feature Service): http://earthquake.usgs.gov/arcgis/rest/services/eq/catalog_2015feature/MapServer <br>
This service contains earthquake catalog data from 1900 - 2015.  It is updated annually.<br><br>

GIS Service for **2012 Landscan Population Data**<br>

2012 LandScan Population Data Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/pager_landscan2012bin/MapServer <br>
This service contains 2012 LandScan Population Data used in PAGER Project.  The data is binned into 5 classes for display purposes.  Complete data information can be found at: http://web.ornl.gov/sci/landscan/
<br><br><br>

### Earthquake Hazards (*haz* folder)

**Hazards GIS Services** <br>
For more information about hazards projects, please visit: http://earthquake.usgs.gov/hazards/<br>

**Alaska Hazard Maps**<br>

Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/

Alaska Hazard Map - 10% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK1hz050_1999/MapServer <br>
 
Alaska Hazard Map - 2% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK1hz250_1999/MapServer <br>
 
Alaska Hazard Map - 10% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK5hz050_1999/MapServer <br>
 
Alaska Hazard Map - 2% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK5hz250_1999/MapServer <br>
 
Alaska Hazard Map - 10% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpga050_1999/MapServer <br>
 
Alaska Hazard Map - 2% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpga250_1999/MapServer <br>
 
Alaska Hazard Map - Gridded Hazard Points: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpts_1999/MapServer <br>
Gridded data for the 1999 Alaska Hazard maps.

**Hawaii Hazard Maps**<br>

Probabilistic seismic-hazard maps were prepared for Hawaii portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2724, http://bssa.geoscienceworld.org/content/91/3/479, and http://earthquake.usgs.gov/hazards/
 
Hawaii Hazard Map - 10% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/HI1hz050_1998/MapServer <br>
 
Hawaii Hazard Map - 2% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/HI1hz250_1998/MapServer <br>
  
Hawaii Hazard Map - 10% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/HI5hz050_1998/MapServer <br>
 
Hawaii Hazard Map - 2% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/HI5hz250_1998/MapServer <br>
  
Hawaii Hazard Map - 10% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/HIpga050_1998/MapServer <br>
 
Hawaii Hazard Map - 2% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/HIpga250_1998/MapServer <br>

Hawaii Hazard Map - Gridded Hazard Points: http://earthquake.usgs.gov/arcgis/rest/services/haz/HIpts_1998/MapServer <br>
 Gridded data for the 1998 Hawaii Hazard maps.

**United States Hazard Maps**<br>

Probabilistic seismic-hazard maps were prepared for the conterminous United States portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.usgs.gov/sim/3195/, http://pubs.usgs.gov/of/2008/1128/, and http://earthquake.usgs.gov/hazards/

2008 United States Hazard Map - 10% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US1hz050_2008/MapServer <br>
 
2008 United States Hazard Map - 2% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US1hz250_2008/MapServer <br>

2008 United States Hazard Map - 10% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US5hz050_2008/MapServer <br>
 
2008 United States Hazard Map - 2% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US5hz250_2008/MapServer <br>

2008 United States Hazard Map - 10% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/USpga050_2008/MapServer <br>
 
2008 United States Hazard Map - 2% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/USpga250_2008/MapServer <br>

2008 United States Hazard Map - Gridded Hazard Points: http://earthquake.usgs.gov/arcgis/rest/services/haz/USpts_2008/MapServer <br>
Gridded data for the 2008 United States Hazard maps.
 
2014 United States Hazard Map - 10% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US1hz050_2014/MapServer <br>
 
2014 United States Hazard Map - 2% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US1hz250_2014/MapServer <br>

2014 United States Hazard Map - 10% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US5hz050_2014/MapServer <br>
 
2014 United States Hazard Map - 2% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/US5hz250_2014/MapServer <br>

2014 United States Hazard Map - 10% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/USpga050_2014/MapServer <br>
 
2014 United States Hazard Map - 2% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/USpga250_2014/MapServer <br>

United States Overview Map: http://earthquake.usgs.gov/arcgis/rest/services/haz/USoverview/MapServer <br>
Overview map of the United States. <br><br>

**Faults** Services<br>
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

2016 Post-Fire Debris Flow - Assessment Data: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2016/MapServer <br>
This service contains post-fire debris flow data for fires during the year of 2016.

Post-Fire Debris Flow - Fire Locations: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_locations/MapServer <br>
This service contains post-fire debris flow fire locations for all fire assessments.<br><br><br>


### Geomagnetism (*gm* folder)
There are currently no GIS services for any Geomagnetism projects within the team.  More information on the USGS Geomagnetism program can be found at: http://geomag.usgs.gov/<br><br><br>


## Leveraging GIS Services
There are numerous ways to interact with and consume GIS data found in these services.  Please visit Esri's ArcGIS Server REST API documentation at: http://resources.arcgis.com/en/help/rest/apiref/ for more information.
