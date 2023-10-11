import os

# Define the path to the directory where you want to insert the header text
directory_path = ''

# Read the content of the headertext.txt file
with open('tools\headertext.txt', 'r') as header_file:
    header_text = header_file.read()

# Define a function to insert header text into Python files
def insert_header(file_path):
    with open(file_path, 'r+') as py_file:
        content = py_file.read()
        py_file.seek(0, 0)
        py_file.write(header_text + content)

# Recursively traverse the directory and its subdirectories
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            insert_header(file_path)
            print(f'Header inserted into {file_path}')

print('Header insertion completed.')
