### Яндекс.Практикум 
## Проект YaMDb (групповой проект). Python-разработчик+ (бекенд)
## Проект: Работа с GitHub actions
### К проекту можно обраться по адресу:
- http://jurgensblog.sytes.net/admin
- http://jurgensblog.sytes.net/redoc
- http://jurgensblog.sytes.net/api/v1/
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (*Review*) и ставят произведению оценку в диапазоне от одного до десяти;
из пользовательских оценок формируется усреднённая оценка произведения — *рейтинг*
Настройка для приложения Continuous Integration и Continuous Deployment: 
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main/master.
***
Цель работы над проектом - получить опыт командной работы.
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

К проекту по адресу http://jurgensblog.sytes.net/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

**Задача**:
— написать бэкенд проекта (приложение reviews) и API для него (приложение api) так, чтобы они полностью соответствовали документации.
- В файле docker-compose.yaml описаны инструкции для трёх контейнеров: web, db, nginx.
- Настроены volumes для базы данных, статики и медиа (файлов, загружаемых пользователями).
- Директория .github/workflows содержит корректный workflow в файле yamdb_workflow.yaml.
- Проект развёрнут и запущен на боевом сервере.
- При пуше в ветку main код автоматически проверяется, тестируется, деплоится на сервер.
- В репозитории в файле README.md установлен бейдж о статусе работы workflow.
- В файле settings.py для переменных из env-файла указаны валидные значения по умолчанию.

### Техническое описание проекта YaMDb. ###

Проект **YaMDb** собирает отзывы (*Review*) пользователей на произведения (*Titles*).

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (*Category*) может быть расширен администратором.

Произведению может быть присвоен жанр (*Genre*) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (*Review*) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — *рейтинг* (целое число). На одно произведение пользователь может оставить только один отзыв.

Отзыв может быть прокомментирован (*Сomment*) пользователями.




* **Пользовательские роли**
	* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
	* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
	* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
	* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
	* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

* **Самостоятельная регистрация новых пользователей**
	* Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
	* Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
	* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
	* В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
	* После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

* **Создание пользователя администратором**
	* Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
	* После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.
	* Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

* **Ресурсы API YaMDb**
	* Ресурс auth: аутентификация.
	* Ресурс users: пользователи.
	* Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
	* Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
	* Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
	* Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
	* Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
	* Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

* **Связанные данные и каскадное удаление**
	* При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
	* При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
	* При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
	* При удалении объекта категории Category не нужно удалять связанные с этой категорией произведения.
	* При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.

* **База данных**
	* В репозитории с заданием, в директории /api_yamdb/static/data, подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Review и Comments.
	* Для тестирования работы проекта можно наполнить БД данным контентом из приложенных csv-файлов.
	* Процедура импорта из CSV - на усмотрение исполнителя.

* **Распределение задач в команде**
	* Вариант распределения работы между участниками:
		* Первый разработчик пишет всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail.
		* Второй разработчик пишет категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.
		* Третий разработчик занимается отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивает эндпойнты, определяет права доступа для запросов. Рейтинги произведений тоже достаются третьему разработчику.

***


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/yandex-praktikum/
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

Для *nix-систем:
```bash
source venv/bin/activate
```

Для windows-систем:
```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd api_yamdb
python3 manage.py migrate
```

Создать суперпользователя (для раздачи прав админам):

```bash
python manage.py createsuperuser
```

Запустить проект:

```bash
python manage.py runserver
```

```
Если получаем ошибку с simplejwt при запуске тестов, то устанавливаем зависимость:

pip install --upgrade djangorestframework-simplejwt
```

Сам проект и админ-панель искать по адресам:
```bash
http://127.0.0.1:8000

http://127.0.0.1:8000/admin
```
***


### Описание эндпоинтов:

- [Auth](api_yamdb/static/readme_files/README_Auth.md)
- [Categories](api_yamdb/static/readme_files/README_Categories.md)
- [Genres](api_yamdb/static/readme_files/README_Genres.md)
- [Titles](api_yamdb/static/readme_files/README_Titles.md)
- [Reviews](api_yamdb/static/readme_files/README_Reviews.md)
- [Comments](api_yamdb/static/readme_files/README_Comments.md)
- [Users](api_yamdb/static/readme_files/README_Users.md)

***

### Примечания:


* ### Authentication

    jwt-token

    Используется аутентификация с использованием JWT-токенов

    Security Scheme Type: `API Key`

    Header parameter name: `Bearer`

***

***Над проектом работали:***
* Дубровин Антон  | Github:https://github.com/anton-dubrovin | Тимлид, кастомная модель User, регистрация и аутентификация пользователей.
* Отрашкевич Михаил  | Github:https://github.com/KlemixSurfer | Разработчик, контент Администратора.
* Семёнов Юрий  | Github:https://github.com/SemenovY | Разработчик, контент пользователей.


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

### Команды для заполнения базы данными:

Теперь в контейнере web нужно выполнить миграции
```bash
docker-compose exec web python manage.py migrate
```
Чтобы создать суперпользователя и собрать статику, 
выполните по очереди эти команды:
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

***Над проектом работал:***
* Семёнов Юрий  | Github:https://github.com/SemenovY | Разработчик.

![This is an image](https://github.com/SemenovY/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
