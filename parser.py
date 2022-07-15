import requests
from bs4 import BeautifulSoup as bs

person_card_list = [] #Список ссылок на карточки пользователей

#Проходим по каждой странице пагинации
for i in range(1):
    url = f'http://www.rozysk.org/people?page={i}'

    q = requests.get(url)
    result = q.content.decode('utf-8')

    #Получаем строки таблицы
    soup = bs(result, 'lxml')
    persons = soup.find_all(True, {'class':['odd', 'even']})

    #Сохраняем список ссылок на карточки пропавших людей
    for person in persons:
        person_card = person.a.get('href')

        print(person_card)

