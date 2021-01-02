from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, EnvironmentHelper
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.helper import StringHelperHelper, SettingHelperHelper

global ACTIVE_ENVIRONMENT_VALUE
ACTIVE_ENVIRONMENT_VALUE = None

ACTIVE_ENVIRONMENT = 'ACTIVE_ENVIRONMENT'
DEFAULT_ENVIRONMENT = 'default'
LOCAL_ENVIRONMENT = 'local'

def logEnvironmentSettings() :
    try :
        LogHelper.setting(logEnvironmentSettings, StringHelper.prettyJson(EnvironmentHelper.getActiveEnvironmentVariableSet()))
    except Exception as exception :
        LogHelper.failure(logEnvironmentSettings, 'Not possible do get a pretty json from EnvironmentHelper.getActiveEnvironmentVariableSet()', exception)
        LogHelper.setting(logEnvironmentSettings, EnvironmentHelper.getActiveEnvironmentVariableSet())

def updateActiveEnvironment(activeEnvironment) :
    global ACTIVE_ENVIRONMENT_VALUE
    ACTIVE_ENVIRONMENT_VALUE = activeEnvironment if ObjectHelper.isNotNone(activeEnvironment) else DEFAULT_ENVIRONMENT
    EnvironmentHelper.updateEnvironmentValue(ACTIVE_ENVIRONMENT, ACTIVE_ENVIRONMENT_VALUE, avoidRecursiveCall=True)
    return ACTIVE_ENVIRONMENT_VALUE

def getActiveEnvironment() :
    global ACTIVE_ENVIRONMENT_VALUE
    if ObjectHelper.isEmpty(ACTIVE_ENVIRONMENT_VALUE) :
        activeEnvironment = EnvironmentHelper.getEnvironmentValue(ACTIVE_ENVIRONMENT)
        ACTIVE_ENVIRONMENT_VALUE = activeEnvironment if ObjectHelper.isNotEmpty(activeEnvironment) else DEFAULT_ENVIRONMENT
    return ACTIVE_ENVIRONMENT_VALUE

def activeEnvironmentIsDefault() :
    global ACTIVE_ENVIRONMENT_VALUE
    return DEFAULT_ENVIRONMENT == ACTIVE_ENVIRONMENT_VALUE

def activeEnvironmentIsLocal() :
    global ACTIVE_ENVIRONMENT_VALUE
    return LOCAL_ENVIRONMENT == ACTIVE_ENVIRONMENT_VALUE

def getSettingTree(settingFilePath, settingTree=None, keepDepthInLongString=False, depthStep=c.TAB_UNITS, fallbackSettingTree=None) :
    with open(settingFilePath,c.READ,encoding=c.ENCODING) as settingsFile :
        allSettingLines = settingsFile.readlines()
    settingInjectionList = []
    longStringCapturing = False
    quoteType = None
    longStringList = None
    depth = 0
    nodeRefference = 0
    nodeKey = c.NOTHING
    if settingTree is None :
        settingTree = {}
    for line, settingLine in enumerate(allSettingLines) :
        if SettingHelperHelper.lineAproved(settingLine) :
            if longStringCapturing :
                if not currentDepth :
                    currentDepth = 0
                longStringList.append(depthStep*c.SPACE + settingLine if keepDepthInLongString else settingLine[depth:])
                if quoteType in str(settingLine) :
                    longStringList[-1] = c.NOTHING.join(longStringList[-1].split(quoteType))[:-1] + quoteType
                    settingValue = c.NOTHING.join(longStringList)
                    nodeKey = SettingHelperHelper.updateSettingTreeAndReturnNodeKey(settingKey,settingValue,nodeKey,settingTree)
                    longStringCapturing = False
                    quoteType = None
                    longStringList = None
            else :
                currentDepth = SettingHelperHelper.getDepth(settingLine)
                if currentDepth == depth :
                    settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                        settingLine,
                        nodeKey,
                        settingTree,
                        longStringCapturing,
                        quoteType,
                        longStringList,
                        settingInjectionList
                    )
                elif currentDepth > depth :
                    currentNodeRefference = currentDepth // (currentDepth - depth)
                    if currentNodeRefference - nodeRefference == 1 :
                        settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                            settingLine,
                            nodeKey,
                            settingTree,
                            longStringCapturing,
                            quoteType,
                            longStringList,
                            settingInjectionList
                        )
                        nodeRefference = currentNodeRefference
                        depth = currentDepth
                elif currentDepth < depth :
                    nodeRefference = currentDepth // depthStep
                    depth = currentDepth
                    splitedNodeKey = nodeKey.split(c.DOT)[:nodeRefference]
                    splitedNodeKeyLength = len(splitedNodeKey)
                    if splitedNodeKeyLength == 0 :
                        nodeKey = c.NOTHING
                    elif splitedNodeKeyLength == 1 :
                        nodeKey = splitedNodeKey[0]
                    else :
                        nodeKey = c.DOT.join(splitedNodeKey)
                    settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                        settingLine,
                        nodeKey,
                        settingTree,
                        longStringCapturing,
                        quoteType,
                        longStringList,
                        settingInjectionList
                    )
                    depth = currentDepth
    SettingHelperHelper.handleSettingInjectionList(settingInjectionList, settingTree, fallbackSettingTree=fallbackSettingTree)
    updateSettingTree(settingTree, fallbackSettingTree)
    return settingTree

def updateSettingTree(toUpdateSettingTree, gatheringSettingTree) :
    if ObjectHelper.isNotEmpty(gatheringSettingTree) :
        if ObjectHelper.isNone(toUpdateSettingTree) or StringHelper.isBlank(toUpdateSettingTree) :
            toUpdateSettingTree = {}
        if ObjectHelper.isCollection(gatheringSettingTree) and ObjectHelper.isNotEmpty(gatheringSettingTree) :
            for key,value in gatheringSettingTree.items() :
                if ObjectHelper.isNotEmpty(value) :
                    if key not in toUpdateSettingTree or ObjectHelper.isEmpty(toUpdateSettingTree[key]) :
                        toUpdateSettingTree[key] = value
                    else :
                        updateSettingTree(toUpdateSettingTree[key], gatheringSettingTree[key])
                elif key not in toUpdateSettingTree :
                    toUpdateSettingTree[key] == value

def getSetting(nodeKey,settingTree) :
    setting = None
    try :
        setting = SettingHelperHelper.accessTree(nodeKey,settingTree)
    except Exception as exception :
        LogHelper.failure(getSetting,f'Not possible to get {nodeKey} node key. Returning "{setting}" by default', exception)
    return StringHelper.filterString(setting) if isinstance(setting, str) else setting

def querySetting(keywordQuery,tree) :
    if StringHelper.isBlank(keywordQuery) or ObjectHelper.isNotDictionary(tree) :
        LogHelper.warning(querySetting,f'''Not possible to parse "{tree}". It's either is not a dictionary or "{keywordQuery}" keyword query is blank''')
    querySet = {}
    SettingHelperHelper.keepSearching(keywordQuery,tree,querySet)
    return querySet

def printSettings(tree,name,depth=1,withColors=activeEnvironmentIsLocal()):
    withColors = activeEnvironmentIsLocal()
    settingKeyColor = SettingHelperHelper.getSettingKeyPrompColor(withColors)
    colonColor = SettingHelperHelper.getSettingColonPrompColor(withColors)
    print(f'{c.NEW_LINE}{settingKeyColor}{c.OPEN_LIST}{name.upper()}{c.CLOSE_LIST}{colonColor}{c.SPACE}{c.COLON}')
    SettingHelperHelper.printNodeTree(
        tree,
        depth,
        settingKeyColor = settingKeyColor,
        settingValueColor = SettingHelperHelper.getSettingValuePrompColor(withColors),
        colonColor = colonColor,
        resetColor = SettingHelperHelper.getSettingResetPrompColor(withColors)
    )
    print()
