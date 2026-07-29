---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Контекст

- [Вступ](#introduction)
    - [Як це працює](#how-it-works)
- [Збереження контексту](#capturing-context)
    - [Стеки](#stacks)
- [Отримання контексту](#retrieving-context)
    - [Перевірка наявності елемента](#determining-item-existence)
- [Видалення контексту](#removing-context)
- [Прихований контекст](#hidden-context)
- [Події](#events)
    - [Дегідратація](#dehydrating)
    - [Гідратація](#hydrated)

<a name="introduction"></a>
## Вступ

Можливості «контексту» в Laravel дозволяють зберігати, отримувати та передавати інформацію крізь запити, завдання й команди, що виконуються у вашому застосунку. Ця збережена інформація також потрапляє до логів, які пише ваш застосунок, даючи глибше розуміння історії виконання коду перед появою запису в логу й дозволяючи простежити потоки виконання в розподіленій системі.

<a name="how-it-works"></a>
### Як це працює

Найкращий спосіб зрозуміти можливості контексту в Laravel - побачити їх у дії разом із вбудованими можливостями логування. Щоб почати, [додайте інформацію до контексту](#capturing-context) через фасад `Context`. У цьому прикладі ми скористаємося [`middleware`](/docs/{{version}}/middleware), щоб додавати URL запиту та унікальний ідентифікатор трасування до контексту для кожного вхідного запиту:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}
```

Інформація, додана до контексту, автоматично додається як метадані до всіх [записів логу](/docs/{{version}}/logging), що пишуться протягом запиту. Додавання контексту саме як метаданих дозволяє відрізнити інформацію, передану окремим записам логу, від інформації, спільної через `Context`. Наприклад, уявімо, що ми пишемо такий запис:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

Записаний лог міститиме `auth_id`, переданий запису, а також `url` і `trace_id` із контексту як метадані:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Інформація, додана до контексту, також стає доступною завданням, надісланим до черги. Наприклад, уявімо, що ми надсилаємо до черги завдання `ProcessPodcast` після додавання певної інформації до контексту:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

Коли завдання надсилається, уся інформація, що зараз зберігається в контексті, захоплюється й передається завданню. Далі, поки завдання виконується, її гідратують назад у поточний контекст. Тож якби метод `handle` нашого завдання писав до логу:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}
```

Отриманий запис логу міститиме інформацію, додану до контексту під час запиту, який спочатку надіслав це завдання:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Хоча ми зосередилися на вбудованих можливостях логування, наведена далі документація покаже, як контекст дозволяє передавати інформацію через межу «HTTP-запит - завдання в черзі», а також як додавати [приховані дані контексту](#hidden-context), які не потрапляють до записів логу.

<a name="capturing-context"></a>
## Збереження контексту

Ви можете зберегти інформацію в поточному контексті методом `add` фасаду `Context`:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

Щоб додати кілька елементів одразу, передайте методу `add` асоціативний масив:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

Метод `add` перезапише будь-яке наявне значення з тим самим ключем. Якщо ви хочете додати інформацію лише тоді, коли ключа ще немає, скористайтеся методом `addIf`:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

Контекст також надає зручні методи для збільшення чи зменшення значення за ключем. Обидва приймають щонайменше один аргумент - ключ, який відстежуємо. Другим аргументом можна вказати величину, на яку слід змінити значення:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### Умовний контекст

Метод `when` дозволяє додавати дані до контексту залежно від певної умови. Перше замикання, передане методу `when`, буде викликано, якщо умова дає `true`, а друге - якщо `false`:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="scoped-context"></a>
#### Контекст з обмеженою областю

Метод `scope` дає спосіб тимчасово змінити контекст під час виконання переданого колбека й відновити його початковий стан після завершення. Крім того, ви можете передати додаткові дані (другим і третім аргументами), які буде об'єднано з контекстом на час виконання замикання.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> [!WARNING]
> Якщо об'єкт усередині контексту змінено всередині замикання зі scope, ця зміна відобразиться й поза межами області.

<a name="stacks"></a>
### Стеки

Контекст дозволяє створювати «стеки» - списки даних, збережених у порядку додавання. Додати інформацію до стека можна методом `push`:

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

Стеки корисні для збереження історичної інформації про запит - наприклад, подій, що відбуваються у вашому застосунку. Скажімо, ви можете створити слухач подій, який додаватиме до стека запис щоразу, коли виконується запит до бази, зберігаючи SQL і тривалість як кортеж:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

Визначити, чи є значення в стеці, можна методами `stackContains` і `hiddenStackContains`:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

Методи `stackContains` і `hiddenStackContains` також приймають замикання другим аргументом, що дає більший контроль над порівнянням значень:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## Отримання контексту

Отримати інформацію з контексту можна методом `get` фасаду `Context`:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

Методи `only` та `except` дозволяють отримати підмножину інформації з контексту:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

Метод `pull` дозволяє отримати інформацію з контексту й одразу вилучити її звідти:

```php
$value = Context::pull('key');
```

Якщо дані контексту зберігаються у [стеці](#stacks), ви можете дістати елементи зі стека методом `pop`:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

Методи `remember` і `rememberHidden` дозволяють отримати інформацію з контексту, водночас задавши значення контексту тим, що повертає передане замикання, якщо запитаної інформації немає:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

Якщо ви хочете отримати всю збережену в контексті інформацію, викличте метод `all`:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### Перевірка наявності елемента

Методи `has` і `missing` дозволяють визначити, чи має контекст будь-яке значення для вказаного ключа:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

Метод `has` поверне `true` незалежно від збереженого значення. Тож, наприклад, ключ зі значенням `null` вважатиметься присутнім:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## Видалення контексту

Метод `forget` дозволяє вилучити ключ та його значення з поточного контексту:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

Ви можете вилучити кілька ключів одразу, передавши методу `forget` масив:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## Прихований контекст

Контекст дозволяє зберігати «приховані» дані. Ця інформація не додається до логів і недоступна через описані вище методи отримання даних. Для роботи з прихованим контекстом контекст надає окремий набір методів:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

«Приховані» методи дзеркалять функціональність звичайних методів, описаних вище:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## Події

Контекст надсилає дві події, що дозволяють підключитися до процесів гідратації та дегідратації контексту.

Щоб проілюструвати їх використання, уявіть, що в `middleware` вашого застосунку ви задаєте значення конфігурації `app.locale` на основі заголовка `Accept-Language` вхідного HTTP-запиту. Події контексту дозволяють зберегти це значення під час запиту й відновити його в черзі, гарантуючи, що сповіщення, надіслані з черги, матимуть правильне значення `app.locale`. Досягти цього можна за допомогою подій контексту та [прихованих](#hidden-context) даних, що й показує наведена далі документація.

<a name="dehydrating"></a>
### Дегідратація

Щоразу, коли завдання надсилається до черги, дані контексту «дегідратуються» й зберігаються разом із даними завдання. Метод `Context::dehydrating` дозволяє зареєструвати замикання, яке буде викликано під час дегідратації. У цьому замиканні ви можете змінити дані, які буде передано завданню в черзі.

Зазвичай колбеки `dehydrating` слід реєструвати в методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}
```

> [!NOTE]
> Не використовуйте фасад `Context` усередині колбека `dehydrating`, адже це змінить контекст поточного процесу. Переконайтеся, що вносите зміни лише до репозиторію, переданого колбеку.

<a name="hydrated"></a>
### Гідратація

Щоразу, коли завдання з черги починає виконуватися, будь-який контекст, переданий разом із ним, «гідратується» назад у поточний контекст. Метод `Context::hydrated` дозволяє зареєструвати замикання, яке буде викликано під час гідратації.

Зазвичай колбеки `hydrated` слід реєструвати в методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> [!NOTE]
> Не використовуйте фасад `Context` усередині колбека `hydrated` - натомість вносьте зміни лише до репозиторію, переданого колбеку.
