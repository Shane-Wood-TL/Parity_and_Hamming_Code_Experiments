'''
Shane Wood
ECE 483 Random Processes
Hamming Code
'''

import random as rand
import matplotlib.pyplot as plt
import copy
import numpy as np

length_of_stream = 7

def even_parity_finder(value_to_parity): #normal even parity bit finder
    ones = 0
    zeros = 0
    for bit in value_to_parity:
        if(bit == 0):
            zeros = zeros + 1
        elif(bit == 1):
            ones = ones + 1
    if(ones % 2 == 0):
        return 0
    else:
        return 1
    return


def noise_generator(value_to_destroy, values_to_change, length_of_stream): #add noise to data
    for _ in range(values_to_change):
        index_to_change = rand.randint(0,length_of_stream-1)
        if(value_to_destroy[index_to_change]) == 0:
           value_to_destroy[index_to_change] = 1
        else:
            value_to_destroy[index_to_change] = 0
    

def generate_data(length_of_this_stream): #generate binary data
    binary_stream = []
    for i in range(length_of_this_stream):
        binary_stream.append(rand.randint(0,1))
    return binary_stream

def parity_bit_locations(data): #find the indexes for the parity bits (powers of 2), 2^0, 2^1, 2^2 (no index 0)
    positions = []
    values = len(data)
    i = 0
    while 2**i <= values:
        if(2**i <= values):
            positions.append((2**i)-1)
            values = values + 1
            i = i + 1
    return positions
        
    
def data_expander(data, parity_locations): #add x's to the data in the parity locations
    new_data = []
    skippers = 0
    for i in range(len(data)+len(parity_locations)):
        if(i in parity_locations):
            new_data.append("x")
            skippers = skippers + 1
        else:
            new_data.append(data[i-skippers])
    return new_data
    

def parity_finders(data): #find the sub-parities
    for i in range(len(data)):
        if data[i] == 'x': #find all marked parity spots
            parity_index = i + 1 #convert to one based index instead of 0 based (hamming code needs this)
            
            parity_value = 0
            j = parity_index - 1
            while j < len(data):
                k = 0
                #loosely used code from here: https://www.geeksforgeeks.org/hamming-code-implementation-in-python/
                while k < parity_index and (j + k < len(data)): #prevent over indexing
                    if data[j + k] != 'x':
                        parity_value ^= int(data[j + k])  #use xor to calculate parity
                    k += 1
                j += (2 * parity_index)
            data[i] = int(parity_value)
    return data


def check_hamming_code(data): #check hamming code
    error_position = 0
    for i in range(len(data)):
        if bin(i + 1).count('1') == 1: 
            parity_index = i + 1
            parity_value = 0
            j = parity_index - 1
            while j < len(data):
                k = 0
                while k < parity_index and (j + k < len(data)): #does a very similar process to parity_finders
                    parity_value ^= int(data[j + k])
                    k += 1
                j += (2 * parity_index)
            
            if parity_value != 0:
                error_position += parity_index
    if(error_position > len(data)):
        return None
    if(error_position > 0):
        return error_position - 1
    else:
        return None

'''
#inital testing code
data = generate_data(length_of_stream)
#need to find indexies to add parity bits
parity_spots = parity_bit_locations(data)
print(data)
expanded_data = data_expander(data, parity_spots)
print(expanded_data)
parity_bits_placed = parity_finders(expanded_data)
print(parity_bits_placed)

print(check_hamming_code(parity_bits_placed))

noise_generator(parity_bits_placed,2)
print(parity_bits_placed)
print(check_hamming_code(parity_bits_placed))
'''

test_values = []
fixed_test_results = []
detected_test_results = []

length_with_parity = generate_data(length_of_stream)
test_parity_spots = parity_bit_locations(length_with_parity)
test_expanded_data = data_expander(length_with_parity, test_parity_spots)

#flip up to all bits
for bits_to_flip in range(len(test_expanded_data)):
    results_of_flipping_bits = 0
    errors_detected = 0
    for i in range(10000): #tests to perform
        this_stream = generate_data(length_of_stream)
        parity_spots = parity_bit_locations(this_stream)
        expanded_data = data_expander(this_stream, parity_spots)
        parity_bits_placed = parity_finders(expanded_data)
        original_data = copy.deepcopy(parity_bits_placed)
        noise_generator(parity_bits_placed, bits_to_flip, len(test_expanded_data))
        while True:
            error_pos = check_hamming_code(parity_bits_placed)
            if error_pos is not None:
                errors_detected +=1
                parity_bits_placed[error_pos] ^= 1 #fix error location
            else:
                break
        if original_data == parity_bits_placed: #see if fixed data matches orginal
            results_of_flipping_bits += 1
    test_values.append(bits_to_flip)
    fixed_test_results.append(results_of_flipping_bits)
    detected_test_results.append(errors_detected)

#set up the y labels
labels = []
for i in range(len(test_expanded_data)):
    labels.append(str(test_values[i]))


#double bar graphs are slightly more complex than single ones
x = np.arange(len(labels))

width = 0.35
main_plot, bar_plot = plt.subplots() #need to usb subplots
bar_plot.bar(x - width/2, fixed_test_results, width, label="Data Fixed") #1/2 of the bars
bar_plot.bar(x + width/2, detected_test_results, width, label="Errors Detected")

#finish setting up plots
bar_plot.set_xticks(x)
bar_plot.set_xticklabels(labels)
bar_plot.legend()
bar_plot.set_ylabel("Tests")
bar_plot.set_xlabel("Bits Flipped") 
plt.show()

        
        
