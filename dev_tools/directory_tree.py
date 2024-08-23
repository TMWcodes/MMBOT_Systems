import os
import fnmatch

def print_directory_tree(startpath, file_handle=None, ignore=None):
    ignore = ignore or []
    for root, dirs, files in os.walk(startpath):
        # Calculate the relative path from the startpath
        relative_root = os.path.relpath(root, startpath)
        if relative_root == '.':
            relative_root = ''
        
        # Filter directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore)]
        # Filter files
        files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore)]

        indent = ' ' * 4 * (relative_root.count(os.sep))
        print(f'{indent}{os.path.basename(root)}/', file=file_handle)
        subindent = ' ' * 4 * (relative_root.count(os.sep) + 1)
        for f in files:
            print(f'{subindent}{f}', file=file_handle)

if __name__ == "__main__":
    # Set the starting path to the directory you want to scan
    start_path = os.path.abspath(os.path.join(os.getcwd(), '..'))

    # List of patterns to ignore
    ignore_list = ['__pycache__', '.DS_Store', '*.pyc', '.git', 'myenv', '.pytest_cache', 'pytest-cache-files-*']

    # Determine the directory of the current working directory's parent
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)

    # Set the output file path to the parent directory
    output_file = os.path.join(parent_dir, 'app_structure.txt')

    # Option 1: Print to console
    print("Directory Tree:")
    print_directory_tree(start_path, ignore=ignore_list)

    # Option 2: Save to a text file
    with open(output_file, 'w') as f:
        print_directory_tree(start_path, file_handle=f, ignore=ignore_list)

    print(f"\nDirectory tree saved to {output_file}")