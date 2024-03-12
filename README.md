# Housing Needs Assessment (HNA) Dashboard - 2021

## Introduction

A census-based tool that measures core housing need and affordable shelter costs by income category, household size, and priority populations. Our methods allow governments to set effective housing targets that will lift Canadians out of chronic housing need and homelessness.

The tool is powered by census data custom built by Statistics Canada in collaboration with HART researchers.

The HART tool and dashboard includes data for Canada; the Provinces and Territories; Census divisions (CD), a general term for regional planning areas; and Census subdivisions (CSD), a general term for municipalities.  

The repository of code is used to create and run the HART Housing Needs Assessment (HNA) Dashboard, as built by Licker Geospatial Consulting Co. (LGeo) on behalf of the Peter A. Allard School of Law at The University of British Columbia.

Link: https://hart.ubc.ca/housing-needs-assessment-tool/

## Deep Dive
For both technical and non-technical deep dive into how this project works, see [here](docs/DeepDive.md)

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

Please make sure you have the following installed (requirements.txt is provided in the repository):

Changelog: 
2023/10/16 - To use the requirements.txt as is, python 3.11 or before is recommended as one of the packages uses the 
deprecated "distutils" setup package.  (https://peps.python.org/pep-0632/)
2024/03/12 - There exists a Dockerfile if you'd like a guaranteed working environment.  

- Python 3
- Pandas
- GeoPandas
- Numpy
- Plotly
- Dash
- SQL Alchemy

It is recommended to just use the requirements file, as you most likely will be missing libraries that aren't core.

### Start Local Server and Run the Dashboard

1. Git Clone or Download the code package from the repository
2. Run `pip install -r requirements.txt` to install all the required packages.
3. Type `python app.py` on your Shell inside of the folder of the code package.
4. Type `localhost:8000/page1`, up to page 5 on your browser. Each page indicates:
    - page1: Map Picker
    - page2: Core Housing Need page
    - page3: Household Projections page
    - page4: Indigenous Household Core Housing Need page
    - page5: Renter vs Owners (and Subsidized Renters) page
    
## Technical Support

Please email contact@hart.ubc.ca for any technical questions related to the dashboard.
