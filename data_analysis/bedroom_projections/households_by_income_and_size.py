# Specify the file path of the CSV file
import numpy as np
import pandas as pd

csv_file = '../2021_Consolidated_trans added.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

minority_status = [x.strip() for x in df.iloc[0, 1:].unique()]
housing_type = [x.strip() for x in df.iloc[1, 1:].unique()]

AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[3, 1:].unique()]

numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

# Total households/Transgender households are the last two types
groups = len(CHN_status) * len(AMHI) * len(housing_type)
subset = numbers.iloc[:, :groups]

# Create the names of the columns
columnName = pd.Series([""] * (groups))

index = 1
for housing in housing_type:
    for income in AMHI:
        for status in CHN_status:
            columnName[index] = f"{housing}-{income}-{status}"
            index += 1
subset = subset.reset_index(drop=True)
subset = subset.rename(columns=columnName.to_dict())
subset.insert(0, "Geography", df.iloc[4:, 0].reset_index(drop=True))

# I only want to keep household count by income and household sizes
columns = [f"{housing}-{income}" for income in AMHI for housing in housing_type]
CHN_examined = CHN_status[0]

def keep_income_by_hh_size(row: pd.Series):
    output = dict([(col, 0) for col in columns])
    if row.empty or np.isnan(row.iat[1]):
        return pd.Series(output)
    for housing in housing_type:
        for income in AMHI:
            output[f"{housing}-{income}"] = row[f"{housing}-{income}-{CHN_examined}"]
    return pd.Series(output)


households_by_income_and_size: pd.DataFrame = subset.apply(keep_income_by_hh_size, axis=1)
households_by_income_and_size.insert(0, "Geography", df.iloc[4:, 0].reset_index(drop=True))
households_by_income_and_size.to_csv('../households_by_income_and_size.csv', index=False)