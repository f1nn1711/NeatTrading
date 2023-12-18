def getChange(oldValue: float | int, newValue: float | int) -> float:
    if oldValue == 0:
        raise ZeroDivisionError('Your original value cannot be zero')

    return (newValue - oldValue) / oldValue


if __name__ == '__main__':
    print(getChange(10, 10))
