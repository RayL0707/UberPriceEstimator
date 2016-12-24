import csv

# with open('yellow_tripdata_2015-01-06.csv', 'rb') as f:
# 	reader = csv.reader(f)
# 	for row in reader:
# 		print row
f1 = file('2015-02-01.txt', 'r')
c1 = list(csv.reader(f1))
# f2 = file('DailyHistory.csv', 'r')
f3 = file('2016-06-30.csv', 'w')
c3 = csv.writer(f3)

def func(l):
	return {'12': '00', '1:': '01:', '2:': '02:', '3:': '03:', '4:': '04:', '5:': '05:', \
	'6:': '06:', '7:': '07:', '8:': '08:', '9:': '09:', '10': '10', '11': '11'}[l]
def func2(l):
	return {'12': '12', '1:': '13:', '2:': '14:', '3:': '15:', '4:': '16:', '5:': '17:', \
	'6:': '18:', '7:': '19:', '8:': '20:', '9:': '21:', '10': '22', '11': '23'}[l]

def weather(l):
	return {'Clear': '1', 'Mostly Cloudy': '2', 'Partly Cloudy': '2', 'Scattered Clouds': '2', 'Overcast': '3', 'Rain': '4', \
	'Light Freezing Rain': '4', 'Light Rain': '4', 'Heavy Rain': '4', 'Light Snow': '5', 'Snow': '5', 'Heavy Snow': '5', \
	'Fog': '6', 'Mist': '6', 'Haze': '6', 'Light Freezing Fog': '6', 'Unknown': '7'}[l]

rr = 1
for row in c1:
	# print row
	if(rr == 1):
		res = ['time', 'temp', 'wind', 'weather']
		c3.writerow(res)
		rr += 1
	# print row[0:2]
	else:
		t = row[0][5:8]
		# print t
		res = []
		tem = row[0][0:2]
		if(t == ' AM' or t == 'AM'):
			tem = map(func, [tem])
			results = []
			results.append(tem[0] + row[0][2:])
			for x in row[1:]:
				results.append(x)
			# print results[7]
			if results[7] == 'Calm' or results[7] == '-9999.0':
				# print results[7]
				results[7] = '0'
			tem = results[11]
			tem = map(weather, [tem])
			results[11] = tem[0]
			res.append(results[0])
			res.append(results[1])
			res.append(results[7])
			res.append(results[11])
			c3.writerow(res)
		else:
			tem = map(func2, [tem])
			results = []
			results.append(tem[0] + row[0][2:])
			for x in row[1:]:
				results.append(x)
			if results[7] == 'Calm' or results[7] == '-9999.0':
				results[7] = '0'
			tem = results[11]
			tem = map(weather, [tem])
			results[11] = tem[0]
			res.append(results[0])
			res.append(results[1])
			res.append(results[7])
			res.append(results[11])
			c3.writerow(res)
			