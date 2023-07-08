from collections import deque


def brackets_handling_algorithm(array):
    OPENING_BRACKETS = ('(', '[', '{')
    CLOSING_BRACKETS = (')', ']', '}')

    brackets_deque = deque()

    for element in array:
        if element in OPENING_BRACKETS:  # if the element is an opening bracket, append it to the deque
            brackets_deque.append(element)
        elif element in CLOSING_BRACKETS:  # if the element is a closing bracket, and the deque is empty, it means that the closing bracket has been added without an opening one
            if len(brackets_deque) == 0:
                return False
            else:
                element_index = CLOSING_BRACKETS.index(
                    element)  # this insures that the opening and the closing are of the same type
                if OPENING_BRACKETS[element_index] != brackets_deque.pop():
                    return False

    if len(brackets_deque) != 0:
        return False

    return True


def signs_algorithm(array):
    signs = ('+', '-')
    signs2 = ('/', '*')

    index_counter = -1
    for element in array:
        index_counter += 1
        if element in signs and array[index_counter + 1] in signs:
            return False
        elif element in signs2 and array[index_counter + 1] in signs:
            return False
    return True




