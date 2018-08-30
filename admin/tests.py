from django.test import TestCase

# Create your tests here.
#带有参数的装饰器
import time

def deco(func):
    def wrapper(a,b):
        startTime = time.time()
        func(a,b)
        endTime = time.time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
    return wrapper


@deco
def func(a,b):
    print("hello，here is a func for add :")
    time.sleep(1)
    print("result is %d" %(a+b))

func(2,3)
    #func()