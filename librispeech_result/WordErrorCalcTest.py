file_dict_actual = {}  # Initialize the dictionary for actual values
file_dict_predicted = {}  # Initialize the dictionary for predicted values

# Assuming lines for actual values are read into 'actual_lines' and for predicted values into 'predicted_lines'

# Processing actual values (split by space)
for line in actual_lines:  # Replace actual_lines with your actual list of lines
    split_line = line.strip().split(' ', 1)  # Split by space
    if len(split_line) == 2:
        file_code, text = split_line
        # Remove the last 5 characters from the file code
        file_code = file_code[:-5].strip()  # Remove last 5 chars and strip extra whitespace
        file_dict_actual[file_code] = text.strip()  # Strip text as well

# Processing predicted values (split by tab)
for line in predicted_lines:  # Replace predicted_lines with your predicted list of lines
    split_line = line.strip().split('\t', 1)  # Split by tab character
    if len(split_line) == 2:
        file_code, text = split_line
        # Remove the last 5 characters from the file code
        file_code = file_code[:-5].strip()  # Remove last 5 chars and strip extra whitespace
        file_dict_predicted[file_code] = text.strip()  # Strip text as well

# Extracting values from both dictionaries
actual = []
predicted = []

for key in file_dict_actual:
    if key in file_dict_predicted:  # Only process keys that exist in both dictionaries
        actual.append(file_dict_actual[key])
        predicted.append(file_dict_predicted[key])

# Now you can print or use the actual and predicted lists
print("Actual:", actual)
print("Predicted:", predicted)
