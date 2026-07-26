---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# База даних: початок роботи

- [Вступ](#introduction)
    - [Конфігурація](#configuration)
    - [Підключення для читання та запису](#read-and-write-connections)
    - [Пулінг підключень PostgreSQL](#pooled-postgresql-connections)
- [Виконання SQL-запитів](#running-queries)
    - [Кілька підключень до бази даних](#using-multiple-database-connections)
    - [Прослуховування подій запитів](#listening-for-query-events)
    - [Моніторинг сумарного часу запитів](#monitoring-cumulative-query-time)
- [Транзакції](#database-transactions)
- [Підключення до CLI бази даних](#connecting-to-the-database-cli)
- [Огляд баз даних](#inspecting-your-databases)
- [Моніторинг баз даних](#monitoring-your-databases)

<a name="introduction"></a>
## Вступ

Майже кожен сучасний вебзастосунок працює з базою даних. Laravel робить цю роботу дуже простою для цілої низки підтримуваних баз: через чистий SQL, [конструктор запитів](/docs/{{version}}/queries) та [Eloquent ORM](/docs/{{version}}/eloquent). Наразі Laravel має власну підтримку п'яти баз даних:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([Політика версій](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Політика версій](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([Політика версій](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([Політика версій](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

Крім того, MongoDB підтримується через пакет `mongodb/laravel-mongodb`, який офіційно супроводжує сама MongoDB. Детальніше читайте в документації [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/).

<a name="configuration"></a>
### Конфігурація

Налаштування сервісів бази даних лежать у файлі `config/database.php` вашого застосунку. У цьому файлі ви описуєте всі підключення до баз даних і вказуєте, яке з них використовується за замовчуванням. Більшість опцій у цьому файлі спираються на значення змінних оточення застосунку. Тут-таки наведено приклади для більшості підтримуваних Laravel баз даних.

За замовчуванням зразкова [конфігурація середовища](/docs/{{version}}/configuration#environment-configuration) готова до роботи з [Laravel Sail](/docs/{{version}}/sail) - це конфігурація Docker для локальної розробки Laravel-застосунків. Втім, ви можете вільно змінити налаштування бази даних під свою локальну базу.

<a name="sqlite-configuration"></a>
#### Налаштування SQLite

База даних SQLite міститься в одному файлі на вашій файловій системі. Створити нову базу SQLite можна командою `touch` у терміналі: `touch database/database.sqlite`. Після цього достатньо вказати абсолютний шлях до бази у змінній оточення `DB_DATABASE`:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

За замовчуванням для підключень SQLite увімкнено обмеження зовнішніх ключів. Щоб їх вимкнути, встановіть змінній оточення `DB_FOREIGN_KEYS` значення `false`:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> Якщо ви створюєте застосунок через [інсталятор Laravel](/docs/{{version}}/installation#creating-a-laravel-project) і обираєте SQLite, Laravel сам створить файл `database/database.sqlite` і виконає стандартні [міграції бази даних](/docs/{{version}}/migrations).

<a name="mssql-configuration"></a>
#### Налаштування Microsoft SQL Server

Щоб працювати з базою даних Microsoft SQL Server, переконайтеся, що у вас встановлено PHP-розширення `sqlsrv` і `pdo_sqlsrv`, а також усі потрібні їм залежності - зокрема драйвер Microsoft SQL ODBC.

<a name="configuration-using-urls"></a>
#### Налаштування через URL

Зазвичай підключення до бази даних описують кількома окремими значеннями: `host`, `database`, `username`, `password` тощо. Кожне з них має власну змінну оточення. Це означає, що на продакшн-сервері вам доводиться керувати одразу кількома змінними.

Деякі керовані провайдери баз даних, як-от AWS і Heroku, натомість дають єдиний «URL» бази, у якому одним рядком зібрано всю інформацію про підключення. Виглядає він приблизно так:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

Такі URL зазвичай побудовані за стандартною схемою:

```html
driver://username:password@host:port/database?options
```

Для зручності Laravel підтримує ці URL як альтернативу налаштуванню через кілька окремих опцій. Якщо задано опцію `url` (або відповідну змінну оточення `DB_URL`), Laravel візьме з неї дані підключення та облікові дані.

<a name="read-and-write-connections"></a>
### Підключення для читання та запису

Іноді вам потрібне одне підключення для запитів SELECT і зовсім інше - для INSERT, UPDATE та DELETE. Laravel робить це елементарно: потрібне підключення завжди буде обрано правильно, хоч ви пишете чистий SQL, хоч користуєтеся конструктором запитів чи Eloquent ORM.

Погляньмо на приклад, щоб зрозуміти, як налаштовуються підключення для читання та запису:

```php
'mysql' => [
    'driver' => 'mysql',
    
    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '192.168.1.3',
        ],
    ],
    'sticky' => true,
    
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        (PHP_VERSION_ID >= 80500 ? \Pdo\Mysql::ATTR_SSL_CA : \PDO::MYSQL_ATTR_SSL_CA) => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

Зверніть увагу: до масиву конфігурації додалося три ключі - `read`, `write` і `sticky`. Ключі `read` і `write` містять масиви з єдиним ключем `host`. Решту опцій для підключень `read` і `write` буде взято з основного масиву `mysql`.

Складати щось у масиви `read` і `write` потрібно лише тоді, коли ви хочете перевизначити значення з основного масиву `mysql`. Тож у цьому прикладі `192.168.1.1` буде хостом для підключення «read», а `192.168.1.3` - для «write». Облікові дані, префікс, кодування та всі інші опції з основного масиву `mysql` спільні для обох підключень. Якщо в масиві `host` кілька значень, для кожного запиту хост обирається випадково.

<a name="the-sticky-option"></a>
#### Опція `sticky`

`sticky` - це *необов'язкова* опція, яка дозволяє одразу читати записи, щойно записані в базу в межах поточного циклу запиту. Якщо `sticky` увімкнено і протягом поточного циклу запиту вже була операція «write», усі подальші операції «read» підуть через підключення «write». Так дані, записані під час запиту, можна одразу ж прочитати назад у межах цього самого запиту. Чи потрібна така поведінка вашому застосунку - вирішувати вам.

<a name="pooled-postgresql-connections"></a>
### Пулінг підключень PostgreSQL

Багато керованих провайдерів PostgreSQL пропонують пулінг підключень у режимі транзакцій - через PgBouncer або проксіювання підключень. Такі пулери чудово підходять для звичайних запитів застосунку, але частина операцій зі схемою, міграції та команди обслуговування потребують прямого підключення до бази.

Щоб використовувати транзакційний пулер із PostgreSQL, налаштуйте підключення через пул як завжди, а дані прямого підключення передайте в опції `direct`:

```php
'pgsql' => [
    'driver' => 'pgsql',
    // ...
    'pooled' => env('DB_POOLED', false),
    'direct' => array_filter([
        'host' => env('DB_DIRECT_HOST'),
        'port' => env('DB_DIRECT_PORT'),
        'username' => env('DB_DIRECT_USERNAME'),
        'password' => env('DB_DIRECT_PASSWORD'),
        'sslmode' => env('DB_DIRECT_SSLMODE'),
    ]),
],
```

Коли підключення PostgreSQL налаштоване як пульоване, Laravel автоматично вмикає для нього емуляцію підготовлених запитів. Пряме підключення успадковує всі опції, які явно не задані в конфігурації `direct`, і за замовчуванням користується нативними підготовленими запитами.

Laravel автоматично бере пряме підключення для міграцій, дампів і відновлення схеми, а також для `db:wipe`, `db:show` і `db:table`. Команда `db` теж за замовчуванням іде через пряме підключення, якщо увімкнено режим пулінгу й налаштоване пряме підключення; щоб підключитися через пул, передайте опцію `--pooled`:

```shell
php artisan db --pooled
```

Якщо вам потрібно явно скористатися прямим підключенням у застосунку, додайте до назви підключення суфікс `::direct`:

```php
DB::connection('pgsql::direct')->statement('create extension if not exists "uuid-ossp"');
```

<a name="running-queries"></a>
## Виконання SQL-запитів

Коли підключення налаштоване, ви можете виконувати запити до бази через фасад `DB`. Для кожного типу запиту він має свій метод: `select`, `update`, `insert`, `delete` і `statement`.

<a name="running-a-select-query"></a>
#### Виконання запиту SELECT

Щоб виконати базовий запит SELECT, скористайтеся методом `select` фасаду `DB`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

Перший аргумент методу `select` - це SQL-запит, а другий - прив'язки параметрів, які потрібно підставити в запит. Зазвичай це значення обмежень у `where`. Прив'язка параметрів захищає від SQL-ін'єкцій.

Метод `select` завжди повертає `array` результатів. Кожен результат у масиві - це PHP-об'єкт `stdClass`, який представляє запис із бази даних:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### Отримання скалярних значень

Іноді запит до бази повертає єдине скалярне значення. Замість того щоб діставати його з об'єкта запису, ви можете отримати значення напряму методом `scalar`:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### Отримання кількох наборів результатів

Якщо ваш застосунок викликає збережені процедури, які повертають кілька наборів результатів, скористайтеся методом `selectResultSets` - він поверне всі набори, які віддала процедура:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### Іменовані прив'язки

Замість `?` для прив'язок параметрів ви можете виконувати запит з іменованими прив'язками:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### Виконання запиту INSERT

Щоб виконати запит `insert`, скористайтеся методом `insert` фасаду `DB`. Як і `select`, цей метод приймає SQL-запит першим аргументом, а прив'язки - другим:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### Виконання запиту UPDATE

Метод `update` оновлює наявні записи в базі даних. Він повертає кількість рядків, які зачепив запит:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### Виконання запиту DELETE

Метод `delete` видаляє записи з бази даних. Як і `update`, він повертає кількість зачеплених рядків:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### Виконання довільного запиту

Деякі запити до бази не повертають жодного значення. Для таких операцій скористайтеся методом `statement` фасаду `DB`:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### Виконання непідготовленого запиту

Іноді потрібно виконати SQL-запит без прив'язки значень. Для цього у фасаду `DB` є метод `unprepared`:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> Оскільки непідготовлені запити не прив'язують параметри, вони вразливі до SQL-ін'єкцій. Ніколи не допускайте в такий запит значення, які контролює користувач.

<a name="implicit-commits-in-transactions"></a>
#### Неявні коміти

Використовуючи методи `statement` і `unprepared` фасаду `DB` всередині транзакцій, стежте за тим, щоб не виконати запит, який спричиняє [неявний коміт](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). Такі запити змушують рушій бази даних непрямо закомітити всю транзакцію, і Laravel втрачає уявлення про поточний рівень вкладеності транзакцій. Приклад такого запиту - створення таблиці:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

[Повний перелік запитів](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html), які спричиняють неявні коміти, шукайте в посібнику MySQL.

<a name="using-multiple-database-connections"></a>
### Кілька підключень до бази даних

Якщо у вашому файлі `config/database.php` описано кілька підключень, звертатися до кожного з них можна методом `connection` фасаду `DB`. Назва підключення, яку ви передаєте в `connection`, має відповідати одному з підключень, перелічених у `config/database.php` або налаштованих під час виконання через хелпер `config`:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

Отримати «сирий» PDO-екземпляр, що стоїть за підключенням, можна методом `getPdo`:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### Прослуховування подій запитів

Якщо ви хочете задати замикання, яке викликатиметься для кожного SQL-запиту вашого застосунку, скористайтеся методом `listen` фасаду `DB`. Це зручно для логування запитів чи налагодження. Зареєструвати замикання-слухач можна в методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
### Моніторинг сумарного часу запитів

Типове вузьке місце сучасних вебзастосунків - час, який вони витрачають на запити до бази даних. На щастя, Laravel може викликати ваше замикання чи колбек, коли застосунок забагато часу проводить у запитах до бази в межах одного HTTP-запиту. Для цього передайте методу `whenQueryingForLongerThan` поріг часу (у мілісекундах) і замикання. Викликати цей метод можна в методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // Notify development team...
        });
    }
}
```

<a name="database-transactions"></a>
## Транзакції

Щоб виконати набір операцій у межах транзакції, скористайтеся методом `transaction` фасаду `DB`. Якщо всередині замикання транзакції буде викинуто виняток, транзакція автоматично відкотиться, а виняток буде викинуто далі. Якщо замикання відпрацює успішно, транзакцію буде автоматично закомічено. З методом `transaction` вам не доведеться вручну дбати про відкат чи коміт:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### Обробка взаємних блокувань

Метод `transaction` приймає необов'язковий другий аргумент - кількість повторних спроб виконати транзакцію в разі взаємного блокування (deadlock). Коли спроби вичерпано, буде викинуто виняток:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a name="manually-using-transactions"></a>
#### Ручне керування транзакціями

Якщо ви хочете розпочати транзакцію вручну й повністю контролювати відкати та коміти, скористайтеся методом `beginTransaction` фасаду `DB`:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

Відкотити транзакцію можна методом `rollBack`:

```php
DB::rollBack();
```

Нарешті, закомітити транзакцію можна методом `commit`:

```php
DB::commit();
```

> [!NOTE]
> Методи транзакцій фасаду `DB` керують транзакціями і для [конструктора запитів](/docs/{{version}}/queries), і для [Eloquent ORM](/docs/{{version}}/eloquent).

<a name="connecting-to-the-database-cli"></a>
## Підключення до CLI бази даних

Щоб підключитися до CLI вашої бази даних, скористайтеся artisan-командою `db`:

```shell
php artisan db
```

За потреби ви можете вказати назву підключення, щоб підключитися не до того, яке використовується за замовчуванням:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## Огляд баз даних

Artisan-команди `db:show` і `db:table` дають цінну інформацію про вашу базу даних та її таблиці. Щоб побачити загальний огляд бази - її розмір, тип, кількість відкритих підключень і зведення по таблицях - скористайтеся командою `db:show`:

```shell
php artisan db:show
```

Вказати, яке саме підключення оглядати, можна опцією `--database` з назвою підключення:

```shell
php artisan db:show --database=pgsql
```

Щоб додати до виводу кількість рядків у таблицях і подробиці про представлення бази даних, передайте опції `--counts` і `--views` відповідно. На великих базах збір кількості рядків і даних про представлення може бути повільним:

```shell
php artisan db:show --counts --views
```

Крім того, для огляду бази даних вам стануть у пригоді такі методи `Schema`:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

Якщо ви хочете оглянути підключення, яке не є підключенням за замовчуванням, скористайтеся методом `connection`:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### Огляд таблиці

Щоб отримати огляд окремої таблиці бази даних, виконайте artisan-команду `db:table`. Вона показує загальну інформацію про таблицю: її стовпці, типи, атрибути, ключі та індекси:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## Моніторинг баз даних

За допомогою artisan-команди `db:monitor` ви можете наказати Laravel надсилати подію `Illuminate\Database\Events\DatabaseBusy`, якщо ваша база даних обслуговує більше за вказану кількість відкритих підключень.

Для початку заплануйте команду `db:monitor` на [щохвилинне виконання](/docs/{{version}}/scheduling). Команда приймає назви конфігурацій підключень, які ви хочете моніторити, і максимальну кількість відкритих підключень, яку варто терпіти, перш ніж надсилати подію:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

Самого лише планування цієї команди замало, щоб отримати сповіщення про кількість відкритих підключень. Коли команда натрапляє на базу даних, у якої кількість відкритих підключень перевищує ваш поріг, надсилається подія `DatabaseBusy`. Щоб надіслати сповіщення собі чи команді розробників, прослухайте цю подію в `AppServiceProvider` вашого застосунку:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```
