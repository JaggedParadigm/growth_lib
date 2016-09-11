import datetime
import time
import numpy as np

def project_growth(start_time=[],final_OD=[],
                    end_time=[],doubling_time=[],measured_OD=[],
                    specific_growth_rate=[],number_points=10,t0=0.0):
    """
    Projects growth 
    """
    # Check inputs
    _check_inputs(doubling_time=doubling_time,final_OD=final_OD,
                           specific_growth_rate=specific_growth_rate)
    
    # Calculate time difference between now or start time and end time
    time_difference = _calc_time_interval(start_time=start_time,end_time=end_time)

    # Save variables with shorter names for equation readability
    N = number_points
    delt = time_difference
    if doubling_time:
        mu = np.log(2.0)/doubling_time
    else:
        mu = specific_growth_rate
    C_f = final_OD
    
    time_series = np.array([t0+i*delt/N for i in range(N+1)])
    
    C = lambda t: C_f*np.exp(mu*(t-delt))
    
    return [time_series,C(time_series)]
    
    
    
def _check_inputs(doubling_time=[],final_OD=[],specific_growth_rate=[]):
    # Check that only doubling time or specific growth rate specified (not both)
    if specific_growth_rate and doubling_time:
        raise NameError('\nThe maximum specific growth rate and doubling time cannot be specified at the same time\n')
    elif not specific_growth_rate and not doubling_time:
        raise NameError('\nEither the specific growth rate or doubling time must be specified\n')
    
    # Check that all necessary keyword arguments are present
    if not final_OD:
        raise NameError('\nFinal OD keyword argument, final_OD, must be specifed\n')    
    
def calc_preculture_volume(culture_volume=[],start_time=[],final_OD=[],
                            end_time=[],doubling_time=[],measured_OD=[],
                            specific_growth_rate=[],detailed_flag=False):
    """
    Calculates the amount of exponential phase culture to add
    to a new culture to acheive a particular cell concentration (OD)
    at a particular time
    
    -----------------------------------------------------------------------------------
    Variable name           Type    Description
    -----------------------------------------------------------------------------------
    culture_volume          float   Cultural volume in mL (Ex: 40.0)
    start_time              str     Starting time in format '%I:%M %p' (Ex: '5:34 PM').                                    
    final_OD                float   Final desired cell concentration in OD_600 units
                                    (Ex: 0.7). 
    end_time                str     Starting time in format '%I:%M %p' (Ex: '9:30 AM').
                                    (time I'd use often)
    doubling_time           float   Strain doubling time in hours. Only this or the 
                                    specific growth rate must be specific. (Ex: 3.4).
    specific_growth_rate    float   Maximum specific growth rate in 1/h.
                                    Only this or the doubling time can be specified.
                                    (Ex: 0.2).
    measured_OD             float   Measured exponential culture concentration (OD_600)
    -----------------------------------------------------------------------------------
    """
    # Check inputs
    if not culture_volume:
        raise NameError('\nCulture volume keyword argument, culture_volume, must be specifed\n')
    if not measured_OD.any():
        raise NameError('\nMeasured OD must be specific\n')
    _check_inputs(doubling_time=doubling_time,final_OD=final_OD,
                           specific_growth_rate=specific_growth_rate)
        
    # Calculate time difference between now or start time and end time
    time_difference = _calc_time_interval(start_time=start_time,end_time=end_time)
    
    # Save variables with shorter names for equation readability
    OD = final_OD
    delt = time_difference
    mu = np.log(2.0)/doubling_time
    OD_c = measured_OD
    V_m = culture_volume
    
    # Calculate volume of exponential culture to add to flask with medium
    if not detailed_flag:
        V_a = V_m/(OD_c*np.exp(mu*delt)/OD)
    else:
        V_a = V_m/(OD_c*np.exp(mu*delt)/OD-1)
    
    # Return volume to add
    return V_a
    
def _calc_time_interval(start_time=[],end_time=[]):
    """
    Returns time difference from the start time today until
    the end time tomorrow in hours given an optional starting
    time (default is the current time) and a desired end time
    """
    # Check data inputs
    if not end_time:
        raise NameError('End/final time keyword argument, end_time, must be specifed\n')
    
    # Get current time
    current_datetime = datetime.datetime.now()

    # Convert start time to time object if given
    if start_time:
        start_time = time.strptime(start_time,'%I:%M %p')
        datetime_replace_kwargs = {
            'hour': start_time.tm_hour,
            'minute': start_time.tm_min,
            'second': 0,
            'microsecond': 0
        }
        start_time = current_datetime
        start_time.replace(**datetime_replace_kwargs)
    
    # Convert desired time into time object
    end_time = time.strptime(end_time,'%I:%M %p')
    
    # Convert end_time into datetime object corresponding to that time tomorrow
    tommorrows_datetime = current_datetime + datetime.timedelta(days=1)
    datetime_replace_kwargs = {
        'hour': end_time.tm_hour,
        'minute': end_time.tm_min,
        'second': 0,
        'microsecond': 0
    }
    end_time = tommorrows_datetime.replace(**datetime_replace_kwargs)
    
    # Make start_time the current_datetime if not provided by user
    if not start_time:
        start_time = current_datetime
    
    # Calculate difference in time in hours
    time_difference = (end_time-start_time).total_seconds()/60.0/60.0
    
    # Return time difference
    return time_difference

if __name__ == '__main__':
    kwargs = {
        'start_time': '3:45 PM',
        'culture_volume': 60.0, # mL
        'final_OD': 0.7,
        'desired_time': '9:30 AM',
        'measured_OD': 5*np.array([0.3435]),
        'doubling_time': 3.4
    }

    print calc_culture_dilution(**kwargs)