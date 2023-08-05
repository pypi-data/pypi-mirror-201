import os
# get the path of this directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# list all CSV files in this directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# create a dictionary of CSV files with their names as keys
csv_data = {}
for csv_file in csv_files:
    with open(os.path.join(dir_path, csv_file), 'r') as f:
        csv_data[csv_file] = f.read()

# make the dictionary of CSV data available when this package is imported
__all__ = ['csv_data']