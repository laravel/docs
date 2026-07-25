---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Маршрутизація

- [Базова маршрутизація](#basic-routing)
    - [Типові файли маршрутів](#the-default-route-files)
    - [Маршрути-перенаправлення](#redirect-routes)
    - [Маршрути-представлення](#view-routes)
    - [Перегляд списку маршрутів](#listing-your-routes)
    - [Налаштування маршрутизації](#routing-customization)
- [Параметри маршруту](#route-parameters)
    - [Обов'язкові параметри](#required-parameters)
    - [Необов'язкові параметри](#parameters-optional-parameters)
    - [Обмеження регулярними виразами](#parameters-regular-expression-constraints)
- [Іменовані маршрути](#named-routes)
- [Групи маршрутів](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Контролери](#route-group-controllers)
    - [Маршрутизація піддоменів](#route-group-subdomain-routing)
    - [Префікси маршрутів](#route-group-prefixes)
    - [Префікси імен маршрутів](#route-group-name-prefixes)
- [Прив'язка моделей до маршрутів](#route-model-binding)
    - [Неявна прив'язка](#implicit-binding)
    - [Неявна прив'язка enum](#implicit-enum-binding)
    - [Явна прив'язка](#explicit-binding)
- [Резервні маршрути](#fallback-routes)
- [Обмеження частоти](#rate-limiting)
    - [Визначення обмежувачів частоти](#defining-rate-limiters)
    - [Призначення обмежувачів маршрутам](#attaching-rate-limiters-to-routes)
- [Підміна методу форми](#form-method-spoofing)
- [Доступ до поточного маршруту](#accessing-the-current-route)
- [Спільне використання ресурсів між джерелами (CORS)](#cors)
- [Кешування маршрутів](#route-caching)

<a name="basic-routing"></a>
## Базова маршрутизація

Найпростіші маршрути Laravel приймають URI та замикання, даючи дуже простий і виразний спосіб визначати маршрути й поведінку без складних конфігураційних файлів:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### Типові файли маршрутів

Усі маршрути Laravel визначаються у файлах маршрутів, розташованих у каталозі `routes`. Ці файли автоматично завантажуються Laravel за конфігурацією, вказаною у файлі `bootstrap/app.php` вашого застосунку. Файл `routes/web.php` визначає маршрути для вашого веб-інтерфейсу. Цим маршрутам призначається [група `middleware`](/docs/{{version}}/middleware#laravels-default-middleware-groups) `web`, що дає такі можливості, як стан сесії та захист від CSRF.

Для більшості застосунків ви почнете з визначення маршрутів у файлі `routes/web.php`. До маршрутів, визначених у `routes/web.php`, можна звертатися, ввівши URL маршруту в браузері. Наприклад, до наведеного нижче маршруту можна звернутися, перейшовши на `http://example.com/user`:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### Маршрути API

Якщо ваш застосунок також надаватиме безстанове API, ви можете увімкнути маршрутизацію API командою Artisan `install:api`:

```shell
php artisan install:api
```

Команда `install:api` встановлює [Laravel Sanctum](/docs/{{version}}/sanctum), який надає надійний і водночас простий гард автентифікації за API-токенами - його можна використовувати для автентифікації сторонніх споживачів API, SPA чи мобільних застосунків. Крім того, команда `install:api` створює файл `routes/api.php`:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

Звісно, ви вільні не додавати `middleware` `auth:sanctum` до маршрутів, які мають бути загальнодоступними.

Маршрути у `routes/api.php` є безстановими й належать до [групи `middleware`](/docs/{{version}}/middleware#laravels-default-middleware-groups) `api`. Крім того, до цих маршрутів автоматично застосовується префікс URI `/api`, тож вам не потрібно додавати його вручну до кожного маршруту у файлі. Змінити префікс можна у файлі `bootstrap/app.php`:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### Доступні методи маршрутизатора

Маршрутизатор дозволяє реєструвати маршрути, що відповідають на будь-який HTTP-метод:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

Іноді вам може знадобитися зареєструвати маршрут, що відповідає на кілька HTTP-методів. Це робиться методом `match`. Або ж ви можете зареєструвати маршрут, що відповідає на всі HTTP-методи, методом `any`:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> Визначаючи кілька маршрутів зі спільним URI, маршрути з методами `get`, `post`, `put`, `patch`, `delete` та `options` слід визначати перед маршрутами з методами `any`, `match` і `redirect`. Це гарантує, що вхідний запит буде зіставлено з правильним маршрутом.

<a name="dependency-injection"></a>
#### Впровадження залежностей

Ви можете вказати типи будь-яких потрібних маршруту залежностей у сигнатурі його колбека. Оголошені залежності буде автоматично розв'язано й впроваджено в колбек [сервіс-контейнером](/docs/{{version}}/container) Laravel. Наприклад, ви можете вказати тип `Illuminate\Http\Request`, щоб поточний HTTP-запит автоматично впроваджувався у колбек маршруту:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### Захист від CSRF

Пам'ятайте: будь-які HTML-форми, що вказують на маршрути `POST`, `PUT`, `PATCH` чи `DELETE`, визначені у файлі маршрутів `web`, мають містити поле з CSRF-токеном. Інакше запит буде відхилено. Докладніше про захист від CSRF читайте в [документації з CSRF](/docs/{{version}}/csrf):

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### Маршрути-перенаправлення

Якщо ви визначаєте маршрут, який перенаправляє на інший URI, скористайтеся методом `Route::redirect`. Він дає зручне скорочення, тож вам не доведеться визначати повноцінний маршрут чи контролер заради простого перенаправлення:

```php
Route::redirect('/here', '/there');
```

За замовчуванням `Route::redirect` повертає статус-код `302`. Ви можете змінити його необов'язковим третім параметром:

```php
Route::redirect('/here', '/there', 301);
```

Або ж скористайтеся методом `Route::permanentRedirect`, щоб повернути статус-код `301`:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> Використовуючи параметри маршруту в маршрутах-перенаправленнях, пам'ятайте: параметри `destination` і `status` зарезервовані Laravel і не можуть бути використані.

<a name="view-routes"></a>
### Маршрути-представлення

Якщо ваш маршрут має лише повернути [представлення](/docs/{{version}}/views), скористайтеся методом `Route::view`. Як і метод `redirect`, він дає просте скорочення, тож вам не доведеться визначати повноцінний маршрут чи контролер. Метод `view` приймає URI першим аргументом та ім'я представлення другим. Крім того, ви можете передати масив даних для представлення необов'язковим третім аргументом:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> Використовуючи параметри маршруту в маршрутах-представленнях, пам'ятайте: параметри `view`, `data`, `status` і `headers` зарезервовані Laravel і не можуть бути використані.

<a name="listing-your-routes"></a>
### Перегляд списку маршрутів

Команда Artisan `route:list` дає зручний огляд усіх маршрутів, визначених вашим застосунком:

```shell
php artisan route:list
```

За замовчуванням `middleware`, призначені кожному маршруту, у виводі `route:list` не показуються; однак ви можете вказати Laravel показувати `middleware` маршрутів та імена їхніх груп, додавши до команди опцію `-v`:

```shell
php artisan route:list -v

# Expand middleware groups...
php artisan route:list -vv
```

Ви також можете вказати Laravel показувати лише маршрути, що починаються з певного URI:

```shell
php artisan route:list --path=api
```

Крім того, ви можете сховати маршрути, визначені сторонніми пакетами, передавши опцію `--except-vendor` під час виконання команди `route:list`:

```shell
php artisan route:list --except-vendor
```

І навпаки, ви можете показати лише маршрути, визначені сторонніми пакетами, передавши опцію `--only-vendor`:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### Налаштування маршрутизації

За замовчуванням маршрути вашого застосунку налаштовуються й завантажуються файлом `bootstrap/app.php`:

```php
<?php

use Illuminate\Foundation\Application;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )->create();
```

Утім, іноді вам може знадобитися визначити цілком новий файл для частини маршрутів застосунку. Для цього передайте замикання `then` методу `withRouting`. У цьому замиканні ви можете зареєструвати будь-які додаткові маршрути, потрібні вашому застосунку:

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
    then: function () {
        Route::middleware('api')
            ->prefix('webhooks')
            ->name('webhooks.')
            ->group(base_path('routes/webhooks.php'));
    },
)
```

Або ж ви можете взяти повний контроль над реєстрацією маршрутів, передавши замикання `using` методу `withRouting`. Коли передано цей аргумент, фреймворк не зареєструє жодного HTTP-маршруту, і ви відповідаєте за реєстрацію всіх маршрутів вручну:

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    commands: __DIR__.'/../routes/console.php',
    using: function () {
        Route::middleware('api')
            ->prefix('api')
            ->group(base_path('routes/api.php'));

        Route::middleware('web')
            ->group(base_path('routes/web.php'));
    },
)
```

<a name="route-parameters"></a>
## Параметри маршруту

<a name="required-parameters"></a>
### Обов'язкові параметри

Іноді вам знадобиться захопити сегменти URI у своєму маршруті. Наприклад, вам може знадобитися взяти з URL ідентифікатор користувача. Це робиться визначенням параметрів маршруту:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

Ви можете визначити стільки параметрів маршруту, скільки потрібно:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

Параметри маршруту завжди беруться у фігурні дужки `{}` і мають складатися з літер. Символи підкреслення (`_`) в іменах параметрів теж допустимі. Параметри впроваджуються в колбеки чи контролери маршрутів за їхнім порядком - імена аргументів колбека чи контролера значення не мають.

<a name="parameters-and-dependency-injection"></a>
#### Параметри та впровадження залежностей

Якщо ваш маршрут має залежності, які сервіс-контейнер Laravel має автоматично впровадити в колбек, перелічуйте параметри маршруту після залежностей:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### Необов'язкові параметри

Подекуди вам може знадобитися параметр маршруту, який не завжди присутній в URI. Для цього поставте `?` після імені параметра. Обов'язково задайте відповідній змінній маршруту значення за замовчуванням:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### Обмеження регулярними виразами

Ви можете обмежити формат параметрів маршруту методом `where` на екземплярі маршруту. Метод `where` приймає ім'я параметра та регулярний вираз, що визначає обмеження:

```php
Route::get('/user/{name}', function (string $name) {
    // ...
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function (string $id) {
    // ...
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

Для зручності деякі поширені регулярні вирази мають методи-хелпери, що дозволяють швидко додати обмеження до ваших маршрутів:

```php
Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function (string $name) {
    // ...
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUuid('id');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUlid('id');

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', ['movie', 'song', 'painting']);

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', CategoryEnum::cases());
```

Якщо вхідний запит не відповідає обмеженням маршруту, буде повернуто HTTP-відповідь 404.

<a name="parameters-global-constraints"></a>
#### Глобальні обмеження

Якщо ви хочете, щоб параметр маршруту завжди був обмежений певним регулярним виразом, скористайтеся методом `pattern`. Ці шаблони слід визначати в методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

Щойно шаблон визначено, він автоматично застосовується до всіх маршрутів із цим іменем параметра:

```php
Route::get('/user/{id}', function (string $id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### Закодовані прямі скісні риски

Компонент маршрутизації Laravel дозволяє будь-які символи, окрім `/`, у значеннях параметрів маршруту. Щоб `/` міг бути частиною вашого заповнювача, потрібно явно дозволити це регулярним виразом в умові `where`:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> Закодовані прямі скісні риски підтримуються лише в останньому сегменті маршруту.

<a name="named-routes"></a>
## Іменовані маршрути

Іменовані маршрути дозволяють зручно генерувати URL чи перенаправлення для конкретних маршрутів. Задати ім'я маршруту можна, приєднавши метод `name` до його визначення:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

Ви також можете задавати імена маршрутів для дій контролерів:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> Імена маршрутів завжди мають бути унікальними.

<a name="generating-urls-to-named-routes"></a>
#### Генерація URL до іменованих маршрутів

Щойно ви призначили маршруту ім'я, ви можете використовувати його під час генерації URL чи перенаправлень через функції-хелпери `route` і `redirect`:

```php
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');

return to_route('profile');
```

Якщо іменований маршрут визначає параметри, ви можете передати їх другим аргументом функції `route`. Передані параметри буде автоматично вставлено в згенерований URL у правильних позиціях:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

Якщо ви передасте в масиві додаткові параметри, ці пари «ключ - значення» буде автоматично додано до рядка запиту згенерованого URL:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> Іноді вам може знадобитися задати значення за замовчуванням для параметрів URL у межах усього запиту - наприклад, поточну локаль. Для цього скористайтеся [методом URL::defaults](/docs/{{version}}/urls#default-values).

<a name="inspecting-the-current-route"></a>
#### Перевірка поточного маршруту

Якщо ви хочете визначити, чи спрямовано поточний запит до певного іменованого маршруту, скористайтеся методом `named` на екземплярі Route. Наприклад, ви можете перевірити ім'я поточного маршруту з `middleware` маршруту:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Handle an incoming request.
 *
 * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
 */
public function handle(Request $request, Closure $next): Response
{
    if ($request->route()->named('profile')) {
        // ...
    }

    return $next($request);
}
```

<a name="route-groups"></a>
## Групи маршрутів

Групи маршрутів дозволяють спільно використовувати атрибути маршрутів - як-от `middleware` - для великої кількості маршрутів, не визначаючи ці атрибути для кожного окремо.

Вкладені групи намагаються розумно «об'єднати» атрибути з батьківською групою. `Middleware` та умови `where` об'єднуються, а імена й префікси додаються в кінець. Роздільники просторів імен і скісні риски в префіксах URI додаються автоматично там, де це доречно.

<a name="route-group-middleware"></a>
### Middleware

Щоб призначити [`middleware`](/docs/{{version}}/middleware) усім маршрутам групи, скористайтеся методом `middleware` перед визначенням групи. `Middleware` виконуються в тому порядку, у якому їх перелічено в масиві:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // Uses first & second middleware...
    });

    Route::get('/user/profile', function () {
        // Uses first & second middleware...
    });
});
```

<a name="route-group-controllers"></a>
### Контролери

Якщо група маршрутів використовує той самий [контролер](/docs/{{version}}/controllers), ви можете скористатися методом `controller`, щоб визначити спільний контролер для всіх маршрутів групи. Тоді, визначаючи маршрути, вам потрібно вказати лише метод контролера, який вони викликають:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### Маршрутизація піддоменів

Групи маршрутів також можна використовувати для маршрутизації піддоменів. Піддоменам можна призначати параметри маршруту так само, як і URI, що дозволяє захопити частину піддомену для використання у вашому маршруті чи контролері. Піддомен вказується викликом методу `domain` перед визначенням групи:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a name="route-group-prefixes"></a>
### Префікси маршрутів

Метод `prefix` дозволяє додати кожному маршруту групи вказаний префікс URI. Наприклад, ви можете захотіти додати всім URI маршрутів групи префікс `admin`:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a name="route-group-name-prefixes"></a>
### Префікси імен маршрутів

Метод `name` дозволяє додати кожному імені маршруту в групі вказаний рядок-префікс. Наприклад, ви можете захотіти додати іменам усіх маршрутів групи префікс `admin`. Переданий рядок додається до імені маршруту точно так, як його вказано, тож не забудьте про крапку `.` наприкінці префікса:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## Прив'язка моделей до маршрутів

Впроваджуючи ідентифікатор моделі в маршрут чи дію контролера, ви часто робите запит до бази даних, щоб отримати модель, яка відповідає цьому ідентифікатору. Прив'язка моделей до маршрутів у Laravel дає зручний спосіб автоматично впроваджувати екземпляри моделей просто у ваші маршрути. Наприклад, замість впроваджувати ідентифікатор користувача, ви можете впровадити цілий екземпляр моделі `User`, що відповідає цьому ідентифікатору.

<a name="implicit-binding"></a>
### Неявна прив'язка

Laravel автоматично розв'язує моделі Eloquent, визначені в маршрутах чи діях контролерів, коли імена їхніх типізованих змінних збігаються з іменем сегмента маршруту. Наприклад:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

Оскільки змінна `$user` має тип моделі Eloquent `App\Models\User`, а ім'я змінної збігається із сегментом URI `{user}`, Laravel автоматично впровадить екземпляр моделі з ідентифікатором, що відповідає значенню з URI запиту. Якщо відповідного екземпляра в базі даних не знайдено, автоматично буде згенеровано HTTP-відповідь 404.

Звісно, неявна прив'язка можлива й у методах контролерів. Знову ж таки, зверніть увагу: сегмент URI `{user}` збігається зі змінною `$user` у контролері, яка має тип `App\Models\User`:

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// Route definition...
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller method definition...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### М'яко видалені моделі

Зазвичай неявна прив'язка не отримує моделі, які було [м'яко видалено](/docs/{{version}}/eloquent#soft-deleting). Утім, ви можете вказати неявній прив'язці отримувати такі моделі, приєднавши метод `withTrashed` до визначення маршруту:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### Налаштування ключа

Іноді ви можете захотіти розв'язувати моделі Eloquent за колонкою, відмінною від `id`. Для цього вкажіть колонку у визначенні параметра маршруту:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

Якщо ви хочете, щоб прив'язка моделей завжди використовувала колонку, відмінну від `id`, під час отримання певного класу моделі, застосуйте до моделі Eloquent атрибут `RouteKey`:

```php
use Illuminate\Database\Eloquent\Attributes\RouteKey;
use Illuminate\Database\Eloquent\Model;

#[RouteKey('slug')]
class Post extends Model
{
    // ...
}
```

<a name="implicit-model-binding-scoping"></a>
#### Власні ключі та обмеження області

Неявно прив'язуючи кілька моделей Eloquent в одному визначенні маршруту, ви можете захотіти обмежити другу модель так, щоб вона обов'язково була дочірньою щодо попередньої. Наприклад, розгляньмо визначення маршруту, що отримує допис блогу за slug для конкретного користувача:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Коли ви використовуєте неявну прив'язку з власним ключем як параметр вкладеного маршруту, Laravel автоматично обмежить запит так, щоб отримати вкладену модель через її батька, використовуючи домовленості для вгадування імені зв'язку. У цьому випадку припускатиметься, що модель `User` має зв'язок `posts` (множина від імені параметра маршруту), через який можна отримати модель `Post`.

За бажанням ви можете вказати Laravel обмежувати «дочірні» прив'язки навіть тоді, коли власного ключа не передано. Для цього викличте метод `scopeBindings` під час визначення маршруту:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

Або ж ви можете вказати цілій групі визначень маршрутів використовувати прив'язки з обмеженою областю:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

Так само ви можете явно вказати Laravel не обмежувати прив'язки, викликавши метод `withoutScopedBindings`:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### Налаштування поведінки для відсутньої моделі

Зазвичай, якщо неявно прив'язану модель не знайдено, генерується HTTP-відповідь 404. Утім, ви можете налаштувати цю поведінку, викликавши метод `missing` під час визначення маршруту. Метод `missing` приймає замикання, яке буде викликано, якщо неявно прив'язану модель не вдалося знайти:

```php
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->name('locations.view')
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

<a name="implicit-enum-binding"></a>
### Неявна прив'язка enum

PHP 8.1 запровадив підтримку [enum](https://www.php.net/manual/en/language.enumerations.backed.php). Доповнюючи цю можливість, Laravel дозволяє вказати у визначенні маршруту тип [enum на основі рядка](https://www.php.net/manual/en/language.enumerations.backed.php), і Laravel викличе маршрут лише тоді, коли сегмент маршруту відповідає дійсному значенню enum. Інакше автоматично буде повернуто HTTP-відповідь 404. Наприклад, маючи такий enum:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

Ви можете визначити маршрут, який буде викликано лише тоді, коли сегмент `{category}` дорівнює `fruits` чи `people`. Інакше Laravel поверне HTTP-відповідь 404:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### Явна прив'язка

Ви не зобов'язані використовувати неявне розв'язання моделей за домовленостями, щоб користуватися прив'язкою моделей. Ви також можете явно визначити, як параметри маршруту відповідають моделям. Щоб зареєструвати явну прив'язку, скористайтеся методом `model` маршрутизатора, вказавши клас для певного параметра. Явні прив'язки моделей слід визначати на початку методу `boot` вашого класу `AppServiceProvider`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

Далі визначте маршрут, що містить параметр `{user}`:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

Оскільки ми прив'язали всі параметри `{user}` до моделі `App\Models\User`, у маршрут буде впроваджено екземпляр цього класу. Тож, наприклад, запит до `users/1` впровадить екземпляр `User` із бази даних, що має ідентифікатор `1`.

Якщо відповідного екземпляра в базі даних не знайдено, автоматично буде згенеровано HTTP-відповідь 404.

<a name="customizing-the-resolution-logic"></a>
#### Налаштування логіки розв'язання

Якщо ви хочете визначити власну логіку розв'язання прив'язок моделей, скористайтеся методом `Route::bind`. Замикання, передане методу `bind`, отримає значення сегмента URI й має повернути екземпляр класу, який слід впровадити в маршрут. Знову ж таки, це налаштування має відбуватися в методі `boot` вашого `AppServiceProvider`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

Як альтернативу ви можете перевизначити метод `resolveRouteBinding` у своїй моделі Eloquent. Він отримає значення сегмента URI й має повернути екземпляр класу для впровадження в маршрут:

```php
/**
 * Retrieve the model for a bound value.
 *
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

Якщо маршрут використовує [обмеження області неявних прив'язок](#implicit-model-binding-scoping), для розв'язання дочірньої прив'язки батьківської моделі буде використано метод `resolveChildRouteBinding`:

```php
/**
 * Retrieve the child model for a bound value.
 *
 * @param  string  $childType
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

<a name="fallback-routes"></a>
## Резервні маршрути

За допомогою методу `Route::fallback` ви можете визначити маршрут, який виконуватиметься, коли жоден інший маршрут не збігається з вхідним запитом. Зазвичай необроблені запити автоматично рендерять сторінку «404» через обробник винятків вашого застосунку. Однак оскільки резервний маршрут ви зазвичай визначаєте у файлі `routes/web.php`, до нього застосовуватимуться всі `middleware` групи `web`. Ви вільні додавати до цього маршруту й інші `middleware` за потреби:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## Обмеження частоти

<a name="defining-rate-limiters"></a>
### Визначення обмежувачів частоти

Laravel містить потужні й гнучкі сервіси обмеження частоти, якими можна скористатися, щоб обмежити обсяг трафіку для певного маршруту чи групи маршрутів. Щоб почати, визначте конфігурації обмежувачів, що відповідають потребам вашого застосунку.

Обмежувачі частоти можна визначати в методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

Обмежувачі визначаються методом `for` фасаду `RateLimiter`. Метод `for` приймає ім'я обмежувача й замикання, що повертає конфігурацію обмеження для маршрутів, яким призначено цей обмежувач. Конфігурації обмежень є екземплярами класу `Illuminate\Cache\RateLimiting\Limit`. Цей клас містить корисні методи-будівельники, щоб ви могли швидко визначити своє обмеження. Ім'ям обмежувача може бути будь-який рядок:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

Якщо вхідний запит перевищує вказане обмеження, Laravel автоматично поверне відповідь зі статус-кодом 429. Якщо ви хочете визначити власну відповідь для перевищення обмеження, скористайтеся методом `response`:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

Оскільки колбеки обмежувачів отримують екземпляр вхідного HTTP-запиту, ви можете будувати відповідне обмеження динамічно на основі запиту чи автентифікованого користувача:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()?->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### Сегментація обмежень частоти

Іноді ви можете захотіти сегментувати обмеження за якимось довільним значенням. Наприклад, ви можете дозволити користувачам звертатися до маршруту 100 разів на хвилину з однієї IP-адреси. Для цього скористайтеся методом `by` під час побудови обмеження:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

Проілюструймо цю можливість ще одним прикладом: ми можемо обмежити доступ до маршруту до 100 разів на хвилину для автентифікованого користувача або 10 разів на хвилину з IP-адреси для гостей:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### Кілька обмежень частоти

За потреби ви можете повернути масив обмежень для конфігурації обмежувача. Кожне обмеження оцінюватиметься для маршруту в тому порядку, у якому їх розміщено в масиві:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

Якщо ви призначаєте кілька обмежень, сегментованих однаковими значеннями `by`, переконайтеся, що кожне значення `by` унікальне. Найпростіший спосіб цього досягти - додати до переданих методу `by` значень префікси:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### Обмеження частоти на основі відповіді

Окрім обмеження вхідних запитів, Laravel дозволяє обмежувати частоту на основі відповіді за допомогою методу `after`. Це корисно, коли ви хочете зараховувати до обмеження лише певні відповіді - як-от помилки валідації, відповіді 404 чи інші конкретні HTTP-статуси.

Метод `after` приймає замикання, яке отримує відповідь і має повернути `true`, якщо цю відповідь слід зарахувати до обмеження, або `false`, якщо її слід проігнорувати. Це особливо корисно, щоб запобігти атакам перебору, обмеживши послідовні відповіді 404, або щоб дозволити користувачам повторювати запити, які не пройшли валідацію, не вичерпуючи ліміт на точці, що має обмежувати лише успішні операції:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // Only count 404 responses toward the rate limit to prevent enumeration...
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### Призначення обмежувачів маршрутам

Обмежувачі частоти можна призначати маршрутам чи групам маршрутів за допомогою [`middleware`](/docs/{{version}}/middleware) `throttle`. Цей `middleware` приймає ім'я обмежувача, який ви хочете призначити маршруту:

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        // ...
    });

    Route::post('/video', function () {
        // ...
    });
});
```

<a name="throttling-with-redis"></a>
#### Обмеження частоти з Redis

За замовчуванням `middleware` `throttle` зіставлено з класом `Illuminate\Routing\Middleware\ThrottleRequests`. Однак якщо ви використовуєте Redis як драйвер кешу застосунку, ви можете захотіти вказати Laravel керувати обмеженням частоти через Redis. Для цього скористайтеся методом `throttleWithRedis` у файлі `bootstrap/app.php`. Він зіставляє `middleware` `throttle` із класом `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## Підміна методу форми

HTML-форми не підтримують дій `PUT`, `PATCH` чи `DELETE`. Тож, визначаючи маршрути `PUT`, `PATCH` чи `DELETE`, які викликаються з HTML-форми, вам потрібно додати до форми приховане поле `_method`. Значення, надіслане з полем `_method`, буде використано як метод HTTP-запиту:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

Для зручності ви можете скористатися [директивою Blade](/docs/{{version}}/blade) `@method`, щоб згенерувати поле `_method`:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## Доступ до поточного маршруту

Ви можете скористатися методами `current`, `currentRouteName` і `currentRouteAction` фасаду `Route`, щоб отримати інформацію про маршрут, який обробляє вхідний запит:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

Щоб переглянути всі доступні методи маршрутизатора та класів маршрутів, зверніться до документації API [базового класу фасаду Route](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) та [екземпляра Route](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Route.html).

<a name="cors"></a>
## Спільне використання ресурсів між джерелами (CORS)

Laravel може автоматично відповідати на HTTP-запити CORS `OPTIONS` значеннями, які ви налаштуєте. Запити `OPTIONS` автоматично обробляє [`middleware`](/docs/{{version}}/middleware) `HandleCors`, який автоматично входить до глобального стека вашого застосунку.

Іноді вам може знадобитися налаштувати значення конфігурації CORS. Це можна зробити, опублікувавши конфігураційний файл `cors` командою Artisan `config:publish`:

```shell
php artisan config:publish cors
```

Ця команда розмістить конфігураційний файл `cors.php` у каталозі `config` вашого застосунку.

> [!NOTE]
> Докладніше про CORS і заголовки CORS читайте у [веб-документації MDN щодо CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers).

<a name="route-caching"></a>
## Кешування маршрутів

Розгортаючи застосунок у продакшені, скористайтеся кешем маршрутів Laravel. Використання кешу різко зменшить час, потрібний для реєстрації всіх маршрутів вашого застосунку. Щоб згенерувати кеш маршрутів, виконайте команду Artisan `route:cache`:

```shell
php artisan route:cache
```

Після виконання цієї команди закешований файл маршрутів завантажуватиметься під час кожного запиту. Пам'ятайте: якщо ви додасте нові маршрути, вам потрібно буде згенерувати новий кеш. Через це команду `route:cache` варто виконувати лише під час розгортання проєкту.

Щоб очистити кеш маршрутів, скористайтеся командою `route:clear`:

```shell
php artisan route:clear
```
