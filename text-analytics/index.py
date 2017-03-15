# ************************************************************************
# PRODUCE CSV FILES BASED ON 3 CONFIGURATONS - PRODUCE, CONCAT, TRANSFORM
# CSV FILES ARE UPLOADED TO AZURE ML FOR MODEL BUILDING
# ************************************************************************
import csv
import os
import sys
from analyse_data import analyse_data
from curve_fit import get_training_data

if (len(sys.argv) >= 2):
    action = str(sys.argv[1])
    yearNum = sys.argv[2]
    if (len(sys.argv) == 5):
        ASSET_TYPE = str(sys.argv[3])
        ASSET = str(sys.argv[4])

year = str(yearNum) + '/'
year_master_file = 'o-' + str(yearNum) + '-master.csv'
base_input_path = 'input_csv/'
arr_input_file = os.listdir(base_input_path + year)
base_output_path = 'output_csv/'
arr_output_file = os.listdir(base_output_path + year)

ASSET_FILE = ASSET_TYPE + '.csv'
ASSET_NAME = ASSET.replace(" ", "_")

if (action == "produce"):
    for f in arr_input_file:
        output_arr_2d = analyse_data(ASSET_FILE, ASSET, base_input_path + year + f)
        with open(base_output_path + year + "o-" + f,'wb') as outputFile:
            wr = csv.writer(outputFile, dialect='excel')
            wr.writerows(output_arr_2d)
        print("Successfully generated: o-" + f)

if (action == "concat"):
    # Concatinate output files
    fout = open(base_output_path + year + year_master_file ,"a")
    # first file:
    for line in open(base_output_path + year + arr_output_file[0]):
        fout.write(line)
    # now the rest:
    for index in range(1, len(arr_output_file)):
        f = open(base_output_path + year + arr_output_file[index])
        f.readline() # skip the header
        for line in f:
             fout.write(line)
        f.close()
        print("Successfully concat: " + str(arr_output_file[index]))
    fout.close()

def transform_file(asset_file, asset, filename):
    # Read input CSV file
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        input_data = list(reader)

    arr_size = len(input_data)
    for i in range(1, arr_size): # start from 1, ignore header row
        # date
        date = input_data[i][0]
        percentage_change = get_training_data(asset_file, asset, date)
        input_data[i][2] = percentage_change # refer to analyse_data.py
        print("Successfully changed: " + str(arr_size) + " " + str(i) + " " + str(percentage_change))

    with open(base_output_path + year + "o-" + str(yearNum) + "-" + ASSET_TYPE + "-" + ASSET_NAME + ".csv",'wb') as outputFile:
        wr = csv.writer(outputFile, dialect='excel')
        wr.writerows(input_data)

if (action == "transform"):
    transform_file(ASSET_FILE, ASSET, base_output_path + year + year_master_file)
