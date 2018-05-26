Components used to:
- Open a suite of NetCDF files
- Check whether the model variables are present in the files
- Adjust the units of time to gregorian calendar.
- If yes, extract them and adjust units
- If no, look for other variables from which the needed variable can be derived from, then adjust units.
- Perform one last check
- Export as text files that can be read by Topoflow.

This is meant as an example of the kind of transformation needed to run the full meteorological component of Topoflow.

Details about each component can be found [here](https://github.com/khider/NetCDFWINGS/blob/master/NetCDF_Wings.ipynb).
