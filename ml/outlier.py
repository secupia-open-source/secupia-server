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


def outlier(logs, value): 
    hours = []
    minutes = []
    
    for timeval in logs:
        time = timeval.strftime("%H:%M:%S")
        myhour, myminute, mysecond = time.split(':')
        hours.append(int(myhour) * 60)
        minutes.append(int(myminute))
    
    time_final = np.asarray(hours) + np.asarray(minutes)

    mytime = datetime.strptime(str(value),"%H:%M:%S")
    myhour = mytime.hour
    myminute = mytime.minute
    # mysecond = mytime.second
   
    newVal = int(myhour) * 60 + int(myminute)
    
    meanTime = np.mean(np.asarray(time_final))
    stdTime = np.std(np.asarray(time_final))

    zscore = np.abs(newVal - meanTime) / stdTime
    print(zscore)

    # general threshold for use is 3
    if(zscore > 3):
        return True

    return False


currentTime = datetime.now().strftime("%H:%M:%S")
print(currentTime)
print(outlier(log, currentTime))