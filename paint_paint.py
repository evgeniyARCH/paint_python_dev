import os
import subprocess

from paint_addons import *
from paint_isk_ris import *
from paint_output import *

x = 1
y = 1
text_output = ""
nol = True


def help_func():
    line_number = 0
    commands = [
        'move <up/down/right/left> <distance> - передвигает курсор в направлении на distance',
        'text <string> - вставляет текст, двигается вправо на len(<string>) символов',
        'paint <character> - изменяет точку на character',
        'square <side_of_square> <character> - создает квадрат со стороной <side_of_square> и делает его грани <character>',
        'square_dig <side_of_square> <character> - создает ромб со стороной <side_of_square> и делает его грани <character>',
        'rect <width_of_rectangle> <height_of_rectangle> <character> - создает прямоугольник со сторонами <width_of_rectangle> и <height_of_rectangle> и делает его грани <character>',
        'rect_fill <width_of_rectangle> <height_of_rectangle> <character> - создает прямоугольник со сторонами <width_of_rectangle> и <height_of_rectangle> и заливает его <character>',
        'coord <x> <y> - перемещает курсор в координа <x>, <y>',
        'exit - выход из программы',
        'resolution - узнать разрешение вывода терминала'
    ]
    debug_text('Список команд:')
    for i in commands:
        line_number += 1
        debug_text(f'{line_number}) {i}\n')


def resolution(mass):
    res_x = int(subprocess.check_output('tput cols', shell=True))
    res_y = int(subprocess.check_output('tput lines', shell=True))
    debug_text(f'x = {res_x}, y = {res_y}. size = {res_x * res_y}')


def command_match(usr_command: str, args: list, mass: list):
    global x, y, nol
    side_of_square = 0
    match usr_command:
        case 'move':
            direction = try_get_arguments(args, 0)
            distance = try_get_arguments(args, 1)
            if direction is not None and distance is not None:
                move_func(direction, distance)
            else:
                debug_text("Argument Exception")

        case 'paint':
            character = try_get_arguments(args, 0)
            coord_ris([character, x, y], mass)

        case 'text':
            text = ""
            list_of_text = []
            for i in range(len(args)):
                list_of_text.append(try_get_arguments(args, i))
            text = ".".join(list_of_text)
            paint_text(text, x, y, mass)

        case 'square':
            side_of_square = str_to_int(try_get_arguments(args, 0))
            character = try_get_arguments(args, 1)
            if side_of_square is not None and character is not None:
                square_first = paint_square(side_of_square, character, x, y, mass)
            else:
                debug_text("Argument Exception")

        case 'square_dig':
            side_of_square = str_to_int(try_get_arguments(args, 0))
            character = try_get_arguments(args, 1)
            if side_of_square is not None and character is not None:
                square_second = paint_sqare_ft(side_of_square, character, x, y, mass)
            else:
                debug_text("Argument Exception")

        case 'rect':
            width_of_rectangle = str_to_int(try_get_arguments(args, 0))
            height_of_rectangle = str_to_int(try_get_arguments(args, 1))
            character = try_get_arguments(args, 2)
            if width_of_rectangle is not None and height_of_rectangle is not None and character is not None:
                paint_rectangle_nofill(width_of_rectangle, height_of_rectangle, character, x, y, mass)
            else:
                debug_text("Argument Exception")

        case 'rect_fill':
            width_of_rectangle = str_to_int(try_get_arguments(args, 0))
            height_of_rectangle = str_to_int(try_get_arguments(args, 1))
            character = try_get_arguments(args, 2)
            if width_of_rectangle is not None and height_of_rectangle is not None and character is not None:
                paint_rectangle(width_of_rectangle, height_of_rectangle, character, x, y, mass)
            else:
                debug_text("Argument Exception")

        case 'coord':
            if try_get_arguments(args, 0) is not None and try_get_arguments(args, 1) is not None:
                x = str_to_int(try_get_arguments(args, 0))
                x-=1
                y = str_to_int(try_get_arguments(args, 1))
            else:
                debug_text("Argument Exception")

        case 'help':
            help_func()

        case 'resolution':
            resolution(mass)

        case 'exit':
            nol = False

        case _:
            debug_text("Неизвестая команда. Используйте help для списка операций")


def try_get_arguments(arg_list: list, index: int):
    try:
        element = arg_list[index]
    except IndexError:
        debug_text("Not enough args")
        return None
    return element


def move_func(direction: str, distance: str):
    global x, y
    match direction:
        case "up":
            y -= str_to_int(distance)
        case "down":
            print(1)
            y += str_to_int(distance)
        case "right":
            x += str_to_int(distance)
        case "left":
            x -= str_to_int(distance)


def str_to_int(string: str):
    if string is None:
        pass
    else:
        try:
            integer = int(string)
        except ValueError:
            debug_text("Not Integer")
            return -1
        return integer


def debug_text(string: any):
    global text_output
    text_output = text_output + '\n' + str(string)
    print(text_output)


def clear_screen():
    os.system('clear')


def paint(mass, cursor):
    global x, y, text_output, nol

    px = [' ', 1, 1]

    while nol:
        dist = 0
        output(mass)
        #dist = 1

        print(text_output)
        text_output = ""
        usr_input = input("Enter command: ")
        if usr_input == '' or usr_input == ' ':
            usr_input = '_'
        usr_command, *args = usr_input.split()
        if usr_command == 'move':
            dist = 1
        usr_command.lower()
        command_match(usr_command, args, mass)
        if dist == 0:
            x += 1
        if x > len(mass[0]) or x < 1 or y > len(mass) or y < 1:
            x = 1
            y = 1
        sx = x
        sy = y
        ns = coord_isk([sx, sy], mass)
        nx = [ns, sx, sy]
        coord_ris(px, mass)
        px = nx

        coord_ris([cursor, x, y], mass)

        clear_screen()
        # time.sleep(0.1)
