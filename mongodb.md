---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# MongoDB

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Драйвер MongoDB](#mongodb-driver)
    - [Запуск сервера MongoDB](#starting-a-mongodb-server)
    - [Встановлення пакета Laravel MongoDB](#install-the-laravel-mongodb-package)
- [Конфігурація](#configuration)
- [Можливості](#features)

<a name="introduction"></a>
## Вступ

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) - одна з найпопулярніших документоорієнтованих NoSQL-баз даних, яку обирають за високе навантаження на запис (корисно для аналітики чи IoT) і високу доступність (легко налаштувати набори реплік з автоматичним перемиканням при збої). Вона також легко шардить базу для горизонтального масштабування й має потужну мову запитів для агрегації, текстового пошуку чи геопросторових запитів.

Замість того щоб зберігати дані в таблицях із рядків і стовпців, як SQL-бази, кожен запис у базі MongoDB - це документ, описаний у BSON, двійковому представленні даних. Далі застосунки можуть отримувати цю інформацію у форматі JSON. Підтримується широкий набір типів даних, зокрема документи, масиви, вкладені документи та двійкові дані.

Перш ніж користуватися MongoDB разом із Laravel, ми рекомендуємо встановити пакет `mongodb/laravel-mongodb` через Composer. Пакет `laravel-mongodb` офіційно підтримує MongoDB, і хоча PHP підтримує MongoDB нативно через драйвер MongoDB, пакет [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) дає багатшу інтеграцію з Eloquent та іншими можливостями Laravel:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## Встановлення

<a name="mongodb-driver"></a>
### Драйвер MongoDB

Щоб підключитися до бази даних MongoDB, потрібне розширення PHP `mongodb`. Якщо ви розробляєте локально через [Laravel Herd](https://herd.laravel.com) або встановили PHP через `php.new`, це розширення вже є у вашій системі. Проте якщо вам треба встановити його вручну, зробіть це через PECL:

```shell
pecl install mongodb
```

Докладніше про встановлення розширення MongoDB для PHP читайте в [інструкції зі встановлення розширення MongoDB PHP](https://www.php.net/manual/en/mongodb.installation.php).

<a name="starting-a-mongodb-server"></a>
### Запуск сервера MongoDB

MongoDB Community Server дозволяє запустити MongoDB локально й доступний для встановлення на Windows, macOS, Linux або як контейнер Docker. Щоб дізнатися, як встановити MongoDB, зверніться до [офіційного посібника зі встановлення MongoDB Community](https://docs.mongodb.com/manual/administration/install-community/).

Рядок підключення до сервера MongoDB можна задати у вашому файлі `.env`:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

Щоб розмістити MongoDB у хмарі, розгляньте [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
Щоб звертатися до кластера MongoDB Atlas локально зі свого застосунку, вам треба [додати власну IP-адресу в мережевих налаштуваннях кластера](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) до списку дозволених IP проєкту.

Рядок підключення до MongoDB Atlas також можна задати у вашому файлі `.env`:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Встановлення пакета Laravel MongoDB

Нарешті, встановіть пакет Laravel MongoDB через Composer:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> Встановлення цього пакета зазнає невдачі, якщо розширення PHP `mongodb` не встановлено. Конфігурація PHP може відрізнятися для CLI та вебсервера, тож переконайтеся, що розширення увімкнено в обох.

<a name="configuration"></a>
## Конфігурація

Налаштувати підключення до MongoDB можна через конфігураційний файл `config/database.php` вашого застосунку. Додайте до нього підключення `mongodb`, що використовує драйвер `mongodb`:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],
```

<a name="features"></a>
## Можливості

Коли конфігурацію завершено, ви можете користуватися пакетом `mongodb` і цим підключенням до бази у своєму застосунку, щоб скористатися низкою потужних можливостей:

- [Через Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/) моделі можуть зберігатися в колекціях MongoDB. Окрім стандартних можливостей Eloquent, пакет Laravel MongoDB надає додаткові - як-от вкладені зв'язки. Пакет також дає прямий доступ до драйвера MongoDB, яким можна виконувати сирі запити та конвеєри агрегації.
- [Пишіть складні запити](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) через конструктор запитів.
- [Пошук за схожістю / векторний пошук](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) через векторні ембединги та метод Eloquent `vectorSearch`.
- [Драйвер кешу](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) `mongodb` оптимізовано під можливості MongoDB - як-от TTL-індекси, що автоматично прибирають прострочені записи кешу.
- [Відправляйте й обробляйте завдання в черзі](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) через драйвер черги `mongodb`.
- [Зберігання файлів у GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/) через [адаптер GridFS для Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/).
- [Повнотекстовий пошук](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/) через рушій Scout `mongodb`.
- Більшість сторонніх пакетів, що працюють із підключенням до бази чи Eloquent, можна використовувати з MongoDB.

Щоб дізнатися більше про використання MongoDB разом із Laravel, зверніться до [посібника Quick Start](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) від MongoDB.
