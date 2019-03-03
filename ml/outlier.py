import numpy as np
import datetime
from datetime import datetime
from datetime import time
import radar


# list of exit details in DateTime format
log = [] 

# random initialization
for i in range(100):
    newTime = radar.random_datetime(start='2012-05-24T00:00:00', stop='2012-05-24T02:59:59')
    log.append(newTime)


def outlier(log, value):
    
    hours = []
    minutes = []
    
    for timeval in log:
        time = timeval.strftime("%H:%M:%S")
        myhour, myminute, mysecond = time.split(':')
        hours.append(int(myhour) * 60)
        minutes.append(int(myminute))
    
    time_final = np.asarray(hours) + np.asarray(minutes)

    mytime = datetime.strptime(str(value),"%H:%M:%S")
    
    myhour = mytime.hour
    myminute = mytime.minute
    mysecond = mytime.second
   
    new_val = int(myhour) * 60 + int(myminute)
    
    time_mean = np.mean(np.asarray(time_final))
    time_std = np.std(np.asarray(time_final))

    z_score = np.abs(new_val - time_mean) / time_std
    print(z_score)

    if(z_score > 3):
        return True

    return False


currentTime = datetime.now().strftime("%H:%M:%S")
print(currentTime)
print(outlier(log, currentTime))