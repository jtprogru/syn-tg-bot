# Домашнее задание №3
Постановка задачи:
Создать бота, который из сообщения пользователя будет создавать опрос. Первая строка сообщения пользователя - вопрос, 2 - 11 строки - варианты ответов. Если сообщение пользователя менее 3 строк или более 11, то выводить соответствующее сообщение.
Примечания:
> Для упрощения можете считать не количество строк, а количество переводов строк (их на 1 меньше):
>
> `message.text.count("\n")`

> Для разделения текста пользователя на список строк можете использовать:
>
> `lst = message.text.split('\n')`

Внимательно: на проверку необходимо отправить:
- файл с кодом для бота БЕЗ токена,
- скриншот, где видно работу бота

Критерии оценки:

- 1 балл - Создан файл и импортирована библиотека telebot
- 2 балла - Бот создает опрос, но делит на варианты ответа неверно.
- 3 балла - Бот создает опрос, но нет проверки количество строк в сообщении пользователя.
- 4 балла - Бот создает опрос. Есть проверка на корректность ввода. Но есть проблемы с оформлением кода.
- 5 баллов - Бот создает опрос. Есть проверка на корректность ввода.  Минимум 50% кода покрыто комментариями, код соответствует PEP8.
