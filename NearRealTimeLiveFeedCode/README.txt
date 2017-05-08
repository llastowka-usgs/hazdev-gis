USGS 30 Day Significant Event Near Real-time Feed Python Scripts
----------------------------------------------------------------

The Python scripts contained in this directory allow external users to configure near real-time USGS GIS service feeds on their own GIS server infrastructure.

The 3 scripts are outlined below:

EventService.py
---------------
The event service script exposes event data for the last month's worth of significant earthquakes via a GIS service. When run, the script will get data for
earthquakes within the last 30 days and format and publish it to a GIS server. The script can be triggered by a custom mechanism or set to run as scheduled
tasks.

ShakeMapService.py
------------------
The ShakeMap service script exposes Shakemap MI, PGA, PGV, PSA03, PSA10, and PSA30 data for the last month's worth of significant earthquakes via a GIS service.
When run, the script will retrieve and format data for earthquakes within the last 30 days and publish it to a GIS server. The script can be triggered by a
custom mechanism or set to run as scheduled tasks.

DYFIService.py
--------------
The "Did You Feel It?" service script exposes 10km and 1km geocoded polygons for the last month's worth of significant earthquakes via a GIS service. When run,
the script will retrieve and format data from .geojson files and publish these data to a GIS server. The script can be triggered by a custom mechanism or set to
run as scheduled tasks.

NOTE: All customized variables pertaining to directory information, file locations, or geodatabase structure will need to be set to the environment of the new
      user's system framework. These scripts were built referencing Python 2.7 on Windows Server 2012 R2. Customized architectures that vary from these settings
      may see different results!

