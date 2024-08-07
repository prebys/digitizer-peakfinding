import numpy as np
import matplotlib.pyplot as plt
import os

target_dir = r"./"
target_file = r"WaveDump_Data_15_25_15_clipped.csv"

plot_data = True

def working_anim(index, refresh): #Just command line animation to see if code is hung or slowing
    if (index%400 == 0):
        print("Working  |", end = "\r")
    if (index%400 == int(refresh/4)):
        print("Working  /", end = "\r")
    if (index%400 == int(refresh/2)):
        print("Working  -", end = "\r")
    if (index%400 == int(refresh*3/4)):
        print("Working  \\", end = "\r")

def transform_data(raw_data): #chatGPT wrote this
    str_data = [string.split(',') for string in raw_data]
    unformatted_data = [[int(sublist[0]), float(sublist[1]), float(sublist[2])] for sublist in str_data]
    data = list(map(list, zip(*unformatted_data)))
    return data

def extract_data(file_in, plot_data):  
    index = 0
    all_data = []
    with open(file_in, 'r') as file:                                #Open file     
        while True:                

############Get the trace from the file
            line = file.readline().strip()                          #Readline
            
            if not any(line):                                       #Check to see if input file line is empty (aka end of file)
                break       
                    
            if (line[:6] == "Record"):                              #Check for start of trace
                n_data = int(line.split(":")[1].strip())            #Get points per trace
                
                nline = file.readline().strip()             
                n_event = int(nline.split(":")[1].strip())          #Get the event number
                
                nline = file.readline().strip()
                t_event = int(nline.split(":")[1].strip())          #Get the event time
                
                nline = file.readline().strip()
                header = [ item for item in nline.split(',')]       #get the header for the data
               
                line_data = [None]*n_data                           #Create an empty list with size of points in trace
                for n in range(0,n_data):       
                    line_data[n] = file.readline().strip()          #Add each point into a list
                
                data = np.asarray(transform_data(line_data))        #transform list of strings to correct format
                
    
            else:                                                   #Check to see if we are synconized
                print("Something went wrong\nLine reading got desynced")
                input()
             
            all_data.append(data)
###################################################################
            #Put Code here to analyze each trace one by one (for vectorized form, use code outside of function)
            #Trace data is saved to a numpy array of shape [[t],[ch0],[ch1],...,[chN]]
            #The name of the trace data is 'data'
            
            
            
            
            
            
            if plot_data:
                plt.plot(data[0]/10, data[1])                               #SiPM signal
                plt.plot(data[0]/10, (data[2]-np.average(data[2]))*100+760) #RF signal offset and enlarged
                plt.ylim(720,800)
                plt.title("Event Number = %i, Event 'time' = %i"%(n_event, t_event))
                plt.xlabel("Time [ns]")
                plt.ylabel("Digitizer value")
                plt.draw()
                plt.pause(2)
                plt.clf()
            
            
            #needless animation for fun
            index += 1
            working_anim(index, 400)
            
    return(np.array(all_data))
                                

#Put Code here to analyze the data in vector form with the shape: data[trace_idx][data_channel_idx][channel_data_idx]
data = extract_data(target_dir+target_file,plot_data) 


    








