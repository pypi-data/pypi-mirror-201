from collections import UserList
from abc import ABC, abstractmethod
import os
import pickle
import re
from time import sleep
from datetime import datetime, timedelta, date
from colorama import init, Fore, Style


class NoteBook(UserList):
    def __init__(self):
        super().__init__()
        self.data = []

    def __str__(self):
        result = []
        for contact in self.data:
            result.append(f"title: {contact['title']}"
                          f"note: {contact['note']}"
                          f"tag: {contact['tag']}")
        return '\n '.join(result)

    def __setitem__(self, key, value):
        self.data[key] = {'title': value.title,
                          'note': value.note,
                          'tag': value.tag
                          }

    def __getitem__(self, key):
        return self.data[key]

    def add(self, record):
        contact = {'title': record.title,
                   'note': record.note,
                   'tag': record.tag
                   }
        self.data.append(contact)
        print(Fore.RED + f'  record {record.title} added')
        log(f'record {record.title} added')

    def iterator(self, n):
        index = 0
        temp = []
        for record in self.data:
            temp.append(record)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp

    def get_page(self, n):
        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                for record in result:
                    print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN +
                          '\n  title: ' + Fore.WHITE + f"{record['title']}",
                          Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}",
                          Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{record['tag']}\n"
                          + Fore.WHITE + ' ' + '*' * 25)

                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '\n  press enter for next page >>>')

            except StopIteration:
                break

    def add_tag(self, new_tag, title):
        for key in self.data:
            if key['title'] == title:
                if new_tag in key['tag']:
                    print(Fore.RED + f'  tag {new_tag} already exist')
                    break
                key['tag'].append(new_tag)
                print(Fore.RED + f' new tag {new_tag} saved')
                break

    def find_note_by_word(self, word):
        notes = []
        for key in self.data:
            if word in key['note']:
                notes.append(key)
        if notes:
            for key in notes:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN + '\n  title: ' + Fore.WHITE + f"{key['title']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{key['note']}",
                      Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{key['tag']}\n" + Fore.WHITE + ' ' + '*' * 25)
        else:
            print(Fore.RED + '  no matches found for the keyword')

    def find_note_by_tag(self, tag):
        tags = []
        for key in self.data:
            if tag in key['tag']:
                tags.append(key)
        if tags:
            for key in tags:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN + '\n  title: ' + Fore.WHITE + f"{key['title']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{key['note']}",
                      Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{key['tag']}\n" + Fore.WHITE + ' ' + '*' * 25)
        else:
            print(Fore.RED + '  no matches found for the tags')

    def edit_note(self, title, parameter, new_value):
        for key in self.data:
            if key['title'] == title:
                key[parameter] = new_value
                print(Fore.RED + f'  note {title} edited')
                log(f'note {title} edited')
                break
            else:
                continue

    def delete(self, name):
        for key in self.data:
            if key['title'] == name:
                print(Fore.GREEN + '  are you sure for delete note? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  note {key["title"]} deleted')
                    log(f'note {key["title"]} deleted')
                    break
                else:
                    break
        else:
            log('title not found')
            print(Fore.RED + '  title not found')

    def clear_book(self):
        self.data.clear()

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('note book saved')

    def load(self, file_name):
        try:
            empty_ness = os.stat(file_name)
            if empty_ness.st_size != 0:
                with open(file_name, 'rb') as file:
                    self.data = pickle.load(file)
                log('note book loaded')
        except FileNotFoundError:
            with open(file_name, 'wb+') as file:
                pickle.dump(self.data, file)
            print(Fore.RED + '\n  note book created')
            log('note book created')


class Record:
    def __init__(self, title='', note='', tag=None):
        self.title = title
        self.note = note
        self.tag = [tag]


class Field(ABC):
    @abstractmethod
    def __getitem__(self):
        pass


class Title(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  title >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,50}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class Note(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  note >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,250}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class Tag(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  tag >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class Bot:
    def __init__(self):
        self.book = NoteBook()

    def handle(self, command):
        try:
            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of note per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except Exception:
                        print(Fore.RED + '  incorrect number of note, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  note book empty')
                            break

            elif command == '2':
                title = Title().value.strip().lower()
                if title:
                    if self.book:
                        for item in self.book:
                            if title == item['title']:
                                print(Fore.RED + '\n  this title already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            note = Note().value.strip().lower()
                            tag = Tag().value.strip().lower()
                            record = Record(title, note, tag)
                            self.book.add(record)
                    else:
                        note = Note().value.strip().lower()
                        tag = Tag().value.strip().lower()
                        record = Record(title, note, tag)
                        self.book.add(record)

                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '3':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title')
                title = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  add new tag')
                    new_tag = input(Fore.BLUE + '  >>>: ')
                    self.book.add_tag(new_tag, title)
                else:
                    log('title not found')
                    print(Fore.RED + '  title not found')

            elif command == '4':
                print(Fore.GREEN + '  enter the word to find note')
                word = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_word(word)

            elif command == '5':
                print(Fore.GREEN + '  enter the tag to find note')
                tag = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_tag(tag)

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to edit')
                title = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(title, note, tag)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit_note(title, parameter, new_value)
                else:
                    log('title not found')
                    print(Fore.RED + '  title not found')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if value:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  note book cleared')
                        log('note book cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  note book {file_name} saved')
                else:
                    print(Fore.RED + '  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  note book {file_name} loaded')
                else:
                    print(Fore.RED + '  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def log(command):
    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {command}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def menu(*args):
    print(Fore.RED + f" {' ' * 11}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ************** NOTEBOOK **************\n',
          Fore.GREEN + ' 1. show all notes\n',
                       ' 2. add new note\n',
                       ' 3. add tag for note\n',
                       ' 4. find note by word\n',
                       ' 5. find note by tag\n',
                       ' 6. edit note\n',
                       ' 7. delete  note\n',
                       ' 8. clear notebook\n',
                       ' 9. save notebook\n',
                       ' 10. load notebook\n',
                       ' 11. exit\n',
          Fore.WHITE + '**************************************\n')


def main():
    init()
    file_name = 'nb_save.bin'
    bot = Bot()
    bot.book.load(file_name)

    while True:
        os.system('cls')
        menu()
        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '11':
            bot.book.save(file_name)
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'

        bot.handle(user_input)
        input(Fore.YELLOW + '\n  press Enter to continue')

        if user_input in ['2', '3', '6', '7', '8']:
            bot.book.save(file_name)


if __name__ == "__main__":
    main()
