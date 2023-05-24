#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 09:36:13 2023

@author: mashroornitol
"""

import re
import glob

def find_file_with_lowest_float(file_list):
    lowest_float = float('inf')
    lowest_file = None

    for file_name in file_list:
        match = re.search(r'(\d+\.\d+)$', file_name)
        if match:
            float_num = float(match.group(1))
            if float_num < lowest_float:
                lowest_float = float_num
                lowest_file = file_name

    return lowest_file


def allocate_variables(file_path, variable_names, line_numbers, column_positions):
    variables = {}

    # Open the file for reading
    with open(file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Extract the desired values from the specified line numbers and column positions
    for variable_name, line_number, column_position in zip(variable_names, line_numbers, column_positions):
        if line_number <= len(lines):
            line_values = re.split(r'\s+', lines[line_number - 1].strip())
            if column_position < len(line_values):
                variable_value = float(line_values[column_position])
            else:
                variable_value = None
        else:
            variable_value = None

        variables[variable_name] = variable_value

    return variables


def assign_variables_with_multipliers(lowest_file, variable_names, line_numbers, column_positions, multiplier1, multiplier2):
    allocated_variables = allocate_variables(lowest_file, variable_names, line_numbers, column_positions)
    output_list = []

    for var_name, var_value in allocated_variables.items():
        # Check if the value is negative
        if var_value < 0:
            # If negative, append the values in reverse order
            output_list.append((multiplier2 * var_value, multiplier1 * var_value))
        else:
            # If positive, append the values in normal order
            output_list.append((multiplier1 * var_value, multiplier2 * var_value))

    assigned_variables = {}

    for i, var_name in enumerate(variable_names):
        assigned_variables[var_name] = (output_list[i][0], output_list[i][1])

    return assigned_variables


element = 'Ti'
pf = 'potential_files_%s' % element
folder_path = '%s/' % pf  # Replace './' with the actual folder path if different
file_pattern = "%sTi.library_*" % folder_path
file_list = glob.glob(file_pattern)
lowest_file = find_file_with_lowest_float(file_list)
print(lowest_file)
variable_names = ['b_0', 'b_1', 'b_2', 'b_3', 'asub_0', 't_1', 't_2', 't_3']
line_numbers = [2, 2, 2, 2, 2, 3, 3, 3]
column_positions = [1, 2, 3, 4, 7, 1, 2, 3]  # Adjust the column positions accordingly

multiplier1 = 0.90
multiplier2 = 1.10

assigned_variables = assign_variables_with_multipliers(
    lowest_file,
    variable_names,
    line_numbers,
    column_positions,
    multiplier1,
    multiplier2
)

b0b=assigned_variables['b_0']
b1b=assigned_variables['b_1']
b2b=assigned_variables['b_2']
b3b=assigned_variables['b_3']
t1b=assigned_variables['t_1']
t2b=assigned_variables['t_2']
t3b=assigned_variables['t_3']
asubb=assigned_variables['asub_0']

print('b0b = (%s , %s)'%b0b)
print('b1b = (%s , %s)'%b1b)
print('b2b = (%s , %s)'%b2b)
print('b3b = (%s , %s)'%b3b)
print('t1b = (%s , %s)'%t1b)
print('t2b = (%s , %s)'%t2b)
print('t3b = (%s , %s)'%t3b)
print('asubb = (%s , %s)'%asubb)