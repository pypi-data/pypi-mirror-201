import numexpr
import os
from time import sleep
from colorama import init, Fore


def about():
    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ******************** DESCRIPTION *******************\n',
          Fore.GREEN + ' to use the calculator in the line, enter the\n',
                            ' mathematical operation of the example "5+12/9",and\n',
                            ' to get the result of the calculation, press Enter\n',
          Fore.WHITE + '****************************************************\n')


def menu():
    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** CALCULATOR ******\n',
               Fore.GREEN + ' 1. about\n',
                            ' 2. run calculator\n',
                            ' 3. exit\n',
          Fore.WHITE + '************************\n')


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
            print(Fore.RED + f" {' ' * 6}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** CALCULATOR **********')
            print(Fore.GREEN + '  enter a mathematical operation')
            operation = input(Fore.BLUE + '  >>>: ')
            try:
                result = numexpr.evaluate(operation)
                print(Fore.MAGENTA + f"  result: {result}")
                input(Fore.YELLOW + '\n  press Enter to continue')
            except Exception:
                print(Fore.RED + '\n  incorrect operating, try again')
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'


if __name__ == '__main__':
    main()
