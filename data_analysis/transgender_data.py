import pandas as pd

# Specify the file path of the CSV file
csv_file = '2021_Consolidated_trans added.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)
MinorityStatus = df.iloc[0,1:].unique()
HousingType = df.iloc[1,1:].unique()
AMHI = df.iloc[2,1:].unique()
FourthColumn = df.iloc[3,1:].unique()

numbers = df.iloc[4:, 1:2500].replace("x","0").replace("nan", "0").astype(int)
# Display the DataFrame
print(MinorityStatus)