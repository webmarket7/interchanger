import re

test = '''Риби та ондатри, риби і ондатри. Торт і іриска, Ірак і Іран. Оля і Аня, Оля та Аня. Кіт й миша, кіт та миша. Кріт й Рига, Кріт та Рига.
          Зміст й опис, зміст та опис. Світ й Україна, світ та Україна. Вода й ящірка, Австралія й Ямайка. Він доробив, та все збереглося. 
          Він доробив, й усе збереглося. І Іван любить її. і Іван любить її. Й при цьому він любить її. Та вона любить його. '''


def breakInSentences(text):
  start = 0
  sentences = []
  pattern = re.compile(r'[.:;]\s|[.:;]\n|[.:;]$')
  delimiters = pattern.findall(text)
  for delimiter in delimiters:
    match = pattern.search(text, start)
    end = match.start() + 1
    sentences.append(text[start:end])
    start = match.end()
  return sentences
  
def createPatterns():
  patterns = []  
  vowel = '[аоуиіеяюєї]'
  consonant = '[^аоуіиеяюєї]'
  
  # Wrong patterns - 'й'
  patterns.append(r'{}\b\s{}\s\b{}'.format(consonant, 'й', consonant)) # Кіт й миша, Кріт й Рига. 
  patterns.append(r'{}\b\s{}\s\b{}'.format(consonant, 'й', '[аоуиеяюєї]')) #  Зміст й опис, світ й Україна.
  patterns.append(r'{}\b\s{}\s\b{}'.format(vowel, 'й', '[йєїюя]')) # Вода й ящірка, Австралія й Ямайка.
  patterns.append(r'[,\-\–\—)]\s{}\s\b\w'.format('й')) # Він доробив, й усе збереглося.
  patterns.append(r'^{}\s\b[^і]'.format('Й')) # Й при цьому він любить її.
  
  # Wrong patterns - 'та'
  patterns.append(r'{}\b\s{}\s\b{}'.format(consonant, 'та', consonant)) # Кіт та миша, Кріт та Рига.
  patterns.append(r'{}\b\s{}\s\b{}'.format(vowel, 'та', '[аоуие]')) # Риби та ондатри, Оля та Аня.
  patterns.append(r'{}\b\s{}\s\b{}'.format(consonant, 'та', '[аоуиеяюєї]')) # Зміст та опис, світ та Україна.
  patterns.append(r'[,\-\–\—)]\s{}\s\b\w'.format('та')) # Він доробив, та все збереглося.
  patterns.append(r'^{}\s\b[^і]'.format('Та')) # Та при цьому він любить її.
  
  # Wrong patterns - 'і'
  patterns.append(r'{}\b\s{}\s\b{}'.format(vowel, 'і', '[^йєїюя]')) # Риби і ондатри, Оля і Аня.
  patterns.append(r'.?\s?\bі\s\bі') # Торт і іриска, Ірак і Іран. І Іван любить її.
  
  return patterns

def findAllCases(patterns, sentence):
  cases = []
  for pattern in patterns:
    substrings = re.compile(pattern, flags = re.I).findall(sentence)
    for substring in substrings:
      if len(substring) > 0:
        cases.append(substring)
      else:
        continue
  return cases

def tokenize(text):
  sentences = breakInSentences(text)
  patterns = createPatterns()
  tokens = []
  for sentence in sentences:
    cases = findAllCases(patterns, sentence)
    tokens.append((sentence, cases))
  return tokens

def findConjunction(case):
  if len(case) > 4:
    conjunctions = [' і ', ' та ', ' й ']
  else:
    conjunctions = ['та', 'Та', 'і', 'І', 'й', 'Й']
  for conjunction in conjunctions:
    if conjunction in case:
      break
    else:
      continue
  conjunction = conjunction.strip(' ')
  return conjunction
  
def highlightSource(tokens):
  source = []
  for token in tokens:
    if len(token[1]) == 0:
      segment = token[0]  
    else:
      segment = token[0]
      for case in token[1]:
        conjunction = findConjunction(case)
        if len(case) > 4:
          subReg = r'\s{}\s'.format(conjunction)
          highlighter = re.compile(subReg, flags = re.I).sub('<span style="background-color:#F08080;"> ' + conjunction + ' </span>', case)
        else:
          subReg = r'^{}\s'.format(conjunction)
          highlighter = re.compile(subReg, flags = re.I).sub('<span style="background-color:#F08080;">' + conjunction + ' </span>', case)
        segment = segment.replace(case, highlighter)
    source.append(segment)
  return source
  
def isVowel(letter):
  vowels = ['а', 'А', 'о', 'О', 'у', 'У', 'и', 'И', 'і', 'І', 'е', 'Е', 'я', 'Я', 'ю', 'Ю', 'є', 'Є', 'ї' 'Ї']
  if letter in vowels:
    return True
  else:
    return False
  
def correct(cases):
  data = []
  for case in cases:
    conjunction = findConjunction(case)
    if len(case) > 4:
      start = case[0]
      end = case[-1]
      if isVowel(start) and end in ['а', 'А', 'о', 'О', 'у', 'У', 'и', 'И', 'і', 'І', 'е', 'Е']:      # Риба та ондатри, риба і ондатри. Оля і Аня, Оля та Аня.
        correctConjunction = 'й'
      elif not isVowel(start) and end in ['і', 'І']:                                                  # Торт і іриска, Ірак і Іран.
        correctConjunction = 'та'  
      elif not isVowel(start) and not isVowel(end):                                                   # Кіт й миша, кіт та миша. Кріт й Рига, Кріт та Рига.
        correctConjunction = 'і'
      elif not isVowel(start) and end not in ['і', 'І']:                                              # Зміст й опис, зміст та опис. Світ й Україна, світ та Україна. 
        correctConjunction = 'і'
      elif isVowel(start) and end in ['й', 'Й', 'є', 'Є', 'ї', 'Ї', 'ю', 'Ю', 'я', 'Я']:              # Вода й ящірка, Австралія й Ямайка.
        correctConjunction = 'і'
      elif start in [',', '-', '–', '—', ')'] and end not in ['і', 'І']:                              # Він доробив, та все збереглося. Він доробив, й усе збереглося.
        correctConjunction = 'і'
      else:
        continue
    else:
      end = case[-1]
      if end in ['і', 'І']:                                                                           # І Іван любить її. і Іван любить її.
        if conjunction[0].isupper():
          correctConjunction = 'Та'
        else:
          correctConjunction = 'та'
      elif end not in ['і', 'І']:                                                                     # Й при цьому він любить її. Та при цьому він любить її.  
        if conjunction[0].isupper():
          correctConjunction = 'І'
        else:
          correctConjunction = 'і'
      else:
        continue
    data.append((conjunction, correctConjunction))
  return data

def highlightTarget(tokens):
  target = []
  for token in tokens:
    if len(token[1]) == 0:
      segment = token[0]  
    else:
      segment = token[0]
      data = correct(token[1])
      i = 0
      for item in token[1]:
        conjunction = data[i][0]
        correctConjunction = data[i][1]
        if len(item) > 4:
          subReg = r'\s{}\s'.format(conjunction)
          highlighter = re.compile(subReg, flags = re.I).sub('<span style="background-color:#98FB98;"> ' + correctConjunction + ' </span>', item)
        else:
          subReg = r'^{}\s'.format(conjunction)
          highlighter = re.compile(subReg, flags = re.I).sub('<span style="background-color:#98FB98;">' + correctConjunction + ' </span>', item)
        segment = segment.replace(item, highlighter)
        i += 1
    target.append(segment)
  return target

def main(text):
  tokens = tokenize(text)
  source = highlightSource(tokens)
  target = highlightTarget(tokens)
  print('<table border="1">')
  num = 0
  for num in range(len(source)):
    print('<tr>')
    print('<td>' + str(num + 1) + '</td>')
    print('<td>' + source[num] + '</td>')
    print('<td>' + target[num] + '</td>')
    num += 1
    print('</tr>')
  print('</table>')
  
main(test)

