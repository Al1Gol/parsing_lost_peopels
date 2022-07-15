import json
import requests
from bs4 import BeautifulSoup as bs

person_card_list = [] #Список ссылок на карточки пользователей
site = 'http://www.rozysk.org'
data_dict = []

#Проходим по каждой странице пагинации
for i in range(1, 9999):
    url = f'{site}/people?page={i}'

    q = requests.get(url)
    result = q.content.decode('utf-8')
    
    soup = bs(result, 'lxml')
    page = int(soup.find(class_='current').text) 

    #Проверка наличия страницы пагинации
    if i == page:
        print(f'Получено записей: {i}')
        #Получаем строки таблицы
        persons = soup.find_all(True, {'class':['odd', 'even']})
        #Сохраняем список ссылок на карточки пропавших людей
        for person in persons:
            person_card = person.a.get('href')
            person_card_list.append(person_card)
    else:
        break

#Сохраняем полученные карточки в файл
with open('person_card_list.txt', 'w') as file:
    for line in person_card_list:
        file.write(f'{line}\n')

#Начинаем работу со списком карточек из файла
with open('person_card_list.txt', 'r') as file:

    cards = [line.strip() for line in file.readlines()]
    count = 0

    #Парсим полученный список карточек
    for card in cards:
        q = requests.get(site+card)
        result = q.content.decode('utf-8')

        soup = bs(result, 'lxml')

        info_card = soup.find(class_='people_show')

        #Получаем необхрдимые значения
        name = info_card.find('b', text = 'ФИО:').next_sibling.strip(' \n\t')
        status = info_card.find('span').get_text().strip(' \n\t')
        birthday = info_card.find('b', text = 'Дата рождения:').next_sibling.strip(' \n\t')
        date_lost = info_card.find('b', text = 'Дата  исчезновения:').next_sibling.strip(' \n\t')
        place_lost = info_card.find('b', text = 'Место исчезновения:').next_sibling.strip(' \n\t')

        #Записвываем полученные значения в словарь
        data = {
            'name' : name,
            'status' : status,
            'birthday' : birthday,
            'date_lost' : date_lost,
            'place_lost' : place_lost  
        }

        # Добавляем словари в итоговый список
        data_dict.append(data)
        print(data_dict)
       
        #Записываем итоговые данные в файл
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
        
        #Счетчик прогресса
        count += 1
        print(f'Записано в бд: {count} из {len(cards)}')
    print('Запись завершена!!!')