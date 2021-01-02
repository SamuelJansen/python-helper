from python_helper.api.test.api.src.service import StringHelperTest
from python_helper.api.test.api.src.service import SettingHelperTest
from python_helper.api.test.api.src.service import LogHelperTest
from python_helper.api.test.api.src.service import ObjectHelperTest
from python_helper.api.test.api.src.service import ReflectionHelperTest
from python_helper.api.test.api.src.service import RandomHelperTest
from python_helper.api.test.api.src.service import MethodAnnotationTest

SettingHelperTest.updateActiveEnvironment_withSuccess()
SettingHelperTest.mustReadSettingFile()
SettingHelperTest.mustNotReadSettingFile()
SettingHelperTest.mustPrintSettingTree()
SettingHelperTest.querySetting_withSuccess()
SettingHelperTest.mustHandleSettingValueInFallbackSettingTree()

StringHelperTest.mustFilterSetting()
StringHelperTest.prettyJson_withSucces()
StringHelperTest.prettyPython_withSucces()
StringHelperTest.filterJson_withSucces()
StringHelperTest.isLongString_withSuccess()

LogHelperTest.mustLogWithColors()
LogHelperTest.mustLogWithoutColors()
LogHelperTest.mustLogWithoutColorsAsWell()
LogHelperTest.mustLogEnvironmentSettings()
LogHelperTest.mustLogPretyPythonWithoutColors()
LogHelperTest.mustLogPretyPythonWithColors()
LogHelperTest.mustLogPretyJsonWithColors()

ObjectHelperTest.basicMethods()
ObjectHelperTest.mustAssertEquals()
ObjectHelperTest.mustIgnoreKeyCorrectly()

ReflectionHelperTest.isNotMethodInstance_withSuccess()
ReflectionHelperTest.overrideSignatures_withSuccess()
ReflectionHelperTest.getArgsOrder_withSuccess()

RandomHelperTest.sample_withSuccess()
RandomHelperTest.randomValues()

MethodAnnotationTest.Function_withSuccess()
MethodAnnotationTest.Method_withSuccess()
MethodAnnotationTest.FunctionThrough_withSuccess()
