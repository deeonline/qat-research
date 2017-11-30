# -*- coding: utf-8 -*-
#print(GR_ABS_DATE_WISE)

date_of_year = '20100119'
timespan = 'tick'

timespans = ['tick','1s', '3s', '5s', '10s', '20s', '30s', '1T', '5T']


Prob_df = pd.DataFrame()

for timespan in timespans:
    ConditionalProb = {}
    Prob = {}
    for date_of_year in GR_PROB_DATE_WISE.keys():
    
        #print(date_of_year)
        ConditionalProb[date_of_year] = GR_PROB_DATE_WISE[date_of_year][timespan][0].values[1]
        Prob[date_of_year] = (GR_ABS_DATE_WISE[date_of_year][timespan][0][1] + GR_ABS_DATE_WISE[date_of_year][timespan][0][3])/sum(GR_ABS_DATE_WISE[date_of_year][timespan][0])
        
    
    Prob_df['P(+|-)'+timespan] = pd.DataFrame([ConditionalProb, Prob]).T[0]
    Prob_df['P(+)'+timespan] = pd.DataFrame([ConditionalProb, Prob]).T[1]
    
    print("=========Timespan:",timespan)
    print(ttest_ind(Prob_df['P(+|-)'+timespan].values,Prob_df['P(+)'+timespan].values))
    
    
    
#Prob_df['P(+|-)tick'].values
