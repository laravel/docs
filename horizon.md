---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Horizon

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Конфігурація](#configuration)
    - [Авторизація панелі](#dashboard-authorization)
    - [Максимум спроб для завдання](#max-job-attempts)
    - [Тайм-аут завдання](#job-timeout)
    - [Затримка перед повтором](#job-backoff)
    - [Інші опції воркерів](#other-worker-options)
    - [Приглушені завдання](#silenced-jobs)
- [Стратегії балансування](#balancing-strategies)
    - [Автоматичне балансування](#auto-balancing)
    - [Просте балансування](#simple-balancing)
    - [Без балансування](#no-balancing)
- [Оновлення Horizon](#upgrading-horizon)
- [Запуск Horizon](#running-horizon)
    - [Розгортання Horizon](#deploying-horizon)
- [Теги](#tags)
- [Сповіщення](#notifications)
- [Метрики](#metrics)
- [Видалення провалених завдань](#deleting-failed-jobs)
- [Очищення завдань із черг](#clearing-jobs-from-queues)

<a name="introduction"></a>
## Вступ

> [!NOTE]
> Перш ніж заглиблюватися в Laravel Horizon, ознайомтеся з базовими [сервісами черг](/docs/{{version}}/queues) у Laravel. Horizon доповнює черги Laravel додатковими можливостями, які можуть заплутати, якщо ви ще не знайомі з основами черг у Laravel.

[Laravel Horizon](https://github.com/laravel/horizon) надає гарну панель керування та конфігурацію в коді для ваших [черг на Redis](/docs/{{version}}/queues) у Laravel. Horizon дозволяє легко стежити за ключовими метриками системи черг - як-от пропускна здатність, час виконання та провали завдань.

Коли ви користуєтеся Horizon, уся конфігурація воркерів черг зберігається в одному простому конфігураційному файлі. Описавши конфігурацію воркерів у файлі під контролем версій, ви можете легко масштабувати чи змінювати воркери черг вашого застосунку під час розгортання.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## Встановлення

> [!WARNING]
> Laravel Horizon вимагає, щоб ваші черги працювали на [Redis](https://redis.io). Тому переконайтеся, що підключення черги у вашому конфігураційному файлі `config/queue.php` має значення `redis`. Наразі Horizon не сумісний із Redis Cluster.

Ви можете встановити Horizon у свій проєкт через менеджер пакетів Composer:

```shell
composer require laravel/horizon
```

Після встановлення Horizon опублікуйте його ресурси артизан-командою `horizon:install`:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### Конфігурація

Після публікації ресурсів Horizon його основний конфігураційний файл буде розташований у `config/horizon.php`. Цей файл дозволяє налаштувати опції воркерів черг вашого застосунку. Кожна опція конфігурації супроводжується описом призначення, тож обов'язково ретельно перегляньте цей файл.

> [!WARNING]
> Horizon використовує всередині підключення Redis на ім'я `horizon`. Це ім'я зарезервоване й не має призначатися іншому підключенню Redis у конфігураційному файлі `database.php` чи як значення опції `use` у файлі `horizon.php`.

<a name="content-security-policy-csp-nonce"></a>
#### Nonce для Content Security Policy (CSP)

Якщо ви хочете використовувати [атрибут nonce](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce) на тегах script і style у представленнях Horizon у межах вашої [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), скористайтеся методом `Horizon::cspNonce`, щоб указати потрібний nonce. Зазвичай цей метод викликають у `middleware`, щоб для кожного запиту призначався новий nonce:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Horizon\Horizon;
use Symfony\Component\HttpFoundation\Response;

public function handle(Request $request, Closure $next): Response
{
    Horizon::cspNonce('csp-nonce');

    return $next($request);
}
```

Ви можете додати це `middleware` до опції `middleware` у конфігураційному файлі `config/horizon.php` вашого застосунку:

```php
'middleware' => [
    'web',
    App\Http\Middleware\AddHorizonCspNonce::class,
],
```

<a name="environments"></a>
#### Середовища

Після встановлення головна опція конфігурації Horizon, з якою вам варто ознайомитися, - `environments`. Ця опція є масивом середовищ, у яких працює ваш застосунок, і визначає опції процесів-воркерів для кожного з них. За замовчуванням цей запис містить середовища `production` і `local`. Проте ви вільні додати за потреби й інші:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],

    'local' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Ви також можете визначити середовище-джокер (`*`), яке буде використано, коли не знайдено жодного іншого відповідного середовища:

```php
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Коли ви запускаєте Horizon, він використає опції конфігурації процесів-воркерів для того середовища, у якому працює ваш застосунок. Зазвичай середовище визначається значенням [змінної оточення](/docs/{{version}}/configuration#determining-the-current-environment) `APP_ENV`. Наприклад, стандартне середовище Horizon `local` налаштоване запускати три процеси-воркери й автоматично балансувати їхню кількість між чергами. Стандартне середовище `production` налаштоване запускати максимум 10 процесів-воркерів і автоматично балансувати їхню кількість між чергами.

> [!WARNING]
> Переконайтеся, що частина `environments` вашого конфігураційного файлу `horizon` містить запис для кожного [середовища](/docs/{{version}}/configuration#environment-configuration), у якому ви плануєте запускати Horizon.

<a name="supervisors"></a>
#### Супервізори

Як видно зі стандартного конфігураційного файлу Horizon, кожне середовище може містити один чи кілька «супервізорів». За замовчуванням конфігураційний файл описує супервізор як `supervisor-1`; проте ви вільні називати супервізори як завгодно. Кожен супервізор, по суті, відповідає за «нагляд» за групою процесів-воркерів і дбає про балансування воркерів між чергами.

Ви можете додати до заданого середовища додаткові супервізори, якщо хочете описати нову групу процесів-воркерів для цього середовища. Це може знадобитися, якщо ви хочете задати іншу стратегію балансування чи кількість процесів-воркерів для певної черги вашого застосунку.

<a name="maintenance-mode"></a>
#### Режим обслуговування

Доки ваш застосунок перебуває в [режимі обслуговування](/docs/{{version}}/configuration#maintenance-mode), Horizon не оброблятиме завдань із черг, якщо в конфігураційному файлі Horizon опція супервізора `force` не має значення `true`:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'force' => true,
        ],
    ],
],
```

<a name="default-values"></a>
#### Значення за замовчуванням

У стандартному конфігураційному файлі Horizon ви помітите опцію `defaults`. Ця опція задає значення за замовчуванням для [супервізорів](#supervisors) вашого застосунку. Стандартні значення супервізора буде об'єднано з конфігурацією супервізора для кожного середовища, тож ви зможете уникнути зайвих повторів під час опису супервізорів.

<a name="dashboard-authorization"></a>
### Авторизація панелі

Панель Horizon доступна за маршрутом `/horizon`. За замовчуванням ви зможете відкрити її лише в середовищі `local`. Проте у вашому файлі `app/Providers/HorizonServiceProvider.php` є визначення [гейта авторизації](/docs/{{version}}/authorization#gates). Цей гейт керує доступом до Horizon у **нелокальних** середовищах. Ви вільні змінювати його як потрібно, щоб обмежити доступ до вашої установки Horizon:

```php
/**
 * Register the Horizon gate.
 *
 * This gate determines who can access Horizon in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewHorizon', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

<a name="alternative-authentication-strategies"></a>
#### Альтернативні стратегії автентифікації

Пам'ятайте, що Laravel автоматично впроваджує автентифікованого користувача в замикання гейта. Якщо ваш застосунок захищає Horizon іншим способом - наприклад, обмеженнями за IP, - вашим користувачам Horizon може не знадобитися «входити». Тому вам треба буде змінити сигнатуру замикання вище з `function (User $user)` на `function (User $user = null)`, щоб Laravel не вимагав автентифікації.

<a name="max-job-attempts"></a>
### Максимум спроб для завдання

> [!NOTE]
> Перш ніж налаштовувати ці опції, переконайтеся, що ви знайомі зі стандартними [сервісами черг](/docs/{{version}}/queues#max-job-attempts-and-timeout) у Laravel і з поняттям «спроб».

Ви можете задати максимальну кількість спроб, які може витратити завдання, у конфігурації супервізора:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'tries' => 10,
        ],
    ],
],
```

> [!NOTE]
> Ця опція подібна до опції `--tries` під час обробки черг артизан-командою.

Налаштування опції `tries` вкрай важливе, коли ви користуєтеся `middleware` на кшталт `WithoutOverlapping` чи `RateLimited`, адже вони витрачають спроби. Щоб це врахувати, підлаштуйте значення `tries` або на рівні супервізора, або через властивість `$tries` у класі завдання.

Якщо ви не задасте опцію `tries`, Horizon за замовчуванням використає одну спробу - хіба що клас завдання визначає `$tries`, що має перевагу над конфігурацією Horizon.

Значення `tries` чи `$tries`, встановлене в 0, дозволяє необмежену кількість спроб, що ідеально, коли кількість спроб наперед невідома. Щоб запобігти нескінченним провалам, ви можете обмежити кількість дозволених винятків, задавши властивість `$maxExceptions` у класі завдання.

<a name="job-timeout"></a>
### Тайм-аут завдання

Так само ви можете задати значення `timeout` на рівні супервізора - воно визначає, скільки секунд процес-воркер може виконувати завдання, перш ніж його буде примусово завершено. Після завершення завдання буде або повторено, або позначено як провалене - залежно від конфігурації вашої черги:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> Зі стратегією балансування `auto` Horizon вважатиме воркери, що виконують завдання, «завислими» й примусово вб'є їх після тайм-ауту Horizon під час зменшення масштабу. Завжди стежте, щоб тайм-аут Horizon був більшим за будь-який тайм-аут на рівні завдання, інакше завдання можуть бути перервані на середині виконання. Крім того, значення `timeout` завжди має бути щонайменше на кілька секунд меншим за значення `retry_after`, задане у вашому конфігураційному файлі `config/queue.php`. Інакше ваші завдання можуть бути оброблені двічі.

<a name="job-backoff"></a>
### Затримка перед повтором

Ви можете задати значення `backoff` на рівні супервізора, щоб указати, як довго Horizon має чекати, перш ніж повторити завдання, яке зіткнулося з необробленим винятком:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => 10,
        ],
    ],
],
```

Ви також можете налаштувати «експоненційні» затримки, передавши в `backoff` масив. У цьому прикладі затримка перед повтором становитиме 1 секунду для першої спроби, 5 секунд для другої, 10 секунд для третьої й 10 секунд для кожної наступної, якщо спроби ще лишилися:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => [1, 5, 10],
        ],
    ],
],
```

<a name="other-worker-options"></a>
### Інші опції воркерів

Окрім `tries`, `timeout` і `backoff`, кожен супервізор приймає ще кілька опцій, які керують поведінкою його процесів-воркерів і тим, коли їх автоматично перезапускати. Періодичний перезапуск воркерів - хороша практика для довготривалих процесів, адже вона допомагає захиститися від витоків пам'яті:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'memory' => 128,
            'maxJobs' => 1000,
            'maxTime' => 3600,
            'sleep' => 3,
            'rest' => 0,
            'nice' => 0,
        ],
    ],
],
```

<div class="content-list" markdown="1">

- `memory` визначає максимальний обсяг пам'яті в мегабайтах, який може спожити один процес-воркер, перш ніж його буде перезапущено. За замовчуванням це значення - `128`.
- `maxJobs` визначає кількість завдань, які воркер має обробити перед перезапуском. Значення `0` означає, що воркери не перезапускатимуться за кількістю оброблених завдань. За замовчуванням це значення - `0`.
- `maxTime` визначає кількість секунд, які воркер має пропрацювати перед перезапуском. Значення `0` означає, що воркери не перезапускатимуться за часом. За замовчуванням це значення - `0`.
- `sleep` визначає кількість секунд, які воркер має почекати за відсутності завдань, перш ніж знову опитати чергу. За замовчуванням це значення - `3`.
- `rest` визначає кількість секунд паузи між обробкою кожного завдання. За замовчуванням це значення - `0`.
- `nice` визначає «люб'язність» (пріоритет планування) процесів-воркерів. Вище значення дає процесу нижчий пріоритет. За замовчуванням це значення - `0`.

</div>

<a name="silenced-jobs"></a>
### Приглушені завдання

Іноді вам можуть бути нецікаві певні завдання, які відправляє ваш застосунок чи сторонні пакети. Замість того щоб вони займали місце у вашому списку «Completed Jobs», ви можете їх приглушити. Для початку додайте ім'я класу завдання до опції конфігурації `silenced` у файлі `horizon` вашого застосунку:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

Окрім приглушення окремих класів завдань, Horizon підтримує також приглушення за [тегами](#tags). Це стане в пригоді, якщо ви хочете сховати кілька завдань зі спільним тегом:

```php
'silenced_tags' => [
    'notifications'
],
```

Або ж завдання, яке ви хочете приглушити, може реалізувати інтерфейс `Laravel\Horizon\Contracts\Silenced`. Якщо завдання реалізує цей інтерфейс, його буде приглушено автоматично, навіть якщо його немає в масиві конфігурації `silenced`:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## Стратегії балансування

Кожен супервізор може обробляти одну чи кілька черг, але, на відміну від стандартної системи черг Laravel, Horizon дозволяє обрати одну з трьох стратегій балансування воркерів: `auto`, `simple` та `false`.

<a name="auto-balancing"></a>
### Автоматичне балансування

Стратегія `auto`, яка є стандартною, підлаштовує кількість процесів-воркерів на чергу відповідно до її поточного навантаження. Наприклад, якщо у вашій черзі `notifications` 1000 завдань в очікуванні, а черга `default` порожня, Horizon виділить більше воркерів на чергу `notifications`, доки та не спорожніє.

Зі стратегією `auto` ви можете також налаштувати опції конфігурації `minProcesses` та `maxProcesses`:

<div class="content-list" markdown="1">

- `minProcesses` визначає мінімальну кількість процесів-воркерів на чергу. Це значення має бути більшим за 1 або дорівнювати йому.
- `maxProcesses` визначає максимальну загальну кількість процесів-воркерів, до якої Horizon може масштабуватися по всіх чергах. Зазвичай це значення має бути більшим за кількість черг, помножену на `minProcesses`. Щоб супервізор не породжував жодних процесів, ви можете задати тут 0.

</div>

Наприклад, ви можете налаштувати Horizon тримати щонайменше один процес на чергу й масштабуватися до 10 процесів-воркерів загалом:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default', 'notifications'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
],
```

Опція конфігурації `autoScalingStrategy` визначає, як Horizon призначатиме чергам більше процесів-воркерів. Ви можете обрати одну з двох стратегій:

<div class="content-list" markdown="1">

- Стратегія `time` призначатиме воркерів за загальним оцінюваним часом, потрібним, щоб розібрати чергу.
- Стратегія `size` призначатиме воркерів за загальною кількістю завдань у черзі.

</div>

Значення конфігурації `balanceMaxShift` і `balanceCooldown` визначають, як швидко Horizon масштабуватиметься під потребу у воркерах. У прикладі вище щотри секунди створюватиметься чи знищуватиметься максимум один новий процес. Ви вільні підлаштувати ці значення під потреби вашого застосунку.

<a name="auto-queue-priorities"></a>
#### Пріоритети черг і автоматичне балансування

Зі стратегією балансування `auto` Horizon не забезпечує суворого пріоритету між чергами. Порядок черг у конфігурації супервізора не впливає на те, як призначаються процеси-воркери. Натомість Horizon спирається на обрану `autoScalingStrategy`, щоб динамічно розподіляти процеси-воркери за навантаженням черг.

Наприклад, у наведеній нижче конфігурації черга high не має пріоритету над чергою default, попри те що стоїть у списку першою:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['high', 'default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

Якщо вам потрібен відносний пріоритет між чергами, ви можете описати кілька супервізорів і явно розподілити обчислювальні ресурси:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
        'supervisor-2' => [
            // ...
            'queue' => ['images'],
            'minProcesses' => 1,
            'maxProcesses' => 1,
        ],
    ],
],
```

У цьому прикладі черга default може масштабуватися до 10 процесів, тоді як черга `images` обмежена одним процесом. Така конфігурація гарантує, що ваші черги масштабуватимуться незалежно.

> [!NOTE]
> Відправляючи ресурсомісткі завдання, іноді найкраще призначити їм окрему чергу з обмеженим значенням `maxProcesses`. Інакше ці завдання можуть з'їсти надмірно багато ресурсів CPU й перевантажити вашу систему.

<a name="simple-balancing"></a>
### Просте балансування

Стратегія `simple` розподіляє процеси-воркери рівномірно між указаними чергами. З цією стратегією Horizon не масштабує кількість процесів-воркерів автоматично, а використовує фіксовану кількість:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => 'simple',
            'processes' => 10,
        ],
    ],
],
```

У прикладі вище Horizon призначить кожній черзі по 5 процесів, розділивши загальні 10 порівну.

Якщо ви хочете керувати кількістю процесів-воркерів для кожної черги окремо, опишіть кілька супервізорів:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'balance' => 'simple',
            'processes' => 10,
        ],
        'supervisor-notifications' => [
            // ...
            'queue' => ['notifications'],
            'balance' => 'simple',
            'processes' => 2,
        ],
    ],
],
```

За такої конфігурації Horizon призначить 10 процесів черзі `default` і 2 процеси черзі `notifications`.

<a name="no-balancing"></a>
### Без балансування

Коли опція `balance` має значення `false`, Horizon обробляє черги строго в тому порядку, у якому їх перелічено, - подібно до стандартної системи черг Laravel. Проте він усе одно масштабуватиме кількість процесів-воркерів, якщо завдання почнуть накопичуватися:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => false,
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

У прикладі вище завдання з черги `default` завжди матимуть пріоритет над завданнями з черги `notifications`. Наприклад, якщо в `default` 1000 завдань, а в `notifications` лише 10, Horizon повністю обробить усі завдання `default`, перш ніж візьметься за `notifications`.

Ви можете керувати здатністю Horizon масштабувати процеси-воркери через опції `minProcesses` та `maxProcesses`:

<div class="content-list" markdown="1">

- `minProcesses` визначає мінімальну загальну кількість процесів-воркерів. Це значення має бути більшим за 1 або дорівнювати йому.
- `maxProcesses` визначає максимальну загальну кількість процесів-воркерів, до якої Horizon може масштабуватися.

</div>

<a name="upgrading-horizon"></a>
## Оновлення Horizon

Оновлюючись до нової мажорної версії Horizon, обов'язково уважно перегляньте [посібник з оновлення](https://github.com/laravel/horizon/blob/master/UPGRADE.md).

<a name="running-horizon"></a>
## Запуск Horizon

Коли ви налаштували супервізори й воркери в конфігураційному файлі `config/horizon.php` вашого застосунку, запустіть Horizon артизан-командою `horizon`. Ця єдина команда запустить усі налаштовані процеси-воркери для поточного середовища:

```shell
php artisan horizon
```

Ви можете призупинити процес Horizon і знову дозволити йому обробляти завдання артизан-командами `horizon:pause` та `horizon:continue`:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

Ви також можете призупиняти й продовжувати роботу окремих [супервізорів](#supervisors) Horizon артизан-командами `horizon:pause-supervisor` та `horizon:continue-supervisor`:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Перевірити поточний стан процесу Horizon можна артизан-командою `horizon:status`:

```shell
php artisan horizon:status
```

Перевірити поточний стан окремого [супервізора](#supervisors) Horizon можна артизан-командою `horizon:supervisor-status`:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Ви можете плавно завершити процес Horizon артизан-командою `horizon:terminate`. Усі завдання, які наразі обробляються, буде завершено, після чого Horizon зупиниться:

```shell
php artisan horizon:terminate
```

<a name="automatically-restarting-horizon"></a>
#### Автоматичний перезапуск Horizon

Під час локальної розробки ви можете запускати команду `horizon:listen`. Із командою `horizon:listen` вам не доведеться вручну перезапускати Horizon, щоб підхопити оновлений код. Перш ніж користуватися цією можливістю, переконайтеся, що у вашому локальному середовищі розробки встановлено [Node](https://nodejs.org). Крім того, встановіть у своєму проєкті бібліотеку стеження за файлами [Chokidar](https://github.com/paulmillr/chokidar):

```shell
npm install --save-dev chokidar
```

Коли Chokidar встановлено, ви можете запускати Horizon командою `horizon:listen`:

```shell
php artisan horizon:listen
```

Працюючи в Docker чи Vagrant, скористайтеся опцією `--poll`:

```shell
php artisan horizon:listen --poll
```

Ви можете налаштувати каталоги й файли, за якими слід стежити, через опцію конфігурації `watch` у файлі `config/horizon.php` вашого застосунку:

```php
'watch' => [
    'app',
    'bootstrap',
    'config',
    'database',
    'public/**/*.php',
    'resources/**/*.php',
    'routes',
    'composer.lock',
    '.env',
],
```

<a name="deploying-horizon"></a>
### Розгортання Horizon

Коли ви готові розгорнути Horizon на справжньому сервері вашого застосунку, налаштуйте монітор процесів, який стежитиме за командою `php artisan horizon` і перезапускатиме її, якщо та несподівано завершиться. Не хвилюйтеся - нижче ми розповімо, як встановити монітор процесів.

Під час розгортання застосунку вам слід дати процесу Horizon команду завершитися, щоб монітор процесів перезапустив його вже з вашими змінами в коді:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Встановлення Supervisor

Supervisor - це монітор процесів для Linux, який автоматично перезапустить ваш процес `horizon`, якщо той зупиниться. Щоб встановити Supervisor на Ubuntu, скористайтеся такою командою. Якщо ви не на Ubuntu, ви, найімовірніше, зможете встановити Supervisor через менеджер пакетів вашої операційної системи:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Якщо налаштування Supervisor власноруч видається надто складним, розгляньте [Laravel Cloud](https://cloud.laravel.com), який може керувати фоновими процесами ваших застосунків Laravel.

<a name="supervisor-configuration"></a>
#### Конфігурація Supervisor

Конфігураційні файли Supervisor зазвичай зберігаються в каталозі `/etc/supervisor/conf.d` вашого сервера. У цьому каталозі ви можете створити будь-яку кількість файлів, які вказують supervisor, як стежити за вашими процесами. Створімо, наприклад, файл `horizon.conf`, який запускає процес `horizon` і стежить за ним:

```ini
[program:horizon]
process_name=%(program_name)s
command=php /home/forge/example.com/artisan horizon
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/horizon.log
stopwaitsecs=3600
```

Описуючи конфігурацію Supervisor, переконайтеся, що значення `stopwaitsecs` більше за кількість секунд, які займає ваше найдовше завдання. Інакше Supervisor може вбити завдання до того, як його буде оброблено.

> [!WARNING]
> Хоча наведені вище приклади підходять для серверів на Ubuntu, розташування й розширення конфігураційних файлів Supervisor можуть відрізнятися в інших серверних операційних системах. Докладніше читайте в документації до вашого сервера.

<a name="starting-supervisor"></a>
#### Запуск Supervisor

Коли конфігураційний файл створено, ви можете оновити конфігурацію Supervisor і запустити процеси під наглядом такими командами:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Докладніше про роботу з Supervisor читайте в [документації Supervisor](http://supervisord.org/index.html).

<a name="tags"></a>
## Теги

Horizon дозволяє призначати завданням «теги» - зокрема поштовим класам, подіям бродкастингу, сповіщенням і слухачам подій у черзі. Ба більше, Horizon розумно й автоматично проставляє теги більшості завдань залежно від моделей Eloquent, прикріплених до завдання. Погляньте, наприклад, на таке завдання:

```php
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class RenderVideo implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...
    }
}
```

Якщо це завдання поставлено в чергу з екземпляром `App\Models\Video`, чий атрибут `id` дорівнює `1`, воно автоматично отримає тег `App\Models\Video:1`. Так стається тому, що Horizon шукає у властивостях завдання будь-які моделі Eloquent. Якщо їх знайдено, Horizon розумно проставляє тег за іменем класу моделі та її первинним ключем:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### Ручне проставляння тегів завданням

Якщо ви хочете задати теги для одного зі своїх об'єктів у черзі вручну, визначте в його класі метод `tags`:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the job.
     *
     * @return array<int, string>
     */
    public function tags(): array
    {
        return ['render', 'video:'.$this->video->id];
    }
}
```

<a name="manually-tagging-event-listeners"></a>
#### Ручне проставляння тегів слухачам подій

Отримуючи теги для слухача подій у черзі, Horizon автоматично передасть екземпляр події до методу `tags`, тож ви зможете додати дані події до тегів:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the listener.
     *
     * @return array<int, string>
     */
    public function tags(VideoRendered $event): array
    {
        return ['video:'.$event->video->id];
    }
}
```

<a name="notifications"></a>
## Сповіщення

> [!WARNING]
> Налаштовуючи Horizon на надсилання сповіщень у Slack чи SMS, перегляньте [передумови для відповідного каналу сповіщень](/docs/{{version}}/notifications).

Якщо ви хочете отримувати сповіщення, коли в одній із ваших черг довгий час очікування, скористайтеся методами `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo` та `Horizon::routeSmsNotificationsTo`. Викликати ці методи можна в методі `boot` вашого `App\Providers\HorizonServiceProvider`:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Horizon::routeSmsNotificationsTo('15556667777');
    Horizon::routeMailNotificationsTo('example@example.com');
    Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
}
```

<a name="configuring-notification-wait-time-thresholds"></a>
#### Налаштування порогів часу очікування для сповіщень

Ви можете налаштувати, скільки секунд вважається «довгим очікуванням», у конфігураційному файлі `config/horizon.php` вашого застосунку. Опція конфігурації `waits` у цьому файлі дозволяє задати поріг довгого очікування для кожної комбінації підключення / черги. Для не описаних комбінацій підключення / черги поріг за замовчуванням становитиме 60 секунд:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

Поріг черги, встановлений у `0`, вимкне сповіщення про довге очікування для цієї черги.

<a name="metrics"></a>
## Метрики

Horizon містить панель метрик, яка показує інформацію про час очікування й пропускну здатність ваших завдань і черг. Щоб наповнити цю панель, налаштуйте артизан-команду Horizon `snapshot` на запуск щоп'ять хвилин у файлі `routes/console.php` вашого застосунку:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

Ви можете налаштувати, скільки знімків Horizon зберігає для своїх графіків метрик, через опцію `metrics.trim_snapshots` у конфігураційному файлі `config/horizon.php` вашого застосунку. Оскільки ця опція обмежує кількість знімків, а не їхній вік, період зберігання залежить від того, як часто виконується команда `horizon:snapshot`:

```php
'metrics' => [
    'trim_snapshots' => [
        'job' => 24,
        'queue' => 24,
    ],
],
```

Якщо ви хочете видалити всі дані метрик, викличте артизан-команду `horizon:clear-metrics`:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## Видалення провалених завдань

Якщо ви хочете видалити провалене завдання, скористайтеся командою `horizon:forget`. Команда `horizon:forget` приймає єдиним аргументом ID чи UUID проваленого завдання:

```shell
php artisan horizon:forget 5
```

Якщо ви хочете видалити всі провалені завдання, додайте до команди `horizon:forget` опцію `--all`:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## Очищення завдань із черг

Якщо ви хочете видалити всі завдання зі стандартної черги вашого застосунку, скористайтеся артизан-командою `horizon:clear`:

```shell
php artisan horizon:clear
```

Ви можете додати опцію `queue`, щоб видалити завдання з конкретної черги:

```shell
php artisan horizon:clear --queue=emails
```
