import os, sys
import time

print('>>>>>> ARIMA_MA print argv')

for i in range(5):
    time.sleep(1)

for arg in sys.argv:
    print('Arg Value = ', arg)

print('>>>>>> ARIMA_MA print env variables')
for a in os.environ:
    print(a, '=', os.getenv(a))

print('>>>>>> ARIMA_MA done')