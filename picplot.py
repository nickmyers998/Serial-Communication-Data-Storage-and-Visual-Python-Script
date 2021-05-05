import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
global name

def findfile():     
    global name

    # Sets file name to most recently created run file found in code's directory.
    # Run file name formatting is performed in serialcom.py
    # Run file is stored in the same location as serialcom.py and picplot.py

    path = r"Z:\Engineering\02-Users\nmyers\Reports and Proposals\Hydraulic Press\Python"
    enter = ""
    datnum = 0
    with os.scandir(path) as dirs:
        for entry in dirs:
            
            list1 = list(entry.name)
            
            if ((list1[0] == 'R') and (list1[1] == 'U') and (list1[2] == 'N')):
                
                year = (((int(list1[4]))*1000) + ((int(list1[5]))*100) + ((int(list1[6]))*10) + (int(list1[7]))) * 100000000
                day = (((int(list1[12]))*10) + (int(list1[13]))) * 10000
                month = (((int(list1[9]))*10) + (int(list1[10]))) * 1000000
                hour = (((int(list1[17]))*10) + (int(list1[18]))) * 100
                minute = ((int(list1[20]))*10) + (int(list1[21]))
                dat = year + month + day + hour + minute
                if dat > datnum:
                    datnum = dat
                    enter = entry.name
    name = enter
    print(name)


def animate(i):

    # Create real-time graph of load data during run
    # This function does not have to be explicitly called

    data = open(name,'r').read()
    lines = data.split('\n')
    xs = []
    ys = []
   
    for line in lines:
        x, y = line.split(",")
        
        # Denote x data as number before comma and y data as number after comma
        # Convert string representation of data to floating point numbers

        try:
            xs.append(float(x)/60)
            ys.append(float(y))
        except:
            continue
   
    # Apply formatting to graph and label axes

    ax1.clear()
    ax1.plot(xs, ys, color='red')

    plt.xlabel('Time (minutes)', fontsize=14)
    plt.ylabel('Applied Force (lbs)', fontsize=14)
    plt.title(name, fontsize=16)	
    plt.grid(True)


def startplot():

    # Call this function to begin plotting

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()


findfile()
startplot()