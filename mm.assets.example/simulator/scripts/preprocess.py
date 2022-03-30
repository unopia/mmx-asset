import os, sys

print('>>>>>> print argv')
for arg in sys.argv:
    print('Arg Value = ', arg)

print('>>>>>> print env variables')
for a in os.environ:
    print(a, '=', os.getenv(a))

print('>>>>>> done')