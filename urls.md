---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Генерація URL

- [Вступ](#introduction)
- [Основи](#the-basics)
    - [Генерація URL](#generating-urls)
    - [Доступ до поточного URL](#accessing-the-current-url)
- [URL для іменованих маршрутів](#urls-for-named-routes)
    - [Підписані URL](#signed-urls)
- [URL для дій контролерів](#urls-for-controller-actions)
- [Плинні об'єкти URI](#fluent-uri-objects)
- [Значення за замовчуванням](#default-values)

<a name="introduction"></a>
## Вступ

Laravel надає кілька хелперів, які допомагають генерувати URL для вашого застосунку. Вони насамперед корисні, коли ви створюєте посилання у шаблонах і відповідях API або генеруєте відповіді-перенаправлення до іншої частини застосунку.

<a name="the-basics"></a>
## Основи

<a name="generating-urls"></a>
### Генерація URL

Хелпер `url` дозволяє генерувати довільні URL для вашого застосунку. Згенерований URL автоматично використає схему (HTTP чи HTTPS) і хост із поточного запиту, який обробляє застосунок:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

Щоб згенерувати URL із параметрами рядка запиту, скористайтеся методом `query`:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

Передавання параметрів рядка запиту, які вже є у шляху, перезапише їхні наявні значення:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

Як параметри запиту можна також передавати масиви значень. Ці значення отримають коректні ключі й будуть закодовані у згенерованому URL:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### Доступ до поточного URL

Якщо хелперу `url` не передано шляху, повертається екземпляр `Illuminate\Routing\UrlGenerator`, що дає доступ до інформації про поточний URL:

```php
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();
```

До кожного з цих методів можна також звернутися через [фасад](/docs/{{version}}/facades) `URL`:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="accessing-the-previous-url"></a>
#### Доступ до попереднього URL

Іноді корисно знати попередній URL, з якого прийшов користувач. Отримати його можна методами `previous` і `previousPath` хелпера `url`:

```php
// Get the full URL for the previous request...
echo url()->previous();

// Get the path for the previous request...
echo url()->previousPath();
```

Або ж через [сесію](/docs/{{version}}/session) ви можете отримати попередній URL як екземпляр [плинного URI](#fluent-uri-objects):

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});
```

Через сесію також можна отримати ім'я маршруту попередньо відвіданого URL:

```php
$previousRoute = $request->session()->previousRoute();
```

<a name="urls-for-named-routes"></a>
## URL для іменованих маршрутів

Хелпер `route` дозволяє генерувати URL до [іменованих маршрутів](/docs/{{version}}/routing#named-routes). Іменовані маршрути дають змогу генерувати URL, не прив'язуючись до фактичної адреси, визначеної в маршруті. Тому якщо URL маршруту зміниться, ваші виклики функції `route` змінювати не доведеться. Наприклад, уявіть, що ваш застосунок містить такий маршрут:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

Щоб згенерувати URL до цього маршруту, скористайтеся хелпером `route` так:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

Звісно, хелпер `route` можна використовувати й для маршрутів із кількома параметрами:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

Будь-які додаткові елементи масиву, що не відповідають параметрам у визначенні маршруту, буде додано до рядка запиту URL:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Моделі Eloquent

Часто ви генеруватимете URL за ключем маршруту (зазвичай первинним ключем) [моделей Eloquent](/docs/{{version}}/eloquent). Тому ви можете передавати моделі Eloquent як значення параметрів - хелпер `route` автоматично візьме ключ маршруту моделі:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### Підписані URL

Laravel дозволяє легко створювати «підписані» URL до іменованих маршрутів. До рядка запиту таких URL додається хеш-«підпис», що дозволяє Laravel перевірити, чи не змінювався URL після створення. Підписані URL особливо корисні для маршрутів, які є загальнодоступними, але потребують шару захисту від маніпуляцій з адресою.

Наприклад, підписані URL можна використати для публічного посилання «відписатися», яке надсилають клієнтам електронною поштою. Щоб створити підписаний URL до іменованого маршруту, скористайтеся методом `signedRoute` фасаду `URL`:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

Ви можете виключити домен із хешу підписаного URL, передавши методу `signedRoute` аргумент `absolute`:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

Якщо ви хочете згенерувати тимчасовий підписаний URL маршруту, що спливає через певний час, скористайтеся методом `temporarySignedRoute`. Перевіряючи тимчасовий підписаний URL, Laravel переконається, що закодована в ньому мітка часу спливання ще не минула:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### Перевірка запитів до підписаних маршрутів

Щоб перевірити, чи має вхідний запит дійсний підпис, викличте метод `hasValidSignature` на екземплярі `Illuminate\Http\Request`:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

Іноді фронтенду вашого застосунку потрібно додавати дані до підписаного URL - наприклад, під час пагінації на боці клієнта. Тому ви можете вказати параметри рядка запиту, які слід ігнорувати під час перевірки підписаного URL, методом `hasValidSignatureWhileIgnoring`. Пам'ятайте: ігнорування параметрів дозволяє будь-кому змінювати їх у запиті:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

Замість перевіряти підписані URL через екземпляр вхідного запиту, ви можете призначити маршруту [`middleware`](/docs/{{version}}/middleware) `signed` (`Illuminate\Routing\Middleware\ValidateSignature`). Якщо вхідний запит не має дійсного підпису, `middleware` автоматично поверне HTTP-відповідь `403`:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

Якщо ваші підписані URL не містять домену в хеші, передайте `middleware` аргумент `relative`:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### Реакція на недійсні підписані маршрути

Коли хтось відвідує підписаний URL, термін дії якого сплив, він отримає загальну сторінку помилки для HTTP-статусу `403`. Однак ви можете налаштувати цю поведінку, визначивши власне замикання «render» для винятку `InvalidSignatureException` у файлі `bootstrap/app.php` вашого застосунку:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## URL для дій контролерів

Функція `action` генерує URL для вказаної дії контролера:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

Якщо метод контролера приймає параметри маршруту, ви можете передати асоціативний масив параметрів другим аргументом функції:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## Плинні об'єкти URI

Клас `Uri` Laravel надає зручний плинний інтерфейс для створення URI та роботи з ними через об'єкти. Цей клас обгортає функціональність пакета League URI й бездоганно інтегрується із системою маршрутизації Laravel.

Створити екземпляр `Uri` легко за допомогою статичних методів:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();

// Generate a URI instance from the previous request URL...
$uri = $request->session()->previousUri();
```

Маючи екземпляр URI, ви можете плинно його змінювати:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

Докладніше про роботу з плинними об'єктами URI дивіться в [документації URI](/docs/{{version}}/helpers#uri).

<a name="default-values"></a>
## Значення за замовчуванням

У деяких застосунках вам може знадобитися задати значення за замовчуванням для певних параметрів URL у межах усього запиту. Наприклад, уявіть, що багато ваших маршрутів визначають параметр `{locale}`:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

Марудно щоразу передавати `locale`, викликаючи хелпер `route`. Тож ви можете скористатися методом `URL::defaults`, щоб задати значення за замовчуванням для цього параметра, яке застосовуватиметься протягом поточного запиту. Цей метод варто викликати з [`middleware` маршруту](/docs/{{version}}/middleware#assigning-middleware-to-routes), щоб мати доступ до поточного запиту:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;
use Symfony\Component\HttpFoundation\Response;

class SetDefaultLocaleForUrls
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

Щойно значення за замовчуванням для параметра `locale` задано, вам більше не потрібно передавати його, генеруючи URL хелпером `route`.

<a name="url-defaults-middleware-priority"></a>
#### Значення URL за замовчуванням і пріоритет middleware

Задавання значень URL за замовчуванням може заважати обробці неявних прив'язок моделей у Laravel. Тому вам слід [задати пріоритет своєму `middleware`](/docs/{{version}}/middleware#sorting-middleware), який встановлює ці значення, щоб він виконувався перед власним `middleware` `SubstituteBindings` від Laravel. Це можна зробити методом `priority` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
