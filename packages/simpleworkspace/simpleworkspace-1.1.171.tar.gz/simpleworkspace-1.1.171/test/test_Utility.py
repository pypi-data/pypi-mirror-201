import os
import simpleworkspace as sw
import time
from simpleworkspace.utility.stopwatch import StopWatch
import gzip
from basetestcase import BaseTestCase

class Utility_RegexTests(BaseTestCase):
    sampleText = "Hello person1 with short hair\n" "Hello person2 with shoes\n" "Hello person3 with jacket\n" "this is a new walkthrough of version 1.2.8.12 of this app\n" "older available versions are following: v1.2.8.11, v1.2.8.10, v1.2.5.1, v1.1.2.9,\n" "good luck\n"

    def test_Regex_replace_flag_MultiLine(self):
        res = sw.utility.regex.Replace(r"/^Hello person(.) /", r"Hello bobby0 ", self.sampleText)
        resReplaced = sw.utility.regex.Match(r"/bobby. /i", res)
        self.assertEqual(len(resReplaced) , 3)
        self.assertEqual(resReplaced[0][0], "bobby0 ")

        res = sw.utility.regex.Replace(r"/person(.) /", r"bobby\1 ", self.sampleText)
        resReplaced = sw.utility.regex.Match(r"/bobby. /i", res)
        self.assertEqual(len(resReplaced) , 3)
        self.assertEqual(resReplaced[0][0], "bobby1 ")
        self.assertEqual(resReplaced[1][0], "bobby2 ")

        result = sw.utility.regex.Replace(r"/hej (.*?) /i", r"bye \1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3")  # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"
        self.assertEqual(result,  "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3")

    def test_Regex_replace_flag_DotAll(self):
        res = sw.utility.regex.Replace(r"/^Hello person(.) /s", r"bobby0 ", self.sampleText)
        resReplaced = sw.utility.regex.Match(r"/bobby. /i", res)
        self.assertEqual(len(resReplaced),  1)
        self.assertEqual(resReplaced[0][0],  "bobby0 ")

    def test_Regex_Match_flag_MultiLine(self):
        res = sw.utility.regex.Match(r"/^Hello (person.*?) /", self.sampleText)
        self.assertEqual(res[0][0],  "Hello person1 ")
        self.assertEqual(res[0][1],  "person1")

        self.assertEqual(res[1][0],  "Hello person2 ")
        self.assertEqual(res[1][1],  "person2")

        self.assertEqual(res[2][0],  "Hello person3 ")
        self.assertEqual(res[2][1],  "person3")
        self.assertEqual(len(res[0]),  2)
        self.assertEqual(len(res),  3)

    def test_Regex_Match_flag_DotAll(self):
        res = sw.utility.regex.Match(r"/^Hello (person.*?) /s", self.sampleText)
        self.assertEqual(res[0][0],  "Hello person1 ")
        self.assertEqual(res[0][1],  "person1")
        self.assertEqual(len(res[0]),  2)
        self.assertEqual(len(res),  1)

        res = sw.utility.regex.Match(r"/^Hello.*(with) (jacket)/s", self.sampleText)
        self.assertEqual(res[0][0],  "Hello person1 with short hair\nHello person2 with shoes\nHello person3 with jacket")
        self.assertEqual(len(res[0]),  3)
        self.assertEqual(len(res),  1)

    def test_Regex_flag_CaseSensitivity(self):
        res = sw.utility.regex.Match(r"/hello person\d/", self.sampleText)
        self.assertEqual(res,  None)
        res = sw.utility.regex.Match(r"/Hello person\d/", self.sampleText)
        self.assertEqual(res[0][0],  "Hello person1")
        self.assertEqual(res[1][0],  "Hello person2")
        self.assertEqual(res[2][0],  "Hello person3")
        self.assertEqual(len(res[0]),  1)
        self.assertEqual(len(res),  3)
class Utility_StopWatchTest(BaseTestCase):
    def AccurateSleepMS(self, ms):
        start = time.perf_counter()
        time.sleep(ms / 1000)
        elapsed = time.perf_counter() - start
        return elapsed * 1000

    def InDistance(self, val1, val2, maxDistance):
        distance = abs(val1 - val2)
        if distance > maxDistance:
            return False
        return True

    def test_HappyFlow(self):
        #we do delta 1ms resolution, this means that just retrieving the time from stopwatch may take up to 1ms in theory
        allowedDiffMS = 1
        stopWatch = StopWatch()

        res = stopWatch.GetElapsedMilliseconds()
        self.assertEqual(res, 0)

        stopWatch.Start()
        actualSleepTime = self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        # should do nothing since already running
        stopWatch.Start()
        stopWatch.Start()

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        self.AccurateSleepMS(1)  # skip this, since we just want to check if not counted after Stopped timer
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        stopWatch.Start()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= allowedDiffMS)

        stopWatch.Reset()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertEqual(res, 0, f"should be 0 ms since we resetted time")
class Utility_RotatingLogFileReader(BaseTestCase):
    def CreateLog(self, logname = "tmp.log"):
        logPath = f"{self.testPath}/{logname}"
        sw.io.file.Create(logPath, "1\n2\n3\n")
        return logPath
    
    def CreateLog_Delayed_NoCompressions(self):
        logpath = self.CreateLog()
        os.rename(logpath, logpath + ".1")
        sw.io.file.Create(logpath, "4\n5\n6\n")
        return logpath
    
    def CreateLog_Delayed_WithCompressions(self):
        logpath = self.CreateLog_Delayed_NoCompressions()

        with open(f"{logpath}.1", 'rb') as f_in, gzip.open(f"{logpath}.2.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        os.replace(f"{logpath}", f"{logpath}.1")
        sw.io.file.Create(logpath, "7\n8\n9\n")
        return logpath
    
    def CreateLog_WithCompression(self):
        logpath = self.CreateLog()
        
        with open(f"{logpath}", 'rb') as f_in, gzip.open(f"{logpath}.1.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        sw.io.file.Create(logpath, "4\n5\n6\n")
        return logpath
    

    def test_SingleLogFile(self):
        logpath = self.CreateLog()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n"
        )

    def test_DelayedLog_withNoCompressedFiles(self):
        logpath = self.CreateLog_Delayed_NoCompressions()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )
    
    def test_DelayedLog_withCompressedFiles(self):
        logpath = self.CreateLog_Delayed_WithCompressions()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n7\n8\n9\n"
        )

    def test_OnlyCompressedFiles(self):
        logpath = self.CreateLog_WithCompression()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )