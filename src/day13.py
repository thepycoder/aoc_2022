import functools

def compare(x, y):
    packet1 = x
    packet2 = y
    print(f"Comparing {packet1} to {packet2}")
    index = 0
    while True:
        p1 = packet1[index] if index < len(packet1) else None
        p2 = packet2[index] if index < len(packet2) else None
        t1 = isinstance(p1, int)
        t2 = isinstance(p2, int)
        
        if p1 is None and p2 is not None:
            return True
        if p1 is not None and p2 is None:
            return False
        if p1 is None and p2 is None:
            return None
        
        if t1 and t2:
            # Both ints
            if p1 < p2:
                return True
            if p1 > p2:
                return False
        elif not t1 and not t2:
            result = compare(p1, p2)
            if result is not None:
                return result
        else:
            if t1:
                result = compare([p1], p2)
                if result is not None:
                    return result
            else:
                result = compare(p1, [p2])
                if result is not None:
                    return result
        
        # Only here if p1 == p2
        index += 1
        

with open("data/test13_1.txt", "r") as input_file:
    # Part 1
    chunk_list = input_file.read().split("\n\n")
    answers = []
    for chunk in chunk_list:
        s_packet1, s_packet2 = chunk.split("\n")
        packet1 = eval(s_packet1)
        packet2 = eval(s_packet2)
        
        answers.append(compare(packet1, packet2))
    
    total = 0
    for i, answer in enumerate(answers):
        if answer:
            total += i + 1
    
    print(total)
    
    # Part 2
    new_chunk_list = []
    for chunk in chunk_list:
        new_chunk_list += [eval(c) for c in chunk.split("\n")]
    new_chunk_list.append([[2]])
    new_chunk_list.append([[6]])
    part_2 = sorted(new_chunk_list, key=functools.cmp_to_key(compare))
    print(part_2)
    divider_1 = part_2.index([[2]])
    print(divider_1)
    divider_2 = part_2.index([[6]])
    print(divider_2)
    
    print(divider_1 * divider_2)