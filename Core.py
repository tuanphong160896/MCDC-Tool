from os import system
import re 
from itertools import product
import xlsxwriter
from datetime import datetime
from timeit import default_timer as timer
from Define_API import *

def preProcessing():
    input_str = '(((ptrSigConfig->usePort == USE_DATA_SYNCH_FNC) 			||\
					(ptrSigConfig->usePort == USE_DATA_ASYNCH_FNC) 			||\
					(ptrSigConfig->usePort == USE_DATA_RDBI_PAGED_FNC) 		||\
					(ptrSigConfig->usePort == USE_DATA_SYNCH_CLIENT_SERVER) 	||\
					(ptrSigConfig->usePort == USE_DATA_ASYNCH_CLIENT_SERVER)) &&\
					(ptrControlSigConfig->adrReadDataLengthFnc_pfct != NULL_PTR))'
    global origin_str
    origin_str = input_str
    processed_str = ''.join(input_str.split())
    processed_str_nospace = processed_str
    processed_str = processed_str.replace('(', ' ( ').replace(')', ' ) ').replace('&&', ' && ').replace('||', ' || ')
    processed_str_lst = processed_str.split()

    condition_lst = find_each_condition(processed_str_lst)
    if (len(condition_lst) == 0):
        condition_lst = re.findall(r'(?i)\b[a-zA-Z]+\b', processed_str)

    alphabet_lst = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
    for i in range(len(condition_lst)):
        processed_str_nospace =  processed_str_nospace.replace(condition_lst[i], alphabet_lst[i])
        
    processed_str = processed_str_nospace.replace('(', ' ( ').replace(')', ' ) ').replace('&&', ' && ').replace('||', ' || ') 
    processed_str_lst = processed_str.split()

    for i in range(len(processed_str_lst)-1):
        duplicate_num = 1
        for k in range(i+1, len(processed_str_lst)):
            if ((processed_str_lst[i] in alphabet_lst) and (processed_str_lst[i] == processed_str_lst[k])):
                duplicate_num += 1
                processed_str_lst[k] = processed_str_lst[k] + str(duplicate_num)
    processed_str = ' '.join(processed_str_lst)

    # print(condition_lst)
    # main(processed_str)

def find_each_condition(input_str_lst):
    open_idx_lst, close_idx_lst, condition_lst = InitList(3)
    last_close_idx = 0
    input_str_len = len(input_str_lst)
    
    for i in range(0, input_str_len-1):
        if (input_str_lst[i] == '('):
            for k in range(i+1, input_str_len):
                if ((input_str_lst[k] == ')') and (k > last_close_idx)):
                    temp_lst = input_str_lst[i:k+1]
                    if ((isBrackketBalanced(temp_lst)) and (isBoolOprNotInList(temp_lst))):
                        open_idx_lst.append(i)
                        close_idx_lst.append(k)
                        last_close_idx = k
                        break

    for i in range (0, len(open_idx_lst)):
        condition = input_str_lst[open_idx_lst[i]+1 : close_idx_lst[i]]
        condition = ''.join(condition)
        condition_lst.append(condition)
    return condition_lst


def main(bool_str):
    global reduced_str
    alphabet_upper_lst = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
    global conditions_lst
    conditions_lst = re.findall(r'(?i)\b[a-z]+\b', bool_str)
    for i in range (len(conditions_lst)):
        bool_str = bool_str.replace(conditions_lst[i], alphabet_upper_lst[i])
    conditions_lst = re.findall(r'(?i)\b[a-z]+\b', bool_str)
    reduced_str = bool_str

    global bool_exp
    bool_exp =  bool_str.replace('&&', 'and').replace('||', 'or').replace('!', 'not ')
    print(bool_exp)

    try:
        bool_combinations = list(map(list, product([0, 1], repeat=len(conditions_lst))))
    except:
        print('Cannot process this expression !')
        return

    unique_pair_lst = Get_UniquePair_lst(bool_combinations)
    unique_pair_count = countElements(unique_pair_lst)

    global list_OptimizedTCs
    list_OptimizedTCs = []

    if (unique_pair_count >= 50):
        split_factor = int(0.031 * unique_pair_count) + 2
    else:
        split_factor = 1

    if (split_factor > 1):
        subset_lst = Split_lst(unique_pair_lst, split_factor)
        for subset in subset_lst:
            Intersect_Pair(subset)
    else:
        Intersect_Pair(unique_pair_lst)

    finalCombination = findMinLenElement(list_OptimizedTCs)
    final_result = sorted(finalCombination)
    ConvertFinalTCtoBinTable(final_result)


def Get_UniquePair_lst(bool_combinations):
    return_lst = []
    for condition in conditions_lst:
        return_lst.append([condition])

    for comb_index in range(len(bool_combinations)):
        out_prm = CalcBoolExp(conditions_lst, bool_exp, bool_combinations[comb_index])
        unique_check = findunique(bool_combinations[comb_index], comb_index, out_prm, bool_combinations)
        if not (len(unique_check) == 0):
            for k in range(len(unique_check)):
                comb_unique_index = bool_combinations.index(unique_check[k][1])
                return_lst[unique_check[k][0]].append([comb_index, comb_unique_index])

    for column_index in range(len(return_lst)):
        return_lst[column_index].remove(return_lst[column_index][0])

    return return_lst         


def Intersect_Pair(unique_lst):
    temp_lst = []
    mcdc_comb_lst = unique_lst[0]
    for column_index in range(1, len(conditions_lst)):
        length_current_column = len(mcdc_comb_lst)
        length_next_column = len(unique_lst[column_index])
        for prm_pair_index in range(length_current_column):
            for snd_pair_index in range(length_next_column):
                join_lst = mcdc_comb_lst[prm_pair_index] + unique_lst[column_index][snd_pair_index]
                join_lst = list(set(join_lst))
                temp_lst.append(join_lst)
        mcdc_comb_lst = temp_lst[:]
        temp_lst = []

    list_OptimizedTCs.append(findMinLenElement(mcdc_comb_lst))


def findMinLenElement(comb_lst):
    min_length_index = 0
    min_length = len(comb_lst[0])
    for comb_index in range(1, len(comb_lst)):
        if (len(comb_lst[comb_index]) < min_length):
            min_length = len(comb_lst[comb_index])
            min_length_index = comb_index

    OptimizedTC = comb_lst[min_length_index]
    return OptimizedTC


def countElements(processed_str_lst):
    elem_count = 0
    for column in processed_str_lst:
        for elem_in_column in column:
            elem_count += 1
    return elem_count


def Split_lst(processed_str_lst, split_factor):
    return_lst = []
    return_lst_temp = []
    unitlength_lst = []

    for column in range(len(processed_str_lst)):
        unit_length = int(len(processed_str_lst[column])/split_factor)
        temp_lst = [unit_length]*split_factor
        if (sum(temp_lst) < len(processed_str_lst[column])):
            redundant = len(processed_str_lst[column]) - sum(temp_lst)
            for k in range(redundant): temp_lst[k] += 1
        unitlength_lst.append(temp_lst)

    for column_index in range(len(unitlength_lst)):
        for elem_index in range(1, len(unitlength_lst[column_index])):
            unitlength_lst[column_index][elem_index] += unitlength_lst[column_index][elem_index-1]

    for split_step in range(split_factor):
        for column_index in range (len(processed_str_lst)):
            if (split_step == 0): start_index = 0
            else: start_index = unitlength_lst[column_index][split_step-1]
            end_index = unitlength_lst[column_index][split_step]
            return_lst_temp.append(processed_str_lst[column_index][start_index : end_index])
        return_lst.append(return_lst_temp)
        return_lst_temp = []

    return return_lst


def CalcBoolExp(conditions_lst, bool_exp, bool_array):
    if (len(conditions_lst) != len(bool_array)):
        print('Cannot calculate boolean expressions')
    else:
        for condition_index in range(len(conditions_lst)):
            character_index = bool_exp.index(conditions_lst[condition_index])
            bool_exp = bool_exp.replace(bool_exp[character_index], str(bool_array[condition_index]))
        return (eval(bool_exp))


def GetUniquepPair(condition_index, prm_comb, snd_comb):
    diff_elem_lst = []
    for elem_index in range(len(prm_comb)):
        if (prm_comb[elem_index] != snd_comb[elem_index]):
            diff_elem_lst.append(elem_index)
    
    return 1 if (len(diff_elem_lst) == 1 and diff_elem_lst[0] == condition_index) else 0


def findunique(primary_comb, primary_index, out_prm, bool_combinations):
    return_lst = []
    for condition_index in range(len(primary_comb)):
        secondary_comb = list(primary_comb)
        secondary_comb[condition_index] = 0 if (secondary_comb[condition_index] == 1) else 1
        secondary_index = bool_combinations.index(secondary_comb)
        if (secondary_index > primary_index):
            out_snd = CalcBoolExp(conditions_lst, bool_exp, secondary_comb)
            if (out_prm != out_snd):
                return_lst.append([condition_index,secondary_comb])

    return return_lst


def ConvertFinalTCtoBinTable(final_lst_TC):
    leading_zeros = '0' + str(len(conditions_lst)) + 'b'
    binary_lst = []
    result_lst = []
    unique_pair_index = []
    global latest_file

    for comb_index in range(len(final_lst_TC)):
        comb_in_bin = format(final_lst_TC[comb_index], leading_zeros)
        binary_lst.append(comb_in_bin)
    for bin_str in binary_lst:
        result = CalcBoolExp(conditions_lst, bool_exp, bin_str)
        result_lst.append(result)

    for i in range(len(conditions_lst)):
        for j in range(len(binary_lst)-1):
            for k in range(j+1, len(binary_lst)):
                if (GetUniquepPair(i, binary_lst[j], binary_lst[k])): 
                    unique_pair_index.append([j,k])
                    break

    latest_file = str(datetime.now().strftime('%H%M%S_%d%m%Y') + '.xlsx')
    workbook_name = latest_file
    workbook = xlsxwriter.Workbook(workbook_name)
    sheet = workbook.add_worksheet('MCDC Test Cases')
    print(latest_file)
    
    normal_format = workbook.add_format({'font_name': 'Arial', 'font_size': 10 ,'border': 1})
    expr_format = workbook.add_format({'text_wrap': True, 'font_name': 'Arial', 'font_size': 10})
    unique_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'bg_color':'silver','border': 1})

    sheet.write(0, 0, 'Input expression: ' + origin_str, expr_format)
    sheet.write(1, 0, 'Processed expression: ' + reduced_str, expr_format)
    sheet.set_column(0, 0, 72)  # Width of columns 0 set to 72

    for i in range(len(conditions_lst)):
        sheet.write(1, i+1,conditions_lst[i], normal_format)
    sheet.write(1, len(conditions_lst)+1, 'Output', normal_format)


    for i in range(len(unique_pair_index)): #row
        for j in range(len(binary_lst)):    #column
            if (j in unique_pair_index[i]):
                sheet.write(j+2, i+1, int(binary_lst[j][i]), unique_cell_format)
            else:
                sheet.write(j+2, i+1, int(binary_lst[j][i]), normal_format)

    for i in range(len(result_lst)):   
        sheet.write(i+2, len(conditions_lst)+1, int(result_lst[i]), normal_format)

    workbook.close()
    print('Everthing was OK. DONE!')


def Open_latest_file():
    system('start excel.exe ' + latest_file)


preProcessing()