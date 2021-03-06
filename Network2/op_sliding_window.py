import pandas as pd
import sys
import numpy as np
import os
import pickle
from sliding_window import sliding_window
import glob
import csv

NUM_CLASSES = 8
def opp_sliding_window(data_x, data_y, ws, ss, label_pos_end = True):
    '''
    Performs the sliding window approach on the data and the labels
    
    return three arrays.
    - data, an array where first dim is the windows
    - labels per window according to end, middle or mode
    - all labels per window
    
    @param data_x: ids for train
    @param data_y: ids for train
    @param ws: ids for train
    @param ss: ids for train
    @param label_pos_end: ids for train
    '''    


    print("Sliding window: Creating windows {} with step {}".format(ws, ss))
    
    data_x = sliding_window(data_x,(ws,data_x.shape[1]),(ss,1))
    
    # Label from the end
    if label_pos_end:
        data_y = np.asarray([[i[-1]] for i in sliding_window(data_y,(ws,data_y.shape[1]),(ss,1))])
    else:
    
        #Label from the middle
        if False:
            data_y_labels = np.asarray([[i[i.shape[0] // 2]] for i in sliding_window(data_y,(ws,data_y.shape[1]),(ss,1))])
        else:
            count_l=[]
            idy = []
            #Label according to mode
            try:
                
                data_y_labels = []
                for sw in sliding_window(data_y,(ws,data_y.shape[1]),(ss,1)):
                    labels = np.zeros((20)).astype(int)
                    count_l = np.bincount(sw[:,0], minlength = NUM_CLASSES)
                    idy = np.argmax(count_l)
                    attrs = np.sum(sw[:,1:], axis = 0)
                    attrs[attrs > 0] = 1
                    labels[0] = idy  
                    labels[1:] = attrs
                    data_y_labels.append(labels)
                print(len(data_y_labels))
                data_y_labels = np.asarray(data_y_labels)
                
            
            except:
                print("Sliding window: error with the counting {}".format(count_l))
                print("Sliding window: error with the counting {}".format(idy))
                return np.Inf
            
            #All labels per window
            data_y_all = np.asarray([i[:] for i in sliding_window(data_y,(ws,data_y.shape[1]),(ss,1))])
    
    return data_x.astype(np.float32), data_y_labels.astype(np.uint8), data_y_all.astype(np.uint8)


def example_creating_windows_file(k, folder_name, data_x, labels):
        # Sliding window approach

    print("Starting sliding window")
    print(data_x.shape)
    print(labels.shape)
    X, y, y_all = opp_sliding_window(data_x, labels.astype(int),
                                     sliding_window_length,
                                     sliding_window_step, label_pos_end = False)
    print(X.shape)
    print(y.shape)
    print(y_all.shape)
    counter_seq = 0
    value = 0
    if (X.shape[0]<y.shape[0]):
        value = X.shape[0]
    else:
        value = y.shape[0]
   # for f in range(X.shape[0]):
    for f in range(value):
       # try:
        sys.stdout.write('\r' + 'Creating sequence file '
                                'number {} with id {}'.format(f, counter_seq))
        sys.stdout.flush()

        # print "Creating sequence file number {} with id {}".format(f, counter_seq)
        seq = np.reshape(X[f], newshape = (1, X.shape[1], X.shape[2]))
        seq = np.require(seq, dtype=np.float)
        dir = data_dir + "seq_" + folder_name + "_" + str(k) + "_" + str(counter_seq) + ".pkl"
        obj = {"data" : seq, "label" : y[f], "labels" : y_all[f]}
        #f = open(os.path.join(dir, 'seq_{0:06}.pkl'.format(counter_seq)), 'wb')
        f = open(dir, 'wb')
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        counter_seq += 1
        print("dumping")
        f.close()
 

ws = (100,31)
#ws = (200,134)  #for MoCAP
#ss = (25,134)     #for MoCAP
ss = (25,31)
sliding_window_length = 100   # for MoCAP
#sliding_window_length = 100    
sliding_window_step = 25
#data_dir =  "/data/sawasthi/data/MoCAP_data/testData/"
#data_dir = "/media/shrutarv/Drive1/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/Windows2/"
data_dir = "S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/Windows2/"
#data_dir = "S:/MS A&R/4th Sem/Thesis/LaRa/OMoCap data/Test_data/"
#for i in sliding_window(data_y,(ws,data_y.shape[1]),(ss,1)):

#    print (np.shape(i[:,0]))
folder_name = "S07"
FileList_y = []
#os.chdir('/vol/actrec/DFG_Project/2019/Mbientlab/recordings_2019/07_IMU_synchronized_annotated/' + folder_name)
#os.chdir("/vol/actrec/DFG_Project/2019/MoCap/recordings_2019/14_Annotated_Dataset/" + folder_name)
#os.chdir("/media/shrutarv/Drive1/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S13/")
os.chdir("S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/" + folder_name)
#os.chdir("S:/MS A&R/4th Sem/Thesis/LaRa/OMoCap data/OMoCap data/" + folder_name)
FileList_y = glob.glob('*labels.csv')
#os.chdir('/vol/actrec/DFG_Project/2019/Mbientlab/recordings_2019/07_IMU_synchronized_annotated/P13')
#List = glob.glob('*labels.csv')
#FileList_y = FileList_y + List
        
FileList_x = []
#os.chdir('S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S13')
#os.chdir('/vol/actrec/DFG_Project/2019/Mbientlab/recordings_2019/07_IMU_synchronized_annotated/P14')
#os.chdir("/media/shrutarv/Drive1/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S13/")
FileList_x = glob.glob('*.csv')
#os.chdir('S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S14')
#os.chdir('/vol/actrec/DFG_Project/2019/Mbientlab/recordings_2019/07_IMU_synchronized_annotated/P14')
#List = glob.glob('*.csv')
#FileList_x = FileList_x + List
set_x = set(FileList_x)
set_y = set(FileList_y)
FileList_x = list(set_x - set_y)
FileList_x.sort()
FileList_y.sort()
k = 0 


for i,j in zip(FileList_x, FileList_y):
    k += 1
    #data_y = pd.read_csv("/vol/actrec/DFG_Project/2019/MoCap/recordings_2019/14_Annotated_Dataset/" + folder_name + "/" + j) 
    #data_y = pd.read_csv("/media/shrutarv/Drive1/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S13/"+j)
    data_y = pd.read_csv("S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/" + folder_name+ "/" + j) 
    #data_y = pd.read_csv("S:/MS A&R/4th Sem/Thesis/LaRa/OMoCap data/OMoCap data/" + folder_name + "/" + j) 
    data_y = data_y.values
    labels = data_y
    #data_x = pd.read_csv("/vol/actrec/DFG_Project/2019/MoCap/recordings_2019/14_Annotated_Dataset/"+ folder_name + "/" + i) 
    #data_x = pd.read_csv("/media/shrutarv/Drive1/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/S13/"+i)
    data_x = pd.read_csv("S:/MS A&R/4th Sem/Thesis/LaRa/IMU data/IMU data/" + folder_name +"/" + i)
    #data_x = pd.read_csv("S:/MS A&R/4th Sem/Thesis/LaRa/OMoCap data/OMoCap data/" + folder_name + "/" + i)
    data_x = data_x.values
    #data_x = np.delete(data_x,np.s_[68:74], axis=1)
    data_x = data_x[:,1:31]
    
    example_creating_windows_file(k, folder_name, data_x, labels)
    if(k == 1):
        break
    


