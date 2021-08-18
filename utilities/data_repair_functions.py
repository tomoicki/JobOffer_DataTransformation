from forex_python.converter import CurrencyRates

factor_usd = CurrencyRates().get_rate('USD', 'PLN')
factor_gbp = CurrencyRates().get_rate('GBP', 'PLN')
factor_eur = CurrencyRates().get_rate('EUR', 'PLN')
factor_huf = CurrencyRates().get_rate('HUF', 'PLN')


# ========================== functions for skills ==========================
def nf_skills_repairer(given: list) -> dict:
    """Gets rid of 'name', 'level' and returns a dict of skills like {'skill1':value, 'skill2':value}."""
    skills_as_keys = []
    levels_as_values = []
    for item in given:
        skills_as_keys.append(item['value'])
        levels_as_values.append('?')
    return dict(zip(skills_as_keys, levels_as_values))


def jj_skills_repairer(given: list) -> dict:
    """Gets rid of 'name', 'level' and returns a dict of skills like {'skill1':value, 'skill2':value}."""
    skills_as_keys = []
    levels_as_values = []
    for item in given:
        skills_as_keys.append(list(item.values())[0])
        levels_as_values.append(list(item.values())[1])
    return dict(zip(skills_as_keys, levels_as_values))
# =============================================================================


# ========================== functions for locations ==========================
def nf_repair_locations_to_list(given: list) -> list:
    """Picks just the cities from location dictionaries."""
    loc_list = []
    for item in given:
        loc_list.append(item['city'])
    return loc_list


def nf_repair_locations_final(given: list) -> list:
    """Cleans and replaces duplicates."""
    loc_list = []
    for item in given:
        if 'dalnie' in item:
            item = 'Remote'
        if 'wars' in item.lower():
            item = 'Warszawa'
        elif 'wroc' in item.lower():
            item = 'Wrocław'
        elif 'lodz' in item.lower():
            item = 'Łódź'
        elif 'crac' in item.lower() or 'rakow' in item.lower() or 'raków' in item.lower():
            item = 'Kraków'
        elif 'buda' in item.lower():
            item = 'Budapest'
        elif 'odes' in item.lower():
            item = 'Odessa'
        elif 'gda' in item.lower():
            item = 'Gdańsk'
        elif 'pozn' in item.lower():
            item = 'Poznań'
        elif 'biała' in item.lower():
            item = 'Bielsko-Biała'
        elif 'ystok' in item.lower():
            item = 'Białystok'
        elif 'lond' in item.lower():
            item = 'London'
        elif 'szcze' in item.lower():
            item = 'Szczecin'
        elif 'kiev' in item.lower():
            item = 'Kiev'
        loc_list.append(item)
        if '' in loc_list:
            loc_list.remove('')
        try:
            integ = int(item)
        except ValueError:
            integ = 'string'
        if type(integ) == int:
            loc_list.remove(item)
    stripped_w_o_duplicates = list(set([item.strip().capitalize() for item in loc_list]))
    return stripped_w_o_duplicates


def jj_repair_locations_final(given: str) -> list:
    """Cleans and replaces duplicates."""
    given = given.split(',')
    loc_list = []
    for item in given:
        if 'dalnie' in item:
            item = 'Remote'
        if 'wars' in item.lower():
            item = 'Warszawa'
        elif 'wroc' in item.lower():
            item = 'Wrocław'
        elif 'lodz' in item.lower():
            item = 'Łódź'
        elif 'crac' in item.lower() or 'rakow' in item.lower() or 'raków' in item.lower():
            item = 'Kraków'
        elif 'buda' in item.lower():
            item = 'Budapest'
        elif 'odes' in item.lower():
            item = 'Odessa'
        elif 'gda' in item.lower():
            item = 'Gdańsk'
        elif 'pozn' in item.lower():
            item = 'Poznań'
        elif 'biała' in item.lower():
            item = 'Bielsko-Biała'
        elif 'ystok' in item.lower():
            item = 'Białystok'
        elif 'lond' in item.lower():
            item = 'London'
        elif 'szcze' in item.lower():
            item = 'Szczecin'
        elif 'kiev' in item.lower():
            item = 'Kiev'
        loc_list.append(item)
        if '' in loc_list:
            loc_list.remove('')
        try:
            integ = int(item)
        except ValueError:
            integ = 'string'
        if type(integ) == int:
            loc_list.remove(item)
    stripped_w_o_duplicates = list(set([item.strip().capitalize() for item in loc_list]))
    return stripped_w_o_duplicates
# =============================================================================


# ========================== functions for employments ========================
def nf_employment_wages_repairer(given: dict) -> list:
    """Recalculates all wages to be PLN and rates to MONTHLY."""
    list_of_dicts = []
    if given['currency'] == 'USD':
        factor = factor_usd
    elif given['currency'] == 'GBP':
        factor = factor_gbp
    elif given['currency'] == 'EUR':
        factor = factor_eur
    elif given['currency'] == 'HUF':
        factor = factor_huf
    elif given['currency'] == 'PLN':
        factor = 1
    else:
        factor = 0
    for key, value in given['types'].items():
        if key in ['permanent', 'b2b', 'zlecenie']:
            if value['period'] == 'Hour':
                value['range'] = [factor * wage * 8 * 30 for wage in value['range']]
            elif value['period'] == 'Day':
                value['range'] = [factor * wage * 30 for wage in value['range']]
            elif value['period'] == 'Year':
                value['range'] = [factor * wage / 12 for wage in value['range']]
            elif value['period'] == 'Month':
                value['range'] = [factor * wage for wage in value['range']]
            else:
                value['range'] = None
            dict_for_one_type = {key: value['range']}
            list_of_dicts.append(dict_for_one_type)
    return list_of_dicts


def jj_employment_types_repairer(given: list) -> list:
    """Gets rid of keys and returns a list of list like [[b2b,pln,10000,15000],[permanent,pln,9000,12000]].
    This will be divided later so that each info will be in its own column - which later will be useful for SQL."""
    list_of_dicts = []
    for dictionary in given:
        if dictionary['salary'] is not None:
            if dictionary['salary']['currency'] == 'usd':
                factor = factor_usd
            elif dictionary['salary']['currency'] == 'gbp':
                factor = factor_gbp
            elif dictionary['salary']['currency'] == 'eur':
                factor = factor_eur
            elif dictionary['salary']['currency'] == 'pln':
                factor = 1
            else:
                factor = 0
            dict_for_one_type = {dictionary['type']:
                                     [factor * dictionary['salary']['from'], factor * dictionary['salary']['to']]}
        else:
            dict_for_one_type = {dictionary['type']: [0, 0]}
        list_of_dicts.append(dict_for_one_type)
    return list_of_dicts


def employment_type(given: list) -> list:
    """Returns list of employment types for job offer."""
    employment_types_list = []
    for dictionary in given:
        employment_types_list.append(list(dictionary.keys())[0])
    return employment_types_list


def b2b_salaries(given: list):
    """Takes just salary range for b2b."""
    for dictionary in given:
        if list(dictionary.keys())[0] == 'b2b':
            return list(dictionary.values())[0]


def permanent_salaries(given: list):
    """Takes just salary range for permanent."""
    for dictionary in given:
        if list(dictionary.keys())[0] == 'permanent':
            return list(dictionary.values())[0]


def mandate_salaries(given: list):
    """Takes just salary range for mandate contract."""
    for dictionary in given:
        if list(dictionary.keys())[0] == 'mandate_contract' or list(dictionary.keys())[0] == 'zlecenie':
            return list(dictionary.values())[0]
# =============================================================================


# ========================== functions for technologies =======================
def pick_skills_from_dicts(given: dict) -> list:
    """Takes skills (keys in dict), forgets about value and returns list of skills.
    As our data from nofluff doesnt appear to have skill values as it is done in justjoin
    we, unfortunately have to downgrade to keep data from both sites standarized and comparable."""
    return list(given.keys())


def remove_duplicates_from_techs(given: list) -> list:
    """Cleans and replaces duplicates."""
    without_duplicates = []
    for item in given:
        if 'angular' in item:
            item = 'angular'
        if 'english' in item or 'angiel' in item:
            item = 'english'
        elif 'git' in item:
            item = 'git'
        elif 'communication' in item:
            item = 'communication skills'
        elif 'problem' in item:
            item = 'problem solving'
        elif 'docker' in item:
            item = 'docker'
        elif 'postgresql' in item:
            item = 'postgresql'
        elif 'polish' in item:
            item = 'polish'
        elif 'rest' in item:
            item = 'rest'
        elif 'react' in item and 'ative' not in item:
            item = 'react'
        elif 'native' in item and 'react' in item:
            item = 'reactnative'
        elif 'python' in item:
            item = 'python'
        elif 'aws' in item:
            item = 'aws'
        elif 'html' in item or 'css' in item:
            item = 'html&css'
        elif 'linux' in item:
            item = 'linux'
        elif 'spring' in item:
            item = 'spring'
        elif '.net' in item and 'asp' not in item:
            item = '.net'
        elif '.net' in item and 'asp' in item:
            item = 'asp.net'
        elif 'azure' in item:
            item = 'azure'
        elif 'php' in item:
            item = 'php'
        elif 'vue' in item:
            item = 'vue'
        elif 'node' in item:
            item = 'node.js'
        elif 'c++' in item:
            item = 'c++'
        elif 'jira' in item:
            item = 'jira'
        elif 'postgre' in item:
            item = 'postgresql'
        elif 'android' in item:
            item = 'android'
        elif 'javascript' in item:
            item = 'javascript'
        elif 'team' in item:
            item = 'team player'
        elif 'junit' in item:
            item = 'junit'
        elif 'next' in item:
            item = 'next.js'
        elif 'jupyter' in item:
            item = 'jupyter'
        elif 'nosql' in item:
            item = 'nosql'
        elif 'clou' in item:
            item = 'cloud'
        elif 'java' in item and 'javasc' not in item:
            item = 'java'
        without_duplicates.append(item)
        if '' in without_duplicates:
            without_duplicates.remove('')
    return list(set(without_duplicates))


def drop_all_rares(given: list, skills_x_plus: list) -> list:
    """Drops all skills whose quantity in total set of skills is rare (<=5)."""
    clean_tech_list = []
    for item in given:
        if item in skills_x_plus:
            clean_tech_list.append(item)
    return clean_tech_list
# =============================================================================
