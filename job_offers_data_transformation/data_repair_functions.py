from __future__ import annotations
from typing import Union
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter

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


# ========================== functions for skills ==========================
def nf_skills_repairer(given: list[dict[str, str]]) -> dict[str, str]:
    """Gets rid of 'name', 'level' and returns a dict of skills like {'skill1':value, 'skill2':value}."""
    skills_as_keys = []
    levels_as_values = []
    for item in given:
        skills_as_keys.append(item['value'])
        levels_as_values.append('?')
    return dict(zip(skills_as_keys, levels_as_values))


def jj_skills_repairer(given: list[dict[str, Union[str, int]]]) -> dict[str, int]:
    """Gets rid of 'name', 'level' and returns a dict of skills like {'skill1':value, 'skill2':value}."""
    skills_as_keys = []
    levels_as_values = []
    for item in given:
        skills_as_keys.append(list(item.values())[0])
        levels_as_values.append(list(item.values())[1])
    return dict(zip(skills_as_keys, levels_as_values))


# =============================================================================


# ========================== functions for locations ==========================
def nf_repair_locations_to_list(given: list[dict[str, Union[str, dict[str, Union[str, int]]]]]) -> list[str]:
    """Picks just the cities from location dictionaries."""
    loc_list = []
    for item in given:
        loc_list.append(item['city'])
    return loc_list


polish_to_english = {'ę': 'e', 'ó': 'o', 'ą': 'a', 'ś': 's', 'ł': 'l', 'ż': 'z', 'ź': 'z', 'ć': 'c', 'ń': 'n'}
location_replacement_dict = {'zdalnie': 'Remote', 'warsaw': 'Warszawa', 'wroclaw': 'Wroclaw', 'lodz': 'Lodz',
                             'cracow': 'Krakow', 'krakow': 'Krakow', 'budape': 'Budapest', 'odes': 'Odessa',
                             'gdansk': 'Gdansk', 'poznan': 'Poznan', 'bielsko': 'Bielsko-Biala','bialystok': 'Bialystok',
                             'londyn': 'London', 'london': 'London', 'szczecin': 'Szczecin', 'kiev': 'Kiev'}


def repair_locations_final(given: list[str]) -> list[str]:
    """Cleans and replaces duplicates."""
    loc_list = []
    for item in given:
        item = item.lower()
        for key, value in polish_to_english.items():
            item = item.replace(key, value)
        for key, value in location_replacement_dict.items():
            if item.startswith(key):
                item = value
        loc_list.append(item)
        if '' in loc_list:
            loc_list.remove('')
    loc_list = [x for x in loc_list if not x.isdigit()]
    stripped_w_o_duplicates = list(set([item.strip().capitalize() for item in loc_list]))
    return stripped_w_o_duplicates


# =============================================================================


# ========================== functions for employments ========================
currency_to_factor = {'USD': factor_usd, 'GBP': factor_gbp, 'EUR': factor_eur,
                      'HUF': factor_huf, 'CHF': factor_chf, 'PLN': 1}
employment_types_list = ['permanent', 'b2b', 'zlecenie']
wage_to_monthly = {'Hour': 8 * 30, 'Day': 30, 'Month': 1, 'Year': 1 / 12}


def nf_employment_wages_repairer(given: dict[str, Union[str, dict[str, Union[str, list[int], bool]]]]) -> list[dict[str, list[int]]]:
    """Recalculates all wages to be PLN and rates to MONTHLY."""
    factor = currency_to_factor[given['currency']]
    list_of_dicts = []
    for employment in employment_types_list:
        if employment in given['types']:
            wage_rate = wage_to_monthly[given['types'][employment]['period']]
            salary = [factor * wage * wage_rate for wage in given['types'][employment]['range']]
            dict_for_one_type = {employment: salary}
            list_of_dicts.append(dict_for_one_type)
    return list_of_dicts


def jj_employment_types_repairer(given: list[dict[str, Union[str, dict[str, Union[int, str]]]]]) -> list[dict[str, list[int]]]:
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


def employment_type(given: list[dict[str, list[int]]]) -> list[str]:
    """Returns list of employment types for job offer."""
    types = []
    for dictionary in given:
        types.append(list(dictionary.keys())[0])
    return types


def add_salaries(given: list[dict[str, list[int]]], contract_type: str) -> list[int]:
    """Takes salary range for contract type."""
    for dictionary in given:
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


def remove_duplicates_from_skills(given: list[str]) -> list[str]:
    """Cleans and replaces duplicates."""
    without_duplicates = set()
    for item in given:
        for key, value in skill_replacement_dict.items():
            #  i did a.startswith(b) as u advised in line 68 in repair_locations_final()
            #  but here it wont work, many skills in raw data look like
            #  'has knowledge of java' or 'communicates in english' or 'knows git' or 'good with html'
            #  so i have to use key in item to get rid of all those useless words and have just skills names
            if key in item:
                #  special case for java/javascript, react/reactnative
                if 'script' not in item:
                    item = 'java'
                elif 'native' not in item:
                    item = 'react'
                else:
                    item = value
        without_duplicates.add(item)
        if '' in without_duplicates:
            without_duplicates.remove('')
    return list(without_duplicates)


def drop_all_rares(given: list[str], skills_x_plus: list[str]) -> list[str]:
    """Drops all skills that are not in skills_x_plus."""
    return [x for x in given if x in skills_x_plus]
# =============================================================================
