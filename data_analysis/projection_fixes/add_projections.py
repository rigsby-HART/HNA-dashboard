import pandas as pd
from sqlalchemy import create_engine

# Specify the file path of the CSV file

cds = 'data_analysis/projection_fixes/updated_cd_2021.csv'
csds = 'data_analysis/projection_fixes/updated_csd_2021.csv'
engine = create_engine(f'sqlite:///data_analysis//hart2021.db')

# Read the CSV file into a DataFrame
cd_df = pd.read_csv(cds, encoding='latin-1', dtype=float)
csd_df = pd.read_csv(csds, encoding='latin-1', dtype=float)
cd_df["Geo_Code"] = cd_df["Geo_Code"].astype(int)
csd_df["Geo_Code"] = csd_df["Geo_Code"].astype(int)


# replace columns in the tables with the ones from the csvs
cd_hh_projection = pd.read_sql_table('cd_hh_projections', engine.connect())
col_count = len(cd_hh_projection.columns)
cd_hh_projection[cd_df.columns] = cd_df


sql = 'DROP TABLE IF EXISTS cd_hh_projections;'
engine.execute(sql)
cd_hh_projection.to_sql("cd_hh_projections", engine, index=False)

csd_hh_projection = pd.read_sql_table('csd_hh_projections', engine.connect())

# For some dumbass reason our original dataset's name uses some weird long "-" like "–".  This makes it so our new
# data label is incompatible.  As it would be a MASSIVE pita to fix this, I will avoid this issue.
column_rename_map = {
    'Total - Private households by household type including census family structure - Total - Private households by household income proportion to AMHI_1 -   1pp':
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   1pp',
    'Total - Private households by household type including census family structure - Total - Private households by household income proportion to AMHI_1 -   2pp':
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   2pp',
    'Total - Private households by household type including census family structure - Total - Private households by household income proportion to AMHI_1 -   3pp':
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   3pp',
    'Total - Private households by household type including census family structure - Total - Private households by household income proportion to AMHI_1 -   4pp':
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   4pp',
    'Total - Private households by household type including census family structure - Total - Private households by household income proportion to AMHI_1 -   5pp':
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   5pp',
    'Total - Private households by household type including census family structure - Households with income 20% or under of area median household income (AMHI) - Total - Household size':
        'Total - Private households by household type including census family structure -   Households with income 20% or under of area median household income (AMHI) - Total - Household size',
    'Total - Private households by household type including census family structure - Households with income 21% to 50% of AMHI - Total - Household size':
        'Total - Private households by household type including census family structure -   Households with income 21% to 50% of AMHI - Total - Household size',
    'Total - Private households by household type including census family structure - Households with income 81% to 120% of AMHI - Total - Household size':
        'Total - Private households by household type including census family structure -   Households with income 51% to 80% of AMHI - Total - Household size',
    'Total - Private households by household type including census family structure - Households with income 51% to 80% of AMHI - Total - Household size':
        'Total - Private households by household type including census family structure -   Households with income 81% to 120% of AMHI - Total - Household size',
    'Total - Private households by household type including census family structure - Households with income 121% or over of AMHI - Total - Household size':
        'Total - Private households by household type including census family structure -   Households with income 121% or over of AMHI - Total - Household size',
}
csd_df = csd_df.rename(columns=column_rename_map)
csd_hh_projection[csd_df.columns] = csd_df


sql = 'DROP TABLE IF EXISTS csd_hh_projections;'
engine.execute(sql)
csd_hh_projection.to_sql("csd_hh_projections", engine, index=False)

