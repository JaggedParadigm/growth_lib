import datetime
import time
import numpy as np

def calc_culture_dilution(culture_volume=40.0,start_time=[],final_OD = 0.2,desired_time='9:30 AM'):
    """
    Calculates the amount of exponential phase culture to add
    to a new culture to acheive a particular cell concentration (OD)
    at a particular time
    """
    start_time = []
    culture_volume = 40.0 # mL
    final_OD = 0.7
    desired_time = '9:30 AM'
    measured_OD = 5*np.array([0.3435])
    td = 3.4
    
    # Parse desired time into time object
    desired_time = time.strptime(desired_time,'%I:%M %p')
    
    # Get current time
    current_datetime = datetime.datetime.now()
    
    # Convert desired_time into datetime object corresponding to that time tomorrow
    tommorrows_datetime = current_datetime + datetime.timedelta(days=1)
    desired_time = tommorrows_datetime.replace(hour=desired_time.tm_hour,minute=desired_time.tm_min,second=0,microsecond=0)
    
    time_difference = (desired_time-current_datetime).total_seconds()/60.0/60.0
    
    Vco = final_OD/measured_OD/np.exp(np.log(2)/td*time_difference)*culture_volume
    
    print Vco

if __name__ == '__main__':
    startTime = [] #'5:38 PM'
    #la
    #ODm                             = 5*array([0.3435])
    
    timeEnd = '9:30 AM'
    OD = 0.7
    V = 60.0
    td = 3.4 #2.00

    calc_culture_dilution()
    
    #testObj                         = GrowthCalculator(ODm,startTime=startTime,timeEnd=timeEnd,OD=OD,V=V,td=td)    
