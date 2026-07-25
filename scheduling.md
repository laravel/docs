---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Планування завдань

- [Вступ](#introduction)
- [Опис розкладу](#defining-schedules)
    - [Планування команд Artisan](#scheduling-artisan-commands)
    - [Планування завдань у черзі](#scheduling-queued-jobs)
    - [Планування команд оболонки](#scheduling-shell-commands)
    - [Варіанти частоти розкладу](#schedule-frequency-options)
    - [Часові пояси](#timezones)
    - [Запобігання накладанню завдань](#preventing-task-overlaps)
    - [Виконання завдань на одному сервері](#running-tasks-on-one-server)
    - [Фонові завдання](#background-tasks)
    - [Режим обслуговування](#maintenance-mode)
    - [Призупинення запланованих завдань](#pausing-scheduled-tasks)
    - [Групи розкладу](#schedule-groups)
- [Запуск планувальника](#running-the-scheduler)
    - [Завдання частіше ніж раз на хвилину](#sub-minute-scheduled-tasks)
    - [Запуск планувальника локально](#running-the-scheduler-locally)
- [Вивід завдань](#task-output)
- [Хуки завдань](#task-hooks)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Раніше ви, можливо, писали запис у конфігурації cron для кожного завдання, яке треба було запланувати на сервері. Проте це швидко стає болючим, адже ваш розклад завдань більше не під контролем версій, і вам доводиться заходити на сервер через SSH, щоб переглянути наявні записи cron чи додати нові.

Планувальник команд Laravel пропонує свіжий підхід до керування запланованими завданнями на вашому сервері. Планувальник дозволяє плавно й виразно описати розклад команд усередині самого застосунку Laravel. Коли ви користуєтеся планувальником, на сервері потрібен лише один запис cron. Розклад завдань зазвичай описують у файлі `routes/console.php` вашого застосунку.

<a name="defining-schedules"></a>
## Опис розкладу

Ви можете описати всі свої заплановані завдання у файлі `routes/console.php`. Для початку погляньмо на приклад. У ньому ми заплануємо виклик замикання щодня опівночі. Усередині замикання ми виконаємо запит до бази, щоб очистити таблицю:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

Окрім планування замикань, ви можете планувати й [викликаємі об'єкти](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Викликаємі об'єкти - це прості PHP-класи, які містять метод `__invoke`:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

Якщо ви волієте лишити файл `routes/console.php` лише для описів команд, скористайтеся методом `withSchedule` у файлі `bootstrap/app.php`, щоб описати заплановані завдання. Цей метод приймає замикання, яке отримує екземпляр планувальника:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

Якщо ви хочете переглянути огляд своїх запланованих завдань і час їх наступного запуску, скористайтеся командою Artisan `schedule:list`:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Планування команд Artisan

Окрім замикань, ви можете планувати [команди Artisan](/docs/{{version}}/artisan) і системні команди. Наприклад, метод `command` дозволяє запланувати команду Artisan за її назвою або класом.

Плануючи команди Artisan за назвою класу, ви можете передати масив додаткових аргументів командного рядка, які слід передати команді під час виклику:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Планування команд Artisan на замиканнях

Якщо ви хочете запланувати команду Artisan, описану замиканням, додайте методи планування ланцюжком після опису команди:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

Якщо вам потрібно передати аргументи команді на замиканні, передайте їх методу `schedule`:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### Планування завдань у черзі

Метод `job` дозволяє запланувати [завдання в черзі](/docs/{{version}}/queues). Цей метод дає зручний спосіб планувати завдання в черзі, не описуючи замикань через метод `call`:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

Методу `job` можна передати необов'язкові другий і третій аргументи, які вказують ім'я черги та підключення черги, куди слід покласти завдання:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### Планування команд оболонки

Метод `exec` дозволяє віддати команду операційній системі:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### Варіанти частоти розкладу

Ми вже бачили кілька прикладів того, як налаштувати виконання завдання із заданим інтервалом. Проте частот розкладу, які можна призначити завданню, значно більше:

<div class="overflow-auto">

| Метод                              | Опис                                                     |
| ---------------------------------- | -------------------------------------------------------- |
| `->cron('* * * * *');`             | Виконувати завдання за власним розкладом cron.           |
| `->everySecond();`                 | Виконувати завдання щосекунди.                           |
| `->everyTwoSeconds();`             | Виконувати завдання кожні дві секунди.                   |
| `->everyFiveSeconds();`            | Виконувати завдання кожні п'ять секунд.                  |
| `->everyTenSeconds();`             | Виконувати завдання кожні десять секунд.                 |
| `->everyFifteenSeconds();`         | Виконувати завдання кожні п'ятнадцять секунд.            |
| `->everyTwentySeconds();`          | Виконувати завдання кожні двадцять секунд.               |
| `->everyThirtySeconds();`          | Виконувати завдання кожні тридцять секунд.               |
| `->everyMinute();`                 | Виконувати завдання щохвилини.                           |
| `->everyTwoMinutes();`             | Виконувати завдання кожні дві хвилини.                   |
| `->everyThreeMinutes();`           | Виконувати завдання кожні три хвилини.                   |
| `->everyFourMinutes();`            | Виконувати завдання кожні чотири хвилини.                |
| `->everyFiveMinutes();`            | Виконувати завдання кожні п'ять хвилин.                  |
| `->everyTenMinutes();`             | Виконувати завдання кожні десять хвилин.                 |
| `->everyFifteenMinutes();`         | Виконувати завдання кожні п'ятнадцять хвилин.            |
| `->everyThirtyMinutes();`          | Виконувати завдання кожні тридцять хвилин.               |
| `->hourly();`                      | Виконувати завдання щогодини.                            |
| `->hourlyAt(17);`                  | Виконувати завдання щогодини на 17-й хвилині.            |
| `->everyOddHour($minutes = 0);`    | Виконувати завдання щонепарної години.                   |
| `->everyTwoHours($minutes = 0);`   | Виконувати завдання кожні дві години.                    |
| `->everyThreeHours($minutes = 0);` | Виконувати завдання кожні три години.                    |
| `->everyFourHours($minutes = 0);`  | Виконувати завдання кожні чотири години.                 |
| `->everySixHours($minutes = 0);`   | Виконувати завдання кожні шість годин.                   |
| `->daily();`                       | Виконувати завдання щодня опівночі.                      |
| `->dailyAt('13:00');`              | Виконувати завдання щодня о 13:00.                       |
| `->twiceDaily(1, 13);`             | Виконувати завдання щодня о 1:00 та 13:00.               |
| `->twiceDailyAt(1, 13, 15);`       | Виконувати завдання щодня о 1:15 та 13:15.               |
| `->daysOfMonth([1, 10, 20]);`      | Виконувати завдання в певні дні місяця.                  |
| `->weekly();`                      | Виконувати завдання щонеділі о 00:00.                    |
| `->weeklyOn(1, '8:00');`           | Виконувати завдання щотижня в понеділок о 8:00.          |
| `->monthly();`                     | Виконувати завдання першого числа щомісяця о 00:00.      |
| `->monthlyOn(4, '15:00');`         | Виконувати завдання щомісяця 4-го числа о 15:00.         |
| `->twiceMonthly(1, 16, '13:00');`  | Виконувати завдання щомісяця 1-го та 16-го о 13:00.      |
| `->lastDayOfMonth('15:00');`       | Виконувати завдання останнього дня місяця о 15:00.       |
| `->quarterly();`                   | Виконувати завдання першого дня кожного кварталу о 00:00. |
| `->quarterlyOn(4, '14:00');`       | Виконувати завдання щокварталу 4-го числа о 14:00.       |
| `->yearly();`                      | Виконувати завдання першого дня кожного року о 00:00.    |
| `->yearlyOn(6, 1, '17:00');`       | Виконувати завдання щороку 1 червня о 17:00.             |
| `->timezone('America/New_York');`  | Задати часовий пояс для завдання.                        |

</div>

Ці методи можна поєднувати з додатковими обмеженнями, щоб створювати ще тонше налаштовані розклади, які виконуються лише в певні дні тижня. Наприклад, ви можете запланувати команду на щотижневе виконання в понеділок:

```php
use Illuminate\Support\Facades\Schedule;

// Run once per week on Monday at 1 PM...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

Список додаткових обмежень розкладу наведено нижче:

<div class="overflow-auto">

| Метод                                    | Опис                                                   |
| ---------------------------------------- | ------------------------------------------------------ |
| `->weekdays();`                          | Обмежити завдання буднями.                             |
| `->weekends();`                          | Обмежити завдання вихідними.                           |
| `->sundays();`                           | Обмежити завдання неділею.                             |
| `->mondays();`                           | Обмежити завдання понеділком.                          |
| `->tuesdays();`                          | Обмежити завдання вівторком.                           |
| `->wednesdays();`                        | Обмежити завдання середою.                             |
| `->thursdays();`                         | Обмежити завдання четвергом.                           |
| `->fridays();`                           | Обмежити завдання п'ятницею.                           |
| `->saturdays();`                         | Обмежити завдання суботою.                             |
| `->days(array\|mixed);`                  | Обмежити завдання певними днями.                       |
| `->between($startTime, $endTime);`       | Виконувати завдання лише між заданими часами.          |
| `->unlessBetween($startTime, $endTime);` | Не виконувати завдання між заданими часами.            |
| `->when(Closure);`                       | Обмежити завдання за результатом перевірки.            |
| `->environments($env);`                  | Обмежити завдання певними середовищами.                |

</div>

<a name="day-constraints"></a>
#### Обмеження за днями

Метод `days` дозволяє обмежити виконання завдання певними днями тижня. Наприклад, ви можете запланувати щогодинне виконання команди в неділю та середу:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

Як варіант, описуючи дні виконання завдання, ви можете скористатися константами класу `Illuminate\Console\Scheduling\Schedule`:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### Обмеження за часом

Метод `between` дозволяє обмежити виконання завдання за часом доби:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

Так само метод `unlessBetween` дозволяє виключити виконання завдання на певний проміжок часу:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### Обмеження за перевіркою

Метод `when` дозволяє обмежити виконання завдання результатом заданої перевірки. Іншими словами, якщо задане замикання повертає `true`, завдання виконається - за умови, що жодна інша обмежувальна умова цьому не завадить:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

Метод `skip` можна вважати протилежністю `when`. Якщо метод `skip` поверне `true`, заплановане завдання не виконається:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

Коли методи `when` йдуть ланцюжком, запланована команда виконається, лише якщо всі умови `when` повернуть `true`.

<a name="environment-constraints"></a>
#### Обмеження за середовищем

Метод `environments` дозволяє виконувати завдання лише в заданих середовищах (визначених [змінною середовища](/docs/{{version}}/configuration#environment-configuration) `APP_ENV`):

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### Часові пояси

Метод `timezone` дозволяє вказати, що час запланованого завдання слід тлумачити в заданому часовому поясі:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

Якщо ви раз у раз призначаєте той самий часовий пояс усім своїм запланованим завданням, ви можете вказати пояс для всіх розкладів, описавши опцію `schedule_timezone` у файлі конфігурації `app` вашого застосунку:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> Пам'ятайте, що деякі часові пояси використовують перехід на літній час. Коли такий перехід стається, ваше заплановане завдання може виконатися двічі або взагалі не виконатися. Тому ми радимо уникати планування з часовими поясами, коли це можливо.

<a name="preventing-task-overlaps"></a>
### Запобігання накладанню завдань

За замовчуванням заплановані завдання виконуються, навіть якщо попередній екземпляр завдання ще працює. Щоб цьому запобігти, скористайтеся методом `withoutOverlapping`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

У цьому прикладі [команда Artisan](/docs/{{version}}/artisan) `emails:send` виконуватиметься щохвилини, якщо вона ще не працює. Метод `withoutOverlapping` особливо корисний, коли ваші завдання суттєво різняться за часом виконання й ви не можете точно передбачити, скільки триватиме конкретне завдання.

За потреби ви можете вказати, скільки хвилин має минути, перш ніж спливе блокування «без накладання». За замовчуванням блокування спливає за 24 години:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

Під капотом метод `withoutOverlapping` використовує [кеш](/docs/{{version}}/cache) вашого застосунку, щоб отримати блокування. За потреби ви можете очистити ці блокування командою Artisan `schedule:clear-cache`. Зазвичай це потрібно лише тоді, коли завдання зависло через несподівану проблему на сервері.

<a name="running-tasks-on-one-server"></a>
### Виконання завдань на одному сервері

> [!WARNING]
> Щоб скористатися цією можливістю, ваш застосунок має використовувати драйвер кешу `database`, `memcached`, `dynamodb` або `redis` як драйвер за замовчуванням. Крім того, усі сервери мають спілкуватися з одним центральним сервером кешу.

Якщо планувальник вашого застосунку працює на кількох серверах, ви можете обмежити заплановане завдання виконанням лише на одному сервері. Наприклад, припустімо, у вас є заплановане завдання, яке щоп'ятниці ввечері генерує новий звіт. Якщо планувальник працює на трьох робочих серверах, заплановане завдання виконається на всіх трьох і згенерує звіт тричі. Недобре!

Щоб вказати, що завдання має виконуватися лише на одному сервері, скористайтеся методом `onOneServer` під час опису запланованого завдання. Перший сервер, який отримає завдання, встановить атомарне блокування, щоб інші сервери не виконували те саме завдання одночасно:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

Метод `useCache` дозволяє змінити сховище кешу, яке планувальник використовує для отримання атомарних блокувань, потрібних для завдань на одному сервері:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### Іменування завдань для одного сервера

Інколи вам може знадобитися планувати те саме завдання з різними параметрами, водночас вказуючи Laravel виконувати кожну його варіацію на одному сервері. Для цього призначте кожному опису розкладу унікальне ім'я методом `name`:

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```

Так само запланованим замиканням треба призначити ім'я, якщо їх має виконувати один сервер:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### Фонові завдання

За замовчуванням кілька завдань, запланованих на той самий час, виконуються послідовно в порядку їх опису в методі `schedule`. Якщо у вас є довгограючі завдання, наступні завдання можуть стартувати значно пізніше, ніж очікувалося. Якщо ви хочете виконувати завдання у фоні, щоб вони працювали одночасно, скористайтеся методом `runInBackground`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> Метод `runInBackground` можна використовувати лише під час планування завдань методами `command` та `exec`.

<a name="maintenance-mode"></a>
### Режим обслуговування

Заплановані завдання вашого застосунку не виконуватимуться, коли застосунок у [режимі обслуговування](/docs/{{version}}/configuration#maintenance-mode), адже ми не хочемо, щоб ваші завдання заважали незавершеному обслуговуванню сервера. Проте, якщо ви хочете примусово виконувати завдання навіть у режимі обслуговування, викличте метод `evenInMaintenanceMode` під час опису завдання:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="pausing-scheduled-tasks"></a>
### Призупинення запланованих завдань

Ви можете тимчасово призупинити обробку запланованих завдань, не змінюючи розгорнутий код, командою Artisan `schedule:pause`:

```shell
php artisan schedule:pause
```

Доки планувальник призупинено, жодне заплановане завдання не виконуватиметься. Поновити обробку запланованих завдань можна командою `schedule:continue`:

```shell
php artisan schedule:continue
```

Якщо завдання має виконуватися навіть тоді, коли планувальник призупинено, позначте його методом `evenWhenPaused`:

```php
Schedule::command('emails:send')->evenWhenPaused();
```

<a name="schedule-groups"></a>
### Групи розкладу

Описуючи кілька запланованих завдань зі схожими налаштуваннями, ви можете скористатися групуванням завдань у Laravel, щоб не повторювати ті самі налаштування для кожного завдання. Групування спрощує ваш код і забезпечує узгодженість між пов'язаними завданнями.

Щоб створити групу запланованих завдань, викличте потрібні методи налаштування, а за ними - метод `group`. Метод `group` приймає замикання, яке відповідає за опис завдань зі спільною конфігурацією:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```

<a name="running-the-scheduler"></a>
## Запуск планувальника

Тепер, коли ми навчилися описувати заплановані завдання, поговорімо про те, як власне запускати їх на сервері. Команда Artisan `schedule:run` перевірить усі ваші заплановані завдання й визначить, чи потрібно їх виконати, спираючись на поточний час сервера.

Тож, користуючись планувальником Laravel, нам треба додати на сервер лише один запис конфігурації cron, який щохвилини виконує команду `schedule:run`. Якщо ви не знаєте, як додавати записи cron на сервер, розгляньте керовану платформу на кшталт [Laravel Cloud](https://cloud.laravel.com), яка може керувати виконанням запланованих завдань за вас:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### Завдання частіше ніж раз на хвилину

У більшості операційних систем завдання cron можуть виконуватися щонайбільше раз на хвилину. Проте планувальник Laravel дозволяє планувати завдання з частішими інтервалами - навіть щосекунди:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

Коли у вашому застосунку описано завдання частіше ніж раз на хвилину, команда `schedule:run` працюватиме до кінця поточної хвилини, а не завершиться одразу. Це дозволяє команді викликати всі потрібні завдання протягом хвилини.

Оскільки такі завдання, якщо вони виконуються довше за очікуване, можуть затримати виконання наступних, радимо, щоб усі вони диспетчеризували завдання в черзі чи фонові команди, які й робитимуть справжню роботу:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### Переривання завдань частіше ніж раз на хвилину

Оскільки за наявності таких завдань команда `schedule:run` працює всю хвилину від виклику, вам інколи може знадобитися перервати її під час розгортання застосунку. Інакше вже запущений екземпляр `schedule:run` до кінця поточної хвилини й далі використовуватиме раніше розгорнутий код.

Щоб перервати виконання `schedule:run`, додайте команду `schedule:interrupt` до скрипта розгортання вашого застосунку. Цю команду слід викликати після завершення розгортання:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### Запуск планувальника локально

Зазвичай ви не додаватимете запис cron планувальника на локальну машину розробки. Натомість скористайтеся командою Artisan `schedule:work`. Ця команда працюватиме на передньому плані й викликатиме планувальник щохвилини, доки ви її не завершите. Коли описано завдання частіше ніж раз на хвилину, планувальник і далі працюватиме в межах кожної хвилини, щоб їх обробити:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## Вивід завдань

Планувальник Laravel надає кілька зручних методів для роботи з виводом, який генерують заплановані завдання. По-перше, методом `sendOutputTo` ви можете надіслати вивід до файлу для подальшого огляду:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

Якщо ви хочете дописувати вивід до заданого файлу, скористайтеся методом `appendOutputTo`:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

Методом `emailOutputTo` ви можете надіслати вивід на обрану вами електронну адресу. Перш ніж надсилати вивід завдання поштою, налаштуйте [поштові сервіси](/docs/{{version}}/mail) Laravel:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

Якщо ви хочете надсилати вивід поштою, лише коли запланована команда Artisan чи системна команда завершується з ненульовим кодом виходу, скористайтеся методом `emailOutputOnFailure`:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> Методи `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo` та `appendOutputTo` доступні лише для методів `command` та `exec`.

<a name="task-hooks"></a>
## Хуки завдань

Методами `before` та `after` ви можете вказати код, який слід виконати до й після виконання запланованого завдання:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // The task is about to execute...
    })
    ->after(function () {
        // The task has executed...
    });
```

Методи `onSuccess` та `onFailure` дозволяють вказати код, який слід виконати, якщо заплановане завдання завершилося успішно чи невдало. Невдача означає, що запланована команда Artisan чи системна команда завершилася з ненульовим кодом виходу:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```

Якщо ваша команда дає вивід, ви можете звернутися до нього в хуках `after`, `onSuccess` чи `onFailure`, вказавши тип `Illuminate\Support\Stringable` для аргументу `$output` в описі замикання хука:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // The task succeeded...
    })
    ->onFailure(function (Stringable $output) {
        // The task failed...
    });
```

<a name="pinging-urls"></a>
#### Пінгування URL

Методами `pingBefore` та `thenPing` планувальник може автоматично пінгувати заданий URL до чи після виконання завдання. Це стане в пригоді, щоб повідомити зовнішній сервіс - наприклад, [Envoyer](https://envoyer.io) - що ваше заплановане завдання починається чи завершилося:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

Методи `pingOnSuccess` та `pingOnFailure` дозволяють пінгувати заданий URL, лише якщо завдання завершилося успішно чи невдало. Невдача означає, що запланована команда Artisan чи системна команда завершилася з ненульовим кодом виходу:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

Методи `pingBeforeIf`,`thenPingIf`,`pingOnSuccessIf` та `pingOnFailureIf` дозволяють пінгувати заданий URL, лише якщо задана умова є `true`:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a name="events"></a>
## Події

Під час планування Laravel диспетчеризує різні [події](/docs/{{version}}/events). Ви можете [описати слухачів](/docs/{{version}}/events) для будь-якої з них:

<div class="overflow-auto">

| Ім'я події                                                  |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
