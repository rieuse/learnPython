def BinarySearch(arr, key):
    min = 0
    max = len(arr) - 1
    if key in arr:
        while True:
            # 这里一定要加int或者使用整除 //，防止列表是偶数的时候出现浮点数据int((min + max) / 2)
            mid = (min + max) // 2
            if arr[mid] > key:
                max = mid - 1
            elif arr[mid] < key:
                min = mid + 1
            elif arr[mid] == key:
                print(str(key) + "在数组里面的第" + str(mid) + "个位置")
                return arr[mid]
    else:
        print("没有该数字!")


arr = [1, 6, 9, 15, 26, 38, 49, 57, 63, 77, 81, 93]
key = input("请输入你要查找的数字：")
BinarySearch(arr, int(key))
