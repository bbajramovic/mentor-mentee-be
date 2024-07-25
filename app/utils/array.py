def find_common_element(arr1, arr2):
    # Create a hash map to store the frequency of the each element in arr1
    frequency_map = {}
    for num in arr1:
        frequency_map[num] = frequency_map.get(num, 0) + 1
    # Initialize a list to store the common elements
    common_elements = []
    # Iterate through arr2 to the find common elements
    for num in arr2:
        if num in frequency_map and frequency_map[num] > 0:
            common_elements.append(num)
            frequency_map[num] -= 1

    return common_elements
