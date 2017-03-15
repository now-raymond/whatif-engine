import numpy as np
# import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import time
from datetime import date
import math

# date_pattern = '%Y-%m-%d'
date_pattern = '%m/%d/%Y'
input_pattern = '%Y-%m-%d'

def readData(asset_file, ticker, start):
	Ticker = []
	start = time.mktime(time.strptime(start, input_pattern))
	end = start + 950400
	gotten = False
	with open(asset_file) as csvfile:
		reader = csv.DictReader(csvfile, ['Ticker','Date','Open','High','Low','Close'])

		for row in reader:
			if row['Ticker'] == ticker and time.mktime(time.strptime(row['Date'], input_pattern)) > start:
				if gotten == False:
					start_close = (float(row['Close']))
					gotten = True
				elif time.mktime(time.strptime(row['Date'], date_pattern)) > end:
					close = (float(row['Close']))
					break


	ret = (close - start_close) / start_close

	return ret

def get_training_data(asset_file, ticker, start):

	data = readData(asset_file, ticker, start)

	return data
