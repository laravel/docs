---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Консоль Artisan

- [Вступ](#introduction)
    - [Tinker (REPL)](#tinker)
- [Написання команд](#writing-commands)
    - [Генерація команд](#generating-commands)
    - [Структура команди](#command-structure)
    - [Команди на замиканнях](#closure-commands)
    - [Ізольовані команди](#isolatable-commands)
- [Опис очікуваного вводу](#defining-input-expectations)
    - [Аргументи](#arguments)
    - [Опції](#options)
    - [Масиви вводу](#input-arrays)
    - [Описи вводу](#input-descriptions)
    - [Запит відсутнього вводу](#prompting-for-missing-input)
- [Ввід і вивід команди](#command-io)
    - [Отримання вводу](#retrieving-input)
    - [Запит вводу в користувача](#prompting-for-input)
    - [Виведення](#writing-output)
- [Реєстрація команд](#registering-commands)
- [Програмний запуск команд](#programmatically-executing-commands)
    - [Виклик команд з інших команд](#calling-commands-from-other-commands)
- [Обробка сигналів](#signal-handling)
- [Команда dev](#the-dev-command)
    - [Налаштування процесів dev](#customizing-dev-processes)
    - [Фільтрування процесів dev](#filtering-dev-processes)
- [Налаштування стабів](#stub-customization)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Artisan - це інтерфейс командного рядка, що входить до складу Laravel. Artisan лежить у корені вашого застосунку як скрипт `artisan` і надає чимало корисних команд, які стануть у пригоді під час розробки. Щоб побачити список усіх доступних команд Artisan, скористайтеся командою `list`:

```shell
php artisan list
```

Кожна команда має також екран довідки, який показує та описує доступні аргументи й опції команди. Щоб побачити довідку, поставте перед назвою команди слово `help`:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

Якщо ви використовуєте [Laravel Sail](/docs/{{version}}/sail) як локальне середовище розробки, не забувайте викликати команди Artisan через командний рядок `sail`. Sail виконає ваші команди Artisan усередині Docker-контейнерів застосунку:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker) - це потужний REPL для фреймворку Laravel, побудований на пакеті [PsySH](https://github.com/bobthecow/psysh).

<a name="installation"></a>
#### Встановлення

Усі застосунки Laravel містять Tinker за замовчуванням. Проте, якщо ви раніше видалили його з застосунку, встановити Tinker можна через Composer:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Шукаєте гаряче перезавантаження, багаторядкове редагування коду й автодоповнення під час роботи з застосунком Laravel? Погляньте на [Tinkerwell](https://tinkerwell.app)!

<a name="usage"></a>
#### Використання

Tinker дозволяє взаємодіяти з усім вашим застосунком Laravel у командному рядку, включно з моделями Eloquent, завданнями, подіями тощо. Щоб увійти в середовище Tinker, виконайте команду Artisan `tinker`:

```shell
php artisan tinker
```

Опублікувати файл конфігурації Tinker можна командою `vendor:publish`:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> Функція-хелпер `dispatch` і метод `dispatch` класу `Dispatchable` покладаються на збирач сміття, щоб покласти завдання в чергу. Тому в Tinker для диспетчеризації завдань слід використовувати `Bus::dispatch` або `Queue::push`.

<a name="command-allow-list"></a>
#### Список дозволених команд

Tinker використовує список дозволених команд, щоб визначити, які команди Artisan можна запускати в його оболонці. За замовчуванням доступні команди `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up` та `optimize`. Якщо ви хочете дозволити більше команд, додайте їх до масиву `commands` у файлі конфігурації `tinker.php`:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### Класи, для яких не слід створювати аліаси

Зазвичай Tinker автоматично створює аліаси для класів, з якими ви взаємодієте. Проте для деяких класів ви можете цього не хотіти. Перелічіть такі класи в масиві `dont_alias` файлу конфігурації `tinker.php`:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## Написання команд

Окрім команд, які постачаються з Artisan, ви можете створювати власні. Команди зазвичай зберігаються в каталозі `app/Console/Commands`; втім, ви вільні обрати інше місце, доки вказуєте Laravel [сканувати інші каталоги в пошуках команд Artisan](#registering-commands).

<a name="generating-commands"></a>
### Генерація команд

Щоб створити нову команду, скористайтеся командою Artisan `make:command`. Вона створить новий клас команди в каталозі `app/Console/Commands`. Не переймайтеся, якщо цього каталогу у вашому застосунку немає - його буде створено під час першого запуску `make:command`:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### Структура команди

Після генерації команди опишіть її сигнатуру та опис за допомогою атрибутів `Signature` і `Description`. Атрибут `Signature` також дозволяє описати [очікуваний командою ввід](#defining-input-expectations). Метод `handle` викликається під час виконання команди - саме в ньому розміщується логіка.

Погляньмо на приклад команди. Зверніть увагу, що ми можемо запросити будь-які потрібні залежності через метод `handle`. [Сервіс-контейнер](/docs/{{version}}/container) Laravel автоматично впровадить усі залежності, типи яких вказано в сигнатурі цього методу:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('mail:send {user}')]
#[Description('Send a marketing email to a user')]
class SendEmails extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> Задля кращого повторного використання коду варто тримати консольні команди легкими й доручати роботу сервісам застосунку. У прикладі вище ми впроваджуємо сервісний клас, який бере на себе «важку працю» з надсилання листів.

<a name="exit-codes"></a>
#### Коди виходу

Якщо метод `handle` нічого не повертає і команда виконалася успішно, вона завершиться з кодом виходу `0`, що означає успіх. Проте `handle` може повернути ціле число, щоб задати код виходу вручну:

```php
$this->error('Something went wrong.');

return 1;
```

Якщо ви хочете «провалити» команду з будь-якого її методу, скористайтеся методом `fail`. Він негайно припинить виконання команди й поверне код виходу `1`:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### Команди на замиканнях

Команди на замиканнях - це альтернатива описові консольних команд у вигляді класів. Так само, як замикання маршрутів є альтернативою контролерам, замикання команд є альтернативою класам команд.

Хоч файл `routes/console.php` і не описує HTTP-маршрути, він задає консольні точки входу (маршрути) до застосунку. У цьому файлі ви можете описати всі свої консольні команди на замиканнях за допомогою методу `Artisan::command`. Метод `command` приймає два аргументи: [сигнатуру команди](#defining-input-expectations) і замикання, яке отримує аргументи та опції команди:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

Замикання прив'язане до екземпляра команди, тож вам доступні всі допоміжні методи, які ви зазвичай маєте в повноцінному класі команди.

<a name="type-hinting-dependencies"></a>
#### Типізація залежностей

Окрім аргументів і опцій команди, замикання можуть приймати типізовані додаткові залежності, які потрібно розв'язати із [сервіс-контейнера](/docs/{{version}}/container):

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### Описи команд на замиканнях

Описуючи команду на замиканні, ви можете додати їй опис методом `purpose`. Цей опис показуватиметься під час виконання команд `php artisan list` або `php artisan help`:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Ізольовані команди

> [!WARNING]
> Щоб скористатися цією можливістю, ваш застосунок має використовувати драйвер кешу `memcached`, `redis`, `dynamodb`, `database`, `file` або `array` як драйвер за замовчуванням. Крім того, усі сервери мають спілкуватися з одним центральним сервером кешу.

Інколи потрібно гарантувати, що одночасно виконується лише один екземпляр команди. Для цього реалізуйте у класі команди інтерфейс `Illuminate\Contracts\Console\Isolatable`:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

Коли ви позначаєте команду як `Isolatable`, Laravel автоматично робить доступною опцію `--isolated` без потреби описувати її в опціях команди. Коли команду викликано з цією опцією, Laravel переконається, що інші екземпляри цієї команди ще не виконуються. Для цього він намагається отримати атомарне блокування через драйвер кешу за замовчуванням. Якщо інші екземпляри команди вже працюють, команда не виконається, проте все одно завершиться з успішним кодом виходу:

```shell
php artisan mail:send 1 --isolated
```

Якщо ви хочете задати код виходу, який команда має повертати, коли не змогла виконатися, передайте потрібний код через опцію `isolated`:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### Ідентифікатор блокування

За замовчуванням Laravel використовує назву команди, щоб згенерувати рядковий ключ для атомарного блокування в кеші застосунку. Проте ви можете налаштувати цей ключ, визначивши метод `isolatableId` у класі команди Artisan, - це дозволяє вплести в ключ аргументи чи опції команди:

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### Час дії блокування

За замовчуванням блокування ізоляції спливає після завершення команди. Якщо ж команду перервано і вона не змогла завершитися, блокування спливе за годину. Втім, ви можете змінити час дії блокування, визначивши в команді метод `isolationLockExpiresAt`:

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a name="defining-input-expectations"></a>
## Опис очікуваного вводу

Пишучи консольні команди, часто доводиться збирати ввід від користувача через аргументи або опції. Laravel робить опис очікуваного вводу дуже зручним завдяки властивості `signature`. Вона дозволяє описати назву, аргументи та опції команди в одному виразному синтаксисі, схожому на маршрути.

<a name="arguments"></a>
### Аргументи

Усі аргументи та опції, які надає користувач, беруться у фігурні дужки. У прикладі нижче команда описує один обов'язковий аргумент `user`:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

Аргументи можна також робити необов'язковими або задавати їм значення за замовчуванням:

```php
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```

<a name="options"></a>
### Опції

Опції, як і аргументи, є ще однією формою користувацького вводу. У командному рядку опції записуються з двома дефісами (`--`). Є два типи опцій: ті, що приймають значення, і ті, що не приймають. Опції без значення слугують булевим «перемикачем». Погляньмо на приклад такої опції:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

У цьому прикладі перемикач `--queue` можна вказати під час виклику команди Artisan. Якщо його передано, значенням опції буде `true`. Інакше - `false`:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### Опції зі значеннями

Тепер погляньмо на опцію, яка очікує значення. Якщо користувач має вказати значення для опції, додайте до назви опції знак `=`:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

У цьому прикладі користувач може передати значення опції ось так. Якщо опцію не вказано під час виклику команди, її значенням буде `null`:

```shell
php artisan mail:send 1 --queue=default
```

Задати опціям значення за замовчуванням можна, вказавши його після назви опції. Якщо користувач не передасть значення, буде використано значення за замовчуванням:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### Скорочення опцій

Щоб призначити опції скорочення, вкажіть його перед назвою опції та відділіть символом `|`:

```php
'mail:send {user} {--Q|queue=}'
```

Викликаючи команду в терміналі, скорочення опцій пишуться з одним дефісом, а символ `=` під час передавання значення не використовується:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### Масиви вводу

Якщо ви хочете описати аргументи чи опції, які очікують кілька значень, скористайтеся символом `*`. Спершу погляньмо на приклад такого аргументу:

```php
'mail:send {user*}'
```

Під час запуску цієї команди аргументи `user` можна передати в командному рядку один за одним. Наприклад, наступна команда встановить значенням `user` масив зі значеннями `1` і `2`:

```shell
php artisan mail:send 1 2
```

Символ `*` можна поєднати з описом необов'язкового аргументу, щоб дозволити нуль або більше екземплярів аргументу:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### Масиви опцій

Коли ви описуєте опцію, що очікує кілька значень, кожне передане команді значення опції має мати префікс із назвою опції:

```php
'mail:send {--id=*}'
```

Таку команду можна викликати, передавши кілька аргументів `--id`:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### Описи вводу

Ви можете додати описи до аргументів і опцій вводу, відділивши назву від опису двокрапкою. Якщо для опису команди потрібно трохи більше місця, сміливо розбивайте визначення на кілька рядків:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="prompting-for-missing-input"></a>
### Запит відсутнього вводу

Якщо ваша команда містить обов'язкові аргументи, користувач отримає повідомлення про помилку, коли їх не передано. Натомість ви можете налаштувати команду так, щоб вона автоматично запитувала користувача про відсутні обов'язкові аргументи, - для цього реалізуйте інтерфейс `PromptsForMissingInput`:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Якщо Laravel потрібно отримати від користувача обов'язковий аргумент, він автоматично запитає його, розумно сформулювавши питання на основі назви або опису аргументу. Якщо ви хочете змінити питання, яким збирається обов'язковий аргумент, реалізуйте метод `promptForMissingArgumentsUsing`, повернувши масив питань із ключами за назвами аргументів:

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

Ви також можете додати текст-підказку, скориставшись кортежем із питання та підказки:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

Якщо вам потрібен повний контроль над запитом, передайте замикання, яке має запитати користувача й повернути його відповідь:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
Вичерпна документація [Laravel Prompts](/docs/{{version}}/prompts) містить додаткову інформацію про доступні запити та їх використання.

Якщо ви хочете запропонувати користувачеві обрати чи ввести [опції](#options), додайте запити в метод `handle` команди. Проте, якщо ви хочете запитувати користувача лише тоді, коли його вже автоматично запитали про відсутні аргументи, реалізуйте метод `afterPromptingForMissingArguments`:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
## Ввід і вивід команди

<a name="retrieving-input"></a>
### Отримання вводу

Під час виконання команди вам, найімовірніше, знадобиться доступ до значень аргументів і опцій, які вона приймає. Для цього скористайтеся методами `argument` і `option`. Якщо аргументу чи опції не існує, буде повернуто `null`:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

Якщо потрібно отримати всі аргументи як `array`, викличте метод `arguments`:

```php
$arguments = $this->arguments();
```

Опції отримуються так само просто, як аргументи, - методом `option`. Щоб отримати всі опції як масив, викличте метод `options`:

```php
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

Метод `input` дозволяє отримати аргументи й опції команди як екземпляр `Illuminate\Console\CommandInput`, який надає ті самі типізовані аксесори, що доступні для HTTP-запитів та інших контейнерів даних:

```php
use App\Enums\ReportType;

/**
 * Execute the console command.
 */
public function handle(): void
{
    $input = $this->input()->date('from');

    // ...
}
```

Метод `input` також можна використати, щоб отримати одне значення з аргументів або опцій:

```php
$queue = $this->input('queue', 'default');
```

<a name="prompting-for-input"></a>
### Запит вводу в користувача

> [!NOTE]
> [Laravel Prompts](/docs/{{version}}/prompts) - це PHP-пакет для додавання гарних і зручних форм до ваших консольних застосунків, з можливостями на кшталт браузерних: текстом-підказкою та валідацією.

Окрім виведення інформації, ви можете просити користувача ввести дані під час виконання команди. Метод `ask` покаже користувачеві задане питання, прийме його ввід і поверне його вашій команді:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

Метод `ask` також приймає необов'язковий другий аргумент - значення за замовчуванням, яке буде повернуто, якщо користувач нічого не ввів:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

Метод `secret` схожий на `ask`, але ввід користувача не відображатиметься в консолі під час набору. Цей метод стане в пригоді, коли ви запитуєте чутливу інформацію на кшталт паролів:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### Запит підтвердження

Якщо потрібно спитати користувача про просте підтвердження «так чи ні», скористайтеся методом `confirm`. За замовчуванням цей метод повертає `false`. Проте, якщо користувач введе `y` або `yes`, метод поверне `true`.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

За потреби ви можете вказати, що запит підтвердження має за замовчуванням повертати `true`, передавши `true` другим аргументом методу `confirm`:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### Автодоповнення

Метод `anticipate` можна використати, щоб надати автодоповнення для можливих варіантів. Користувач усе одно може ввести будь-яку відповідь, незалежно від підказок автодоповнення:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

Як варіант, ви можете передати другим аргументом методу `anticipate` замикання. Воно викликатиметься щоразу, коли користувач вводить символ. Замикання має приймати рядковий параметр із поточним вводом користувача й повертати масив варіантів для автодоповнення:

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a name="multiple-choice-questions"></a>
#### Питання з кількома варіантами

Якщо потрібно запропонувати користувачеві наперед визначений набір варіантів, скористайтеся методом `choice`. Індекс масиву зі значенням за замовчуванням, яке буде повернуто, якщо користувач нічого не обрав, передається третім аргументом методу:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

Крім того, метод `choice` приймає необов'язкові четвертий і п'ятий аргументи: максимальну кількість спроб обрати коректну відповідь і чи дозволено кілька варіантів вибору:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### Виведення

Щоб вивести щось у консоль, скористайтеся методами `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert` та `error`. Кожен із них використовує відповідні ANSI-кольори. Наприклад, покажемо користувачеві загальну інформацію. Зазвичай метод `info` виводить у консоль текст зеленого кольору:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

Щоб показати повідомлення про помилку, скористайтеся методом `error`. Текст помилки зазвичай виводиться червоним:

```php
$this->error('Something went wrong!');
```

Метод `line` виводить простий неколірний текст:

```php
$this->line('Display this on the screen');
```

Метод `newLine` виводить порожній рядок:

```php
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a name="tables"></a>
#### Таблиці

Метод `table` спрощує правильне форматування кількох рядків / стовпців даних. Усе, що вам потрібно, - передати назви стовпців і дані таблиці, а Laravel автоматично обчислить відповідну ширину й висоту таблиці:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### Індикатори прогресу

Для тривалих завдань корисно показувати індикатор прогресу, який повідомляє користувачам, наскільки завдання виконане. З методом `withProgressBar` Laravel покаже індикатор прогресу й просуватиме його на кожній ітерації по заданому ітерабельному значенню:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

Інколи потрібен більший контроль над тим, як просувається індикатор прогресу. Спершу задайте загальну кількість кроків, які пройде процес. Потім просувайте індикатор після обробки кожного елемента:

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> [!NOTE]
> Про більш просунуті можливості читайте в [документації компонента Symfony Progress Bar](https://symfony.com/doc/current/components/console/helpers/progressbar.html).

<a name="registering-commands"></a>
## Реєстрація команд

За замовчуванням Laravel автоматично реєструє всі команди в каталозі `app/Console/Commands`. Проте ви можете вказати Laravel сканувати інші каталоги в пошуках команд Artisan за допомогою методу `withCommands` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

За потреби ви можете зареєструвати команди й вручну, передавши методу `withCommands` назву класу команди:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Коли Artisan завантажується, усі команди застосунку будуть розв'язані через [сервіс-контейнер](/docs/{{version}}/container) і зареєстровані в Artisan.

<a name="programmatically-executing-commands"></a>
## Програмний запуск команд

Інколи потрібно виконати команду Artisan поза межами CLI. Наприклад, вам може знадобитися виконати команду Artisan з маршруту чи контролера. Для цього скористайтеся методом `call` фасаду `Artisan`. Метод `call` приймає першим аргументом назву сигнатури команди або назву класу, а другим - масив параметрів команди. Він повертає код виходу:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

Як варіант, ви можете передати методу `call` цілу команду Artisan рядком:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### Передавання масивів значень

Якщо ваша команда описує опцію, що приймає масив, ви можете передати цій опції масив значень:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### Передавання булевих значень

Якщо потрібно задати значення опції, яка не приймає рядкових значень, - наприклад, прапорець `--force` команди `migrate:refresh`, - передайте як значення опції `true` або `false`:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Постановка команд Artisan у чергу

За допомогою методу `queue` фасаду `Artisan` ви можете навіть ставити команди Artisan у чергу, щоб їх у фоні обробляли [воркери черги](/docs/{{version}}/queues). Перш ніж користуватися цим методом, переконайтеся, що ви налаштували чергу й запустили слухача черги:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

Методами `onConnection` та `onQueue` можна вказати підключення або чергу, до якої слід відправити команду Artisan:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### Виклик команд з інших команд

Інколи потрібно викликати інші команди з наявної команди Artisan. Це робиться методом `call`. Він приймає назву команди та масив аргументів / опцій:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

Якщо ви хочете викликати іншу консольну команду й приховати весь її вивід, скористайтеся методом `callSilently`. Він має ту саму сигнатуру, що й метод `call`:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## Обробка сигналів

Як ви, можливо, знаєте, операційні системи дозволяють надсилати сигнали запущеним процесам. Наприклад, сигналом `SIGTERM` операційна система просить програму коректно завершити роботу. Якщо ви хочете слухати сигнали у своїх консольних командах Artisan і виконувати код, коли вони надходять, скористайтеся методом `trap`:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

Щоб слухати кілька сигналів одразу, передайте методу `trap` масив сигналів:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="the-dev-command"></a>
## Команда dev

Команда Artisan `dev` запускає в одному вікні термінала всі процеси, потрібні для локальної розробки. За замовчуванням вона паралельно запускає сервер розробки PHP, воркер черги, стеження за логами через [Pail](/docs/{{version}}/logging#tailing-log-messages-using-pail) і компіляцію ресурсів Vite:

```shell
php artisan dev
```

Під капотом команда `dev` керує процесами через npm-пакет `concurrently`. Кожен процес має свою мітку й колір у виводі термінала, тож їх легко розрізнити. Якщо якийсь процес завершиться помилкою, усі інші процеси буде автоматично зупинено.

Процеси за замовчуванням:

| Назва | Команда |
| --- | --- |
| `server` | `php artisan serve --host=localhost` |
| `queue` | `php artisan queue:listen --tries=1 --timeout=0` |
| `logs` | `php artisan pail --timeout=0` |
| `vite` | `npm run dev` |

> [!NOTE]
> Процес `vite` автоматично визначає ваш менеджер пакетів Node (npm, pnpm, Yarn чи Bun) і використовує відповідну команду запуску.

<a name="customizing-dev-processes"></a>
### Налаштування процесів dev

Ви можете налаштувати процеси, які запускає команда `dev`, за допомогою класу `DevCommands` - зазвичай у методі `boot` вашого `AppServiceProvider`. Метод `register` приймає рядок команди й необов'язкову назву:

```php
use Illuminate\Foundation\DevCommands;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    DevCommands::register('some-command --flag', 'my-process');
}
```

Реєструючи команду Artisan, ви можете скористатися методом `artisan`, який автоматично додає до команди префікс `php artisan`:

```php
DevCommands::artisan('horizon', 'horizon');
```

Так само метод `node` додає префікс із командою запуску вашого менеджера пакетів (наприклад, `npm run`), а метод `nodeExec` - префікс із командою виконання менеджера пакетів (наприклад, `npx`):

```php
DevCommands::node('storybook', 'storybook');

DevCommands::nodeExec('tailwindcss -i resources/css/app.css -o public/css/app.css --watch', 'tailwind');
```

Якщо ви зареєструєте процес із такою самою назвою, як у процесу за замовчуванням, ваш процес замінить стандартний. Наприклад, ви можете налаштувати процес сервера на інший порт:

```php
DevCommands::artisan('serve --host=localhost --port=9000', 'server');
```

Ви також можете змінити колір мітки процесу в терміналі. Доступні методи кольорів: `blue`, `purple`, `pink`, `orange`, `green` та `yellow`. Крім того, методу `color` можна передати власний hex-колір:

```php
DevCommands::register('my-command', 'my-process')->green();

DevCommands::register('my-command', 'my-process')->color('#ff6347');
```

Щоб побачити всі зареєстровані процеси dev, не запускаючи їх, скористайтеся командою `dev:list`:

```shell
php artisan dev:list
```

<a name="filtering-dev-processes"></a>
### Фільтрування процесів dev

Ви можете вказати команді `dev` запускати лише певні процеси за допомогою методу `only`. Так само можна виключити певні процеси методом `except`:

```php
// Only run the server and vite processes...
DevCommands::only('server', 'vite');

// Run all processes except the queue worker...
DevCommands::except('queue');
```

<a name="stub-customization"></a>
## Налаштування стабів

Команди `make` консолі Artisan створюють різноманітні класи: контролери, завдання, міграції, тести. Ці класи генеруються з файлів-«стабів», які заповнюються значеннями на основі вашого вводу. Проте вам може захотітися внести невеликі зміни у файли, які генерує Artisan. Для цього скористайтеся командою `stub:publish`, щоб опублікувати найпоширеніші стаби у ваш застосунок і налаштувати їх:

```shell
php artisan stub:publish
```

Опубліковані стаби опиняться в каталозі `stubs` у корені застосунку. Усі зміни, які ви внесете в ці стаби, відображатимуться під час генерації відповідних класів командами `make` Artisan.

<a name="events"></a>
## Події

Під час виконання команд Artisan диспетчеризує три події: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting` і `Illuminate\Console\Events\CommandFinished`. Подія `ArtisanStarting` диспетчеризується одразу, щойно Artisan починає роботу. Далі, безпосередньо перед виконанням команди, диспетчеризується подія `CommandStarting`. Нарешті, після завершення виконання команди диспетчеризується подія `CommandFinished`.
