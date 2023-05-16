import pandas as pd
import re
from fuzzywuzzy import process
from functools import lru_cache, partial
from concurrent.futures import ThreadPoolExecutor
import openai


class TextDetectionFuzzRegex:
    def __init__(
        self,
        keyword,
        alias=None,
        prefix_words=[],
        divisors=[' ', '-', '.', '_'],
        tol_space=4,
        verbose=False
    ) -> None:
        if not alias:
            alias = keyword
        self.verbose = verbose
        self._exe = ThreadPoolExecutor()
        self._map = dict((x.lower(), y) for x, y in zip(keyword, alias))
        self._keys = list(self._map.keys())
        keyword = list(self.__drop_upper_case(keyword))
        self._regex = self.__build(keyword, divisors, prefix_words, tol_space)

    def __run_until(self, word, divisors):
        if not word:
            return None

        for i, c in enumerate(word):
            if c in divisors:
                return word[:i], word[i+1:]

        return None

    def __split(self, word, divisors):
        result = []
        while (info := self.__run_until(word.strip(), divisors)):
            subs, word = info
            result.append(subs.lower())

        if word:
            result.append(word.lower())

        return result

    def is_lower(self, text):
        return text.lower() == text

    def is_upper(self, text):
        return text.upper() == text

    def __drop_upper_case(self, keyword):
        for kw in keyword:
            rkw = kw[0]
            for i in range(1, len(kw)):
                if (
                    re.fullmatch(r'[a-zA-Z]{2}', kw[i-1: i+2])
                    and self.is_lower(kw[i-1])
                    and self.is_upper(kw[i])
                ):
                    rkw += ' '
                rkw += kw[i]

            yield rkw

    def __clean_word(self, word: str):
        for c in ['+', '*', '(', ')', '$', '?', '|']:
            word = word.replace(c, f'\{c}')

        return word

    def __build(self, keyword, divisors, prefix_words, tol_space):
        result = []
        for splitted_kw in self._exe.map(
            partial(self.__split, divisors=divisors),
            keyword
        ):
            regex = r'(?:(?<!\w|\d)'
            for i, word in enumerate(splitted_kw):

                if len(word) > 4:
                    regex += '(?:'
                    for j in range(1, len(word)):
                        regex += f'{self.__clean_word(word[:j-1])}.?{self.__clean_word(word[j:])}|'

                    regex += self.__clean_word(word[:-1]) + '.?)'
                else:
                    regex += self.__clean_word(word)

                if i < len(splitted_kw) - 1:
                    regex += '.{0,' + str(tol_space) + '}'

            regex += r'(?!\w|\d))'
            if self.verbose:
                print(splitted_kw, regex)

            assert re.match(regex, ' '.join(splitted_kw)), (splitted_kw, regex)
            assert not re.match(regex, ' '), (splitted_kw, regex)

            result.append(regex)

        return result


class SingleRegexFind(TextDetectionFuzzRegex):

    def __init__(self, *arg, **kwds) -> None:
        super().__init__(*arg, **kwds)

        self._regex = re.compile('|'.join(self._regex), re.IGNORECASE)

    def predict(self, text):
        entities = self._regex.findall(text)

        @lru_cache
        def mapper(title):
            results = process.extractBests(title, self._keys, limit=1)
            word, score = results[0]

            if self.verbose:
                print('{:<20}|{:<20}|{:<20}'.format(title, word, score))

            if score > 90:
                return self._map[word]

        return list(set(filter(lambda x: mapper(x), entities)))


class NRegexFind(TextDetectionFuzzRegex):

    def __init__(self, *arg, **kwds) -> None:
        super().__init__(*arg, **kwds)

        self._regex = list(self._exe.map(
            re.compile, self._regex, [re.IGNORECASE]*len(self._regex)
        ))

    def predict(self, text):

        entities = [
            e for entities in self._exe.map(
                lambda x: x.findall(text), self._regex
            )
            for e in entities
        ]

        @lru_cache
        def mapper(title):
            results = process.extractBests(title, self._keys, limit=1)
            word, score = results[0]

            if self.verbose:
                print('{:<20}|{:<20}|{:<20}'.format(title, word, score))

            if score > 90:
                return self._map[word]

        return list(set(filter(lambda x: mapper(x), entities)))


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


LLM_PROMPT = """Analyze each of the job offers below and list each of the skills mentioned in them. \
In the list should appear each of the skills as summarized as possible, use aliases, acronyms, synonyms, etc. \
Pay more attention on the skills and requirements needed to get the job. \
And classify Each element in the list in skill, programming language, benefits, experience, availability, modality, academic level or industry.

Offer Text: Empresa requiere personal para su área de desarrollo, \
Título Técnico o Universitario de Ingeniería Ejecución Informática Análisis de Sistemas o carrera afín  \
Programador Web con conocimientos en PHP, JAVA, JAVASCRIPT, JQUERY, BOOTSTRAP, MYSQL. Experiencia mínima 1 año.\
Además se requieren conociemientos de docker y manejo de Visual Studio Code.
Se requiere disponibilidad para 40 horas semanales y reuniones presenciales semanales (model de trabajo hibrido). 

Skills:
0- technical or university (academic level)
1- php (programming language)
2- java (programming language)
3- javascript (programming language)
4- jquery (skill)
5- bootstrap (skill)
6- mysql (skill)
7- +1 years (experience)
8- docker (skill)
9- vs code (skill)
10- it services (industry)
11- 40hrs/week (availability) 
12- hibrid (modality)

Offer Text: {offer}

Skills:
{skills}"""


def deep_split(text):
    if 3000 >= len(text):
        return [text]
    return deep_split(text[:int(len(text)/2)]) + deep_split(text[int(len(text)/2):])


def post_openai(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4097 - len(prompt),
    )

    return response.choices[0].text.strip()


def llm_predict(offer, skills):
    p = LLM_PROMPT.format(offer=offer, skills=skills)
    if 3000 >= len(p):
        return post_openai(p)

    for sub_offer in deep_split(offer):
        p = LLM_PROMPT.format(offer=sub_offer, skills=skills)
        skills += post_openai(p)
        skills += '\n'

    return skills


if __name__ == '__main__':
    from test_skills import data

    skills = pd.read_csv('./asserts/skills.csv')
    companies = pd.read_csv('./asserts/companies.csv')

    skills = [x for x in skills['skills'] if type(x) == str and x]

    model = NRegexFind(
        skills,
        prefix_words=companies['name'].to_list(),
        verbose=True
    )

    for d in data:
        print(model.predict(d))
