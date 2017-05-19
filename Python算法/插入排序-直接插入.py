'''
时间复杂度为O(n^2)
将一个记录插入到已排序好的有序表中，从而得到一个新，记录数增1的有序表。
即：先将序列的第1个记录看成是一个有序的子序列，然后从第2个记录逐个进行插入.
要点：设立哨兵，作为临时存储和判断数组边界之用。如果碰见一个和插入元素相等的，
那么插入元素把想插入的元素放在相等元素的后面。所以，相等元素的前后顺序没有改变，
从原无序序列出去的顺序就是排好序后的顺序，所以插入排序是稳定的。
'''


def insert_sort(lists):
    length = len(lists)
    for i in range(1, length):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1], lists[j] = lists[j], key
            j = j - 1
            print('第', i, '趟', lists)
    return lists


arr = [77, 64, 1, 34, 546, 442, 89, 99, 76, 90]
print(insert_sort(arr))
