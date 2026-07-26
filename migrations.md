---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# База даних: міграції

- [Вступ](#introduction)
- [Створення міграцій](#generating-migrations)
    - [Стискання міграцій](#squashing-migrations)
- [Структура міграції](#migration-structure)
- [Запуск міграцій](#running-migrations)
    - [Відкат міграцій](#rolling-back-migrations)
- [Таблиці](#tables)
    - [Створення таблиць](#creating-tables)
    - [Оновлення таблиць](#updating-tables)
    - [Перейменування та видалення таблиць](#renaming-and-dropping-tables)
- [Стовпці](#columns)
    - [Створення стовпців](#creating-columns)
    - [Доступні типи стовпців](#available-column-types)
    - [Модифікатори стовпців](#column-modifiers)
    - [Зміна стовпців](#modifying-columns)
    - [Перейменування стовпців](#renaming-columns)
    - [Видалення стовпців](#dropping-columns)
- [Індекси](#indexes)
    - [Створення індексів](#creating-indexes)
    - [Перейменування індексів](#renaming-indexes)
    - [Видалення індексів](#dropping-indexes)
    - [Обмеження зовнішніх ключів](#foreign-key-constraints)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Міграції - це наче контроль версій для вашої бази даних: вони дозволяють команді описувати та спільно використовувати схему бази даних застосунку. Якщо вам колись доводилося просити колегу вручну додати стовпець до своєї локальної схеми після того, як він підтягнув ваші зміни з репозиторію, - ви стикалися саме з тією проблемою, яку розв'язують міграції.

[Фасад](/docs/{{version}}/facades) `Schema` в Laravel дає незалежну від бази даних підтримку створення таблиць і роботи з ними в усіх підтримуваних Laravel системах баз даних. Зазвичай міграції користуються цим фасадом, щоб створювати й змінювати таблиці та стовпці.

<a name="generating-migrations"></a>
## Створення міграцій

Щоб згенерувати міграцію, скористайтеся [artisan-командою](/docs/{{version}}/artisan) `make:migration`. Нова міграція потрапить до каталогу `database/migrations`. Назва кожного файлу міграції містить часову позначку, за якою Laravel визначає порядок міграцій:

```shell
php artisan make:migration create_flights_table
```

Laravel спробує вгадати за назвою міграції, як називається таблиця і чи створює міграція нову таблицю. Якщо Laravel зможе визначити назву таблиці з назви міграції, він заздалегідь підставить цю таблицю у згенерований файл. Інакше ви просто вкажете таблицю у файлі міграції вручну.

Якщо ви хочете задати власний шлях для згенерованої міграції, скористайтеся опцією `--path` під час виконання команди `make:migration`. Вказаний шлях має бути відносним до базового шляху вашого застосунку.

> [!NOTE]
> Заготовки міграцій можна налаштувати через [публікацію заготовок](/docs/{{version}}/artisan#stub-customization).

<a name="squashing-migrations"></a>
### Стискання міграцій

Розробляючи застосунок, ви з часом накопичуєте все більше міграцій. Через це каталог `database/migrations` може розростися до сотень файлів. За бажанням ви можете «стиснути» міграції в один SQL-файл. Для початку виконайте команду `schema:dump`:

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

Коли ви виконуєте цю команду, Laravel запише файл «схеми» до каталогу `database/schema` вашого застосунку. Назва файлу схеми відповідатиме підключенню до бази даних. Тепер, коли ви спробуєте виконати міграції й жодної іншої міграції ще не виконано, Laravel спершу виконає SQL-запити з файлу схеми того підключення, яке ви використовуєте. А потім виконає всі решту міграцій, які не входили до дампу схеми.

Якщо тести вашого застосунку працюють з іншим підключенням до бази даних, ніж те, яким ви зазвичай користуєтеся локально, переконайтеся, що ви зробили дамп схеми і для цього підключення, - інакше тести не зможуть побудувати вашу базу. Це варто зробити після дампу того підключення, яким ви зазвичай користуєтеся під час локальної розробки:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

Файл схеми бази даних варто закомітити в репозиторій, щоб нові розробники у вашій команді могли швидко створити початкову структуру бази даних застосунку.

> [!WARNING]
> Стискання міграцій доступне лише для баз даних MariaDB, MySQL, PostgreSQL і SQLite і використовує консольний клієнт бази даних.

<a name="migration-structure"></a>
## Структура міграції

Клас міграції містить два методи: `up` і `down`. Метод `up` додає до бази даних нові таблиці, стовпці чи індекси, а метод `down` має скасовувати те, що зробив метод `up`.

В обох методах ви можете користуватися конструктором схеми Laravel, щоб виразно створювати та змінювати таблиці. Про всі методи конструктора `Schema` читайте в [його документації](#creating-tables). Наприклад, ця міграція створює таблицю `flights`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('airline');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
#### Задання підключення для міграції

Якщо ваша міграція працюватиме не з підключенням до бази даних за замовчуванням, задайте властивість `$connection` вашої міграції:

```php
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 */
public function up(): void
{
    // ...
}
```

<a name="skipping-migrations"></a>
#### Пропуск міграцій

Іноді міграція призначена для можливості, яка ще не активна, і ви поки не хочете її виконувати. У такому разі опишіть у міграції метод `shouldRun`. Якщо `shouldRun` повертає `false`, міграцію буде пропущено:

```php
use App\Models\Flight;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flight::class);
}
```

<a name="running-migrations"></a>
## Запуск міграцій

Щоб виконати всі міграції, які ще не виконано, запустіть artisan-команду `migrate`:

```shell
php artisan migrate
```

Якщо ви хочете побачити, які міграції вже виконано, а які ще очікують, скористайтеся artisan-командою `migrate:status`:

```shell
php artisan migrate:status
```

Якщо передати команді `migrate` опцію `--step`, кожна міграція виконається як окремий пакет, і згодом ви зможете відкотити окремі міграції командою `migrate:rollback`:

```shell
php artisan migrate --step
```

Якщо ви хочете побачити SQL-запити, які виконають міграції, не запускаючи їх насправді, передайте команді `migrate` прапорець `--pretend`:

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### Ізоляція виконання міграцій

Якщо ви розгортаєте застосунок на кількох серверах і виконуєте міграції в межах процесу розгортання, вам навряд чи потрібно, щоб два сервери одночасно намагалися міграцію виконати. Щоб цього не сталося, скористайтеся опцією `isolated` під час виклику команди `migrate`.

Коли передано опцію `isolated`, Laravel перед спробою виконати міграції отримає атомарне блокування через драйвер кешу вашого застосунку. Усі інші спроби запустити команду `migrate`, поки блокування тримається, не виконаються; проте команда все одно завершиться з кодом успішного виходу:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> Щоб скористатися цією можливістю, ваш застосунок має використовувати драйвер кешу `memcached`, `redis`, `dynamodb`, `database`, `file` або `array` як драйвер за замовчуванням. Крім того, усі сервери повинні спілкуватися з одним центральним сервером кешу.

<a name="forcing-migrations-to-run-in-production"></a>
#### Примусовий запуск міграцій на продакшні

Деякі операції міграцій руйнівні, тобто через них ви можете втратити дані. Щоб убезпечити вас від запуску таких команд на продакшн-базі, Laravel запитає підтвердження, перш ніж їх виконати. Щоб виконати команди без запитання, скористайтеся прапорцем `--force`:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### Відкат міграцій

Щоб відкотити останню операцію міграції, скористайтеся artisan-командою `rollback`. Вона відкочує останній «пакет» міграцій, який може містити кілька файлів:

```shell
php artisan migrate:rollback
```

Ви можете відкотити обмежену кількість міграцій, передавши команді `rollback` опцію `step`. Наприклад, ця команда відкотить останні п'ять міграцій:

```shell
php artisan migrate:rollback --step=5
```

Ви можете відкотити конкретний «пакет» міграцій, передавши команді `rollback` опцію `batch`, значення якої відповідає значенню batch у таблиці `migrations` вашої бази даних. Наприклад, ця команда відкотить усі міграції з пакета номер три:

```shell
php artisan migrate:rollback --batch=3
```

Якщо ви хочете побачити SQL-запити, які виконають міграції, не запускаючи їх насправді, передайте команді `migrate:rollback` прапорець `--pretend`:

```shell
php artisan migrate:rollback --pretend
```

Команда `migrate:reset` відкотить усі міграції вашого застосунку:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### Відкат і міграція однією командою

Команда `migrate:refresh` відкотить усі ваші міграції, а потім виконає команду `migrate`. Фактично вона перестворює всю вашу базу даних:

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

Ви можете відкотити й повторно виконати обмежену кількість міграцій, передавши команді `refresh` опцію `step`. Наприклад, ця команда відкотить і виконає заново останні п'ять міграцій:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### Видалення всіх таблиць і міграція

Команда `migrate:fresh` видалить із бази даних усі таблиці, а потім виконає команду `migrate`:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

За замовчуванням команда `migrate:fresh` видаляє таблиці лише з підключення за замовчуванням. Втім, опцією `--database` ви можете вказати, яке підключення слід міграціювати. Назва підключення має відповідати підключенню, описаному у [файлі конфігурації](/docs/{{version}}/configuration) `database` вашого застосунку:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> Команда `migrate:fresh` видалить усі таблиці бази даних незалежно від їхнього префікса. Користуйтеся нею обережно, якщо розробляєте на базі даних, спільній з іншими застосунками.

<a name="tables"></a>
## Таблиці

<a name="creating-tables"></a>
### Створення таблиць

Щоб створити нову таблицю, скористайтеся методом `create` фасаду `Schema`. Метод `create` приймає два аргументи: перший - назва таблиці, другий - замикання, яке отримує об'єкт `Blueprint` для опису нової таблиці:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

Створюючи таблицю, ви можете описувати її стовпці будь-якими [методами стовпців](#creating-columns) конструктора схеми.

<a name="determining-table-column-existence"></a>
#### Перевірка існування таблиці чи стовпця

Перевірити, чи існує таблиця, стовпець або індекс, можна методами `hasTable`, `hasColumn` і `hasIndex`:

```php
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // The "users" table exists and has a unique index on the "email" column...
}
```

<a name="database-connection-table-options"></a>
#### Підключення до бази даних та опції таблиці

Якщо ви хочете виконати операцію зі схемою не на підключенні за замовчуванням, скористайтеся методом `connection`:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

Крім того, кілька інших властивостей і методів дозволяють задати інші аспекти створення таблиці. Властивістю `engine` можна вказати рушій сховища таблиці на MariaDB чи MySQL:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

Властивостями `charset` і `collation` можна задати кодування та порядок сортування для створюваної таблиці на MariaDB чи MySQL:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

Методом `temporary` можна вказати, що таблиця має бути «тимчасовою». Тимчасові таблиці видимі лише в межах сесії поточного підключення й автоматично видаляються, коли підключення закривається:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

Якщо ви хочете додати до таблиці «коментар», викличте метод `comment` на екземплярі таблиці. Коментарі до таблиць наразі підтримують лише MariaDB, MySQL і PostgreSQL:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### Оновлення таблиць

Методом `table` фасаду `Schema` можна оновлювати наявні таблиці. Як і `create`, метод `table` приймає два аргументи: назву таблиці та замикання, яке отримує екземпляр `Blueprint` для додавання стовпців чи індексів:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### Перейменування та видалення таблиць

Щоб перейменувати наявну таблицю, скористайтеся методом `rename`:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

Щоб видалити наявну таблицю, скористайтеся методами `drop` або `dropIfExists`:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### Перейменування таблиць із зовнішніми ключами

Перш ніж перейменовувати таблицю, переконайтеся, що всі обмеження зовнішніх ключів на ній мають у ваших файлах міграцій явну назву, а не ту, яку Laravel призначає за конвенцією. Інакше назва обмеження зовнішнього ключа посилатиметься на стару назву таблиці.

<a name="columns"></a>
## Стовпці

<a name="creating-columns"></a>
### Створення стовпців

Методом `table` фасаду `Schema` можна оновлювати наявні таблиці. Як і `create`, метод `table` приймає два аргументи: назву таблиці та замикання, яке отримує екземпляр `Illuminate\Database\Schema\Blueprint` для додавання стовпців:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### Доступні типи стовпців

Blueprint конструктора схеми має цілу низку методів, що відповідають різним типам стовпців, які ви можете додати до таблиць. Усі доступні методи перелічено в таблиці нижче:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="booleans-method-list"></a>
#### Логічні типи

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### Рядкові та текстові типи

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
#### Числові типи

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[decimal](#column-method-decimal)
[double](#column-method-double)
[float](#column-method-float)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)

</div>

<a name="dates-and-times-method-list"></a>
#### Типи дати й часу

<div class="collection-method-list" markdown="1">

[dateTime](#column-method-dateTime)
[dateTimeTz](#column-method-dateTimeTz)
[date](#column-method-date)
[time](#column-method-time)
[timeTz](#column-method-timeTz)
[timestamp](#column-method-timestamp)
[timestamps](#column-method-timestamps)
[timestampsTz](#column-method-timestampsTz)
[softDeletes](#column-method-softDeletes)
[softDeletesTz](#column-method-softDeletesTz)
[year](#column-method-year)

</div>

<a name="binaries-method-list"></a>
#### Бінарні типи

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
#### Об'єктні типи та JSON

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a name="uuids-and-ulids-method-list"></a>
#### Типи UUID та ULID

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
#### Просторові типи

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

<a name="relationship-method-list"></a>
#### Типи для зв'язків

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[foreignUuidFor](#column-method-foreignUuidFor)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="specifics-method-list"></a>
#### Спеціальні типи

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

Метод `bigIncrements` створює автоінкрементний стовпець, еквівалентний `UNSIGNED BIGINT` (первинний ключ):

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

Метод `bigInteger` створює стовпець, еквівалентний `BIGINT`:

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()` {.collection-method}

Метод `binary` створює стовпець, еквівалентний `BLOB`:

```php
$table->binary('photo');
```

На MySQL, MariaDB чи SQL Server ви можете передати аргументи `length` і `fixed`, щоб створити стовпець, еквівалентний `VARBINARY` або `BINARY`:

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a name="column-method-boolean"></a>
#### `boolean()` {.collection-method}

Метод `boolean` створює стовпець, еквівалентний `BOOLEAN`:

```php
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
#### `char()` {.collection-method}

Метод `char` створює стовпець, еквівалентний `CHAR`, заданої довжини:

```php
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

Метод `dateTimeTz` створює стовпець, еквівалентний `DATETIME` (з часовою зоною), з необов'язковою точністю дробових секунд:

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

Метод `dateTime` створює стовпець, еквівалентний `DATETIME`, з необов'язковою точністю дробових секунд:

```php
$table->dateTime('created_at', precision: 0);
```

<a name="column-method-date"></a>
#### `date()` {.collection-method}

Метод `date` створює стовпець, еквівалентний `DATE`:

```php
$table->date('created_at');
```

<a name="column-method-decimal"></a>
#### `decimal()` {.collection-method}

Метод `decimal` створює стовпець, еквівалентний `DECIMAL`, із заданою точністю (загальна кількість цифр) і масштабом (кількість цифр після коми):

```php
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
#### `double()` {.collection-method}

Метод `double` створює стовпець, еквівалентний `DOUBLE`:

```php
$table->double('amount');
```

<a name="column-method-enum"></a>
#### `enum()` {.collection-method}

Метод `enum` створює стовпець, еквівалентний `ENUM`, із заданими допустимими значеннями:

```php
$table->enum('difficulty', ['easy', 'hard']);
```

Звісно, замість того щоб описувати масив допустимих значень вручну, ви можете скористатися методом `Enum::cases()`:

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

<a name="column-method-float"></a>
#### `float()` {.collection-method}

Метод `float` створює стовпець, еквівалентний `FLOAT`, із заданою точністю:

```php
$table->float('amount', precision: 53);
```

<a name="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

Метод `foreignId` створює стовпець, еквівалентний `UNSIGNED BIGINT`:

```php
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

Метод `foreignIdFor` додає для заданого класу моделі стовпець, еквівалентний `{column}_id`. Тип стовпця буде `UNSIGNED BIGINT`, `CHAR(36)` або `CHAR(26)` - залежно від типу ключа моделі:

```php
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

Метод `foreignUlid` створює стовпець, еквівалентний `ULID`:

```php
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

Метод `foreignUuid` створює стовпець, еквівалентний `UUID`:

```php
$table->foreignUuid('user_id');
```

<a name="column-method-foreignUuidFor"></a>
#### `foreignUuidFor()` {.collection-method}

Метод `foreignUuidFor` додає для заданого класу моделі стовпець `{column}_id`, еквівалентний UUID:

```php
$table->foreignUuidFor(User::class);
```

<a name="column-method-geography"></a>
#### `geography()` {.collection-method}

Метод `geography` створює стовпець, еквівалентний `GEOGRAPHY`, із заданим просторовим типом і SRID (Spatial Reference System Identifier):

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> Підтримка просторових типів залежить від драйвера вашої бази даних. Звіряйтеся з документацією своєї бази. Якщо ваш застосунок працює з PostgreSQL, перед використанням методу `geography` потрібно встановити розширення [PostGIS](https://postgis.net).

<a name="column-method-geometry"></a>
#### `geometry()` {.collection-method}

Метод `geometry` створює стовпець, еквівалентний `GEOMETRY`, із заданим просторовим типом і SRID (Spatial Reference System Identifier):

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> Підтримка просторових типів залежить від драйвера вашої бази даних. Звіряйтеся з документацією своєї бази. Якщо ваш застосунок працює з PostgreSQL, перед використанням методу `geometry` потрібно встановити розширення [PostGIS](https://postgis.net).

<a name="column-method-id"></a>
#### `id()` {.collection-method}

Метод `id` - псевдонім методу `bigIncrements`. За замовчуванням він створює стовпець `id`; втім, ви можете передати назву стовпця, якщо хочете назвати його інакше:

```php
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()` {.collection-method}

Метод `increments` створює автоінкрементний стовпець, еквівалентний `UNSIGNED INTEGER`, як первинний ключ:

```php
$table->increments('id');
```

<a name="column-method-integer"></a>
#### `integer()` {.collection-method}

Метод `integer` створює стовпець, еквівалентний `INTEGER`:

```php
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

Метод `ipAddress` створює стовпець, еквівалентний `VARCHAR`:

```php
$table->ipAddress('visitor');
```

На PostgreSQL буде створено стовпець `INET`.

<a name="column-method-json"></a>
#### `json()` {.collection-method}

Метод `json` створює стовпець, еквівалентний `JSON`:

```php
$table->json('options');
```

На SQLite буде створено стовпець `TEXT`.

<a name="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

Метод `jsonb` створює стовпець, еквівалентний `JSONB`:

```php
$table->jsonb('options');
```

На SQLite буде створено стовпець `TEXT`.

<a name="column-method-longText"></a>
#### `longText()` {.collection-method}

Метод `longText` створює стовпець, еквівалентний `LONGTEXT`:

```php
$table->longText('description');
```

На MySQL чи MariaDB ви можете застосувати до стовпця кодування `binary`, щоб створити стовпець, еквівалентний `LONGBLOB`:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

Метод `macAddress` створює стовпець, призначений для зберігання MAC-адреси. Деякі системи баз даних, як-от PostgreSQL, мають для таких даних окремий тип стовпця. Інші використають стовпець, еквівалентний рядковому:

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

Метод `mediumIncrements` створює автоінкрементний стовпець, еквівалентний `UNSIGNED MEDIUMINT`, як первинний ключ:

```php
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

Метод `mediumInteger` створює стовпець, еквівалентний `MEDIUMINT`:

```php
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

Метод `mediumText` створює стовпець, еквівалентний `MEDIUMTEXT`:

```php
$table->mediumText('description');
```

На MySQL чи MariaDB ви можете застосувати до стовпця кодування `binary`, щоб створити стовпець, еквівалентний `MEDIUMBLOB`:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
#### `morphs()` {.collection-method}

Метод `morphs` - це зручний метод, який додає стовпець `{column}_type`, еквівалентний `VARCHAR`, і стовпець `{column}_id`. Тип стовпця `{column}_id` буде `UNSIGNED BIGINT`, `CHAR(36)` або `CHAR(26)` - залежно від типу ключа моделі.

Цей метод призначений для опису стовпців, потрібних для поліморфного [зв'язку Eloquent](/docs/{{version}}/eloquent-relationships). У прикладі нижче буде створено стовпці `taggable_type` і `taggable_id`:

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

Метод схожий на [morphs](#column-method-morphs), але створені стовпці будуть «nullable»:

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

Метод схожий на [ulidMorphs](#column-method-ulidMorphs), але створені стовпці будуть «nullable»:

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

Метод схожий на [uuidMorphs](#column-method-uuidMorphs), але створені стовпці будуть «nullable»:

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

Метод `rememberToken` створює nullable-стовпець, еквівалентний `VARCHAR(100)`, призначений для зберігання поточного [токена автентифікації](/docs/{{version}}/authentication#remembering-users) «запам'ятати мене»:

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()` {.collection-method}

Метод `set` створює стовпець, еквівалентний `SET`, із заданим списком допустимих значень:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

Метод `smallIncrements` створює автоінкрементний стовпець, еквівалентний `UNSIGNED SMALLINT`, як первинний ключ:

```php
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

Метод `smallInteger` створює стовпець, еквівалентний `SMALLINT`:

```php
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

Метод `softDeletesTz` додає nullable-стовпець `deleted_at`, еквівалентний `TIMESTAMP` (з часовою зоною), з необов'язковою точністю дробових секунд. Цей стовпець призначений для зберігання часової позначки `deleted_at`, потрібної для м'якого видалення (soft delete) в Eloquent:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

Метод `softDeletes` додає nullable-стовпець `deleted_at`, еквівалентний `TIMESTAMP`, з необов'язковою точністю дробових секунд. Цей стовпець призначений для зберігання часової позначки `deleted_at`, потрібної для м'якого видалення в Eloquent:

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
#### `string()` {.collection-method}

Метод `string` створює стовпець, еквівалентний `VARCHAR`, заданої довжини:

```php
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
#### `text()` {.collection-method}

Метод `text` створює стовпець, еквівалентний `TEXT`:

```php
$table->text('description');
```

На MySQL чи MariaDB ви можете застосувати до стовпця кодування `binary`, щоб створити стовпець, еквівалентний `BLOB`:

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

Метод `timeTz` створює стовпець, еквівалентний `TIME` (з часовою зоною), з необов'язковою точністю дробових секунд:

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
#### `time()` {.collection-method}

Метод `time` створює стовпець, еквівалентний `TIME`, з необов'язковою точністю дробових секунд:

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

Метод `timestampTz` створює стовпець, еквівалентний `TIMESTAMP` (з часовою зоною), з необов'язковою точністю дробових секунд:

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

Метод `timestamp` створює стовпець, еквівалентний `TIMESTAMP`, з необов'язковою точністю дробових секунд:

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

Метод `timestampsTz` створює стовпці `created_at` і `updated_at`, еквівалентні `TIMESTAMP` (з часовою зоною), з необов'язковою точністю дробових секунд:

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

Метод `timestamps` створює стовпці `created_at` і `updated_at`, еквівалентні `TIMESTAMP`, з необов'язковою точністю дробових секунд:

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

Метод `tinyIncrements` створює автоінкрементний стовпець, еквівалентний `UNSIGNED TINYINT`, як первинний ключ:

```php
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

Метод `tinyInteger` створює стовпець, еквівалентний `TINYINT`:

```php
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

Метод `tinyText` створює стовпець, еквівалентний `TINYTEXT`:

```php
$table->tinyText('notes');
```

На MySQL чи MariaDB ви можете застосувати до стовпця кодування `binary`, щоб створити стовпець, еквівалентний `TINYBLOB`:

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

Метод `unsignedBigInteger` створює стовпець, еквівалентний `UNSIGNED BIGINT`:

```php
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

Метод `unsignedInteger` створює стовпець, еквівалентний `UNSIGNED INTEGER`:

```php
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

Метод `unsignedMediumInteger` створює стовпець, еквівалентний `UNSIGNED MEDIUMINT`:

```php
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

Метод `unsignedSmallInteger` створює стовпець, еквівалентний `UNSIGNED SMALLINT`:

```php
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

Метод `unsignedTinyInteger` створює стовпець, еквівалентний `UNSIGNED TINYINT`:

```php
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

Метод `ulidMorphs` - це зручний метод, який додає стовпець `{column}_type`, еквівалентний `VARCHAR`, і стовпець `{column}_id`, еквівалентний `CHAR(26)`.

Цей метод призначений для опису стовпців, потрібних для поліморфного [зв'язку Eloquent](/docs/{{version}}/eloquent-relationships), що використовує ідентифікатори ULID. У прикладі нижче буде створено стовпці `taggable_type` і `taggable_id`:

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

Метод `uuidMorphs` - це зручний метод, який додає стовпець `{column}_type`, еквівалентний `VARCHAR`, і стовпець `{column}_id`, еквівалентний `CHAR(36)`.

Цей метод призначений для опису стовпців, потрібних для [поліморфного зв'язку Eloquent](/docs/{{version}}/eloquent-relationships#polymorphic-relationships), що використовує ідентифікатори UUID. У прикладі нижче буде створено стовпці `taggable_type` і `taggable_id`:

```php
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
#### `ulid()` {.collection-method}

Метод `ulid` створює стовпець, еквівалентний `ULID`:

```php
$table->ulid('id');
```

<a name="column-method-uuid"></a>
#### `uuid()` {.collection-method}

Метод `uuid` створює стовпець, еквівалентний `UUID`:

```php
$table->uuid('id');
```

<a name="column-method-vector"></a>
#### `vector()` {.collection-method}

Метод `vector` створює стовпець, еквівалентний `vector`:

```php
$table->vector('embedding', dimensions: 100);
```

На PostgreSQL розширення `pgvector` має бути завантажене, перш ніж можна створювати стовпці `vector`:

```php
Schema::ensureVectorExtensionExists();
```

<a name="column-method-year"></a>
#### `year()` {.collection-method}

Метод `year` створює стовпець, еквівалентний `YEAR`:

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### Модифікатори стовпців

Крім перелічених вище типів, є кілька «модифікаторів» стовпців, якими ви можете скористатися, додаючи стовпець до таблиці. Наприклад, щоб зробити стовпець «nullable», викличте метод `nullable`:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

У таблиці нижче наведено всі доступні модифікатори стовпців. Цей список не містить [модифікаторів індексів](#creating-indexes):

<div class="overflow-auto">

| Модифікатор                         | Опис                                                                                           |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| `->after('column')`                 | Розмістити стовпець «після» іншого стовпця (MariaDB / MySQL).                                   |
| `->autoIncrement()`                 | Зробити стовпці `INTEGER` автоінкрементними (первинний ключ).                                   |
| `->charset('utf8mb4')`              | Задати кодування для стовпця (MariaDB / MySQL).                                                 |
| `->collation('utf8mb4_unicode_ci')` | Задати порядок сортування для стовпця.                                                          |
| `->comment('my comment')`           | Додати коментар до стовпця (MariaDB / MySQL / PostgreSQL).                                      |
| `->default($value)`                 | Задати значення стовпця за замовчуванням.                                                       |
| `->first()`                         | Розмістити стовпець «першим» у таблиці (MariaDB / MySQL).                                       |
| `->from($integer)`                  | Задати початкове значення автоінкрементного поля (MariaDB / MySQL / PostgreSQL).                |
| `->instant()`                       | Додати або змінити стовпець миттєвою операцією (MySQL).                                         |
| `->invisible()`                     | Зробити стовпець «невидимим» для запитів `SELECT *` (MariaDB / MySQL).                          |
| `->lock($mode)`                     | Задати режим блокування для операції зі стовпцем (MySQL).                                       |
| `->nullable($value = true)`         | Дозволити вставляти в стовпець значення `NULL`.                                                 |
| `->storedAs($expression)`           | Створити збережений генерований стовпець (MariaDB / MySQL / PostgreSQL / SQLite).               |
| `->unsigned()`                      | Зробити стовпці `INTEGER` типу `UNSIGNED` (MariaDB / MySQL).                                    |
| `->useCurrent()`                    | Задати стовпцям `TIMESTAMP` значення за замовчуванням `CURRENT_TIMESTAMP`.                      |
| `->useCurrentOnUpdate()`            | Задати стовпцям `TIMESTAMP` значення `CURRENT_TIMESTAMP` при оновленні запису (MariaDB / MySQL). |
| `->virtualAs($expression)`          | Створити віртуальний генерований стовпець (MariaDB / MySQL / SQLite).                           |
| `->generatedAs($expression)`        | Створити identity-стовпець із заданими опціями послідовності (PostgreSQL).                      |
| `->always()`                        | Задати перевагу значень послідовності над вхідними для identity-стовпця (PostgreSQL).            |

</div>

<a name="default-expressions"></a>
#### Вирази за замовчуванням

Модифікатор `default` приймає значення або екземпляр `Illuminate\Database\Query\Expression`. Використання `Expression` не дасть Laravel узяти значення в лапки й дозволить скористатися специфічними для бази функціями. Особливо це стає в пригоді, коли потрібно задати значення за замовчуванням для стовпців JSON:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
            $table->timestamps();
        });
    }
};
```

> [!WARNING]
> Підтримка виразів за замовчуванням залежить від драйвера вашої бази даних, її версії та типу поля. Звіряйтеся з документацією своєї бази.

<a name="column-order"></a>
#### Порядок стовпців

На MariaDB чи MySQL методом `after` можна додавати стовпці після наявного стовпця в схемі:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="instant-column-operations"></a>
#### Миттєві операції зі стовпцями

На MySQL ви можете дописати до опису стовпця модифікатор `instant`, щоб вказати: стовпець слід додати чи змінити «миттєвим» алгоритмом MySQL. Цей алгоритм дозволяє виконати певні зміни схеми без повного перебудування таблиці, тож вони майже миттєві незалежно від її розміру:

```php
$table->string('name')->nullable()->instant();
```

Миттєве додавання стовпців може лише дописувати стовпці в кінець таблиці, тому модифікатор `instant` не можна поєднувати з `after` чи `first`. Крім того, алгоритм підтримує не всі типи стовпців і не всі операції. Якщо запитана операція несумісна, MySQL видасть помилку.

Щоб дізнатися, які операції сумісні з миттєвою зміною стовпців, звіряйтеся з [документацією MySQL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html).

<a name="ddl-locking"></a>
#### Блокування DDL

На MySQL ви можете дописати модифікатор `lock` до опису стовпця, індексу чи зовнішнього ключа, щоб керувати блокуванням таблиці під час операцій зі схемою. MySQL підтримує кілька режимів блокування: `none` дозволяє одночасні читання й записи, `shared` дозволяє одночасні читання, але блокує записи, `exclusive` блокує будь-який одночасний доступ, а `default` дає MySQL самому обрати найдоречніший режим:

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

Якщо запитаний режим блокування несумісний з операцією, MySQL видасть помилку. Модифікатор `lock` можна поєднувати з модифікатором `instant`, щоб додатково оптимізувати зміни схеми:

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
### Зміна стовпців

Метод `change` дозволяє змінити тип і атрибути наявних стовпців. Наприклад, ви можете захотіти збільшити розмір стовпця `string`. Щоб побачити `change` у дії, збільшимо розмір стовпця `name` з 25 до 50. Для цього ми просто описуємо новий стан стовпця й викликаємо метод `change`:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

Змінюючи стовпець, ви маєте явно вказати всі модифікатори, які хочете на ньому зберегти, - будь-який пропущений атрибут буде скинуто. Наприклад, щоб зберегти атрибути `unsigned`, `default` і `comment`, кожен модифікатор потрібно викликати явно:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

Метод `change` не змінює індексів стовпця. Тому, змінюючи стовпець, ви можете скористатися модифікаторами індексів, щоб явно додати чи видалити індекс:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### Перейменування стовпців

Щоб перейменувати стовпець, скористайтеся методом `renameColumn` конструктора схеми:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### Видалення стовпців

Щоб видалити стовпець, скористайтеся методом `dropColumn` конструктора схеми:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

Ви можете видалити з таблиці кілька стовпців, передавши методу `dropColumn` масив їхніх назв:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### Доступні псевдоніми команд

Laravel має кілька зручних методів для видалення поширених типів стовпців. Кожен із них описано в таблиці нижче:

<div class="overflow-auto">

| Команда                             | Опис                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | Видалити стовпці `morphable_type` і `morphable_id`.   |
| `$table->dropRememberToken();`      | Видалити стовпець `remember_token`.                   |
| `$table->dropSoftDeletes();`        | Видалити стовпець `deleted_at`.                       |
| `$table->dropSoftDeletesTz();`      | Псевдонім методу `dropSoftDeletes()`.                 |
| `$table->dropTimestamps();`         | Видалити стовпці `created_at` і `updated_at`.         |
| `$table->dropTimestampsTz();`       | Псевдонім методу `dropTimestamps()`.                  |

</div>

<a name="indexes"></a>
## Індекси

<a name="creating-indexes"></a>
### Створення індексів

Конструктор схеми Laravel підтримує кілька типів індексів. У прикладі нижче створюється новий стовпець `email` і вказується, що його значення мають бути унікальними. Щоб створити індекс, ми дописуємо метод `unique` до опису стовпця:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

Або ж ви можете створити індекс після опису стовпця. Для цього викличте метод `unique` на blueprint конструктора схеми. Цей метод приймає назву стовпця, який має отримати унікальний індекс:

```php
$table->unique('email');
```

Ви можете навіть передати методу індексу масив стовпців, щоб створити складений (композитний) індекс:

```php
$table->index(['account_id', 'created_at']);
```

Створюючи індекс, Laravel автоматично згенерує його назву на основі таблиці, назв стовпців і типу індексу, але ви можете передати другий аргумент, щоб задати назву самостійно:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### Доступні типи індексів

Клас blueprint конструктора схеми Laravel має методи для створення кожного типу індексу, що його підтримує Laravel. Кожен метод індексу приймає необов'язковий другий аргумент - назву індексу. Якщо його не передати, назву буде утворено з назв таблиці й стовпців, використаних для індексу, а також типу індексу. Усі доступні методи індексів описано в таблиці нижче:

<div class="overflow-auto">

| Команда                                          | Опис                                                            |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `$table->primary('id');`                         | Додає первинний ключ.                                          |
| `$table->primary(['id', 'parent_id']);`          | Додає композитні ключі.                                        |
| `$table->unique('email');`                       | Додає унікальний індекс.                                       |
| `$table->index('state');`                        | Додає індекс.                                                  |
| `$table->fullText('body');`                      | Додає повнотекстовий індекс (MariaDB / MySQL / PostgreSQL).     |
| `$table->fullText('body')->language('english');` | Додає повнотекстовий індекс заданої мови (PostgreSQL).          |
| `$table->spatialIndex('location');`              | Додає просторовий індекс (окрім SQLite).                        |

</div>

<a name="online-index-creation"></a>
#### Створення індексу без блокування

За замовчуванням створення індексу на великій таблиці може заблокувати її й перекрити читання чи записи, поки індекс будується. На PostgreSQL або SQL Server ви можете дописати до опису індексу метод `online`, щоб створити індекс без блокування таблиці, - і ваш застосунок зможе далі читати й писати дані під час створення індексу:

```php
$table->string('email')->unique()->online();
```

На PostgreSQL це додає до запиту створення індексу опцію `CONCURRENTLY`. На SQL Server - опцію `WITH (online = on)`.

<a name="renaming-indexes"></a>
### Перейменування індексів

Щоб перейменувати індекс, скористайтеся методом `renameIndex` blueprint конструктора схеми. Він приймає поточну назву індексу першим аргументом і бажану назву - другим:

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### Видалення індексів

Щоб видалити індекс, ви маєте вказати його назву. За замовчуванням Laravel автоматично призначає назву індексу на основі назви таблиці, назви проіндексованого стовпця й типу індексу. Ось кілька прикладів:

<div class="overflow-auto">

| Команда                                                  | Опис                                                        |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`               | Видалити первинний ключ із таблиці «users».                  |
| `$table->dropUnique('users_email_unique');`              | Видалити унікальний індекс із таблиці «users».               |
| `$table->dropIndex('geo_state_index');`                  | Видалити базовий індекс із таблиці «geo».                    |
| `$table->dropFullText('posts_body_fulltext');`           | Видалити повнотекстовий індекс із таблиці «posts».           |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | Видалити просторовий індекс із таблиці «geo» (окрім SQLite). |

</div>

Якщо ви передасте методу видалення індексу масив стовпців, назву індексу буде згенеровано за конвенцією на основі назви таблиці, стовпців і типу індексу:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
### Обмеження зовнішніх ключів

Laravel також підтримує створення обмежень зовнішніх ключів, які забезпечують цілісність посилань на рівні бази даних. Наприклад, опишімо в таблиці `posts` стовпець `user_id`, що посилається на стовпець `id` таблиці `users`:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

Оскільки такий синтаксис досить громіздкий, Laravel має додаткові, лаконічніші методи, які спираються на конвенції й роблять роботу приємнішою. Якщо створювати стовпець методом `foreignId`, приклад вище можна переписати так:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

Метод `foreignId` створює стовпець, еквівалентний `UNSIGNED BIGINT`, а метод `constrained` за конвенціями визначає таблицю й стовпець, на які йде посилання. Якщо назва вашої таблиці не відповідає конвенціям Laravel, ви можете передати її методу `constrained` вручну. Крім того, можна задати й назву згенерованого індексу:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

Ви також можете задати бажану дію для властивостей обмеження «on delete» і «on update»:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

Для цих дій є й альтернативний, виразніший синтаксис:

<div class="overflow-auto">

| Метод                         | Опис                                              |
| ----------------------------- | ------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | Оновлення мають каскадуватися.                     |
| `$table->restrictOnUpdate();` | Оновлення мають бути обмежені.                     |
| `$table->nullOnUpdate();`     | Оновлення мають задавати зовнішньому ключу null.   |
| `$table->noActionOnUpdate();` | Жодних дій при оновленні.                          |
| `$table->cascadeOnDelete();`  | Видалення мають каскадуватися.                     |
| `$table->restrictOnDelete();` | Видалення мають бути обмежені.                     |
| `$table->nullOnDelete();`     | Видалення мають задавати зовнішньому ключу null.   |
| `$table->noActionOnDelete();` | Забороняє видалення, якщо є дочірні записи.        |

</div>

Будь-які додаткові [модифікатори стовпців](#column-modifiers) слід викликати перед методом `constrained`:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### Видалення зовнішніх ключів

Щоб видалити зовнішній ключ, скористайтеся методом `dropForeign`, передавши аргументом назву обмеження, яке слід видалити. Обмеження зовнішніх ключів мають ту саму конвенцію назв, що й індекси. Іншими словами, назва обмеження зовнішнього ключа складається з назви таблиці та стовпців в обмеженні, після яких додається суфікс «\_foreign»:

```php
$table->dropForeign('posts_user_id_foreign');
```

Або ж ви можете передати методу `dropForeign` масив із назвою стовпця, що містить зовнішній ключ. Масив буде перетворено на назву обмеження за конвенціями Laravel:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### Увімкнення та вимкнення обмежень зовнішніх ключів

Увімкнути або вимкнути обмеження зовнішніх ключів у ваших міграціях можна такими методами:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite за замовчуванням вимикає обмеження зовнішніх ключів. Працюючи з SQLite, обов'язково [увімкніть підтримку зовнішніх ключів](/docs/{{version}}/database#configuration) у конфігурації бази даних, перш ніж намагатися створювати їх у міграціях.

<a name="events"></a>
## Події

Для зручності кожна операція міграції надсилає [подію](/docs/{{version}}/events). Усі наведені нижче події розширюють базовий клас `Illuminate\Database\Events\MigrationEvent`:

<div class="overflow-auto">

| Клас                                             | Опис                                             |
| ------------------------------------------------ | ------------------------------------------------ |
| `Illuminate\Database\Events\DatabaseRefreshed`   | Команда `migrate:refresh` завершилася.           |
| `Illuminate\Database\Events\MigrationsStarted`   | Пакет міграцій ось-ось буде виконано.            |
| `Illuminate\Database\Events\MigrationsEnded`     | Пакет міграцій завершився.                       |
| `Illuminate\Database\Events\MigrationStarted`    | Окрему міграцію ось-ось буде виконано.           |
| `Illuminate\Database\Events\MigrationEnded`      | Окрема міграція завершилася.                     |
| `Illuminate\Database\Events\NoPendingMigrations` | Команда міграції не знайшла міграцій в очікуванні. |
| `Illuminate\Database\Events\SchemaDumped`        | Дамп схеми бази даних завершився.                |
| `Illuminate\Database\Events\SchemaLoaded`        | Наявний дамп схеми бази даних завантажено.       |

</div>
