import time
import datetime

__author__ = "Antonio Lima"
__author_email__ = "anto87@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2013-2014 Antonio Lima"

class greedy(object):
    def __init__(self, max_calls, time_interval):
        assert max_calls > 0
        assert time_interval > 0
        self.__last_reset = None
        self.__max_calls = max_calls
        self.__time_interval = time_interval # seconds
        self.__numcalls = 0

    def __call__(self, f, *args, **kwargs):
        def wrapped_f(*args, **kwargs):
            # At the first call, reset the time
            if self.__last_reset == None:
                self.__last_reset = datetime.datetime.now()

            if self.__numcalls >= self.__max_calls:
                time_delta = datetime.datetime.now() - self.__last_reset
                time_delta = int(time_delta.total_seconds()) + 1
                if time_delta <= self.__time_interval:
                    time.sleep(self.__time_interval - time_delta + 1)
                    self.__numcalls = 0
		    self.__last_reset = datetime.datetime.now()

            self.__numcalls += 1
            return f(*args, **kwargs)
        return wrapped_f

    def __numcalls__(self):
        return self.__numcalls

class patient(object):
    def __init__(self, max_calls, time_interval):
        assert max_calls > 0
        assert time_interval > 0
        self.__last_call = None
        self.__time_interval = float(time_interval) / max_calls # seconds

    def __call__(self, f, *args, **kwargs):
        def wrapped_f(*args, **kwargs):
            now = datetime.datetime.now()
            # At the first call, reset the time
            if self.__last_call == None:
                self.__last_call = now
                result = f(*args, **kwargs)
                return result

            time_delta = now - self.__last_call
            time_delta = int(time_delta.total_seconds())
            assert time_delta >= 0
            if time_delta <= self.__time_interval:
                to_sleep = self.__time_interval - time_delta
                # print "To sleep", to_sleep
                time.sleep(to_sleep)

            result = f(*args, **kwargs)
            self.__last_call = datetime.datetime.now()
            return result
        return wrapped_f

    def __numcalls__(self):
        return self.__numcalls

if __name__ == "__main__":
    # Example: func1 can be called not more than 30 times every minute
    # Once the limit 30 is reached, it sleeps until the minute is elapsed.
    @greedy(15,10)
    def func1(i):
        print "I am greedily called for the #{} time".format(i)

    for i in xrange(30):
        func1(i)

    # Example: func2 also can't be called not more than 30 times every minute, but
    # tries to enforce this behavior by limiting the interval between two
    # subsequent calls (in this case every 2 seconds)
    @patient(15,10)
    def func2(i):
        print "I am patiently called for the #{} time".format(i)


    for i in xrange(30):
        func2(i)
