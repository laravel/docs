---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Scout

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Черги](#queueing)
- [Передумови для драйверів](#driver-prerequisites)
- [Конфігурація](#configuration)
    - [Налаштування даних для пошуку](#configuring-searchable-data)
- [Рушії database і collection](#database-and-collection-engines)
    - [Рушій database](#database-engine)
    - [Рушій collection](#collection-engine)
- [Конфігурація сторонніх рушіїв](#third-party-engine-configuration)
    - [Налаштування індексів моделей](#configuring-model-indexes)
    - [Algolia](#algolia-configuration)
    - [Meilisearch](#meilisearch-configuration)
    - [Typesense](#typesense-configuration)
- [Індексування у сторонніх рушіях](#indexing)
    - [Пакетний імпорт](#batch-import)
    - [Додавання записів](#adding-records)
    - [Оновлення записів](#updating-records)
    - [Видалення записів](#removing-records)
    - [Призупинення індексування](#pausing-indexing)
    - [Умовна індексованість екземплярів моделей](#conditionally-searchable-model-instances)
- [Пошук](#searching)
    - [Умови where](#where-clauses)
    - [Пагінація](#pagination)
    - [М'яке видалення](#soft-deleting)
    - [Налаштування пошуку в рушіях](#customizing-engine-searches)
- [Власні рушії](#custom-engines)

<a name="introduction"></a>
## Вступ

[Laravel Scout](https://github.com/laravel/scout) надає просте рішення на драйверах, щоб додати повнотекстовий пошук до ваших [моделей Eloquent](/docs/{{version}}/eloquent). Через спостерігачів моделей Scout автоматично тримає ваші пошукові індекси синхронізованими із записами Eloquent.

Scout постачається із вбудованим рушієм `database`, який використовує повнотекстові індекси MySQL / PostgreSQL та умови `LIKE`, щоб шукати у вашій наявній базі даних - жодного зовнішнього сервісу не потрібно. Для більшості застосунків цього цілком достатньо. Огляд усіх можливостей пошуку в Laravel дивіться в [документації про пошук](/docs/{{version}}/search).

Scout також містить драйвери для [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com) і [Typesense](https://typesense.org) - на випадок, коли вам потрібні стійкість до одруківок, фасетна фільтрація чи геопошук у великих масштабах. Для локальної розробки доступний також драйвер «collection», а ще ви вільні писати [власні рушії](#custom-engines).

<a name="installation"></a>
## Встановлення

Спершу встановіть Scout через менеджер пакетів Composer:

```shell
composer require laravel/scout
```

Після встановлення Scout опублікуйте його конфігураційний файл артизан-командою `vendor:publish`. Ця команда опублікує файл `scout.php` до каталогу `config` вашого застосунку:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

Нарешті, додайте трейт `Laravel\Scout\Searchable` до моделі, яку ви хочете зробити придатною для пошуку. Цей трейт зареєструє спостерігача моделі, який автоматично триматиме модель синхронізованою з вашим пошуковим драйвером:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="queueing"></a>
### Черги

Якщо ви користуєтеся рушієм, відмінним від `database` чи `collection`, вам варто серйозно подумати про налаштування [драйвера черги](/docs/{{version}}/queues), перш ніж працювати з бібліотекою. Запущений воркер черги дозволить Scout ставити в чергу всі операції синхронізації даних моделі з пошуковими індексами, що суттєво покращить час відгуку вебінтерфейсу вашого застосунку.

Коли ви налаштували драйвер черги, встановіть опцію `queue` у вашому конфігураційному файлі `config/scout.php` у значення `true`:

```php
'queue' => true,
```

Навіть коли опція `queue` має значення `false`, важливо пам'ятати, що деякі драйвери Scout - як-от Algolia та Meilisearch - завжди індексують записи асинхронно. Іншими словами, навіть якщо операція індексування завершилася у вашому застосунку Laravel, сам пошуковий рушій може не одразу відобразити нові й оновлені записи.

Щоб указати підключення та чергу, які використовують завдання Scout, задайте опцію конфігурації `queue` масивом:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

Звісно, якщо ви змінюєте підключення та чергу для завдань Scout, вам слід запустити воркер черги, який оброблятиме завдання на цьому підключенні й у цій черзі:

```shell
php artisan queue:work redis --queue=scout
```

<a name="unique-jobs"></a>
#### Унікальні завдання

У застосунках з інтенсивним записом ви можете захотіти завадити Scout ставити в чергу дублікати завдань для тих самих записів моделі. Ви можете ввімкнути унікальні завдання індексування, зареєструвавши класи завдань `MakeSearchableUniquely` та `RemoveFromSearchUniquely` - зазвичай у методі `boot` сервіс-провайдера:

```php
use Laravel\Scout\Jobs\MakeSearchableUniquely;
use Laravel\Scout\Jobs\RemoveFromSearchUniquely;
use Laravel\Scout\Scout;

Scout::makeSearchableUsing(MakeSearchableUniquely::class);
Scout::removeFromSearchUsing(RemoveFromSearchUniquely::class);
```

Ці завдання використовують [блокування унікальних завдань](/docs/{{version}}/queues#unique-jobs) у Laravel, щоб не відправляти дублікати операцій індексування для тих самих записів моделі, доки відповідне завдання вже стоїть у черзі.

<a name="driver-prerequisites"></a>
## Передумови для драйверів

<a name="algolia"></a>
### Algolia

Користуючись драйвером Algolia, налаштуйте свої облікові дані Algolia `id` та `secret` у конфігураційному файлі `config/scout.php`. Коли облікові дані налаштовано, вам також треба встановити PHP SDK для Algolia через менеджер пакетів Composer:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com) - це швидкий пошуковий рушій з відкритим кодом. Якщо ви не знаєте, як встановити Meilisearch на своїй машині, скористайтеся [Laravel Sail](/docs/{{version}}/sail#meilisearch) - офіційно підтримуваним середовищем розробки Laravel на Docker.

Користуючись драйвером Meilisearch, вам треба встановити PHP SDK для Meilisearch через менеджер пакетів Composer:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

Далі задайте змінну оточення `SCOUT_DRIVER`, а також облікові дані Meilisearch `host` і `key` у файлі `.env` вашого застосунку:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Докладніше про Meilisearch читайте в [документації Meilisearch](https://docs.meilisearch.com/learn/getting_started/quick_start.html).

Крім того, переконайтеся, що ви встановили версію `meilisearch/meilisearch-php`, сумісну з версією вашого бінарника Meilisearch, - перегляньте [документацію Meilisearch щодо сумісності бінарників](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch).

> [!WARNING]
> Оновлюючи Scout у застосунку, який використовує Meilisearch, завжди [переглядайте додаткові зміни, що ламають сумісність](https://github.com/meilisearch/Meilisearch/releases) у самому сервісі Meilisearch.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org) - блискавично швидкий пошуковий рушій з відкритим кодом, який підтримує пошук за ключовими словами, семантичний пошук, геопошук і векторний пошук.

Ви можете [хостити Typesense самостійно](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) або скористатися [Typesense Cloud](https://cloud.typesense.org).

Щоб почати роботу з Typesense у Scout, встановіть PHP SDK для Typesense через менеджер пакетів Composer:

```shell
composer require typesense/typesense-php
```

Далі задайте змінну оточення `SCOUT_DRIVER`, а також хост і ключ API Typesense у файлі .env вашого застосунку:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

Якщо ви користуєтеся [Laravel Sail](/docs/{{version}}/sail), вам, можливо, доведеться підлаштувати змінну оточення `TYPESENSE_HOST` під ім'я контейнера Docker. Ви також можете за бажання вказати порт, шлях і протокол вашої установки:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Додаткові налаштування та визначення схем для ваших колекцій Typesense можна знайти в конфігураційному файлі `config/scout.php` вашого застосунку. Докладніше про Typesense читайте в [документації Typesense](https://typesense.org/docs/guide/#quick-start).

<a name="configuration"></a>
## Конфігурація

<a name="configuring-searchable-data"></a>
### Налаштування даних для пошуку

За замовчуванням до пошукового індексу потрапляє вся форма `toArray` заданої моделі. Якщо ви хочете налаштувати дані, які синхронізуються з індексом, перевизначте на моделі метод `toSearchableArray`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the indexable data array for the model.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // Customize the data array...

        return $array;
    }
}
```

<a name="configuring-search-engines-per-model"></a>
#### Налаштування рушіїв для моделей

Під час пошуку Scout зазвичай використовує стандартний пошуковий рушій, указаний у конфігураційному файлі `scout` вашого застосунку. Проте рушій для конкретної моделі можна змінити, перевизначивши на ній метод `searchableUsing`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\Scout;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="database-and-collection-engines"></a>
## Рушії database і collection

<a name="database-engine"></a>
### Рушій database

> [!WARNING]
> Наразі рушій database підтримує MySQL і PostgreSQL - обидві бази надають швидке повнотекстове індексування стовпців.

Рушій `database` використовує повнотекстові індекси MySQL / PostgreSQL та умови `LIKE`, щоб шукати безпосередньо у вашій наявній базі даних. Для багатьох застосунків це найпростіший і найпрактичніший спосіб додати пошук - жодного зовнішнього сервісу чи додаткової інфраструктури не потрібно.

Щоб скористатися рушієм database, встановіть змінну оточення `SCOUT_DRIVER` у значення `database`:

```ini
SCOUT_DRIVER=database
```

Коли рушій налаштовано, ви можете [описати дані для пошуку](#configuring-searchable-data) і почати [виконувати пошукові запити](#searching) до своїх моделей. На відміну від сторонніх рушіїв, рушій database не потребує окремого етапу індексування - він шукає безпосередньо у таблицях вашої бази даних.

#### Налаштування стратегій пошуку в базі даних

За замовчуванням рушій database виконає запит `LIKE` до кожного атрибута моделі, який ви [налаштували для пошуку](#configuring-searchable-data). Проте ви можете призначити конкретним стовпцям ефективніші стратегії пошуку. Атрибут `SearchUsingFullText` використовуватиме для цього стовпця повнотекстовий індекс вашої бази, а `SearchUsingPrefix` шукатиме лише збіг на початку рядків (`example%`), а не по всьому рядку (`%example%`).

Щоб задати цю поведінку, застосуйте PHP-атрибути до методу `toSearchableArray` вашої моделі. Стовпці без атрибута й далі використовуватимуть стандартну стратегію `LIKE`:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray(): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```

> [!WARNING]
> Перш ніж указувати, що стовпець має використовувати повнотекстові обмеження запиту, переконайтеся, що йому призначено [повнотекстовий індекс](/docs/{{version}}/migrations#available-index-types).

<a name="collection-engine"></a>
### Рушій collection

Рушій «collection» призначений для швидких прототипів, украй малих наборів даних (кілька сотень записів) чи прогону тестів. Він дістає з вашої бази всі можливі записи й фільтрує їх у PHP хелпером `Str::is`, тож не потребує ані індексування, ані специфічних можливостей бази даних. Для будь-чого серйознішого за тривіальні випадки скористайтеся натомість [рушієм database](#database-engine).

Щоб скористатися рушієм collection, просто встановіть змінну оточення `SCOUT_DRIVER` у значення `collection` або вкажіть драйвер `collection` безпосередньо в конфігураційному файлі `scout` вашого застосунку:

```ini
SCOUT_DRIVER=collection
```

Коли ви обрали драйвер collection, можете починати [виконувати пошукові запити](#searching) до своїх моделей. Індексування в пошуковому рушії - як-от те, що потрібне для наповнення індексів Algolia, Meilisearch чи Typesense, - із рушієм collection не потрібне.

#### Відмінності від рушія database

Якщо рушій database ефективно знаходить відповідні записи через повнотекстові індекси та умови `LIKE`, то рушій collection дістає всі записи й фільтрує їх у PHP. Рушій collection - найпереносніший варіант, адже працює з усіма реляційними базами, які підтримує Laravel (зокрема SQLite та SQL Server); проте він значно менш ефективний за рушій database і не має використовуватися з великими наборами даних.

<a name="third-party-engine-configuration"></a>
## Конфігурація сторонніх рушіїв

Наведені далі опції конфігурації стосуються лише сторонніх пошукових рушіїв - як-от Algolia, Meilisearch чи Typesense. Якщо ви користуєтеся [рушієм database](#database-engine), цей розділ можна пропустити.

<a name="configuring-model-indexes"></a>
### Налаштування індексів моделей

Коли ви користуєтеся стороннім рушієм, кожна модель Eloquent синхронізується із заданим пошуковим «індексом», що містить усі придатні для пошуку записи цієї моделі. За замовчуванням кожна модель зберігатиметься в індексі, ім'я якого збігається зі звичним іменем «таблиці» моделі. Зазвичай це форма множини від імені моделі; проте ви вільні змінити індекс моделі, перевизначивши на ній метод `searchableAs`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

> [!NOTE]
> Метод `searchableAs` не має жодного впливу під час використання рушія database, який завжди шукає безпосередньо в таблиці бази даних моделі.

<a name="configuring-the-model-id"></a>
#### Налаштування ID моделі

За замовчуванням Scout використовує первинний ключ моделі як її унікальний ID / ключ, що зберігається в пошуковому індексі. Якщо вам треба змінити цю поведінку зі стороннім рушієм, перевизначте на моделі методи `getScoutKey` та `getScoutKeyName`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

> [!NOTE]
> Методи `getScoutKey` та `getScoutKeyName` не мають жодного впливу під час використання рушія database, який завжди використовує первинний ключ моделі.

<a name="algolia-configuration"></a>
### Algolia

<a name="algolia-index-settings"></a>
#### Налаштування індексів

Іноді вам може знадобитися задати додаткові налаштування для ваших індексів Algolia. Хоча керувати ними можна через інтерфейс Algolia, іноді ефективніше описати бажаний стан конфігурації індексу просто в конфігураційному файлі `config/scout.php` вашого застосунку.

Такий підхід дозволяє розгортати ці налаштування через автоматизований пайплайн розгортання вашого застосунку, уникаючи ручного налаштування й забезпечуючи узгодженість між середовищами. Ви можете налаштувати атрибути для фільтрації, ранжування, фасети чи [будь-які інші підтримувані налаштування](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings).

Для початку додайте налаштування для кожного індексу в конфігураційному файлі `config/scout.php` вашого застосунку:

```php
use App\Models\User;
use App\Models\Flight;

'algolia' => [
    'id' => env('ALGOLIA_APP_ID', ''),
    'secret' => env('ALGOLIA_SECRET', ''),
    'index-settings' => [
        User::class => [
            'searchableAttributes' => ['id', 'name', 'email'],
            'attributesForFaceting'=> ['filterOnly(email)'],
            // Other settings fields...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

Якщо модель, що лежить в основі заданого індексу, підтримує м'яке видалення (soft delete) і включена до масиву `index-settings`, Scout автоматично додасть до цього індексу підтримку фасетів для м'яко видалених моделей. Якщо для індексу такої моделі вам більше нічого описувати у фасетах, просто додайте до масиву `index-settings` порожній запис для цієї моделі:

```php
'index-settings' => [
    Flight::class => []
],
```

Налаштувавши індекси вашого застосунку, ви маєте викликати артизан-команду `scout:sync-index-settings`. Ця команда повідомить Algolia про поточні налаштування ваших індексів. Для зручності вам, можливо, варто зробити цю команду частиною процесу розгортання:

```shell
php artisan scout:sync-index-settings
```

<a name="algolia-identifying-users"></a>
#### Ідентифікація користувачів

Scout дозволяє автоматично ідентифікувати користувачів під час роботи з Algolia. Прив'язка автентифікованого користувача до пошукових операцій може стати в пригоді при перегляді пошукової аналітики в панелі Algolia. Увімкнути ідентифікацію користувачів можна, задавши змінну оточення `SCOUT_IDENTIFY` у значення `true` у файлі `.env` вашого застосунку:

```ini
SCOUT_IDENTIFY=true
```

Увімкнення цієї можливості також передаватиме до Algolia IP-адресу запиту та первинний ідентифікатор автентифікованого користувача, тож ці дані буде пов'язано з кожним пошуковим запитом користувача.

<a name="meilisearch-configuration"></a>
### Meilisearch

<a name="meilisearch-index-settings"></a>
#### Налаштування індексів

Meilisearch вимагає наперед описати налаштування пошуку для індексу - як-от атрибути для фільтрації, атрибути для сортування та [інші підтримувані поля налаштувань](https://docs.meilisearch.com/reference/api/settings.html).

Атрибути для фільтрації - це будь-які атрибути, за якими ви плануєте фільтрувати через метод `where` у Scout, а атрибути для сортування - ті, за якими ви плануєте сортувати через метод `orderBy`. Щоб описати налаштування індексів, підлаштуйте частину `index-settings` запису `meilisearch` у конфігураційному файлі `scout` вашого застосунку:

```php
use App\Models\User;
use App\Models\Flight;

'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        User::class => [
            'filterableAttributes'=> ['id', 'name', 'email'],
            'sortableAttributes' => ['created_at'],
            // Other settings fields...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

Якщо модель, що лежить в основі заданого індексу, підтримує м'яке видалення і включена до масиву `index-settings`, Scout автоматично додасть до цього індексу підтримку фільтрації м'яко видалених моделей. Якщо для індексу такої моделі вам більше нічого описувати в атрибутах фільтрації чи сортування, просто додайте до масиву `index-settings` порожній запис для цієї моделі:

```php
'index-settings' => [
    Flight::class => []
],
```

Налаштувавши індекси вашого застосунку, ви маєте викликати артизан-команду `scout:sync-index-settings`. Ця команда повідомить Meilisearch про поточні налаштування ваших індексів. Для зручності вам, можливо, варто зробити цю команду частиною процесу розгортання:

```shell
php artisan scout:sync-index-settings
```

<a name="meilisearch-data-types"></a>
#### Типи даних для пошуку

Meilisearch виконуватиме операції фільтрації (`>`, `<` тощо) лише над даними правильного типу. Налаштовуючи дані для пошуку, переконайтеся, що числові значення приведено до відповідного типу:

```php
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="typesense-configuration"></a>
### Typesense

<a name="typesense-searchable-data"></a>
#### Підготовка даних для пошуку

Користуючись Typesense, ваші придатні до пошуку моделі мають визначати метод `toSearchableArray`, який приводить первинний ключ моделі до рядка, а дату створення - до UNIX-мітки часу:

```php
/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray(): array
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```

Вам також слід описати схеми колекцій Typesense у файлі `config/scout.php` вашого застосунку. Схема колекції описує типи даних кожного поля, доступного для пошуку через Typesense. Докладніше про всі доступні опції схеми читайте в [документації Typesense](https://typesense.org/docs/latest/api/collections.html#schema-parameters).

Якщо вам треба змінити схему колекції Typesense після того, як її описано, ви можете або виконати `scout:flush` і `scout:import`, що видалить усі проіндексовані дані й перестворить схему, або скористатися API Typesense, щоб змінити схему колекції, не видаляючи проіндексованих даних.

Якщо ваша придатна до пошуку модель підтримує м'яке видалення, опишіть поле `__soft_deleted` у відповідній схемі Typesense у конфігураційному файлі `config/scout.php` вашого застосунку:

```php
User::class => [
    'collection-schema' => [
        'fields' => [
            // ...
            [
                'name' => '__soft_deleted',
                'type' => 'int32',
                'optional' => true,
            ],
        ],
    ],
],
```

<a name="typesense-dynamic-search-parameters"></a>
#### Динамічні параметри пошуку

Typesense дозволяє змінювати ваші [параметри пошуку](https://typesense.org/docs/latest/api/search.html#search-parameters) динамічно під час виконання пошуку - через метод `options`:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="indexing"></a>
## Індексування у сторонніх рушіях

> [!NOTE]
> Описані в цьому розділі можливості індексування стосуються передусім сторонніх рушіїв (Algolia, Meilisearch чи Typesense). Рушій database шукає безпосередньо у ваших таблицях, тож не потребує ручного керування індексами.

<a name="batch-import"></a>
### Пакетний імпорт

Якщо ви встановлюєте Scout у наявний проєкт, у вас, можливо, вже є записи в базі даних, які треба імпортувати до індексів. Scout надає артизан-команду `scout:import`, якою можна імпортувати всі наявні записи до ваших пошукових індексів:

```shell
php artisan scout:import "App\Models\Post"
```

Команда `scout:queue-import` дозволяє імпортувати всі ваші наявні записи через [завдання в черзі](/docs/{{version}}/queues):

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

Команда `flush` дозволяє прибрати всі записи моделі з ваших пошукових індексів:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### Зміна запиту для імпорту

Якщо ви хочете змінити запит, яким дістаються всі ваші моделі для пакетного імпорту, визначте на моделі метод `makeAllSearchableUsing`. Це чудове місце, щоб додати будь-яке жадібне завантаження зв'язків, потрібне перед імпортом ваших моделей:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * Modify the query used to retrieve models when making all of the models searchable.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> Метод `makeAllSearchableUsing` може бути незастосовним, коли пакетний імпорт моделей іде через чергу. Зв'язки [не відновлюються](/docs/{{version}}/queues#handling-relationships), коли колекції моделей обробляються завданнями.

<a name="adding-records"></a>
### Додавання записів

Коли ви додали трейт `Laravel\Scout\Searchable` до моделі, вам залишається лише зберегти (`save`) чи створити (`create`) екземпляр моделі - і його буде автоматично додано до вашого пошукового індексу. Якщо ви налаштували Scout [на використання черг](#queueing), цю операцію виконає у фоні ваш воркер черги:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### Додавання записів через запит

Якщо ви хочете додати до пошукового індексу колекцію моделей через запит Eloquent, додайте до нього ланцюжком метод `searchable`. Метод `searchable` [розіб'є результати](/docs/{{version}}/eloquent#chunking-results) запиту на порції й додасть записи до вашого пошукового індексу. І знову ж: якщо ви налаштували Scout на використання черг, усі порції буде імпортовано у фоні вашими воркерами:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Ви також можете викликати метод `searchable` на екземплярі зв'язку Eloquent:

```php
$user->orders()->searchable();
```

Або ж, якщо у вас уже є колекція моделей Eloquent у пам'яті, викличте метод `searchable` на екземплярі колекції, щоб додати екземпляри моделей до відповідного індексу:

```php
$orders->searchable();
```

> [!NOTE]
> Метод `searchable` можна вважати операцією «upsert». Іншими словами, якщо запис моделі вже є у вашому індексі, його буде оновлено. Якщо його в індексі немає, його буде додано.

<a name="updating-records"></a>
### Оновлення записів

Щоб оновити придатну до пошуку модель, вам треба лише змінити властивості її екземпляра й зберегти (`save`) модель до бази даних. Scout автоматично збереже зміни до вашого пошукового індексу:

```php
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

Ви також можете викликати метод `searchable` на екземплярі запиту Eloquent, щоб оновити колекцію моделей. Якщо моделей у вашому пошуковому індексі немає, їх буде створено:

```php
Order::where('price', '>', 100)->searchable();
```

Якщо ви хочете оновити записи пошукового індексу для всіх моделей у зв'язку, викличте `searchable` на екземплярі зв'язку:

```php
$user->orders()->searchable();
```

Або ж, якщо у вас уже є колекція моделей Eloquent у пам'яті, викличте метод `searchable` на екземплярі колекції, щоб оновити екземпляри моделей у відповідному індексі:

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### Зміна записів перед імпортом

Іноді вам може знадобитися підготувати колекцію моделей, перш ніж робити їх придатними до пошуку. Наприклад, ви можете захотіти жадібно завантажити зв'язок, щоб його дані ефективно потрапили до пошукового індексу. Для цього визначте у відповідній моделі метод `makeSearchableUsing`:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * Modify the collection of models being made searchable.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="conditionally-updating-the-search-index"></a>
#### Умовне оновлення пошукового індексу

За замовчуванням Scout переіндексує оновлену модель незалежно від того, які атрибути було змінено. Якщо ви хочете змінити цю поведінку, визначте на моделі метод `searchIndexShouldBeUpdated`:

```php
/**
 * Determine if the search index should be updated.
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```

<a name="removing-records"></a>
### Видалення записів

Щоб прибрати запис із вашого індексу, просто видаліть (`delete`) модель із бази даних. Це працює навіть із моделями, що використовують [м'яке видалення](/docs/{{version}}/eloquent#soft-deleting):

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

Якщо ви не хочете діставати модель перед видаленням запису, скористайтеся методом `unsearchable` на екземплярі запиту Eloquent:

```php
Order::where('price', '>', 100)->unsearchable();
```

Якщо ви хочете прибрати записи пошукового індексу для всіх моделей у зв'язку, викличте `unsearchable` на екземплярі зв'язку:

```php
$user->orders()->unsearchable();
```

Або ж, якщо у вас уже є колекція моделей Eloquent у пам'яті, викличте метод `unsearchable` на екземплярі колекції, щоб прибрати екземпляри моделей із відповідного індексу:

```php
$orders->unsearchable();
```

Щоб прибрати з відповідного індексу всі записи моделі, викличте метод `removeAllFromSearch`:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### Призупинення індексування

Іноді вам може знадобитися виконати пакет операцій Eloquent над моделлю, не синхронізуючи її дані з пошуковим індексом. Зробити це можна методом `withoutSyncingToSearch`. Цей метод приймає єдине замикання, яке буде виконано одразу. Жодна операція з моделлю всередині замикання не потрапить до індексу моделі:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // Perform model actions...
});
```

<a name="conditionally-searchable-model-instances"></a>
### Умовна індексованість екземплярів моделей

Іноді вам може знадобитися робити модель придатною до пошуку лише за певних умов. Уявіть, наприклад, що у вас є модель `App\Models\Post`, яка може бути в одному з двох станів: «draft» і «published». Ви можете захотіти, щоб до пошуку потрапляли лише «published»-дописи. Для цього визначте на моделі метод `shouldBeSearchable`:

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

Метод `shouldBeSearchable` застосовується лише тоді, коли ви працюєте з моделями через методи `save` і `create`, запити чи зв'язки. Пряме додавання моделей чи колекцій до пошуку методом `searchable` перевизначить результат методу `shouldBeSearchable`.

> [!WARNING]
> Метод `shouldBeSearchable` незастосовний із рушієм Scout «database», адже всі дані для пошуку завжди зберігаються в базі. Щоб досягти схожої поведінки з рушієм database, скористайтеся натомість [умовами where](#where-clauses).

<a name="searching"></a>
## Пошук

Почати пошук по моделі можна методом `search`. Метод search приймає єдиний рядок, за яким шукатимуться ваші моделі. Далі додайте до пошукового запиту ланцюжком метод `get`, щоб отримати моделі Eloquent, які відповідають заданому запиту:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Оскільки пошук у Scout повертає колекцію моделей Eloquent, ви можете навіть повертати результати просто з маршруту чи контролера - їх буде автоматично перетворено на JSON:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Якщо ви хочете отримати сирі результати пошуку до їх перетворення на моделі Eloquent, скористайтеся методом `raw`:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### Власні індекси

Шукаючи через сторонні рушії, пошукові запити зазвичай виконуються в індексі, вказаному методом моделі [searchableAs](#configuring-model-indexes). Проте ви можете скористатися методом `within`, щоб указати інший індекс для пошуку:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Умови where

Scout дозволяє додавати до пошукових запитів умови «where». Наприклад, базові перевірки на рівність стають у пригоді, щоб обмежити пошук за ID власника:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

Ви також можете скористатися операторами порівняння `=`, `!=`, `<`, `>`, `>=`, `<=`, щоб будувати складніші запити:

```php
Order::search('Star Trek')
  ->where('status', '=', 'completed')
  ->where('is_refunded', '!=', true)
  ->where('total_price', '>', 100)
  ->where('shipping_cost', '<', 20)
  ->where('discount_percent', '>=', 10)
  ->where('item_count', '<=', 5)
  ->get();
```

Крім того, метод `whereIn` дозволяє перевірити, що значення заданого стовпця міститься в заданому масиві:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

Метод `whereNotIn` перевіряє, що значення заданого стовпця не міститься в заданому масиві:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

> [!WARNING]
> Якщо ваш застосунок використовує Meilisearch, вам треба налаштувати [атрибути для фільтрації](#meilisearch-index-settings), перш ніж користуватися умовами «where» у Scout.

<a name="customizing-the-eloquent-results-query"></a>
#### Налаштування запиту результатів Eloquent

Коли Scout отримає від пошукового рушія вашого застосунку список відповідних моделей Eloquent, Eloquent дістає всі ці моделі за їхніми первинними ключами. Ви можете налаштувати цей запит методом `query`. Метод `query` приймає замикання, яке отримає аргументом екземпляр конструктора запитів Eloquent:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

Зі стороннім рушієм цей колбек викликається вже після того, як потрібні моделі отримано з пошукового рушія, тож його не варто використовувати для «фільтрації» результатів - скористайтеся натомість [умовами where у Scout](#where-clauses). Проте з рушієм database обмеження методу `query` застосовуються безпосередньо до запиту в базу, тож ви можете використовувати його й для фільтрації.

<a name="pagination"></a>
### Пагінація

Окрім отримання колекції моделей, ви можете розбити результати пошуку на сторінки методом `paginate`. Цей метод поверне екземпляр `Illuminate\Pagination\LengthAwarePaginator` - так само, як і при [пагінації звичайного запиту Eloquent](/docs/{{version}}/pagination):

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

Ви можете вказати, скільки моделей отримувати на сторінку, передавши кількість першим аргументом до методу `paginate`:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

З рушієм database ви можете також скористатися методом `simplePaginate`. На відміну від `paginate`, який дістає загальну кількість відповідних записів, щоб показати номери сторінок, `simplePaginate` лише визначає, чи є результати за межами поточної сторінки, - що ефективніше для великих наборів даних, де вам потрібні лише посилання «попередня» й «наступна»:

```php
$orders = Order::search('Star Trek')->simplePaginate(15);
```

Отримавши результати, ви можете показати їх і відрендерити посилання на сторінки через [Blade](/docs/{{version}}/blade) - так само, як при пагінації звичайного запиту Eloquent:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

Звісно, якщо ви хочете отримати результати пагінації як JSON, поверніть екземпляр пагінатора просто з маршруту чи контролера:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> Оскільки пошукові рушії не знають про визначення глобальних скопів вашої моделі Eloquent, вам не слід використовувати глобальні скопи в застосунках, що покладаються на пагінацію Scout. Або ж вам треба відтворити обмеження глобального скопа під час пошуку через Scout.

<a name="soft-deleting"></a>
### М'яке видалення

Якщо ваші проіндексовані моделі використовують [м'яке видалення](/docs/{{version}}/eloquent#soft-deleting) і вам треба шукати серед м'яко видалених моделей, встановіть опцію `soft_delete` у конфігураційному файлі `config/scout.php` у значення `true`:

```php
'soft_delete' => true,
```

Коли ця опція має значення `true`, Scout не прибиратиме м'яко видалені моделі з пошукового індексу. Натомість він встановить прихований атрибут `__soft_deleted` на проіндексованому записі. Далі ви можете скористатися методами `withTrashed` чи `onlyTrashed`, щоб діставати м'яко видалені записи під час пошуку:

```php
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> Коли м'яко видалену модель остаточно видаляють через `forceDelete`, Scout автоматично прибирає її з пошукового індексу.

<a name="customizing-engine-searches"></a>
### Налаштування пошуку в рушіях

Якщо вам потрібне складне налаштування пошукової поведінки рушія, ви можете передати замикання другим аргументом до методу `search`. Наприклад, цим колбеком можна додати геодані до ваших опцій пошуку, перш ніж запит буде передано до Algolia:

```php
use Algolia\AlgoliaSearch\SearchIndex;
use App\Models\Order;

Order::search(
    'Star Trek',
    function (SearchIndex $algolia, string $query, array $options) {
        $options['body']['query']['bool']['filter']['geo_distance'] = [
            'distance' => '1000km',
            'location' => ['lat' => 36, 'lon' => 111],
        ];

        return $algolia->search($query, $options);
    }
)->get();
```

<a name="custom-engines"></a>
## Власні рушії

<a name="writing-the-engine"></a>
#### Написання рушія

Якщо жоден із вбудованих пошукових рушіїв Scout вам не пасує, ви можете написати власний і зареєструвати його в Scout. Ваш рушій має успадковувати абстрактний клас `Laravel\Scout\Engines\Engine`. Цей абстрактний клас містить вісім методів, які має реалізувати ваш рушій:

```php
use Laravel\Scout\Builder;

abstract public function update($models);
abstract public function delete($models);
abstract public function search(Builder $builder);
abstract public function paginate(Builder $builder, $perPage, $page);
abstract public function mapIds($results);
abstract public function map(Builder $builder, $results, $model);
abstract public function getTotalCount($results);
abstract public function flush($model);
```

Вам може бути корисно переглянути реалізації цих методів у класі `Laravel\Scout\Engines\AlgoliaEngine`. Цей клас стане хорошою відправною точкою, щоб зрозуміти, як реалізувати кожен із них у власному рушії.

<a name="registering-the-engine"></a>
#### Реєстрація рушія

Написавши власний рушій, ви можете зареєструвати його в Scout методом `extend` менеджера рушіїв Scout. Менеджер рушіїв Scout можна розв'язати із сервіс-контейнера Laravel. Викликати метод `extend` слід у методі `boot` вашого класу `App\Providers\AppServiceProvider` чи будь-якого іншого сервіс-провайдера вашого застосунку:

```php
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

Коли ваш рушій зареєстровано, ви можете вказати його як стандартний `driver` Scout у конфігураційному файлі `config/scout.php` вашого застосунку:

```php
'driver' => 'mysql',
```
