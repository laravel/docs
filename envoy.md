---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Envoy

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Написання завдань](#writing-tasks)
    - [Визначення завдань](#defining-tasks)
    - [Кілька серверів](#multiple-servers)
    - [Підготовка](#setup)
    - [Змінні](#variables)
    - [Сценарії](#stories)
    - [Хуки](#completion-hooks)
- [Запуск завдань](#running-tasks)
    - [Підтвердження виконання завдання](#confirming-task-execution)
- [Сповіщення](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## Вступ

[Laravel Envoy](https://github.com/laravel/envoy) - інструмент для виконання типових завдань на ваших віддалених серверах. Через синтаксис у стилі [Blade](/docs/{{version}}/blade) ви можете легко описати завдання для розгортання, артизан-команди тощо. Наразі Envoy підтримує лише macOS і Linux. Проте підтримки Windows можна досягти через [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

<a name="installation"></a>
## Встановлення

Спершу встановіть Envoy у свій проєкт через менеджер пакетів Composer:

```shell
composer require laravel/envoy --dev
```

Коли Envoy встановлено, його бінарник буде доступний у каталозі `vendor/bin` вашого застосунку:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## Написання завдань

<a name="defining-tasks"></a>
### Визначення завдань

Завдання - базовий будівельний блок Envoy. Завдання описують команди оболонки, які мають виконатися на ваших віддалених серверах при виклику завдання. Наприклад, ви можете описати завдання, що виконує команду `php artisan queue:restart` на всіх серверах-воркерах черг вашого застосунку.

Усі ваші завдання Envoy слід описувати у файлі `Envoy.blade.php` у корені застосунку. Ось приклад для початку:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

Як бачите, на початку файлу описано масив `@servers` - завдяки цьому ви можете посилатися на ці сервери через опцію `on` у оголошеннях завдань. Оголошення `@servers` завжди має бути в одному рядку. Усередині оголошень `@task` розміщуйте команди оболонки, які мають виконатися на ваших серверах при виклику завдання.

<a name="local-tasks"></a>
#### Локальні завдання

Ви можете змусити скрипт виконуватися на вашому комп'ютері, вказавши IP-адресу сервера `127.0.0.1`:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Імпорт завдань Envoy

За допомогою директиви `@import` ви можете імпортувати інші файли Envoy, щоб їхні сценарії та завдання додалися до ваших. Після імпорту ви можете виконувати їхні завдання так, ніби вони описані у вашому власному файлі Envoy:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### Кілька серверів

Envoy дозволяє легко запустити завдання на кількох серверах. Спершу додайте додаткові сервери до оголошення `@servers`. Кожному серверу слід дати унікальне ім'я. Коли додаткові сервери описано, ви можете перелічити кожен із них у масиві `on` завдання:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### Паралельне виконання

За замовчуванням завдання виконуються на кожному сервері послідовно. Іншими словами, завдання завершиться на першому сервері, перш ніж почне виконуватися на другому. Якщо ви хочете запустити завдання на кількох серверах паралельно, додайте до його оголошення опцію `parallel`:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### Підготовка

Іноді вам може знадобитися виконати довільний PHP-код перед запуском завдань Envoy. Скористайтеся директивою `@setup`, щоб описати блок PHP-коду, який має виконатися перед вашими завданнями:

```php
@setup
    $now = new DateTime;
@endsetup
```

Якщо перед виконанням завдання вам треба підключити інші файли PHP, скористайтеся директивою `@include` на початку вашого файлу `Envoy.blade.php`:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### Змінні

За потреби ви можете передавати завданням Envoy аргументи, вказавши їх у командному рядку під час виклику:

```shell
php vendor/bin/envoy run deploy --branch=master
```

Звертатися до опцій у своїх завданнях можна через синтаксис «echo» у Blade. Ви також можете описувати всередині завдань конструкції `if` і цикли Blade. Наприклад, перевірмо наявність змінної `$branch` перед виконанням команди `git pull`:

```blade
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask
```

<a name="stories"></a>
### Сценарії

Сценарії групують набір завдань під одним зручним іменем. Наприклад, сценарій `deploy` може запускати завдання `update-code` та `install-dependencies`, перелічені в його визначенні:

```blade
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask
```

Коли сценарій написано, ви можете викликати його так само, як і завдання:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### Хуки

Під час виконання завдань і сценаріїв запускається низка хуків. Envoy підтримує такі типи хуків: `@before`, `@after`, `@error`, `@success` та `@finished`. Увесь код у цих хуках інтерпретується як PHP і виконується локально, а не на віддалених серверах, з якими працюють ваші завдання.

Ви можете описати скільки завгодно хуків кожного типу. Вони виконуватимуться в тому порядку, у якому йдуть у вашому скрипті Envoy.

<a name="hook-before"></a>
#### `@before`

Перед виконанням кожного завдання виконаються всі хуки `@before`, зареєстровані у вашому скрипті Envoy. Хуки `@before` отримують ім'я завдання, яке буде виконано:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

Після виконання кожного завдання виконаються всі хуки `@after`, зареєстровані у вашому скрипті Envoy. Хуки `@after` отримують ім'я виконаного завдання:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

Після кожного провалу завдання (вихід із кодом статусу більшим за `0`) виконаються всі хуки `@error`, зареєстровані у вашому скрипті Envoy. Хуки `@error` отримують ім'я виконаного завдання:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

Якщо всі завдання виконалися без помилок, виконаються всі хуки `@success`, зареєстровані у вашому скрипті Envoy:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

Після виконання всіх завдань (незалежно від статусу виходу) виконаються всі хуки `@finished`. Хуки `@finished` отримують код статусу завершеного завдання, який може бути `null` або цілим числом (`integer`), більшим за `0` чи рівним йому:

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished
```

<a name="running-tasks"></a>
## Запуск завдань

Щоб запустити завдання чи сценарій, описаний у файлі `Envoy.blade.php` вашого застосунку, виконайте команду Envoy `run`, передавши ім'я потрібного завдання чи сценарію. Envoy виконає завдання й показуватиме вивід із ваших віддалених серверів у процесі:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### Підтвердження виконання завдання

Якщо ви хочете отримувати запит на підтвердження перед запуском певного завдання на серверах, додайте до його оголошення директиву `confirm`. Ця опція особливо корисна для руйнівних операцій:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## Сповіщення

<a name="slack"></a>
### Slack

Envoy підтримує надсилання сповіщень у [Slack](https://slack.com) після виконання кожного завдання. Директива `@slack` приймає URL хука Slack та ім'я каналу / користувача. Отримати URL вебхука можна, створивши інтеграцію «Incoming WebHooks» у панелі керування Slack.

Передайте повний URL вебхука першим аргументом директиви `@slack`. Другим аргументом має бути ім'я каналу (`#channel`) чи ім'я користувача (`@user`):

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

За замовчуванням сповіщення Envoy надсилатимуть у канал повідомлення з описом виконаного завдання. Проте ви можете перезаписати це повідомлення власним, передавши директиві `@slack` третій аргумент:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy також підтримує надсилання сповіщень у [Discord](https://discord.com) після виконання кожного завдання. Директива `@discord` приймає URL хука Discord і повідомлення. Отримати URL вебхука можна, створивши «Webhook» у налаштуваннях сервера й обравши канал, до якого він публікуватиме. Передайте повний URL вебхука до директиви `@discord`:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy також підтримує надсилання сповіщень у [Telegram](https://telegram.org) після виконання кожного завдання. Директива `@telegram` приймає ID бота Telegram і ID чату. Отримати ID бота можна, створивши нового бота через [BotFather](https://t.me/botfather). Отримати дійсний ID чату можна через [@username_to_id_bot](https://t.me/username_to_id_bot). Передайте повні ID бота та ID чату до директиви `@telegram`:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy також підтримує надсилання сповіщень у [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) після виконання кожного завдання. Директива `@microsoftTeams` приймає вебхук Teams (обов'язково), повідомлення, колір теми (success, info, warning, error) і масив опцій. Отримати вебхук Teams можна, створивши новий [вхідний вебхук](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). API Teams має багато інших атрибутів для налаштування вашого блоку повідомлення - як-от заголовок, підсумок і секції. Докладніше читайте в [документації Microsoft Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). Передайте повний URL вебхука до директиви `@microsoftTeams`:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
