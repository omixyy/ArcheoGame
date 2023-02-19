import json
import random
import os
from inputimeout import inputimeout as inptout


def save_progress(ch, temd, abil):
    with open('archeogame_saved_info.txt', 'w') as text:
        text.write(f'{ch}\n{temd}\n{abil}\n')


def check_os():
    if 'ux' in os.name or 'ix' in os.name:
        name = 'clear'
    else:
        name = 'cls'
    return name


temple_damage = 0
keys, ability = list(), '-'
flag = False
attempts = 2
question, choice_copy = '', ''

# Проверка названия ОС
fn_name = check_os()

with open('archeogame_data.json', 'r', encoding='utf-8') as jsonfile:
    reader = json.load(jsonfile)

with open('archeogame_saved_info.txt', 'r') as textfile:
    rd = list(map(str.rstrip, textfile.readlines()))
    lvl, td, sp = rd[0], rd[1], rd[2]
    if lvl != '0':
        option = input('Хотите продолжить игру с последнего сохранённого этапа?\nНапишите "Да" или "Нет": ')
        if option.lower() == 'да':
            choice = lvl
        else:
            choice = '0'
    else:
        choice = '0'
    temple_damage = int(td)
    if len(sp) != 0:
        ability = sp
    os.system(fn_name)

while flag is False:
    print(f'{reader[choice]["text"]}\n')
    if 'helpful ability' in reader[choice] and reader[choice]['helpful ability'] in ability:
        print(f'{reader[choice]["text2"]}\n')
    if 'attempts' in reader[choice]:
        if '7' in choice:
            attempts = 2
        attempts += int(reader[choice]['attempts'])
        print(f'Попыток осталось: {attempts}\n')

    # Проверка на окончание сюжетной линии
    if 'lost' in reader[choice] or attempts == 0 or 'win' in reader[choice]:
        flag = True
        save_progress('0', '0', '-')
        print(f'Урон, нанесённый храму: {temple_damage}')
        if temple_damage < 20 and 'win' in reader[choice_copy]:
            print('Хорошая работа! Это не такой значительный урон. Храм будет безопасен для следующих исследований')
        elif 'win' in reader[choice_copy]:
            print('Так себе результат. Храм будет небезопасен для будущих исследований')
        if 'ability' in reader[choice]:
            print(reader[choice]['ability'])
        question = input('\nНе хотите сыграть ещё раз? Ответьте "Да" или "Нет" \n')
        if question.lower() == 'да':
            temple_damage = 0
            keys, ability = list(), '-'
            flag = False
            attempts = 2
            choice_copy = choice
            choice = '0'
            os.system(fn_name)
            print(f'{reader[choice]["text"]}\n')
        else:
            choice_copy = choice
            choice = '0'
            flag = True
            continue
        save_progress(choice, '0', ability)

    # Основной код
    if 'spell' not in reader[choice] and (question == '' or question.lower() == 'да'):
        if 'lost' not in reader[choice]:
            for key, val in reader[choice]['choices'].items():
                print(f'{key} - {val}')
                keys.append(key)
            if 'helpful ability' in reader[choice] and ability in reader[choice]['helpful ability'] and\
                    'choices2' in reader[choice]:
                for k, v in reader[choice]['choices2'].items():
                    print(f'{k} - {v}')
                    keys.append(k)
            if 'timer' not in reader[choice]:
                choice = input('\nВведите номер варианта: ')
                choice_copy = choice
                while choice not in keys:
                    choice = input('\nТакого варианта нет! Введите один из данных Вам вариантов: ')
            else:
                try:
                    choice = inptout(prompt=f'\nУ Вас {reader[choice]["timer"]} секунд на ввод номера варианта: ')
                except Exception:
                    if choice_copy in ['21', '28', '29', '30']:
                        choice = 't.o'
                        os.system(fn_name)
                        continue
                    else:
                        choice = 't.o2'
                        os.system(fn_name)
                        continue
                if choice not in keys:
                    choice = 'er'
            choice_copy = choice
            if 'temple damage' in reader[choice]:
                temple_damage += int(reader[choice]['temple damage'])
            if 'ability' in reader[choice]:
                ability = reader[choice]['ability']
        save_progress(choice, temple_damage, ability)

    # Добавляю random в отдельные этапы
    if 'probability' in reader[choice]:
        if random.randint(1, 10) not in reader[choice]['probability']:
            choice = reader[choice]['choice_change']

    keys.clear()
    os.system(fn_name)
