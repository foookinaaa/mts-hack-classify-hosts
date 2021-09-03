# Классификация хостов на пользовательские и технические
### (МТС.Тета Хакатон)

## Задача:   
Построить модель машинного обучения, которая будет разделять хосты на технические (различные API: Яндекс метрика, реклама и т.д) и нетехнические (возвращают html странички).   
Для решения задачи предоставляется подвыборка хостов без разметки. Необходимо собрать разметку самим.  

demo: https://clf-hosts-21.herokuapp.com/  
![this](https://user-images.githubusercontent.com/74900958/132009912-1fc1783e-acca-4299-9d78-1a66288aba40.gif)

## Решение:   
### Сбор разметки  
1) Анализ сырых данных, удаление дублей в ноутбуке [first_analysis.ipynb](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/notebooks/first_analysis.ipynb)  
2) Первый проход по каждому сайту и классификация их на пользовательские (если на страницу получилось зайти) и технические (если на страницу зайти невозможно) в скрипте [auto_host_parser.py](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/apps/netoloka/auto_host_parser.py)  
3) Второй проход по каждому сайту (поиск файла robots.txt, предназначенного для поисковой выдачи сайта: если у хоста есть файл robots.txt и он корректен, то этот хост пользовательский) в скрипте [auto_robotstxt_parser.py](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/apps/netoloka/auto_robotstxt_parser.py) 
4) Дополнительная разметка на основе экспертных решающих правил, описанных в ноутбуке [clf_hosts.ipynb](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/notebooks/clf_hosts.ipynb)  
### Далее все решение выполнено в ноутбуке [clf_hosts.ipynb](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/notebooks/clf_hosts.ipynb)
### Генерация фичей 
{'url_len': 'Длина хоста',  
'max_domain_level': 'Количество поддоменов',  
'max_domain_part_len': 'Максимальная длина поддомена',  
'ngram_max': 'Максимальный вес n-граммы',  
'ngram_min': 'Минимальный вес n-граммы',  
'digits_count': 'Число цифр в хосте',  
'users_start' : 'Начало с "www." или с "m."'}  
### Модель 
CatBoostClassifier(random_state=0, verbose=0, max_depth=3, n_estimators=5)  
### Валидация
Проведение ручной разметки 200 хостов, в которых есть полная уверенность пользовательские они или технические.   
Разметка осуществлялась при помощи скрипта [manual.py](https://github.com/foookinaaa/mts-hack-classify-hosts/blob/main/apps/netoloka/manual.py), который самостоятельно открывает хост, а пользователь вручную проставляет ему метку класса.  
Итоговые файлы после валидации: [validation_manual](https://github.com/foookinaaa/mts-hack-classify-hosts/tree/main/notebooks/validation_manual)  
Прогон модели на данной разметке.   
### Метрики качества на валидационном датасете
precision=0.73  
recall=0.59  
Так, как приоритетнее в данной задаче находить пользовательские хосты, чтобы далее работать с ними в бизнес-целях, то данная модель с точностью 73% может находить такие хосты, что является хорошим качеством предсказания.


