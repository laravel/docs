---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Кеш

- [Вступ](#introduction)
- [Конфігурація](#configuration)
    - [Передумови драйверів](#driver-prerequisites)
- [Використання кешу](#cache-usage)
    - [Отримання екземпляра кешу](#obtaining-a-cache-instance)
    - [Отримання елементів із кешу](#retrieving-items-from-the-cache)
    - [Збереження елементів у кеші](#storing-items-in-the-cache)
    - [Продовження часу життя елемента](#extending-item-lifetime)
    - [Видалення елементів із кешу](#removing-items-from-the-cache)
    - [Мемоізація кешу](#cache-memoization)
    - [Хелпер кешу](#the-cache-helper)
- [Теги кешу](#cache-tags)
- [Атомарні блокування](#atomic-locks)
    - [Керування блокуваннями](#managing-locks)
    - [Керування блокуваннями між процесами](#managing-locks-across-processes)
    - [Оновлення блокувань](#refreshing-locks)
    - [Обмеження паралельності](#concurrency-limiting)
- [Резервування кешу](#cache-failover)
- [Додавання власних драйверів кешу](#adding-custom-cache-drivers)
    - [Написання драйвера](#writing-the-driver)
    - [Реєстрація драйвера](#registering-the-driver)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Деякі завдання з отримання чи обробки даних у вашому застосунку можуть інтенсивно навантажувати процесор або тривати кілька секунд. У такому разі отримані дані зазвичай кешують на певний час, щоб швидко віддавати їх на наступні запити тих самих даних. Закешовані дані зазвичай зберігають у дуже швидкому сховищі на кшталт [Memcached](https://memcached.org) чи [Redis](https://redis.io).

На щастя, Laravel надає виразний уніфікований API для різних бекендів кешу, що дозволяє скористатися їхньою блискавичною швидкістю та пришвидшити ваш веб-застосунок.

<a name="configuration"></a>
## Конфігурація

Конфігураційний файл кешу вашого застосунку розташовано за шляхом `config/cache.php`. У ньому ви можете вказати, яке сховище кешу використовуватиметься за замовчуванням у всьому застосунку. Laravel одразу підтримує популярні бекенди кешування: [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), реляційні бази даних і диски файлової системи. Крім того, доступний файловий драйвер кешу, а драйвери `array` і `null` дають зручні бекенди для ваших автоматизованих тестів.

Конфігураційний файл кешу містить і низку інших опцій, які варто переглянути. За замовчуванням Laravel налаштовано на драйвер кешу `database`, що зберігає серіалізовані закешовані об'єкти в базі даних вашого застосунку.

<a name="driver-prerequisites"></a>
### Передумови драйверів

<a name="prerequisites-database"></a>
#### База даних

Використовуючи драйвер кешу `database`, вам знадобиться таблиця бази даних для зберігання даних кешу. Зазвичай її створює типова [міграція](/docs/{{version}}/migrations) Laravel `0001_01_01_000001_create_cache_table.php`; однак якщо ваш застосунок не містить цієї міграції, ви можете створити її командою Artisan `make:cache-table`:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Використання драйвера Memcached потребує встановленого [пакета Memcached PECL](https://pecl.php.net/package/memcached). Ви можете перелічити всі свої сервери Memcached у конфігураційному файлі `config/cache.php`. Цей файл уже містить запис `memcached.servers`, щоб ви могли почати:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

За потреби ви можете задати опції `host` шлях до UNIX-сокета. Якщо ви це зробите, опції `port` слід задати значення `0`:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```

<a name="redis"></a>
#### Redis

Перш ніж використовувати кеш Redis із Laravel, вам потрібно встановити PHP-розширення PhpRedis через PECL або пакет `predis/predis` через Composer. [Laravel Sail](/docs/{{version}}/sail) уже містить це розширення. Крім того, офіційні платформи для застосунків Laravel - як-от [Laravel Cloud](https://cloud.laravel.com) і [Laravel Forge](https://forge.laravel.com) - мають PhpRedis встановленим за замовчуванням.

Докладніше про налаштування Redis читайте на [сторінці документації Laravel](/docs/{{version}}/redis#configuration).

<a name="storage"></a>
#### Storage

Драйвер кешу `storage` дозволяє зберігати закешовані значення на будь-якому налаштованому [диску файлової системи](/docs/{{version}}/filesystem). Це може бути корисно, коли ви хочете використати наявний диск - наприклад, диск S3 - як сховище кешу «ключ-значення»:

```php
'storage' => [
    'driver' => 'storage',
    'disk' => env('CACHE_STORAGE_DISK'),
    'path' => env('CACHE_STORAGE_PATH', 'framework/cache/data'),
],
```

<a name="dynamodb"></a>
#### DynamoDB

Перш ніж використовувати драйвер кешу [DynamoDB](https://aws.amazon.com/dynamodb), вам потрібно створити таблицю DynamoDB для зберігання всіх закешованих даних. Зазвичай її називають `cache`. Утім, ім'я таблиці слід обирати відповідно до значення конфігурації `stores.dynamodb.table` у файлі `cache`. Ім'я таблиці можна також задати змінною середовища `DYNAMODB_CACHE_TABLE`.

Ця таблиця також має мати рядковий ключ розділу з іменем, що відповідає значенню конфігурації `stores.dynamodb.attributes.key` у файлі `cache` вашого застосунку. За замовчуванням ключ розділу має називатися `key`.

Зазвичай DynamoDB не вилучає з таблиці елементи, термін дії яких сплив. Тому вам слід [увімкнути Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) для таблиці. Налаштовуючи TTL, задайте ім'я атрибута TTL як `expires_at`.

Далі встановіть AWS SDK, щоб ваш застосунок Laravel міг спілкуватися з DynamoDB:

```shell
composer require aws/aws-sdk-php
```

Крім того, переконайтеся, що для опцій конфігурації сховища кешу DynamoDB надано значення. Зазвичай ці опції - як-от `AWS_ACCESS_KEY_ID` та `AWS_SECRET_ACCESS_KEY` - визначають у файлі `.env` вашого застосунку:

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```

<a name="mongodb"></a>
#### MongoDB

Якщо ви використовуєте MongoDB, драйвер кешу `mongodb` надає офіційний пакет `mongodb/laravel-mongodb`, і його можна налаштувати через підключення до бази даних `mongodb`. MongoDB підтримує TTL-індекси, якими можна автоматично очищати застарілі елементи кешу.

Докладніше про налаштування MongoDB читайте в [документації MongoDB щодо кешу та блокувань](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/).

<a name="cache-usage"></a>
## Використання кешу

<a name="obtaining-a-cache-instance"></a>
### Отримання екземпляра кешу

Щоб отримати екземпляр сховища кешу, скористайтеся фасадом `Cache` - саме його ми використовуватимемо в цій документації. Фасад `Cache` дає зручний і стислий доступ до реалізацій контрактів кешу Laravel:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
#### Доступ до кількох сховищ кешу

За допомогою фасаду `Cache` ви можете звертатися до різних сховищ методом `store`. Ключ, переданий методу `store`, має відповідати одному зі сховищ, перелічених у масиві конфігурації `stores` вашого файлу `cache`:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### Отримання елементів із кешу

Метод `get` фасаду `Cache` слугує для отримання елементів із кешу. Якщо елемента в кеші немає, буде повернуто `null`. За бажанням ви можете передати методу `get` другий аргумент, указавши значення за замовчуванням, яке слід повернути за відсутності елемента:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

Ви можете навіть передати замикання як значення за замовчуванням. Його результат буде повернуто, якщо вказаного елемента в кеші немає. Передавання замикання дозволяє відкласти отримання значень за замовчуванням із бази даних чи іншого зовнішнього сервісу:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### Перевірка наявності елемента

Метод `has` дозволяє визначити, чи існує елемент у кеші. Цей метод також поверне `false`, якщо елемент існує, але його значення - `null`:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### Збільшення та зменшення значень

Методи `increment` і `decrement` дозволяють коригувати значення цілочисельних елементів у кеші. Обидва приймають необов'язковий другий аргумент - величину, на яку слід змінити значення:

```php
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->plus(hours: 4));

// Increment or decrement the value...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### Отримати й зберегти

Іноді ви можете захотіти отримати елемент із кешу, але водночас зберегти значення за замовчуванням, якщо запитаного елемента немає. Наприклад, ви можете захотіти отримати всіх користувачів із кешу або, якщо їх там немає, узяти їх з бази даних і додати до кешу. Це робиться методом `Cache::remember`:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

Якщо елемента в кеші немає, буде виконано замикання, передане методу `remember`, а його результат буде поміщено в кеш.

Якщо вам потрібно знати, чи елемент отримано з кешу, а не через виконання замикання, скористайтеся методом `rememberWithWarmth`. Він повертає масив із закешованим значенням і булевим прапорцем, що вказує, чи був елемент «теплим», тобто отриманим із кешу, а не розв'язаним із замикання:

```php
[$value, $warm] = Cache::rememberWithWarmth('users', $seconds, function () {
    return DB::table('users')->get();
});
```

Метод `rememberForever` дозволяє отримати елемент із кешу або зберегти його назавжди, якщо його немає:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

Використовуючи метод `Cache::remember`, частина користувачів може стикатися з повільними відповідями, коли термін дії закешованого значення сплив. Для певних типів даних буває корисно віддавати частково застарілі дані, поки значення перераховується у фоні, - так деякі користувачі не чекатимуть на обчислення. Цей підхід часто називають «stale-while-revalidate», і метод `Cache::flexible` є його реалізацією.

Метод `flexible` приймає масив, що вказує, як довго закешоване значення вважається «свіжим» і коли воно стає «застарілим». Перше значення масиву - кількість секунд, протягом яких кеш вважається свіжим, друге - як довго його можна віддавати як застарілі дані до того, як перерахунок стане необхідним.

Якщо запит надходить у межах свіжого періоду (до першого значення), кеш повертається одразу без перерахунку. Якщо запит надходить у застарілий період (між двома значеннями), користувачеві віддається застаріле значення, а для оновлення кешу після надсилання відповіді реєструється [відкладена функція](/docs/{{version}}/helpers#deferred-functions). Якщо запит надходить після другого значення, кеш вважається простроченим, і значення перераховується одразу, що може призвести до повільнішої відповіді:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### Отримати й видалити

Якщо вам потрібно отримати елемент із кешу й одразу його видалити, скористайтеся методом `pull`. Як і метод `get`, він поверне `null`, якщо елемента в кеші немає:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### Збереження елементів у кеші

Щоб зберегти елементи в кеші, скористайтеся методом `put` фасаду `Cache`:

```php
Cache::put('key', 'value', $seconds = 10);
```

Якщо методу `put` не передано час зберігання, елемент зберігатиметься безстроково:

```php
Cache::put('key', 'value');
```

Замість передавати кількість секунд цілим числом, ви можете передати екземпляр `DateTime`, що представляє бажаний час спливання закешованого елемента:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### Зберегти, якщо відсутній

Метод `add` додасть елемент до кешу лише тоді, коли його там ще немає. Метод поверне `true`, якщо елемент справді додано, інакше - `false`. Метод `add` є атомарною операцією:

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### Продовження часу життя елемента

Метод `touch` дозволяє продовжити час життя (TTL) наявного елемента кешу. Метод `touch` поверне `true`, якщо елемент кешу існує і час його спливання успішно продовжено. Якщо елемента в кеші немає, метод поверне `false`:

```php
Cache::touch('key', 3600);
```

Ви можете передати екземпляр `DateTimeInterface`, `DateInterval` чи `Carbon`, щоб указати точний час спливання:

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### Безстрокове зберігання елементів

Метод `forever` дозволяє зберегти елемент у кеші назавжди. Оскільки термін дії таких елементів не спливає, їх доведеться вилучати вручну методом `forget`:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Якщо ви використовуєте драйвер Memcached, елементи, збережені «назавжди», можуть бути вилучені, коли кеш досягне граничного розміру.

<a name="removing-items-from-the-cache"></a>
### Видалення елементів із кешу

Вилучити елементи з кешу можна методом `forget`:

```php
Cache::forget('key');
```

Ви також можете вилучити елементи, передавши нульову чи від'ємну кількість секунд:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

Очистити весь кеш можна методом `flush`:

```php
Cache::flush();
```

Очистити всі атомарні блокування в кеші можна методом `flushLocks`:

```php
Cache::flushLocks();
```

> [!WARNING]
> Очищення кешу не враховує налаштований «префікс» і вилучить із кешу всі записи. Добре зважте це, очищаючи кеш, який спільно використовують інші застосунки.

<a name="cache-memoization"></a>
### Мемоізація кешу

Драйвер кешу `memo` в Laravel дозволяє тимчасово зберігати розв'язані значення кешу в пам'яті протягом одного запиту чи виконання завдання. Це запобігає повторним зверненням до кешу в межах одного виконання й помітно покращує швидкодію.

Щоб скористатися мемоізованим кешем, викличте метод `memo`:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

Метод `memo` за бажанням приймає ім'я сховища кешу, яке вказує, яке саме сховище декоруватиме мемоізований драйвер:

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

Перший виклик `get` для певного ключа отримує значення з вашого сховища кешу, але наступні виклики в межах того самого запиту чи завдання братимуть значення з пам'яті:

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

Коли викликаються методи, що змінюють значення кешу (як-от `put`, `increment`, `remember` тощо), мемоізований кеш автоматично забуває збережене значення й делегує виклик основному сховищу кешу:

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
### Хелпер кешу

Окрім фасаду `Cache`, ви можете скористатися глобальною функцією `cache`, щоб отримувати та зберігати дані в кеші. Коли функцію `cache` викликано з одним рядковим аргументом, вона поверне значення за вказаним ключем:

```php
$value = cache('key');
```

Якщо ви передасте функції масив пар «ключ-значення» та час спливання, вона збереже значення в кеші на вказаний час:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

Коли функцію `cache` викликано без аргументів, вона повертає екземпляр реалізації `Illuminate\Contracts\Cache\Factory`, що дозволяє викликати інші методи кешування:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> Тестуючи виклики глобальної функції `cache`, ви можете скористатися методом `Cache::shouldReceive` так само, як під час [тестування фасаду](/docs/{{version}}/mocking#mocking-facades).

<a name="cache-tags"></a>
## Теги кешу

> [!WARNING]
> Теги кешу не підтримуються драйверами `file`, `dynamodb`, `database` та `storage`.

<a name="storing-tagged-cache-items"></a>
### Збереження елементів кешу з тегами

Теги кешу дозволяють позначати пов'язані елементи в кеші, а потім скидати всі значення, яким призначено певний тег. Отримати доступ до кешу з тегами можна, передавши впорядкований масив імен тегів. Наприклад, звернімося до кешу з тегами й помістімо в нього значення методом `put`:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### Доступ до елементів кешу з тегами

До елементів, збережених із тегами, не можна звернутися, не вказавши тих самих тегів. Щоб отримати елемент кешу з тегами, передайте методу `tags` той самий упорядкований список тегів, а потім викличте метод `get` із потрібним ключем:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### Видалення елементів кешу з тегами

Ви можете скинути всі елементи, яким призначено тег чи список тегів. Наприклад, наведений нижче код вилучить усі кеші, позначені `people`, `authors` або обома тегами. Тож із кешу буде вилучено і `Anne`, і `John`:

```php
Cache::tags(['people', 'authors'])->flush();
```

Натомість наведений нижче код вилучить лише значення, позначені тегом `authors`, - тож `Anne` буде вилучено, а `John` ні:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## Атомарні блокування

> [!WARNING]
> Щоб скористатися цією можливістю, ваш застосунок має використовувати як типовий драйвер кешу `memcached`, `redis`, `dynamodb`, `database`, `file` чи `array`. Крім того, усі сервери мають спілкуватися з одним центральним сервером кешу.

<a name="managing-locks"></a>
### Керування блокуваннями

Атомарні блокування дозволяють працювати з розподіленими блокуваннями, не турбуючись про стани гонитви. Наприклад, [Laravel Cloud](https://cloud.laravel.com) використовує атомарні блокування, щоб гарантувати виконання лише одного віддаленого завдання на сервері за раз. Створювати блокування та керувати ними можна методом `Cache::lock`:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

Метод `get` також приймає замикання. Після його виконання Laravel автоматично зніме блокування:

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

Якщо блокування недоступне в момент запиту, ви можете вказати Laravel зачекати визначену кількість секунд. Якщо блокування не вдасться отримати за цей час, буде викинуто `Illuminate\Contracts\Cache\LockTimeoutException`:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock->release();
}
```

Наведений вище приклад можна спростити, передавши замикання методу `block`. Коли методу передано замикання, Laravel намагатиметься отримати блокування протягом указаної кількості секунд і автоматично зніме його після виконання замикання:

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
### Керування блокуваннями між процесами

Іноді ви можете захотіти отримати блокування в одному процесі, а зняти його в іншому. Наприклад, ви можете отримати блокування під час веб-запиту й зняти його наприкінці завдання з черги, запущеного цим запитом. У такому сценарії вам слід передати завданню «токен власника» блокування, щоб завдання могло відтворити блокування за цим токеном.

У прикладі нижче ми надішлемо завдання до черги, якщо блокування успішно отримано. Крім того, ми передамо завданню токен власника через метод `owner`:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

У завданні `ProcessPodcast` нашого застосунку ми можемо відновити й зняти блокування за токеном власника:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

Якщо ви хочете зняти блокування, не зважаючи на його поточного власника, скористайтеся методом `forceRelease`:

```php
Cache::lock('processing')->forceRelease();
```

<a name="refreshing-locks"></a>
### Оновлення блокувань

Якщо вам потрібно продовжити час дії блокування, яким ви наразі володієте, скористайтеся методом `refresh`. Якщо кількість секунд не передано, буде використано початкову тривалість блокування. Це корисно для тривалих операцій, коли ви віддаєте перевагу короткому блокуванню з періодичним продовженням замість блокування з дуже довгим часом спливання:

```php
$lock = Cache::lock('generate-reports', 60);

if ($lock->get()) {
    foreach ($reports as $report) {
        $report->generate();

        // Extend the lock for another 60 seconds...
        $lock->refresh();
    }

    $lock->release();
}
```

<a name="concurrency-limiting"></a>
### Обмеження паралельності

Атомарні блокування в Laravel також дають кілька способів обмежити паралельне виконання замикань. Скористайтеся `withoutOverlapping`, коли хочете дозволити лише один запущений екземпляр у всій вашій інфраструктурі:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

За замовчуванням блокування утримується, доки замикання не завершить виконання, а метод чекає на його отримання до 10 секунд. Ви можете змінити ці значення додатковими аргументами:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

Якщо блокування не вдасться отримати за вказаний час очікування, буде викинуто `Illuminate\Contracts\Cache\LockTimeoutException`.

Якщо вам потрібен контрольований паралелізм, скористайтеся методом `funnel`, щоб задати максимальну кількість одночасних виконань. Метод `funnel` працює з будь-яким драйвером кешу, що підтримує блокування:

```php
Cache::funnel('foo')
    ->limit(3)
    ->releaseAfter(60)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired...
    }, function () {
        // Could not acquire concurrency lock...
    });
```

Ключ `funnel` ідентифікує ресурс, який обмежують. Метод `limit` визначає максимальну кількість одночасних виконань. Метод `releaseAfter` задає запобіжний тайм-аут у секундах, після якого зайнятий слот автоматично звільняється. Метод `block` задає, скільки секунд чекати на вільний слот.

Якщо ви віддаєте перевагу обробці тайм-ауту через винятки замість замикання на випадок невдачі, друге замикання можна не передавати. Якщо блокування не вдасться отримати за вказаний час очікування, буде викинуто `Illuminate\Cache\Limiters\LimiterTimeoutException`:

```php
use Illuminate\Cache\Limiters\LimiterTimeoutException;

try {
    Cache::funnel('foo')
        ->limit(3)
        ->releaseAfter(60)
        ->block(10)
        ->then(function () {
            // Concurrency lock acquired...
        });
} catch (LimiterTimeoutException $e) {
    // Unable to acquire concurrency lock...
}
```

Якщо ви хочете використати для обмежувача паралельності конкретне сховище кешу, викличте метод `funnel` на потрібному сховищі:

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> Метод `funnel` потребує, щоб сховище кешу реалізовувало інтерфейс `Illuminate\Contracts\Cache\LockProvider`. Якщо ви спробуєте скористатися `funnel` зі сховищем, що не підтримує блокувань, буде викинуто `BadMethodCallException`.

<a name="cache-failover"></a>
## Резервування кешу

Драйвер кешу `failover` забезпечує автоматичне перемикання на резерв під час роботи з кешем. Якщо основне сховище кешу з якоїсь причини відмовить, Laravel автоматично спробує наступне сховище зі списку. Це особливо корисно для високої доступності в продакшені, де надійність кешу критична.

Щоб налаштувати резервне сховище кешу, вкажіть драйвер `failover` і передайте масив імен сховищ у порядку спроб. За замовчуванням Laravel містить приклад такої конфігурації у файлі `config/cache.php` вашого застосунку:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

Налаштувавши сховище з драйвером `failover`, вам потрібно задати його як типове сховище кешу у файлі `.env`, щоб скористатися резервуванням:

```ini
CACHE_STORE=failover
```

Коли операція зі сховищем кешу зазнає невдачі й активується резервування, Laravel надішле подію `Illuminate\Cache\Events\CacheFailedOver`, що дозволить вам відзвітувати чи залогувати відмову сховища.

<a name="adding-custom-cache-drivers"></a>
## Додавання власних драйверів кешу

<a name="writing-the-driver"></a>
### Написання драйвера

Щоб створити власний драйвер кешу, спершу потрібно реалізувати [контракт](/docs/{{version}}/contracts) `Illuminate\Contracts\Cache\Store`. Тож реалізація кешу для MongoDB може виглядати так:

```php
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```

Нам залишається реалізувати кожен із цих методів через підключення до MongoDB. Приклад реалізації кожного методу можна побачити в класі `Illuminate\Cache\MemcachedStore` у [вихідному коді фреймворку Laravel](https://github.com/laravel/framework). Коли наша реалізація готова, ми можемо завершити реєстрацію власного драйвера викликом методу `extend` фасаду `Cache`:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> Якщо вам цікаво, куди покласти код власного драйвера кешу, можете створити простір імен `Extensions` у каталозі `app`. Утім, пам'ятайте: Laravel не має жорсткої структури застосунку, і ви вільні організовувати його на власний розсуд.

<a name="registering-the-driver"></a>
### Реєстрація драйвера

Щоб зареєструвати власний драйвер кешу в Laravel, ми скористаємося методом `extend` фасаду `Cache`. Оскільки інші сервіс-провайдери можуть намагатися читати закешовані значення у своєму методі `boot`, ми зареєструємо драйвер у колбеку `booting`. Це гарантує, що власний драйвер буде зареєстровано саме перед викликом методу `boot` сервіс-провайдерів застосунку, але після виклику методу `register` на всіх провайдерах. Колбек `booting` ми зареєструємо в методі `register` класу `App\Providers\AppServiceProvider`:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

Перший аргумент, переданий методу `extend`, - ім'я драйвера. Воно відповідатиме вашій опції `driver` у конфігураційному файлі `config/cache.php`. Другий аргумент - замикання, що має повертати екземпляр `Illuminate\Cache\Repository`. Замиканню буде передано екземпляр `$app` - екземпляр [сервіс-контейнера](/docs/{{version}}/container).

Щойно ваше розширення зареєстровано, оновіть змінну середовища `CACHE_STORE` чи опцію `default` у файлі `config/cache.php` вашого застосунку, вказавши ім'я вашого розширення.

<a name="events"></a>
## Події

Щоб виконувати код на кожній операції з кешем, ви можете слухати різні [події](/docs/{{version}}/events), які надсилає кеш:

<div class="overflow-auto">

| Ім'я події                                      |
|-------------------------------------------------|

| `Illuminate\Cache\Events\CacheFlushed`          |
| `Illuminate\Cache\Events\CacheFlushing`         |
| `Illuminate\Cache\Events\CacheFlushFailed`      |
| `Illuminate\Cache\Events\CacheLocksFlushed`     |
| `Illuminate\Cache\Events\CacheLocksFlushing`    |
| `Illuminate\Cache\Events\CacheLocksFlushFailed` |
| `Illuminate\Cache\Events\CacheHit`              |
| `Illuminate\Cache\Events\CacheMissed`           |
| `Illuminate\Cache\Events\ForgettingKey`         |
| `Illuminate\Cache\Events\KeyForgetFailed`       |
| `Illuminate\Cache\Events\KeyForgotten`          |
| `Illuminate\Cache\Events\KeyWriteFailed`        |
| `Illuminate\Cache\Events\KeyWritten`            |
| `Illuminate\Cache\Events\RetrievingKey`         |
| `Illuminate\Cache\Events\RetrievingManyKeys`    |
| `Illuminate\Cache\Events\WritingKey`            |
| `Illuminate\Cache\Events\WritingManyKeys`       |

</div>

Щоб підвищити швидкодію, ви можете вимкнути події кешу, задавши опції конфігурації `events` значення `false` для потрібного сховища у файлі `config/cache.php` вашого застосунку:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
