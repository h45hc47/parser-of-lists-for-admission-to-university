import requests
from bs4 import BeautifulSoup

def what_place(tr):
    main_link = 'https://etu.ru/'
    links = []
    places = []
    td_list = tr.findAll('td')
    td_num = td_list[0].text
    td_name = td_list[1].text
    td_all = td_num + ' ' + td_name
    for link in tr.findAll('a'):
        links.append(link.get('href'))
    for i in range(len(links)):
        links[i] = main_link + links[i]
    for link in links:
        trs_list = []
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'lxml')
        table = soup.find('table', class_="table table-bordered")
        tbody = table.find('tbody')
        trs = tbody.findAll('tr')
        for tr in trs:
            number = tr.find('td', 'number')
            number = number.text
            group = tr.find('td', 'group')
            group = group.text
            ball = tr.find('td', 'ball')
            ball = ball.text
            temp = [number, group, ball]
            trs_list.append(temp)
        for tr in trs_list:
            if (tr[1] == 'ОК' and int(tr[2]) <= 246) or tr[1] == 'К' and int(tr[2]) <= 246:
                places.append(tr[0])
                break
    print(td_all)
    return(td_all, places)

def leti_tables(table):
    places = []
    tbody = table.find('tbody')
    trs = tbody.findAll('tr')
    for tr in trs:
        places.append(what_place(tr))
    return(places)

def leti():
    url = 'https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    div = soup.find('div', class_='col-sm-9')
    lead = div.p.text
    tables = soup.findAll('table', class_='table table-bordered')
    h2 = soup.findAll('h2')
    h2_true = []
    for h in h2:
        h2_true.append(h.text)
    places = []
    for table in tables:
        places.append(leti_tables(table))
    print(lead)
    for i in range(len(h2_true)):
        print('\t', h2_true[i])
        for k in range(len(places[i])):
            print('\t\t', places[i][k][0], *places[i][k][1])
        


def main():
    leti()

if __name__ == '__main__':
    main()