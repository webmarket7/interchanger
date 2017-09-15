import re

text = 'Миші і ондатри. ВІДКРИВАННЯ і активація. Створили та інсталювали. Я тебе люблю і обожнюю. Вийшов та пішов. Зараз й негайно. Стовп та вогонь. Я спав і не бачив. Ковбаса і сир. Я слухаю музику і іду. Собаки і коти. Риба та м’ясо'

previous = ['[^аоуиіиеяюєї]', '[аоуиіиеяюєї]']
next = ['[аоуиіиеяюєї]', '[^аоуиіиеяюєї]']
conjunctions = ['і', 'й', 'та']

# Функція приймає вихідний текст і повертає виправлений відповідно до регулярного виразу
def interchange(text, start, end, correctConjunction):
  for conjunction in conjunctions:
    searchStr = r'{}\b\s{}\s\b{}'.format(start, conjunction, end)                   # Складаємо та компілюємо регулярний вираз
    subStr = r'\s{}\s'.format(conjunction)                                          # для пошуку сполучників між пробілами та голосними/приголосними
    substrings = re.compile(searchStr, re.IGNORECASE).findall(text)                 # Шукаємо збіги з шаблоном у тексті, ігноруючи регістр
    for substring in substrings:                                                    # Заміняємо в циклі неправильні сполучники в кожному випадку на правильні
      result = re.compile(subStr).sub(' ' + correctConjunction + ' ', substring)
      text = text.replace(substring, result)
  corrected = text
  return corrected                                                                  # Повертаємо виправлений текст

# Функція для синхронізації третього списка (conjunctions)
def iter(n):
  if n < 2:
    return 0
  else:
    return n - 1

# Основна функція для чергування і, й, та
def main(text):
  n = 0
  for i in range(2):
    for j in range(2):
      text = interchange(text, previous[i], next[j], conjunctions[iter(n)])
      n += 1
  print(text)

main(text)