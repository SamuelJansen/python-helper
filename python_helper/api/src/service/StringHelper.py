from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import ObjectHelper
from python_helper.api.src.helper import StringHelperHelper

PAST = 'past'
PRESENT = 'present'
FUTURE = 'future'

def isBlank(thing) :
    return isinstance(thing, str) and c.BLANK == thing

def isNotBlank(thing) :
    return isinstance(thing, str) and not c.BLANK == thing

def filterJson(json, extraCharacterList=None) :
    charactereList = [c.NEW_LINE,c.BAR_N]
    if isinstance(extraCharacterList, list) :
        charactereList += extraCharacterList
    filteredJson = json
    for charactere in charactereList :
        filteredJson = removeCharactere(charactere,filteredJson)
    return filteredJson.replace(c.SYSTEM_TAB,c.TAB)

def removeCharactere(charactere,string) :
    if isNotBlank(charactere) and isNotBlank(string) :
        filteredString = c.BLANK.join(string.strip().split(charactere))
        return filteredString.replace(charactere,c.BLANK)
    return string

def join(stringList, character=c.BLANK):
    return character.join(stringList)

def prettyPython(
        outterValue,
        quote = c.SINGLE_QUOTE,
        tabCount = 0,
        nullValue = c.NONE,
        trueValue = c.TRUE,
        falseValue = c.FALSE,
        withColors = False,
        joinAtReturn = True
    ) :
    '''It always sort sets'''
    if ObjectHelper.isCollection(outterValue) :
        if isinstance(outterValue, list) :
            collectionType = c.TYPE_LIST
        elif isinstance(outterValue, set) :
            collectionType = c.TYPE_SET
        elif isinstance(outterValue, tuple):
            collectionType = c.TYPE_TUPLE
        elif isinstance(outterValue, dict) :
            collectionType = c.TYPE_DICT
        else :
            raise Exception(f'Unexpected collection: {outterValue}')
        return StringHelperHelper.prettyCollection(
            StringHelperHelper.getValueCollection(outterValue),
            collectionType,
            quote,
            prettyPython,
            tabCount,
            nullValue,
            trueValue,
            falseValue,
            withColors = withColors,
            joinAtReturn = joinAtReturn
        )
    else :
        return StringHelperHelper.prettyInstance(
            outterValue,
            quote,
            prettyPython,
            tabCount,
            nullValue,
            trueValue,
            falseValue,
            withColors = withColors,
            joinAtReturn = joinAtReturn
        )

def prettyJson(
        outterValue,
        quote = c.DOUBLE_QUOTE,
        tabCount = 0,
        nullValue = c.NULL_VALUE,
        trueValue = c.TRUE_VALUE,
        falseValue = c.FALSE_VALUE,
        withColors = False,
        joinAtReturn = True
    ) :
    '''It always sort sets'''
    if ObjectHelper.isCollection(outterValue) :
        if isinstance(outterValue, list) or isinstance(outterValue, set) or isinstance(outterValue, tuple) :
            collectionType = c.TYPE_LIST
        elif isinstance(outterValue, dict) :
            collectionType = c.TYPE_DICT
        else :
            raise Exception(f'Unexpected collection: {outterValue}')
        return StringHelperHelper.prettyCollection(
            StringHelperHelper.getValueCollection(outterValue),
            collectionType,
            quote,
            prettyJson,
            tabCount,
            nullValue,
            trueValue,
            falseValue,
            withColors = withColors,
            joinAtReturn = joinAtReturn
        )
    else :
        return StringHelperHelper.prettyInstance(
            outterValue,
            quote,
            prettyJson,
            tabCount,
            nullValue,
            trueValue,
            falseValue,
            withColors = withColors,
            joinAtReturn = joinAtReturn
        )

def filterString(string) :
    if ObjectHelper.isNone(string) or not isinstance(string, str) :
        return string
    strippedString = string.strip()
    if c.BLANK == strippedString :
        return strippedString
    if strippedString[-1] == c.NEW_LINE :
        strippedString = strippedString[:-1]
    surroundedBySingleQuote = strippedString.startswith(c.SINGLE_QUOTE) and strippedString.endswith(c.SINGLE_QUOTE) and not (c.SINGLE_QUOTE*2 == strippedString or c.TRIPLE_SINGLE_QUOTE == strippedString)
    surroundedByDoubleQuote = strippedString.startswith(c.DOUBLE_QUOTE) and strippedString.endswith(c.DOUBLE_QUOTE) and not (c.DOUBLE_QUOTE*2 == strippedString or c.TRIPLE_DOUBLE_QUOTE == strippedString)
    if c.HASH_TAG in strippedString and not (surroundedBySingleQuote or surroundedByDoubleQuote) :
        strippedString = filterString(c.HASH_TAG.join(strippedString.split(c.HASH_TAG)[:-1]))
    if strippedString and (
            (
                strippedString.startswith(c.TRIPLE_SINGLE_QUOTE) and
                strippedString.endswith(c.TRIPLE_SINGLE_QUOTE) and
                not c.TRIPLE_SINGLE_QUOTE == strippedString
            ) or
            (
                strippedString.startswith(c.TRIPLE_DOUBLE_QUOTE) and
                strippedString.endswith(c.TRIPLE_DOUBLE_QUOTE) and
                not c.TRIPLE_DOUBLE_QUOTE == strippedString
            )
        ) :
        return filterString(strippedString[3:-3])
    else :
        return strippedString if not (surroundedBySingleQuote or surroundedByDoubleQuote) else filterString(strippedString[1:-1])

def isLongString(thing) :
    if not thing is None and isinstance(thing, str) :
        return (
            (
                thing.startswith(c.TRIPLE_SINGLE_QUOTE) or
                thing.endswith(c.TRIPLE_SINGLE_QUOTE)
            ) and StringHelperHelper.isNotOneLineLongString(c.TRIPLE_SINGLE_QUOTE, thing) or (
                thing.startswith(c.TRIPLE_DOUBLE_QUOTE) or
                thing.endswith(c.TRIPLE_DOUBLE_QUOTE)
            ) and StringHelperHelper.isNotOneLineLongString(c.TRIPLE_DOUBLE_QUOTE, thing)
        )
    else :
        return False

def removeColors(thing) :
    if ObjectHelper.isNotNone(thing) and isNotBlank(thing) :
        for color in c.IMPLEMENTED_PROMP_COLORS :
            if color in thing :
                thing = thing.replace(color,c.BLANK)
    return thing if isinstance(thing, str) else str(string)

def getS(condition, es=False) :
    return c.BLANK if not condition else 'es' if es else 's'

def getToBe(condition, singular=True, tense=PRESENT, negative=False) :
    if condition :
        if negative :
            if PAST == tense :
                return f'wasn{c.SINGLE_QUOTE}t' if singular else f'weren{c.SINGLE_QUOTE}t'
            elif PRESENT == tense :
                return f'isn{c.SINGLE_QUOTE}t' if singular else f'aren{c.SINGLE_QUOTE}t'
            elif FUTURE == tense :
                return f'won{c.SINGLE_QUOTE}t'
        else :
            if PAST == tense :
                return 'was' if singular else 'were'
            elif PRESENT == tense :
                return 'is' if singular else 'are'
            elif FUTURE == tense :
                return 'will'
        return 'to be'
    else :
        return c.BLANK

def getOnlyLetters(value):
    return join([
        char for char in join(
            str(value).replace(c.UNDERSCORE, c.SPACE).replace(c.DASH, c.SPACE).split(),
            character=c.SPACE
        ) if char in c.CHARACTERES
    ])

def isUp(value):
    return 1 == len(str(value)) and str(value) in c.UPPER_CASE_CHARACTERES

def fromPascalToTitle(value):
    return join([f'{c.SPACE}{char}' if isUp(char) else char for char in str(value)], character=c.BLANK)

def toTitle(value):
    return join(fromPascalToTitle(getOnlyLetters(value)).title().split(), character=c.SPACE)

def toPascalCase(value):
    return join(toTitle(value).split())

def toCamelCase(value):
    content = toPascalCase(value)
    return join([content[:1].lower(), content[1:]])

def toSnakeCase(value):
    return join(toTitle(value).lower().split(), character=c.UNDERSCORE)

def toKebabCase(value):
    return join(toTitle(value).lower().split(), character=c.DASH)
