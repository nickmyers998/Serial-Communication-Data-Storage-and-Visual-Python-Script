

import serial, sys
from datetime import datetime

def createfilename():

    # Create filename from date and time to easily identify run data
    # Run file is stored in same location as serialcom.py

    c = datetime.now()
    c = str(c)
    sr = list(c)

    for x in range(10):
        sr.pop()

    sr[4] = '-'
    sr[7] = '-'
    sr.insert(10, "-")
    sr.insert(10, "-")
    sr[15] = '-'
    sr[12] = '-'
    str1 = ""
    fin = str1.join(sr)
    fin = "RUN-" + fin + "-EST.txt"
    return fin
    

def initfile(fin):

    # Create text file and insert (0,0) initialization data

    f = open(fin, 'a')
    f.write("0,0")
    f.close()

def startfunc(fin):

    # Establish serial connection between script and PIC
    # Write load data to text file for storage
    # Data is stored in two columns and comma delimited

    port = 'COM3'

    # Baud rate is synchonized with microcontroller

    baudrate = 9600     
    ser = serial.Serial(port,baudrate,timeout=5)
    load = ""
    hold = ""
    time = 0

    while (ser.dtr):

        data = ser.read(1)
        data+= ser.read(ser.inWaiting())
        sys.stdout.flush()
        hold = data.decode('UTF-8', errors='replace')

        try:

            if hold == "X":         # Reading "X" denotes end of single datapoint transmission
                print(load)
                time += 1

                if len(load) > 5:   # Ocassionally, reading "X" does not trigger string reset and will produce indecipherable data
                    load = ""
                    raise ValueError("Serial Data Corruption")

                f = open(fin, 'a')
                f.write('\n')
                f.write(str(time))
                f.write(",")

                if time == 1:
                    f.write("1")

                f.write(load)
                f.close()
                load = ""

            elif hold == "Q":       # Reading "Q" denotes end of data transmission entirely
                print("Program Terminated")
                break

            else:
                load += str(hold)

        except:                     
            
            # Serial occasionally produces invalid data which is ignored
            # Runs are expected to last hours and invalid data occurances occur very infrequently, so eliminating the data does not corrupt the integrity of the dataset

            print("Bad Data Occurrence")
            

        sys.stdout.flush()




f = createfilename()
initfile(f)
startfunc(f)


