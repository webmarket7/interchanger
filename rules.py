import re

# TODO:
# 1. Implement logic for tag processor

class Text(object):

  def __init__(self, text):
    self.text = text

  def breakInSentences(self):
    start = 0
    sentences = []
    pattern = re.compile(r'[.:;!]\s|[.:;!]\n|[.:;!]$')
    delimiters = pattern.findall(self.text)
    for delimiter in delimiters:
      match = pattern.search(self.text, start)
      end = match.start() + 1
      sentences.append(self.text[start:end])
      start = match.end()
    return sentences
  
class Sentence(Text):

  def __init__(self, sentence):
    self.sentence = sentence
    
  def findCases(self):
    pattern = re.compile(r'(\b\S?|\w+\b)\s?([йіувз]|із|зі|та)\s(\b\S\W|\b\w+)', flags = re.I)
    cases = pattern.findall(self.sentence)
    return cases
    
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
    self.startSound = self.getStartSound()
    self.endSound = self.getEndSound()
  
  def getStartSound(self):
    if self.script == 'cyrrilic':
      vowels = ['а', 'о', 'у', 'и', 'і', 'е', 'я', 'ю', 'є', 'ї']
      if self.el[0] in (vowels or map(str.upper, vowels)): return 'vowel'
      else: 
        if re.match(r'\b[зсцшщ][^аоуиіеяюєї]', self.el, flags = re.I) is not None: return 'consonant+'
        else: return 'consonant'
    elif self.script == 'latin':
      vowels = ['а', 'e', 'i', 'o', 'u', 'y']
      exceptions = ['hour', 'honest', 'honour', 'honor', 'heir']
      if self.el[0] in (vowels or map(str.upper, vowels)) or self.el in exceptions: return 'vowel'
      else: return 'consonant'

  def getEndSound(self):
    if self.script == 'cyrrilic':
      vowels = ['а', 'о', 'у', 'и', 'і', 'е', 'я', 'ю', 'є', 'ї']
      if self.el[-1] in (vowels or map(str.upper, vowels)): return 'vowel'
      else: return 'consonant'
    elif self.script == 'latin': 
      charset1 = ['a', 'r', 'o', 'u', 'w']
      charset2 = ['e', 'h', 'y', 'i']
      if self.el[-1] in (charset1 or map(str.upper, charset1)): return 'vowel'
      elif self.el[-1] in (charset2 or map(str.upper, charset2)):
        if self.el[-1] == ('e' or 'E'):   return self.caseE()
        elif self.el[-1] == ('h' or 'H'): return self.caseH()
        elif self.el[-1] == ('y' or 'Y'): return self.caseY()
        elif self.el[-1] == ('i' or 'I'): return self.caseI()
      else: return 'consonant'
        
  def caseE(self):
    charset3 = ['c', 'd', 'f', 'g', 'k', 'l', 'p', 's', 't', 'v', 'x', 'y', 'z']
    charset4 = ['b', 'h', 'i', 'm', 'n', 'u']
    if self.el[-2] in (charset3 or map(str.upper, charset3)): return 'consonant'
    elif self.el[-2] in (charset4 or map(str.upper, charset4)):
      if self.el[-2] == ('i' or 'I'):
        if len(self.el) == 3: return 'consonant'
        else: return 'vowel'
      else:
        if self.el in self.exceptions: return 'vowel'
        else: return 'consonant'
    else: return 'vowel'
  
  def caseH(self):
    charset5 = ['c', 'p', 't']   
    if self.el[-2] in (charset5 or map(str.upper, charset5)): return 'consonant'
    elif self.el[-2] == ('g' or 'G'):
      if self.el in self.exceptions: return 'vowel'
      else: return 'consonant'
    else: return 'vowel'
      
  def caseY(self):
    charset6 = ['a', 'o', 'u']
    charset7 = ['r', 'h', 'e']
    if self.el[-2] in (charset6 or map(str.upper, charset6)): return 'consonant'
    elif self.el[-2] in (charset7 or map(str.upper, charset7)):
      if self.el[-2] == ('e' or 'E'):
        if self.el[-3] == ('h' or 'H'): return 'consonant'
        else: return 'vowel'
      else:
        if len(self.el) == 3: return 'consonant'
        else: return 'vowel'
    else: return 'vowel'
      
  def caseI(self):
    charset8 = ['a', 'e']
    if self.el[-2] in (charset8 or map(str.upper, charset8)): return 'consonant'
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
    self.rule = self.getRule()
    self.correct = self.findCorrect()
    self.evaluation = self.evaluate()

  def getRuleSet(self):
    if self.linkword in ['й', 'Й', 'та', 'Та', 'і', 'І']:
      return  [ {'before': 'vowel',     'correct': 'й',  'after': 'vowel',                               'exceptions': ['й', 'є', 'ї', 'ю', 'я']},
                {'before': 'vowel',     'correct': 'та', 'after': ['vowel', 'consonant', 'consonant+'],  'exceptions': ['а', 'о', 'у', 'и', 'е']},
                {'before': 'consonant', 'correct': 'і',  'after': ['vowel', 'consonant', 'consonant+'],  'exceptions': 'і'},
                {'before': 'linestart', 'correct': 'І',  'after': ['consonant', 'consonant+'],           'exceptions': 'і'} ]
    elif self.linkword in ['у', 'У', 'в', 'В']:
      return  [ {'before': 'linestart', 'correct': 'В',  'after': 'vowel',                     'exceptions': []},
                {'before': 'vowel',     'correct': 'в',  'after': 'vowel',                     'exceptions': []},
                {'before': 'consonant', 'correct': 'в',  'after': 'vowel',                     'exceptions': []},
                {'before': 'linestart', 'correct': 'У',  'after': ['consonant', 'consonant+'], 'exceptions': []},
                {'before': 'consonant', 'correct': 'у',  'after': ['consonant', 'consonant+'], 'exceptions': []},
                {'before': 'vowel',     'correct': 'у',  'after': ['consonant', 'consonant+'], 'exceptions': ['в', 'ф', 'льв', 'св', 'тв', 'хв', 'зв', 'гв', 'дв']} ]
    elif self.linkword in ['з', 'З', 'із', 'Із', 'зі', 'Зі']:
      return  [ {'before': 'linestart',            'correct': 'З',  'after': ['consonant', 'vowel'], 'exceptions': []},
                {'before': ['consonant', 'vowel'], 'correct': 'з',  'after': 'vowel',                'exceptions': []},
                {'before': 'vowel',                'correct': 'з',  'after': 'consonant',            'exceptions': []},
                {'before': 'consonant',            'correct': 'із', 'after': 'consonant',            'exceptions': []},
                {'before': ['consonant', 'vowel'], 'correct': 'зі', 'after': 'consonant+',           'exceptions': []}]
    else: print('ERROR: Unknown link-word!')
      
  
  def getRule(self):
      for rule in self.ruleset:
        if self.before in rule.get('before'):
          if self.after in rule.get('after'):
            exceptions = rule.get('exceptions')
            if len(exceptions) > 0:
              for exception in exceptions:
                if len(self.after) >= len(exception):
                  if self.case[2][0:len(exception)] != exception:
                    return rule
            else: return rule
  
  def findCorrect(self):
    return self.rule.get('correct')
      
  def evaluate(self):
    if self.linkword == self.correct: return 'correct'
    else: return 'wrong'

def check(string):
  text = Text(string)
  sentences = text.breakInSentences()
  for sentence in sentences:
    cases = Sentence(sentence).findCases()
    for item in cases:
      print(item)
      case = Rule(item)
      print('Evaluation: ' + case.evaluation)
      print('Correct link-word: ' + case.correct)
      
myString = '''Я маю що сказати і чому. У Маші вдома живуть кіт та собака. Відкриється електронна таблиця для перевірки розрахунку й автоматично обчислить математичні вирази. Та вже ж гарні!'''
      
check(myString)