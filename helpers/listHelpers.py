def listSplit(inputList: list, splitPercent: float) -> list[list]:
    return [inputList[:round(len(inputList) * splitPercent)], inputList[round(len(inputList) * splitPercent):]]


def scaleValues(inputList: list, scaleFrom: int|float = 0, scaleTo: int|float = 1) -> list:
    maxValue = max(inputList)
    minValue = min(inputList)

    return list(map(lambda value: (((value-minValue)/(maxValue-minValue))*(scaleTo-scaleFrom))+scaleFrom, inputList))


if __name__ == '__main__':
    print(scaleValues([0,1,2,3,4]))

