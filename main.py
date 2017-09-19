# TODOS
# Add function to take care of cases with paired subjunctions, e.g. і він, і вона (і Ігор, і Іван)

import re

# Input text
text = str(input())

# Global variables
original = text
conjunctions = ['й', 'та', 'і']
boundaries = ['[аоуиіеяюєї]', '[^аоуіиеяюєї]']

# vowel /й/ vowel,  vowel /та/ consonant, consonant /і/ consonant
def editRegulars(text, start, end, correctConjunction):
  for conjunction in conjunctions:
    searchReg = r'{}\b\s{}\s\b{}'.format(start, conjunction, end)                   
    substrings = re.compile(searchReg, flags = re.I).findall(text)
    for substring in substrings:
      subReg = r'\s{}\s'.format(conjunction)
      result = re.compile(subReg).sub(' ' + correctConjunction + ' ', substring)
      text = text.replace(substring, result)
  corrected = text
  return corrected

# (consonant /i/ vowel), ([.,:;–] і ...), (І ...) 
def editExceptions(text):
  for conjunction in conjunctions:
    pattern1 = r'\b{}\s\b[^і]'.format(conjunction[0].upper())
    pattern2 = r'[^аоуиіеяюєї]\b\s{}\s\b[аоуиеяюєї]'.format(conjunction)
    pattern3 = r'[.,:;\–)]\s{}\s\b[^і]'.format(conjunction)
    patterns = [pattern1, pattern2, pattern3]
    for pattern in patterns:
      substrings = re.compile(pattern, flags = re.I).findall(text)
      for substring in substrings:
        if substring[2].isupper():
          subReg = r'\s{}\s'.format(conjunction.replace(conjunction[0], conjunction[0].upper()))
          result = re.compile(subReg).sub(' ' + 'І' + ' ', substring)
        elif substring[0].isupper():
          subReg = r'^{}\s'.format(conjunction.replace(conjunction[0], conjunction[0].upper()))
          result = re.compile(subReg).sub('І' + ' ', substring)
        else:
          subReg = r'\s{}\s'.format(conjunction)
          result = re.compile(subReg).sub(' ' + 'і' + ' ', substring)
        text = text.replace(substring, result)
  woExceptions = text
  return woExceptions

# Fix for cases, when next word begins with "і"
def fix(text):
  cases = re.findall(r'.?\s?\bі\s\bі', text, flags = re.I)
  for case in cases:
    if len(case) > 3:
      if case[2].isupper():
        conjunction = "Та"
      else:
        conjunction = "та"
      subReg = r'\s{}\s'.format(case[2])
      result = re.compile(subReg).sub(' ' + conjunction + ' ', case)
    else:
      conjunction = "Та"
      subReg = r'\b{}\s'.format(conjunction)
      result = re.compile(subReg).sub('Та' + ' ', case)
    text = text.replace(case, result)
  fixed = text
  return fixed

# Main function
def interchange(text):
  for i in range(2):
    for j in range(2):
      if i == 1 and j == 0:
        continue
      text = editRegulars(text, boundaries[i], boundaries[j], conjunctions[i + j])
  text = editExceptions(text)
  corrected = fix(text)
  # print(original)
  print(corrected)

interchange(text)