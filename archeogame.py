import json
import random
import os
from inputimeout import inputimeout as t_input, TimeoutOccurred


# Функция сохранения прогресса
def save_progress(ch, temd, abil):
    with open('archeogame_saved_info.txt', 'w') as text:
        text.write(f'{ch}\n{temd}\n{abil}\n')


# Функция проверки названия ОС
def check_os():
    if 'ux' in os.name or 'ix' in os.name:
        name = 'clear'
    else:
        name = 'cls'
    return name


# Начальные значения переменных
temple_damage, attempts = 0, 2
keys, ability = list(), '-'
flag = False
question, choice_copy = '', ''
key_counter, keys_to_json_lvl = 1, dict()

# Считывание сюжета из файла archeogame_data.json
with open('archeogame_data.json', 'r', encoding='utf-8') as jsonfile:
    reader = json.load(jsonfile)

# Считывание сохранённой информации из файла archeogame_saved_info.txt
with open('archeogame_saved_info.txt', 'r') as textfile:
    rd = list(map(str.rstrip, textfile.readlines()))
    lvl, td, sp = rd[0], rd[1], rd[2]
    if lvl != '0':
        option = input('Хотите продолжить игру с последнего сохранённого этапа?\nНапишите "Да" или "Нет": ')
        if option.lower() == 'да':
            choice = lvl
        else:
            choice = '0'
            save_progress('0', '0', '-')
    else:
        choice = '0'

    temple_damage = int(td)
    if len(sp) != 0:
        ability = sp
    os.system(check_os())

# Главный цикл
while flag is False:
    print(f'{reader[choice]["text"]}\n')

    # Проверка наличия дополнительных параметров уровня и возможности игрока пользоваться ими
    if 'helpful ability' in reader[choice] and reader[choice]['helpful ability'] in ability:
        print(f'{reader[choice]["text2"]}\n')

    # Считаем количество попыток на определённом этапе
    if 'attempts' in reader[choice]:
        attempts += int(reader[choice]['attempts'])
        print(f'Попыток осталось: {attempts}\n')

    # Возвращаем исходное количество попыток, если игрок доходит до 53 этапа
    if choice == '53':
        attempts = 2

    # Проверка на окончание сюжетной линии
    if 'lost' in reader[choice] or attempts == 0 or 'win' in reader[choice]:
        flag = True
        save_progress('0', '0', '-')
        print(f'Урон, нанесённый храму: {temple_damage}')
        if temple_damage < 20 and 'win' in reader[choice_copy]:
            print('Хорошая работа! Это не такой значительный урон. Храм будет безопасен для следующих исследований')
        elif 'win' in reader[choice_copy]:
            print('Так себе результат. Храм будет небезопасен для будущих исследований')
        else:
            print('Вы всё равно проиграли, какая разница, будет ли кому-то безопасно в этом храме после Вас?')

        # Предложение пользователю сыграть ещё раз
        question = input('\nНе хотите сыграть ещё раз? Ответьте "Да" или "Нет" \n')
        if question.lower() == 'да':
            temple_damage, flag = 0, False
            keys, ability = list(), '-'
            choice_copy = choice
            attempts, choice = 2, '0'
            os.system(check_os())
            save_progress('0', 0, '-')
            print(f'{reader[choice]["text"]}\n')
        else:
            flag = True
            continue

    # Основной код
    if 'sp' not in reader[choice] and (question == '' or question.lower() == 'да'):

        # Печатаем варианты
        if 'lost' not in reader[choice]:
            for key, val in reader[choice]['choices'].items():
                print(f'{key_counter} - {val}')
                keys.append(key)
                keys_to_json_lvl[key_counter] = key
                key_counter += 1
            if 'helpful ability' in reader[choice] and ability in reader[choice]['helpful ability'] and \
                    'choices2' in reader[choice]:
                for k, v in reader[choice]['choices2'].items():
                    print(f'{key_counter} - {v}')
                    keys.append(k)
                    keys_to_json_lvl[key_counter] = k
                    key_counter += 1

            # Обычный ввод без таймера
            if 'timer' not in reader[choice]:
                choice = input('\nВведите номер варианта: ')
                choice_copy = choice
                while choice == '' or int(choice) not in keys_to_json_lvl:
                    choice = input('\nТакого варианта нет! Введите один из данных Вам вариантов: ')
            else:

                # Ввод с таймером
                # Использование конструкции try-except для избежания падения программы
                # после истечения времени в таймере функции t_input()
                try:
                    choice = t_input(prompt=f'\nУ Вас {reader[choice]["timer"]} секунд на ввод номера варианта: ',
                                     timeout=int(reader[choice]["timer"]))
                except TimeoutOccurred:
                    if choice_copy in ['21', '28', '29', '30']:
                        choice = 't.o'
                        os.system(check_os())
                    else:
                        choice = 't.o2'
                        os.system(check_os())
                    continue
                if choice not in [str(i) for i in range(1, 11)] or int(choice) not in keys_to_json_lvl:
                    choice = 'er'
            if choice not in ['t.o', 't,o2', 'er']:
                choice = keys_to_json_lvl[int(choice)]

            # Проверка наличия специальных игровых параметров в уровне
            choice_copy = choice
            if 'temple damage' in reader[choice]:
                temple_damage += int(reader[choice]['temple damage'])
            if 'ability' in reader[choice]:
                ability = reader[choice]['ability']

    # Добавляю random в отдельные этапы
    if 'probability' in reader[choice]:
        if random.randint(1, 10) not in reader[choice]['probability']:
            choice = reader[choice]['choice_change']
            
    # Обнуляем урон храму после успешного использования заклинания
    if choice == 'sp2':
        temple_damage = 0

    save_progress(choice, temple_damage, ability)
    keys.clear()
    os.system(check_os())
    key_counter = 1
    keys_to_json_lvl = dict()
