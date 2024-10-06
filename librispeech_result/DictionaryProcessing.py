# Initialize an empty dictionary
file_dict_actual = {}

# Specify the file path
file_path = r'C:\Users\sadelli\Documents\GitHub\stuttered-speech-asr\librispeech_result\gt_librispeech.txt'  # Replace with the correct file path

# Open and read the file
with open(file_path, 'r') as file:
    lines = file.readlines()
    # Process each line in the file
    for line in lines:
        # Split the line into code and text using the first space as the delimiter
        split_line = line.strip().split(maxsplit=1)
        if len(split_line) == 2:
            file_code, text = split_line
            file_dict_actual[file_code] = text



# Initialize an empty dictionary
file_dict_predicted = {}

# Specify the file path
file_path = r'C:\Users\sadelli\Documents\GitHub\stuttered-speech-asr\librispeech_result\wav2vec_librespeech.txt'  # Replace with the correct file path

# Open and read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

    # Process each line in the file
    for line in lines:
        # Split the line into code and text using the first space as the delimiter
        split_line = line.strip().split('\t', 1)
        if len(split_line) == 2:
            file_code, text = split_line
            # Remove the last 5 characters from the file code
            file_code_short = file_code[:-5]  
            file_dict_predicted[file_code_short] = text
