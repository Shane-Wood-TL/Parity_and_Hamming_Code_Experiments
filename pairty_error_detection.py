'''
Shane Wood
ECE 483 Random Processes
Pairity bit issues
'''
import random as rand
import matplotlib.pyplot as plt


length_of_stream = 7

def even_parity_finder(value_to_parity): #add a parity bit to the end of a list
    ones = 0
    zeros = 0
    for bit in value_to_parity:
        if(bit == 0):
            zeros = zeros + 1
        elif(bit == 1):
            ones = ones + 1
    if(ones % 2 == 0):
        value_to_parity.append(0)
    else:
        value_to_parity.append(1)
    return


def passes_even_parity(value_to_check): #checks if the list has even parity
    ones = 0
    zeros = 0
    for bit in value_to_check:
        if(bit == 0):
            zeros = zeros + 1
        elif(bit == 1):
            ones = ones + 1
    if(ones % 2 == 0):
        return True
    else:
        return False

def noise_generator(value_to_destroy, values_to_change): #takes a generated list, flips values_to_change bits
    for _ in range(values_to_change):
        index_to_change = rand.randint(0,length_of_stream)
        if(value_to_destroy[index_to_change]) == 0:
           value_to_destroy[index_to_change] = 1
        else:
            value_to_destroy[index_to_change] = 0
        #print(index_to_change)
    

def generate_data(length_of_this_stream): #generate a binary list
    binary_stream = []
    for i in range(length_of_this_stream):
        binary_stream.append(rand.randint(0,1))
    return binary_stream


'''
#testing code
binary_stream = generate_data(length_of_stream)
print(f"Data: \t\t{binary_stream}")
even_parity_finder(binary_stream)
print(f"Parity: \t{binary_stream}")
noise_generator(binary_stream,2)
print(f"Noised Data: \t{binary_stream}")
print(f"Parity Check {passes_even_parity(binary_stream)}")

'''


test_values = []
test_results = []

for bits_to_flip in range(0,length_of_stream+2): #ensure that the parity bit can be flip aswell (0-length_of_stream + 1 flips)
    results_of_flipping_bits = 0
    for i in range(1000): #run 1000 tests
        this_stream = generate_data(length_of_stream) #generate data
        #print(this_stream)
        even_parity_finder(this_stream) #add the parity bit
        #print(this_stream)
        noise_generator(this_stream, bits_to_flip) #induce noise
        #print(this_stream)
        if(passes_even_parity(this_stream)): #if still passes despite not matching add to counter
            results_of_flipping_bits = results_of_flipping_bits + 1
    test_values.append(bits_to_flip) #append the number of bits flipped
    test_results.append(results_of_flipping_bits) #append the number of tests passed

print(test_values) #print results
print(test_results)


#graph results
labels = []
for i in range(len(test_values)):
    labels.append(str(test_values[i])) #make labels into strings (ensures all labels are present)
print(labels)
plt.bar(labels, test_results) #make a bar graph

plt.ylim(bottom=0)

plt.title("Parity Bits Flipped vs Bits Flipped") #add titles
plt.xlabel("Bits Flipped")
plt.ylabel("Parity Tests Passed")


plt.show() #show the bar graph




    



