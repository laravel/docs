---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Telescope

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Встановлення лише для локальної розробки](#local-only-installation)
    - [Конфігурація](#configuration)
    - [Очищення даних](#data-pruning)
    - [Авторизація панелі](#dashboard-authorization)
- [Оновлення Telescope](#upgrading-telescope)
- [Фільтрація](#filtering)
    - [Записи](#filtering-entries)
    - [Пакети](#filtering-batches)
- [Теги](#tagging)
- [Доступні спостерігачі](#available-watchers)
    - [Спостерігач пакетів](#batch-watcher)
    - [Спостерігач кешу](#cache-watcher)
    - [Спостерігач команд](#command-watcher)
    - [Спостерігач дампів](#dump-watcher)
    - [Спостерігач подій](#event-watcher)
    - [Спостерігач винятків](#exception-watcher)
    - [Спостерігач гейтів](#gate-watcher)
    - [Спостерігач HTTP-клієнта](#http-client-watcher)
    - [Спостерігач завдань](#job-watcher)
    - [Спостерігач логів](#log-watcher)
    - [Спостерігач пошти](#mail-watcher)
    - [Спостерігач моделей](#model-watcher)
    - [Спостерігач сповіщень](#notification-watcher)
    - [Спостерігач запитів до бази](#query-watcher)
    - [Спостерігач Redis](#redis-watcher)
    - [Спостерігач запитів](#request-watcher)
    - [Спостерігач планувальника](#schedule-watcher)
    - [Спостерігач представлень](#view-watcher)
- [Показ аватарів користувачів](#displaying-user-avatars)

<a name="introduction"></a>
## Вступ

[Laravel Telescope](https://github.com/laravel/telescope) стане чудовим супутником вашого локального середовища розробки на Laravel. Telescope дає змогу зазирнути всередину запитів, що надходять до вашого застосунку, а також винятків, записів логу, запитів до бази даних, завдань у черзі, пошти, сповіщень, операцій із кешем, запланованих завдань, дампів змінних тощо.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## Встановлення

Ви можете встановити Telescope у свій проєкт Laravel через менеджер пакетів Composer:

```shell
composer require laravel/telescope
```

Після встановлення Telescope опублікуйте його ресурси й міграції артизан-командою `telescope:install`. Далі виконайте команду `migrate`, щоб створити таблиці, потрібні для зберігання даних Telescope:

```shell
php artisan telescope:install

php artisan migrate
```

Нарешті, ви можете відкрити панель Telescope за маршрутом `/telescope`.

<a name="local-only-installation"></a>
### Встановлення лише для локальної розробки

Якщо ви плануєте користуватися Telescope лише для локальної розробки, встановіть його з прапорцем `--dev`:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

Виконавши `telescope:install`, приберіть реєстрацію сервіс-провайдера `TelescopeServiceProvider` з конфігураційного файлу `bootstrap/providers.php` вашого застосунку. Натомість зареєструйте сервіс-провайдери Telescope вручну в методі `register` вашого класу `App\Providers\AppServiceProvider`. Перед реєстрацією провайдерів ми переконаємося, що поточне середовище - `local`:

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

Нарешті, вам також слід завадити [автовиявленню](/docs/{{version}}/packages#package-discovery) пакета Telescope, додавши до свого файлу `composer.json` таке:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a name="configuration"></a>
### Конфігурація

Після публікації ресурсів Telescope його основний конфігураційний файл буде розташований у `config/telescope.php`. Цей файл дозволяє налаштувати [опції спостерігачів](#available-watchers). Кожна опція конфігурації супроводжується описом призначення, тож обов'язково ретельно перегляньте цей файл.

За бажання ви можете цілком вимкнути збирання даних Telescope через опцію конфігурації `enabled`:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### Очищення даних

Без очищення таблиця `telescope_entries` може дуже швидко накопичити записи. Щоб цьому запобігти, [заплануйте](/docs/{{version}}/scheduling) щоденний запуск артизан-команди `telescope:prune`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

За замовчуванням буде видалено всі записи, старші за 24 години. Ви можете скористатися опцією `hours` під час виклику команди, щоб визначити, як довго зберігати дані Telescope. Наприклад, така команда видалить усі записи, створені понад 48 годин тому:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### Авторизація панелі

Панель Telescope доступна за маршрутом `/telescope`. За замовчуванням ви зможете відкрити її лише в середовищі `local`. У вашому файлі `app/Providers/TelescopeServiceProvider.php` є визначення [гейта авторизації](/docs/{{version}}/authorization#gates). Цей гейт керує доступом до Telescope у **нелокальних** середовищах. Ви вільні змінювати його як потрібно, щоб обмежити доступ до вашої установки Telescope:

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> Обов'язково змініть у продакшн-середовищі змінну оточення `APP_ENV` на `production`. Інакше ваша установка Telescope буде публічно доступною.

<a name="upgrading-telescope"></a>
## Оновлення Telescope

Оновлюючись до нової мажорної версії Telescope, обов'язково уважно перегляньте [посібник з оновлення](https://github.com/laravel/telescope/blob/master/UPGRADE.md).

Крім того, оновлюючись до будь-якої нової версії Telescope, повторно опублікуйте його ресурси:

```shell
php artisan telescope:publish
```

Щоб тримати ресурси актуальними й уникнути проблем у майбутніх оновленнях, ви можете додати команду `vendor:publish --tag=laravel-assets` до скриптів `post-update-cmd` у файлі `composer.json` вашого застосунку:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="filtering"></a>
## Фільтрація

<a name="filtering-entries"></a>
### Записи

Ви можете фільтрувати дані, які записує Telescope, через замикання `filter`, визначене у вашому класі `App\Providers\TelescopeServiceProvider`. За замовчуванням це замикання записує всі дані в середовищі `local`, а в решті середовищ - винятки, провалені завдання, заплановані завдання й дані з відстежуваними тегами:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a name="filtering-batches"></a>
### Пакети

Якщо замикання `filter` фільтрує дані для окремих записів, то метод `filterBatch` дозволяє зареєструвати замикання, яке фільтрує всі дані для заданого запиту чи консольної команди. Якщо замикання поверне `true`, Telescope запише всі записи:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a name="tagging"></a>
## Теги

Telescope дозволяє шукати записи за «тегом». Часто теги - це імена класів моделей Eloquent чи ID автентифікованих користувачів, які Telescope додає до записів автоматично. Іноді вам може знадобитися прикріпити до записів власні теги. Для цього скористайтеся методом `Telescope::tag`. Метод `tag` приймає замикання, яке має повернути масив тегів. Повернені замиканням теги буде об'єднано з тими, які Telescope додав би до запису автоматично. Зазвичай метод `tag` викликають у методі `register` вашого класу `App\Providers\TelescopeServiceProvider`:

```php
use Laravel\Telescope\EntryType;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === EntryType::REQUEST
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
}
```

<a name="available-watchers"></a>
## Доступні спостерігачі

«Спостерігачі» (watchers) Telescope збирають дані застосунку під час виконання запиту чи консольної команди. Ви можете налаштувати список спостерігачів, які хочете ввімкнути, у своєму конфігураційному файлі `config/telescope.php`:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

Деякі спостерігачі дозволяють також задати додаткові опції налаштування:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],
```

<a name="batch-watcher"></a>
### Спостерігач пакетів

Спостерігач пакетів записує інформацію про [пакети](/docs/{{version}}/queues#job-batching) у чергах, зокрема дані про завдання та підключення.

<a name="cache-watcher"></a>
### Спостерігач кешу

Спостерігач кешу записує дані, коли ключ кешу знайдено, не знайдено, оновлено чи забуто.

<a name="command-watcher"></a>
### Спостерігач команд

Спостерігач команд записує аргументи, опції, код виходу та вивід щоразу, коли виконується артизан-команда. Якщо ви хочете виключити певні команди із запису, вкажіть їх в опції `ignore` у своєму файлі `config/telescope.php`:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],
```

<a name="dump-watcher"></a>
### Спостерігач дампів

Спостерігач дампів записує й показує ваші дампи змінних у Telescope. У Laravel змінні можна дампити глобальною функцією `dump`. Щоб дамп було записано, вкладка спостерігача дампів має бути відкрита у браузері - інакше спостерігач ігноруватиме дампи.

<a name="event-watcher"></a>
### Спостерігач подій

Спостерігач подій записує дані, слухачів і дані бродкастингу для всіх [подій](/docs/{{version}}/events), відправлених вашим застосунком. Внутрішні події фреймворку Laravel спостерігач подій ігнорує.

<a name="exception-watcher"></a>
### Спостерігач винятків

Спостерігач винятків записує дані та стек викликів для всіх винятків вашого застосунку, які підлягають звітуванню.

<a name="gate-watcher"></a>
### Спостерігач гейтів

Спостерігач гейтів записує дані та результат перевірок [гейтів і політик](/docs/{{version}}/authorization) у вашому застосунку. Якщо ви хочете виключити певні можливості із запису, вкажіть їх в опції `ignore_abilities` у своєму файлі `config/telescope.php`:

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],
```

<a name="http-client-watcher"></a>
### Спостерігач HTTP-клієнта

Спостерігач HTTP-клієнта записує вихідні [запити HTTP-клієнта](/docs/{{version}}/http-client), які робить ваш застосунок.

<a name="job-watcher"></a>
### Спостерігач завдань

Спостерігач завдань записує дані та статус усіх [завдань](/docs/{{version}}/queues), відправлених вашим застосунком.

<a name="log-watcher"></a>
### Спостерігач логів

Спостерігач логів записує [дані логу](/docs/{{version}}/logging) для всіх записів, які створює ваш застосунок.

За замовчуванням Telescope записує лише логи рівня `error` і вище. Проте ви можете змінити опцію `level` у конфігураційному файлі `config/telescope.php` вашого застосунку, щоб змінити цю поведінку:

```php
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a name="mail-watcher"></a>
### Спостерігач пошти

Спостерігач пошти дозволяє переглянути у браузері попередній вигляд [листів](/docs/{{version}}/mail), надісланих вашим застосунком, разом із пов'язаними даними. Ви також можете завантажити лист як файл `.eml`.

<a name="model-watcher"></a>
### Спостерігач моделей

Спостерігач моделей записує зміни моделей щоразу, коли відправляється [подія моделі](/docs/{{version}}/eloquent#events) Eloquent. Ви можете вказати, які саме події моделей слід записувати, через опцію `events` цього спостерігача:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

Якщо ви хочете записувати кількість моделей, створених із даних під час заданого запиту, увімкніть опцію `hydrations`:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],
```

<a name="notification-watcher"></a>
### Спостерігач сповіщень

Спостерігач сповіщень записує всі [сповіщення](/docs/{{version}}/notifications), надіслані вашим застосунком. Якщо сповіщення спричиняє надсилання листа й у вас увімкнено спостерігач пошти, лист також буде доступний для перегляду на екрані спостерігача пошти.

<a name="query-watcher"></a>
### Спостерігач запитів до бази

Спостерігач запитів записує сирий SQL, прив'язки та час виконання всіх запитів, які виконує ваш застосунок. Спостерігач також позначає тегом `slow` усі запити, повільніші за 100 мілісекунд. Ви можете змінити поріг повільного запиту через опцію `slow` цього спостерігача:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],
```

<a name="redis-watcher"></a>
### Спостерігач Redis

Спостерігач Redis записує всі команди [Redis](/docs/{{version}}/redis), які виконує ваш застосунок. Якщо ви використовуєте Redis для кешування, спостерігач Redis записуватиме й команди кешу.

<a name="request-watcher"></a>
### Спостерігач запитів

Спостерігач запитів записує запит, заголовки, сесію та дані відповіді для всіх запитів, які обробляє застосунок. Ви можете обмежити обсяг записуваних даних відповіді опцією `size_limit` (у кілобайтах):

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],
```

<a name="schedule-watcher"></a>
### Спостерігач планувальника

Спостерігач планувальника записує команду та вивід усіх [запланованих завдань](/docs/{{version}}/scheduling), які виконує ваш застосунок.

<a name="view-watcher"></a>
### Спостерігач представлень

Спостерігач представлень записує ім'я, шлях, дані та «композери» [представлення](/docs/{{version}}/views), використані під час рендерингу.

<a name="displaying-user-avatars"></a>
## Показ аватарів користувачів

Панель Telescope показує аватар користувача, який був автентифікований на момент збереження запису. За замовчуванням Telescope отримує аватари через вебсервіс Gravatar. Проте ви можете налаштувати URL аватара, зареєструвавши колбек у вашому класі `App\Providers\TelescopeServiceProvider`. Колбек отримає ID та адресу електронної пошти користувача й має повернути URL зображення аватара:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}
```
