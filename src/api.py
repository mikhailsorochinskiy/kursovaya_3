from abc import ABC, abstractmethod
import requests


class Parser(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def connect_api(self):
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str):
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'page': 0, 'per_page': 100}
        self.vacancies = []
        self.employers = []

    def connect_api(self):
        """ Метод, отправляющий get-запрос и возвращающий объект response"""
        response = requests.get(self.__url, headers=self.__headers, params=self._params)
        if response.status_code != 200:
            raise ConnectionError
        return response

    def load_vacancies(self, employer_ids: list):
        """ Метод, который забирает вакансии с объекта response и добавляет их в атрибут vacancies"""
        self._params['per_page'] = 20
        self._params['employer_id'] = employer_ids
        while self._params.get('page') != 20:
            response = self.connect_api()
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self._params['page'] += 1

    def get_info_employers(self, employer_ids):
        for employer_id in employer_ids:
            response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
            self.employers.append(response.json())
