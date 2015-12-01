import Quandl
import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
import datetime

required_data = {"Soybean_Oil_Futures": "CHRIS/CME_BO1", 
							 "Soybean_Futures": "CHRIS/CME_S1", 
							 "Commitment_of_Traders_Soybeans_Futures_Only": "CFTC/S_F_ALL",
							 "Commitment_of_Traders_Soybean_Oil_Futures_Only": "CFTC/BO_F_ALL"}

quandl_return_type = {"Open Interest": 5,
											"Producer/Merchant/Processor/User Longs": 6,
											"Producer/Merchant/Processor/User Shorts": 7,
											"Swap Dealer Longs": 8,
											"Swap Dealer Shorts": 9,
											"Swap Dealer Spreads": 10,
											"Money Manager Longs": 11,
											"Money Manager Shorts": 12,
											"Money Manager Spreads": 13,
											"Other Reportable Longs": 14,
											"Other Reportable Shorts": 15,
											"Other Reportable Spreads": 16,
											"Total Reportable Longs": 17,
											"Total Reportable Shorts": 18,
											"Non Reportable Longs": 19,
											"Non Reportable Shorts": 20 }

########################################################
#                  Data Analysis Suite
########################################################

# Tasks 1 & 2
# data_type can be "diff, rdiff, cumul, and normalize"
def download(quandl_code, data_type):
	data_set = Quandl.get(quandl_code, authtoken='n4x1M7BSxGDxtjM55xTG', transformation=data_type, collapse='daily', returns='numpy')
	return data_set

def store(data_needs, data_type):
	for key, value in data_needs.iteritems():
		text_file = "data_" + key + "_" + data_type + ".txt"
		new_file = open(text_file, 'w')
		data = download(value, data_type)
		for i in data:
			new_file.write(str(i) + '\n')

	new_file.close()

def read(data_needs, data_type):
	for key, value in data_needs.iteritems():
		text_file = "data_" + key + "_" + data_type + ".txt"
		open_file = open(text_file, 'r')
		arr = []
		for data in open_file:
			# print data
			arr.append(data)
	open_file.close()
	return arr

# These functions are all used for analyzing and graphing the data

def plot_graph(x, y, graph_title):
	plt.plot(x,y)
	plt.title(graph_title)
	plt.show()

def ratio_graph(data_set, data_type, numerator_type, denominator_type, graph_title):
	date_arr = []
	y_axis_arr = []
	numerator_index = quandl_return_type[numerator_type]
	denominator_index = quandl_return_type[denominator_type]
	for i in read(data_set, data_type):
		temp_str = i.split(", ")
		date_arr.append(datetime.datetime(int(temp_str[0].split('(')[2]), int(temp_str[1]), int(temp_str[2]), int(temp_str[3]), int(temp_str[4].split(')')[0])))
		y_axis_arr.append(float(temp_str[numerator_index]) /  float(temp_str[denominator_index]))
	
	plot_graph(np.array(date_arr), np.array(y_axis_arr), graph_title)

def daily_returns_graph(data_set, data_type, graph_title):
	date_arr = []
	y_axis_arr = []
	for i in read(data_set, data_type):
		temp_str = i.split(", ")
		date_arr.append(datetime.datetime(int(temp_str[0].split('(')[2]), int(temp_str[1]), int(temp_str[2]), int(temp_str[3]), int(temp_str[4].split(')')[0])))
		y_axis_arr.append(float(temp_str[8]))

	plot_graph(np.array(date_arr), np.array(y_axis_arr), graph_title)

def correlate(data_set1, data_set2, data_type1, data_type2):
	date_arr1 = []
	y_axis_arr1 = []
	y_axis_arr2 = []
	date_arr2 = []
	for i in read(data_set1, data_type1):
		temp_str = i.split(", ")
		date_arr1.append(datetime.datetime(int(temp_str[0].split('(')[2]), int(temp_str[1]), int(temp_str[2]), int(temp_str[3]), int(temp_str[4].split(')')[0])))
		y_axis_arr1.append(float(temp_str[8]))

	for i in read(data_set2, data_type2):
		temp_str = i.split(", ")
		date_arr2.append(datetime.datetime(int(temp_str[0].split('(')[2]), int(temp_str[1]), int(temp_str[2]), int(temp_str[3]), int(temp_str[4].split(')')[0])))
		y_axis_arr2.append(float(temp_str[8]))

	return np.correlate(y_axis_arr1, y_axis_arr2)


# Downloads and Stores all the data into text files
# store(required_data, 'normalize')
# store(required_data, 'diff')
# store(required_data, 'rdiff')
# store(required_data, 'cumul')

# Task 3a
daily_returns_graph({"Soybean_Oil_Futures": "CHRIS/CME_BO1"}, "cumul", "Cumulative Daily Returns for Soybean Oil")
daily_returns_graph({"Soybean_Futures": "CHRIS/CME_S1"}, "cumul", "Cumulative Daily Returns for Soybeans")

# Task 3b
ratio_graph({"Commitment_of_Traders_Soybeans_Futures_Only": "CFTC/S_F_ALL"}, "normalize", 
"Total Reportable Longs", 
"Total Reportable Shorts", 
"Ratio between Long and Short for Soybeans") # Task 3b

# Task 4
print correlate({"Soybean_Oil_Futures": "CHRIS/CME_BO1"}, {"Soybean_Futures": "CHRIS/CME_S1"}, "cumul", "cumul")
