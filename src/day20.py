import _ctypes


def get_object(obj_id):
    """ Inverse of id() function. But only works if the object is not garbage collected"""
    return _ctypes.PyObj_FromPtr(obj_id)


def day20_1(filepath):
    # Read the input file line by line
    with open(filepath, 'r') as f:
        input_list = [int(i) for i in f.readlines()]

    # Format: [original index, modified index, number value]
    original = input_list
    modified = [id(x) for x in input_list]  # Swap out values with the pointers to the original value!

    for original_value in original:
        # Get the modified index of the original value
        modified_index = modified.index(id(original_value))
        modified_value = modified.pop(modified_index)
        # Then re-insert at the new location
        new_index = modified_index + original_value
        if new_index >= len(original):
            new_index = new_index % (len(original)-1)
        if new_index == 0:
            new_index = len(original) - 1
        modified.insert(new_index, modified_value)

    result_list = [str(get_object(t)) for t in modified]
    print(" ".join(result_list))
    zero_index = result_list.index('0')
    answer = 0
    for x in [1000, 2000, 3000]:
        answer += int(result_list[((zero_index + x) % len(modified))])
    print(answer)


if __name__ == '__main__':
    day20_1('data/test20_1.txt')
    # day20_1('data/input20_1.txt')
