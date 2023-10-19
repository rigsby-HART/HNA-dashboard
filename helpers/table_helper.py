from dash import dcc

from helpers.create_engine import mapped_geo_code


def area_scale_comparison(geo, geo_c, scale):
    if "to-geography-1" == scale:
        geo = geo
        geo_c = geo_c
    elif "to-region-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Region'].tolist()[0]
    elif "to-province-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Province'].tolist()[0]
    return geo, geo_c


def area_scale_primary_only(geo, scale):
    if "to-geography-1" == scale:
        geo = geo
    elif "to-region-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
    elif "to-province-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
    return geo


def storage_variables():
    return [
        dcc.Store(id='area-scale-store', storage_type='local'),
        dcc.Store(id='main-area', storage_type='local'),
        dcc.Store(id='comparison-area', storage_type='local'),
        dcc.Store(id='year-comparison', storage_type='local'),
    ]
