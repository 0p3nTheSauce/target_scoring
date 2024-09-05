from collections import Counter

# my_list = [72, 72, 36, 36, 72, 72, 72, 72, 72, 70, 20]
my_list = [72, 70, 20]
most_common_element = Counter(my_list).most_common(1)[0][0]

print(most_common_element)  # Output: 72
