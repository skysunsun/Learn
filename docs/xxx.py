def find(arr,target):
    i,j = 0,len(arr)-1
    while i<=j:
        m = (i+j)//2
        if arr[m]>=target:
            j = m-1
        else:
            i = m+1
    return i
a = [1,2,3,4,5,5,5,6,7]
y = find(a,5)
print(y)