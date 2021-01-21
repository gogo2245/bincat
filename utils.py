import os


# move files with requested suffix to end_directory
def move_files(directory, end_directory, new_name, suffix):
    counter = 0
    for path in os.walk(directory):
        for name in path[2]:
            if name.endswith(suffix):
                os.rename(os.path.join(path[0], name),
                          os.path.join(end_directory, new_name + '_' + str(counter) + suffix))
                counter += 1


# Checks if directory exists. If directory is not found creates this directory
def check_if_dir_exists_or_create(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


# calculates directory size
def get_directory_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


# prepares all needed directories
def check_required_directories(output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
