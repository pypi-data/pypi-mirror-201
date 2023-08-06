# Copernicus Marine Service client

A library to facilitate the access of Copernicus Marine Service products and datasets.

## Introduction

This package allows to recover products and datasets information from Command Line Interface or with Python code,
as well as download subsets through opendap protocol.

## Command Line Interface (CLI)

### Command *describe*
Retrieve information about products as JSON:

```
> copernicus-marine describe
{
  "products": [
    {
      "bbox": [
        "-25.00",
        "75.00",
        "70.00",
        "86.00"
      ],
      "created": "2011-10-11",
      "product_id": "SEAICE_ARC_PHY_L3M_NRT_011_017",
      "temporal_extent": [
        "2021-04-27",
        null
      ],
      "thumbnail": "https://catalogue.marine.copernicus.eu/documents/IMG/SEAICE_ARC_PHY_L3M_NRT_011_017.png",
      "title": "ARCTIC Ocean and Sea-Ice Sigma-Nought"
    }
    ...
  ]
}
```

Retrieve all information about products and datasets as JSON:

```
> copernicus-marine describe --include-description --include-datasets --include-providers --include-keywords
{
  "products": {
    "title": "ARCTIC Ocean and Sea-Ice Sigma-Nought",
    "product_id": "SEAICE_ARC_PHY_L3M_NRT_011_017",
    "thumbnail": "https://catalogue.marine.copernicus.eu/documents/IMG/SEAICE_ARC_PHY_L3M_NRT_011_017.png",
    "description": "'''Short description:''' \nFor the Arctic Ocean  - multiple Sentinel-1 scenes, Sigma0 calibrated and noise-corrected, with individual geographical map projections over Svalbard and Greenland Sea regions.\n\n'''DOI (product) :'''   \nhttps://doi.org/10.48670/moi-00124",
    "providers": [
      {
        "name": "OSI-METNO-OSLO-NO (SD)",
        "roles": [
          "pointOfContact"
        ],
        "url": null,
        "email": "marine-servicedesk@met.no"
      },
      {
        "name": "OSI-METNO-OSLO-NO (PM)",
        "roles": [
          "originator"
        ],
        "url": null,
        "email": "cecilie.wettre@met.no"
      },
      {
        "name": "OSI-METNO-OSLO-NO (WPL)",
        "roles": [
          "custodian"
        ],
        "url": null,
        "email": "ositac-manager@met.no"
      },
      {
        "name": "SIW-METNO-OSLO-NO",
        "roles": [
          "resourceProvider"
        ],
        "url": null,
        "email": "ositac-prod@met.no"
      },
      {
        "name": "SIW-METNO-OSLO-NO",
        "roles": [
          "distributor"
        ],
        "url": null,
        "email": "cmems-tech@met.no"
      }
    ],
    "created": "2011-10-11",
    "bbox": [
      "-25.00",
      "75.00",
      "70.00",
      "86.00"
    ],
            "uri": "ftp://nrt.cmems-du.eu/Core/SEAICE_ARC_PHY_L3M_NRT_011_017/cmems_obs-si_arc_physic_nrt_L2-EW_PT1H-irr"
          }
        ]
      }
    ...
    ]
  }
}

```

Check out the help:

```
> copernicus-marine describe --help
Usage: copernicus-marine describe [OPTIONS]

Options:
  --one-line             Output JSON on one line
  --include-description  Include product description in output
  --include-datasets     Include product dataset details in output
  --include-providers    Include product provider details in output
  --include-keywords     Include product keyword details in output
  -c, --contains TEXT    Filter catalogue output. Returns products with
                         attributes matching a string token
  --overwrite-cache      Force to refresh the catalogue by overwriting the
                         local cache
  --help                 Show this message and exit.
```

### Command *subset*

Download a dataset subset, based on dataset id, variable names and attributes slices:

```
> copernicus-marine subset -p METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 2021-01-03 -g 0.0 0.1 0.0 0.1

< Login:
< Password:
< Trying to download as one file...
```

File downloaded to ./{dataset_id}.nc if not specified otherwise (through -o/--output-path and -f/--output-file options).

Check out the help:

```
> copernicus-marine subset --help

Usage: copernicus-marine subset [OPTIONS]

  Downloads subsets of datasets as NetCDF files taking into account the server
  data query limit. A 'dataset-id' (can be found via the 'copernicus-marine
  describe' command) is required.

  Example:

    copernicus-marine subset --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
    --variable analysed_sst --variable sea_ice_fraction --temporal-subset
    2021-01-01 2021-01-02 --geographical-subset 0.0 0.1 0.0 0.1

    copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v
    analysed_sst   -v sea_ice_fraction -t 2021-01-01 2021-01-02 -g 0.0 0.1 0.0
    0.1

Options:
  -u, --dataset-url TEXT          The full dataset URL option is mutually
                                  exclusive with dataset_id.
  -i, --dataset-id TEXT           The dataset id option is mutually exclusive
                                  with dataset_url.
  --login TEXT
  --password TEXT
  -v, --variable TEXT             Specify dataset variables
  -g, --geographical-subset <FLOAT RANGE FLOAT RANGE FLOAT RANGE FLOAT RANGE>...
                                  The geographical subset as minimal latitude,
                                  maximal latitude, minimal longitude and
                                  maximal longitude
  -t, --temporal-subset <DATETIME DATETIME>...
                                  The temporal subset as start datetime and
                                  end datetime
  -d, --depth-range <FLOAT RANGE FLOAT RANGE>...
                                  The depth range in meters, if depth is a
                                  dataset coordinate
  -o, --output-path PATH          The destination path for the downloaded
                                  files. Default is the current directory
                                  [required]
  -f, --output-file PATH          Concatenate the downloaded data in the given
                                  file name (under the output path)
  -l, --limit INTEGER             Specify the download size limit (in MB) of
                                  the Opendap server if it can't be provided
                                  by the message error
  --confirmation                  Print dataset metadata and ask for
                                  confirmation before download
  --force-protocol [WWW:OPENDAP|MYO:MOTU-SUB]
                                  Force download through one of the available
                                  protocols
  --dry-run                       Flag to specify NOT to send the request to
                                  external server. Returns the request instead
  --help                          Show this message and exit.
```

### Command *native*

Download a native file (or files), based on dataset id or path to files:

Example:
```
> copernicus-marine native -u ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/

< Login:
< Password:
< You requested the download of the following files:
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202207.nc - 3.27 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202208.nc - 3.29 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202209.nc - 3.28 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202210.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202211.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202212.nc - 3.26 MB

Total size of the download: 19.62 MB


Do you want to continue? [y/N]:
```

File(s) downloaded to ./{path}/{filename} if not specified otherwise:
- "--output-path" specifies a directory to dump the files in
- "--no-directories" to not recreate the folder structure

If not specified otherwise, after the header display with a summary of the request,
the user is asked for confirmation:
- "--no-confirmation" to turn down the confirmation prompt
- "--show-outputnames" to display the full paths of the outputs files

Check out the help:

```
> copernicus-marine native --help

Usage: copernicus-marine native [OPTIONS]

  Downloads native data files based on     dataset_id or datafiles url path.
  The function fetches the files recursively if a folder path is passed as
  url.     When provided a dataset id,     all the files in the corresponding
  folder will be downloaded.

      By default for any download request, a summary of the request result is
      displayed to the user and a confirmation is asked.     This can be
      turned down. Example:

    copernicus-marine native -nd -o data_folder --dataset-id
    cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m

    copernicus-marine native -nd -o data_folder --dataset-url
    ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-
    pft_myint_7km-3D-diato_P1M-m

Options:
  -u, --dataset-url TEXT  Path to the data files option is mutually exclusive
                          with dataset_id.
  -i, --dataset-id TEXT   The dataset id option is mutually exclusive with
                          dataset_url.
  --login TEXT
  --password TEXT
  -nd, --no-directories   Option to not recreate folder hierarchy in ouput
                          directory.
  --show-outputnames      Option to display the names of the output files
                          before download.
  -o, --output-path PATH  The destination path for the downloaded files.
                          Default is the current directory  [required]
  --no-confirmation       Ask for confirmation before download, after header
                          display
  --dry-run               Flag to specify NOT to send the request to external
                          server. Returns the request instead
  --help                  Show this message and exit.
```

## Installation

Using pip, for example:
```
pip install copernicus-marine-client
```
## Technical details

This module is organized around two capabilities:
- a catalogue, parsed from web requests, that contains informations on the available datasets
- a downloader, to simplify the download of dataset files or subsets

The catalogue can be displayed by the user and is used by the downloader to link the user
requests with files or subset of files to retrieve.
The downloader will help the user download the needed datasets.
