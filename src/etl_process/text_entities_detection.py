import pandas as pd
import re
from fuzzywuzzy import process
from functools import lru_cache


def build_regex(tags: list[str], dividers=[r'\s', r'\.', r'\-', r"\'"], companies=[]):
    regex = []
    regex_div = f"[{'|'.join(dividers)}]*"
    for tag in tags:
        tag = tag.strip()
        ntag, index, first_step, companies_regex = '', 0, True, ''
        while index < len(tag):
            replace = False
            try:
                while tag[index] in [' ', '.', '-', "'"]:
                    index += 1
                    replace = True
            except IndexError:
                break
            if first_step and replace and ntag in companies:
                companies_regex = '(?:' + ntag + '}){0,1}'
                first_step = False
                ntag = ''
            if replace or (
                index != 0 and
                # Check case changes
                re.fullmatch(r'\w', tag[index: index+2]) and
                tag[index] == tag[index].upper() and
                tag[index - 1] == tag[index - 1].lower()
            ):
                ntag += regex_div
            if tag[index] in ['+', '*', '(', ')', '$', '?', '|']:
                ntag += '\\' + tag[index]
            else:
                ntag += tag[index]
            index += 1
        # Check the open and the end because
        # substr of alpha-numeric words can't be detected
        regex.append(r'(?<!\w|\d)' + companies_regex + ntag + r'(?!\w|\d)')
    return '|'.join(regex)


def build_language_programming_detector():

    lp = pd.read_csv('./asserts/programming_languages.csv')

    refactors = [(x.replace('++', '-plus-plus'), x.lower())
                 for x in lp['name'] if '++' in x]
    refactors += [(x.replace('#', '-sharp'), x.lower())
                  for x in lp['name'] if '#' in x]
    refactors += [(x.replace('*', '-star'), x.lower())
                  for x in lp['name'] if '*' in x]

    theasuarus = dict([(x, x.lower()) for x in lp['name']] + refactors)

    lp_regex = build_regex(lp['name'].to_list() + [x for x, _ in refactors])
    lp_pattern = re.compile(lp_regex, re.IGNORECASE)

    theasuarus['TS'] = 'typescript'
    theasuarus['Golang'] = 'go'
    theasuarus['JS'] = 'javascript'

    lps_keys = list(theasuarus.keys())

    @lru_cache
    def lp_mapper(title):
        results = process.extractBests(title, lps_keys, limit=1)
        lp, score = results[0]
        if score > 70:
            return theasuarus[lp]

    def lp_detector(text, exe):
        lps = lp_pattern.findall(text)
        return list(set(filter(lambda x: x, exe.map(lp_mapper, lps))))

    return lp_detector


def build_skills_detector():

    skills = pd.read_csv('./asserts/skills.csv')
    companies = pd.read_csv('./asserts/companies.csv')

    skills = [x for x in skills['skills'] if type(x) == str and x]

    skills_regex = build_regex(skills, companies=companies['name'].to_list())
    skills_pattern = re.compile(skills_regex, re.IGNORECASE)

    # skills_theasuarus = dict((x,x) for x in skills)

    @lru_cache
    def skill_mapper(title):
        results = process.extractBests(title, skills, limit=1)
        skill, score = results[0]
        if score > 70:
            return skill

    def skill_detector(text, exe):
        skills = skills_pattern.findall(text)
        # return skills
        return list(set(filter(lambda x: x, exe.map(skill_mapper, skills))))

    return skill_detector
