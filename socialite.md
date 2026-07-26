---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Socialite

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Оновлення Socialite](#upgrading-socialite)
- [Конфігурація](#configuration)
- [Автентифікація](#authentication)
    - [Маршрутизація](#routing)
    - [Автентифікація та збереження](#authentication-and-storage)
    - [Скопи доступу](#access-scopes)
    - [Скопи ботів Slack](#slack-bot-scopes)
    - [Необов'язкові параметри](#optional-parameters)
- [Отримання даних користувача](#retrieving-user-details)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

Окрім звичайної автентифікації через форму, Laravel надає простий і зручний спосіб автентифікуватися через провайдери OAuth за допомогою [Laravel Socialite](https://github.com/laravel/socialite). Наразі Socialite підтримує автентифікацію через Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket і Slack.

> [!NOTE]
> Адаптери для інших платформ доступні на сайті [Socialite Providers](https://socialiteproviders.com/), який розвиває спільнота.

<a name="installation"></a>
## Встановлення

Щоб почати роботу із Socialite, додайте пакет до залежностей вашого проєкту через менеджер пакетів Composer:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Оновлення Socialite

Оновлюючись до нової мажорної версії Socialite, обов'язково уважно перегляньте [посібник з оновлення](https://github.com/laravel/socialite/blob/master/UPGRADE.md).

<a name="configuration"></a>
## Конфігурація

Перш ніж користуватися Socialite, вам треба додати облікові дані для провайдерів OAuth, які використовує ваш застосунок. Зазвичай ці облікові дані можна отримати, створивши «застосунок розробника» в панелі керування сервісу, через який ви автентифікуватиметеся.

Ці облікові дані слід розмістити в конфігураційному файлі `config/services.php` вашого застосунку під ключем `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack` чи `slack-openid` - залежно від того, які провайдери потрібні вашому застосунку:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> Якщо опція `redirect` містить відносний шлях, його буде автоматично перетворено на повний URL.

<a name="authentication"></a>
## Автентифікація

<a name="routing"></a>
### Маршрутизація

Щоб автентифікувати користувачів через провайдер OAuth, вам знадобляться два маршрути: один - для перенаправлення користувача до провайдера, другий - для отримання зворотного виклику від провайдера після автентифікації. Наведені нижче приклади демонструють реалізацію обох маршрутів:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

Метод `redirect`, який надає фасад `Socialite`, дбає про перенаправлення користувача до провайдера OAuth, а метод `user` перевіряє вхідний запит і отримує дані користувача від провайдера після того, як той схвалив запит на автентифікацію.

<a name="authentication-and-storage"></a>
### Автентифікація та збереження

Отримавши користувача від провайдера OAuth, ви можете визначити, чи існує він у базі даних вашого застосунку, і [автентифікувати його](/docs/{{version}}/authentication#authenticate-a-user-instance). Якщо користувача у вашій базі немає, зазвичай ви створюєте новий запис, що представлятиме його:

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::updateOrCreate([
        'github_id' => $githubUser->id,
    ], [
        'name' => $githubUser->name,
        'email' => $githubUser->email,
        'github_token' => $githubUser->token,
        'github_refresh_token' => $githubUser->refreshToken,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
});
```

> [!NOTE]
> Щоб дізнатися більше про те, які дані користувача доступні від конкретних провайдерів OAuth, зверніться до документації про [отримання даних користувача](#retrieving-user-details).

<a name="access-scopes"></a>
### Скопи доступу

Перед перенаправленням користувача ви можете скористатися методом `scopes`, щоб указати «скопи» (scopes), які слід включити до запиту на автентифікацію. Цей метод об'єднає всі раніше вказані скопи з тими, які ви задаєте:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

Ви можете перезаписати всі наявні скопи в запиті на автентифікацію методом `setScopes`:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Скопи ботів Slack

API Slack надає [різні типи токенів доступу](https://api.slack.com/authentication/token-types), кожен зі своїм набором [скопів дозволів](https://api.slack.com/scopes). Socialite сумісний з обома такими типами токенів доступу Slack:

<div class="content-list" markdown="1">

- Bot (з префіксом `xoxb-`)
- User (з префіксом `xoxp-`)

</div>

За замовчуванням драйвер `slack` генеруватиме токен `user`, а виклик методу `user` цього драйвера поверне дані користувача.

Токени ботів передусім корисні, якщо ваш застосунок надсилатиме сповіщення до зовнішніх робочих просторів Slack, що належать вашим користувачам. Щоб згенерувати токен бота, викличте метод `asBotUser`, перш ніж перенаправляти користувача до Slack для автентифікації:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

Крім того, ви маєте викликати метод `asBotUser` перед викликом методу `user` після того, як Slack поверне користувача до вашого застосунку:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

Під час генерування токена бота метод `user` усе одно поверне екземпляр `Laravel\Socialite\Two\User`; проте заповненою буде лише властивість `token`. Цей токен можна зберегти, щоб [надсилати сповіщення до робочих просторів Slack автентифікованого користувача](/docs/{{version}}/notifications#notifying-external-slack-workspaces).

<a name="optional-parameters"></a>
### Необов'язкові параметри

Низка провайдерів OAuth підтримує інші необов'язкові параметри в запиті на перенаправлення. Щоб додати такі параметри до запиту, викличте метод `with` з асоціативним масивом:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> Користуючись методом `with`, стежте, щоб не передати зарезервованих ключових слів на кшталт `state` чи `response_type`.

<a name="retrieving-user-details"></a>
## Отримання даних користувача

Після того як користувача перенаправлено назад на маршрут зворотного виклику вашого застосунку, ви можете отримати його дані методом `user` у Socialite. Об'єкт користувача, який повертає метод `user`, надає різні властивості й методи, якими ви можете скористатися, щоб зберегти інформацію про користувача у власній базі даних.

Набір доступних властивостей і методів цього об'єкта різниться залежно від того, чи підтримує провайдер OAuth, через який ви автентифікуєтеся, OAuth 1.0 чи OAuth 2.0:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 providers...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 providers...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All providers...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### Отримання даних користувача за токеном

Якщо ви вже маєте дійсний токен доступу користувача, ви можете отримати його дані методом `userFromToken` у Socialite:

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

Якщо ви користуєтеся Facebook Limited Login через застосунок для iOS, Facebook поверне токен OIDC замість токена доступу. Як і токен доступу, токен OIDC можна передати методу `userFromToken`, щоб отримати дані користувача.

<a name="stateless-authentication"></a>
#### Автентифікація без збереження стану

Метод `stateless` дозволяє вимкнути перевірку стану сесії. Це стає в пригоді, коли ви додаєте соціальну автентифікацію до stateless-API, який не використовує сесій на основі cookie:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
## Тестування

Laravel Socialite надає зручний спосіб тестувати потоки автентифікації OAuth, не роблячи справжніх запитів до провайдерів. Метод `fake` дозволяє підробити поведінку провайдера OAuth і задати дані користувача, які має бути повернено.

<a name="faking-the-redirect"></a>
#### Підроблення перенаправлення

Щоб перевірити, що ваш застосунок правильно перенаправляє користувачів до провайдера OAuth, викличте метод `fake` перед запитом до вашого маршруту перенаправлення. Тоді Socialite поверне перенаправлення на фіктивний URL авторизації замість справжнього провайдера OAuth:

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a name="faking-the-callback"></a>
#### Підроблення зворотного виклику

Щоб протестувати маршрут зворотного виклику вашого застосунку, викличте метод `fake` і передайте екземпляр `User`, який має бути повернено, коли застосунок запитає в провайдера дані користувача. Екземпляр `User` можна створити методом `fake`:

```php
use Laravel\Socialite\Socialite;
use Laravel\Socialite\Two\User;

test('user can login with github', function () {
    Socialite::fake('github', User::fake([
        'id' => 'github-123',
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
    ]));

    $response = $this->get('/auth/github/callback');

    $response->assertRedirect('/dashboard');

    $this->assertDatabaseHas('users', [
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
        'github_id' => 'github-123',
    ]);
});
```

За замовчуванням екземпляр `User` міститиме фіктивні значення токенів OAuth. За потреби ви можете перевизначити ці значення, передавши методу `fake` додаткові атрибути:

```php
$fakeUser = User::fake([
    'id' => 'github-123',
    'name' => 'Jason Beggs',
    'email' => 'jason@example.com',
    'token' => 'fake-token',
    'refreshToken' => 'fake-refresh-token',
    'expiresIn' => 3600,
    'approvedScopes' => ['read', 'write'],
]);
```

Користувачів OAuth 1 можна підробити через клас `Laravel\Socialite\One\User`.
