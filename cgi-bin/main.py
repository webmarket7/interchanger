import re, json
from itertools import chain
from collections import Counter


# TODOS:
# 1. Implement logic for tag processor
# 2. Implement logic for interchange within a sentence

class Options(object):
  
  def __init__(self):
    self.lwSet = self.getLWSet()

  def getLWSet(self):
    return ['і|й|та', 'у|в', 'з|із|зі']

class Text(object):
  
  def __init__(self, text):
    self.text = text
    self.sentences = self.breakInSentences()
    
  def breakInSentences(self):
    return list(map(lambda s: s.strip(' '), re.findall(r'.+?[.:;?!]|.+', self.text, flags = re.M)))
    
class Sentence(object):
  
  def __init__(self, element):
    self.content = element

  def findCases(self, linkwords):
    def findByPattern(linkwords):
       regExp = r'([,–—]|\w+\b|^)\s?({})\s(\b\S\W|\b\w+)'.format(linkwords) 
       pattern = re.compile(regExp, flags = re.I)
       return pattern.findall(self.content)
    return list(chain.from_iterable(list(filter(lambda x: len(x) > 0, list(map(findByPattern, linkwords))))))
  
  def performQA(self):
    occurences = re.findall(r'(<span class=correct>)(і|й|та)(<\/span)', self.content, flags = re.I)
    subjunctions = list(map(lambda x: x[1], occurences))
    warnings = []
    if len(subjunctions) >= 2:
      counted = dict(Counter(subjunctions))
      for subj in ['й', 'і']:
        if subj in counted.keys() and counted.get(subj) >= 2:
          # note = 'NOTE. There are', counted.get(subj), ' occurences of  \"' + subj + '\" in this segment. It is recommended to use preposition \"та\" if a sentence already contains preposition \"й\" or \"і\".'
          warnings.append((subj, counted.get(subj)))
    if len(warnings) > 0:
      return True
    else: return False

class Element(object):
  
  def __init__(self, el, pos):
    self.el = el
    self.pos = pos
    
  def getScript(self):
    if re.findall(u"[\u0400-\u0500]+", self.el): return 'cyrrilic'
    else: return 'latin'
    
  def makeObject(self):
    if len(self.el) > 0:     
      if self.el.isalpha():
        if self.el.isupper(): return Acronym(self.el)
        else: return Word(self.el)
      elif self.el.isdigit(): return Number(self.el)
      else:
        if self.el[-1] in [',', '.', ':', ';', '–', '—']: return Delimiter(self.el)
        elif self.el[0].isdigit() or self.el[-1].isdigit():
          if self.el[-1].isdigit() and self.pos == 0: return Number(self.el)
          elif self.el[0].isdigit() and self.pos == 2: return Number(self.el)
          else: return Word(self.el)
        elif self.el[0] == '<' and self.el[-1] == '>': return Tag(self.el)
        else: print('Problem occured while creating object')
    else: return LineStart()
      
class Acronym(Element):
  
  def __init__(self, el):
    self.el = el  
    self.script = self.getScript()
    self.startSound = self.getStartSound()
    self.endSound = self.getEndSound()
    
  def getStartSound(self):
    if self.script == 'cyrrilic':
      cyrrilicVowels = ['А', 'Е', 'Є', 'И', 'І', 'Ї', 'Л', 'М', 'Н', 'О', 'Р', 'С', 'У', 'Ф', 'Ю', 'Я']
      if self.el[0] in cyrrilicVowels: return 'vowel'
      else: return 'consonant'
    elif self.script == 'latin':
      latinVowels = ['A', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'R', 'S', 'U', 'X']
      if self.el[0] in latinVowels: return 'vowel'
      else: return 'consonant'

  def getEndSound(self):
    if self.script == 'cyrrilic':
      cyrrilicConsonants = ['Й', 'Л', 'М', 'Н', 'Р', 'С', 'Ф']
      if self.el[-1] in cyrrilicConsonants: return 'consonant'
      else: return 'vowel'
    elif self.script == 'latin':
      latinConsonants = ['F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'S', 'X', 'Z']
      if self.el[-1] in latinConsonants: return 'consonant'
      else: return 'vowel'

class Word(Element):

  exceptions = ['be', 'he', 'me', 'acme', 'acne', 'bacne', 'she', 'the', 'argue', 'ague', 
                'die', 'lie', 'pie', 'vie', 'through', 'plough', 'borough', 'bough', 
                'dough', 'furlough', 'though', 'thorough']
  
  def __init__(self, el):
    self.el = el  
    self.script = self.getScript()
    self.endSound = self.getEndSound()
    self.startSound = self.getStartSound()

  def ignoreCase(self, myList):
    upper = list(map(str.upper, myList))
    myList.extend(upper)
    return myList
  
  def getStartSound(self):
    if self.script == 'cyrrilic':
      vowels = ['а', 'о', 'у', 'и', 'і', 'е', 'я', 'ю', 'є', 'ї']
      if self.el[0] in self.ignoreCase(vowels): return 'vowel'
      else: 
        if re.match(r'\b[зсцшщ][^аоуиіеяюєї]', self.el, flags = re.I) is not None: return 'consonant+'
        else: return 'consonant'
    elif self.script == 'latin':
      vowels = ['а', 'e', 'i', 'o', 'u', 'y']
      exceptions = ['hour', 'honest', 'honour', 'honor', 'heir']
      if self.el[0] in self.ignoreCase(vowels) or self.el in exceptions: return 'vowel'
      else: return 'consonant'

  def getEndSound(self):
    if self.script == 'cyrrilic':
      vowels = ['а', 'о', 'у', 'и', 'і', 'е', 'я', 'ю', 'є', 'ї']
      if self.el[-1] in self.ignoreCase(vowels): return 'vowel'
      else: return 'consonant'
    elif self.script == 'latin': 
      charset1 = ['a', 'r', 'o', 'u', 'w']
      charset2 = ['e', 'h', 'y', 'i']
      if self.el[-1] in self.ignoreCase(charset1): return 'vowel'
      elif self.el[-1] in self.ignoreCase(charset2):
        if self.el[-1] == ('e' or 'E'):   return self.caseE()
        elif self.el[-1] == ('h' or 'H'): return self.caseH()
        elif self.el[-1] == ('y' or 'Y'): return self.caseY()
        elif self.el[-1] == ('i' or 'I'): return self.caseI()
      else: return 'consonant'
        
  def caseE(self):
    charset3 = ['c', 'd', 'f', 'g', 'k', 'l', 'p', 's', 't', 'v', 'x', 'y', 'z']
    charset4 = ['b', 'h', 'i', 'm', 'n', 'u']
    if self.el[-2] in self.ignoreCase(charset3): return 'consonant'
    elif self.el[-2] in self.ignoreCase(charset4):
      if self.el[-2] == ('i' or 'I'):
        if len(self.el) == 3: return 'consonant'
        else: return 'vowel'
      else:
        if self.el in self.exceptions: return 'vowel'
        else: return 'consonant'
    else: return 'vowel'
  
  def caseH(self):
    charset5 = ['c', 'p', 't']   
    if self.el[-2] in self.ignoreCase(charset5): return 'consonant'
    elif self.el[-2] == ('g' or 'G'):
      if self.el in self.exceptions: return 'vowel'
      else: return 'consonant'
    else: return 'vowel'
      
  def caseY(self):
    charset6 = ['a', 'o', 'u']
    charset7 = ['r', 'h', 'e']
    if self.el[-2] in self.ignoreCase(charset6): return 'consonant'
    elif self.el[-2] in self.ignoreCase(charset7):
      if self.el[-2] == ('e' or 'E'):
        if self.el[-3] == ('h' or 'H'): return 'consonant'
        else: return 'vowel'
      else:
        if len(self.el) == 3: return 'consonant'
        else: return 'vowel'
    else: return 'vowel'
      
  def caseI(self):
    charset8 = ['a', 'e']
    if self.el[-2] in self.ignoreCase(charset8): return 'consonant'
    else: return 'vowel'
  

class Number(Element):
  def __init__(self, el):
    self.el = el  
    self.num = re.findall(r'\d+', self.el)
    self.startSound = self.getStartSound()
    self.endSound = self.getEndSound()
    
  def getStartSound(self):
    if self.num[0] == '11' or self.num[0] == '1': return 'vowel'
    else: return 'consonant'
    
  def getEndSound(self):
    if self.num[-1][-1] in ['2', '3', '4']: return 'vowel'
    else: return 'consonant'

class Delimiter(Element):
  def __init__(self, el):
    self.el = el  
    self.endSound = 'consonant'

class LineStart(Element):
  def __init__(self):
    self.endSound = 'linestart'

class Tag(Element):
  pass

class Rule(object):
  
  def __init__(self, case):
    self.case = case
    self.before = Element(case[0], 0).makeObject().endSound
    self.linkword = self.case[1]
    self.after = Element(case[2], 2).makeObject().startSound
    self.ruleset = self.getRuleSet()
    self.rule, self.correct = self.findCorrect()
    self.evaluation = self.evaluate()

  def getRuleSet(self):
    if self.linkword in ['й', 'Й', 'та', 'Та', 'і', 'І']:
      return  [ {'before': 'vowel',     'correct': 'й',  'after': 'vowel',                               'exceptions': ['й', 'є', 'ї', 'ю', 'я'], 'elseCorrect': 'та'},
                {'before': 'vowel',     'correct': 'та', 'after': ['consonant', 'consonant+'],           'exceptions': [],                        'elseCorrect':  '' },
                {'before': 'consonant', 'correct': 'і',  'after': ['vowel', 'consonant', 'consonant+'],  'exceptions': ['і'],                     'elseCorrect': 'та'},
                {'before': 'linestart', 'correct': 'І',  'after': ['vowel', 'consonant', 'consonant+'],  'exceptions': ['і'],                     'elseCorrect': 'Та'} ]
    elif self.linkword in ['у', 'У', 'в', 'В']:
      return  [ {'before': 'linestart', 'correct': 'В',  'after': 'vowel',                               'exceptions': [],  'elseCorrect': ''},
                {'before': 'vowel',     'correct': 'в',  'after': 'vowel',                               'exceptions': [],  'elseCorrect': ''},
                {'before': 'consonant', 'correct': 'в',  'after': 'vowel',                               'exceptions': [],  'elseCorrect': ''},
                {'before': 'vowel',     'correct': 'в',  'after': ['consonant', 'consonant+'], 
                 'exceptions': ['в', 'ф', 'льв', 'св', 'тв', 'хв', 'зв', 'гв', 'дв'],                                       'elseCorrect': 'у'},
                {'before': 'linestart', 'correct': 'У',  'after': ['consonant', 'consonant+'],           'exceptions': [],  'elseCorrect': ''},
                {'before': 'consonant', 'correct': 'у',  'after': ['consonant', 'consonant+'],           'exceptions': [],  'elseCorrect': ''} ]
    elif self.linkword in ['з', 'З', 'із', 'Із', 'зі', 'Зі']:
      return  [ {'before': 'linestart',            'correct': 'З',  'after': ['consonant', 'vowel'],     'exceptions': [],  'elseCorrect': ''},
                {'before': ['consonant', 'vowel'], 'correct': 'з',  'after': 'vowel',                    'exceptions': [],  'elseCorrect': ''},
                {'before': 'vowel',                'correct': 'з',  'after': 'consonant',                'exceptions': [],  'elseCorrect': ''},
                {'before': 'consonant',            'correct': 'із', 'after': 'consonant',                'exceptions': [],  'elseCorrect': ''},
                {'before': ['consonant', 'vowel'], 'correct': 'зі', 'after': 'consonant+',               'exceptions': [],  'elseCorrect': ''}]
    else: print('ERROR: Unknown link-word!')
      
  
  def findCorrect(self):
      for rule in self.ruleset:
        if self.before in rule.get('before'):
          if self.after in rule.get('after'):
            exceptions = rule.get('exceptions')
            if len(exceptions) > 0:
              for exception in exceptions:
                if len(self.after) >= len(exception):
                  found = []
                  if self.case[2][0:len(exception)] == exception:
                    found.append(exception)
                  else: continue
              if len(found) > 0: return rule, rule.get('elseCorrect')
              else: return rule, rule.get('correct')
            else: return rule, rule.get('correct')

  def evaluate(self):
    if self.linkword == self.correct: return 'correct'
    else: return 'wrong'
    
  def applyRule(self, sentence):
    pattern = re.compile(r'({}\s)({})(\s{})'.format(self.case[0], self.case[1], self.case[2]))
    return re.sub(pattern, r'\g<1>' + '<span class=correct>' + self.correct + '</span>' + r'\g<3>', sentence)
    
  def highlight(self, sentence):
    pattern = re.compile(r'({}\s)({})(\s{})'.format(self.case[0], self.case[1], self.case[2]))
    if self.evaluation == 'correct':
      return re.sub(pattern, r'\g<1>' + '<span class=correct>' + r'\g<2>' + '</span>' + r'\g<3>', sentence)
    elif self.evaluation == 'wrong':
      return re.sub(pattern, r'\g<1>' + '<span class=wrong>' + r'\g<2>' + '</span>' + r'\g<3>', sentence)
    else: print('Error occured while highlighting!')
    
def countCorrections(cases):
  evaluations = list(map(lambda x: x.evaluation, cases))
  wrong = list(filter(lambda x: x == 'wrong', evaluations))
  return len(wrong)
        
def check(string):
  options = Options()
  text = Text(string)
  output = []
  for element in text.sentences:
    sentence = Sentence(element)
    original = sentence.content
    reviewed = sentence.content
    cases = sentence.findCases(options.lwSet)
    if any(cases):
      cases = list(map(Rule, cases))
      corrections = countCorrections(cases)
      for case in cases:
        original = case.highlight(original)
        reviewed = case.applyRule(reviewed)
    warnings = Sentence(reviewed).performQA()
    output.append({'original': original, 'warnings': warnings, 'reviewed': reviewed, 'corrections': corrections})
  encoded = json.dumps(output, ensure_ascii=False)
  print(encoded)
  # with open('data.txt', 'w') as outfile:
  #   json.dump(output, outfile)

  
    
myString = '''Я маю що сказати і чому. У Маші вдома живуть кіт та собака. Відкриється електронна таблиця для перевірки розрахунку й автоматично обчислить математичні вирази. Кабелі, датчики та інше допоміжне обладнання, для яких необхідна електромагнітна сумісність, перелічено в документації з експлуатації, яка входить в комплект постачання цього продукту. Завантажувальний накопичувач, масив RAID 5 із 3 накопичувачів і один запасний накопичувач для масиву RAID. Отака в нас біда\nНі туди, і ні сюди. Шукаємо баги й упиваємося свободою, стріляємо й охаємо. Втомились і лягли, а тоді навідпочивались і встали.'''
      
check(myString)