# Асинхронный чат клиент

Чтение и запись чата в файл, а так же отправка сообщений

Чтение чата осуществляется  с помощью reader.py, отпарвка сообещний через client.py, так же есть отдельный скрипт для регистарции registration.py

## Как установить

Для работы микросервиса нужен Python версии не ниже 3.6.

```bash
pip install -r requirements.txt
```

## Как запустить

### Чтение
```bash
python reader.py
```

Клиент подключится на 5000 порт к хосту minechat.dvmn.org, так же в директории со скриптом появится лог файл - chat.log


### Отправка сообщений
```bash
python client.py -m "моё сообщение"
```

### Регистрация
```
python registration.py 
Enter your nick: test
```
Токен будет записан в файл token в директории со скриптом.

## Доступные настройки

## Чтение

#### Доступные настройки через командную строку:
```
-H,--host - адрес хоста чата 
-p,--port - порт хоста чата
--history - путь для записи истории
```
#### Доступные настройки через переменные окружения

Пример:
```
HOST=minechat.dvmn.org
PORT=5000
LOG=/var/chat/log.txt
```

## Отправка сообщений

#### Доступные настройки через командную строку:

```
-H,--host - адрес хоста чата 
-p,--port - порт хоста чата
-m,--message - сообщение для отправки в чат
-t,--token - токен пользователя
-n,--nickname - имя для регистрации нового пользователя
```

Если не указан токен или имя для регистарции, будет попытка отрыть файл в директории со скриптом, пример файла:
```
{"nickname": "Confident USer", "account_hash": "aea28cac-b19a-11eb-8c47-0242ac110002"}
```
#### Доступные настройки через переменные окружения

Пример:
```
HOST=minechat.dvmn.org
PORT=5000
```

## Регистрация
```
-H,--host - адрес хоста чата 
-p,--port - порт хоста чата
```
#### Доступные настройки через переменные окружения

Пример:
```
HOST=minechat.dvmn.org
PORT=5000
LOG=/var/chat/log.txt
```

# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).