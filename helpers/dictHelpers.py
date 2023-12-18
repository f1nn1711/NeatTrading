def isSet(dictionary: dict, path: str, delimiter: str = '.') -> bool:
    try:
        splitPath = path.split(delimiter, 1)
        result = dictionary[splitPath[0]]

        if len(splitPath) == 1:
            return True

        if type(result) is not dict:
            raise KeyError

        return isSet(result, splitPath[1])

    except KeyError:
        return False


def getDeeperValue(dictionary: dict, path: str, delimiter: str = '.'):
    splitPath = path.split(delimiter, 1)
    result = dictionary[splitPath[0]]

    if len(splitPath) == 1:
        return result

    return getDeeperValue(result, splitPath[1])


def getNested(dictionary: dict, path: str, delimiter: str = '.', notFoundReturn: None = None) -> any:
    if not isSet(dictionary, path, delimiter):
        return notFoundReturn

    return getDeeperValue(dictionary, path, delimiter)


def pluck(inputList: list, path: str) -> list:
    result = []
    for element in inputList:
        result.append(getNested(element, path))

    return result


if __name__ == '__main__':
    testDict = {'request': {'endpoint': 'test'}, 'response': []}
    testList = [
        {'x': 1, 'y': {'z': 'a'}},
        {'x': 2, 'y': {'z': 'b'}},
        {'x': 3, 'y': {'z': 'c'}},
        {'x': 4, 'y': {'z': 'd'}},
    ]

    print(isSet(testDict, 'response'))
    print(isSet(testDict, 'nothing'))
    print(isSet(testDict, 'request.endpoint'))
    print(isSet(testDict, 'request.endpoint.nothing'))

    print(pluck(testList, 'y.z'))
