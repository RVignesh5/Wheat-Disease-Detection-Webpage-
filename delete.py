import os
import random

# Path to the folder containing the files
folder_path = r'C:\Users\ADMIN\Desktop\Project\PlantVillage\train\Strawberry___healthy'

# Number of files to keep
num_files_to_keep = 50

# List all files in the folder
files = os.listdir(folder_path)

# Check if the number of files is more than the desired number to keep
if len(files) > num_files_to_keep:
    # Calculate the number of files to delete
    num_files_to_delete = len(files) - num_files_to_keep
    
    # Randomly select files to delete
    files_to_delete = random.sample(files, num_files_to_delete)
    
    # Delete the selected files
    for file_name in files_to_delete:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_name}")
else:
    print("The number of files in the folder is equal to or less than the desired number to keep.")
