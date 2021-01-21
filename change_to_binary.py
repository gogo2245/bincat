from code import code
from compiled_code import compiled_code
from images import images
from text import text
from utils import *
import json
import os
import shutil


def prepare_directories_s2(output_dir_s2):
    if os.path.isdir('output'):
        shutil.rmtree(output_dir_s2)
    os.mkdir(output_dir_s2)
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'code'))
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'compiled_code'))
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'images'))
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'text'))
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'text', 'languages'))
    check_if_dir_exists_or_create(os.path.join(output_dir_s2, 'text', 'formats'))


def change_data_to_binary(input_folder, output_folder, start, end):
    _, dir_names, _ = next(os.walk(input_folder))
    for dir_name in dir_names:
        _, _, file_names = next(os.walk(os.path.join(input_folder, dir_name)))
        data = bytes()
        for file_name in file_names:
            byte = open(os.path.join(input_folder, dir_name, file_name), 'rb').read()
            data += byte[start:-end]
        output = open(os.path.join(output_folder, dir_name + '.bin'), 'wb')
        output.write(data)
        output.close()


print('loading config')
config_file = open('config.json')
config = json.load(config_file)
config_file.close()
output_dir_s1 = config['stage1_output_dir']
output_dir_s2 = config['stage2_output_dir']
start = config['remove_bytes_start']
end = config['remove_bytes_end']

if not os.path.isdir(output_dir_s1):
    os.mkdir(output_dir_s1)

print('downloading code')
code.run(config['code_config'])
print('downloading code for compiling')
compiled_code.run(config['compiled_code_config'])
print('downloading images')
images.run(config['images_config'])
print('downloading text')
text.run(config['text_config'])

prepare_directories_s2(output_dir_s2)
change_data_to_binary(config['code_config']['output_dir'], os.path.join(output_dir_s2, 'code'), start, end)
change_data_to_binary(config['compiled_code_config']['output_dir'], os.path.join(output_dir_s2, 'compiled_code'), start,
                      end)
change_data_to_binary(config['images_config']['output_dir'], os.path.join(output_dir_s2, 'images'), start, end)
change_data_to_binary(os.path.join(config['text_config']['output_dir'], 'languages'),
                      os.path.join(output_dir_s2, 'text', 'languages'), start, end)
change_data_to_binary(os.path.join(config['text_config']['output_dir'], 'formats'),
                      os.path.join(output_dir_s2, 'text', 'formats'), start, end)
