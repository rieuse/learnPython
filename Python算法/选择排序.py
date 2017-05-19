'''
时间复杂度为O(n^2)
第1趟，在待排序记录r1 ~ r[n]中选出最小的记录，
将它与r1交换；第2趟，在待排序记录r2 ~ r[n]中选出最小的记录，
将它与r2交换；以此类推，第i趟在待排序记录r[i] ~ r[n]中选出最小的记录，
将它与r[i]交换，使有序序列不断增长直到全部排序完毕。
'''


def select_sort(lists):
    length = len(lists)
    for i in range(0, length):
        min = i
        for j in range(i + 1, length):
            if lists[min] > lists[j]:
                min = j
        lists[min], lists[i] = lists[i], lists[min]
    return lists


arr = [2, 645, 1, 344, 546, 442, 89, 99, 76, 90]
print(select_sort(arr))
