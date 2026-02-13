import serial
import csv
import time
import pandas as pd

from .data_analysis import plot_field_data

def collect_data(field_length,field_width):
    stop = 0
    ser = serial.Serial('COM6', 115200)  # adjust port
    time.sleep(2)
    ser.write(b"begin\n")
    print('Beginning read...')
    while(1):
        if stop == 1: # Need to update from user - ROD
            break
        headers = ['id','distance1','distance2','distance3']
        index = 0
        with open("data.csv", "w",newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            f.flush()
            try:
                while index < 100: # Currently only collects 100 points
                    line = ser.readline().decode().strip()
                    data = line.split(', ')
                    data.insert(0,str(index))
                    writer.writerow(data)
                    f.flush()
                    print(data)
                    index += 1

            except KeyboardInterrupt:
                stop = 0
                print('Exiting...')
            except Exception as e:
                stop = 0
                # Catch any other errors
                print(f"Error: {e}")
            finally:
                stop = 0
                ser.close()
                print("Serial port closed, file saved.")
        
        if index >= 100:
            stop = 1
            break

    #ser.write(b"stop\n")

    data = pd.read_csv('data.csv')
    # User supplies field length and width via front end - ROD
    # length is Y axis, width is X axis
    plot_field_data(distance_data=data,field_length=field_length,field_width=field_width)

