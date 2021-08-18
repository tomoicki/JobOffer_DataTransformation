import pandas
from utilities import data_repair_functions
from collections import Counter


def nofluff_repair_procedure(given: list):
    """Data standardization os its similar to justjoin data."""
    nofluff_data = pandas.DataFrame(given)
    #  repair skills
    nofluff_data['skills_must'] = nofluff_data['skills_must'].map(data_repair_functions.nf_skills_repairer)
    nofluff_data['skills_nice'] = nofluff_data['skills_nice'].map(data_repair_functions.nf_skills_repairer)
    #  repair offer link
    nofluff_data['offer_url'] = nofluff_data['offer_url'].map(lambda x: 'https://nofluffjobs.com/pl/job/' + x)
    #  repair cities
    nofluff_data['location'] = nofluff_data['location'].map(data_repair_functions.nf_repair_locations_to_list)
    nofluff_data['location'] = nofluff_data['location'].map(data_repair_functions.nf_repair_locations_final)
    #  repair employment types
    #  1st step is to change dict to list and get rid of excess info
    nofluff_data['employment_types'] = \
        nofluff_data['employment_types'].map(data_repair_functions.nf_employment_wages_repairer)
    #  2nd step is to split into their own columns
    #  salaries for b2b
    nofluff_data['b2b_min'] = nofluff_data['b2b_max'] = nofluff_data['employment_types'].map(
        lambda x: data_repair_functions.b2b_salaries(x))
    nofluff_data['b2b_min'] = nofluff_data['b2b_min'].map(lambda x: x[0] if x is not None else x)
    nofluff_data['b2b_max'] = nofluff_data['b2b_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    #  salaries for permanent
    nofluff_data['permanent_min'] = nofluff_data['permanent_max'] = \
        nofluff_data['employment_types'].map(data_repair_functions.permanent_salaries)
    nofluff_data['permanent_min'] = nofluff_data['permanent_min'].map(lambda x: x[0] if x is not None else x)
    nofluff_data['permanent_max'] = nofluff_data['permanent_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    #  salaries for mandate contract
    nofluff_data['mandate_min'] = nofluff_data['mandate_max'] = \
        nofluff_data['employment_types'].map(data_repair_functions.mandate_salaries)
    nofluff_data['mandate_min'] = nofluff_data['mandate_min'].map(lambda x: x[0] if x is not None else x)
    nofluff_data['mandate_max'] = nofluff_data['mandate_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    nofluff_data[['b2b_min', 'b2b_max', 'permanent_min', 'permanent_max', 'mandate_min', 'mandate_max']] = \
        nofluff_data[['b2b_min', 'b2b_max', 'permanent_min', 'permanent_max', 'mandate_min', 'mandate_max']].fillna(0)
    #  b2b, permanent true/false
    nofluff_data['employment_type'] = nofluff_data['employment_types'].map(data_repair_functions.employment_type)
    nofluff_data['employment_type'] = nofluff_data['employment_type'].map(
        lambda x: [item.replace('zlecenie', 'mandate_contract') for item in x])
    #  we can safely drop 'employment_types'
    nofluff_data.drop(columns='employment_types', inplace=True)
    #  to repair skills/tech we have to do it in several steps
    #  step 1: plucking just skills (keys) from dictionaries
    nofluff_data['skills_must'] = nofluff_data['skills_must'].map(data_repair_functions.pick_skills_from_dicts)
    nofluff_data['skills_nice'] = nofluff_data['skills_nice'].map(data_repair_functions.pick_skills_from_dicts)
    #  step 2: cleaning from excess spaces and lowering to not miss out duplicates in next step
    nofluff_data['skills_must'].update(nofluff_data['skills_must'].map(
        lambda x: [item.lower().strip() for item in x]))
    nofluff_data['skills_nice'].update(nofluff_data['skills_nice'].map(
        lambda x: [item.lower().strip() for item in x]))
    #  step 3: replacing duplicates
    nofluff_data['skills_must'] = nofluff_data['skills_must'].map(data_repair_functions.remove_duplicates_from_techs)
    nofluff_data['skills_nice'] = nofluff_data['skills_nice'].map(data_repair_functions.remove_duplicates_from_techs)
    #  sums skills from both categories
    all_skills = nofluff_data['skills_must'].sum() + nofluff_data['skills_nice'].sum()
    return nofluff_data, all_skills


def justjoin_repair_procedure(given: list):
    """Data standardization os its similar to nofluff data."""
    justjoin_data = pandas.DataFrame(given)
    #  repair skills
    justjoin_data['skills_must'] = justjoin_data['skills'].map(data_repair_functions.jj_skills_repairer)
    justjoin_data['skills_nice'] = ''
    justjoin_data['skills_nice'] = justjoin_data['skills_nice'].map(lambda x: {} if x == '' else {})
    #  repair offer link
    justjoin_data['offer_url'] = justjoin_data['offer_url'].map(lambda x: 'https://justjoin.it/offers/' + x)
    #  repair cities so it's similar to nofluff data
    justjoin_data['remote'] = justjoin_data['remote'].map(lambda x: 'Remote,' if x is True else ',')
    justjoin_data['location'] = justjoin_data['remote'] + justjoin_data['location']
    justjoin_data.drop('remote', axis=1, inplace=True)
    justjoin_data['location'] = justjoin_data['location'].map(data_repair_functions.jj_repair_locations_final)
    #  list experience_level so its the same as in nofluff
    justjoin_data['experience'] = justjoin_data['experience'].map(lambda x: [x.capitalize()])
    #  repair employment types
    #  1st step is to change dict to list and get rid of excess info
    justjoin_data['employment_types'] = justjoin_data['employment_types'].map(
        data_repair_functions.jj_employment_types_repairer)
    #  2nd step is to split into their own columns
    #  salaries for b2b
    justjoin_data['b2b_min'] = justjoin_data['b2b_max'] = \
        justjoin_data['employment_types'].map(data_repair_functions.b2b_salaries)
    justjoin_data['b2b_min'] = justjoin_data['b2b_min'].map(lambda x: x[0] if x is not None else x)
    justjoin_data['b2b_max'] = justjoin_data['b2b_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    #  salaries for permanent
    justjoin_data['permanent_min'] = justjoin_data['permanent_max'] = \
        justjoin_data['employment_types'].map(data_repair_functions.permanent_salaries)
    justjoin_data['permanent_min'] = justjoin_data['permanent_min'].map(lambda x: x[0] if x is not None else x)
    justjoin_data['permanent_max'] = justjoin_data['permanent_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    #  salaries for mandate contract
    justjoin_data['mandate_min'] = justjoin_data['mandate_max'] = \
        justjoin_data['employment_types'].map(data_repair_functions.mandate_salaries)
    justjoin_data['mandate_min'] = justjoin_data['mandate_min'].map(lambda x: x[0] if x is not None else x)
    justjoin_data['mandate_max'] = justjoin_data['mandate_max'].map(
        lambda x: (x[1] if len(x) > 1 else x[0]) if x is not None else x)
    justjoin_data[['b2b_min', 'b2b_max', 'permanent_min', 'permanent_max', 'mandate_min', 'mandate_max']] = \
        justjoin_data[['b2b_min', 'b2b_max', 'permanent_min', 'permanent_max', 'mandate_min', 'mandate_max']].fillna(0)
    #  b2b, permanent true/false
    justjoin_data['employment_type'] = justjoin_data['employment_types'].map(data_repair_functions.employment_type)
    justjoin_data['employment_type'] = justjoin_data['employment_type'].map(
        lambda x: [item.replace('zlecenie', 'mandate_contract') for item in x])
    #  we can safely drop 'employment_types'
    justjoin_data.drop(columns='employment_types', inplace=True)
    #  to repair skills/tech we have to do it in several steps
    #  step 1: plucking just skills (keys) from dictionaries
    justjoin_data['skills_must'] = justjoin_data['skills_must'].map(data_repair_functions.pick_skills_from_dicts)
    justjoin_data['skills_nice'] = justjoin_data['skills_nice'].map(data_repair_functions.pick_skills_from_dicts)
    #  step 2: cleaning from excess spaces and lowering to not miss out duplicates in next step
    justjoin_data['skills_must'].update(justjoin_data['skills_must'].map(
        lambda x: [item.lower().strip() for item in x]))
    #  step 3: replacing duplicates
    justjoin_data['skills_must'] = justjoin_data['skills_must'].map(data_repair_functions.remove_duplicates_from_techs)
    #  sums skills from both categories
    all_skills = justjoin_data['skills_must'].sum() + justjoin_data['skills_nice'].sum()
    return justjoin_data, all_skills


def get_skills_x_plus(all_skills_jj: list, all_skills_nf: list, x: int) -> list:
    """Sums all skills from both datasets, counts their occurrence and discards all with occurrence < x."""
    all_skills = all_skills_jj + all_skills_nf
    all_skills_dict = dict(Counter(all_skills))
    skills_x_plus = []
    for key, value in all_skills_dict.items():
        if value >= x:
            skills_x_plus.append(key)
    return skills_x_plus


def both_repair_procedure(justjoin_data: pandas.DataFrame,
                          nofluff_data: pandas.DataFrame,
                          skills_x_plus: list) -> pandas.DataFrame:
    """Cleans skills - if skill doesn't appear in skills_x_plus list, it gets discarded.
    Joins both DFs and returns, clean, standardized data set that contains all job offers from justjoin and nofluff."""
    all_data = pandas.concat([justjoin_data, nofluff_data], axis=0)
    all_data.reset_index(drop=True, inplace=True)
    all_data['skills_must'] = all_data['skills_must'].map(
        lambda x: data_repair_functions.drop_all_rares(x, skills_x_plus))
    all_data['skills_nice'] = all_data['skills_nice'].map(
        lambda x: data_repair_functions.drop_all_rares(x, skills_x_plus))
    #  reorder columns
    all_data = all_data[['title',
                         'location',
                         'company',
                         'company_size',
                         'experience',
                         'employment_type',
                         'b2b_min',
                         'b2b_max',
                         'permanent_min',
                         'permanent_max',
                         'mandate_min',
                         'mandate_max',
                         'skills_must',
                         'skills_nice',
                         'expired',
                         'expired_at',
                         'scraped_at',
                         'jobsite',
                         'offer_url']]
    return all_data
