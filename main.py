import re

text = str(input())

conjunctions = ['і', 'й', 'та']

pre = ['[^аоуиіиеяюєї]', '[аоуиіиеяюєї]']
post = ['[аоуиіиеяюєї]', '[^аоуиіиеяюєї]']

# consonant /i/ vowel, consonant /і/ consonant, vowel /й/ vowel, vowel /та/ consonant 

def interchange(text, start, end, correctConjunction):
  for conjunction in conjunctions:
    searchReg = r'{}\b\s{}\s\b{}'.format(start, conjunction, end)                   
    substrings = re.compile(searchReg, flags = re.I).findall(text)
    for substring in substrings:
      subReg = r'\s{}\s'.format(conjunction)
      result = re.compile(subReg).sub(' ' + correctConjunction + ' ', substring)
      text = text.replace(substring, result)
  corrected = text
  return corrected

# .,:;– і (except i)
exceptions = ['[.,:;\–)]', '[^і]']
  
def checkExceptions(text, start, end, correctConjunction):
  for conjunction in conjunctions:
    searchReg = r'{}\s{}\s\b{}'.format(start, conjunction, end)                   
    substrings = re.compile(searchReg, flags = re.I).findall(text)
    for substring in substrings:
      if substring[2].isupper():
        subReg = r'\s{}\s'.format(conjunction.replace(conjunction[0], conjunction[0].upper()))
        result = re.compile(subReg).sub(' ' + correctConjunction.upper() + ' ', substring)
      else:
        subReg = r'\s{}\s'.format(conjunction)
        result = re.compile(subReg).sub(' ' + correctConjunction + ' ', substring)
      text = text.replace(substring, result)
  woExceptions = text
  return woExceptions  

# Функція для синхронізації третього списка (conjunctions)
def iter(n):
  if n < 2:
    return 0
  else:
    return n - 1

# Основна функція для чергування і, й, та
def main(text):
  n = 0
  for start in pre:
    for end in post:
      text = interchange(text, start, end, conjunctions[iter(n)])
      n += 1
  text = checkExceptions(text, exceptions[0], exceptions[1], conjunctions[0])
  print(text)

main(text)

