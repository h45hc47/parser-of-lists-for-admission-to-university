import requests

from typing import List, Tuple

from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

from parsers.base import BaseParser


class Parser(BaseParser):
    _base_url: str = "https://etu.ru/"
    need_print: bool

    def _parse(self) -> None:
        url = urljoin(self._base_url, "ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/")
        req = requests.get(url)

        soup = BeautifulSoup(req.text, 'lxml')

        if self.need_print:
            print(self._get_lead(soup))

        tables = soup.findAll('table', class_='table table-bordered')
        places = []
        for table in tables:
            places.append(self._parse_table(table))

        h2 = soup.findAll('h2')
        h2_true = []
        for h in h2:
            h2_true.append(h.text)

        for i in range(len(h2_true)):
            print('\t', h2_true[i])
            for k in range(len(places[i])):
                print('\t\t', places[i][k][0], *places[i][k][1])

    def _get_lead(self, soup: BeautifulSoup) -> str:
        div = soup.find('div', class_='col-sm-9')
        return div.p.text

    def _parse_table(self, table: Tag) -> List[Tuple[str, List[str]]]:
        trs = table.find('tbody').findAll('tr')

        places = []
        for tr in trs:
            places.append(self._parse_places(tr))
        return places

    def _parse_places(self, tr: Tag) -> Tuple[str, List[str]]:
        places = []
        for link in self._collect_links(tr):
            req = requests.get(link)
            soup = BeautifulSoup(req.text, 'lxml')
            trs = soup.find('table', class_="table table-bordered").find('tbody').findAll('tr')

            trs_list = [
                (tr.find('td', 'number').text, tr.find('td', 'group').text, tr.find('td', 'ball').text)
                for tr in trs
            ]

            places += [
                tr[0] for tr in trs_list
                if (tr[1] == 'ОК' and int(tr[2]) <= 246) or tr[1] == 'К' and int(tr[2]) <= 246
            ]

        num, name, *_ = tr.findAll('td')
        td_all = f"{num.text} {name.text}"

        if self.need_print:
            print(td_all)

        return td_all, places

    def _collect_links(self, tr: Tag) -> List[str]:
        links = [l.get("href") for l in tr.findAll('a')]

        return [urljoin(self._base_url, l) for l in links]

    def __call__(self, print_results: bool = True) -> None:
        self.need_print = print_results
        self._parse()
