from DictionaryProcessing import file_dict_actual, file_dict_predicted
from jiwer import wer

# Extract values from both dictionaries, ensuring keys exist in both
actual = []
predicted = []

# Extract values from both dictionaries, ensuring keys exist in both
for key in file_dict_actual:
    if key in file_dict_predicted:  # Only process keys that exist in both dictionaries
        actual.append(file_dict_actual[key])
        predicted.append(file_dict_predicted[key])

# Calculate WER
error = wer(actual, predicted)

# Output the WER
print(f"Word Error Rate: {error}")