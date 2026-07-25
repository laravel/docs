---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Логування

- [Вступ](#introduction)
- [Конфігурація](#configuration)
    - [Доступні драйвери каналів](#available-channel-drivers)
    - [Передумови каналів](#channel-prerequisites)
    - [Логування попереджень про застарілість](#logging-deprecation-warnings)
- [Створення стеків логів](#building-log-stacks)
- [Запис повідомлень до логу](#writing-log-messages)
    - [Контекстна інформація](#contextual-information)
    - [Запис до конкретних каналів](#writing-to-specific-channels)
- [Налаштування каналів Monolog](#monolog-channel-customization)
    - [Налаштування Monolog для каналів](#customizing-monolog-for-channels)
    - [Створення каналів з обробниками Monolog](#creating-monolog-handler-channels)
    - [Створення власних каналів через фабрики](#creating-custom-channels-via-factories)
- [Стеження за логами за допомогою Pail](#tailing-log-messages-using-pail)
    - [Встановлення](#pail-installation)
    - [Використання](#pail-usage)
    - [Фільтрування логів](#pail-filtering-logs)

<a name="introduction"></a>
## Вступ

Щоб допомогти вам дізнатися більше про те, що відбувається всередині вашого застосунку, Laravel надає надійні сервіси логування, які дозволяють записувати повідомлення у файли, системний лог помилок і навіть у Slack, щоб сповістити всю вашу команду.

Логування Laravel побудоване на «каналах». Кожен канал представляє конкретний спосіб запису інформації логу. Наприклад, канал `single` пише логи в один файл, тоді як канал `slack` надсилає повідомлення до Slack. Повідомлення можуть записуватися до кількох каналів залежно від їхньої серйозності.

Під капотом Laravel використовує бібліотеку [Monolog](https://github.com/Seldaek/monolog), яка підтримує різноманітні потужні обробники логів. Laravel робить налаштування цих обробників дуже простим, дозволяючи комбінувати їх, щоб налаштувати обробку логів вашого застосунку.

<a name="configuration"></a>
## Конфігурація

Усі опції конфігурації, що керують поведінкою логування вашого застосунку, містяться у файлі `config/logging.php`. Цей файл дозволяє налаштувати канали логування, тож обов'язково перегляньте кожен доступний канал і його опції. Кілька поширених опцій ми розглянемо нижче.

За замовчуванням Laravel використовує канал `stack` для запису повідомлень. Канал `stack` слугує для об'єднання кількох каналів логування в один. Докладніше про створення стеків читайте в [документації нижче](#building-log-stacks).

<a name="available-channel-drivers"></a>
### Доступні драйвери каналів

Кожен канал логування працює на «драйвері». Драйвер визначає, як і де насправді записується повідомлення. Наведені нижче драйвери каналів доступні в кожному застосунку Laravel. Запис для більшості з них уже присутній у вашому файлі `config/logging.php`, тож обов'язково перегляньте його вміст:

<div class="overflow-auto">

| Назва        | Опис                                                                 |
| ------------ | -------------------------------------------------------------------- |
| `custom`     | Драйвер, що викликає вказану фабрику для створення каналу.           |
| `daily`      | Драйвер Monolog на основі `RotatingFileHandler` із щоденною ротацією. |
| `errorlog`   | Драйвер Monolog на основі `ErrorLogHandler`.                         |
| `monolog`    | Фабричний драйвер Monolog, що може використовувати будь-який підтримуваний обробник. |
| `papertrail` | Драйвер Monolog на основі `SyslogUdpHandler`.                        |
| `single`     | Канал логера на основі одного файлу чи шляху (`StreamHandler`).      |
| `slack`      | Драйвер Monolog на основі `SlackWebhookHandler`.                     |
| `stack`      | Обгортка для створення «багатоканальних» каналів.                    |
| `syslog`     | Драйвер Monolog на основі `SyslogHandler`.                           |

</div>

> [!NOTE]
> Перегляньте документацію з [розширеного налаштування каналів](#monolog-channel-customization), щоб дізнатися більше про драйвери `monolog` і `custom`.

<a name="configuring-the-channel-name"></a>
#### Налаштування імені каналу

За замовчуванням Monolog створюється з «іменем каналу», що відповідає поточному середовищу - наприклад, `production` чи `local`. Щоб змінити це значення, додайте до конфігурації каналу опцію `name`:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### Передумови каналів

<a name="configuring-the-single-and-daily-channels"></a>
#### Налаштування каналів single і daily

Канали `single` та `daily` мають три необов'язкові опції конфігурації: `bubble`, `permission` і `locking`.

<div class="overflow-auto">

| Назва        | Опис                                                                          | За замовчуванням |
| ------------ | ----------------------------------------------------------------------------- | ------- |
| `bubble`     | Вказує, чи мають повідомлення після обробки підніматися до інших каналів.      | `true`  |
| `locking`    | Спробувати заблокувати файл логу перед записом до нього.                       | `false` |
| `permission` | Права доступу до файлу логу.                                                   | `0644`  |

</div>

Крім того, політику зберігання для каналу `daily` можна налаштувати змінною середовища `LOG_DAILY_DAYS` або опцією конфігурації `days`.

<div class="overflow-auto">

| Назва  | Опис                                                        | За замовчуванням |
| ------ | ----------------------------------------------------------- | ------- |
| `days` | Кількість днів, протягом яких зберігаються щоденні файли логів. | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Налаштування каналу Papertrail

Канал `papertrail` потребує опцій конфігурації `host` і `port`. Їх можна задати змінними середовища `PAPERTRAIL_URL` і `PAPERTRAIL_PORT`. Ці значення можна отримати в [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app).

<a name="configuring-the-slack-channel"></a>
#### Налаштування каналу Slack

Канал `slack` потребує опції конфігурації `url`. Це значення можна задати змінною середовища `LOG_SLACK_WEBHOOK_URL`. Ця адреса має відповідати URL [вхідного вебхука](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks), налаштованого для вашої команди в Slack.

За замовчуванням Slack отримуватиме лише логи рівня `critical` і вище; утім, ви можете змінити це змінною середовища `LOG_LEVEL` або опцією `level` у масиві конфігурації вашого каналу Slack.

<a name="logging-deprecation-warnings"></a>
### Логування попереджень про застарілість

PHP, Laravel та інші бібліотеки часто сповіщають користувачів, що деякі їхні можливості застаріли й будуть вилучені в майбутній версії. Якщо ви хочете логувати ці попередження, вкажіть бажаний канал `deprecations` змінною середовища `LOG_DEPRECATIONS_CHANNEL` або у файлі `config/logging.php` вашого застосунку:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

Або ж ви можете визначити канал логування з іменем `deprecations`. Якщо канал із таким іменем існує, він завжди використовуватиметься для логування попереджень про застарілість:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## Створення стеків логів

Як згадувалося раніше, драйвер `stack` дозволяє для зручності поєднати кілька каналів в один. Щоб проілюструвати використання стеків, погляньмо на приклад конфігурації, яку ви можете побачити в продакшен-застосунку:

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'], // [tl! add]
        'ignore_exceptions' => false,
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => env('LOG_LEVEL', 'debug'),
        'facility' => env('LOG_SYSLOG_FACILITY', LOG_USER),
        'replace_placeholders' => true,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => env('LOG_SLACK_USERNAME', 'Laravel Log'),
        'emoji' => env('LOG_SLACK_EMOJI', ':boom:'),
        'level' => env('LOG_LEVEL', 'critical'),
        'replace_placeholders' => true,
    ],
],
```

Розберімо цю конфігурацію. Спершу зверніть увагу, що наш канал `stack` об'єднує два інші канали через опцію `channels`: `syslog` і `slack`. Тож під час запису повідомлень обидва ці канали матимуть змогу його залогувати. Однак, як ми побачимо нижче, чи справді вони це зроблять, залежить від серйозності повідомлення, тобто його «рівня».

<a name="log-levels"></a>
#### Рівні логування

Зверніть увагу на опцію `level` у конфігураціях каналів `syslog` і `slack` у прикладі вище. Вона визначає мінімальний «рівень», якого має досягти повідомлення, щоб канал його залогував. Monolog, на якому працюють сервіси логування Laravel, пропонує всі рівні, визначені у [специфікації RFC 5424](https://tools.ietf.org/html/rfc5424). У порядку спадання серйозності це: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** і **debug**.

Тож уявімо, що ми логуємо повідомлення методом `debug`:

```php
Log::debug('An informational message.');
```

За нашої конфігурації канал `syslog` запише повідомлення до системного логу; однак оскільки це повідомлення не має рівня `critical` чи вищого, до Slack воно не потрапить. Натомість якщо ми залогуємо повідомлення рівня `emergency`, воно потрапить і до системного логу, і до Slack, адже рівень `emergency` вищий за мінімальний поріг обох каналів:

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## Запис повідомлень до логу

Ви можете записувати інформацію до логів за допомогою [фасаду](/docs/{{version}}/facades) `Log`. Як згадувалося раніше, логер надає вісім рівнів логування, визначених у [специфікації RFC 5424](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** і **debug**:

```php
use Illuminate\Support\Facades\Log;

Log::emergency($message);
Log::alert($message);
Log::critical($message);
Log::error($message);
Log::warning($message);
Log::notice($message);
Log::info($message);
Log::debug($message);
```

Ви можете викликати будь-який із цих методів, щоб залогувати повідомлення відповідного рівня. За замовчуванням повідомлення буде записано до типового каналу логування, налаштованого у вашому конфігураційному файлі `logging`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        Log::info('Showing the user profile for user: {id}', ['id' => $id]);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<a name="contextual-information"></a>
### Контекстна інформація

Методам логування можна передати масив контекстних даних. Ці дані буде відформатовано й показано разом із повідомленням логу:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

Подекуди вам може знадобитися вказати контекстну інформацію, яку слід додавати до всіх наступних записів логу в певному каналі. Наприклад, ви можете захотіти логувати ідентифікатор запиту, пов'язаний із кожним вхідним запитом до вашого застосунку. Для цього викличте метод `withContext` фасаду `Log`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        $response = $next($request);

        $response->headers->set('Request-Id', $requestId);

        return $response;
    }
}
```

Якщо ви хочете надати контекстну інформацію _всім_ каналам логування, викличте метод `Log::shareContext()`. Він передасть контекстну інформацію всім створеним каналам, а також усім каналам, створеним згодом:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::shareContext([
            'request-id' => $requestId
        ]);

        // ...
    }
}
```

> [!NOTE]
> Якщо вам потрібно ділитися контекстом логу під час обробки завдань у черзі, скористайтеся [`middleware` завдань](/docs/{{version}}/queues#job-middleware).

<a name="writing-to-specific-channels"></a>
### Запис до конкретних каналів

Іноді ви можете захотіти залогувати повідомлення до каналу, відмінного від типового каналу вашого застосунку. Скористайтеся методом `channel` фасаду `Log`, щоб отримати будь-який визначений у конфігурації канал і залогувати до нього:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

Якщо ви хочете створити стек логування на вимогу з кількох каналів, скористайтеся методом `stack`:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### Канали на вимогу

Також можна створити канал на вимогу, надавши конфігурацію під час виконання, без її присутності у файлі `logging` вашого застосунку. Для цього передайте масив конфігурації методу `build` фасаду `Log`:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

Ви також можете захотіти включити канал на вимогу до стека логування на вимогу. Це робиться додаванням екземпляра вашого каналу до масиву, переданого методу `stack`:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Налаштування каналів Monolog

<a name="customizing-monolog-for-channels"></a>
### Налаштування Monolog для каналів

Іноді вам може знадобитися повний контроль над тим, як Monolog налаштовано для наявного каналу. Наприклад, ви можете захотіти налаштувати власну реалізацію `FormatterInterface` для вбудованого каналу `single` від Laravel.

Щоб почати, визначте в конфігурації каналу масив `tap`. Він має містити список класів, які матимуть змогу налаштувати (тобто «підключитися» до) екземпляр Monolog після його створення. Загальноприйнятого місця для цих класів немає, тож ви вільні створити для них каталог у своєму застосунку:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

Налаштувавши опцію `tap` у своєму каналі, ви готові визначити клас, який налаштує ваш екземпляр Monolog. Цей клас потребує лише одного методу - `__invoke`, який отримує екземпляр `Illuminate\Log\Logger`. Цей екземпляр проксіює всі виклики методів до відповідного екземпляра Monolog:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
     */
    public function __invoke(Logger $logger): void
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```

> [!NOTE]
> Усі ваші класи «tap» розв'язуються через [сервіс-контейнер](/docs/{{version}}/container), тож будь-які потрібні їм залежності конструктора буде впроваджено автоматично.

<a name="creating-monolog-handler-channels"></a>
### Створення каналів з обробниками Monolog

Monolog має чимало [доступних обробників](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler), і Laravel не містить вбудованого каналу для кожного з них. У деяких випадках ви можете захотіти створити власний канал, який є просто екземпляром конкретного обробника Monolog без відповідного драйвера логування Laravel. Такі канали легко створити драйвером `monolog`.

Використовуючи драйвер `monolog`, опція конфігурації `handler` вказує, який обробник буде створено. За бажанням будь-які потрібні обробнику параметри конструктора можна задати опцією `handler_with`:

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'handler_with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a name="monolog-formatters"></a>
#### Форматувальники Monolog

Використовуючи драйвер `monolog`, типовим форматувальником буде `LineFormatter` від Monolog. Утім, ви можете налаштувати тип форматувальника, переданого обробнику, опціями `formatter` і `formatter_with`:

```php
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```

Якщо ви використовуєте обробник Monolog, здатний надати власний форматувальник, ви можете задати опції `formatter` значення `default`:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Процесори Monolog

Monolog також може обробляти повідомлення перед їх логуванням. Ви можете створити власні процесори або скористатися [наявними процесорами Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor).

Якщо ви хочете налаштувати процесори для драйвера `monolog`, додайте до конфігурації каналу значення `processors`:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // Simple syntax...
        Monolog\Processor\MemoryUsageProcessor::class,

        // With options...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### Створення власних каналів через фабрики

Якщо ви хочете визначити цілком власний канал, у якому маєте повний контроль над створенням і конфігурацією Monolog, вкажіть тип драйвера `custom` у файлі `config/logging.php`. Ваша конфігурація має містити опцію `via` з іменем класу фабрики, який буде викликано для створення екземпляра Monolog:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

Налаштувавши канал із драйвером `custom`, ви готові визначити клас, який створюватиме ваш екземпляр Monolog. Цей клас потребує лише одного методу `__invoke`, який має повертати екземпляр логера Monolog. Метод отримає масив конфігурації каналу як єдиний аргумент:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Стеження за логами за допомогою Pail

Часто вам може знадобитися стежити за логами застосунку в реальному часі - наприклад, коли ви налагоджуєте проблему чи відстежуєте певні типи помилок.

Laravel Pail - це пакет, який дозволяє легко зазирнути у файли логів вашого застосунку Laravel просто з командного рядка. На відміну від стандартної команди `tail`, Pail працює з будь-яким драйвером логування, зокрема [Laravel Nightwatch](https://nightwatch.laravel.com), Sentry чи Flare. Крім того, Pail надає набір корисних фільтрів, щоб швидко знайти те, що ви шукаєте.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### Встановлення

> [!WARNING]
> Laravel Pail потребує PHP-розширення [PCNTL](https://www.php.net/manual/en/book.pcntl.php).

Щоб почати, встановіть Pail у свій проєкт менеджером пакетів Composer:

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### Використання

Щоб почати стежити за логами, виконайте команду `pail`:

```shell
php artisan pail
```

Щоб збільшити докладність виводу й уникнути скорочення (…), скористайтеся опцією `-v`:

```shell
php artisan pail -v
```

Для максимальної докладності та показу стеків викликів винятків скористайтеся опцією `-vv`:

```shell
php artisan pail -vv
```

Щоб припинити стеження за логами, будь-коли натисніть `Ctrl+C`.

<a name="pail-filtering-logs"></a>
### Фільтрування логів

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

Опція `--filter` дозволяє фільтрувати логи за типом, файлом, повідомленням і вмістом стека викликів:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

Щоб фільтрувати логи лише за повідомленням, скористайтеся опцією `--message`:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

Опція `--level` дозволяє фільтрувати логи за їхнім [рівнем](#log-levels):

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

Щоб показувати лише логи, записані під час автентифікації певного користувача, передайте ідентифікатор цього користувача опції `--user`:

```shell
php artisan pail --user=1
```
