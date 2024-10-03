def create_dictionary_from_file(file_path):
    file_dict = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            # Split the line into code and text using the first space as the delimiter
            split_line = line.strip().split(' ', 1)
            if len(split_line) == 2:
                file_code, text = split_line
                file_dict[file_code] = text

    return file_dict

# Example usage
file_path = r'C:\Users\sadelli\Desktop\AIMPOWER\FluentSpeechFiles\441-128982.trans.txt'  # Replace this with the path to your text file
file_dictionary = create_dictionary_from_file(file_path)

# Print the resulting dictionary
for code, text in file_dictionary.items():
    print(f"{code}: {text}")
