import wikipedia
import time
from utils import *


# prepares all needed directories
def check_required_directories(output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(os.path.join(output_dir, 'formats')):
        os.mkdir(os.path.join(output_dir, 'formats'))
    if not os.path.isdir(os.path.join(output_dir, 'languages')):
        os.mkdir(os.path.join(output_dir, 'languages'))


def run(config):
    langs = config['langs']
    texts = config['queries']
    formats = config['formats']
    output_dir = config['output_dir']

    prefix = str(int(time.time()))
    counter = 0

    check_required_directories(output_dir)

    for lang in langs:
        check_if_dir_exists_or_create(os.path.join(output_dir, 'languages', lang))

    for f in formats:
        check_if_dir_exists_or_create(os.path.join(output_dir, 'formats', f))

    for l in langs:
        wikipedia.set_lang(l)
        for t in texts:
            result = wikipedia.search(t, results=10)
            for r in result:
                page = None
                try:
                    page = wikipedia.page(r)
                except wikipedia.exceptions.DisambiguationError as e:
                    if 0 in e.options:
                        try:
                            page = wikipedia.page(e.options[0])
                        except e:
                            print(e)
                except:
                    print('Error occurred skipping page', l, t)
                if page is None:
                    continue
                f = open(os.path.join(output_dir, 'languages', l, prefix + '_' + str(counter)), 'wb')
                counter += 1
                f.write(str(page.content).encode('utf8'))
                f.close()
                for form in formats:
                    try:
                        content = str(page.content).encode(form)
                        f = open(os.path.join(output_dir, 'formats', form, prefix + '_' + str(counter)), 'wb')
                        counter += 1
                        f.write(content)
                        f.close()
                    except:
                        print('Error occurred when encoding skipping entry', form, l)

