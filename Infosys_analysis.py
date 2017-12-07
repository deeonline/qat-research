
# coding: utf-8

# ### Stock reversal on a daily data
# 
# In this notebook we'll explore how we can take
# 
# Input: A file with a particular stock's data (preferably daily but doesn't matter)
# 
# Output: Not concrete yet
# 
# Lets explore

# In[1]:

import pandas as pd
import seaborn as sns
import numpy as np
#get_ipython().magic('matplotlib inline')


# In[2]:

# Master Dictionaries to store various probabilities and absoulte numbers for each day
# Keys are dates eg '20091201'  
GR_ABS_DATE_WISE = {}
GR_PROB_DATE_WISE = {}
    
for month in ['12']:#['01','02','03','04','05','06','07','08','09','10','11', '12']:

    # The input file is data file having all trades of a particular security for 
    # the entire month
    filename = "DataSet/INFOSYSTCH/INFOSYSTCH_2008" + month
    
    df = pd.read_csv(filename, sep='|', names=['id','instrument','type','ts','Y','qty'])
    df['date'], df['id'] = df['id'].str.split('.', 1).str
    
    
    # In[3]:
    
    df.index = pd.to_datetime(df['date'] + ' ' + df['ts'])
    df['trade_size'] = df.Y*df.qty
    
    
    # In[23]:
    
    #Split into dictinoary with dates as keys 
    gb = df.groupby('date')
    t ={}
    for x in gb.groups:
        t[x] = gb.get_group(x)
    
    
    
    # various timespan for resmapling data
    timespans = ['tick','1s', '3s', '5s', '10s', '20s', '30s', '1T', '5T', '30T']
    
    
    
    # In[182]:
    
    
    for day_of_the_month in t:
        print("======", day_of_the_month)
        if(day_of_the_month in ['20090518','20080115','20081226']):
            #Handle special cases
            #20090518 Exception as trading was halted that day
            #20080115 - Issue in 5min - debug later 
            continue
        df = t[day_of_the_month]
        df = df[(df.ts > '09:15:00') & (df.ts < '15:29:29' )]
        GR_ABS = {}
        GR_PROB = {}
        for timespan in timespans:
            print ("======", timespan)
            if (timespan != 'tick'):
                # Resmapling based on timespans
                dfH = df.resample(timespan).sum().dropna()
                dfH.Y = dfH.trade_size/dfH.qty
            else:
                # Special case where no re-sampling is required
                dfH = df
    
            dfH['Y'] = dfH['Y'].round(2)
            dfH['ΔYt'] = dfH['Y'].diff().round(2)
    
            #Control depth as some timespans may have too sparse data
            if (timespan in ['5T']):
                memory = 6-2 #Used to configure lookback period
            elif(timespan in ['30T']):
                memory = 6-4
            else:
                #The script will break as there may be too few options in 30min time frame. Controlling the lookbakc period
                memory = 6
    
            width = 0.001 #Used to configure minimum price change movement to capture Eg 0.1 will treat any movement b/w -0.1 and 0.1 as none
    
            ## Old logic - not used
            boundaries = [-100,-width,width,100]
            #boundaries = [-100,-0.2,-0.1,0,0.1,0.2,100]
            #edge2 = [-2.795001e+01,-1.500000e-01,-5.000000e-02,5.000000e-02,1.500000e-01,2.740000e+01]
            l = [-1.0,0.0,1.0]
    
            dfH = dfH[dfH['ΔYt'] != 0.0]
            
            #dfH['ΔYt'] = pd.cut(dfH['ΔYt'],bins=boundaries,labels=l)
            #dfH.dropna(inplace=True)
            #dfH['ΔYt'] = dfH.ΔYt.astype(int)
            
            #New logic
            dfH['ΔYt'] = ((dfH['ΔYt'] > 0) * 1) + ((dfH['ΔYt'] < 0) * -1)
            
            col_list = ['ΔYt']
    
            #Create various ΔYt-i       
            for i in range(1,memory):
                col_name = 'ΔYt-' + str(i)
                dfH[col_name] = dfH['ΔYt'].shift(i).round(2)
                #dfH[col_name] = pd.cut(dfH[col_name],bins=boundaries,labels=l)
                #dfH.dropna(inplace=True)
                #dfH[col_name] = dfH[col_name].astype(int)
                col_list.append(col_name)
            dfH.dropna(inplace=True)
    
    
            #memory = 6
            #List to store probability tables for various depths
            gr_abs = []
            gr_prob = []
            for i in range(1,memory):
                #print("Depth:", i)
                gr = dfH.groupby(col_list[:i+1][::-1]).size()
                gr = gr.astype(float)
                GR = dfH.groupby(col_list[:i][::-1]).size()
                gr_abs.append(list(gr))
                if(gr.size == GR.size*2):
                    #print("======Absolute Numbers======")
                    #print (gr)
                    #print("======Prboabilities======")
                    for j in range(0,2**(i+1),2):
                        #print(j,gr.values[j],gr.values[j+1])
                        gr.values[j] = gr.values[j]/GR.values[j/2]
                        gr.values[j+1] = gr.values[j+1]/GR.values[j/2]
                    #print(gr)
                    gr_prob.append(gr)
    
            GR_ABS[timespan] = gr_abs
            GR_PROB[timespan] = gr_prob
        GR_ABS_DATE_WISE[day_of_the_month] =  GR_ABS
        GR_PROB_DATE_WISE[day_of_the_month] =  GR_PROB
    
    




