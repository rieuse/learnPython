def binary(list, item):
    min2 = 0
    max2 = len(list) - 1
    while True:
        mid = (min2 + max2) // 2
        if list[mid] < item:
            min2 = mid + 1
        elif list[mid] > item:
            max2 = mid - 1
        elif list[mid] == item:
            print('ok')
        return None


mylist = [1, 2, 4, 6, 9, 11, 13, 111, 43, 13, 990]
print(binary(mylist, 2))
