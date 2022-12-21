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
    modified = [_ctypes.addressof(x) for x in input_list]  # Swap out values with the pointers to the original value!
    print(original)
    print(modified)
    list_len = len(original)

    for original_value in original:
        # Get the modified index of the original value
        modified_index = modified.index(id(original_value))
        modified_value = modified.pop(modified_index)
        # Then re-insert at the new location
        new_index = modified_index + original_value
        new_index = new_index % (list_len - 1)
        modified.insert(new_index, modified_value)

    result_list = [str(get_object(t)) for t in modified]
    print(" ".join(result_list))
    zero_index = result_list.index('0')
    answer = 0
    for x in [1000, 2000, 3000]:
        add = int(result_list[((zero_index + x) % list_len)])
        answer += add
    print(answer)

    # WTF
    buffer = [(idx, i) for idx, i in enumerate(input_list)]

    for idx, i in enumerate(input_list):
        old_idx = buffer.index((idx, i))

        buffer.remove((idx, i))
        buffer.insert((old_idx + i + len(input_list) - 1) %
                      (len(input_list) - 1), (-1, i))

    zero_idx = buffer.index((-1, 0))
    print(" ".join([str(f[1]) for f in buffer]))

    print(sum(buffer[(zero_idx + (i+1) * 1000) % len(buffer)][1]
          for i in range(3)))


if __name__ == '__main__':
    day20_1('data/test20_1.txt')
    # 4348 too low
    # day20_1('data/input20_1.txt')
