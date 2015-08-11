def vol(arr):
    volume = 0
    for i in range(1, len(arr) - 1):
        max_height_left = max(arr[0:i])        
        if(max_height_left > arr[i]):
            max_height_right = max(arr[i+1:len(arr)])       
            if(max_height_right > arr[i]):
                volume += (min(max_height_left, max_height_right) - arr[i])
    return volume

print vol([2, 5, 1, 2, 3, 4, 7, 7, 6])
print vol([2, 5, 1, 3, 1, 2, 1, 7, 7, 6])
print vol([2, 7, 2, 7, 4, 7, 1, 7, 3, 7])
print vol([6, 7, 7, 4, 3, 2, 1, 5, 2])
print vol([2, 5, 1, 2, 3, 4, 7, 7, 6, 2, 7, 1, 2, 3, 4, 5, 5, 4])
