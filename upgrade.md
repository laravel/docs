---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Посібник з оновлення

- [Оновлення з 12.x до 13.0](#upgrade-13.0)
    - [Оновлення за допомогою AI](#upgrading-using-ai)

<a name="high-impact-changes"></a>
## Зміни з високим впливом

<div class="content-list" markdown="1">

- [Оновлення залежностей](#updating-dependencies)
- [Оновлення інсталятора Laravel](#updating-the-laravel-installer)
- [Захист від підробки запитів](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
## Зміни з середнім впливом

<div class="content-list" markdown="1">

- [Конфігурація кешу `serializable_classes`](#cache-serializable_classes-configuration)
- [`upsert` бази даних з MySQL або MariaDB](#database-upsert-mariadb-mysql)

</div>

<a name="low-impact-changes"></a>
## Зміни з низьким впливом

<div class="content-list" markdown="1">

- [Префікси кешу та імена cookie сесії](#cache-prefixes-and-session-cookie-names)
- [Серіалізація колекцій моделей відновлює жадібно завантажені зв'язки](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` і значення за замовчуванням для nullable-класів](#containercall-and-nullable-class-defaults)
- [Пріоритет реєстрації доменних маршрутів](#domain-route-registration-precedence)
- [Дані винятку в події `JobAttempted`](#jobattempted-event-exception-payload)
- [Прив'язка колбека `extend` у менеджерах](#manager-extend-callback-binding)
- [Запити `DELETE` у MySQL із `JOIN`, `ORDER BY` та `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [Імена представлень пагінації для Bootstrap](#pagination-bootstrap-view-names)
- [Генерація імен поліморфних зведених таблиць](#polymorphic-pivot-table-name-generation)
- [Перейменування властивості події `QueueBusy`](#queuebusy-event-property-rename)
- [Фабрики `Str` скидаються між тестами](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
## Оновлення з 12.x до 13.0

#### Орієнтовний час оновлення: 10 хвилин

> [!NOTE]
> Ми намагаємося задокументувати кожну можливу зміну, що порушує сумісність. Оскільки частина цих змін стосується маловживаних частин фреймворку, реально вплинути на ваш застосунок може лише частина з них. Щоб заощадити час, скористайтеся [Shift](https://laravelshift.com) - сервісом, який підтримує спільнота і який автоматизує оновлення Laravel.

<a name="upgrading-using-ai"></a>
### Оновлення за допомогою AI

Ви можете автоматизувати оновлення за допомогою [Laravel Boost](https://github.com/laravel/boost). Boost - це офіційний MCP-сервер, який дає вашому AI-асистенту покрокові підказки для оновлення. Щойно його встановлено в будь-якому застосунку Laravel 12, скористайтеся slash-командою `/upgrade-laravel-v13` у Claude Code, Cursor, OpenCode, Gemini чи VS Code, щоб почати оновлення до Laravel 13. Ця команда потребує Laravel Boost `^2.0`.

<a name="updating-dependencies"></a>
### Оновлення залежностей

**Імовірність впливу: висока**

Вам слід оновити такі залежності у файлі `composer.json` вашого застосунку:

<div class="content-list" markdown="1">

- `laravel/framework` до `^13.0`
- `laravel/boost` до `^2.0`
- `laravel/tinker` до `^3.0`
- `phpunit/phpunit` до `^12.0`
- `pestphp/pest` до `^4.0`

</div>

<a name="updating-the-laravel-installer"></a>
### Оновлення інсталятора Laravel

Якщо ви користуєтеся CLI-інструментом інсталятора Laravel для створення нових застосунків, оновіть його для сумісності з Laravel 13.x.

Якщо ви встановили інсталятор Laravel через `composer global require`, оновіть його командою `composer global update`:

```shell
composer global update laravel/installer
```

Або, якщо ви користуєтеся копією інсталятора Laravel, що постачається з [Laravel Herd](https://herd.laravel.com), оновіть свою інсталяцію Herd до найновішого релізу.

<a name="cache"></a>
### Кеш

<a name="cache-prefixes-and-session-cookie-names"></a>
#### Префікси кешу та імена cookie сесії

**Імовірність впливу: низька**

Префікси ключів кешу та Redis за замовчуванням тепер використовують суфікси з дефісами.

У більшості застосунків ця зміна не діятиме, бо конфігураційні файли рівня застосунку вже визначають ці значення. Насамперед вона стосується застосунків, що покладаються на резервну конфігурацію рівня фреймворку, коли відповідних значень у конфігурації застосунку немає.

Якщо ваш застосунок покладається на ці згенеровані значення за замовчуванням, ключі кешу та імена cookie сесії після оновлення можуть змінитися:

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';
```

Щоб зберегти попередню поведінку, явно задайте `CACHE_PREFIX`, `REDIS_PREFIX` і `SESSION_COOKIE` у своєму середовищі.

<a name="store-and-repository-contracts-touch"></a>
#### Контракти `Store` і `Repository`: `touch`

**Імовірність впливу: дуже низька**

Контракти кешу тепер містять метод `touch` для продовження TTL елементів. Якщо ви підтримуєте власні реалізації сховищ кешу, додайте цей метод:

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
#### Конфігурація кешу `serializable_classes`

**Імовірність впливу: середня**

Конфігурація `cache` застосунку за замовчуванням тепер містить опцію `serializable_classes` зі значенням `false`. Це посилює поведінку десеріалізації кешу, щоб запобігти атакам через ланцюжки гаджетів десеріалізації PHP, якщо `APP_KEY` вашого застосунку витече. Якщо ваш застосунок навмисне зберігає PHP-об'єкти в кеші, явно перелічіть класи, які дозволено десеріалізувати:

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

Якщо раніше ваш застосунок покладався на десеріалізацію довільних закешованих об'єктів, вам доведеться перевести це на явні списки дозволених класів або на дані кешу без об'єктів (наприклад, масиви).

<a name="container"></a>
### Контейнер

<a name="containercall-and-nullable-class-defaults"></a>
#### `Container::call` і значення за замовчуванням для nullable-класів

**Імовірність впливу: низька**

`Container::call` тепер враховує значення за замовчуванням для nullable-параметрів класів, коли прив'язки не існує, що відповідає поведінці впровадження через конструктор, запровадженій у Laravel 12:

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: екземпляр Carbon
// Laravel >= 13.x: null
```

Якщо ваша логіка впровадження при виклику методів залежала від попередньої поведінки, її може знадобитися оновити.

<a name="contracts"></a>
### Контракти

<a name="dispatcher-contract-dispatchafterresponse"></a>
#### Контракт `Dispatcher`: `dispatchAfterResponse`

**Імовірність впливу: дуже низька**

Контракт `Illuminate\Contracts\Bus\Dispatcher` тепер містить метод `dispatchAfterResponse($command, $handler = null)`.

Якщо ви підтримуєте власну реалізацію диспетчера, додайте цей метод до свого класу.

<a name="responsefactory-contract-eventstream"></a>
#### Контракт `ResponseFactory`: `eventStream`

**Імовірність впливу: дуже низька**

Контракт `Illuminate\Contracts\Routing\ResponseFactory` тепер містить сигнатуру `eventStream`.

Якщо ви підтримуєте власну реалізацію цього контракту, додайте цей метод.

<a name="mustverifyemail-contract-markemailasunverified"></a>
#### Контракт `MustVerifyEmail`: `markEmailAsUnverified`

**Імовірність впливу: дуже низька**

Контракт `Illuminate\Contracts\Auth\MustVerifyEmail` тепер містить `markEmailAsUnverified()`.

Якщо ви надаєте власну реалізацію цього контракту, додайте цей метод, щоб лишитися сумісними.

<a name="database"></a>
### База даних

<a name="database-upsert-mariadb-mysql"></a>
#### `upsert` бази даних з MySQL або MariaDB

**Імовірність впливу: середня**

Laravel тепер перевіряє, що той, хто викликає метод, передає непорожнє значення для `uniqueBy`, і викидає `InvalidArgumentException` замість генерації некоректного SQL.

Хоча драйвери MariaDB та MySQL ігнорують значення `uniqueBy` і завжди використовують первинні та унікальні індекси таблиці для виявлення наявних записів, перевірка все одно застосовується. Якщо `uniqueBy` порожній, буде викинуто `InvalidArgumentException`.

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### Запити `DELETE` у MySQL із `JOIN`, `ORDER BY` та `LIMIT`

**Імовірність впливу: низька**

Laravel тепер компілює повні запити `DELETE ... JOIN`, включно з `ORDER BY` та `LIMIT`, для граматики MySQL.

У попередніх версіях речення `ORDER BY` / `LIMIT` могли мовчки ігноруватися при видаленні з приєднанням. У Laravel 13 ці речення потрапляють до згенерованого SQL. Як наслідок, рушії баз даних, що не підтримують цей синтаксис (як-от стандартні варіанти MySQL / MariaDB), тепер можуть викидати `QueryException` замість виконання необмеженого видалення.

<a name="eloquent"></a>
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
#### Завантаження моделі та вкладене створення екземплярів

**Імовірність впливу: дуже низька**

Створення нового екземпляра моделі, поки ця модель ще завантажується, тепер заборонено й викидає `LogicException`.

Це стосується коду, який створює екземпляри моделей усередині методів `boot` моделі або методів `boot*` трейтів:

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

Винесіть цю логіку за межі циклу завантаження, щоб уникнути вкладеного завантаження.

<a name="polymorphic-pivot-table-name-generation"></a>
#### Генерація імен поліморфних зведених таблиць

**Імовірність впливу: низька**

Коли імена таблиць виводяться для поліморфних зведених моделей із власними класами зведених моделей, Laravel тепер генерує імена у множині.

Якщо ваш застосунок покладався на попередні виведені імена в однині для морф-зведених таблиць і використовував власні класи зведених моделей, явно визначте ім'я таблиці у своїй зведеній моделі.

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
#### Серіалізація колекцій моделей відновлює жадібно завантажені зв'язки

**Імовірність впливу: низька**

Коли колекції моделей Eloquent серіалізуються та відновлюються (наприклад, у завданнях черги), жадібно завантажені (eager loading) зв'язки тепер відновлюються для моделей колекції.

Якщо ваш код покладався на те, що після десеріалізації зв'язків немає, цю логіку може знадобитися скоригувати.

<a name="http-client"></a>
### HTTP-клієнт

<a name="http-client-response-throw-and-throwif-signatures"></a>
#### Сигнатури `Response::throw` і `throwIf` HTTP-клієнта

**Імовірність впливу: дуже низька**

Методи відповіді HTTP-клієнта тепер оголошують параметри колбеків у сигнатурах:

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

Якщо ви перевизначаєте ці методи у власних класах відповідей, переконайтеся, що сигнатури ваших методів сумісні.

<a name="notifications"></a>
### Сповіщення

<a name="default-password-reset-subject"></a>
#### Тема листа скидання пароля за замовчуванням

**Імовірність впливу: дуже низька**

Тема листа скидання пароля Laravel за замовчуванням змінилася:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

Якщо ваші тести, перевірки чи перевизначення перекладів залежать від попереднього рядка за замовчуванням, оновіть їх відповідно.

<a name="queued-notifications-and-missing-models"></a>
#### Сповіщення в черзі та відсутні моделі

**Імовірність впливу: дуже низька**

Сповіщення в черзі тепер враховують атрибут `#[DeleteWhenMissingModels]` і властивість `$deleteWhenMissingModels`, визначені в класі сповіщення.

У попередніх версіях відсутні моделі все одно могли призводити до провалу завдань черги зі сповіщеннями в тих випадках, коли ви очікували, що їх буде видалено.

<a name="queue"></a>
### Черги

<a name="jobattempted-event-exception-payload"></a>
#### Дані винятку в події `JobAttempted`

**Імовірність впливу: низька**

Подія `Illuminate\Queue\Events\JobAttempted` тепер надає об'єкт винятку (або `null`) через `$exception`, замінюючи попередню булеву властивість `$exceptionOccurred`:

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

Якщо ви слухаєте цю подію, оновіть код свого слухача відповідно.

<a name="queuebusy-event-property-rename"></a>
#### Перейменування властивості події `QueueBusy`

**Імовірність впливу: низька**

Властивість `$connection` події `Illuminate\Queue\Events\QueueBusy` перейменовано на `$connectionName` задля узгодженості з іншими подіями черг.

Якщо ваші слухачі звертаються до `$connection`, оновіть їх на `$connectionName`.

<a name="queue-contract-method-additions"></a>
#### Додані методи контракту `Queue`

**Імовірність впливу: дуже низька**

Контракт `Illuminate\Contracts\Queue\Queue` тепер містить методи перевірки розміру черги, які раніше були оголошені лише в docblock'ах.

Якщо ви підтримуєте власні реалізації драйверів черг за цим контрактом, додайте реалізації для:

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
### Маршрутизація

<a name="domain-route-registration-precedence"></a>
#### Пріоритет реєстрації доменних маршрутів

**Імовірність впливу: низька**

Маршрути з явно вказаним доменом тепер мають пріоритет над недоменними маршрутами під час зіставлення маршрутів.

Це дозволяє маршрутам-перехоплювачам піддоменів поводитися послідовно навіть тоді, коли недоменні маршрути зареєстровані раніше. Якщо ваш застосунок покладався на попередній пріоритет реєстрації між доменними та недоменними маршрутами, перевірте поведінку зіставлення маршрутів.

<a name="scheduling"></a>
### Планування

<a name="withscheduling-registration-timing"></a>
#### Момент реєстрації `withScheduling`

**Імовірність впливу: дуже низька**

Розклади, зареєстровані через `ApplicationBuilder::withScheduling()`, тепер відкладаються до моменту, коли розв'язується `Schedule`.

Якщо ваш застосунок покладався на негайну реєстрацію розкладу під час завантаження, цю логіку може знадобитися скоригувати.

<a name="security"></a>
### Безпека

<a name="request-forgery-protection"></a>
#### Захист від підробки запитів

**Імовірність впливу: висока**

CSRF-`middleware` Laravel перейменовано з `VerifyCsrfToken` на `PreventRequestForgery`, і тепер він містить перевірку джерела запиту за допомогою заголовка `Sec-Fetch-Site`.

`VerifyCsrfToken` і `ValidateCsrfToken` лишаються як застарілі псевдоніми, але прямі посилання слід оновити на `PreventRequestForgery`, особливо коли ви виключаєте `middleware` у тестах чи визначеннях маршрутів:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

API конфігурації `middleware` тепер також надає `preventRequestForgery(...)`.

<a name="support"></a>
### Support

<a name="manager-extend-callback-binding"></a>
#### Прив'язка колбека `extend` у менеджерах

**Імовірність впливу: низька**

Замикання власних драйверів, зареєстровані через методи `extend` менеджерів, тепер прив'язуються до екземпляра менеджера.

Якщо раніше ви покладалися на інший прив'язаний об'єкт (наприклад, екземпляр сервіс-провайдера) як `$this` усередині цих колбеків, перенесіть ці значення до замикання через `use (...)`.

<a name="str-factories-reset-between-tests"></a>
#### Фабрики `Str` скидаються між тестами

**Імовірність впливу: низька**

Laravel тепер скидає власні фабрики `Str` під час завершення тесту.

Якщо ваші тести покладалися на те, що власні фабрики UUID / ULID / випадкових рядків зберігаються між тестовими методами, задавайте їх у кожному відповідному тесті або в хуку налаштування.

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from` за замовчуванням використовує неекранований Unicode

**Імовірність впливу: дуже низька**

`Illuminate\Support\Js::from` тепер за замовчуванням використовує `JSON_UNESCAPED_UNICODE`.

Якщо ваші тести чи порівняння виводу фронтенду залежали від екранованих послідовностей Unicode (наприклад, `è`), оновіть свої очікування.

<a name="utilities"></a>
### Утиліти

<a name="symfony-polyfill"></a>
#### Поліфіл Symfony для PHP 8.5 і конфлікти глобальних функцій

**Імовірність впливу: низька**

Laravel 13 додає залежність від `symfony/polyfill-php85`. На версіях PHP нижче 8.5 цей поліфіл визначає глобальні функції на кшталт `array_first()` та `array_last()`, якщо їх не було визначено раніше під час завантаження.

Ці функції можуть конфліктувати зі старими пакетами хелперів, як-от `laravel/helpers`, або з власними глобальними хелперами з такими самими іменами. Наприклад, історичний хелпер `array_first()` приймав колбек і повертав перший відповідний елемент, тоді як версія з поліфілу повертає лише перший елемент масиву.

Щоб уникнути конфліктів і забезпечити послідовну поведінку на різних версіях PHP, надавайте перевагу методам `Illuminate\Support\Arr`:

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a name="views"></a>
### Представлення

<a name="pagination-bootstrap-view-names"></a>
#### Імена представлень пагінації для Bootstrap

**Імовірність впливу: низька**

Внутрішні імена представлень пагінації для типових налаштувань Bootstrap 3 тепер явні:

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

Якщо ваш застосунок посилається безпосередньо на старі імена представлень пагінації, оновіть ці посилання.

<a name="miscellaneous"></a>
### Різне

Радимо також переглянути зміни в [репозиторії GitHub](https://github.com/laravel/laravel) `laravel/laravel`. Хоча багато з цих змін не є обов'язковими, ви можете захотіти тримати ці файли синхронізованими зі своїм застосунком. Частину змін розглянуто в цьому посібнику з оновлення, але інші - як-от зміни в конфігураційних файлах чи коментарях - ні. Ви можете легко переглянути зміни за допомогою [інструмента порівняння GitHub](https://github.com/laravel/laravel/compare/12.x...13.x) і вибрати, які оновлення для вас важливі.
