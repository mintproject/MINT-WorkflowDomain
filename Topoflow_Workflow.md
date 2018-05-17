# Topoflow Workflow

## Simple Configuration

In the simplest configuration, the following components are provided with South Sudan data while the others are set to default:
* Infiltration
* Channel (TBD)
* Meteorology (Precip only)

The components are set in the providers file.

### Configuration files

[Link to configuration files here]

### Executable Workflow

[Link to WINGS image here]

### Data preparation
#### Meteorology

* Precipitation only from NOAA FLDAS data. Current State: Working on a WINGS workflow to process the data.

#### DEM (Data elevation model)

So far, working on the small Gel-Aliab catchment, which is small enough to be processed on a local machine.

* Flow directory (rtg file)
* Slope (rtg file)
* Area (rtg file)

#### Channel width and channel roughness
Need to create a rtg file manually. Tried to use River Tools to do so but the demo version doesn't allow to do so.
