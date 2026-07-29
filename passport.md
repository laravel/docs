---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Passport

- [Вступ](#introduction)
    - [Passport чи Sanctum?](#passport-or-sanctum)
- [Встановлення](#installation)
    - [Розгортання Passport](#deploying-passport)
    - [Оновлення Passport](#upgrading-passport)
- [Конфігурація](#configuration)
    - [Час життя токенів](#token-lifetimes)
    - [Заміна моделей за замовчуванням](#overriding-default-models)
    - [Заміна маршрутів](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [Керування клієнтами](#managing-clients)
    - [Запит токенів](#requesting-tokens)
    - [Керування токенами](#managing-tokens)
    - [Оновлення токенів](#refreshing-tokens)
    - [Відкликання токенів](#revoking-tokens)
    - [Очищення токенів](#purging-tokens)
- [Authorization Code Grant з PKCE](#code-grant-pkce)
    - [Створення клієнта](#creating-a-auth-pkce-grant-client)
    - [Запит токенів](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Створення клієнта Device Code Grant](#creating-a-device-authorization-grant-client)
    - [Запит токенів](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Створення клієнта Password Grant](#creating-a-password-grant-client)
    - [Запит токенів](#requesting-password-grant-tokens)
    - [Запит усіх скопів](#requesting-all-scopes)
    - [Зміна провайдера користувачів](#customizing-the-user-provider)
    - [Зміна поля username](#customizing-the-username-field)
    - [Зміна валідації пароля](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Персональні токени доступу](#personal-access-tokens)
    - [Створення клієнта персонального доступу](#creating-a-personal-access-client)
    - [Зміна провайдера користувачів](#customizing-the-user-provider-for-pat)
    - [Керування персональними токенами доступу](#managing-personal-access-tokens)
- [Захист маршрутів](#protecting-routes)
    - [Через middleware](#via-middleware)
    - [Передавання токена доступу](#passing-the-access-token)
- [Скопи токенів](#token-scopes)
    - [Визначення скопів](#defining-scopes)
    - [Скоп за замовчуванням](#default-scope)
    - [Призначення скопів токенам](#assigning-scopes-to-tokens)
    - [Перевірка скопів](#checking-scopes)
- [Автентифікація SPA](#spa-authentication)
- [Події](#events)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

[Laravel Passport](https://github.com/laravel/passport) дає повну реалізацію сервера OAuth2 для вашого Laravel-застосунку за лічені хвилини. Passport побудований на [League OAuth2 server](https://github.com/thephpleague/oauth2-server), який підтримують Andy Millington і Simon Hamp.

> [!NOTE]
> Ця документація припускає, що ви вже знайомі з OAuth2. Якщо ви нічого не знаєте про OAuth2, перш ніж продовжувати, ознайомтеся із загальною [термінологією](https://oauth2.thephpleague.com/terminology/) та можливостями OAuth2.

<a name="passport-or-sanctum"></a>
### Passport чи Sanctum?

Перш ніж почати, вам, можливо, варто визначити, що краще підійде вашому застосунку: Laravel Passport чи [Laravel Sanctum](/docs/{{version}}/sanctum). Якщо вашому застосунку конче потрібна підтримка OAuth2, вам слід використовувати Laravel Passport.

Однак, якщо ви намагаєтеся автентифікувати односторінковий застосунок, мобільний застосунок або видавати API-токени, вам слід використовувати [Laravel Sanctum](/docs/{{version}}/sanctum). Laravel Sanctum не підтримує OAuth2; однак він дає значно простіший досвід розробки автентифікації API.

<a name="installation"></a>
## Встановлення

Встановити Laravel Passport можна артизан-командою `install:api`:

```shell
php artisan install:api --passport
```

Ця команда опублікує й виконає міграції бази даних, потрібні для створення таблиць, у яких ваш застосунок зберігатиме OAuth2-клієнтів і токени доступу. Команда також створить ключі шифрування, потрібні для генерації безпечних токенів доступу.

Після виконання команди `install:api` додайте трейт `Laravel\Passport\HasApiTokens` та інтерфейс `Laravel\Passport\Contracts\OAuthenticatable` до своєї моделі `App\Models\User`. Цей трейт надасть вашій моделі кілька хелпер-методів, які дозволяють оглядати токен і скопи автентифікованого користувача:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

Насамкінець у конфігураційному файлі `config/auth.php` вашого застосунку вам слід визначити гард автентифікації `api` і встановити опцію `driver` у `passport`. Це вкаже вашому застосунку використовувати `TokenGuard` з Passport під час автентифікації вхідних API-запитів:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```

<a name="deploying-passport"></a>
### Розгортання Passport

Розгортаючи Passport на сервери свого застосунку вперше, вам, найімовірніше, потрібно буде виконати команду `passport:keys`. Ця команда генерує ключі шифрування, потрібні Passport для генерації токенів доступу. Згенеровані ключі зазвичай не тримають під контролем версій:

```shell
php artisan passport:keys
```

За потреби ви можете визначити шлях, з якого слід завантажувати ключі Passport. Зробити це можна методом `Passport::loadKeysFrom`. Зазвичай цей метод слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### Завантаження ключів з оточення

Як альтернативу ви можете опублікувати конфігураційний файл Passport артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --tag=passport-config
```

Після публікації конфігураційного файлу ви можете завантажити ключі шифрування свого застосунку, визначивши їх як змінні оточення:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Оновлення Passport

Оновлюючись до нової мажорної версії Passport, важливо уважно переглянути [посібник з оновлення](https://github.com/laravel/passport/blob/master/UPGRADE.md).

<a name="configuration"></a>
## Конфігурація

<a name="token-lifetimes"></a>
### Час життя токенів

За замовчуванням Passport видає довгоживучі токени доступу, які спливають через рік. Якщо ви хочете налаштувати довший / коротший час життя токена, скористайтеся методами `tokensExpireIn`, `refreshTokensExpireIn` і `personalAccessTokensExpireIn`. Ці методи слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```

> [!WARNING]
> Колонки `expires_at` у таблицях бази даних Passport доступні лише для читання і призначені лише для показу. Видаючи токени, Passport зберігає інформацію про строк дії всередині підписаних і зашифрованих токенів. Якщо вам потрібно зробити токен недійсним, вам слід [відкликати його](#revoking-tokens).

<a name="overriding-default-models"></a>
### Заміна моделей за замовчуванням

Ви можете розширювати моделі, які Passport використовує внутрішньо, визначивши власну модель і розширивши відповідну модель Passport:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

Визначивши свою модель, ви можете вказати Passport використовувати вашу власну модель через клас `Laravel\Passport\Passport`. Зазвичай повідомляти Passport про ваші власні моделі слід у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```

<a name="overriding-routes"></a>
### Заміна маршрутів

Іноді ви можете захотіти змінити маршрути, визначені Passport. Щоб досягти цього, спершу вам потрібно проігнорувати маршрути, зареєстровані Passport, додавши `Passport::ignoreRoutes` до методу `register` `AppServiceProvider` вашого застосунку:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

Далі ви можете скопіювати маршрути, визначені Passport у [його файлі маршрутів](https://github.com/laravel/passport/blob/master/routes/web.php), до файлу `routes/web.php` свого застосунку і змінити їх на свій смак:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="authorization-code-grant"></a>
## Authorization Code Grant

Використання OAuth2 через коди авторизації - це те, з чим знайома більшість розробників. Коли використовуються коди авторизації, клієнтський застосунок перенаправляє користувача на ваш сервер, де той або схвалить, або відхилить запит на видачу токена доступу клієнту.

Для початку нам потрібно вказати Passport, як повертати наше «авторизаційне» представлення.

Усю логіку рендерингу авторизаційного представлення можна змінити відповідними методами, доступними через клас `Laravel\Passport\Passport`. Зазвичай цей метод слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::authorizationView('auth.oauth.authorize');

    // By providing a closure...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```

Passport автоматично визначить маршрут `/oauth/authorize`, який повертає це представлення. Ваш шаблон `auth.oauth.authorize` має містити форму, що робить POST-запит до маршруту `passport.authorizations.approve`, щоб схвалити авторизацію, і форму, що робить DELETE-запит до маршруту `passport.authorizations.deny`, щоб відхилити авторизацію. Маршрути `passport.authorizations.approve` і `passport.authorizations.deny` очікують поля `state`, `client_id` та `auth_token`.

<a name="managing-clients"></a>
### Керування клієнтами

Розробникам, які створюють застосунки, що мають взаємодіяти з API вашого застосунку, потрібно буде зареєструвати свій застосунок у вашому, створивши «клієнта». Зазвичай це полягає в наданні імені їхнього застосунку та URI, на який ваш застосунок може перенаправити після того, як користувачі схвалять їхній запит на авторизацію.

<a name="managing-first-party-clients"></a>
#### Власні клієнти

Найпростіший спосіб створити клієнта - артизан-команда `passport:client`. Цю команду можна використовувати для створення власних клієнтів або для тестування вашої функціональності OAuth2. Коли ви виконаєте команду `passport:client`, Passport запитає у вас більше інформації про вашого клієнта і надасть вам ID та секрет клієнта:

```shell
php artisan passport:client
```

Якщо ви хочете дозволити своєму клієнту кілька URI перенаправлення, вкажіть їх списком через кому, коли команда `passport:client` запитає URI. Будь-які URI, що містять коми, слід закодувати як URI:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### Сторонні клієнти

Оскільки користувачі вашого застосунку не зможуть скористатися командою `passport:client`, ви можете застосувати метод `createAuthorizationCodeGrantClient` класу `Laravel\Passport\ClientRepository`, щоб зареєструвати клієнта для заданого користувача:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// Creating an OAuth app client that belongs to the given user...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// Retrieving all the OAuth app clients that belong to the user...
$clients = $user->oauthApps()->get();
```

Метод `createAuthorizationCodeGrantClient` повертає екземпляр `Laravel\Passport\Client`. Ви можете показати користувачеві `$client->id` як ID клієнта і `$client->plainSecret` як секрет клієнта.

<a name="requesting-tokens"></a>
### Запит токенів

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### Перенаправлення для авторизації

Щойно клієнта створено, розробники можуть використовувати свій ID і секрет клієнта, щоб запитати код авторизації й токен доступу у вашого застосунку. Спершу застосунок-споживач має зробити запит на перенаправлення до маршруту `/oauth/authorize` вашого застосунку, ось так:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

Параметр `prompt` можна використати, щоб задати поведінку автентифікації застосунку Passport.

Якщо значення `prompt` - `none`, Passport завжди видаватиме помилку автентифікації, коли користувач ще не автентифікований у застосунку Passport. Якщо значення - `consent`, Passport завжди показуватиме екран схвалення авторизації, навіть якщо всі скопи вже раніше було надано застосунку-споживачу. Коли значення - `login`, застосунок Passport завжди пропонуватиме користувачеві повторно увійти до застосунку, навіть якщо той уже має наявну сесію.

Якщо значення `prompt` не надано, користувачеві буде запропоновано авторизацію лише тоді, коли він раніше не авторизував доступ застосунку-споживачу до запитаних скопів.

> [!NOTE]
> Пам'ятайте: маршрут `/oauth/authorize` уже визначено Passport. Вам не потрібно визначати цей маршрут вручну.

<a name="approving-the-request"></a>
#### Схвалення запиту

Отримуючи запити на авторизацію, Passport автоматично відповідатиме на основі значення параметра `prompt` (якщо він присутній) і може показати користувачеві шаблон, що дозволяє схвалити чи відхилити запит на авторизацію. Якщо користувач схвалить запит, його буде перенаправлено назад на `redirect_uri`, указаний застосунком-споживачем. `redirect_uri` має збігатися з URL `redirect`, указаним під час створення клієнта.

Іноді ви можете захотіти пропустити запит на авторизацію, наприклад авторизуючи власного клієнта. Досягти цього можна, [розширивши модель `Client`](#overriding-default-models) і визначивши метод `skipsAuthorization`. Якщо `skipsAuthorization` поверне `true`, клієнта буде схвалено, а користувача одразу перенаправлено назад на `redirect_uri` - хіба що застосунок-споживач явно встановив параметр `prompt` під час перенаправлення для авторизації:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### Обмін кодів авторизації на токени доступу

Якщо користувач схвалить запит на авторизацію, його буде перенаправлено назад до застосунку-споживача. Споживач має спершу звірити параметр `state` зі значенням, збереженим перед перенаправленням. Якщо параметр state збігається, споживач має надіслати `POST`-запит до вашого застосунку, щоб запитати токен доступу. Запит має містити код авторизації, виданий вашим застосунком, коли користувач схвалив запит на авторизацію:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

Цей маршрут `/oauth/token` поверне JSON-відповідь з атрибутами `access_token`, `refresh_token` та `expires_in`. Атрибут `expires_in` містить кількість секунд до спливання токена доступу.

> [!NOTE]
> Як і маршрут `/oauth/authorize`, маршрут `/oauth/token` визначено за вас у Passport. Визначати цей маршрут вручну не потрібно.

<a name="managing-tokens"></a>
### Керування токенами

Ви можете отримати авторизовані токени користувача методом `tokens` трейта `Laravel\Passport\HasApiTokens`. Наприклад, це можна використати, щоб запропонувати вашим користувачам панель для відстеження їхніх з'єднань зі сторонніми застосунками:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Retrieving all of the valid tokens for the user...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// Retrieving all the user's connections to third-party OAuth app clients...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```

<a name="refreshing-tokens"></a>
### Оновлення токенів

Якщо ваш застосунок видає короткоживучі токени доступу, користувачам потрібно буде оновлювати свої токени доступу через refresh-токен, наданий їм під час видачі токена доступу:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

Цей маршрут `/oauth/token` поверне JSON-відповідь з атрибутами `access_token`, `refresh_token` та `expires_in`. Атрибут `expires_in` містить кількість секунд до спливання токена доступу.

<a name="revoking-tokens"></a>
### Відкликання токенів

Ви можете відкликати токен методом `revoke` на моделі `Laravel\Passport\Token`. Відкликати refresh-токен токена можна методом `revoke` на моделі `Laravel\Passport\RefreshToken`:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Revoke an access token...
$token->revoke();

// Revoke the token's refresh token...
$token->refreshToken?->revoke();

// Revoke all of the user's tokens...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### Очищення токенів

Коли токени відкликано або вони сплили, ви можете захотіти прибрати їх з бази даних. Артизан-команда `passport:purge`, що входить до Passport, може зробити це за вас:

```shell
# Purge revoked and expired tokens, auth codes, and device codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens, auth codes, and device codes...
php artisan passport:purge --revoked

# Only purge expired tokens, auth codes, and device codes...
php artisan passport:purge --expired
```

Ви також можете налаштувати [заплановане завдання](/docs/{{version}}/scheduling) у файлі `routes/console.php` свого застосунку, щоб автоматично прибирати токени за розкладом:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## Authorization Code Grant з PKCE

Authorization Code grant з «Proof Key for Code Exchange» (PKCE) - це безпечний спосіб автентифікувати односторінкові чи мобільні застосунки для доступу до вашого API. Цей grant слід використовувати, коли ви не можете гарантувати, що секрет клієнта зберігатиметься конфіденційно, або щоб зменшити ризик перехоплення коду авторизації зловмисником. Комбінація «code verifier» і «code challenge» замінює секрет клієнта під час обміну коду авторизації на токен доступу.

<a name="creating-a-auth-pkce-grant-client"></a>
### Створення клієнта

Перш ніж ваш застосунок зможе видавати токени через authorization code grant з PKCE, вам потрібно створити клієнта з увімкненим PKCE. Зробити це можна артизан-командою `passport:client` з опцією `--public`:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### Запит токенів

<a name="code-verifier-code-challenge"></a>
#### Code Verifier і Code Challenge

Оскільки цей grant авторизації не передбачає секрету клієнта, розробникам потрібно буде згенерувати комбінацію code verifier і code challenge, щоб запитати токен.

Code verifier має бути випадковим рядком довжиною від 43 до 128 символів, що містить літери, цифри та символи `"-"`, `"."`, `"_"`, `"~"`, як визначено в [специфікації RFC 7636](https://tools.ietf.org/html/rfc7636).

Code challenge має бути рядком у кодуванні Base64 із символами, безпечними для URL та імен файлів. Кінцеві символи `'='` слід прибрати, і в ньому не має бути переносів рядків, пробілів чи інших додаткових символів.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### Перенаправлення для авторизації

Щойно клієнта створено, ви можете використати ID клієнта та згенеровані code verifier і code challenge, щоб запитати код авторизації й токен доступу у вашого застосунку. Спершу застосунок-споживач має зробити запит на перенаправлення до маршруту `/oauth/authorize` вашого застосунку:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### Обмін кодів авторизації на токени доступу

Якщо користувач схвалить запит на авторизацію, його буде перенаправлено назад до застосунку-споживача. Споживач має звірити параметр `state` зі значенням, збереженим перед перенаправленням, як і у стандартному Authorization Code Grant.

Якщо параметр state збігається, споживач має надіслати `POST`-запит до вашого застосунку, щоб запитати токен доступу. Запит має містити код авторизації, виданий вашим застосунком, коли користувач схвалив запит на авторизацію, разом із початково згенерованим code verifier:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="device-authorization-grant"></a>
## Device Authorization Grant

Device authorization grant в OAuth2 дозволяє пристроям без браузера чи з обмеженим введенням, як-от телевізорам та ігровим консолям, отримати токен доступу, обмінявши «device code». Використовуючи device flow, клієнт на пристрої вкаже користувачеві скористатися другим пристроєм, наприклад комп'ютером чи смартфоном, і підключитися до вашого сервера, де той введе наданий «user code» і схвалить або відхилить запит на доступ.

Для початку нам потрібно вказати Passport, як повертати наші представлення «user code» та «авторизація».

Усю логіку рендерингу авторизаційного представлення можна змінити відповідними методами, доступними через клас `Laravel\Passport\Passport`. Зазвичай цей метод слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // By providing a closure...
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```

Passport автоматично визначить маршрути, які повертають ці представлення. Ваш шаблон `auth.oauth.device.user-code` має містити форму, що робить GET-запит до маршруту `passport.device.authorizations.authorize`. Маршрут `passport.device.authorizations.authorize` очікує параметр рядка запиту `user_code`.

Ваш шаблон `auth.oauth.device.authorize` має містити форму, що робить POST-запит до маршруту `passport.device.authorizations.approve`, щоб схвалити авторизацію, і форму, що робить DELETE-запит до маршруту `passport.device.authorizations.deny`, щоб відхилити авторизацію. Маршрути `passport.device.authorizations.approve` і `passport.device.authorizations.deny` очікують поля `state`, `client_id` та `auth_token`.

<a name="creating-a-device-authorization-grant-client"></a>
### Створення клієнта Device Authorization Grant

Перш ніж ваш застосунок зможе видавати токени через device authorization grant, вам потрібно створити клієнта з увімкненим device flow. Зробити це можна артизан-командою `passport:client` з опцією `--device`. Ця команда створить власного клієнта з увімкненим device flow і надасть вам ID та секрет клієнта:

```shell
php artisan passport:client --device
```

Крім того, ви можете скористатися методом `createDeviceAuthorizationGrantClient` класу `ClientRepository`, щоб зареєструвати стороннього клієнта, що належить заданому користувачеві:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```

<a name="requesting-device-authorization-grant-tokens"></a>
### Запит токенів

<a name="device-code"></a>
#### Запит device code

Щойно клієнта створено, розробники можуть використовувати свій ID клієнта, щоб запитати device code у вашого застосунку. Спершу пристрій-споживач має зробити `POST`-запит до маршруту `/oauth/device/code` вашого застосунку, щоб запитати device code:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

Це поверне JSON-відповідь з атрибутами `device_code`, `user_code`, `verification_uri`, `interval` та `expires_in`. Атрибут `expires_in` містить кількість секунд до спливання device code. Атрибут `interval` містить кількість секунд, які пристрій-споживач має чекати між запитами, опитуючи маршрут `/oauth/token`, щоб уникнути помилок обмеження частоти.

> [!NOTE]
> Пам'ятайте: маршрут `/oauth/device/code` уже визначено Passport. Вам не потрібно визначати цей маршрут вручну.

<a name="user-code"></a>
#### Показ verification URI та user code

Щойно запит на device code виконано, пристрій-споживач має вказати користувачеві скористатися іншим пристроєм, відвідати наданий `verification_uri` і ввести `user_code`, щоб схвалити запит на авторизацію.

<a name="polling-token-request"></a>
#### Запит токена опитуванням

Оскільки користувач надаватиме (чи відхилятиме) доступ з окремого пристрою, пристрій-споживач має опитувати маршрут `/oauth/token` вашого застосунку, щоб визначити, коли користувач відповів на запит. Пристрій-споживач має використовувати мінімальний інтервал опитування `interval`, наданий у JSON-відповіді під час запиту device code, щоб уникнути помилок обмеження частоти:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

Якщо користувач схвалив запит на авторизацію, це поверне JSON-відповідь з атрибутами `access_token`, `refresh_token` та `expires_in`. Атрибут `expires_in` містить кількість секунд до спливання токена доступу.

<a name="password-grant"></a>
## Password Grant

> [!WARNING]
> Ми більше не рекомендуємо використовувати токени password grant. Натомість вам слід обрати [тип grant, який наразі рекомендує OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

Password grant в OAuth2 дозволяє іншим вашим власним клієнтам, наприклад мобільному застосунку, отримати токен доступу за адресою електронної пошти / іменем користувача й паролем. Це дозволяє безпечно видавати токени доступу вашим власним клієнтам, не змушуючи користувачів проходити весь потік перенаправлень з кодом авторизації OAuth2.

Щоб увімкнути password grant, викличте метод `enablePasswordGrant` у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
### Створення клієнта Password Grant

Перш ніж ваш застосунок зможе видавати токени через password grant, вам потрібно створити клієнта password grant. Зробити це можна артизан-командою `passport:client` з опцією `--password`.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### Запит токенів

Щойно ви увімкнули grant і створили клієнта password grant, ви можете запитати токен доступу, надіславши `POST`-запит до маршруту `/oauth/token` з адресою електронної пошти й паролем користувача. Пам'ятайте: цей маршрут уже зареєстровано Passport, тож визначати його вручну не потрібно. Якщо запит буде успішним, ви отримаєте `access_token` і `refresh_token` у JSON-відповіді від сервера:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> Пам'ятайте: за замовчуванням токени доступу довгоживучі. Однак за потреби ви можете [налаштувати максимальний час життя токена доступу](#configuration).

<a name="requesting-all-scopes"></a>
### Запит усіх скопів

Використовуючи password grant чи client credentials grant, ви можете захотіти авторизувати токен для всіх скопів, які підтримує ваш застосунок. Зробити це можна, запитавши скоп `*`. Якщо ви запитаєте скоп `*`, метод `can` на екземплярі токена завжди повертатиме `true`. Цей скоп можна призначити лише токену, виданому через grant `password` чи `client_credentials`:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### Зміна провайдера користувачів

Якщо ваш застосунок використовує більше одного [провайдера користувачів для автентифікації](/docs/{{version}}/authentication#introduction), ви можете вказати, який провайдер користувачів використовує клієнт password grant, передавши опцію `--provider` під час створення клієнта командою `artisan passport:client --password`. Задане ім'я провайдера має відповідати дійсному провайдеру, визначеному в конфігураційному файлі `config/auth.php` вашого застосунку. Далі ви можете [захистити свій маршрут за допомогою middleware](#multiple-authentication-guards), щоб авторизованими були лише користувачі з указаного провайдера гарда.

<a name="customizing-the-username-field"></a>
### Зміна поля username

Автентифікуючись через password grant, Passport використовуватиме атрибут `email` вашої автентифіковної моделі як «username». Однак ви можете змінити цю поведінку, визначивши на своїй моделі метод `findForPassport`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Bridge\Client;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### Зміна валідації пароля

Автентифікуючись через password grant, Passport використовуватиме атрибут `password` вашої моделі для перевірки наданого пароля. Якщо ваша модель не має атрибута `password` або ви хочете змінити логіку валідації пароля, визначте на своїй моделі метод `validateForPassportPasswordGrant`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## Implicit Grant

> [!WARNING]
> Ми більше не рекомендуємо використовувати токени implicit grant. Натомість вам слід обрати [тип grant, який наразі рекомендує OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

Implicit grant схожий на authorization code grant; однак токен повертається клієнту без обміну коду авторизації. Цей grant найчастіше використовують для JavaScript- чи мобільних застосунків, де облікові дані клієнта не можна зберігати безпечно. Щоб увімкнути цей grant, викличте метод `enableImplicitGrant` у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

Перш ніж ваш застосунок зможе видавати токени через implicit grant, вам потрібно створити клієнта implicit grant. Зробити це можна артизан-командою `passport:client` з опцією `--implicit`.

```shell
php artisan passport:client --implicit
```

Щойно grant увімкнено, а implicit-клієнта створено, розробники можуть використовувати свій ID клієнта, щоб запитати токен доступу у вашого застосунку. Застосунок-споживач має зробити запит на перенаправлення до маршруту `/oauth/authorize` вашого застосунку, ось так:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> Пам'ятайте: маршрут `/oauth/authorize` уже визначено Passport. Вам не потрібно визначати цей маршрут вручну.

<a name="client-credentials-grant"></a>
## Client Credentials Grant

Client credentials grant підходить для автентифікації між машинами. Наприклад, ви можете використати цей grant у запланованому завданні, яке виконує обслуговування через API.

Перш ніж ваш застосунок зможе видавати токени через client credentials grant, вам потрібно створити клієнта client credentials grant. Зробити це можна опцією `--client` артизан-команди `passport:client`:

```shell
php artisan passport:client --client
```

Далі призначте маршруту `middleware` `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner`:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

Щоб обмежити доступ до маршруту конкретними скопами, передайте список потрібних скопів до методу `using`:

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

> [!WARNING]
> [Сервер OAuth2, що лежить в основі](https://oauth2.thephpleague.com/database-setup/#:~:text=Please%20note%20that,the%20bearer%20token.), встановлює claim `sub` токена в ідентифікатор клієнта для токенів client credentials. За замовчуванням Passport використовує UUID для клієнтів, тож це не може конфліктувати з цілочисловим первинним ключем користувача. Однак, якщо ви встановили `Passport::$clientUuids` у `false`, токен client credentials може ненавмисно знайти користувача, чий ID збігається з ID клієнта. У таких випадках цей `middleware` не може гарантувати, що вхідний токен є токеном client credentials.

<a name="retrieving-tokens"></a>
### Отримання токенів

Щоб отримати токен за допомогою цього типу grant, зробіть запит до ендпоїнта `oauth/token`:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## Персональні токени доступу

Іноді ваші користувачі можуть захотіти видати токени доступу самим собі, не проходячи звичний потік перенаправлень з кодом авторизації. Дозвіл користувачам видавати собі токени через UI вашого застосунку може бути корисним, щоб вони могли поекспериментувати з вашим API, або ж бути простішим підходом до видачі токенів доступу загалом.

> [!NOTE]
> Якщо ваш застосунок використовує Passport переважно для видачі персональних токенів доступу, розгляньте [Laravel Sanctum](/docs/{{version}}/sanctum) - легку власну бібліотеку Laravel для видачі API-токенів доступу.

<a name="creating-a-personal-access-client"></a>
### Створення клієнта персонального доступу

Перш ніж ваш застосунок зможе видавати персональні токени доступу, вам потрібно створити клієнта персонального доступу. Зробити це можна, виконавши артизан-команду `passport:client` з опцією `--personal`. Якщо ви вже виконували команду `passport:install`, виконувати цю команду не потрібно:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### Зміна провайдера користувачів

Якщо ваш застосунок використовує більше одного [провайдера користувачів для автентифікації](/docs/{{version}}/authentication#introduction), ви можете вказати, який провайдер користувачів використовує клієнт personal access grant, передавши опцію `--provider` під час створення клієнта командою `artisan passport:client --personal`. Задане ім'я провайдера має відповідати дійсному провайдеру, визначеному в конфігураційному файлі `config/auth.php` вашого застосунку. Далі ви можете [захистити свій маршрут за допомогою middleware](#multiple-authentication-guards), щоб авторизованими були лише користувачі з указаного провайдера гарда.

<a name="managing-personal-access-tokens"></a>
### Керування персональними токенами доступу

Щойно ви створили клієнта персонального доступу, ви можете видавати токени для заданого користувача методом `createToken` на екземплярі моделі `App\Models\User`. Метод `createToken` приймає ім'я токена як перший аргумент і необов'язковий масив [скопів](#token-scopes) як другий:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Creating a token without scopes...
$token = $user->createToken('My Token')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// Creating a token with all scopes...
$token = $user->createToken('My Token', ['*'])->accessToken;

// Retrieving all the valid personal access tokens that belong to the user...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## Захист маршрутів

<a name="via-middleware"></a>
### Через middleware

Passport містить [гард автентифікації](/docs/{{version}}/authentication#adding-custom-guards), який перевірятиме токени доступу у вхідних запитах. Щойно ви налаштували гард `api` на використання драйвера `passport`, вам достатньо вказати `middleware` `auth:api` на будь-яких маршрутах, що мають вимагати дійсний токен доступу:

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```

> [!WARNING]
> Якщо ви використовуєте [client credentials grant](#client-credentials-grant), для захисту своїх маршрутів вам слід використовувати [`middleware` `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner`](#client-credentials-grant), а не `middleware` `auth:api`.

<a name="multiple-authentication-guards"></a>
#### Кілька гардів автентифікації

Якщо ваш застосунок автентифікує різні типи користувачів, які, можливо, використовують цілком різні Eloquent-моделі, вам, найімовірніше, потрібно буде визначити конфігурацію гарда для кожного типу провайдера користувачів у своєму застосунку. Це дозволяє захищати запити, призначені для конкретних провайдерів користувачів. Наприклад, за такої конфігурації гардів у конфігураційному файлі `config/auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```

Наведений нижче маршрут використовуватиме гард `api-customers`, який використовує провайдер користувачів `customers`, для автентифікації вхідних запитів:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Докладніше про використання кількох провайдерів користувачів з Passport дивіться в [документації щодо персональних токенів доступу](#customizing-the-user-provider-for-pat) і [документації щодо password grant](#customizing-the-user-provider).

<a name="passing-the-access-token"></a>
### Передавання токена доступу

Викликаючи маршрути, захищені Passport, споживачі API вашого застосунку мають указувати свій токен доступу як `Bearer`-токен у заголовку `Authorization` свого запиту. Наприклад, використовуючи фасад `Http`:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## Скопи токенів

Скопи дозволяють вашим API-клієнтам запитувати конкретний набір дозволів, коли вони запитують авторизацію для доступу до облікового запису. Наприклад, якщо ви створюєте застосунок електронної комерції, не всім споживачам API знадобиться можливість оформлювати замовлення. Натомість ви можете дозволити споживачам запитувати авторизацію лише на доступ до статусів відправлення замовлень. Іншими словами, скопи дозволяють користувачам вашого застосунку обмежувати дії, які сторонній застосунок може виконувати від їхнього імені.

<a name="defining-scopes"></a>
### Визначення скопів

Ви можете визначити скопи свого API методом `Passport::tokensCan` у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку. Метод `tokensCan` приймає масив імен скопів та їхніх описів. Опис скопу може бути будь-яким, і його буде показано користувачам на екрані схвалення авторизації:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### Скоп за замовчуванням

Якщо клієнт не запитує жодних конкретних скопів, ви можете налаштувати свій сервер Passport додавати до токена скопи за замовчуванням методом `defaultScopes`. Зазвичай цей метод слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### Призначення скопів токенам

<a name="when-requesting-authorization-codes"></a>
#### Під час запиту кодів авторизації

Запитуючи токен доступу через authorization code grant, споживачі мають указати бажані скопи як параметр рядка запиту `scope`. Параметр `scope` має бути списком скопів, розділених пробілами:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
#### Під час видачі персональних токенів доступу

Якщо ви видаєте персональні токени доступу методом `createToken` моделі `App\Models\User`, ви можете передати масив бажаних скопів другим аргументом методу:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### Перевірка скопів

Passport містить два `middleware`, якими можна перевірити, що вхідний запит автентифіковано токеном, якому надано певний скоп.

<a name="check-for-all-scopes"></a>
#### Перевірка всіх скопів

`middleware` `Laravel\Passport\Http\Middleware\CheckToken` можна призначити маршруту, щоб перевірити, що токен доступу вхідного запиту має всі перелічені скопи:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### Перевірка будь-якого зі скопів

`middleware` `Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` можна призначити маршруту, щоб перевірити, що токен доступу вхідного запиту має *принаймні один* з перелічених скопів:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="scope-attributes"></a>
#### Атрибути скопів

Якщо ваш застосунок використовує [атрибути middleware контролерів](/docs/{{version}}/controllers#middleware-attributes), ви можете скористатися атрибутом `Laravel\Passport\Attributes\AuthorizeToken` як зручним скороченням для `middleware` скопів у Passport:

```php
<?php

namespace App\Http\Controllers;

use Laravel\Passport\Attributes\AuthorizeToken;

#[AuthorizeToken('orders:read')]
#[AuthorizeToken('orders:create', only: ['store'])]
class OrderController
{
    #[AuthorizeToken(['orders:read', 'orders:create'], anyScope: true)]
    public function index()
    {
        // Access token has either "orders:read" or "orders:create" scope...
    }

    public function store()
    {
        // Access token has both "orders:read" and "orders:create" scopes...
    }
}
```

За замовчуванням атрибут `AuthorizeToken` вимагає всі задані скопи. Якщо ви передасте `anyScope: true`, запит буде авторизовано, коли токен має принаймні один із заданих скопів.

<a name="checking-scopes-on-a-token-instance"></a>
#### Перевірка скопів на екземплярі токена

Щойно запит, автентифікований токеном доступу, потрапив до вашого застосунку, ви все ще можете перевірити, чи має токен певний скоп, методом `tokenCan` на автентифікованому екземплярі `App\Models\User`:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### Додаткові методи для скопів

Метод `scopeIds` поверне масив усіх визначених ID / імен:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

Метод `scopes` поверне масив усіх визначених скопів як екземплярів `Laravel\Passport\Scope`:

```php
Passport::scopes();
```

Метод `scopesFor` поверне масив екземплярів `Laravel\Passport\Scope`, що відповідають заданим ID / іменам:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

Ви можете визначити, чи задано певний скоп, методом `hasScope`:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## Автентифікація SPA

Створюючи API, буває надзвичайно корисно мати змогу споживати власний API зі свого JavaScript-застосунку. Такий підхід до розробки API дозволяє вашому власному застосунку споживати той самий API, яким ви ділитеся зі світом. Той самий API можуть споживати ваш вебзастосунок, мобільні застосунки, сторонні застосунки та будь-які SDK, які ви можете публікувати в різних менеджерах пакетів.

Зазвичай, якщо ви хочете споживати свій API зі свого JavaScript-застосунку, вам потрібно було б вручну надсилати токен доступу застосунку й передавати його з кожним запитом до вашого застосунку. Однак Passport містить `middleware`, який може впоратися з цим за вас. Усе, що вам потрібно зробити, - додати `middleware` `CreateFreshApiToken` до групи `middleware` `web` у файлі `bootstrap/app.php` вашого застосунку:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> Переконайтеся, що `middleware` `CreateFreshApiToken` є останнім `middleware` у вашому стеку `middleware`.

Цей `middleware` додасть до ваших вихідних відповідей cookie `laravel_token`. Цей cookie містить зашифрований JWT, який Passport використовуватиме для автентифікації API-запитів з вашого JavaScript-застосунку. Час життя JWT дорівнює значенню вашої конфігурації `session.lifetime`. Тепер, оскільки браузер автоматично надсилатиме цей cookie з усіма наступними запитами, ви можете робити запити до API свого застосунку, не передаючи токен доступу явно:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### Зміна імені cookie

За потреби ви можете змінити ім'я cookie `laravel_token` методом `Passport::cookie`. Зазвичай цей метод слід викликати з методу `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### Захист від CSRF

Використовуючи цей спосіб автентифікації, вам потрібно буде подбати, щоб до ваших запитів було включено дійсний заголовок з CSRF-токеном. Стандартний JavaScript-каркас Laravel, що входить до скелета застосунку й усіх стартових наборів, містить екземпляр [Axios](https://github.com/axios/axios), який автоматично використовуватиме зашифроване значення cookie `XSRF-TOKEN`, щоб надсилати заголовок `X-XSRF-TOKEN` у запитах з того самого джерела.

> [!NOTE]
> Якщо ви вирішите надсилати заголовок `X-CSRF-TOKEN` замість `X-XSRF-TOKEN`, вам потрібно буде використовувати незашифрований токен, який надає `csrf_token()`.

<a name="events"></a>
## Події

Passport здіймає події під час видачі токенів доступу й refresh-токенів. Ви можете [слухати ці події](/docs/{{version}}/events), щоб прибирати чи відкликати інші токени доступу у своїй базі даних:

<div class="overflow-auto">

| Event Name                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## Тестування

Метод `actingAs` у Passport можна використати, щоб указати поточного автентифікованого користувача, а також його скопи. Перший аргумент методу `actingAs` - екземпляр користувача, а другий - масив скопів, які слід надати токену користувача:

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```

Метод `actingAsClient` у Passport можна використати, щоб указати поточного автентифікованого клієнта, а також його скопи. Перший аргумент методу `actingAsClient` - екземпляр клієнта, а другий - масив скопів, які слід надати токену клієнта:

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```
