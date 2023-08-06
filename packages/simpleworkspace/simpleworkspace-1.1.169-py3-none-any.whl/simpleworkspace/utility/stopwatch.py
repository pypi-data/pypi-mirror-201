import time as _time
from typing import Callable

class StopWatch:
    def __init__(self) -> None:
        self.timeHistory = []
        self.__timeElapsed = 0
        self.__isRunning = False

    def Start(self):
        if(self.__isRunning):
            return
        self.__isRunning = True
        self.timeHistory.append({
            "timestamp": _time.perf_counter(),
            "isStartEvent": True
        })
        self.__UpdateTimeElapsed()
        return
    
    def Stop(self):
        if not(self.__isRunning):
            return
        self.__isRunning = False
        self.timeHistory.append({
            "timestamp": _time.perf_counter(),
            "isStartEvent": False
        })
        return
    def Reset(self):
        '''Stops and resets the timer'''
        self.__init__()
        return

    def __UpdateTimeElapsed(self):
        endTime = _time.perf_counter() #take end time directly to avoid spending time while calculating
        self.__timeElapsed = 0
        startTime = None
        for timeEvent in self.timeHistory:
            if(timeEvent["isStartEvent"]):
                startTime = timeEvent["timestamp"]
                continue
            self.__timeElapsed += timeEvent["timestamp"] - startTime
            startTime = None
        if(startTime is not None):
            self.__timeElapsed += endTime - startTime

    def RecordedCall(self, action: Callable):
        '''Starts the timer, runs the action/callback and then stops the timer and returns action results'''
        self.Start()
        res = action()
        self.Stop()
        return res

    def _PrecisionConverter(self, value:float|int, decimalPrecision:int):
        if(decimalPrecision < 1):
            decimalPrecision = None #None as decimalPrecision strips all decimals and returns int, but precision of even 0 returns a float 1.0
        return round(value, decimalPrecision) 

    def GetElapsedSeconds(self, decimalPrecision:int = None) -> float: 
        '''
        @param decimalPrecision: specify how many decimals you want in resulting time, the default None does no rounding and returns max precision
        @returns elapsed time in seconds with high precision
        '''
        self.__UpdateTimeElapsed()
        timeElapsed = self.__timeElapsed
        if(decimalPrecision is not None):
            timeElapsed = self._PrecisionConverter(timeElapsed, decimalPrecision)
        return timeElapsed

    def GetElapsedMilliseconds(self, decimalPrecision:int = None):
        '''
        @param decimalPrecision: specify how many decimals you want in resulting time, the default None does no rounding and returns max precision
        @returns elapsed time in milliseconds with high precision
        '''
        
        timeElapsed = self.GetElapsedSeconds() * 1000
        if(decimalPrecision is not None):
            timeElapsed = self._PrecisionConverter(timeElapsed, decimalPrecision)
        return timeElapsed
    
    def ToString(self, decimalPrecision:int = None) -> str:
        '''
        @param decimalPrecision: specify how many decimals you want in resulting time, the default None does no rounding and returns max precision
        @returns elapsed time in seconds with high precision as string, example "1.00202312323"
        '''

        return str(self.GetElapsedSeconds(decimalPrecision=decimalPrecision))


