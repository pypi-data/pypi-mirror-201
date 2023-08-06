import json
import simpleworkspace as sw
from basetestcase import BaseTestCase
from simpleworkspace.types.time import TimeEnum

class ConversionTest(BaseTestCase):
    def test_Times_HasCorrectSeconds(self):
        self.assertEqual(TimeEnum.Day.value    * 2, 172800)
        self.assertEqual(TimeEnum.Hour.value   * 2, 7200)
        self.assertEqual(TimeEnum.Minute.value * 2, 120)

class AppTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        sw.App.Setup(self.testAppName, self.testAppCompany)

    def tearDown(self) -> None:
        super().tearDown()
        if self.testAppName in sw.App.path_currentAppData and self.testAppCompany in sw.App.path_currentAppData:
            sw.io.directory.Remove(sw.App.path_currentAppData)

    def test_settings_json(self):
        sw.App.settingsManager.LoadSettings()
        sw.App.settingsManager.Settings["test1"] = 10
        sw.App.settingsManager.Settings["test2"] = 20
        sw.App.settingsManager.SaveSettings()
        savedSettingData = sw.io.file.Read(sw.App.settingsManager._settingsPath)
        obj = json.loads(savedSettingData)
        self.assertEqual(obj, {"test1": 10, "test2": 20})

    def test_appdata_logging(self):
        sw.App.logger.debug("test log 1")
        sw.App.logger.debug("test log 2")
        sw.App.logger.debug("test log 3")
        for handler in sw.App.logger.handlers:
            handler.flush()
        logData = sw.io.file.Read(sw.App._loggerFilepath)
        result = sw.utility.regex.Match(f"/(.*?) (\w+?) <(.*?)>: (.*)/i", logData)
        
        self.assertEqual(len(result),  3)
        self.assertEqual(result[0][4],  "test log 1")
        self.assertEqual(result[1][4],  "test log 2")
        self.assertEqual(result[2][4],  "test log 3")
        pass
