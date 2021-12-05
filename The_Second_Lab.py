# Доброго времени суток.
# Программу осознанно старался делать без исключений и их обработки, чтобы не нарушать логику работы.
# Все пустые и бесполезные (на мой взгляд) поля были заменены на "Null" (Не Null, так как он не пишется в CSV) или отредактированы
# Программа работает, результат в файле result.csv
# Время выполнения: около 30 минут (Да, это несомненно долго. В проектах часто парсил динамику через запросы с помощью Requests, что выходит в сотни раз быстрее)

from selenium import webdriver
import time
from csv import DictWriter

link = 'http://wikimipt.org/wiki/'

chromedriver = r"C:\Users\Serge\Desktop\chromedriver.exe"
options = webdriver.ChromeOptions()

# Оптимизация
options.add_argument('headless')
options.add_argument("--log-level=3")
options.add_argument("--window-size=400,800")

# Инициализация класса
browser = webdriver.Chrome(executable_path=chromedriver, options=options)
browser.get(link)

# Получение количества кафедр
count_i = len(browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div[3]/ul/li'))

# Инициализация файла, запись заголовков
with open("result.csv", 'w', newline='') as csv_file:
    fieldnames = ['Cafedra', 'Teacher','Birth_day','Degree', 'Knowledge', 'Teaching_skill', 'Commication_skill', 'Easy_exam', 'Overall_score']

    writer = DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

# Цикл для прохода по кафедрам
for i in range(count_i):

    # Исключение кафедры из-за отсутсвия записей в ней
    if i == 12: continue

    tmp = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li[{i + 1}]/a')
    teach_place = tmp.text
    tmp.click()

    # Получение количества преподавателей кафедры (условия из-за кривости сайта, так как на разных кафедрах разная вёрстка )
    if browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div[4]/div[5]/ul/li'):
        count_j = len(browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div[4]/div[5]/ul/li'))
    elif browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div[4]/div[3]/ul/li'):
        count_j = len(browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div[4]/div[3]/ul/li'))
    else:
        print("Не смог найти количество элементов")

    # Цикл для прохода по преподавателям (условия из-за кривости сайта, так как на разных кафедрах разная вёрстка)
    for j in range(count_j):
        if browser.find_elements_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li[1]/div/div[2]/p/a'):
            tmp = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li[{j + 1}]/div/div[2]/p/a')

        elif browser.find_elements_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[5]/ul/li[1]/div/div[2]/p/a'):
            tmp = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[5]/ul/li[{j + 1}]/div/div[2]/p/a')

        elif browser.find_elements_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li/div/div[2]/p/a'): 
            tmp = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li/div/div[2]/p/a')

        else:
            tmp = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/div[3]/ul/li[{j + 1}]/a')

        tmp.click()

        # Получение длины таблицы для прохода по ней в цикле (Пришлось так делать из-за того, что данные часто разнятся)
        tmp = len(browser.find_elements_by_xpath(f'//*[@id="mw-content-text"]/table/tbody/tr'))

        prepod = browser.find_element_by_xpath(f'//*[@id="firstHeading"]')

        # Инициализация переменных
        birth_day = 'None'
        degree = 'None'
        knowledge = 'None'
        teaching_skill = 'None'
        commication_skill = 'None'
        easy_exam = 'None'
        overall_score = 'None'

        # Цикл для прохода по таблице, парсинга и редактирования нужных данных (Через Pandas не вышло - пришлось искать другой метод с помощью xpath, например)
        # Большое количество проверок и условий сделано по причине разной верстки разделов сайта.
        # Выход из цикла сразу после нахождения требуемых данных, чтобы не тратить время и ресурсы попусту
        for k in range(2, tmp):
            if browser.find_elements_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/th'):
                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/th').text == "Дата рождения":
                    birth_day = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td').text
                
                elif browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/th').text == "Учёная степень":
                    degree = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td').text

            if browser.find_elements_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody'):
                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[1]/td[1]').text == "Знания":
                    knowledge = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[1]/td[2]/div/span[2]').text
                    if knowledge == "( нет голосов )": knowledge = 'None'
                    elif knowledge.endswith(")"): knowledge = knowledge.split()[0]

                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[2]/td[1]').text == "Умение преподавать":
                    teaching_skill = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[2]/td[2]/div/span[2]').text
                    if teaching_skill == "( нет голосов )": teaching_skill = 'None'
                    elif teaching_skill.endswith(")"): teaching_skill = teaching_skill.split()[0]

                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[3]/td[1]').text == "В общении":
                    commication_skill = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[3]/td[2]/div/span[2]').text
                    if commication_skill == "( нет голосов )": commication_skill = 'None'
                    elif commication_skill.endswith(")"): commication_skill = commication_skill.split()[0]

                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[4]/td[1]').text == "«Халявность»":
                    easy_exam = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[4]/td[2]/div/span[2]').text
                    if easy_exam == "( нет голосов )": easy_exam = 'None'
                    elif easy_exam.endswith(")"): easy_exam = easy_exam.split()[0]

                if browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[5]/td[1]').text == "Общая оценка":
                    overall_score = browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div[4]/table/tbody/tr[{k}]/td/table/tbody/tr[5]/td[2]/div/span[2]').text
                    if overall_score == "( нет голосов )": overall_score = 'None'
                    elif overall_score.endswith(")"): overall_score = overall_score.split()[0]
                    break

        # Запись данных в файл
        with open("result.csv", 'a', newline='') as csv_file:
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerows([{'Cafedra': teach_place, 'Teacher': prepod.text,'Birth_day': birth_day,'Degree': degree, 'Knowledge': knowledge, 'Teaching_skill': teaching_skill, 'Commication_skill': commication_skill, 'Easy_exam': easy_exam, 'Overall_score': overall_score}])

        print(f'Номер кафедры: {i + 1}, номер преподавателя: {j + 1}')

        browser.back()
    browser.back()

browser.close()
