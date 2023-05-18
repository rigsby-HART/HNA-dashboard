# Housing Needs Assessment (HNA) Dashboard

## Introduction

A census-based tool that measures core housing need and affordable shelter costs by income category, household size, and priority populations. Our methods allow governments to set effective housing targets that will lift Canadians out of chronic housing need and homelessness.

The tool is powered by census data custom built by Statistics Canada in collaboration with HART researchers.

The HART tool and dashboard includes data for Canada; the Provinces and Territories; Census divisions (CD), a general term for regional planning areas; and Census subdivisions (CSD), a general term for municipalities.  

The repository of code is used to create and run the HART Housing Needs Assessment (HNA) Dashboard, as built by Licker Geospatial Consulting Co. (LGeo) on behalf of the Pater A. Allard School of Law at The University of British Columbia.

Link: https://hart.ubc.ca/housing-needs-assessment-tool/

## Features

The HART dashboard provides the following features:

- Map picker for selecting regions
- Plots and tables for Core Housing Need
- Plots and tables for Household Projections
- Plots and tables for Indigenous Households' Core Housing Need
- Comparison between two regions
- Download functions for all plots and tables

## Getting Started In Your Local Environment

### System requirements

Please make sure you have the following installed(Requirements.txt is provided in the repository):

- Python 3
- Pandas
- GeoPandas
- Numpy
- Plotly
- Dash
- SQL Alchemy

### Start Local Server and Run the Dashboard

1. Git Clone or Download the code package from the repository
2. Type `python app.py` on your Shell inside of the folder of the code package.
3. Type `000.000.0.00:8050/page1`, `000.000.0.00:8050/page2`, `000.000.0.00:8050/page3`, and `000.000.0.00:8050/page4` on your browser. 000.000.0.00 is your IP address. Each page indicates:
    - page1: Map Picker
    - page2: Core Housing Need page
    - page3: Household Projections page
    - page4: Indigenous Household Core Housing Need Page
    
## Technical Support

Please email ooo@ooo.ooo for any technical questions related to the dashboard.