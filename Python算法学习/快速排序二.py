def quick_sort(ls, left, right):
    if left < right:
        mid = (left + right) // 2
        pivot = ls[mid]
        ls[mid], ls[right] = ls[right], ls[mid]
        boundary = left
        for index in range(left, right):
            if ls[index] < pivot:
                ls[index], ls[boundary] = ls[boundary], ls[index]
                boundary += 1
        ls[right], ls[boundary] = ls[boundary], ls[right]
        quick_sort(ls, left, boundary - 1)
        quick_sort(ls, boundary + 1, right)


ls = [1, 3, 56, 23, 34, 99, 532, 4, 59]
print('before:', ls)
quick_sort(ls, 0, len(ls) - 1)
print('after :', ls)
