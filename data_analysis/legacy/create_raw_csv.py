import pandas as pd
import numpy as np
from decimal import Decimal
import re
import pdb

source_file_path = r'L:\Projects\22005 - Housing Needs Assessment\Processed\Script Outputs\2021_Update\CHN\Canada_CHN_20230821.csv'
french_mapping_path = r'L:\Projects\22005 - Housing Needs Assessment\Scripts\Dashboard\Formatting\22005 - French regions name matching_230324.xlsx'
old_new_column_mapping_path = r'L:\Projects\22005 - Housing Needs Assessment\Processed\2021_Data_Update\Dataprep\CHN_OldNewFieldNameMapping.xlsx'
csd_ids_path = r"L:\Projects\22005 - Housing Needs Assessment\Source\2021\2021_CSDs.xlsx"
cd_ids_path = r"L:\Projects\22005 - Housing Needs Assessment\Source\2021\2021_CDs.xlsx"
p_ids_path = r"L:\Projects\22005 - Housing Needs Assessment\Source\2021\2021_Provinces.xlsx"
median_income_path = r"L:\Projects\22005 - Housing Needs Assessment\Source\2021\2021_Median_HH_income.xlsx"

# Setting 4 header columns
source_file = pd.read_csv(source_file_path,  encoding='utf-8', header=[0, 1, 2, 3])
french_mapping_file = pd.read_excel(french_mapping_path, sheet_name='Final_Mapping_2021')
old_new_column_mapping_file = pd.read_excel(old_new_column_mapping_path)
csd_ids = pd.read_excel(csd_ids_path)
cd_ids = pd.read_excel(cd_ids_path)
p_ids = pd.read_excel(p_ids_path)
median_income = pd.read_excel(median_income_path)


# Creating dictionary for mapping and renaming column names
column_mapping = pd.DataFrame({'Original_dim1': list(old_new_column_mapping_file['Dimension 1_2016']),
                                    'Updated_dim1': list(old_new_column_mapping_file['Dimension 1_2021']),
                                    'Original_dim2': list(old_new_column_mapping_file['Dimension 2_2016']),
                                    'Updated_dim2': list(old_new_column_mapping_file['Dimension 2_2021']),
                                    'Original_dim3': list(old_new_column_mapping_file['Dimension 3_2016']),
                                    'Updated_dim3': list(old_new_column_mapping_file['Dimension 3_2021']),
                                    'Original_dim4': list(old_new_column_mapping_file['Dimension 4_2016']),
                                    'Updated_dim4': list(old_new_column_mapping_file['Dimension 4_2021'])
                                    })

rename_mapping_dim1 = dict(zip(column_mapping['Updated_dim1'], column_mapping['Original_dim1']))
rename_mapping_dim2 = dict(zip(column_mapping['Updated_dim2'], column_mapping['Original_dim2']))
rename_mapping_dim3 = dict(zip(column_mapping['Updated_dim3'], column_mapping['Original_dim3']))
rename_mapping_dim4 = dict(zip(column_mapping['Updated_dim4'], column_mapping['Original_dim4']))

mapped_columns_source_file = source_file.rename(columns=rename_mapping_dim1, level=0)
mapped_columns_source_file = mapped_columns_source_file.rename(columns=rename_mapping_dim2, level=1)
mapped_columns_source_file = mapped_columns_source_file.rename(columns=rename_mapping_dim3, level=2)
mapped_columns_source_file = mapped_columns_source_file.rename(columns=rename_mapping_dim4, level=3)


# Cleaning extra space and unknown characters from column names
mapped_columns_source_file.columns = mapped_columns_source_file.columns.map('-'.join).str.strip(' ')
mapped_columns_source_file = mapped_columns_source_file.rename(
    columns={element: re.sub(r"-?[A-Za-z]+: ([A-Za-z0-9]+(_[A-Za-z0-9]+)+)-?", "", element)
             for element in mapped_columns_source_file.columns.tolist()})
mapped_columns_source_file.columns = mapped_columns_source_file.columns.str.replace(r'\s{2,}', '', regex=True)

# pdb.set_trace()
# Fetching province, CD and CSD ids from geography names
mapped_columns_source_file['CD_ids'] = mapped_columns_source_file['Geography'].str.findall(r"\b\d{4}\b")
mapped_columns_source_file['P_ids'] = mapped_columns_source_file['Geography'].str.findall(r"\b\d{2}\b")
mapped_columns_source_file['CSD_ids'] = mapped_columns_source_file['Geography'].str.findall(r"\b\d{7}\b")

# Fetching only strings from Geography
mapped_columns_source_file['Temp_Geography'] = mapped_columns_source_file['Geography'].str.split('(').apply(lambda x: [e.strip() for e in x])
mapped_columns_source_file['Temp_Geography'] = mapped_columns_source_file['Temp_Geography'].str[0].replace(r'\s{2,}', '', regex=True)

# Concating all ids for easy join
mapped_columns_source_file['All_ids'] = mapped_columns_source_file['CD_ids'].fillna('') + \
                                        mapped_columns_source_file['CSD_ids'].fillna('') + \
                                        mapped_columns_source_file['P_ids'].fillna('')
mapped_columns_source_file['All_ids'] = mapped_columns_source_file['All_ids'].str[0]
mapped_columns_source_file['All_ids'] = mapped_columns_source_file['All_ids'].fillna(0).astype(int)


# Preparing IDs data to be joined with original data in required format
cd_ids['Type'] = 'CD'
csd_ids['Type'] = 'CSD'
cd_ids = cd_ids.rename(columns={'CDUID': 'CSDUID'})
cd_csd_ids = pd.concat([cd_ids[['CSDUID', 'Type', 'PRUID']], csd_ids[['CSDUID', 'Type', 'PRUID']]])
merge_ids = cd_csd_ids.merge(p_ids[['PRUID', 'Dash_Abbr']], how='left')
merge_ids['Type_State'] = '(' + merge_ids['Type'] + ', ' + merge_ids['Dash_Abbr'] + ')'


# Merging the id format with original data to fetch formatted geography names
formatted_geography_source_file = mapped_columns_source_file.merge(merge_ids[['CSDUID', 'Type_State']], how='left',
                                                                   left_on='All_ids', right_on='CSDUID')
formatted_geography_source_file['Type_State'] = formatted_geography_source_file['Type_State'].fillna('(Province)')
formatted_geography_source_file['Formatted_Geography'] = formatted_geography_source_file['Temp_Geography'] + ' ' + \
                                                         formatted_geography_source_file['Type_State']
formatted_geography_source_file['Formatted_Geography'] = formatted_geography_source_file['Formatted_Geography'].\
    replace('Canada 20000 (Province)', 'Canada')




french_mapped_source_file = formatted_geography_source_file.merge(french_mapping_file, how="left",
                                                                  left_on='Formatted_Geography', right_on='Broken French Names')
french_mapped_source_file['French_mapped_Geography'] = french_mapped_source_file['Fixed names'].\
    fillna(french_mapped_source_file['Formatted_Geography'])


median_income['CD_ids'] = median_income['Geographies'].str.findall(r"\b\d{4}\b")
median_income['P_ids'] = median_income['Geographies'].str.findall(r"\b\d{2}\b")
median_income['CSD_ids'] = median_income['Geographies'].str.findall(r"\b\d{7}\b")
median_income['Median_Geography'] = median_income['Geographies'].str.split('(').apply(lambda x: [e.strip() for e in x])
median_income['Median_Geography'] = median_income['Median_Geography'].str[0].replace(r'\s{2,}', '', regex=True)
median_income['All_ids'] = median_income['CD_ids'].fillna('') + \
                                        median_income['CSD_ids'].fillna('') + \
                                        median_income['P_ids'].fillna('')
median_income['All_ids'] = median_income['All_ids'].str[0]
median_income['All_ids'] = median_income['All_ids'].fillna(0).astype(int)

formatted_median_income_file = median_income.merge(merge_ids[['CSDUID', 'Type_State']], how='left',
                                                                   left_on='All_ids', right_on='CSDUID')
formatted_median_income_file['Type_State'] = formatted_median_income_file['Type_State'].fillna('(Province)')
formatted_median_income_file['Formatted_Median_Geography'] = formatted_median_income_file['Median_Geography'] + ' ' + \
                                                         formatted_median_income_file['Type_State']
formatted_median_income_file['Formatted_Median_Geography'] = formatted_median_income_file['Formatted_Median_Geography'].\
    replace('Canada 00000 (Province)', 'Canada')

median_income_source_file = french_mapped_source_file.merge(formatted_median_income_file[['Formatted_Median_Geography', 'Median income of household']], how='left',
                                                            left_on='French_mapped_Geography', right_on='Formatted_Median_Geography')


median_income_source_file.to_csv(r'L:\Projects\22005 - Housing Needs Assessment\Processed\Script Outputs\2021_Update\CHN\CHN_RawData_20230821.csv')


# income_csv = formatted_chn_file[['Geography', 'French_mapped_Geography', 'Median income of household']]
# income_csv = income_csv.rename(columns={'French_mapped_Geography': 'Formatted Name',
#                                         'Median income of household': 'Median income of household ($)'})
# income_csv['Median income of household ($)'] = income_csv['Median income of household ($)'].replace('x', np.NAN)
# # pdb.set_trace()
# income_csv['20% of AMHI'] = (income_csv['Median income of household ($)'].astype(float) * 0.2).map('${:,.0f}'.format)
# income_csv['50% of AMHI'] = (income_csv['Median income of household ($)'].astype(float) * 0.5).map('${:,.0f}'.format)
# income_csv['80% of AMHI'] = (income_csv['Median income of household ($)'].astype(float) * 0.8).map('${:,.0f}'.format)
# income_csv['120% of AMHI'] = (income_csv['Median income of household ($)'].astype(float) * 1.2).map('${:,.0f}'.format)
#
# income_csv['20% or under of AMHI'] = "<=" + income_csv['20% of AMHI']
# income_csv['21% to 50% of AMHI'] = income_csv['20% of AMHI'] + " - " + income_csv['50% of AMHI']
# income_csv['51% to 80% of AMHI'] = income_csv['50% of AMHI'] + " - " + income_csv['80% of AMHI']
# income_csv['81% to 120% of AMHI'] = income_csv['80% of AMHI'] + " - " + income_csv['120% of AMHI']
# # income_csv['121% and more of AMHI'] = ">=" + Decimal(sub(r'[^\d.]','',income_csv['120% of AMHI']))+1
#
# income_csv['Rent AMHI'] = (income_csv['Median income of household ($)'].astype(float) * 0.3 / 12).map('${:,.0f}'.format)
# income_csv['Rent 20% of AMHI'] = (income_csv['20% of AMHI'].astype(float) * 0.3 / 12).map('${:,.0f}'.format)
# income_csv['Rent 50% of AMHI'] = (income_csv['50% of AMHI'].astype(float) * 0.5 / 12).map('${:,.0f}'.format)
# income_csv['Rent 80% of AMHI'] = (income_csv['80% of AMHI'].astype(float) * 0.8 / 12).map('${:,.0f}'.format)
# income_csv['Rent 120% of AMHI'] = (income_csv['120% of AMHI'].astype(float) * 1.2 / 12).map('${:,.0f}'.format)
#
# income_csv['20% or under of AMHI.1'] = "<=" + income_csv['Rent 20% of AMHI']
# income_csv['21% to 50% of AMHI.1'] = income_csv['Rent 20% of AMHI'] + " - " + income_csv['Rent 50% of AMHI']
# income_csv['51% to 80% of AMHI.1'] = income_csv['Rent 50% of AMHI'] + " - " + income_csv['Rent 80% of AMHI']
# income_csv['81% to 120% of AMHI.1'] = income_csv['Rent 80% of AMHI'] + " - " + income_csv['Rent 120% of AMHI']
# # income_csv['121% and more of AMHI.1'] = ">=" + income_csv['Rent 120% of AMHI']+1
#
# pdb.set_trace()







# print(source_file)
# pdb.set_trace()
