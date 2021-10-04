from __future__ import annotations
from typing import Union, Any
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter
from unidecode import unidecode

try:
    factor_usd = CurrencyRates().get_rate('USD', 'PLN')
    factor_gbp = CurrencyRates().get_rate('GBP', 'PLN')
    factor_eur = CurrencyRates().get_rate('EUR', 'PLN')
    factor_huf = CurrencyRates().get_rate('HUF', 'PLN')
    factor_chf = CurrencyRates().get_rate('CHF', 'PLN')
except RatesNotAvailableError:
    c = CurrencyConverter()
    factor_usd = c.convert(1, 'USD', 'PLN')
    factor_gbp = c.convert(1, 'GBP', 'PLN')
    factor_eur = c.convert(1, 'EUR', 'PLN')
    factor_huf = c.convert(1, 'HUF', 'PLN')
    factor_chf = c.convert(1, 'CHF', 'PLN')


# ========================== functions for locations ==========================
location_replacement_dict = {'zdalnie': 'Remote', 'warsaw': 'Warszawa', 'wroclaw': 'Wroclaw', 'lodz': 'Lodz',
                             'cracow': 'Krakow', 'krakow': 'Krakow', 'budape': 'Budapest', 'odes': 'Odessa',
                             'gdansk': 'Gdansk', 'poznan': 'Poznan', 'bielsko': 'Bielsko-Biala','bialystok': 'Bialystok',
                             'londyn': 'London', 'london': 'London', 'szczecin': 'Szczecin', 'kiev': 'Kiev'}


def repair_locations(location_list: list[str]) -> list[str]:
    """Renames locations to unidecode (cleans from polish letters) and drops duplicates."""
    loc_list = []
    for location in location_list:
        location = location.lower()
        location = unidecode(location)
        for key, value in location_replacement_dict.items():
            if location.startswith(key):
                location = value
        if location:
            loc_list.append(location)
    loc_list = [location for location in loc_list if not location.isdigit()]
    stripped_w_o_duplicates = list(set([location.strip().capitalize() for location in loc_list]))
    return stripped_w_o_duplicates


# =============================================================================


# ========================== functions for employments ========================
currency_to_factor = {'USD': factor_usd, 'GBP': factor_gbp, 'EUR': factor_eur,
                      'HUF': factor_huf, 'CHF': factor_chf, 'PLN': 1}
employment_types_list = ['permanent', 'b2b', 'zlecenie']
wage_to_monthly = {'Hour': 8 * 30, 'Day': 30, 'Month': 1, 'Year': 1 / 12}


def nfjobs_employment_wages_repairer(employment_types_dict: dict[str, Any]) -> list[dict[str, list[int]]]:
    """Recalculates all wages to be PLN and rates to MONTHLY."""
    factor = currency_to_factor[employment_types_dict['currency']]
    list_of_dicts = []
    for employment in employment_types_list:
        if employment in employment_types_dict['types']:
            wage_rate = wage_to_monthly[employment_types_dict['types'][employment]['period']]
            salary = [factor * wage * wage_rate for wage in employment_types_dict['types'][employment]['range']]
            dict_for_one_type = {employment: salary}
            list_of_dicts.append(dict_for_one_type)
    return list_of_dicts


def justjoin_employment_wages_repairer(given: list[dict[str, Union[str, dict[str, Union[int, str]]]]]) -> list[dict[str, list[int]]]:
    """Gets rid of keys and returns a list of list like [[b2b,pln,10000,15000],[permanent,pln,9000,12000]].
    This will be divided later so that each info will be in its own column - which later will be useful for SQL."""
    list_of_dicts = []
    for dictionary in given:
        if dictionary['salary'] is not None:
            factor = currency_to_factor[dictionary['salary']['currency'].upper()]
            dict_for_one_type = {
                dictionary['type']: [factor * dictionary['salary']['from'], factor * dictionary['salary']['to']]}
        else:
            dict_for_one_type = {dictionary['type']: [0, 0]}
        list_of_dicts.append(dict_for_one_type)
    return list_of_dicts


def employment_type(list_of_employment_types: list[dict[str, list[int]]]) -> list[str]:
    """Returns list of employment types for job offer."""
    types = []
    for dictionary in list_of_employment_types:
        types.append(list(dictionary.keys())[0])
    return types


def add_salaries(list_of_employment_types: list[dict[str, list[int]]], contract_type: str) -> list[int]:
    """Returns list of salary range for employment type."""
    for dictionary in list_of_employment_types:
        if dictionary.keys() == {contract_type}:
            return dictionary[contract_type]


# =============================================================================


# ========================== functions for technologies =======================
skill_replacement_dict = {'angular': 'angular', 'english': 'english', 'angiel': 'english', 'git': 'git',
                          'communication': 'communication skills', 'problem': 'problem solving',
                          'native': 'reactnative',
                          'react': 'react', 'docker': 'docker', 'postgresql': 'postgresql', 'polish': 'polish',
                          'rest': 'rest', 'python': 'python', 'html': 'html&css', 'css': 'html&css',
                          'linux': 'linux', 'spring': 'spring', '.net': '.net', 'azure': 'azure', 'php': 'php',
                          'vue': 'vue', 'node': 'node.js', 'c++': 'c++', 'postgre': 'postgresql', 'android': 'android',
                          'javascript': 'javascript', 'team': 'team player', 'junit': 'junit', 'next': 'next.js',
                          'jupyter': 'jupyter', 'nosql': 'nosql', 'clou': 'cloud', 'java': 'java'}


def remove_duplicates_from_skills(skills_list: list[str]) -> list[str]:
    """Cleans and replaces duplicates."""
    without_duplicates = set()
    for skill in skills_list:
        for key, value in skill_replacement_dict.items():
            #  i did a.startswith(b) as u advised in line 68 in repair_locations_final()
            #  but here it wont work, many skills in raw data look like
            #  'has knowledge of java' or 'communicates in english' or 'knows git' or 'good with html'
            #  so i have to use key in item to get rid of all those useless words and have just skills names
            if key in skill:
                #  special case for java/javascript, react/reactnative
                if 'java' in skill and 'script' not in skill:
                    skill = 'java'
                elif 'react' in skill and 'native' not in skill:
                    skill = 'react'
                else:
                    skill = value
        without_duplicates.add(skill)
    return list(without_duplicates - {""})


def drop_all_rares(given: list[str], skills_x_plus: list[str]) -> list[str]:
    """Drops all skills that are not in skills_x_plus."""
    return [x for x in given if x in skills_x_plus]
# =============================================================================
