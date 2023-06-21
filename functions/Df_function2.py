def check_first_second_degree(base):
    condition1 = False
    condition2 = False
    a = None
    index_counter2 = -1
    for h in base:
        index_counter2 += 1
        if h == 'x':
            condition1 = True
            a = base[index_counter2 - 2]
            if base[index_counter2 + 1] == '^' and base[index_counter2 + 2] == 2:
                condition2 = True
                break
    return condition1, condition2, a
