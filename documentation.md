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
This service contains ShakeMap station, mi, pga, pgv, psa03, psa10, and psa30 data.  It is updated every 15 minutes with significant earthquake events from around the world. <br><br>

30 Day Significant Earthquake Did You Feel It? Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/dyfi_responses/MapServer <br>
This service contains aggregated DYFI? responses for events within the last 30 days.  The responses are geographically aggregated into 1km and 10km boxes.  It is updated every 15 minutes in real-time. <br><br>

GIS Service for the **USGS Earthquake Catalog**<br>

Earthquake Catalog Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/catalog_2015/MapServer <br>
This service contains earthquake catalog data from 1900 - 2015.  It is updated annually.<br><br>

GIS Service for **2012 Landscan Population Data**<br>

2012 LandScan Population Data Feed: http://earthquake.usgs.gov/arcgis/rest/services/eq/pager_landscan2012bin/MapServer <br>
This service contains 2012 LandScan Population Data used in PAGER Project.  The data is binned into 5 classes for display purposes.  Complete data information can be found at: http://web.ornl.gov/sci/landscan/
<br><br><br>

### Earthquake Hazards (*haz* folder)

Hazards GIS Services <br>
For more information about hazards projects, please visit: http://earthquake.usgs.gov/hazards/<br>

Alaska Hazard Map - 10% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK1hz050_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for horizontal spectral response acceleration for 1.0-second period with a 10 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/
 
Alaska Hazard Map - 2% in 50 year 1 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK1hz250_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for horizontal spectral response acceleration for 1.0-second period with a 2 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/
 
Alaska Hazard Map - 10% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK5hz050_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for horizontal spectral response acceleration for 0.2-second period with a 10 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/
 
Alaska Hazard Map - 2% in 50 year 5 hz: http://earthquake.usgs.gov/arcgis/rest/services/haz/AK5hz250_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for horizontal spectral response acceleration for 0.2-second period with a 2 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/
 
Alaska Hazard Map - 10% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpga050_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for peak horizontal acceleration with a 10 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/ 
 
Alaska Hazard Map - 2% in 50 year PGA: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpga250_1999/MapServer <br>
 Probabilistic seismic-hazard maps were prepared for Alaska portraying peak horizontal acceleration and horizontal spectral response acceleration for 0.2- and 1.0-second periods with probabilities of exceedance of 10 percent in 50 years and 2 percent in 50 years. This particular data set is for peak horizontal acceleration with a 10 percent probability of exceedance in 50 years. All of the maps were prepared by combining the hazard derived from spatially smoothed historic seismicity with the hazard from fault-specific sources. The acceleration values contoured are the random horizontal component. The reference site condition is firm rock, defined as having an average shear-wave velocity of 760 m/sec in the top 30 meters corresponding to the boundary between NEHRP (National Earthquake Hazards Reduction program) site classes B and C. For more information online visit: http://pubs.er.usgs.gov/publication/i2679, http://pubs.er.usgs.gov/publication/ofr9936, and http://earthquake.usgs.gov/hazards/
 
Alaska Hazard Map - Gridded Hazard Points: http://earthquake.usgs.gov/arcgis/rest/services/haz/AKpts_1999/MapServer <br>
 Gridded data for the 1999 Alaska Hazard maps. 

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
This service contains stream channel segments of "Volume" data for debris flow areas after fires during the year of 2015.

2015 Post-Fire Debris Flows: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2015/MapServer <br>
This service contains post-fire debris flow data for select fires during the year of 2015. (Note: Most 2015 fires are contained in the other 2015 post-fire debris flow GIS services because they were created with a previous system architecture.)

2016 Post-Fire Debris Flows: http://earthquake.usgs.gov/arcgis/rest/services/ls/pwfdf_2016/MapServer <br>
This service contains post-fire debris flow data for fires during the year of 2016.<br><br><br>


### Geomagnetism (*gm* folder)
There are currently no GIS services for any Geomagnetism projects within the team.  More information on the USGS Geomagnetism program can be found at: http://geomag.usgs.gov/<br><br><br>


## Leveraging GIS Services
There are numerous ways to interact with and consume GIS data found in these services.  Please visit Esri's ArcGIS Server REST API documentation at: http://resources.arcgis.com/en/help/rest/apiref/ for more information.
