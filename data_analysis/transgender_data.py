import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert
# Specify the file path of the CSV file
csv_file = '2021_Consolidated_trans added.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)
minority_status = [x.strip() for x in df.iloc[0, 1:].unique()]
housing_type = [x.strip() for x in df.iloc[1, 1:].unique()]
AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[3, 1:].unique()]

# Pure data
numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

# Total households/Transgender households are the last two types
groups = len(CHN_status) * len(AMHI) * len(housing_type)
offset = (len(minority_status) - 2) * groups
transgender_households = numbers.iloc[:, offset:]

# Create the names of the columns
columnName = pd.Series([""] * (groups * 2))
index = 0
for minority in (minority_status[-2:]):
    for housing in housing_type:
        for income in AMHI:
            for status in CHN_status:
                columnName[index] = f"{minority}-{housing}-{income}-{status}"
                index += 1
columnName = columnName.rename({x: (x+offset+1) for x in range(groups*2)})
transgender_households = transgender_households.rename(columns=columnName.to_dict())
transgender_households.insert(0, "Geography", df.iloc[4:,0])
transgender_households = transgender_households.reset_index(drop=True)

# Create
# Display the DataFrame

# Create engine
engine = create_engine(f'sqlite:///sources//previous_years//hart2021.db')
conn = engine.connect()

Base = declarative_base()

# 'Percent Non-Binary HH in core housing need'
# Calculate percent of the non binary ppl in CHN by income category
class Indigenous(Base):
    __tablename__ = "indigenous"

    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    Geography = Column(String)
    for i in transgender_households.columns[1:]:
        vars()[f'{i}'] = Column(Float)


Indigenous.__table__.create(bind=engine, checkfirst=True)

for i in range(0, len(transgender_households)):
    conn.execute(insert(Indigenous), [transgender_households.loc[i,:].to_dict()])