---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Sanctum

- [Вступ](#introduction)
    - [Як це працює](#how-it-works)
- [Встановлення](#installation)
- [Конфігурація](#configuration)
    - [Перевизначення стандартних моделей](#overriding-default-models)
- [Автентифікація через API-токени](#api-token-authentication)
    - [Видача API-токенів](#issuing-api-tokens)
    - [Можливості токенів](#token-abilities)
    - [Захист маршрутів](#protecting-routes)
    - [Відкликання токенів](#revoking-tokens)
    - [Термін дії токенів](#token-expiration)
- [Автентифікація SPA](#spa-authentication)
    - [Конфігурація](#spa-configuration)
    - [Автентифікація](#spa-authenticating)
    - [Захист маршрутів](#protecting-spa-routes)
    - [Авторизація приватних каналів бродкастингу](#authorizing-private-broadcast-channels)
- [Автентифікація мобільних застосунків](#mobile-application-authentication)
    - [Видача API-токенів](#issuing-mobile-api-tokens)
    - [Захист маршрутів](#protecting-mobile-api-routes)
    - [Відкликання токенів](#revoking-mobile-api-tokens)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

[Laravel Sanctum](https://github.com/laravel/sanctum) надає легку як пір'їнка систему автентифікації для SPA (односторінкових застосунків), мобільних застосунків і простих API на токенах. Sanctum дозволяє кожному користувачеві вашого застосунку генерувати кілька API-токенів для свого облікового запису. Цим токенам можна надати можливості / скопи, які визначають, які дії дозволено виконувати з токеном.

<a name="how-it-works"></a>
### Як це працює

Laravel Sanctum існує, щоб розв'язати дві окремі проблеми. Обговорімо кожну з них, перш ніж заглиблюватися в бібліотеку.

<a name="how-it-works-api-tokens"></a>
#### API-токени

По-перше, Sanctum - це простий пакет, яким ви можете видавати API-токени своїм користувачам без складнощів OAuth. Ця можливість надихнута GitHub та іншими застосунками, які видають «персональні токени доступу». Уявіть, наприклад, що в «налаштуваннях облікового запису» вашого застосунку є екран, де користувач може згенерувати API-токен. Sanctum дозволяє генерувати такі токени й керувати ними. Зазвичай вони мають дуже довгий термін дії (роки), але користувач може будь-коли відкликати їх вручну.

Laravel Sanctum реалізує цю можливість, зберігаючи API-токени користувачів в одній таблиці бази даних і автентифікуючи вхідні HTTP-запити через заголовок `Authorization`, який має містити дійсний API-токен.

<a name="how-it-works-spa-authentication"></a>
#### Автентифікація SPA

По-друге, Sanctum пропонує простий спосіб автентифікувати односторінкові застосунки (SPA), яким треба спілкуватися з API на Laravel. Такі SPA можуть жити в тому самому репозиторії, що й ваш застосунок Laravel, або в цілком окремому - наприклад, SPA, створений на Next.js чи Nuxt.

Для цієї можливості Sanctum не використовує жодних токенів. Натомість Sanctum спирається на вбудовані сервіси сесійної автентифікації Laravel на основі cookie. Зазвичай для цього Sanctum використовує гард автентифікації `web`. Це дає переваги захисту від CSRF, сесійної автентифікації, а також захищає від витоку облікових даних через XSS.

Sanctum намагатиметься автентифікувати через cookie лише тоді, коли вхідний запит надходить із фронтенду вашого власного SPA. Перевіряючи вхідний HTTP-запит, Sanctum спершу шукає cookie автентифікації, а якщо його немає - перевіряє заголовок `Authorization` на наявність дійсного API-токена.

> [!NOTE]
> Цілком нормально користуватися Sanctum лише для автентифікації через API-токени або лише для автентифікації SPA. Використання Sanctum не зобов'язує вас застосовувати обидві його можливості.

<a name="installation"></a>
## Встановлення

Ви можете встановити Laravel Sanctum артизан-командою `install:api`:

```shell
php artisan install:api
```

Далі, якщо ви плануєте автентифікувати через Sanctum ваш SPA, зверніться до розділу [Автентифікація SPA](#spa-authentication) цієї документації.

<a name="configuration"></a>
## Конфігурація

<a name="overriding-default-models"></a>
### Перевизначення стандартних моделей

Хоча зазвичай це не потрібно, ви вільні розширити модель `PersonalAccessToken`, яку Sanctum використовує всередині:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

Далі ви можете вказати Sanctum використовувати вашу модель через метод `usePersonalAccessTokenModel`, який надає Sanctum. Зазвичай цей метод викликають у методі `boot` файлу `AppServiceProvider` вашого застосунку:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## Автентифікація через API-токени

> [!NOTE]
> Вам не слід автентифікувати власний SPA через API-токени. Натомість скористайтеся вбудованими [можливостями автентифікації SPA](#spa-authentication) у Sanctum.

<a name="issuing-api-tokens"></a>
### Видача API-токенів

Sanctum дозволяє видавати API-токени / персональні токени доступу, якими можна автентифікувати API-запити до вашого застосунку. Роблячи запити з API-токеном, передавайте його в заголовку `Authorization` як токен `Bearer`.

Щоб почати видавати токени користувачам, ваша модель User має використовувати трейт `Laravel\Sanctum\HasApiTokens`:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

Щоб видати токен, скористайтеся методом `createToken`. Метод `createToken` повертає екземпляр `Laravel\Sanctum\NewAccessToken`. API-токени хешуються через SHA-256 перед збереженням у вашій базі даних, але ви можете отримати значення токена відкритим текстом через властивість `plainTextToken` екземпляра `NewAccessToken`. Це значення слід показати користувачеві одразу після створення токена:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

Ви можете дістатися всіх токенів користувача через зв'язок Eloquent `tokens`, який надає трейт `HasApiTokens`:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### Можливості токенів

Sanctum дозволяє призначати токенам «можливості» (abilities). Можливості слугують схожій меті, що й «скопи» в OAuth. Ви можете передати масив рядків-можливостей другим аргументом до методу `createToken`:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Обробляючи вхідний запит, автентифікований через Sanctum, ви можете визначити, чи має токен задану можливість, методами `tokenCan` чи `tokenCant`:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### Middleware для можливостей токенів

Sanctum також містить два `middleware`, якими можна перевірити, що вхідний запит автентифіковано токеном із заданою можливістю. Для початку визначте у файлі `bootstrap/app.php` вашого застосунку такі аліаси `middleware`:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

`middleware` `abilities` можна призначити маршруту, щоб перевірити, що токен вхідного запиту має **усі** перелічені можливості:

```php
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`middleware` `ability` можна призначити маршруту, щоб перевірити, що токен вхідного запиту має *хоча б одну* з перелічених можливостей:

```php
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### Запити, ініційовані власним UI

Для зручності метод `tokenCan` завжди повертатиме `true`, якщо вхідний автентифікований запит надійшов із вашого власного SPA й ви користуєтеся вбудованою [автентифікацією SPA](#spa-authentication) у Sanctum.

Проте це не означає, що ваш застосунок зобов'язаний дозволити користувачеві виконати дію. Зазвичай [політики авторизації](/docs/{{version}}/authorization#creating-policies) вашого застосунку визначатимуть і те, чи надано токену дозвіл виконувати ці можливості, і те, чи має право виконати дію сам користувач.

Наприклад, якщо уявити застосунок для керування серверами, це може означати перевірку того, що токену дозволено оновлювати сервери **і** що сервер належить користувачеві:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

Спершу може здатися дивним, що метод `tokenCan` можна викликати й він завжди повертає `true` для запитів, ініційованих власним UI; проте зручно завжди мати змогу припускати, що API-токен доступний і його можна перевірити методом `tokenCan`. Завдяки такому підходу ви можете завжди викликати метод `tokenCan` у політиках авторизації вашого застосунку, не переймаючись тим, чи запит надійшов з UI вашого застосунку, чи його ініціював хтось зі сторонніх споживачів вашого API.

<a name="protecting-routes"></a>
### Захист маршрутів

Щоб захистити маршрути так, аби всі вхідні запити мали бути автентифікованими, додайте гард автентифікації `sanctum` до ваших захищених маршрутів у файлах `routes/web.php` та `routes/api.php`. Цей гард гарантуватиме, що вхідні запити або автентифіковані як stateful-запити через cookie, або містять заголовок із дійсним API-токеном, якщо запит надійшов від третьої сторони.

Ви можете замислитися, чому ми радимо автентифікувати гардом `sanctum` і маршрути у файлі `routes/web.php`. Пам'ятайте: Sanctum спершу спробує автентифікувати вхідні запити через звичайний сесійний cookie автентифікації Laravel. Якщо цього cookie немає, Sanctum спробує автентифікувати запит токеном із заголовка `Authorization`. До того ж автентифікація всіх запитів через Sanctum гарантує, що ми завжди зможемо викликати метод `tokenCan` на екземплярі поточного автентифікованого користувача:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### Відкликання токенів

Ви можете «відкликати» токени, видаливши їх зі своєї бази даних через зв'язок `tokens`, який надає трейт `Laravel\Sanctum\HasApiTokens`:

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### Термін дії токенів

За замовчуванням токени Sanctum ніколи не спливають, і їх можна знеструмити лише [відкликанням](#revoking-tokens). Проте якщо ви хочете задати час дії API-токенів вашого застосунку, зробіть це через опцію конфігурації `expiration` у вашому конфігураційному файлі `sanctum`. Ця опція визначає кількість хвилин, після яких виданий токен вважатиметься простроченим:

```php
'expiration' => 525600,
```

Якщо ви хочете задати термін дії кожного токена окремо, передайте його третім аргументом до методу `createToken`:

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

Якщо ви налаштували термін дії токенів для свого застосунку, вам, можливо, варто також [запланувати завдання](/docs/{{version}}/scheduling), яке прибиратиме прострочені токени. На щастя, Sanctum містить артизан-команду `sanctum:prune-expired` саме для цього. Наприклад, ви можете налаштувати заплановане завдання, яке видалятиме всі записи токенів, прострочених щонайменше 24 години:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## Автентифікація SPA

Sanctum також існує, щоб дати простий спосіб автентифікувати односторінкові застосунки (SPA), яким треба спілкуватися з API на Laravel. Такі SPA можуть жити в тому самому репозиторії, що й ваш застосунок Laravel, або в цілком окремому.

Для цієї можливості Sanctum не використовує жодних токенів. Натомість Sanctum спирається на вбудовані сервіси сесійної автентифікації Laravel на основі cookie. Такий підхід до автентифікації дає переваги захисту від CSRF, сесійної автентифікації, а також захищає від витоку облікових даних через XSS.

> [!WARNING]
> Щоб автентифікація працювала, ваш SPA та API мають бути на одному домені верхнього рівня. Проте вони можуть бути на різних піддоменах. Крім того, надсилайте із запитом заголовок `Accept: application/json` і заголовок `Referer` чи `Origin`.

<a name="spa-configuration"></a>
### Конфігурація

<a name="configuring-your-first-party-domains"></a>
#### Налаштування власних доменів

Спершу вам треба вказати, з яких доменів ваш SPA робитиме запити. Налаштувати ці домени можна через опцію конфігурації `stateful` у вашому конфігураційному файлі `sanctum`. Ця настройка визначає, які домени підтримуватимуть «stateful»-автентифікацію через сесійні cookie Laravel під час запитів до вашого API.

Щоб допомогти вам налаштувати власні stateful-домени, Sanctum надає дві допоміжні функції, які можна включити до конфігурації. Перша, `Sanctum::currentApplicationUrlWithPort()`, поверне поточний URL застосунку зі змінної оточення `APP_URL`, а `Sanctum::currentRequestHost()` вставить до списку stateful-доменів плейсхолдер, який під час виконання буде замінено на хост із поточного запиту, - тож усі запити з тим самим доменом вважатимуться stateful.

> [!WARNING]
> Якщо ви звертаєтеся до застосунку за URL із портом (`127.0.0.1:8000`), обов'язково вкажіть номер порту разом із доменом.

<a name="sanctum-middleware"></a>
#### Middleware Sanctum

Далі вам слід указати Laravel, що вхідні запити з вашого SPA можуть автентифікуватися через сесійні cookie Laravel, водночас дозволивши запитам від третіх сторін чи мобільних застосунків автентифікуватися через API-токени. Легко зробити це можна викликом методу `middleware` `statefulApi` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS і cookie

Якщо у вас виникають проблеми з автентифікацією у вашому застосунку з SPA, що працює на окремому піддомені, ви, найімовірніше, неправильно налаштували CORS (Cross-Origin Resource Sharing) або сесійні cookie.

Конфігураційний файл `config/cors.php` за замовчуванням не публікується. Якщо вам треба налаштувати опції CORS у Laravel, опублікуйте повний конфігураційний файл `cors` артизан-командою `config:publish`:

```shell
php artisan config:publish cors
```

Далі переконайтеся, що конфігурація CORS вашого застосунку повертає заголовок `Access-Control-Allow-Credentials` зі значенням `True`. Це можна зробити, встановивши опцію `supports_credentials` у вашому файлі `config/cors.php` у значення `true`.

Крім того, увімкніть опції `withCredentials` та `withXSRFToken` на глобальному екземплярі `axios` вашого застосунку. Зробити це можна у файлі `resources/js/app.js`. Якщо ви не користуєтеся Axios для HTTP-запитів із фронтенду, виконайте рівнозначну конфігурацію у своєму HTTP-клієнті:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

Нарешті, переконайтеся, що конфігурація домену сесійних cookie вашого застосунку підтримує будь-який піддомен вашого кореневого домену. Для цього додайте до домену провідну крапку `.` у вашому конфігураційному файлі `config/session.php`:

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### Автентифікація

<a name="csrf-protection"></a>
#### Захист від CSRF

Щоб автентифікувати ваш SPA, сторінка «входу» вашого SPA має спершу зробити запит до ендпоїнта `/sanctum/csrf-cookie`, щоб ініціалізувати захист від CSRF:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

Під час цього запиту Laravel установить cookie `XSRF-TOKEN` з поточним CSRF-токеном. Далі цей токен слід декодувати з URL і передавати в заголовку `X-XSRF-TOKEN` у наступних запитах - деякі HTTP-клієнти на кшталт Axios чи Angular HttpClient зроблять це за вас автоматично. Якщо ваша JavaScript-бібліотека не встановлює це значення сама, вам доведеться вручну задати заголовок `X-XSRF-TOKEN` так, щоб він відповідав URL-декодованому значенню cookie `XSRF-TOKEN`, встановленого цим маршрутом.

<a name="logging-in"></a>
#### Вхід

Коли захист від CSRF ініціалізовано, зробіть запит `POST` до маршруту `/login` вашого застосунку Laravel. Цей маршрут `/login` можна [реалізувати вручну](/docs/{{version}}/authentication#authenticating-users) або через headless-пакет автентифікації на кшталт [Laravel Fortify](/docs/{{version}}/fortify).

Якщо запит на вхід успішний, вас буде автентифіковано, і наступні запити до маршрутів вашого застосунку автоматично автентифікуватимуться через сесійний cookie, який застосунок Laravel видав вашому клієнту. До того ж, оскільки ваш застосунок уже звернувся до маршруту `/sanctum/csrf-cookie`, наступні запити мають автоматично отримувати захист від CSRF, доки ваш JavaScript HTTP-клієнт надсилає значення cookie `XSRF-TOKEN` у заголовку `X-XSRF-TOKEN`.

Звісно, якщо сесія користувача спливе через брак активності, наступні запити до застосунку Laravel можуть отримати HTTP-помилку 401 чи 419. У такому разі перенаправте користувача на сторінку входу вашого SPA.

Оскільки такий підхід до автентифікації SPA базується на сесіях, ви можете користуватися стандартними сервісами автентифікації Laravel, зокрема функціональністю [«запам'ятати мене»](/docs/{{version}}/authentication#remembering-users).

> [!WARNING]
> Ви вільні написати власний ендпоїнт `/login`; проте переконайтеся, що він автентифікує користувача через стандартні [сервіси сесійної автентифікації, які надає Laravel](/docs/{{version}}/authentication#authenticating-users). Зазвичай це означає використання гарда автентифікації `web`.

<a name="protecting-spa-routes"></a>
### Захист маршрутів

Щоб захистити маршрути так, аби всі вхідні запити мали бути автентифікованими, додайте гард автентифікації `sanctum` до ваших API-маршрутів у файлі `routes/api.php`. Цей гард гарантуватиме, що вхідні запити або автентифіковані як stateful-запити з вашого SPA, або містять заголовок із дійсним API-токеном, якщо запит надійшов від третьої сторони:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### Авторизація приватних каналів бродкастингу

Якщо вашому SPA треба автентифікуватися в [приватних каналах чи каналах присутності](/docs/{{version}}/broadcasting#authorizing-channels), приберіть запис `channels` з методу `withRouting` у файлі `bootstrap/app.php` вашого застосунку. Натомість викличте метод `withBroadcasting`, щоб указати правильне `middleware` для маршрутів бродкастингу вашого застосунку:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
```

Далі, щоб запити авторизації Pusher були успішними, вам треба передати власний `authorizer` для Pusher під час ініціалізації [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation). Це дозволить вашому застосунку налаштувати Pusher на використання екземпляра `axios`, [належно налаштованого для міждоменних запитів](#cors-and-cookies):

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a name="mobile-application-authentication"></a>
## Автентифікація мобільних застосунків

Ви також можете автентифікувати токенами Sanctum запити вашого мобільного застосунку до вашого API. Процес автентифікації запитів мобільного застосунку схожий на автентифікацію сторонніх API-запитів; проте є невеликі відмінності в тому, як ви видаватимете API-токени.

<a name="issuing-mobile-api-tokens"></a>
### Видача API-токенів

Для початку створіть маршрут, який приймає пошту / ім'я користувача, пароль та ім'я пристрою, а потім обмінює ці облікові дані на новий токен Sanctum. «Ім'я пристрою», передане цьому ендпоїнту, потрібне лише для інформації й може бути будь-яким. Загалом ім'я пристрою має бути таким, яке користувач упізнає, - наприклад, «Nuno's iPhone 17».

Зазвичай ви робитимете запит до цього ендпоїнта з екрана «входу» вашого мобільного застосунку. Ендпоїнт поверне API-токен відкритим текстом, який потім можна зберегти на мобільному пристрої й використовувати для наступних API-запитів:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

Коли мобільний застосунок робить із цим токеном API-запит до вашого застосунку, він має передавати токен у заголовку `Authorization` як токен `Bearer`.

> [!NOTE]
> Видаючи токени для мобільного застосунку, ви так само вільні вказати [можливості токенів](#token-abilities).

<a name="protecting-mobile-api-routes"></a>
### Захист маршрутів

Як уже описано раніше, ви можете захистити маршрути так, аби всі вхідні запити мали бути автентифікованими, додавши до них гард автентифікації `sanctum`:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### Відкликання токенів

Щоб дозволити користувачам відкликати API-токени, видані мобільним пристроям, ви можете вивести їх за іменами разом із кнопкою «Revoke» у розділі «налаштування облікового запису» інтерфейсу вашого вебзастосунку. Коли користувач натисне «Revoke», ви можете видалити токен із бази даних. Пам'ятайте: до API-токенів користувача можна дістатися через зв'язок `tokens`, який надає трейт `Laravel\Sanctum\HasApiTokens`:

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## Тестування

Під час тестування метод `Sanctum::actingAs` дозволяє автентифікувати користувача й указати, які можливості слід надати його токену:

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

Якщо ви хочете надати токену всі можливості, включіть `*` до списку можливостей, переданого методу `actingAs`:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
