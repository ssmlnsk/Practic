import datetime
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta

if __name__ == '__main__':
    ftime = '0 2022-06-09 08:00'
    stime = '600  2022-06-09 18:00'
    ftime = ftime.split()[2]
    stime = stime.split()[2]
    print(ftime+'-'+stime)

df = pd.DataFrame({"time":pd.date_range(start="8:00",
                                        end = "18:00",
                                        freq="T")})
print(df)

"""
df = pd.DataFrame({"time":pd.date_range(start="8:00",
                                        end = "18:00",
                                        freq="T")})
print(df)
"""

a = [
['10:00', 60],
['11:00', 30],
['15:00', 10],
['15:30', 10],
['16:50', 40]
]

for i in range(len(a)):
    print(a[i][1])
    print(datetime.strptime(a[i][0], '%H:%M'))
    print (datetime.strptime(a[i][0], '%H:%M') + timedelta(minutes=a[i][1]))