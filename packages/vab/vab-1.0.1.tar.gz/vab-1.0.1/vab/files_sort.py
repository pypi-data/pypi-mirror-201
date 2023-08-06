import sys
import os
import re
import shutil
import os.path
from colorama import init, Fore
from datetime import datetime, timedelta, date
from time import sleep


def normalize(name):  # заміна кирилиці на латиницю
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!#$%&()*+,-/:;<>=?@[]^~{|}'\\`. "
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
        "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
        "_",
        "_", "_", "_", "_", "_", "_", "_", "_", "_")
    TRANS = {}
    CYRILLIC = tuple(CYRILLIC_SYMBOLS)

    for c, l in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    if re.search(r'\..{2,5}$', name):
        s_res = re.search(r'\..{2,5}$', name)
        suffix = s_res.group()
        name = name.removesuffix(suffix)
        name = name.translate(TRANS)
        name = name + suffix
    else:
        name = name.translate(TRANS)
    return name


# переміщує відомі файлу у спеціальну теку
def move_file(files_patern, path, el, dst):
    for doc_patern in files_patern:
        if re.search(doc_patern, el):
            new_el = normalize(el)  # змінюю назову файлу
            src = os.path.join(path, el)  # шлях папки, з якої переміщуємо файл
            dst = os.path.join(dst, new_el)  # шлях папки, куде переміщуємо файл
            # пробуємо перемісти файл (переміщуємо з валениям)
            try:
                shutil.copy(src, dst)
                print(Fore.WHITE + "  file is copied successfully", el)
                os.remove(src)
                print(Fore.WHITE + "  file is deleted successfully", el)

            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file", el)
                os.remove(src)
                print(Fore.RED + "  file is deleted successfully", el)

            except PermissionError:
                print(Fore.RED + "  permission denied", el)

            except Exception:
                print(Fore.RED + "  error occurred while copying file", el)


# переміщує невідомі файлу у спеціальну папку
def move_unknown_file(files_patern, path, el, dst):
    for doc_patern in files_patern:
        if re.search(doc_patern, el) is None:
            new_el = normalize(el)  # змінюю назву файлу
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)
            try:
                shutil.copy(src, dst)
                os.remove(src)
                print(Fore.WHITE + "  file is copied successfully")
            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file")
            except PermissionError:
                print(Fore.RED + "  permission denied")
            except OSError:
                pass


def rec_sort(path):  # сортуємо файл
    # створюємо папки для сортування файлів
    new_folders = ['images',
                   'documents',
                   'audio',
                   'video',
                   'archives',
                   'programs',
                   'unknown']

    for el in new_folders:
        try:
            os.mkdir(path + '\\' + el)
        except FileExistsError:
            print(Fore.RED + f"  file already exists: {el}")
        except OSError:
            print(Fore.RED + f"  error creating folder: {el}")

    dst_doc = os.path.join(path, 'documents')
    dst_img = os.path.join(path, 'images')
    dst_aud = os.path.join(path, 'audio')
    dst_vid = os.path.join(path, 'video')
    dst_arh = os.path.join(path, 'archives')
    dst_prg = os.path.join(path, 'programs')
    dst_un = os.path.join(path, 'unknown')
    el_list = os.listdir(path)

    for folder in new_folders:  # видаляємо стандартні папки з циклу
        for el in el_list:
            if folder == el:
                el_list.remove(el)
    for el in el_list:
        image_files = ['\.jpeg$', '\.png$', '\.jpg$', '\.svg$', '\.tiff$', '\.tif$', '\.bmp$', '\.gif$']
        video_files = ['\.avi$', '\.mp4$', '\.mov$', '\.mkv$', '\.3gp$', '\.3g2$', '\.mpg$', '\.mpeg$']
        doc_files = ['\.doc$', '\.docx$', '\.txt$', '\.pdf$',
                     '\.xls$', '\.xlsx$', '\.pptx$', '\.mpp$', '\.html$', '\.csv$', '\.bin$', '\.rtf$']
        audio_files = ['\.mp3$', '\.ogg$', '\.wav$', '\.amr$', '\.mid$', '\.midi$', '\.mpa$', '\.wma$']
        arch_files = ['\.zip$', '\.gz$', '\.tar$', '\.7z$', '\.rar$']
        program_files = ['\.exe$', '\.bat$', '\.apk$']
        unknown_files = []

        # створив список з відомих розширень файлів
        unknown_files.extend(image_files)
        unknown_files.extend(video_files)
        unknown_files.extend(doc_files)
        unknown_files.extend(audio_files)
        unknown_files.extend(arch_files)
        unknown_files.extend(program_files)

        if not os.path.isdir(path + '\\' + el):  # It is a file
            # move the file
            move_file(image_files, path, el, dst_img)  # переміщуємо картинки
            move_file(video_files, path, el, dst_vid)
            move_file(doc_files, path, el, dst_doc)
            move_file(audio_files, path, el, dst_aud)
            move_file(arch_files, path, el, dst_arh)
            move_file(program_files, path, el, dst_prg)
            move_unknown_file(unknown_files, path, el, dst_un)
        elif os.path.isdir(path + '\\' + el):  # It is a folder
            rec_sort(path + '\\' + el)


def delete_empty_folders(path):  # видаляє порожні папки
    for el in os.listdir(path):  # перебираємо всі елементи в структурі (теки, файли)
        if os.path.isdir(path + '\\' + el):  # якщо елемент є тека
            try:
                os.rmdir(path + '\\' + el)
                print(Fore.WHITE + "  directory '%s' has been removed successfully" % (path + '\\' + el))
                log("directory '%s' has been removed successfully" % (path + '\\' + el))
                delete_empty_folders(path)
            except OSError:
                print(Fore.RED + "  directory '%s' can not be removed" % (path + '\\' + el))
                log("directory '%s' can not be removed" % (path + '\\' + el))
                delete_empty_folders(path + '\\' + el)


def about():
    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ********************* DESCRIPTION ********************\n',
               Fore.GREEN + ' the script helps to sort files in folders according\n',
                            ' to popular file types as a result, files will be \n',
                            ' moved into folders: <images>, <documents>,\n',
                            ' <audio>, <video>, <archives>, <programs>, <unknown>\n',
                            ' if the folder does\'t contain files of some file\n',
                            ' type then a new folder for this type will not create\n',
          Fore.WHITE + '*******************************************************\n')


def menu():
    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** FILE SORT ******\n',
               Fore.GREEN + ' 1. about\n',
                            ' 2. run file sort\n',
                            ' 3. exit\n',
          Fore.WHITE + '************************\n')


def log(command):
    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {command}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def main():
    init()
    while True:
        os.system('cls')
        menu()
        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '1':
            os.system('cls')
            about()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 7}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** FILE SORT **********')
            print(Fore.GREEN + '  input the file path')
            path = input(Fore.BLUE + '  >>>: ')
            try:
                if os.path.exists(path):
                    rec_sort(path)
                    delete_empty_folders(path)
                    print(Fore.MAGENTA + '\n  sorting completed successfully')
                    input(Fore.YELLOW + '\n  press Enter to continue')
                else:
                    print(Fore.RED + f'\n  path {path} is not found, try again')
                    log(f'path {path} is not found, try again')
                    input(Fore.YELLOW + '\n  press Enter to continue')

            except Exception:
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'


if __name__ == '__main__':
    main()
