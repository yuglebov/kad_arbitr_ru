# Kad.py v0.1

Script for the web scraping site kad.arbitr.ru

## Run

python kad.ry [parameters]

Parameters(all optional):
- -participant - Участник дела
- -judge - Судья
- -court - Суд
- -num - Номер дела
- -datefrom - Дата регистрации дела с какого числа искать, в формате dd.mm.yyyy
- -dateto - Дата регистрации дела по какое число искать, в формате dd.mm.yyyy (для корректного поиска должны быть обязательно две даты)
- -file - файл для экспорта, по умолчанию data.json

## ToDo

- Search for several same options
- Filter for type of cases
- Scraping cards
