def ShellInsetSort(array, len_array, dk):  # 直接插入排序
    for i in range(dk, len_array):  # 从下标为dk的数进行插入排序
        position = i
        current_val = array[position]  # 要插入的数
        index = i
        j = int(index / dk)  # index与dk的商
        index = index - j * dk
        while position > index and current_val < array[position - dk]:
            array[position] = array[position - dk]  # 往后移动
            position = position - dk
        else:
            array[position] = current_val


def ShellSort(array, len_array):  # 希尔排序
    dk = int(len_array / 2)  # 增量
    while (dk >= 1):
        ShellInsetSort(array, len_array, dk)
        print(">>:", array)
        dk = int(dk / 2)


array = [49, 38, 65, 97, 76, 13, 27, 49, 55, 4]
print(">:", array)
ShellSort(array, len(array))
