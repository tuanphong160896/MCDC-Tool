def InitList(listnum_int) -> list:
    if (listnum_int > 1):
        return ([] for _ in range(listnum_int))
    else: return []


def ClearList(*all_list) -> list:
    for lst in all_list:
        lst.clear()


def isBrackketBalanced(input_lst) -> bool:
    if (input_lst.count('(') == input_lst.count(')')): return True
    else: return False


def isBoolOprNotInList(input_lst) -> bool:
    if (('&&' and '||') not in input_lst): return True
    else: return False