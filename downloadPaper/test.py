# a = '1.D._Chizhik++328+Keyholes,_correlations,_and_capacities_of_multielement_transmit_and_receive_antennas'
#
# num_list = a.split('.')[0].strip('+').strip('-').strip('~')
# print(num_list)
import numpy as np

a = ['1', '4', '6', '10', '11', '12', '2', '3', '5', '8', '9']
b = max(list(map(int, a)))
print(b)