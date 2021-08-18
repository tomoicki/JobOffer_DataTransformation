import json
from utilities.data_repair_procedure import nofluff_repair_procedure, justjoin_repair_procedure
from utilities.data_repair_procedure import get_skills_x_plus, both_repair_procedure


with open('nofluff_example_data.json', 'r') as nof:
    nf = json.load(nof)
with open('justjoin_example_data.json', 'r') as jus:
    jj = json.load(jus)

#  data standarization step
#  normally we put list(dict) as nofluff_repair_procedure and justjoin_repair_procedure which was previously
#  gathered by DataExtraction part of the project. As our project is split into separate repositories we cannot
#  directly use DataExtraction functions so to show how the program works we provided example_data.json files.
nofluff, nofluff_skills = nofluff_repair_procedure(nf)
justjoin, justjoin_skills = justjoin_repair_procedure(jj)
all_skills = get_skills_x_plus(nofluff_skills, justjoin_skills, 5)
all_data = both_repair_procedure(justjoin, nofluff, all_skills)

