import os
from time import sleep
from datetime import datetime, timedelta, date
from collections import UserList
import pickle
import re
from abc import ABC, abstractmethod
from colorama import init, Fore, Style


class AddressBook(UserList):

    def __init__(self):
        super().__init__()
        self.data = []

    def __str__(self):
        result = []
        for contact in self.data:
            result.append(f"name: {contact['name']}"
                          f"phone: {contact['phone']}"
                          f"birthday: {contact['birthday']}"
                          f"email: {contact['email']}"
                          f"address: {contact['address']}"
                          f"note: {contact['note']}")
        return '\n '.join(result)

    def __setitem__(self, key, value):
        self.data[key] = {'name': value.name,
                          'phone': value.phone,
                          'birthday': value.birthday,
                          'address': value.address,
                          'note': value.note
                          }

    def __getitem__(self, key):
        return self.data[key]

    def add(self, record):
        contact = {'name': record.name,
                   'phone': record.phone,
                   'birthday': record.birthday,
                   'email': record.email,
                   'address': record.address,
                   'note': record.note
                   }
        self.data.append(contact)
        print(Fore.RED + f'  record {record.name} added')
        log(f'record {record.name} added')

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
                          '\n  name: ' + Fore.WHITE + f"{record['name']}",
                          Fore.GREEN + '\n  phone: ' + Fore.WHITE + f"{record['phone']}",
                          Fore.GREEN + '\n  birthday: ' + Fore.WHITE + f"{record['birthday']}",
                          Fore.GREEN + '\n  address: ' + Fore.WHITE + f"{record['address']}",
                          Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}\n"
                          + Fore.WHITE + ' ' + '*' * 25)
                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '  press enter for next page >>>')

            except StopIteration:
                break

    def find_info(self, parameter, pattern):
        result = []
        for key in self.data:
            if pattern in key[parameter]:
                result.append(key)

        if result:
            for record in result:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN +
                      '\n  name: ' + Fore.WHITE + f"{record['name']}",
                      Fore.GREEN + '\n  phone: ' + Fore.WHITE + f"{record['phone']}",
                      Fore.GREEN + '\n  birthday: ' + Fore.WHITE + f"{record['birthday']}",
                      Fore.GREEN + '\n  address: ' + Fore.WHITE + f"{record['address']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}\n"
                      + Fore.WHITE + ' ' + '*' * 25)

        else:
            print(Fore.RED + '  no matches found for pattern')

    def edit(self, name, parameter, new_value):
        for contact in self.data:
            if contact['name'] == name:
                contact[parameter] = new_value
                print(Fore.RED + f'  record {name} edited')
                log(f'record {name} edited')
                break
            else:
                continue

    def congratulate(self):
        result = []
        WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        congratulate = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': []}
        for contact in self.data:
            if contact['birthday']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                new_birthday = birth_day.replace(year=current_date.year)
                birthday_weekday = new_birthday.weekday()
                if get_current_week()[0] <= new_birthday < get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(contact['name'])
                    else:
                        congratulate['monday'].append(contact['name'])
        for k, v in congratulate.items():
            if len(v):
                result.append(Fore.GREEN + f"{k}:" + Fore.WHITE + f" {', '.join(v)}")
        return '  ' + '\n  '.join(result)

    def days_to_birthday(self, name):
        for contact in self.data:
            if name == contact['name']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                user_date = birth_day.replace(year=current_date.year)
                delta_days = user_date - current_date
                if delta_days.days >= 0:
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                else:
                    user_date = user_date.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                break
        else:
            log('record not found')
            print(Fore.RED + '  record not found')

    def delete(self, name):
        for key in self.data:
            if key['name'] == name:
                print(Fore.GREEN + '  are you sure for delete record? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  record {key["name"]} deleted')
                    log(f'record {key["name"]} deleted')
                    break
                else:
                    break
        else:
            log('record not found')
            print(Fore.RED + '  record not found')

    def clear_book(self):
        self.data.clear()

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('address book saved')

    def load(self, file_name):
        try:
            empty_ness = os.stat(file_name)
            if empty_ness.st_size != 0:
                with open(file_name, 'rb') as file:
                    self.data = pickle.load(file)
                log('address book loaded')
        except FileNotFoundError:
            with open(file_name, 'wb+') as file:
                pickle.dump(self.data, file)
            print(Fore.RED + '\n  address book created')
            log('address book created')


class Record:
    def __init__(self, name='', phone='', birthday='', email='', address='', note=''):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.address = address
        self.note = note


class Field(ABC):
    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  name >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect name')
                print(Fore.RED + '  incorrect name, try again')

    def __getitem__(self):
        return self.value


class Phone(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  phone(+380xxxxxxxxx) >>>: ')
            try:
                if re.match(r'^\+380\d{9}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  number')
                print(Fore.RED + '  incorrect number, try again')

    def __getitem__(self):
        return self.value


class Birthday(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  birthday(dd.mm.YYYY) >>>: ')
            try:
                if re.match(r'^\d{2}.\d{2}.\d{4}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  birthday')
                print(Fore.RED + '  incorrect birthday, try again')

    def __getitem__(self):
        return self.value


class Email(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  email >>>: ')
            try:
                if re.match(r'^(\w|\.|_|-)+@(\w|_|-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  email')
                print(Fore.RED + '  incorrect email, try again')

    def __getitem__(self):
        return self.value


class Address(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  address >>>: ')
            try:
                if self.value:
                    break
                else:
                    raise ValueError
            except ValueError:
                log('incorrect address')
                print(Fore.RED + '  incorrect address, try again')

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
                if self.value:
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect note')
                print(Fore.RED + '  incorrect note, try again')

    def __getitem__(self):
        return self.value


class Bot:
    def __init__(self):
        self.book = AddressBook()

    def handle(self, command):
        try:
            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of record per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except Exception:
                        print(Fore.RED + '  incorrect number of record, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  address book empty')
                            break

            elif command == '2':
                name = Name().value.strip().lower()
                if name:
                    if self.book:
                        for item in self.book:
                            if name == item['name']:
                                print(Fore.RED + '\n  this name already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            phone = Phone().value.strip()
                            birth = Birthday().value.strip()
                            email = Email().value.strip()
                            status = Address().value.strip()
                            note = Note().value.strip()
                            record = Record(name, phone, birth, email, status, note)
                            self.book.add(record)
                    else:
                        phone = Phone().value.strip()
                        birth = Birthday().value.strip()
                        email = Email().value.strip()
                        status = Address().value.strip()
                        note = Note().value.strip()
                        record = Record(name, phone, birth, email, status, note)
                        self.book.add(record)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '3':
                print(Fore.GREEN + '  parameter to find (name, phone, birthday, address, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                pattern = input(Fore.GREEN + '  pattern >>>: ').strip().lower()
                if pattern:
                    self.book.find_info(parameter, pattern)
                else:
                    print(Fore.RED + '  please enter a pattern')

            elif command == '4':
                all_records = []
                for key in self.book:
                    all_records.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_records}')
                print(Fore.GREEN + '  enter the name to edit')
                name = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(name, phone, birthday, address, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if name in all_records:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit(name, parameter, new_value)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '5':
                print(self.book.congratulate())

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name for birthday')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.days_to_birthday(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  address book cleared')
                        log('address book cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  address book {file_name} saved')
                else:
                    print(Fore.RED + f'  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  address book {file_name} loaded')
                else:
                    print(Fore.RED + f'  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def get_current_week():
    now = datetime.now()
    current_weekday = now.weekday()
    if current_weekday < 5:
        week_start = now - timedelta(days=2 + current_weekday)
    else:
        week_start = now - timedelta(days=current_weekday - 5)
    return [week_start.date(), week_start.date() + timedelta(days=7)]


def log(command):
    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {command}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def menu():
    print(Fore.RED + f" {' ' * 12}CLI ASSISTANT BOT")
    print(Style.RESET_ALL + ' ************** ADDRESSBOOK **************\n',
               Fore.GREEN + ' 1. show all contacts\n',
                            ' 2. add new contact\n',
                            ' 3. find contacts by pattern\n',
                            ' 4. edit contact\n',
                            ' 5. congratulate contacts\n',
                            ' 6. days to birthday\n',
                            ' 7. delete contact\n',
                            ' 8. clear addressbook\n',
                            ' 9. save addressbook\n',
                            ' 10. load addressbook\n',
                            ' 11. exit\n',
          Style.RESET_ALL + '******************************************\n')


def main():
    init()
    file_name = 'ab_save.bin'
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

        if user_input in ['2', '4', '7', '8']:
            bot.book.save(file_name)


if __name__ == '__main__':
    main()

