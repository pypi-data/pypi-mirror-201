from .address_book import main as ab
from .note_book import main as nb
from .files_sort import main as fs
from .calculator import main as calc
import os
from time import sleep
from colorama import init, Fore


def main():
    init()
    while True:
        os.system('cls')
        print(Fore.RED + f" {' ' * 11}CLI ASSISTANT BOT")
        print(Fore.WHITE + ' **************** MENU ****************\n',
                   Fore.GREEN + ' 1. address book\n',
                                ' 2. note book\n',
                                ' 3. file sort\n',
                                ' 4. calculator\n',
                                ' 5. exit\n',
              Fore.WHITE + '***************************************\n')

        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '1':
            result = ab()
            if result == 'exit':
                continue

        elif user_input == '2':
            result = nb()
            if result == 'exit':
                continue

        elif user_input == '3':
            result = fs()
            if result == 'exit':
                continue

        elif user_input == '4':
            result = calc()
            if result == 'exit':
                continue

        elif user_input == '5':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            break


if __name__ == '__main__':
    main()
