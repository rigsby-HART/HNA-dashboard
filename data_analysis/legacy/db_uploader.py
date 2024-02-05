# import sqlalchemy
import pdb

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert

# Importing income data

df_income = pd.read_csv("./sources/income_2021.csv")
# df_income = pd.read_csv("./sources/income.csv")
df_income = df_income.reset_index()
df_income = df_income.rename(columns = {'index': 'pk'})

# Importing partners data

df_partners = pd.read_csv("./sources/partners_2021.csv")
# df_partners = pd.read_csv("./sources/partners_small_230324_name_revised_r4.csv")
df_partners = df_partners.reset_index()
df_partners = df_partners.rename(columns = {'index': 'pk'})

# Importing csd_hhprojection

# df_csd_projection = pd.read_csv('./sources/updated_csd.csv')
df_csd_projection = pd.read_csv('./sources/updated_csd_2021.csv')

# Importing cd_hhprojection

# df_cd_projection = pd.read_csv("./sources/updated_cd.csv")
df_cd_projection = pd.read_csv("./sources/updated_cd_2021.csv")

# Importing indigenous dataset

df_ind = pd.read_csv("./sources/indigenous_2021.csv")
# df_ind = pd.read_csv("./sources/indigenous_230329_r2.csv")

# Importing list of CSDs we don't have data

df_nil = pd.read_csv("./sources/not_in_list_2021.csv")
# df_nil = pd.read_csv("./sources/not_in_list.csv")
df_nil['PK'] = df_nil['CSDUID']
df_nil = df_nil[['PK', 'CSDUID']]

# Importing all provinces
df_provinces = pd.read_excel('../../../Source/2021/2021_Provinces.xlsx')

# Preprocessing for Geocode Mapping Tables

geo_code = df_income['Geography']

def geo_code_extractor(geography):
    geo = geography.split()
    # print(geo)
    for g in geo:
        if g[0] == '(' and g[1].isdigit():
            g = g.replace("(", "")
            g = g.replace(")", "")
            break
    return g

geo_code_list = geo_code.apply(lambda x: geo_code_extractor(x))
region_code_list = geo_code_list.apply(lambda x: x[:4])
province_code_list = geo_code_list.apply(lambda x: x[:2])

geo_code_mapping = pd.DataFrame({'Geo_Code': geo_code_list, 'Region_Code': region_code_list, 'Province_Code': province_code_list, 'Geography': df_income['Formatted Name']})
geo_code_mapping['Geo_Code_Length'] = geo_code_mapping['Geo_Code'].apply(lambda x: len(x))

region_code_mapping = geo_code_mapping.loc[geo_code_mapping['Geo_Code_Length'] == 4, :]
province_code_mapping = geo_code_mapping.loc[geo_code_mapping['Geo_Code_Length'] <= 2, :]

mapped_geo_code = geo_code_mapping.merge(region_code_mapping[['Geo_Code','Geography']], how = 'left', left_on = 'Region_Code', right_on = 'Geo_Code')
mapped_geo_code = mapped_geo_code.merge(province_code_mapping[['Geo_Code','Geography']], how = 'left', left_on = 'Province_Code', right_on = 'Geo_Code')
mapped_geo_code = mapped_geo_code[['Geo_Code_x', 'Region_Code', 'Province_Code', 'Geography_x','Geography_y','Geography']]
mapped_geo_code.columns = ['Geo_Code', 'Region_Code', 'Province_Code', 'Geography','Region','Province']
mapped_geo_code['Region'] = mapped_geo_code['Region'].fillna(mapped_geo_code['Province'])
# pdb.set_trace()

geo_code_table = mapped_geo_code[['Geo_Code', 'Geography']].drop_duplicates()
geo_code_table = geo_code_table.loc[geo_code_table['Geo_Code'].astype(int) > 9999, :].reset_index() #307
geo_code_table = geo_code_table.drop(columns = ['index'])

region_code_table = mapped_geo_code[['Region_Code', 'Region']].drop_duplicates()
region_code_table = region_code_table.loc[region_code_table['Region_Code'].astype(int) > 999, :].reset_index() #307
region_code_table = region_code_table.drop(columns = ['index'])

province_code_table = mapped_geo_code[['Province_Code', 'Province']].drop_duplicates()

df_provinces['PRUID'] = df_provinces['PRUID'].astype(str)
province_code_table = province_code_table.merge(df_provinces[['PRUID', 'PRENAME']],
                                                how='left', left_on='Province_Code', right_on='PRUID')
province_code_table['Province'] = province_code_table['Province'].fillna(province_code_table['PRENAME'] + ' (Province)')
province_code_table = province_code_table[['Province_Code', 'Province']]

# print(province_code_table)
# pdb.set_trace()

# Defining sqlalchemy engine

engine = create_engine('sqlite:///L:\\Projects\\22005 - Housing Needs Assessment\\Scripts\\Dashboard\\Code_Package_2021\\sources\\hart2021.db')#, echo=True)

# Creating tables

Base = declarative_base()

class Partners(Base):
    __tablename__ = "partners"

    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    Geography = Column(String)
    for i in df_partners.columns[2:]:
        vars()[f'{i}'] = Column(Float)

Partners.__table__.create(bind=engine, checkfirst=True)

class Indigenous(Base):
    __tablename__ = "indigenous"
    
    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    Geography = Column(String)
    for i in df_ind.columns[1:]:
        vars()[f'{i}'] = Column(Float)

Indigenous.__table__.create(bind=engine, checkfirst=True)

class Income(Base):
    __tablename__ = "income"
    
    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in df_income.columns[1:]:
        if df_income.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(String)

Income.__table__.create(bind=engine, checkfirst=True)

class GeoCodesIntegrated(Base):
    __tablename__ = "geocodes_integrated"
    
    # define your primary key
    Geo_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in mapped_geo_code.columns[1:]:
        if mapped_geo_code.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(String)

GeoCodesIntegrated.__table__.create(bind=engine, checkfirst=True)

class GeoCode(Base):
    __tablename__ = "geocodes"
    
    # define your primary key
    Geo_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in geo_code_table.columns[1:]:
        if geo_code_table.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(String)

GeoCode.__table__.create(bind=engine, checkfirst=True)

class RegionCode(Base):
    __tablename__ = "regioncodes"
    
    # define your primary key
    Region_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in region_code_table.columns[1:]:
        if region_code_table.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(String)

RegionCode.__table__.create(bind=engine, checkfirst=True)

class ProvinceCode(Base):
    __tablename__ = "provincecodes"
    
    # define your primary key
    Province_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in province_code_table.columns[1:]:
        if province_code_table.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(String)

ProvinceCode.__table__.create(bind=engine, checkfirst=True)

class CSDHHProjections(Base):
    __tablename__ = "csd_hh_projections"
    
    # define your primary key
    Geo_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in df_csd_projection.columns[1:]:
        if df_csd_projection.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(Float)

CSDHHProjections.__table__.create(bind=engine, checkfirst=True)

class CDHHProjections(Base):
    __tablename__ = "cd_hh_projections"
    
    # define your primary key
    Geo_Code = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    for i in df_cd_projection.columns[1:]:
        if df_cd_projection.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(Float)

CDHHProjections.__table__.create(bind=engine, checkfirst=True)

class NotInList(Base):
    __tablename__ = "not_available_csd"
    
    # define your primary key
    Geo_Code = Column(Integer, primary_key=True, comment='primary key')
    
    # columns except pk
    for i in df_nil.columns[1:]:
        if df_nil.dtypes[i] =='int64':
            vars()[f'{i}'] = Column(Integer)
        else:
            vars()[f'{i}'] = Column(Float)

NotInList.__table__.create(bind=engine, checkfirst=True)

# Inserting data

conn = engine.connect()

for i in range(0, len(df_partners)):
    conn.execute(insert(Partners), [df_partners.loc[i,:].to_dict()])

for i in range(0, len(df_ind)):
    conn.execute(insert(Indigenous), [df_ind.loc[i,:].to_dict()])

for i in range(0, len(df_income)):
    conn.execute(insert(Income), [df_income.loc[i,:].to_dict()])

for i in range(0, len(mapped_geo_code)):
    conn.execute(insert(GeoCodesIntegrated), [mapped_geo_code.loc[i,:].to_dict()])

for i in range(0, len(geo_code_table)):
    conn.execute(insert(GeoCode), [geo_code_table.loc[i,:].to_dict()])

for i in range(0, len(region_code_table)):
    conn.execute(insert(RegionCode), [region_code_table.loc[i,:].to_dict()])

for i in range(0, len(province_code_table)):
    conn.execute(insert(ProvinceCode), [province_code_table.loc[i,:].to_dict()])

for i in range(0, len(df_csd_projection)):
    conn.execute(insert(CSDHHProjections), [df_csd_projection.loc[i,:].to_dict()])

for i in range(0, len(df_cd_projection)):
    conn.execute(insert(CDHHProjections), [df_cd_projection.loc[i,:].to_dict()])

for i in range(0, len(df_nil)):
    conn.execute(insert(NotInList), [df_nil.loc[i,:].to_dict()])

conn.close()

print('done')