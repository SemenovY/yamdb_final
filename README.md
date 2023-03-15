### Яндекс.Практикум 
## Проект: Работа с GitHub actions
### Описание
Настройка для приложения Continuous Integration и Continuous Deployment: 
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main/master.
***
Цель работы над проектом - получить опыт работы Ci/CD.

***

### Задание. ###

Клонируйте репозиторий yamdb_final и скопируйте в него проект api_yamdb. 
Для этого проекта у вас уже настроен docker-compose для трёх контейнеров — web, db и nginx.
Создайте workflow для репозитория yamdb_final на GitHub Actions и дайте ему название yamdb_workflow.yml.
Проверьте настройки файла docker-compose.yaml: он должен разворачивать контейнер web, используя образ, который вы создали на Docker Hub.
Опишите workflow в файле .github/workflows/yamdb_workflow.yml.
В workflow должно быть четыре задачи (job):

- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final;
- сборка и доставка докер-образа для контейнера web на Docker Hub;
- автоматический деплой проекта на боевой сервер;
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.

К проекту по адресу http://localhost/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

**Задача**:
- В файле docker-compose.yaml описаны инструкции для трёх контейнеров: web, db, nginx.
- Настроены volumes для базы данных, статики и медиа (файлов, загружаемых пользователями).
- Директория .github/workflows содержит корректный workflow в файле yamdb_workflow.yaml.
- Проект развёрнут и запущен на боевом сервере.
- При пуше в ветку main код автоматически проверяется, тестируется, деплоится на сервер.
- В репозитории в файле README.md установлен бейдж о статусе работы workflow.
- В файле settings.py для переменных из env-файла указаны валидные значения по умолчанию.

**Обязательно**: заполнение описания проекта в файле README.md.

### Шаблон наполнения env файла. ###
***Готовый шаблон прописан в файле .env.example***

***


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/yandex-praktikum/
cd yamdb_final
```
```bash:
docker-compose up
```
***

### команды для заполнения базы данными:

Теперь в контейнере web нужно выполнить миграции
```bash
docker-compose exec web python manage.py migrate
```
Cоздать суперпользователя и собрать статику. 
Выполните по очереди команды:
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

***Над проектом работал:***
* Семёнов Юрий  | Github:https://github.com/SemenovY | Разработчик.

![This is an image](https://github.com/SemenovY/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
