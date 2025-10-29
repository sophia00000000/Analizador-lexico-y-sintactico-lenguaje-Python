def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped: break

# Dada una lista desordenada                
x = [9, 8, 7, 5, 4, 3, 0]

# La ordenamos utilizando bubble sort
bubble_sort(x)
print(x)
# [0, 3, 4, 5, 7, 8, 9]