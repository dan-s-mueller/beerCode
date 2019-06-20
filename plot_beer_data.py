# Reads in csv output file and creates a plot showing temperature and operational history.

import csv
from datetime import datetime
import matplotlib.dates
import matplotlib.pyplot as plt

# Set up data
fileName='second_crack_porter_intermediate'
temp_air=[]
temp_liquid=[]
op_hot=[]
op_cold=[]

# Read in data
line_count = 0
with open('./logs/'+fileName+'.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		if line_count!=0:
			tempTime=datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
			if line_count==1:
				time=[tempTime];
			else:
				time.append(tempTime);
			temp_air.append(float(row[1]))
			temp_liquid.append(float(row[2]))
			op_hot.append(int(row[3]))
			op_cold.append(int(row[4]))
		line_count = line_count+1

# Plot things
time = matplotlib.dates.date2num(time)
days = matplotlib.dates.DayLocator()
days_format=matplotlib.dates.DateFormatter("%D")
fig, ax1 = plt.subplots()
color = 'black'
ax1.set_xlabel('Datetime')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# Plot the second axis first, so it's hidden (operational history)
ax1.plot_date(time,op_hot,marker='',color='red',linewidth=1,linestyle='solid',label="op_hot")
ax1.plot_date(time,op_cold,marker='',color='cyan',linewidth=1,linestyle='solid',label="op_cold")
ax1.tick_params(axis='x',labelcolor=color,labelrotation=90)
ax1.tick_params(axis='y',labelcolor=color)
# Now plot the first axis (temperature)
ax2.plot_date(time,temp_air,marker='',color='blue',linewidth=2,linestyle='solid',label="temp_air")
ax2.plot_date(time,temp_liquid,marker='',color='green',linewidth=2,linestyle='solid',label="temp_liquid")

ax2.tick_params(axis='y', labelcolor=color)
ax2.xaxis.set_major_locator(days)
ax2.xaxis.set_major_formatter(days_format)
ax2.xaxis.grid()
plt.legend(loc=6)

ax1.yaxis.tick_right()
ax2.yaxis.tick_left()
ax2.set_ylabel('Opeartion',color=color,labelpad=30)
ax1.set_ylabel('Temperature (deg F)',color=color,labelpad=30)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.legend(loc=1)
plt.savefig('./logs/'+fileName+'.png')
plt.show()
