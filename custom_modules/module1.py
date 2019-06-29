# path1 = "/uscms_data/d3/mkim/MKWorkingArea/CMSSW_10_2_0/src/JL/Melrose/P2_CMSSW_10_1_5/src/L1TMuonSimulations/Analyzers/test7/histos_tba.20.npz"
def load_input_file(path1):
    import numpy as np
    file_in = np.load(path1)
    print(type(file_in))
    print(file_in.keys())
    arr_X = file_in['variables']
    arr_y = file_in['parameters']
    csc_phi = arr_X[:,0:5]
    csc_theta = arr_X[:,0+12:5+12]
    # return cnn_input, arr_y[:,0]
    
    # hits in all 4 stations
    t1 = ~np.isnan(csc_phi[:,0]) # ME1/1
    #t2 = ~np.isnan(csc_phi[:,1])
    #t3 = np.logical_or(t1,t2)
    #del t1,t2
    t4 = ~np.isnan(csc_phi[:,2]) # ME2/X
    t5 = ~np.isnan(csc_phi[:,3]) # ME3/X
    t6 = np.logical_and(t4,t5) 
    # del t4,t5
    t7 = np.logical_and(t1,t6) # ME2/X,3/X,1/1
    # del t3,t6
    t8 = ~np.isnan(csc_phi[:,4])
    t9 = np.logical_and(t7,t8) # ME1/1, 2, 3, 4
    # del t7,t8

    csc_phi[np.isnan(csc_phi[:,0]),0] = 1
    csc_phi[np.isnan(csc_phi[:,1]),1] = 1
    csc_phi[:,1] = csc_phi[:,0]*csc_phi[:,1]
    csc_phi2 = np.delete(csc_phi, 1, 1)

    csc_theta[np.isnan(csc_theta[:,0]),0] = 1
    csc_theta[np.isnan(csc_theta[:,1]),1] = 1
    csc_theta[:,1] = csc_theta[:,0]*csc_theta[:,1]

    csc_theta2 = np.delete(csc_theta, 1, 1)
    mm = len(csc_phi2[t9])
    csc_phi3 = csc_phi2[t9].reshape(mm,4,1)
    csc_theta3 = csc_theta2[t9].reshape(mm,4,1)
    cnn_input = np.insert(csc_theta3.astype(int),[0], csc_phi3.astype(int), axis=2)
    
    return cnn_input, arr_y[t9,0]