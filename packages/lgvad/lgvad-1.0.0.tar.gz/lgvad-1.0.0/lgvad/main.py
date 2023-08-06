import random
import sys
import time
import os
from colorama import init, Fore, Style

init()
while True:
    os.system('cls')
    print(Fore.RED + '"lgvad" генератор лотерей(v 1.0.0)')
    print(Fore.WHITE + '================================')

    amount_num = int(input(Fore.GREEN + 'введите количество номеров для выпадения\n>>>: '))
    amount_all = int(input(Fore.GREEN + 'введите общее количество номеров\n>>>: '))
    time.sleep(1)
    if amount_all <= amount_num:
        print(Fore.RED + '\nобщее количество номеров не может\n'
              'быть меньше либо равно количества\n'
              'номеров для выпадения, введите ещё раз\n')
        input('нажмите Enter для продолжения\n')
        continue

    else:
        os.system('cls')
        print(Fore.YELLOW + f'это {amount_num} случайных шаров из барабана  от 1 до {amount_all}: ')
        start_list = list(range(1, amount_all + 1))
        new_list = []
        time.sleep(1)

        for i in range(1, amount_num + 1):
            random.shuffle(start_list)
            num = random.choice(start_list)
            new_list.append(num)
            print(Fore.GREEN + f'шар номер {i} >>>: ' + Fore.WHITE + f'{num}')
            time.sleep(1)
            start_list.remove(num)

        print(Fore.GREEN + '\nв порядке выпадения' + Fore.WHITE)
        print(', '.join(map(str, new_list)))
        time.sleep(1.5)

        print(Fore.GREEN + '\nпосле сортировки min > max' + Fore.WHITE)
        list_sort = sorted(new_list)
        print(*list_sort, sep=', ')
        time.sleep(1.5)

        print(Fore.RED + '\nпрограмма завершена!')
        while True:
            ex = input(Fore.YELLOW + 'хотите попробовать ещё раз (y/n) >>>: ')
            if ex == 'y':
                break
            elif ex == 'n':
                time.sleep(1.5)
                print(Fore.MAGENTA + 'good bye')
                sys.exit()





