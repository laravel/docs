---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: початок роботи

- [Вступ](#introduction)
- [Створення класів моделей](#generating-model-classes)
- [Конвенції моделей Eloquent](#eloquent-model-conventions)
    - [Назви таблиць](#table-names)
    - [Первинні ключі](#primary-keys)
    - [Ключі UUID та ULID](#uuid-and-ulid-keys)
    - [Часові позначки](#timestamps)
    - [Підключення до бази даних](#database-connections)
    - [Значення атрибутів за замовчуванням](#default-attribute-values)
    - [Налаштування строгості Eloquent](#configuring-eloquent-strictness)
- [Отримання моделей](#retrieving-models)
    - [Колекції](#collections)
    - [Обробка результатів частинами](#chunking-results)
    - [Обробка частинами через ліниві колекції](#chunking-using-lazy-collections)
    - [Курсори](#cursors)
    - [Складніші підзапити](#advanced-subqueries)
- [Отримання окремих моделей та агрегатів](#retrieving-single-models)
    - [Отримання або створення моделей](#retrieving-or-creating-models)
    - [Отримання агрегатів](#retrieving-aggregates)
- [Вставка та оновлення моделей](#inserting-and-updating-models)
    - [Вставка](#inserts)
    - [Оновлення](#updates)
    - [Масове призначення](#mass-assignment)
    - [Upsert](#upserts)
- [Видалення моделей](#deleting-models)
    - [М'яке видалення](#soft-deleting)
    - [Запити до м'яко видалених моделей](#querying-soft-deleted-models)
- [Очищення моделей](#pruning-models)
- [Копіювання моделей](#replicating-models)
- [Скопи запитів](#query-scopes)
    - [Глобальні скопи](#global-scopes)
    - [Локальні скопи](#local-scopes)
    - [Відкладені атрибути](#pending-attributes)
- [Порівняння моделей](#comparing-models)
- [Події](#events)
    - [Використання замикань](#events-using-closures)
    - [Спостерігачі](#observers)
    - [Вимкнення подій](#muting-events)

<a name="introduction"></a>
## Вступ

Laravel містить Eloquent - об'єктно-реляційний мапер (ORM), який робить роботу з базою даних приємною. Коли ви користуєтеся Eloquent, кожній таблиці бази даних відповідає своя «модель», через яку ви з цією таблицею працюєте. Крім читання записів, моделі Eloquent дозволяють вставляти, оновлювати та видаляти записи в таблиці.

> [!NOTE]
> Перш ніж почати, обов'язково налаштуйте підключення до бази даних у файлі `config/database.php` вашого застосунку. Детальніше про налаштування бази читайте в [документації з конфігурації бази даних](/docs/{{version}}/database#configuration).

<a name="generating-model-classes"></a>
## Створення класів моделей

Для початку створімо модель Eloquent. Моделі зазвичай лежать у каталозі `app\Models` і розширюють клас `Illuminate\Database\Eloquent\Model`. Щоб згенерувати нову модель, скористайтеся [artisan-командою](/docs/{{version}}/artisan) `make:model`:

```shell
php artisan make:model Flight
```

Якщо ви хочете разом із моделлю згенерувати [міграцію бази даних](/docs/{{version}}/migrations), скористайтеся опцією `--migration` або `-m`:

```shell
php artisan make:model Flight --migration
```

Разом із моделлю можна згенерувати й інші класи: фабрики, сідери, політики, контролери та form request. Ці опції можна поєднувати, щоб створити кілька класів одразу:

```shell
# Generate a model and a FlightFactory class...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# Generate a model and a FlightSeeder class...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# Generate a model and a FlightController class...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# Generate a model, FlightController resource class, and form request classes...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# Generate a model and a FlightPolicy class...
php artisan make:model Flight --policy

# Generate a model and a migration, factory, seeder, and controller...
php artisan make:model Flight -mfsc

# Shortcut to generate a model, migration, factory, seeder, policy, controller, and form requests...
php artisan make:model Flight --all
php artisan make:model Flight -a

# Generate a pivot model...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### Огляд моделей

Іноді буває непросто зрозуміти всі доступні атрибути та зв'язки моделі, лише проглянувши її код. Натомість спробуйте artisan-команду `model:show` - вона дає зручний огляд усіх атрибутів і зв'язків моделі:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Конвенції моделей Eloquent

Моделі, згенеровані командою `make:model`, потрапляють до каталогу `app/Models`. Розгляньмо простий клас моделі й обговорімо кілька ключових конвенцій Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    // ...
}
```

<a name="table-names"></a>
### Назви таблиць

Погляньте на приклад вище: ми ніде не сказали Eloquent, яка таблиця відповідає нашій моделі `Flight`. За конвенцією назвою таблиці стає назва класу в «snake case» і в множині - хіба що ви явно вказали іншу. Тож у цьому випадку Eloquent вважатиме, що модель `Flight` зберігає записи в таблиці `flights`, а модель `AirTrafficController` - у таблиці `air_traffic_controllers`.

Якщо відповідна таблиця вашої моделі не відповідає цій конвенції, ви можете вказати назву таблиці вручну атрибутом `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table('my_flights')]
class Flight extends Model
{
    // ...
}
```


<a name="primary-keys"></a>
### Первинні ключі

Eloquent також вважає, що відповідна таблиця кожної моделі має стовпець первинного ключа з назвою `id`. За потреби ви можете вказати інший стовпець як первинний ключ моделі через аргумент `key` атрибута `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'flight_id')]
class Flight extends Model
{
    // ...
}
```

Крім того, Eloquent вважає, що первинний ключ - це автоінкрементне ціле число, тож він автоматично приводить його до цілого. Якщо ви хочете скористатися неавтоінкрементним або нечисловим первинним ключем, задайте аргументи `keyType` та `incrementing` атрибута `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'uuid', keyType: 'string', incrementing: false)]
class Flight extends Model
{
    // ...
}
```

Якщо вам потрібно лише вимкнути автоінкрементні ID, скористайтеся атрибутом `WithoutIncrementing`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutIncrementing;
use Illuminate\Database\Eloquent\Model;

#[WithoutIncrementing]
class Flight extends Model
{
    // ...
}
```

<a name="composite-primary-keys"></a>
#### «Складені» первинні ключі

Eloquent вимагає, щоб кожна модель мала щонайменше один унікальний «ID», який може служити первинним ключем. «Складені» первинні ключі моделі Eloquent не підтримують. Втім, ви вільні додавати до таблиць додаткові унікальні індекси з кількох стовпців - окрім самого первинного ключа, що унікально ідентифікує рядок.

<a name="uuid-and-ulid-keys"></a>
### Ключі UUID та ULID

Замість автоінкрементних цілих чисел як первинних ключів моделі Eloquent ви можете обрати UUID. UUID - це універсально унікальні буквенно-цифрові ідентифікатори довжиною 36 символів.

Якщо ви хочете, щоб модель використовувала ключ UUID замість автоінкрементного цілого, застосуйте до неї трейт `Illuminate\Database\Eloquent\Concerns\HasUuids`. Звісно, переконайтеся, що модель має [стовпець первинного ключа, еквівалентний UUID](/docs/{{version}}/migrations#column-method-uuid):

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "018f2b5c-6a7f-7b12-9d6f-2f8a4e0c9c11"
```

За замовчуванням трейт `HasUuids` генерує для ваших моделей ідентифікатори [UUIDv7](/docs/{{version}}/strings#method-str-uuid7). Такі UUID ефективніші для зберігання в проіндексованій базі, бо їх можна сортувати лексикографічно.

Ви можете перевизначити процес генерації UUID для конкретної моделі, описавши в ній метод `newUniqueId`. Крім того, методом `uniqueIds` можна вказати, які стовпці мають отримувати UUID:

```php
use Ramsey\Uuid\Uuid;

/**
 * Generate a new UUID for the model.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * Get the columns that should receive a unique identifier.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

За бажанням ви можете скористатися «ULID» замість UUID. ULID схожі на UUID, але мають довжину лише 26 символів. Як і впорядковані UUID, ULID сортуються лексикографічно, що дає ефективне індексування в базі. Щоб скористатися ULID, застосуйте до моделі трейт `Illuminate\Database\Eloquent\Concerns\HasUlids`. Також переконайтеся, що модель має [стовпець первинного ключа, еквівалентний ULID](/docs/{{version}}/migrations#column-method-ulid):

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a name="timestamps"></a>
### Часові позначки

За замовчуванням Eloquent очікує, що у відповідній таблиці моделі є стовпці `created_at` та `updated_at`. Eloquent автоматично задає їхні значення, коли модель створюється чи оновлюється. Якщо ви не хочете, щоб Eloquent керував цими стовпцями автоматично, задайте `timestamps` значення `false` в атрибуті `Table` вашої моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(timestamps: false)]
class Flight extends Model
{
    // ...
}
```

Якщо вам потрібно лише вимкнути часові позначки, скористайтеся атрибутом `WithoutTimestamps`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutTimestamps;
use Illuminate\Database\Eloquent\Model;

#[WithoutTimestamps]
class Flight extends Model
{
    // ...
}
```

Якщо вам потрібно змінити формат часових позначок моделі, скористайтеся аргументом `dateFormat` атрибута `Table`. Він визначає, як атрибути дати зберігаються в базі даних, а також їхній формат при серіалізації моделі в масив чи JSON:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

Якщо вам потрібно задати лише формат дати, скористайтеся атрибутом `DateFormat`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\DateFormat;
use Illuminate\Database\Eloquent\Model;

#[DateFormat('U')]
class Flight extends Model
{
    // ...
}
```

Якщо вам потрібно змінити назви стовпців для зберігання часових позначок, опишіть у моделі константи `CREATED_AT` та `UPDATED_AT`:

```php
<?php

class Flight extends Model
{
    /**
     * The name of the "created at" column.
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * The name of the "updated at" column.
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

Якщо ви хочете виконати операції з моделлю, не змінюючи її часову позначку `updated_at`, працюйте з моделлю в замиканні, переданому методу `withoutTimestamps`:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### Підключення до бази даних

За замовчуванням усі моделі Eloquent використовують підключення до бази даних, налаштоване для вашого застосунку за замовчуванням. Якщо ви хочете вказати інше підключення для роботи з конкретною моделлю, скористайтеся атрибутом `Connection`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Connection;
use Illuminate\Database\Eloquent\Model;

#[Connection('mysql')]
class Flight extends Model
{
    // ...
}
```

<a name="default-attribute-values"></a>
### Значення атрибутів за замовчуванням

За замовчуванням новостворений екземпляр моделі не містить жодних значень атрибутів. Якщо ви хочете задати значення за замовчуванням для деяких атрибутів моделі, опишіть у ній властивість `$attributes`. Значення в масиві `$attributes` мають бути в «сирому» форматі для зберігання - так, ніби їх щойно прочитали з бази даних:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The model's default values for attributes.
     *
     * @var array<string, mixed>
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```

<a name="configuring-eloquent-strictness"></a>
### Налаштування строгості Eloquent

Laravel має кілька методів, якими можна налаштувати поведінку та «строгість» Eloquent у різних ситуаціях.

По-перше, метод `preventLazyLoading` приймає необов'язковий булевий аргумент, що вказує, чи слід забороняти ліниве завантаження (lazy loading). Наприклад, ви можете вимкнути ліниве завантаження лише в непродакшн-середовищах, щоб продакшн і далі працював нормально, навіть якщо в код випадково потрапило ліниве завантаження зв'язку. Зазвичай цей метод викликають у методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

Також ви можете наказати Laravel викидати виняток при спробі заповнити атрибут, недоступний для заповнення, - для цього викличте метод `preventSilentlyDiscardingAttributes`. Це допомагає уникнути неочікуваних помилок під час локальної розробки, коли ви намагаєтеся задати атрибут, якого немає в масиві `fillable` моделі:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## Отримання моделей

Коли ви створили модель і [відповідну таблицю бази даних](/docs/{{version}}/migrations#generating-migrations), можна починати діставати дані з бази. Уявляйте кожну модель Eloquent як потужний [конструктор запитів](/docs/{{version}}/queries), що дозволяє плавно робити запити до пов'язаної з моделлю таблиці. Метод `all` моделі дістає всі записи з відповідної таблиці:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### Побудова запитів

Метод `all` в Eloquent повертає всі результати з таблиці моделі. Але оскільки кожна модель Eloquent є [конструктором запитів](/docs/{{version}}/queries), ви можете додати до запиту обмеження, а потім викликати метод `get`, щоб отримати результати:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Оскільки моделі Eloquent є конструкторами запитів, варто переглянути всі методи [конструктора запитів](/docs/{{version}}/queries) Laravel. Будь-який із них можна використовувати у своїх запитах Eloquent.

<a name="refreshing-models"></a>
#### Оновлення моделей

Якщо у вас уже є екземпляр моделі Eloquent, дістаний із бази даних, ви можете «оновити» його методами `fresh` і `refresh`. Метод `fresh` заново дістає модель із бази. Наявний екземпляр моделі при цьому не змінюється:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

Метод `refresh` наповнює наявний екземпляр свіжими даними з бази. Крім того, оновлюються й усі завантажені зв'язки:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### Колекції

Як ми бачили, методи Eloquent на кшталт `all` і `get` дістають із бази кілька записів. Проте вони повертають не звичайний PHP-масив, а екземпляр `Illuminate\Database\Eloquent\Collection`.

Клас `Collection` в Eloquent розширює базовий клас Laravel `Illuminate\Support\Collection`, який має [цілу низку корисних методів](/docs/{{version}}/collections#available-methods) для роботи з наборами даних. Наприклад, методом `reject` можна прибрати з колекції моделі за результатом виклику замикання:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Крім методів базового класу колекцій Laravel, клас колекції Eloquent має [кілька додаткових методів](/docs/{{version}}/eloquent-collections#available-methods), призначених саме для роботи з колекціями моделей Eloquent.

Оскільки всі колекції Laravel реалізують інтерфейси ітерування PHP, ви можете обходити колекції в циклі, наче масиви:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### Обробка результатів частинами

Якщо ви спробуєте завантажити десятки тисяч записів Eloquent методами `all` чи `get`, вашому застосунку може забракнути пам'яті. Замість них скористайтеся методом `chunk` - він опрацьовує велику кількість моделей ефективніше.

Метод `chunk` дістає підмножину моделей Eloquent і передає їх у замикання для обробки. Оскільки за раз дістається лише поточна частина моделей, метод `chunk` значно зменшує споживання пам'яті при роботі з великою кількістю моделей:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

Перший аргумент методу `chunk` - кількість записів, які ви хочете отримувати в кожній «частині». Замикання, передане другим аргументом, буде викликано для кожної частини, дістаної з бази. Щоб отримати кожну частину записів для замикання, виконується окремий запит до бази.

Якщо ви фільтруєте результати методу `chunk` за стовпцем, який заодно оновлюєте під час обходу, скористайтеся методом `chunkById`. Метод `chunk` у таких випадках може дати неочікувані й неузгоджені результати. Усередині метод `chunkById` завжди дістає моделі зі значенням стовпця `id`, більшим за останню модель попередньої частини:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

Оскільки методи `chunkById` і `lazyById` додають до запиту власні умови «where», свої умови варто [логічно згрупувати](/docs/{{version}}/queries#logical-grouping) в замиканні:

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) {
    $flights->each->update([
        'departed' => false,
        'cancelled' => true
    ]);
}, column: 'id');
```

<a name="chunking-using-lazy-collections"></a>
### Обробка частинами через ліниві колекції

Метод `lazy` працює схоже на [метод `chunk`](#chunking-results) у тому, що всередині виконує запит частинами. Але замість того щоб передавати кожну частину прямо в колбек, метод `lazy` повертає «розплющену» [LazyCollection](/docs/{{version}}/collections#lazy-collections) моделей Eloquent, і ви працюєте з результатами як з єдиним потоком:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

Якщо ви фільтруєте результати методу `lazy` за стовпцем, який заодно оновлюєте під час обходу, скористайтеся методом `lazyById`. Усередині метод `lazyById` завжди дістає моделі зі значенням стовпця `id`, більшим за останню модель попередньої частини:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

Ви можете фільтрувати результати за спаданням `id` методом `lazyByIdDesc`.

<a name="cursors"></a>
### Курсори

Як і метод `lazy`, метод `cursor` значно зменшує споживання пам'яті вашим застосунком, коли ви обходите десятки тисяч записів моделей Eloquent.

Метод `cursor` виконує лише один запит до бази даних; проте окремі моделі Eloquent не наповнюються даними, аж поки ви до них не дійдете в обході. Тому в будь-який момент обходу курсора в пам'яті тримається лише одна модель Eloquent.

> [!WARNING]
> Оскільки метод `cursor` тримає в пам'яті лише одну модель Eloquent за раз, він не може жадібно завантажувати зв'язки. Якщо вам потрібне жадібне завантаження, розгляньте [метод `lazy`](#chunking-using-lazy-collections).

Усередині метод `cursor` реалізує це через [генератори](https://www.php.net/manual/en/language.generators.overview.php) PHP:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor` повертає екземпляр `Illuminate\Support\LazyCollection`. [Ліниві колекції](/docs/{{version}}/collections#lazy-collections) дозволяють користуватися багатьма методами звичайних колекцій Laravel, тримаючи в пам'яті лише одну модель за раз:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

Хоч метод `cursor` споживає значно менше пам'яті, ніж звичайний запит (бо тримає в пам'яті лише одну модель Eloquent за раз), пам'ять усе одно колись закінчиться. Причина в тому, що [драйвер PDO у PHP усередині кешує всі сирі результати запиту у своєму буфері](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). Якщо ви маєте справу з дуже великою кількістю записів Eloquent, розгляньте [метод `lazy`](#chunking-using-lazy-collections).

<a name="advanced-subqueries"></a>
### Складніші підзапити

<a name="subquery-selects"></a>
#### Підзапити у SELECT

Eloquent також має розширену підтримку підзапитів, яка дозволяє дістати інформацію з пов'язаних таблиць одним запитом. Наприклад, уявімо, що ми маємо таблицю напрямків рейсів `destinations` і таблицю рейсів `flights` до цих напрямків. Таблиця `flights` містить стовпець `arrived_at`, що вказує, коли рейс прибув у пункт призначення.

За допомогою підзапитів у методах `select` і `addSelect` конструктора запитів ми можемо одним запитом вибрати всі `destinations` і назву рейсу, який прибув у цей пункт останнім:

```php
use App\Models\Destination;
use App\Models\Flight;

return Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```

<a name="subquery-ordering"></a>
#### Сортування за підзапитом

Крім того, функція `orderBy` конструктора запитів підтримує підзапити. Продовжуючи приклад із рейсами, ми можемо відсортувати всі напрямки за часом прибуття останнього рейсу до кожного з них. І знову ж таки, це робиться одним запитом до бази:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## Отримання окремих моделей та агрегатів

Крім отримання всіх записів, що відповідають запиту, ви можете дістати окремі записи методами `find`, `first` або `firstWhere`. Замість колекції моделей вони повертають один екземпляр моделі:

```php
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```

Іноді ви хочете виконати якусь іншу дію, якщо результатів не знайдено. Методи `findOr` і `firstOr` повертають один екземпляр моделі або, якщо результатів немає, виконують задане замикання. Значення, яке повернуло замикання, стане результатом методу:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Винятки «не знайдено»

Іноді ви хочете викинути виняток, якщо модель не знайдено. Це особливо зручно в маршрутах і контролерах. Методи `findOrFail` і `firstOrFail` дістають перший результат запиту; але якщо результату немає, буде викинуто `Illuminate\Database\Eloquent\ModelNotFoundException`:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

Якщо `ModelNotFoundException` не перехоплено, клієнту автоматично надсилається HTTP-відповідь 404:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### Отримання або створення моделей

Метод `firstOrCreate` спробує знайти запис у базі за заданими парами «стовпець - значення». Якщо моделі в базі немає, буде вставлено запис з атрибутами, які утворюються об'єднанням першого масиву-аргументу з необов'язковим другим.

Метод `firstOrNew`, як і `firstOrCreate`, спробує знайти в базі запис, що відповідає заданим атрибутам. Але якщо моделі не знайдено, буде повернуто новий екземпляр моделі. Зверніть увагу: модель, яку повернув `firstOrNew`, ще не збережена в базі. Щоб зберегти її, потрібно вручну викликати метод `save`:

```php
use App\Models\Flight;

// Retrieve flight by name or create it if it doesn't exist...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or create it with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// Retrieve flight by name or instantiate a new Flight instance...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or instantiate with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### Отримання агрегатів

Працюючи з моделями Eloquent, ви можете також користуватися методами `count`, `sum`, `max` та іншими [агрегатними методами](/docs/{{version}}/queries#aggregates) [конструктора запитів](/docs/{{version}}/queries) Laravel. Як і слід очікувати, вони повертають скалярне значення, а не екземпляр моделі Eloquent:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## Вставка та оновлення моделей

<a name="inserts"></a>
### Вставка

Звісно, працюючи з Eloquent, ми не лише дістаємо моделі з бази - нам потрібно вставляти й нові записи. На щастя, Eloquent робить це просто. Щоб вставити новий запис, створіть екземпляр моделі й задайте йому атрибути. Далі викличте на екземплярі метод `save`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

У цьому прикладі ми присвоюємо поле `name` із вхідного HTTP-запиту атрибуту `name` екземпляра моделі `App\Models\Flight`. Коли ми викликаємо метод `save`, у базу даних вставляється запис. Часові позначки `created_at` та `updated_at` буде задано автоматично при виклику `save`, тож задавати їх вручну не потрібно.

Якщо ви хочете зберегти модель у межах транзакції, скористайтеся методом `saveOrFail`. Якщо під час збереження буде викинуто виняток, транзакція автоматично відкотиться:

```php
$flight->saveOrFail();
```

Або ж ви можете скористатися методом `create`, щоб «зберегти» нову модель однією PHP-інструкцією. Метод `create` поверне вам вставлений екземпляр моделі:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

Проте, перш ніж користуватися методом `create`, вам потрібно задати в класі моделі атрибут `Fillable` або `Guarded`. Ці атрибути обов'язкові, бо всі моделі Eloquent за замовчуванням захищені від вразливостей масового призначення. Детальніше про це читайте в [документації з масового призначення](#mass-assignment).

<a name="updates"></a>
### Оновлення

Методом `save` можна оновлювати й моделі, які вже є в базі даних. Щоб оновити модель, дістаньте її та задайте атрибути, які хочете змінити. Далі викличте метод `save`. І знову ж таки, часову позначку `updated_at` буде оновлено автоматично, тож задавати її вручну не потрібно:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

Якщо ви хочете оновити модель у межах транзакції, скористайтеся методом `updateOrFail`. Якщо під час оновлення буде викинуто виняток, транзакція автоматично відкотиться:

```php
$flight->updateOrFail(['name' => 'Paris to London']);
```

Іноді вам потрібно оновити наявну модель або створити нову, якщо відповідної немає. Як і `firstOrCreate`, метод `updateOrCreate` зберігає модель, тож викликати `save` вручну не потрібно.

У прикладі нижче, якщо існує рейс із пунктом відправлення `Oakland` і пунктом призначення `San Diego`, буде оновлено його стовпці `price` та `discounted`. Якщо такого рейсу немає, буде створено новий з атрибутами, які утворюються об'єднанням першого масиву-аргументу з другим:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

Користуючись методами на кшталт `firstOrCreate` чи `updateOrCreate`, ви можете не знати, чи створено нову модель, чи оновлено наявну. Властивість `wasRecentlyCreated` вказує, чи була модель створена протягом її поточного життєвого циклу:

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // New flight record was inserted...
}
```

<a name="mass-updates"></a>
#### Масові оновлення

Оновлення можна виконувати й над моделями, що відповідають заданому запиту. У цьому прикладі всі рейси, що є `active` і мають `destination` зі значенням `San Diego`, буде позначено як затримані:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

Метод `update` очікує масив пар «стовпець - значення», які вказують, що саме оновити. Метод `update` повертає кількість зачеплених рядків.

> [!WARNING]
> Коли ви робите масове оновлення через Eloquent, події моделі `saving`, `saved`, `updating` та `updated` для оновлених моделей не спрацюють. Причина в тому, що при масовому оновленні моделі насправді ніколи не дістаються з бази.

<a name="examining-attribute-changes"></a>
#### Перевірка змін атрибутів

Eloquent має методи `isDirty`, `isClean` і `wasChanged`, щоб перевірити внутрішній стан моделі й визначити, як змінилися її атрибути з моменту, коли модель дістали з бази.

Метод `isDirty` визначає, чи змінився хоч якийсь атрибут моделі відтоді, як її дістали. Ви можете передати `isDirty` назву конкретного атрибута або масив атрибутів, щоб перевірити, чи є серед них «брудні». Метод `isClean` визначає, чи лишився атрибут незмінним відтоді, як модель дістали. Він теж приймає необов'язковий аргумент-атрибут:

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty(); // true
$user->isDirty('title'); // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true
$user->isClean(['first_name', 'title']); // false

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```

Метод `wasChanged` визначає, чи змінювалися атрибути при останньому збереженні моделі в межах поточного циклу запиту. За потреби ви можете передати назву атрибута, щоб перевірити, чи змінився саме він:

```php
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
$user->wasChanged(['title', 'slug']); // true
$user->wasChanged('first_name'); // false
$user->wasChanged(['first_name', 'title']); // true
```

Метод `getOriginal` повертає масив із початковими атрибутами моделі незалежно від того, як вона змінилася відтоді, як її дістали. За потреби ви можете передати назву конкретного атрибута, щоб отримати його початкове значення:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```

Метод `getChanges` повертає масив атрибутів, які змінилися при останньому збереженні моделі, а метод `getPrevious` - масив значень атрибутів, які були до останнього збереження:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->update([
    'name' => 'Jack',
    'email' => 'jack@example.com',
]);

$user->getChanges();

/*
    [
        'name' => 'Jack',
        'email' => 'jack@example.com',
    ]
*/

$user->getPrevious();

/*
    [
        'name' => 'John',
        'email' => 'john@example.com',
    ]
*/
```

<a name="mass-assignment"></a>
### Масове призначення

Ви можете скористатися методом `create`, щоб «зберегти» нову модель однією PHP-інструкцією. Метод поверне вам вставлений екземпляр моделі:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

Проте, перш ніж користуватися методом `create`, вам потрібно задати в класі моделі атрибут `Fillable` або `Guarded`. Ці атрибути обов'язкові, бо всі моделі Eloquent за замовчуванням захищені від вразливостей масового призначення.

Вразливість масового призначення виникає, коли користувач передає неочікуване поле HTTP-запиту, і це поле змінює стовпець вашої бази даних, якого ви не очікували. Наприклад, зловмисник може надіслати в HTTP-запиті параметр `is_admin`, який потім потрапляє в метод `create` вашої моделі й дозволяє йому підвищити собі права до адміністратора.

Отже, для початку вам слід описати, які атрибути моделі мають бути доступні для масового призначення. Це робиться атрибутом `Fillable` на моделі. Наприклад, зробімо атрибут `name` нашої моделі `Flight` доступним для масового призначення:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['name'])]
class Flight extends Model
{
    // ...
}
```

Коли ви вказали, які атрибути доступні для масового призначення, можна вставляти новий запис у базу методом `create`. Метод `create` повертає щойно створений екземпляр моделі:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

Якщо у вас уже є екземпляр моделі, ви можете наповнити його масивом атрибутів методом `fill`:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### Масове призначення та стовпці JSON

Присвоюючи стовпці JSON, кожен ключ, доступний для масового призначення, потрібно вказати в атрибуті `Fillable` вашої моделі. З міркувань безпеки Laravel не підтримує оновлення вкладених атрибутів JSON при використанні атрибута `Guarded`:

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```

<a name="allowing-mass-assignment"></a>
#### Дозвіл масового призначення

Якщо ви хочете зробити доступними для масового призначення всі атрибути, скористайтеся на моделі атрибутом `Unguarded`. Якщо ви знімаєте захист із моделі, будьте особливо уважні: масиви, які передаються методам `fill`, `create` та `update` Eloquent, завжди складайте вручну:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Unguarded;
use Illuminate\Database\Eloquent\Model;

#[Unguarded]
class Flight extends Model
{
    // ...
}
```

<a name="mass-assignment-exceptions"></a>
#### Винятки при масовому призначенні

За замовчуванням атрибути, яких немає в атрибуті `Fillable`, під час масового призначення мовчки відкидаються. На продакшні це очікувана поведінка, але під час локальної розробки вона може спантеличити: незрозуміло, чому зміни моделі не застосовуються.

За бажанням ви можете наказати Laravel викидати виняток при спробі заповнити атрибут, недоступний для заповнення, - для цього викличте метод `preventSilentlyDiscardingAttributes`. Зазвичай цей метод викликають у методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upsert

Метод `upsert` в Eloquent оновлює або створює записи однією атомарною операцією. Перший аргумент методу - значення для вставки чи оновлення, другий - стовпці, які унікально ідентифікують записи у відповідній таблиці. Третій і останній аргумент - масив стовпців, які слід оновити, якщо відповідний запис у базі вже є. Метод `upsert` автоматично задасть часові позначки `created_at` і `updated_at`, якщо вони увімкнені на моделі:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> Усі бази даних, окрім SQL Server, вимагають, щоб стовпці з другого аргументу методу `upsert` мали індекс «primary» або «unique». Крім того, драйвери MariaDB і MySQL ігнорують другий аргумент `upsert` і завжди використовують індекси «primary» та «unique» таблиці, щоб виявити наявні записи.

<a name="deleting-models"></a>
## Видалення моделей

Щоб видалити модель, викличте на її екземплярі метод `delete`:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

Якщо ви хочете видалити модель у межах транзакції, скористайтеся методом `deleteOrFail`. Якщо під час видалення буде викинуто виняток, транзакція автоматично відкотиться:

```php
$flight->deleteOrFail();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### Видалення наявної моделі за первинним ключем

У прикладі вище ми дістаємо модель із бази, перш ніж викликати метод `delete`. Але якщо ви знаєте первинний ключ моделі, її можна видалити, не дістаючи явно, - методом `destroy`. Крім одного первинного ключа, метод `destroy` приймає кілька первинних ключів, масив первинних ключів або [колекцію](/docs/{{version}}/collections) первинних ключів:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

Якщо ви користуєтеся [м'яким видаленням моделей](#soft-deleting), ви можете видалити моделі назавжди методом `forceDestroy`:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> Метод `destroy` завантажує кожну модель окремо й викликає метод `delete`, щоб події `deleting` та `deleted` коректно надсилалися для кожної моделі.

<a name="deleting-models-using-queries"></a>
#### Видалення моделей запитами

Звісно, ви можете побудувати запит Eloquent, щоб видалити всі моделі, що відповідають його умовам. У цьому прикладі ми видалимо всі рейси, позначені як неактивні. Як і масові оновлення, масові видалення не надсилають подій моделі для видалених моделей:

```php
$deleted = Flight::where('active', 0)->delete();
```

Щоб видалити всі моделі в таблиці, виконайте запит без жодних умов:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Коли ви виконуєте масове видалення через Eloquent, події моделі `deleting` та `deleted` для видалених моделей не надсилаються. Причина в тому, що при виконанні запиту на видалення моделі насправді ніколи не дістаються з бази.

<a name="soft-deleting"></a>
### М'яке видалення

Крім справжнього видалення записів із бази даних, Eloquent уміє «м'яко видаляти» моделі (soft delete). Коли модель видалено м'яко, вона насправді лишається в базі. Натомість їй задається атрибут `deleted_at` з датою й часом «видалення». Щоб увімкнути м'яке видалення для моделі, додайте до неї трейт `Illuminate\Database\Eloquent\SoftDeletes`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model
{
    use SoftDeletes;
}
```

> [!NOTE]
> Трейт `SoftDeletes` автоматично приведе атрибут `deleted_at` до екземпляра `DateTime` / `Carbon`.

Вам також слід додати до таблиці стовпець `deleted_at`. [Конструктор схеми](/docs/{{version}}/migrations) Laravel має для цього допоміжний метод:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```

Тепер, коли ви викликаєте на моделі метод `delete`, стовпцю `deleted_at` буде задано поточну дату й час. Проте запис моделі лишиться в таблиці. Коли ви робите запит до моделі з м'яким видаленням, м'яко видалені моделі автоматично виключаються з усіх результатів.

Щоб визначити, чи був конкретний екземпляр моделі м'яко видалений, скористайтеся методом `trashed`:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### Відновлення м'яко видалених моделей

Іноді вам потрібно «скасувати видалення» м'яко видаленої моделі. Щоб відновити її, викличте на екземплярі моделі метод `restore`. Метод `restore` задасть стовпцю `deleted_at` значення `null`:

```php
$flight->restore();
```

Метод `restore` можна використати й у запиті, щоб відновити кілька моделей. І знову ж таки, як і інші «масові» операції, це не надішле жодних подій моделі для відновлених моделей:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

Метод `restore` можна також використовувати при побудові запитів до [зв'язків](/docs/{{version}}/eloquent-relationships):

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### Остаточне видалення моделей

Іноді вам потрібно справді прибрати модель із бази даних. Щоб назавжди видалити м'яко видалену модель із таблиці, скористайтеся методом `forceDelete`:

```php
$flight->forceDelete();
```

Метод `forceDelete` можна також використовувати при побудові запитів до зв'язків Eloquent:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### Запити до м'яко видалених моделей

<a name="including-soft-deleted-models"></a>
#### Включення м'яко видалених моделей

Як зазначено вище, м'яко видалені моделі автоматично виключаються з результатів запитів. Втім, ви можете примусово включити їх до результатів, викликавши на запиті метод `withTrashed`:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

Метод `withTrashed` можна викликати й при побудові запиту до [зв'язку](/docs/{{version}}/eloquent-relationships):

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### Отримання лише м'яко видалених моделей

Метод `onlyTrashed` дістане **лише** м'яко видалені моделі:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## Очищення моделей

Іноді вам потрібно періодично видаляти моделі, які більше не потрібні. Для цього додайте до таких моделей трейт `Illuminate\Database\Eloquent\Prunable` або `Illuminate\Database\Eloquent\MassPrunable`. Після цього реалізуйте метод `prunable`, що повертає конструктор запитів Eloquent, який відбирає непотрібні моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

Позначаючи моделі як `Prunable`, ви можете також описати в моделі метод `pruning`. Його буде викликано перед видаленням моделі. Це стане в пригоді, щоб видалити пов'язані з моделлю додаткові ресурси - наприклад, збережені файли, - перш ніж модель назавжди зникне з бази:

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```

Налаштувавши модель для очищення, заплануйте artisan-команду `model:prune` у файлі `routes/console.php` вашого застосунку. Ви вільні обрати доречний інтервал запуску цієї команди:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

Усередині команда `model:prune` автоматично знаходить моделі «Prunable» у каталозі `app/Models` вашого застосунку. Якщо ваші моделі лежать деінде, вкажіть назви класів опцією `--model`:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

Якщо ви хочете виключити певні моделі з очищення, а решту знайдених очищати, скористайтеся опцією `--except`:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

Перевірити свій запит `prunable` можна, виконавши команду `model:prune` з опцією `--pretend`. У цьому режимі команда `model:prune` просто повідомить, скільки записів було б видалено, якби вона справді відпрацювала:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> Моделі з м'яким видаленням буде видалено назавжди (`forceDelete`), якщо вони відповідають запиту очищення.

<a name="mass-pruning"></a>
#### Масове очищення

Коли моделі позначені трейтом `Illuminate\Database\Eloquent\MassPrunable`, вони видаляються з бази запитами масового видалення. Тому метод `pruning` не буде викликано, а події моделі `deleting` та `deleted` не надішлються. Причина в тому, що моделі насправді ніколи не дістаються перед видаленням, і саме тому очищення відбувається значно ефективніше:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## Копіювання моделей

Ви можете створити незбережену копію наявного екземпляра моделі методом `replicate`. Це особливо зручно, коли у вас є моделі, що мають багато однакових атрибутів:

```php
use App\Models\Address;

$shipping = Address::create([
    'type' => 'shipping',
    'line_1' => '123 Example Street',
    'city' => 'Victorville',
    'state' => 'CA',
    'postcode' => '90001',
]);

$billing = $shipping->replicate()->fill([
    'type' => 'billing'
]);

$billing->save();
```

Щоб виключити один чи кілька атрибутів із копіювання в нову модель, передайте методу `replicate` масив:

```php
$flight = Flight::create([
    'destination' => 'LAX',
    'origin' => 'LHR',
    'last_flown' => '2020-03-04 11:00:00',
    'last_pilot_id' => 747,
]);

$flight = $flight->replicate([
    'last_flown',
    'last_pilot_id'
]);
```

<a name="query-scopes"></a>
## Скопи запитів

<a name="global-scopes"></a>
### Глобальні скопи

Глобальні скопи (global scope) дозволяють додати обмеження до всіх запитів певної моделі. Власна функція [м'якого видалення](#soft-deleting) в Laravel користується глобальними скопами, щоб діставати з бази лише «невидалені» моделі. Власні глобальні скопи дають зручний і простий спосіб гарантувати, що кожен запит до певної моделі отримає потрібні обмеження.

<a name="generating-scopes"></a>
#### Створення скопів

Щоб згенерувати новий глобальний скоп, викличте artisan-команду `make:scope` - вона покладе згенерований скоп у каталог `app/Models/Scopes` вашого застосунку:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### Написання глобальних скопів

Написати глобальний скоп просто. Спершу командою `make:scope` згенеруйте клас, що реалізує інтерфейс `Illuminate\Database\Eloquent\Scope`. Інтерфейс `Scope` вимагає реалізувати один метод - `apply`. Метод `apply` може додавати до запиту обмеження `where` чи інші потрібні вирази:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> Якщо ваш глобальний скоп додає стовпці до виразу select запиту, користуйтеся методом `addSelect`, а не `select`. Так ви не заміните ненавмисно наявний вираз select запиту.

<a name="applying-global-scopes"></a>
#### Застосування глобальних скопів

Щоб призначити моделі глобальний скоп, просто поставте на ній атрибут `ScopedBy`:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy([AncientScope::class])]
class User extends Model
{
    //
}
```

Або ж ви можете зареєструвати глобальний скоп вручну, перевизначивши метод `booted` моделі й викликавши метод `addGlobalScope`. Метод `addGlobalScope` приймає єдиний аргумент - екземпляр вашого скопа:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

Після додавання скопа з прикладу вище до моделі `App\Models\User` виклик методу `User::all()` виконає такий SQL-запит:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### Анонімні глобальні скопи

Eloquent дозволяє також описувати глобальні скопи замиканнями - це особливо зручно для простих скопів, яким не потрібен окремий клас. Описуючи глобальний скоп замиканням, передайте першим аргументом методу `addGlobalScope` назву скопа на власний розсуд:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->minus(years: 2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### Прибирання глобальних скопів

Якщо ви хочете прибрати глобальний скоп для конкретного запиту, скористайтеся методом `withoutGlobalScope`. Він приймає єдиний аргумент - назву класу глобального скопа:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

Або, якщо ви описали глобальний скоп замиканням, передайте рядкову назву, яку йому призначили:

```php
User::withoutGlobalScope('ancient')->get();
```

Якщо ви хочете прибрати кілька або навіть усі глобальні скопи запиту, скористайтеся методами `withoutGlobalScopes` та `withoutGlobalScopesExcept`:

```php
// Remove all of the global scopes...
User::withoutGlobalScopes()->get();

// Remove some of the global scopes...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// Remove all global scopes except the given ones...
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### Локальні скопи

Локальні скопи дозволяють описати типові набори обмежень запиту, які легко перевикористовувати в усьому застосунку. Наприклад, вам може часто знадобитися діставати всіх користувачів, що вважаються «популярними». Щоб описати скоп, додайте до методу Eloquent атрибут `Scope`.

Скопи завжди мають повертати той самий екземпляр конструктора запитів або `void`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include popular users.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * Scope a query to only include active users.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### Використання локального скопа

Коли скоп описано, ви можете викликати його методи, роблячи запити до моделі. Виклики різних скопів можна навіть зчіплювати ланцюжком:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

Поєднання кількох скопів моделі Eloquent через оператор `or` може потребувати замикань, щоб досягти правильного [логічного групування](/docs/{{version}}/queries#logical-grouping):

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

Але оскільки це громіздко, Laravel має метод `orWhere` «вищого порядку», який дозволяє плавно зчіплювати скопи без замикань:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### Динамічні скопи

Іноді вам потрібен скоп, що приймає параметри. Для цього просто додайте свої додаткові параметри до сигнатури методу скопа. Параметри скопа описуються після параметра `$query`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include users of a given type.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

Коли ви додали очікувані аргументи до сигнатури методу скопа, їх можна передавати при виклику скопа:

```php
$users = User::ofType('admin')->get();
```

Методи скопів з атрибутом мають бути `protected`. Викликаючи такий скоп зсередини класу моделі, робіть це через екземпляр конструктора запитів - наприклад, `static::query()->ofType('admin')`, - щоб виклик пройшов через механізм обробки скопів Eloquent.

<a name="pending-attributes"></a>
### Відкладені атрибути

Якщо ви хочете створювати скопами моделі з тими самими атрибутами, які цей скоп використовує як обмеження, скористайтеся методом `withAttributes` при побудові запиту скопа:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Scope the query to only include drafts.
     */
    #[Scope]
    protected function draft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

Метод `withAttributes` додасть до запиту умови `where` із заданими атрибутами, а також задасть ці атрибути будь-яким моделям, створеним через цей скоп:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

Щоб метод `withAttributes` не додавав до запиту умов `where`, задайте аргументу `asConditions` значення `false`:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## Порівняння моделей

Іноді вам потрібно визначити, чи є дві моделі «однаковими». Методи `is` та `isNot` швидко перевіряють, чи мають дві моделі однакові первинний ключ, таблицю й підключення до бази даних:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

Методи `is` та `isNot` доступні також при роботі зі [зв'язками](/docs/{{version}}/eloquent-relationships) `belongsTo`, `hasOne`, `morphTo` і `morphOne`. Це особливо зручно, коли ви хочете порівняти пов'язану модель, не виконуючи запиту для її отримання:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## Події

> [!NOTE]
> Хочете транслювати події Eloquent прямо до клієнтської частини застосунку? Погляньте на [бродкастинг подій моделей](/docs/{{version}}/broadcasting#model-broadcasting) у Laravel.

Моделі Eloquent надсилають кілька подій, що дозволяють вклинитися в такі моменти життєвого циклу моделі: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored` і `replicating`.

Подія `retrieved` надсилається, коли наявну модель дістають із бази даних. Коли нову модель зберігають уперше, надсилаються події `creating` та `created`. Події `updating` / `updated` надсилаються, коли наявну модель змінюють і викликають метод `save`. Події `saving` / `saved` надсилаються, коли модель створюють або оновлюють - навіть якщо атрибути моделі не змінилися. Назви подій, що закінчуються на `-ing`, надсилаються до того, як зміни моделі збережено, а ті, що закінчуються на `-ed`, - після збереження змін.

Щоб почати слухати події моделі, опишіть у моделі Eloquent властивість `$dispatchesEvents`. Вона зіставляє різні моменти життєвого циклу моделі з вашими власними [класами подій](/docs/{{version}}/events). Кожен клас події моделі має очікувати екземпляр відповідної моделі у своєму конструкторі:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The event map for the model.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Описавши та зіставивши події Eloquent, ви можете обробляти їх [слухачами подій](/docs/{{version}}/events#defining-listeners).

> [!WARNING]
> Коли ви виконуєте масове оновлення чи видалення через Eloquent, події моделі `saved`, `updated`, `deleting` та `deleted` для зачеплених моделей не надсилаються. Причина в тому, що при масових оновленнях чи видаленнях моделі насправді ніколи не дістаються з бази.

<a name="events-using-closures"></a>
### Використання замикань

Замість власних класів подій ви можете зареєструвати замикання, які виконуються при надсиланні різних подій моделі. Зазвичай ці замикання реєструють у методі `booted` вашої моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

За потреби, реєструючи події моделі, ви можете скористатися [анонімними слухачами подій, які можна ставити в чергу](/docs/{{version}}/events#queueable-anonymous-event-listeners). Так ви накажете Laravel виконувати слухача події моделі у фоні через [чергу](/docs/{{version}}/queues) вашого застосунку:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### Спостерігачі

<a name="defining-observers"></a>
#### Опис спостерігачів

Якщо ви слухаєте багато подій певної моделі, ви можете згрупувати всіх слухачів в одному класі-спостерігачі. Назви методів класу спостерігача відповідають подіям Eloquent, які ви хочете слухати. Кожен такий метод отримує єдиний аргумент - відповідну модель. Найпростіше створити новий клас спостерігача artisan-командою `make:observer`:

```shell
php artisan make:observer UserObserver --model=User
```

Ця команда покладе нового спостерігача в каталог `app/Observers`. Якщо каталогу немає, Artisan створить його за вас. Ваш новий спостерігач виглядатиме так:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "updated" event.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "deleted" event.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "restored" event.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "forceDeleted" event.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

Щоб зареєструвати спостерігача, поставте на відповідній моделі атрибут `ObservedBy`:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

Або ж ви можете зареєструвати спостерігача вручну, викликавши метод `observe` на моделі, за якою хочете спостерігати. Реєструвати спостерігачів можна в методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> Спостерігач може слухати й додаткові події - наприклад, `saving` і `retrieved`. Ці події описано в документації з [подій](#events).

<a name="observers-and-database-transactions"></a>
#### Спостерігачі та транзакції

Коли моделі створюються в межах транзакції, ви можете захотіти, щоб спостерігач виконував свої обробники подій лише після коміту транзакції. Для цього реалізуйте у спостерігачі інтерфейс `ShouldHandleEventsAfterCommit`. Якщо транзакції немає, обробники подій виконаються негайно:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### Вимкнення подій

Іноді вам потрібно тимчасово «вимкнути» всі події, які надсилає модель. Це робиться методом `withoutEvents`. Метод `withoutEvents` приймає єдиний аргумент - замикання. Будь-який код, виконаний у цьому замиканні, не надсилатиме подій моделі, а значення, яке поверне замикання, поверне й метод `withoutEvents`:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### Збереження однієї моделі без подій

Іноді ви хочете «зберегти» певну модель, не надсилаючи жодних подій. Це робиться методом `saveQuietly`:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

Ви можете також «оновити», «видалити», «м'яко видалити», «відновити» та «скопіювати» модель без надсилання подій:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
