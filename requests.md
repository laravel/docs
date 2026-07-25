---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# HTTP-запити

- [Вступ](#introduction)
- [Робота із запитом](#interacting-with-the-request)
    - [Доступ до запиту](#accessing-the-request)
    - [Шлях, хост і метод запиту](#request-path-and-method)
    - [Заголовки запиту](#request-headers)
    - [IP-адреса запиту](#request-ip-address)
    - [Узгодження вмісту](#content-negotiation)
    - [Запити PSR-7](#psr7-requests)
- [Вхідні дані](#input)
    - [Отримання вхідних даних](#retrieving-input)
    - [Наявність вхідних даних](#input-presence)
    - [Додавання вхідних даних](#merging-additional-input)
    - [Попередні вхідні дані](#old-input)
    - [Cookie](#cookies)
    - [Обрізання та нормалізація вхідних даних](#input-trimming-and-normalization)
- [Файли](#files)
    - [Отримання завантажених файлів](#retrieving-uploaded-files)
    - [Збереження завантажених файлів](#storing-uploaded-files)
- [Налаштування довірених проксі](#configuring-trusted-proxies)
- [Налаштування довірених хостів](#configuring-trusted-hosts)

<a name="introduction"></a>
## Вступ

Клас `Illuminate\Http\Request` у Laravel дає об'єктно-орієнтований спосіб працювати з поточним HTTP-запитом, який обробляє ваш застосунок, а також отримувати вхідні дані, cookie й файли, надіслані разом із запитом.

<a name="interacting-with-the-request"></a>
## Робота із запитом

<a name="accessing-the-request"></a>
### Доступ до запиту

Щоб отримати екземпляр поточного HTTP-запиту через впровадження залежностей, вкажіть тип `Illuminate\Http\Request` у замиканні маршруту чи методі контролера. [Сервіс-контейнер](/docs/{{version}}/container) Laravel автоматично впровадить екземпляр вхідного запиту:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // Store the user...

        return redirect('/users');
    }
}
```

Як згадувалося, ви також можете вказати тип `Illuminate\Http\Request` у замиканні маршруту. Сервіс-контейнер автоматично впровадить вхідний запит у замикання під час його виконання:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### Впровадження залежностей і параметри маршруту

Якщо ваш метод контролера також очікує вхідні дані з параметра маршруту, перелічуйте параметри маршруту після інших залежностей. Наприклад, якщо ваш маршрут визначено так:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

Ви все одно можете вказати тип `Illuminate\Http\Request` і звертатися до параметра маршруту `id`, визначивши метод контролера так:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### Шлях, хост і метод запиту

Екземпляр `Illuminate\Http\Request` надає різноманітні методи для дослідження вхідного HTTP-запиту й успадковує клас `Symfony\Component\HttpFoundation\Request`. Нижче ми розглянемо кілька найважливіших методів.

<a name="retrieving-the-request-path"></a>
#### Отримання шляху запиту

Метод `path` повертає інформацію про шлях запиту. Тож якщо вхідний запит спрямовано на `http://example.com/foo/bar`, метод `path` поверне `foo/bar`:

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### Перевірка шляху чи маршруту запиту

Метод `is` дозволяє перевірити, чи збігається шлях вхідного запиту із заданим шаблоном. У цьому методі можна використовувати символ `*` як підстановочний:

```php
if ($request->is('admin/*')) {
    // ...
}
```

Методом `routeIs` ви можете визначити, чи збігся вхідний запит із [іменованим маршрутом](/docs/{{version}}/routing#named-routes):

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### Отримання URL запиту

Щоб отримати повний URL вхідного запиту, скористайтеся методами `url` чи `fullUrl`. Метод `url` поверне URL без рядка запиту, а `fullUrl` - разом із ним:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

Якщо ви хочете додати дані рядка запиту до поточного URL, викличте метод `fullUrlWithQuery`. Він об'єднає переданий масив змінних рядка запиту з поточним рядком запиту:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

Якщо ви хочете отримати поточний URL без певного параметра рядка запиту, скористайтеся методом `fullUrlWithoutQuery`:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### Отримання хоста запиту

Отримати «хост» вхідного запиту можна методами `host`, `httpHost` і `schemeAndHttpHost`:

```php
// http://localhost:8000
$request->host(); // localhost
$request->httpHost(); // localhost:8000
$request->schemeAndHttpHost(); // http://localhost:8000
```

<a name="retrieving-the-request-method"></a>
#### Отримання методу запиту

Метод `method` поверне HTTP-метод запиту. Ви можете скористатися методом `isMethod`, щоб перевірити, чи збігається HTTP-метод із заданим рядком:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### Заголовки запиту

Отримати заголовок запиту з екземпляра `Illuminate\Http\Request` можна методом `header`. Якщо заголовка в запиті немає, буде повернуто `null`. Утім, метод `header` приймає необов'язковий другий аргумент, який буде повернуто за відсутності заголовка:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

Метод `hasHeader` дозволяє визначити, чи містить запит певний заголовок:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

Для зручності метод `bearerToken` дозволяє отримати bearer-токен із заголовка `Authorization`. Якщо такого заголовка немає, буде повернуто порожній рядок:

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### IP-адреса запиту

Метод `ip` дозволяє отримати IP-адресу клієнта, який зробив запит до вашого застосунку:

```php
$ipAddress = $request->ip();
```

Якщо ви хочете отримати масив IP-адрес, зокрема всі адреси клієнта, переслані проксі-серверами, скористайтеся методом `ips`. «Початкова» IP-адреса клієнта буде в кінці масиву:

```php
$ipAddresses = $request->ips();
```

Загалом IP-адреси слід вважати недовіреними даними, які контролює користувач, і використовувати лише в інформаційних цілях.

<a name="content-negotiation"></a>
### Узгодження вмісту

Laravel надає кілька методів для дослідження типів вмісту, які запитує вхідний запит, через заголовок `Accept`. Спершу метод `getAcceptableContentTypes` поверне масив усіх типів вмісту, прийнятних для запиту:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

Метод `accepts` приймає масив типів вмісту й повертає `true`, якщо хоч один із них прийнятний для запиту. Інакше буде повернуто `false`:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

Метод `prefers` дозволяє визначити, який тип вмісту з переданого масиву є найбажанішим для запиту. Якщо жоден із наданих типів не прийнятний, буде повернуто `null`:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

Оскільки багато застосунків віддають лише HTML чи JSON, метод `expectsJson` дозволяє швидко визначити, чи очікує вхідний запит JSON-відповідь:

```php
if ($request->expectsJson()) {
    // ...
}
```

Якщо вам потрібно визначити, чи запит саме віддає перевагу Markdown або чи прийме його серед інших типів вмісту - наприклад, коли ви обслуговуєте AI-агентів чи інших клієнтів, що споживають Markdown-відповіді, - скористайтеся методами `wantsMarkdown` і `acceptsMarkdown`:

```php
if ($request->wantsMarkdown()) {
    // The client's most preferred content type is text/markdown...
}

if ($request->acceptsMarkdown()) {
    // The client accepts Markdown responses...
}
```

<a name="psr7-requests"></a>
### Запити PSR-7

[Стандарт PSR-7](https://www.php-fig.org/psr/psr-7/) визначає інтерфейси для HTTP-повідомлень, зокрема запитів і відповідей. Якщо ви хочете отримати екземпляр запиту PSR-7 замість запиту Laravel, спершу потрібно встановити кілька бібліотек. Laravel використовує компонент *Symfony HTTP Message Bridge* для перетворення типових запитів і відповідей Laravel на сумісні з PSR-7 реалізації:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

Встановивши ці бібліотеки, ви можете отримати запит PSR-7, вказавши тип інтерфейсу запиту в замиканні маршруту чи методі контролера:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> Якщо ви повернете з маршруту чи контролера екземпляр відповіді PSR-7, його буде автоматично перетворено назад на екземпляр відповіді Laravel і показано фреймворком.

<a name="input"></a>
## Вхідні дані

<a name="retrieving-input"></a>
### Отримання вхідних даних

<a name="retrieving-all-input-data"></a>
#### Отримання всіх вхідних даних

Ви можете отримати всі вхідні дані запиту як `array` методом `all`. Цей метод працює незалежно від того, надійшов запит із HTML-форми чи є XHR-запитом:

```php
$input = $request->all();
```

Методом `collect` ви можете отримати всі вхідні дані запиту як [колекцію](/docs/{{version}}/collections):

```php
$input = $request->collect();
```

Метод `collect` також дозволяє отримати як колекцію лише частину вхідних даних:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### Отримання окремого значення

За допомогою кількох простих методів ви можете звертатися до всіх вхідних даних користувача з екземпляра `Illuminate\Http\Request`, не переймаючись тим, який HTTP-метод було використано. Незалежно від методу, отримати дані користувача можна методом `input`:

```php
$name = $request->input('name');
```

Ви можете передати значення за замовчуванням другим аргументом методу `input`. Воно повернеться, якщо запитаного значення в запиті немає:

```php
$name = $request->input('name', 'Sally');
```

Працюючи з формами, що містять масиви, використовуйте «крапкову» нотацію для доступу до них:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

Ви можете викликати метод `input` без аргументів, щоб отримати всі вхідні значення як асоціативний масив:

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### Отримання даних із рядка запиту

Тоді як метод `input` отримує значення з усього тіла запиту (включно з рядком запиту), метод `query` бере значення лише з рядка запиту:

```php
$name = $request->query('name');
```

Якщо запитаного значення в рядку запиту немає, буде повернуто другий аргумент цього методу:

```php
$name = $request->query('name', 'Helen');
```

Ви можете викликати метод `query` без аргументів, щоб отримати всі значення рядка запиту як асоціативний масив:

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### Отримання значень із JSON

Надсилаючи JSON-запити до вашого застосунку, ви можете звертатися до JSON-даних методом `input`, якщо заголовок `Content-Type` запиту правильно встановлено в `application/json`. Ви навіть можете скористатися «крапковим» синтаксисом, щоб отримати значення, вкладені в JSON-масиви чи об'єкти:

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Отримання значень як Stringable

Замість отримувати вхідні дані запиту як примітивний `string`, ви можете скористатися методом `string`, щоб отримати їх як екземпляр [Illuminate\Support\Stringable](/docs/{{version}}/strings):

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### Отримання цілочисельних значень

Щоб отримати вхідні значення як цілі числа, скористайтеся методом `integer`. Він спробує привести значення до цілого. Якщо значення відсутнє або приведення не вдалося, буде повернуто вказане вами значення за замовчуванням. Це особливо корисно для пагінації чи інших числових даних:

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### Отримання булевих значень

Працюючи з HTML-елементами на кшталт чекбоксів, ваш застосунок може отримувати «істинні» значення, які насправді є рядками - наприклад, «true» чи «on». Для зручності скористайтеся методом `boolean`, щоб отримати ці значення як булеві. Метод `boolean` повертає `true` для 1, "1", true, "true", "on" та "yes". Усі інші значення дадуть `false`:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### Отримання масивів

Вхідні значення, що містять масиви, можна отримати методом `array`. Він завжди приведе значення до масиву. Якщо запит не містить значення з указаним іменем, буде повернуто порожній масив:

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### Отримання дат

Для зручності вхідні значення з датами чи часом можна отримати як екземпляри Carbon методом `date`. Якщо запит не містить значення з указаним іменем, буде повернуто `null`:

```php
$birthday = $request->date('birthday');
```

Другий і третій аргументи методу `date` дозволяють указати формат дати та часовий пояс відповідно:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

Якщо значення присутнє, але має недійсний формат, буде викинуто `InvalidArgumentException`; тому рекомендуємо валідувати дані перед викликом методу `date`.

<a name="retrieving-interval-input-values"></a>
#### Отримання інтервалів

Вхідні значення, що містять тривалості, можна отримати як екземпляри `CarbonInterval` методом `interval`. Якщо запит не містить значення з указаним іменем, буде повернуто `null`:

```php
$duration = $request->interval('duration');
```

Якщо значення числове, ви можете передати одиницю виміру другим аргументом. Це може бути рядок на кшталт `second`, `minute` чи `day`, або екземпляр enum `Carbon\Unit`:

```php
use Carbon\Unit;

$timeout = $request->interval('timeout', 'second');

$delay = $request->interval('delay', Unit::Minute);
```

Якщо значення присутнє, але має недійсний формат, буде викинуто `InvalidArgumentException`; тому рекомендуємо валідувати дані перед викликом методу `interval`.

<a name="retrieving-enum-input-values"></a>
#### Отримання значень enum

Вхідні значення, що відповідають [enum PHP](https://www.php.net/manual/en/language.types.enumerations.php), також можна отримати із запиту. Якщо запит не містить значення з указаним іменем або enum не має відповідного значення, буде повернуто `null`. Метод `enum` приймає ім'я вхідного значення та клас enum першим і другим аргументами:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

Ви також можете передати значення за замовчуванням, яке повернеться, якщо значення відсутнє чи недійсне:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

Якщо вхідне значення є масивом значень, що відповідають enum PHP, скористайтеся методом `enums`, щоб отримати масив значень як екземпляри enum:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### Отримання даних через динамічні властивості

Ви також можете звертатися до вхідних даних користувача через динамічні властивості екземпляра `Illuminate\Http\Request`. Наприклад, якщо одна з форм вашого застосунку містить поле `name`, ви можете звернутися до його значення так:

```php
$name = $request->name;
```

Використовуючи динамічні властивості, Laravel спершу шукатиме значення параметра в тілі запиту. Якщо його там немає, Laravel шукатиме поле серед параметрів відповідного маршруту.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### Отримання частини вхідних даних

Якщо вам потрібно отримати підмножину вхідних даних, скористайтеся методами `only` та `except`. Обидва приймають один `array` або динамічний список аргументів:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> Метод `only` повертає всі запитані пари «ключ - значення»; однак він не поверне пар, яких немає в запиті.

<a name="input-presence"></a>
### Наявність вхідних даних

Метод `has` дозволяє визначити, чи присутнє значення в запиті. Він повертає `true`, якщо значення присутнє:

```php
if ($request->has('name')) {
    // ...
}
```

Якщо передати масив, метод `has` визначить, чи присутні всі вказані значення:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

Метод `hasAny` повертає `true`, якщо присутнє хоч одне з указаних значень:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

Метод `whenHas` виконає передане замикання, якщо значення присутнє в запиті:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

Методу `whenHas` можна передати друге замикання, яке виконається, якщо вказаного значення в запиті немає:

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

Якщо ви хочете визначити, що значення присутнє в запиті й не є порожнім рядком, скористайтеся методом `filled`:

```php
if ($request->filled('name')) {
    // ...
}
```

Якщо ви хочете визначити, що значення відсутнє в запиті або є порожнім рядком, скористайтеся методом `isNotFilled`:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

Якщо передати масив, метод `isNotFilled` визначить, чи всі вказані значення відсутні або порожні:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

Метод `anyFilled` повертає `true`, якщо хоч одне з указаних значень не є порожнім рядком:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

Метод `whenFilled` виконає передане замикання, якщо значення присутнє в запиті й не є порожнім рядком:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

Методу `whenFilled` можна передати друге замикання, яке виконається, якщо вказане значення не «заповнене»:

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

Щоб визначити, що певного ключа в запиті немає, скористайтеся методами `missing` і `whenMissing`:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a name="merging-additional-input"></a>
### Додавання вхідних даних

Іноді вам може знадобитися вручну додати додаткові дані до наявних вхідних даних запиту. Це робиться методом `merge`. Якщо переданий ключ уже існує в запиті, його буде перезаписано даними, переданими методу `merge`:

```php
$request->merge(['votes' => 0]);
```

Метод `mergeIfMissing` дозволяє додати дані до запиту, якщо відповідних ключів у ньому ще немає:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### Попередні вхідні дані

Laravel дозволяє зберігати вхідні дані одного запиту для наступного. Ця можливість особливо корисна для повторного заповнення форм після виявлення помилок валідації. Утім, якщо ви користуєтеся вбудованими [можливостями валідації](/docs/{{version}}/validation) Laravel, вам, імовірно, не доведеться викликати ці методи вручну, адже частина вбудованих засобів валідації робить це автоматично.

<a name="flashing-input-to-the-session"></a>
#### Запис вхідних даних до сесії

Метод `flash` класу `Illuminate\Http\Request` запише поточні вхідні дані до [сесії](/docs/{{version}}/session), щоб вони були доступні під час наступного запиту користувача:

```php
$request->flash();
```

Ви також можете скористатися методами `flashOnly` та `flashExcept`, щоб записати до сесії лише частину даних запиту. Ці методи корисні, щоб не зберігати в сесії конфіденційну інформацію на кшталт паролів:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### Запис даних із подальшим перенаправленням

Оскільки часто потрібно записати дані до сесії й одразу перенаправити на попередню сторінку, ви можете легко приєднати запис даних до перенаправлення методом `withInput`:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### Отримання попередніх даних

Щоб отримати збережені дані попереднього запиту, викличте метод `old` на екземплярі `Illuminate\Http\Request`. Метод `old` візьме раніше збережені дані із [сесії](/docs/{{version}}/session):

```php
$username = $request->old('username');
```

Laravel також надає глобальний хелпер `old`. Якщо ви показуєте попередні дані в [шаблоні Blade](/docs/{{version}}/blade), зручніше скористатися хелпером `old`, щоб заново заповнити форму. Якщо попередніх даних для вказаного поля немає, буде повернуто `null`:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### Cookie

<a name="retrieving-cookies-from-requests"></a>
#### Отримання cookie із запитів

Усі cookie, створені фреймворком Laravel, зашифровані й підписані кодом автентифікації, тобто вважатимуться недійсними, якщо клієнт їх змінив. Щоб отримати значення cookie із запиту, скористайтеся методом `cookie` на екземплярі `Illuminate\Http\Request`:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## Обрізання та нормалізація вхідних даних

За замовчуванням Laravel додає `middleware` `Illuminate\Foundation\Http\Middleware\TrimStrings` та `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` до глобального стека вашого застосунку. Ці `middleware` автоматично обрізають усі вхідні рядкові поля запиту, а також перетворюють порожні рядки на `null`. Завдяки цьому вам не потрібно перейматися нормалізацією в маршрутах і контролерах.

#### Вимкнення нормалізації вхідних даних

Якщо ви хочете вимкнути цю поведінку для всіх запитів, вилучіть ці два `middleware` зі стека вашого застосунку, викликавши метод `$middleware->remove` у файлі `bootstrap/app.php`:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

Якщо ви хочете вимкнути обрізання рядків і перетворення порожніх рядків лише для частини запитів, скористайтеся методами `trimStrings` і `convertEmptyStringsToNull` у файлі `bootstrap/app.php`. Обидва приймають масив замикань, які мають повертати `true` чи `false`, вказуючи, чи слід пропустити нормалізацію:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a name="files"></a>
## Файли

<a name="retrieving-uploaded-files"></a>
### Отримання завантажених файлів

Отримати завантажені файли з екземпляра `Illuminate\Http\Request` можна методом `file` або через динамічні властивості. Метод `file` повертає екземпляр класу `Illuminate\Http\UploadedFile`, який успадковує PHP-клас `SplFileInfo` і надає різноманітні методи для роботи з файлом:

```php
$file = $request->file('photo');

$file = $request->photo;
```

Визначити, чи присутній файл у запиті, можна методом `hasFile`:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

Якщо завантажений файл є зображенням, яке потрібно обробити перед збереженням, скористайтеся методом `image`, щоб отримати екземпляр `Illuminate\Image\Image`, або `null`, якщо файла немає:

```php
$image = $request->image('photo');
```

Докладніше про обробку зображень читайте в повній [документації з обробки зображень](/docs/{{version}}/images).

<a name="validating-successful-uploads"></a>
#### Перевірка успішності завантаження

Окрім перевірки наявності файлу, ви можете переконатися, що під час завантаження не було проблем, методом `isValid`:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### Шляхи та розширення файлів

Клас `UploadedFile` також містить методи для доступу до повного шляху файлу та його розширення. Метод `extension` спробує вгадати розширення на основі вмісту файлу. Це розширення може відрізнятися від того, що надав клієнт:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### Інші методи файлів

Екземпляри `UploadedFile` мають чимало інших методів. Докладніше про них дивіться в [документації API цього класу](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php).

<a name="storing-uploaded-files"></a>
### Збереження завантажених файлів

Щоб зберегти завантажений файл, ви зазвичай скористаєтеся однією з налаштованих [файлових систем](/docs/{{version}}/filesystem). Клас `UploadedFile` має метод `store`, який перемістить завантажений файл на один із ваших дисків - це може бути розташування в локальній файловій системі чи хмарне сховище на кшталт Amazon S3.

Метод `store` приймає шлях, за яким слід зберегти файл, відносно кореневого каталогу файлової системи. Цей шлях не має містити імені файлу, адже як ім'я автоматично буде згенеровано унікальний ідентифікатор.

Метод `store` також приймає необов'язковий другий аргумент - ім'я диска, на якому слід зберегти файл. Метод поверне шлях до файлу відносно кореня диска:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

Якщо ви не хочете, щоб ім'я файлу генерувалося автоматично, скористайтеся методом `storeAs`, який приймає шлях, ім'я файлу та ім'я диска:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Докладніше про зберігання файлів у Laravel читайте в повній [документації з файлового сховища](/docs/{{version}}/filesystem).

<a name="configuring-trusted-proxies"></a>
## Налаштування довірених проксі

Коли ваші застосунки працюють за балансувальником навантаження, що завершує TLS/SSL-з'єднання, ви можете помітити, що застосунок іноді не генерує HTTPS-посилання через хелпер `url`. Зазвичай це тому, що трафік надходить від балансувальника на порт 80, і застосунок не знає, що має генерувати захищені посилання.

Щоб це виправити, увімкніть `middleware` `Illuminate\Http\Middleware\TrustProxies`, який входить до вашого застосунку Laravel і дозволяє швидко вказати балансувальники чи проксі, яким має довіряти застосунок. Довірені проксі задаються методом `trustProxies` у файлі `bootstrap/app.php`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

Окрім налаштування довірених проксі, ви можете також налаштувати заголовки проксі, яким слід довіряти:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> Якщо ви використовуєте AWS Elastic Load Balancing, значенням `headers` має бути `Request::HEADER_X_FORWARDED_AWS_ELB`. Якщо ваш балансувальник використовує стандартний заголовок `Forwarded` із [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4), значенням `headers` має бути `Request::HEADER_FORWARDED`. Докладніше про константи, які можна використовувати у значенні `headers`, дивіться в документації Symfony щодо [довіри проксі](https://symfony.com/doc/current/deployment/proxies.html).

<a name="trusting-all-proxies"></a>
#### Довіра всім проксі

Якщо ви користуєтеся Amazon AWS чи іншим «хмарним» провайдером балансувальників, ви можете не знати IP-адрес своїх балансувальників. У такому разі скористайтеся `*`, щоб довіряти всім проксі:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## Налаштування довірених хостів

За замовчуванням Laravel відповідатиме на всі отримані запити незалежно від вмісту заголовка `Host`. Крім того, значення заголовка `Host` використовуватиметься під час генерації абсолютних URL до вашого застосунку.

Зазвичай варто налаштувати ваш веб-сервер - Nginx чи Apache - так, щоб він надсилав до застосунку лише запити, що відповідають певному імені хоста. Утім, якщо ви не можете налаштувати веб-сервер напряму й хочете вказати Laravel відповідати лише певним іменам хостів, увімкніть для свого застосунку `middleware` `Illuminate\Http\Middleware\TrustHosts`.

Щоб увімкнути `middleware` `TrustHosts`, викличте метод `trustHosts` у файлі `bootstrap/app.php`. За допомогою аргументу `at` ви можете вказати імена хостів, на які має відповідати ваш застосунок. Рядок імені хоста трактується як регулярний вираз. Вхідні запити з іншими заголовками `Host` буде відхилено:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

За замовчуванням запити з піддоменів URL застосунку теж автоматично вважаються довіреними. Якщо ви хочете вимкнути цю поведінку, скористайтеся аргументом `subdomains`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

Якщо для визначення довірених хостів вам потрібен доступ до конфігураційних файлів чи бази даних застосунку, передайте аргументу `at` замикання:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
