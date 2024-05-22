
def ArrayJumping(arr):
    largest_number = max(arr)
    index_largest_number = arr.index(largest_number)
    moves_left = []
    moves_right = []
    pos_right,pos_left = index_largest_number,index_largest_number
    jumps = 0
    
    for i in range(len(arr)):
        movement_right = i + arr[i]
        movement_left = i - arr[i]
        moves_right.append(movement_right % len(arr ))
        moves_left.append(((movement_left % len(arr))))

    
    possible_steps = [(moves_left[0],moves_right[0])]
    for i in range(len(arr)):
        jumps +=1
        if i % 2 == 0:
            step = (moves_left[possible_steps[-1][1]],moves_right[possible_steps[-1][0]])
        else:
            step = (moves_right[possible_steps[-1][0]],moves_left[possible_steps[-1][1]])
        possible_steps.append(step)
        if index_largest_number in step:
            return jumps
    # code goes here
    return -1




# keep this function call here 
print (ArrayJumping([2, 3, 5, 6, 1]))