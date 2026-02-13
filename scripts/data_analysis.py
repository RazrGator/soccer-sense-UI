import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trilateration_solver(anchor1, distance1, anchor2, distance2, anchor3, distance3):
  # Inputs: location of anchor i, distance i from tracked object for anchors 1 to 3
  # Outputs: relative coordinates of tracked object based on anchor position
  # Math From: https://math.stackexchange.com/questions/884807/find-x-location-using-3-known-x-y-location-using-trilateration
  x1 = anchor1[0]
  y1 = anchor1[1]
  x2 = anchor2[0]
  y2 = anchor2[1]
  x3 = anchor3[0]
  y3 = anchor3[1]

  A = 2*(-x1+x2)
  B = 2*(-y1+y2)
  C = distance1**2 - distance2**2 - x1**2 + x2**2 - y1**2 + y2**2
  D = 2*(-x2+x3)
  E = 2*(-y2+y3)
  F = distance2**2 - distance3**2 - x2**2 + x3**2 - y2**2 + y3**2
  x = (C*E - F*B) / (E*A - B*D)
  y = (C*D - A*F) / (B*D - A*E)
  return [x,y]

def initialize_from_anchor_dist(anchor_dist_1_2,anchor_dist_1_3):
  # Input: Distance between Anchor 1 and 2, distance between Anchor 1 and 3
  # Output: X,Y coordinates of each anchor
  anchor1 = [0,0] # Base, always at 0,0
  anchor2 = [0,anchor_dist_1_2] # Using 0,0 as reference, top left anchor
  anchor3 = [anchor_dist_1_3,0] # Using 0,0 as reference, bottom right anchor

  return anchor1,anchor2,anchor3

def initialize_plot(anchor_dist_1_2,anchor_dist_1_3):
  # This is just a combination of everything written previously.
  # Input: Distance between Anchor 1 and 2, distance between Anchor 1 and 3
  # Output: Displays randomly generated point within "field"
  anchor1,anchor2,anchor3 = initialize_from_anchor_dist(anchor_dist_1_2,anchor_dist_1_3)

  plt.vlines(anchor1[0], color='black', linestyle='-',ymin=anchor1[1],ymax=anchor2[1])
  plt.vlines(anchor3[0], color='black', linestyle='-',ymin=anchor3[1],ymax=anchor2[1])
  plt.hlines(anchor1[0], color='black', linestyle='-',xmin=anchor1[0],xmax=anchor3[0])
  plt.hlines(anchor2[1], color='black', linestyle='-',xmin=anchor2[0],xmax=anchor3[0])


  plt.plot(anchor1[0],anchor1[1], marker='o', markersize=10, linewidth=1, color='blue')
  plt.plot(anchor2[0],anchor2[1], marker='o', markersize=10, linewidth=1, color='green')
  plt.plot(anchor3[0],anchor3[1], marker='o', markersize=10, linewidth=1, color='red')
  plt.grid()

  return plt,anchor1,anchor2,anchor3

def smooth_points(data,n=5):
  filtered_points = pd.DataFrame(columns=['value'])
  count = 0
  for i in range(0,len(data)-n):
    filtered_points.loc[len(filtered_points)] = [data[i:i+n].mean()]
  return filtered_points

def plot_field_data(distance_data,field_length,field_width):
    '''
    Docstring for plot_field_data
    
    Field length and width to be supplied by user on front end.
    
    '''
    field_plot,anchor1,anchor2,anchor3 = initialize_plot(field_length,field_width) # length is Y axis, width is X axis

    smooth_d1 = smooth_points(distance_data['distance1'],n=10).rename(columns={'value':'distance1'})
    smooth_d2 = smooth_points(distance_data['distance2'],n=10).rename(columns={'value':'distance2'})
    smooth_d3 = smooth_points(distance_data['distance3'],n=10).rename(columns={'value':'distance3'})
    smooth_data = pd.concat([smooth_d1,smooth_d2,smooth_d3],axis=1)

    coordinates = pd.DataFrame(columns=['id','x','y'])
    count = 0
    for index, row in smooth_data.iterrows():
        coord = trilateration_solver(anchor1,row['distance1'],anchor2,row['distance2'],anchor3,row['distance3'])
        coordinates.loc[index] = [count,coord[0],coord[1]]
        count += 1

    x = list(coordinates['x'].values[1:])
    y = list(coordinates['y'].values[1:])
    field_plot.plot(x, y, marker='o', markersize=5, linewidth=2, color='blue')
    field_plot.scatter(x[0], y[0], color='red', s=100, edgecolor='black')  # Start
    field_plot.scatter(x[-1],y[-1], color='black', s=100, marker='X')       # End
    print('Generating Plot.')
    field_plot.savefig('static/media/field_plot.jpg',dpi=300,bbox_inches='tight')
    field_plot.close()