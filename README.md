# bincat
This repository is created for downloading dataset for bincat neural network.
It contains scripts that can be used to download code, images and text used for machine learning.


## Stage 1
If you want to use any of this scripts listed bellow you need to setup `config.json` file in script directory according to `config.example.json` file and run `standalone_*` file

### Code
code folder contains scripts for downloading code from github repositories.
#### config explained
`github_access_key` - This key can be obtained from github. It is used for github authorization.

`max_repos` - How many repos can script use. (If more repos are needed script stops instead).

`languages_with_suffix` - This object contains language-suffix pairs. 

`output_dir` - Where script should store data.

`required_bytes` - When this goal is achieved or too many repos is used script stops.

### Compiled code
compiled_code folder contains scripts for downloading code from [this](https://beginnersbook.com/2015/02/simple-c-programs/) page.
#### config explained

`architectures` - This object contains architecture-compile script pairs. In this script input and output paths must be replaced with INPUT_PATH and OUTPUT_PATH (see example).

`output_dir` - Where script should store data.

### Images
images folder contains scripts for downloading images with google api.
#### config explained

`google_api_key` - Put your google api key here. For more info see [google documentation](https://developers.google.com/custom-search/v1/overview).

`google_cse_id` - Put your cse id here. For more info see [google documentation](https://developers.google.com/custom-search/v1/overview).

`queries` - Queries used for google search. Script downloads 10 images for every query-format pair.

`formats` - Script will download images in this formats

`output_dir` - Where script should store data

`required_bytes` - When this goal is achieved or all queries are used script stops.

### Text
text folder contains scripts for downloading texts from wikipedia.
#### config explained

`langs` - Languages used when searching on wikipedia

`queries` - Queries used for Wikipedia search. Script tries to download 10 page contents for every query-language pair.

`formats` - Script will store all page contents in this formats

`output_dir` - Where script should store data

## Stage 2
If you want use all script listed above and merge data to `*.bin` files you can use `change_to_binary`. Before that setup `config.json` according to `config.example.json`.

#### config explained

`stage1_output_dir` - Where data from stage one will be stored

`stage2_output_dir` - where `*.bin` data will be stored

`remove_bytes_start` - How much bytes will script remove from start of every file.

`remove_bytes_end` - How much bytes will script remove from end of every file.

`code_config` - Object containing config for code script. See code config explained.

`compiled_code_config` - Object containing config for compiled code script. See compiled code config explained.

`images_config` - Object containing config for images script. See images config explained.

`text_config` - Object containing config for text script. See text config explained.