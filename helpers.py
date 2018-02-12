import json
# from flask import request

# класс задания
class Box():
    level = 0
    course = ''
    theme = ''
    name = ''
    subs = [['','','']]
    errors = []

    def __init__(self, name=''):
        self.name = name

    def add_subs(self, lst):
        temp_lst = []
        for elem in lst:
            # print(elem)
            if len(elem.strip())>0:
                temp_lst.append(elem)
        self.subs.append(lst)

    def export_dict(self):
        # print(self.subs)
        return {'level': self.level, 'course': self.course, 'theme': self.theme, 'name': self.name, 'subs': self.subs, 'errors': self.errors}

    def export_json(self):
        # return json.dumps(self.get_dict())
        return {'level': self.level, 'course': self.course, 'theme': self.theme, 'name': self.name, 'subs': json.dumps(self.subs), 'errors': self.errors}

    def import_json(self, string):
        try:
            decoded = json.loads(string)
            self.add_subs(decoded)
            return True
        except JSONDecodeError:
            print('Wrong import, decoder Error!')
            return False
        except Exception as e:
            print('Wrong import')
            print(str(e))
            return False

    def import_json_old(self, string):
        try:
            decoded = json.loads(string)
            self.level = decoded['level']
            self.course = decoded['course']
            self.theme = decoded['theme']
            self.name = decoded['level']
            self.add_subs(decoded['subs'])
            return True
        except JSONDecodeError:
            print('Wrong import, decoder Error!')
            return False
        except Exception as e:
            print('Wrong import')
            print(str(e))
            return False

    def import_request(self, req):
        sended = {}
        print(req)
        self.errors = []
        # превращаем формы в словарь
        for elem in req:
            sended[elem] = req[elem]
        # {'finish': '', 'level': '', 'theme': '', 'name': 'name', '1/1': 'werwe', '1/2': 'd', '1/3': '', 
        # '1/4': '', '1/5': '', '2/1': '', '2/2': '', '2/3': '', '2/4': '', '2/5': '', '2/6': '', '3/1': '', '3/2': '', '3/3': ''}\
        if ('level' in sended) and (sended['level'] != ''):
            self.level = sended['level']
        else:
            self.errors.append('Забыли проставить уровень сложности!')

        # if ('course' in sended) and (sended['course'] != ''):
        #     self.course = sended['course']
        # else:
        #     self.errors.append('Забыли проставить курс!')

        if ('theme' in sended) and (sended['theme'] != ''):
            self.theme = sended['theme']
        else:
            self.errors.append('Забыли проставить тему!')

        if ('name' in sended) and (sended['name'] != ''):
            self.name = sended['name']
        else:
            self.errors.append('Забыли проставить название урока!')            

        temp_dict = {}
        flag_add_line = ''
        flag_add_subtask = False
        # разбираем формы реквеста
        for elem in sended:
            if '/' in elem:
                sublist, line = elem.split('/')
                if line == 'add_line':
                    flag_add_line = sublist
                elif line == 'add_subtask': 
                    flag_add_subtask = True
                else:
                    # добавляем в словарь значения
                    if sublist in temp_dict:
                        temp_dict[sublist][line] = str_parse(sended[elem])
                    else:
                        temp_dict[sublist] = {line: str_parse(sended[elem])}
        if flag_add_line != '':
            # print(flag_add_line)
            temp_dict[flag_add_line][str(max([int(x) for x in temp_dict[flag_add_line].keys()])+1)] = ''
        if flag_add_subtask is True:
            temp_dict[str(max([int(x) for x in temp_dict.keys()])+1)] = {'1': ''}
        print(temp_dict)
        # {'1': {'1': 'e3e3e', '2': '', '3': '', '4': '', '5': '', '6': ''}, 
        # '2': {'1': '', '2': '', '3': '', '4': '', '5': '', '6': ''}, '3': {'1': '', '2': '', '3': ''}}
        # print(errors)
        # делаем из словаря список с нормальной очерёдностью
        temp_list = []
        i = 1
        k = 1
        while i <= len(temp_dict.keys()):
            lines = len(temp_dict[str(i)])
            temp_lines = []
            while k <= lines:
                # if temp_dict[str(i)][str(k)] != '':
                temp_lines.append(temp_dict[str(i)][str(k)])
                k += 1
            temp_list.append(temp_lines)
            k = 1
            i += 1
        # print('>>> Add request to subs')
        # print(temp_dict)
        # print(temp_list)
        if 'save' in req: 
            temp_list = clear_list(temp_list) # если POST пришёл от нажатой кнопки "сохранить", то надо удалить пустые строки и сабтаски

        self.subs = temp_list


# очистка задания от пустых подзаданий и строк
def clear_list(lst):
    tmp_lst = []
    for subl in lst:
        tmp_sblst = []
        for line in subl:
            # if len(line.strip())>0:
            # если там пустой список типа:
            if (len(line) == 1) and (line[0] == ''):
                pass
            else:
                tmp_sblst.append(line)
        if len(tmp_sblst)>0:
            tmp_lst.append(tmp_sblst)
    return tmp_lst


# переводим строку в список
def str_parse(string):
    # return string.replace('||', '||$BOX$||').split('||')
    return ['||' if x=='$BOX$' else x for x in string.replace('||', '||$BOX$||').split('||')]
