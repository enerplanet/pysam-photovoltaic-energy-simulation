# Attributions

## Weather data

`merra_2_access/input_files.7z` redistributes subsets of NASA's MERRA-2
reanalysis: hourly data for Austria, Czechia, Germany and the Netherlands,
2015 to 2025, combined into one NetCDF file per country and year.

| Collection | Variables used |
| --- | --- |
| M2T1NXRAD | `SWGDN` |
| M2T1NXSLV | `T2M`, `U2M`, `V2M`, `U10M`, `V10M`, `PS` |
| M2T1NXLND | `SNODP`, `PRECSNOLAND` |

Global Modeling and Assimilation Office (GMAO) (2015), MERRA-2 tavg1_2d_rad_Nx:
2d,1-Hourly,Time-Averaged,Single-Level,Assimilation,Radiation Diagnostics
V5.12.4, Greenbelt, MD, USA, Goddard Earth Sciences Data and Information
Services Center (GES DISC). https://doi.org/10.5067/Q9QMY5PBNV1T

Global Modeling and Assimilation Office (GMAO) (2015), MERRA-2 tavg1_2d_slv_Nx:
2d,1-Hourly,Time-Averaged,Single-Level,Assimilation,Single-Level Diagnostics
V5.12.4, Greenbelt, MD, USA, Goddard Earth Sciences Data and Information
Services Center (GES DISC). https://doi.org/10.5067/VJAFPLI1CSIV

Global Modeling and Assimilation Office (GMAO) (2015), MERRA-2 tavg1_2d_lnd_Nx:
2d,1-Hourly,Time-Averaged,Single-Level,Assimilation,Land Surface Diagnostics
V5.12.4, Greenbelt, MD, USA, Goddard Earth Sciences Data and Information
Services Center (GES DISC). https://doi.org/10.5067/RKPHT8KC1Y1T

The data were obtained through GES DISC:
https://www.earthdata.nasa.gov/eosdis/daacs/gesdisc

## Software

| Package | Use | Licence |
| --- | --- | --- |
| [NREL-PySAM](https://github.com/NREL/pysam) | PVWatts v8 PV performance model | BSD 3-Clause |
| [pvlib python](https://github.com/pvlib/pvlib-python) | Solar position, GHI decomposition (DIRINT), snow loss | BSD 3-Clause |
