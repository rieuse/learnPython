'''
时间复杂度为O(nlogn)
希尔排序(Shell Sort)是插入排序的一种。也称缩小增量排序，
是直接插入排序算法的一种更高效的改进版本。希尔排序是非稳定排序算法。
希尔排序是把记录按下标的一定增量分组，对每组使用直接插入排序算法排序；
随着增量逐渐减少，每组包含的关键词越来越多，
当增量减至1时，整个文件恰被分成一组，算法便终止。
'''


# def shell_sort(lists):
#     count=len(lists)
#     step = 2
#     group = int(count/step)
#     print(type(group))
#     while group>0:
#         for i in range(group):
#             j=i+group
#             while j<count:
#                 key=lists[j]
#                 k=j-group
#                 while k>=0:
#                     if lists[k]>key:
#                         lists[k+group]=lists[k]
#                         lists[k]=key
#                     k=k-group
#                 j=j+group
#         group=group/step
#     return lists
#
# arr = [2, 645, 1, 344, 546, 442, 89, 99, 76]
# print(shell_sort(arr))
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
