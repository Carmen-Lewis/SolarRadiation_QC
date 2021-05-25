# SolarRadiation_QC
Quality control tests for solar radiation.

## Code
May be used for either timezone-naive datasets such as [SAURAN](https://sauran.ac.za/) or timezone-aware datasets such as [BSRN](https://bsrn.awi.de/).

[`main.py`](main.py):
* Set `LOCATION` parameters (latitude, longitude, timezone, altitude, name) via pvlib.location.Location
* Set `FILEPATH` to .csv file, or directory of files if BSRN monthly files are used
* Set `DATASOURCE` to either 'BSRN' or 'SAURAN' to select pre-set date formats for .csv or .tab
* For locations other than SUN/STB (SAURAN) and DAA (BSRN), please set the correct numbers of rows to skip and column names
