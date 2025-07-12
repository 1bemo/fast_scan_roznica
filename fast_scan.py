import os
import subprocess
import colorama

# -------------------------------------------- глобальные -------------------------------------------- #

# текущий путь 
current_path = os.path.abspath(__file__).replace('\\fast_scan.py','')

# параметры по умолчанию
ip_datas = []

# -------------------------------------------- классы -------------------------------------------- #

class IP_Data:
    # конструктор
    def __init__(self, is_divider, ip, name):
        self.is_divider = is_divider
        self.ip = ip
        self.name = name

# -------------------------------------------- функции -------------------------------------------- #

# пинг до IP
def ping_to_ip(ip: str, count = 2):
    result = subprocess.check_output(f'ping {ip} -n {count}', shell = True, text = True)
    return True if result.lower().find('ttl=') != -1 else False

# ------------------------------------------------------------------------------------------------- #

def main():
    
    global ip_datas
    global current_path

    # ---------------------------- получаем настройки из файлов cfg ---------------------------- #

    ip_cfg_file_name = 'ip.cfg'
    ip_cfg_file_path = f'{current_path}\\{ip_cfg_file_name}'

    ip_cfg_file = open(ip_cfg_file_path, 'rt', -1, 'utf-8')

    # заполняем массив ip_datas и получаем макс. длину строки
    str_len = 0
    for l in ip_cfg_file:
        l = l.strip()

        if l == '' or l[0] == '#':
            continue
            
        if l[0] == '-':
            # разделитель
            ip_data = IP_Data(True, '', l[1:].strip())
        else:
            # IP
            splitters = l.split(':')

            name = splitters[1].strip()
            if len(name) > str_len:
                str_len = len(name)

            ip_data = IP_Data(False, splitters[0].strip(), name)

        ip_datas.append(ip_data)

    # макс. длина строки для отображения
    max_len = str_len + 1

    # ---------------------------- пингуем ---------------------------- #

    colorama.init()

    for el in ip_datas:
        if el.is_divider:
            print(f'\n----- {el.name} -----\n')
        else:
            # сколько пробелов
            spaces_count = max_len - len(el.name)
            spaces = ''
            for i in range(spaces_count):
                spaces += ' '

            if ping_to_ip(el.ip, 1):
                style = colorama.Fore.GREEN
                status = '[ONLINE]'
            else:
                style = colorama.Back.RED
                status = '[OFFLINE]'

            print(f'{style}{status} [{el.name}]{spaces}{el.ip}{colorama.Style.RESET_ALL}')

    print(f'\nPRESS ANY KEY TO EXIT\n')

main()