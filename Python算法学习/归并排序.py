"""
平均,最好,最坏 都是 O(nlogn)
"""


def merge_sort(ls):
    mid = len(ls) // 2
    if len(ls) <= 1:
        return ls
    left = merge_sort(ls[:mid])
    right = merge_sort(ls[mid:])
    return merge(left, right)


def merge(left, right):
    l, r = 0, 0
    result = []
    while l < len(left) and r < len(right):
        if ls[l] < ls[r]:
            result.append(ls[l])
            l += 1
        else:
            result.append(ls[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result


ls = [1, 4, 68, 34, 66, 99, 312]
merge_sort(ls)
print(ls)
