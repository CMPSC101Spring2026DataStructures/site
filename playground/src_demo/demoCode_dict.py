# Declare the dictionary
num_dict = {} # define the dictionary here

# Populating the dictionary
print("\t Populaing the dictionary.")
for i in range(10):
     key = i
     value = i**2
     print(f"\t {key} --> {value}")
     num_dict[key] = value # store keys associated to their values

# Pull values out of the dictionary
print("i\t Pulling values from the dictionary their keys.")
for i in range(10):
     print(f"\t num_dict: {i} --> {num_dict[i]}") # pull values by their keys
     