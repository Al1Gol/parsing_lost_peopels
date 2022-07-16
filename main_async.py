from time import time
import json
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp

site = 'http://www.rozysk.org'
data_dict = []

#Сбор информации
async def gather_data(site):

    async with aiohttp.ClientSession() as session:  
        tasks = []    
        count = 0
        for i in range(1, 3):
            response = await session.get(url=f'{site}/people?page={i}')
            soup = bs(await response.text(), "lxml")
            
            page = int(soup.find(class_='current').text) 

            if i == page:
                persons = soup.find_all(True, {'class':['odd', 'even']})
                for person in persons:
                        link = person.a.get('href')
                        task = asyncio.create_task(get_cards(session, link))
                        tasks.append(task)
                        count += 1
                        print(f'Получена запись №{count}')
            else:
                break

        await asyncio.gather(*tasks)

#Получение карточек
async def get_cards(session, link):
    async with session.get(url=site+link) as response:
        result = await response.text()
        soup = bs(result, 'lxml')
        info_card = soup.find(class_='people_show')
        name = info_card.find('b', text = 'ФИО:').next_sibling.strip(' \n\t')
        status = info_card.find('span').get_text().strip(' \n\t')
        birthday = info_card.find('b', text = 'Дата рождения:').next_sibling.strip(' \n\t')
        date_lost = info_card.find('b', text = 'Дата  исчезновения:').next_sibling.strip(' \n\t')
        place_lost = info_card.find('b', text = 'Место исчезновения:').next_sibling.strip(' \n\t')
        
        data = {
            'name' : name,
            'status' : status,
            'birthday' : birthday,
            'date_lost' : date_lost,
            'place_lost' : place_lost  
        }

        data_dict.append(data)


def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data(site))
    
    with open('.\data\data.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)
    


if __name__ == '__main__':
    t0 = time()
    main()
    print(f'time completed async: {time() - t0}')