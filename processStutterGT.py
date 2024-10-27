import pandas as pd 
import os
import shutil
from pathlib import Path

def collect_files(source_dir, target_dir, file_extension=None):
    """
    Collect all files from nested directories and copy them to a single target directory.
    
    Args:
        source_dir (str): Root directory to start searching from
        target_dir (str): Directory where files will be copied to
        file_extension (str, optional): If specified, only collect files with this extension
    """
    # Convert to Path objects for better path handling
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Counter for processed files
    file_count = 0
    
    # Walk through all directories and files
    for root, dirs, files in os.walk(source_path):
        for file in files:
            # Check if we need to filter by extension
            if file_extension and not file.endswith(file_extension):
                continue
                
            # Get the full path of the source file
            source_file = Path(root) / file
            
            # Create a new filename to avoid conflicts
            # You might want to modify this naming scheme
            new_filename = f"{file_count}_{file}"
            target_file = target_path / new_filename
            
            # Copy the file
            try:
                if file.endswith('.csv'):
                    shutil.copy2(source_file, target_file)
                    #print(f"Copied: {source_file} -> {target_file}")
                    file_count += 1
                    
            except Exception as e:
                print(f"Error copying {source_file}: {e}")
    
    print(f"\nProcessing complete. Copied {file_count} files to {target_path}")

# USE THIS TO CHECK LENGTH 
def traverse_directory(directory):
    """Traverses a directory and its subdirectories, printing all folders."""
    fileCount = 0 
    finalDF = pd.DataFrame()
    for root, dirs, files in os.walk(directory):
        
        for name in files:          
            fileCount +=1 
            #print(os.path.join(root, name))
            if name.endswith('.csv'):
                filePath = Path(root) / name

                df = pd.read_csv(filePath, header=None)
                result = df.iloc[:, 0].str.cat(sep=' ')
                annotation = df.iloc[:, 3].values
                
            new_row = pd.DataFrame({
                'text': [result],
                'StutterType': [annotation]
            })
            
            finalDF = pd.concat([finalDF, new_row], ignore_index=True)
        finalDF.to_csv('StutterGTXavier.csv', index=False)

                
    print("Num of Files:"+ str(fileCount))  
    
if __name__ == "__main__":
    source_directory = r"C:\Users\xnishikawa\OneDrive - Olin College of Engineering\Documents\GitHub\stuttered-speech-asr\StutterGTData"
    target_directory = r"C:\Users\xnishikawa\OneDrive - Olin College of Engineering\Documents\GitHub\stuttered-speech-asr\FlattenedStutterGTData"      # Replace with your target directory
    
    # flatten files into one directory for ease of use
    collect_files(source_directory, target_directory)  
    
    # Grab text from CSV
    traverse_directory(target_directory)

