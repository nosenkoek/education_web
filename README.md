*Данные репозитория являются интеллектуальной собственностью автора 
и не подлежат копированию без согласования.*

# Веб-сервис для организации учебного процесса в ВУЗЕ
Веб-сервис решает задачу администрирования учебного процесса в ВУЗе. 
Администратор формирует направления подготовки и наполняет его дисциплинами. 
Дисциплины могут находиться в разных направлениях подготовки. 
Администратор назначает куратора на каждое из направлений.

Куратор организует группы для студентов. При поступлении студенту присваивается направление, 
в дальнейшем куратор распределяет студентов по группам. 
Максимальное количество студентов в группе - 20.

# Процесс разворачивания проекта
Для разворачивания проекта используется docker-compose. Для этого необходимо:
- указать переменные окружения в store_education/config/.env
```
DB_NAME =
DB_USER =
DB_PASSWORD =
SECRET_KEY=
```
- указать переменные окружения БД в schema_design/pg.env
```
POSTGRES_DB = 
POSTGRES_USER =
POSTGRES_PASSWORD =
PORT = 5432
```
- скачать данные репозитория и запустить docker:
```
docker-compose up -d --build
```
- при необходимости заполнить БД студентами для этого необходимо запустить скрипт 
```
common/util_fill_db/fill_students.py
```

Для удобства тестирования предварительно составлены и загружены фикстуры с данными, 
в том числе с аккаунтами пользователей (superuser, admin, curator).

# Архитектура приложения
## Основные компоненты
Интернет-магазин построен на базе фреймворка Django. Данное веб-приложение состоит 
из 6 основных компонентов (контейнеров):
- База данных (СУБД PostgreSQL),
- education_app (веб-сервис),
- redis (брокер и бэкэнд для Celery),
- celery (асинхронные задачи),
- celery-beat (планировщик задач),
- nginx (прокси-сервер для работы с media).

## База данных
База данных разворачивается в контейнере db. Основные файлы хранятся в папке schema_design.

Инициализация базы производится с помощью запуска DDL-файла (init.sql), в котором 
описана структура БД, а также необходимые связи и индексы для работы.
Кроме этого, для дополнительной информации имеется схема БД(schema_design/shema_db.jpg).

В дальнейшем взаимодействие с БД производится с помощью ORM-django. 
Запросы к БД оптимизированы с помощью методов select_related, prefetch_related.

## Приложение для организации учебного процесса
Разворачивается в контейнере education_app. Состоит из 5 приложений:
- образование (app_education),
- студенты (app_students),
- пользователи (app_users),
- отчеты (app_report),
- API (app_api).

Кроме этого, добавлено документирование с помощью swagger(drf-yasg) и docutils. 
Посмотреть документацию можно по url-адресам:
- /admin/doc
- /swagger

### App_education
Приложение, которое отвечает за хранение и обработку данных о направлениях и дисциплинах. 

Модели: 
- Direction(направления подготовки),
- Discipline(дисциплины),
- DirectionDiscipline(промежуточная таблица для связи many-to-many).

Администрирование:
- доступ к данному блоку имеет только Администратор
- поиск по названию направления/дисциплины
- фильтрация по куратору в направлениях

### App_students
Приложение, которое отвечает за хранение и обработку данных о группах студентов. 
Может просматривать и менять информацию о студентах.

Модели: 
- Class(группы),
- Student(студенты).

Администрирование:
- доступ к данному блоку имеет только Куратор,
- просмотр состава групп,
- поиск по ФИО и email студентов,
- фильтрация студентов и групп по направлению
- фильтрация студентов по группам.

Есть ограничения для добавления студента в группу:
- студент должен поступать по направлению соответствующему группе,
- максимальное количество студентов в группу - 20 
 (задается в app_students/models.py MAX_STUDENT_IN_CLASS = 20).
Данные ограничения реализованы путем невозможности выбора заполненной группы 
и группы по другим направлениям.

### App_users
Приложение, которое отвечает за данные о пользователях, 
их групповых возможностей и распределения доступа.

Для добавления возможностей доступа написана дополнительная команда 
add_permissions(app_users/management/commands/add_permissions.py)
При выполнении команды:
```
python manage.py add_permissions
```
Происходит создание двух групп пользователей (Администратор и Куратор) и 
добавление доступа к этим группам.
В дальнейшем администратор создает пользователя и добавляет его 
в необходимую группу с пометкой "Статус персонала".

Сервисы(services):
- decorator.py (декоратор для сбора объектов доступа в Фабричный метод)

### App_report
Приложение, которое отвечает за формирование отчетов по направлениям. Сформировать отчет и скачать 
его может только администратор с правами на просмотр данных о направлениях подготовки.

Представления: 
- ReportView(формирование отчета),
- StatusReportView(статус отчета по его id),
- DownloadReportView(скачать результат по его id).

URL-адреса: 
- /report/ - сформировать отчет,
- /report/status/report_id - узнать статус готовности отчета по report_id,
- /report/download/report_id - скачать отчет по report_id.

Сервисы:
- looking_for_files.py
 get_path_file(file_name: str) - производит поиск необходимого отчета 
и возвращает путь к нему.
- report_handler.py 
Создание отчета. Построен на базе паттерна Адаптер, где производится 
последовательная адаптация данных из БД к последующей записи в Excel-файл.
ReportHandler(directions: QuerySet).create_report(task_id: str) - внешний интерфейс

Формирование отчета производится в виде задач, управление очередью осуществляется Celery, 
брокером и бэкэндом является Redis. Каждая задача имеет свой id, на базе которого 
формируется название отчета и сам отчет. 
Для записи в Excel-файл используется библиотека Pandas. Запись производится пакетами, 
что позволило оптимизировать работу с большим объемом данных. 
Каждое направление записывается на отдельный лист.
Формат и вид отчета может быть изменен при необходимости.


### App_api
Приложение построенное на DRF для создания API

Представления: 
- DirectionListAPIView(список всех направлений),
- DisciplineListAPIView(список дисциплин с возможностью фильтрации 
по id или name направления),

URL-адреса: 
- /api/directions - список всех направлений,
- /api/disciplines - список всех дисциплин,
- /api/disciplines?direction_id=... - список всех дисциплин в направлении по id,
- /api/disciplines?direction_name=... - список всех дисциплин в направлении по названию,
- /api/students - список всех дисциплин в направлении по названию,
- /api/students?direction_id=... - список всех всех студентов в направлении,
- /api/students?class_id=... - список всех студентов в группе,
- /api/students?last_name=... - поиск студентов по фамилии,

Кроме того, можно совмещать возможность фильтрации, например:
- одновременный поиск студентов по фамилии и направлению:
/api/students/?last_name=..&direction_id=..
- одновременный поиск студентов по фамилии и группе:
/api/students/?last_name=..&class_id=..

Для лучшей читаемости в оболочке DRF была добавлена пагинация.

# Идеи для развития:
- добавление unit-тестов на базе django или test pytest
- ограничение действий со студентами направлений, не принадлежащих данному куратору,
- групповые действия для добавления в группу студентов
- расширение возможностей API(create, update)
