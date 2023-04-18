import os
target_dir = 'C:\\Users\\DCS34\\Documents\\temp\\python-prefix-remover'
prefix="test_"
os.chdir(target_dir)
directory_list = os.listdir()
for filename in directory_list:    
    if filename.startswith(prefix):
        os.rename(filename, filename[len(prefix):])
print("The prefix is removed from the filenames.")
print("The prefix is: " + prefix)
print("The directory is: " + target_dir)