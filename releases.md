---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Нотатки релізу

- [Схема версіонування](#versioning-scheme)
- [Політика підтримки](#support-policy)
- [Laravel 13](#laravel-13)

<a name="versioning-scheme"></a>
## Схема версіонування

Laravel та інші його офіційні пакети дотримуються [семантичного версіонування](https://semver.org). Мажорні релізи фреймворку виходять щороку (приблизно в першому кварталі), тоді як мінорні та патч-релізи можуть виходити навіть щотижня. Мінорні та патч-релізи **ніколи** не повинні містити змін, що порушують сумісність.

Посилаючись на фреймворк Laravel або його компоненти зі свого застосунку чи пакета, завжди використовуйте обмеження версії на кшталт `^13.0`, оскільки мажорні релізи Laravel таки містять зміни, що порушують сумісність. Утім, ми прагнемо завжди забезпечити можливість оновитися до нового мажорного релізу за день або швидше.

<a name="named-arguments"></a>
#### Іменовані аргументи

[Іменовані аргументи](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) не підпадають під настанови Laravel щодо зворотної сумісності. За потреби ми можемо перейменовувати аргументи функцій, щоб покращити кодову базу Laravel. Тому використовувати іменовані аргументи, викликаючи методи Laravel, слід обачно й з розумінням, що імена параметрів можуть змінитися в майбутньому.

<a name="support-policy"></a>
## Політика підтримки

Для всіх релізів Laravel виправлення помилок надаються протягом 18 місяців, а виправлення безпеки - протягом 2 років. Для всіх додаткових бібліотек виправлення помилок отримує лише останній мажорний реліз. Крім того, перегляньте версії баз даних, [які підтримує Laravel](/docs/{{version}}/database#introduction).

<div class="overflow-auto">

| Версія  | PHP (*)   | Реліз               | Виправлення помилок до | Виправлення безпеки до |
| ------- |-----------| ------------------- | ---------------------- | ---------------------- |
| 10      | 8.1 - 8.3 | 14 лютого 2023      | 6 серпня 2024          | 4 лютого 2025          |
| 11      | 8.2 - 8.4 | 12 березня 2024     | 3 вересня 2025         | 12 березня 2026        |
| 12      | 8.2 - 8.5 | 24 лютого 2025      | 13 серпня 2026         | 24 лютого 2027         |
| 13      | 8.3 - 8.5 | 17 березня 2026     | 3 квартал 2027         | 17 березня 2028        |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>Кінець підтримки</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Лише виправлення безпеки</div>
    </div>
</div>

(*) Підтримувані версії PHP

<a name="laravel-13"></a>
## Laravel 13

Laravel 13 продовжує щорічний ритм релізів Laravel, зосереджуючись на робочих процесах, орієнтованих на AI, надійніших налаштуваннях за замовчуванням і виразніших API для розробників. Цей реліз містить офіційні AI-примітиви, ресурси JSON:API, можливості семантичного та векторного пошуку, а також поступові покращення в чергах, кеші й безпеці.

<a name="minimal-breaking-changes"></a>
### Мінімум змін, що порушують сумісність

Значну частину зусиль у цьому циклі релізу ми присвятили тому, щоб звести до мінімуму зміни, які порушують сумісність. Натомість ми зосередилися на тому, щоб протягом року постійно постачати покращення, які не ламають наявні застосунки.

Тому реліз Laravel 13 - відносно незначне оновлення з погляду зусиль, хоча й дає суттєві нові можливості. З огляду на це більшість застосунків Laravel можуть оновитися до Laravel 13, майже не змінюючи код застосунку.

<a name="php-8"></a>
### PHP 8.3

Laravel 13.x потребує щонайменше PHP версії 8.3.

<a name="ai-sdk"></a>
### Laravel AI SDK

Laravel 13 представляє офіційний [Laravel AI SDK](https://laravel.com/ai), що дає уніфікований API для генерації тексту, агентів із викликом інструментів, ембедингів, аудіо, зображень та інтеграцій із векторними сховищами.

За допомогою AI SDK ви можете створювати AI-можливості, незалежні від конкретного провайдера, зберігаючи водночас послідовний і природний для Laravel досвід розробки.

Наприклад, базового агента можна запитати одним викликом:

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

Laravel AI SDK також може генерувати зображення, аудіо та ембединги.

Для сценаріїв візуальної генерації SDK пропонує зрозумілий API для створення зображень із запитів звичайною мовою:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

Для голосових сценаріїв ви можете синтезувати природне звучання з тексту для асистентів, начитки та можливостей доступності:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

А для семантичного пошуку та сценаріїв пошуку інформації ви можете генерувати ембединги прямо з рядків:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
### Ресурси JSON:API

Laravel тепер містить офіційні [ресурси JSON:API](/docs/{{version}}/eloquent-resources#jsonapi-resources), що спрощує повернення відповідей, сумісних зі специфікацією JSON:API.

Ресурси JSON:API беруть на себе серіалізацію об'єктів ресурсу, долучення зв'язків, розріджені набори полів (sparse fieldsets), посилання та заголовки відповідей, сумісні з JSON:API.

<a name="request-forgery-protection"></a>
### Захист від підробки запитів

Задля безпеки `middleware` [захисту від підробки запитів](/docs/{{version}}/csrf#preventing-csrf-requests) було вдосконалено та формалізовано як `PreventRequestForgery`, додавши перевірку запитів з урахуванням джерела (origin) і зберігши сумісність із захистом CSRF на основі токенів.

<a name="queue-routing"></a>
### Маршрутизація черг

Laravel 13 додає [маршрутизацію черг за класом](/docs/{{version}}/queues#queue-routing) через `Queue::route(...)`, що дозволяє визначити в одному місці правила маршрутизації черги чи підключення за замовчуванням для конкретних завдань:

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
### Розширені атрибути PHP

Laravel 13 продовжує розширювати офіційну підтримку атрибутів PHP у фреймворку, роблячи типові питання конфігурації та поведінки декларативнішими й розміщеними поруч із вашими класами та методами.

Серед помітних доповнень - атрибути контролерів і авторизації, як-от [`#[Middleware]`](/docs/{{version}}/controllers#controller-middleware) та [`#[Authorize]`](/docs/{{version}}/controllers#authorization-attributes), а також засоби керування завданнями черг: [`#[Tries]`](/docs/{{version}}/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/{{version}}/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/{{version}}/queues#max-job-attempts-and-timeout) і [`#[FailOnTimeout]`](/docs/{{version}}/queues#failing-on-timeout).

Наприклад, `middleware` контролера та перевірки політик тепер можна оголошувати прямо на класах і методах:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}
```

Додаткові атрибути з'явилися також в API Eloquent, подій, сповіщень, валідації, тестування та серіалізації ресурсів, даючи вам послідовний підхід «спочатку атрибути» в більшій кількості областей фреймворку.

<a name="cache-touch"></a>
### Продовження TTL кешу

Laravel тепер містить [`Cache::touch(...)`](/docs/{{version}}/cache), що дозволяє продовжити TTL наявного елемента кешу, не отримуючи та не зберігаючи його значення заново.

<a name="semantic-search"></a>
### Семантичний та векторний пошук

Laravel 13 поглиблює підтримку семантичного пошуку завдяки нативним векторним запитам, робочим процесам з ембедингами та відповідним API, описаним у розділах [пошуку](/docs/{{version}}/search#semantic-vector-search), [запитів](/docs/{{version}}/queries#vector-similarity-clauses) та [AI SDK](/docs/{{version}}/ai-sdk#embeddings).

Ці можливості спрощують створення пошуку на основі AI за допомогою PostgreSQL і `pgvector`, зокрема пошук за схожістю щодо ембедингів, згенерованих безпосередньо з рядків.

Наприклад, ви можете виконувати пошук за семантичною схожістю прямо з конструктора запитів:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```
