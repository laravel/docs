---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Fortify

- [Вступ](#introduction)
    - [Що таке Fortify?](#what-is-fortify)
    - [Коли варто використовувати Fortify?](#when-should-i-use-fortify)
- [Встановлення](#installation)
    - [Можливості Fortify](#fortify-features)
    - [Вимкнення представлень](#disabling-views)
- [Автентифікація](#authentication)
    - [Налаштування автентифікації користувачів](#customizing-user-authentication)
    - [Налаштування конвеєра автентифікації](#customizing-the-authentication-pipeline)
    - [Налаштування перенаправлень](#customizing-authentication-redirects)
- [Двофакторна автентифікація](#two-factor-authentication)
    - [Увімкнення двофакторної автентифікації](#enabling-two-factor-authentication)
    - [Автентифікація з двофакторною автентифікацією](#authenticating-with-two-factor-authentication)
    - [Вимкнення двофакторної автентифікації](#disabling-two-factor-authentication)
- [Passkeys](#passkeys)
    - [Увімкнення passkeys](#enabling-passkeys)
    - [JavaScript-клієнт](#passkeys-javascript-client)
    - [Автентифікація через passkeys](#authenticating-with-passkeys)
    - [Підтвердження пароля через passkeys](#confirming-password-with-passkeys)
    - [Реєстрація passkeys](#registering-passkeys)
    - [Видалення passkeys](#deleting-passkeys)
- [Реєстрація](#registration)
    - [Налаштування реєстрації](#customizing-registration)
- [Скидання пароля](#password-reset)
    - [Запит посилання для скидання пароля](#requesting-a-password-reset-link)
    - [Скидання пароля](#resetting-the-password)
    - [Налаштування скидання паролів](#customizing-password-resets)
- [Підтвердження електронної пошти](#email-verification)
    - [Захист маршрутів](#protecting-routes)
- [Підтвердження пароля](#password-confirmation)

<a name="introduction"></a>
## Вступ

[Laravel Fortify](https://github.com/laravel/fortify) - це незалежна від фронтенду реалізація бекенду автентифікації для Laravel. Fortify реєструє маршрути й контролери, потрібні для всіх можливостей автентифікації Laravel, - зокрема входу, реєстрації, скидання пароля, підтвердження пошти тощо. Після встановлення Fortify ви можете виконати артизан-команду `route:list`, щоб побачити зареєстровані ним маршрути.

Оскільки Fortify не має власного інтерфейсу користувача, він призначений для роботи з вашим власним інтерфейсом, який робить запити до зареєстрованих ним маршрутів. Далі в цій документації ми детально розберемо, як саме робити запити до цих маршрутів.

> [!NOTE]
> Пам'ятайте: Fortify - пакет, покликаний дати вам фору в реалізації можливостей автентифікації Laravel. **Користуватися ним не обов'язково.** Ви завжди вільні працювати із сервісами автентифікації Laravel вручну, дотримуючись документації з [автентифікації](/docs/{{version}}/authentication), [скидання пароля](/docs/{{version}}/passwords) та [підтвердження пошти](/docs/{{version}}/verification).

<a name="what-is-fortify"></a>
### Що таке Fortify?

Як згадувалося раніше, Laravel Fortify - це незалежна від фронтенду реалізація бекенду автентифікації для Laravel. Fortify реєструє маршрути й контролери, потрібні для всіх можливостей автентифікації Laravel, - зокрема входу, реєстрації, скидання пароля, підтвердження пошти тощо.

**Щоб користуватися можливостями автентифікації Laravel, Fortify не потрібен.** Ви завжди вільні працювати із сервісами автентифікації Laravel вручну, дотримуючись документації з [автентифікації](/docs/{{version}}/authentication), [скидання пароля](/docs/{{version}}/passwords) та [підтвердження пошти](/docs/{{version}}/verification).

Якщо ви новачок у Laravel, вам, можливо, варто дослідити [наші стартові набори застосунку](/docs/{{version}}/starter-kits). Стартові набори Laravel використовують Fortify всередині, щоб дати каркас автентифікації з інтерфейсом на [Tailwind CSS](https://tailwindcss.com). Це дозволяє вивчити можливості автентифікації Laravel і освоїтися з ними.

По суті, Laravel Fortify бере маршрути й контролери з наших стартових наборів і пропонує їх як пакет без інтерфейсу користувача. Тож ви можете швидко створити бекенд-реалізацію шару автентифікації свого застосунку, не прив'язуючись до жодних поглядів на фронтенд.

<a name="when-should-i-use-fortify"></a>
### Коли варто використовувати Fortify?

Ви можете замислитися, коли саме доречно брати Laravel Fortify. По-перше, якщо ви користуєтеся одним зі [стартових наборів застосунку](/docs/{{version}}/starter-kits) Laravel, встановлювати Laravel Fortify не потрібно: усі стартові набори Laravel використовують Fortify і вже дають повну реалізацію автентифікації.

Якщо ви не користуєтеся стартовим набором, а вашому застосунку потрібні можливості автентифікації, у вас є два варіанти: реалізувати їх вручну або скористатися Laravel Fortify як бекенд-реалізацією.

Якщо ви оберете Fortify, ваш інтерфейс робитиме запити до маршрутів автентифікації Fortify, описаних у цій документації, щоб автентифікувати й реєструвати користувачів.

Якщо ж ви вирішите працювати із сервісами автентифікації Laravel вручну, а не через Fortify, дотримуйтеся документації з [автентифікації](/docs/{{version}}/authentication), [скидання пароля](/docs/{{version}}/passwords) та [підтвердження пошти](/docs/{{version}}/verification).

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify і Laravel Sanctum

Деякі розробники плутаються в різниці між [Laravel Sanctum](/docs/{{version}}/sanctum) і Laravel Fortify. Оскільки ці два пакети розв'язують різні, хоч і пов'язані задачі, Laravel Fortify та Laravel Sanctum не є взаємовиключними чи конкурентними.

Laravel Sanctum опікується лише керуванням API-токенами та автентифікацією наявних користувачів через сесійні cookie чи токени. Sanctum не надає маршрутів, що обробляють реєстрацію користувачів, скидання пароля тощо.

Якщо ви намагаєтеся вручну побудувати шар автентифікації для застосунку, який пропонує API чи слугує бекендом для односторінкового застосунку, цілком імовірно, що ви використаєте і Laravel Fortify (для реєстрації, скидання пароля тощо), і Laravel Sanctum (керування API-токенами, сесійна автентифікація).

<a name="installation"></a>
## Встановлення

Для початку встановіть Fortify через менеджер пакетів Composer:

```shell
composer require laravel/fortify
```

Далі опублікуйте ресурси Fortify артизан-командою `fortify:install`:

```shell
php artisan fortify:install
```

Ця команда опублікує дії Fortify до вашого каталогу `app/Actions`, який буде створено, якщо його немає. Крім того, буде опубліковано `FortifyServiceProvider`, конфігураційний файл і всі потрібні міграції бази даних.

Далі виконайте міграції:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Можливості Fortify

Конфігураційний файл `fortify` містить масив конфігурації `features`. Цей масив визначає, які бекенд-маршрути й можливості Fortify відкриватиме за замовчуванням. Ми радимо вмикати лише такі можливості - базові для більшості застосунків Laravel:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### Вимкнення представлень

За замовчуванням Fortify визначає маршрути, які повертають представлення, - як-от екран входу чи реєстрації. Проте якщо ви будуєте односторінковий застосунок на JavaScript, ці маршрути вам можуть бути не потрібні. Тому ви можете вимкнути їх цілком, встановивши значення конфігурації `views` у файлі `config/fortify.php` вашого застосунку в `false`:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### Вимкнення представлень і скидання пароля

Якщо ви вимкнете представлення Fortify, але реалізовуватимете скидання пароля у своєму застосунку, вам усе одно слід визначити маршрут з іменем `password.reset`, що відповідає за показ представлення «reset password». Це потрібно, бо сповіщення Laravel `Illuminate\Auth\Notifications\ResetPassword` генеруватиме URL скидання пароля саме через іменований маршрут `password.reset`.

<a name="authentication"></a>
## Автентифікація

Для початку нам треба вказати Fortify, як повертати наше представлення «login». Пам'ятайте: Fortify - headless-бібліотека автентифікації. Якщо вам потрібна готова фронтенд-реалізація можливостей автентифікації Laravel, скористайтеся [стартовим набором застосунку](/docs/{{version}}/starter-kits).

Усю логіку рендерингу представлень автентифікації можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку. Fortify подбає про визначення маршруту `/login`, який повертає це представлення:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

Ваш шаблон входу має містити форму, що робить POST-запит до `/login`. Ендпоїнт `/login` очікує рядок `email` / `username` і `password`. Ім'я поля пошти / імені користувача має збігатися зі значенням `username` у конфігураційному файлі `config/fortify.php`. Крім того, можна передати булеве поле `remember`, щоб вказати, що користувач хоче скористатися функціональністю «запам'ятати мене» від Laravel.

Якщо спроба входу успішна, Fortify перенаправить вас на URI, налаштований опцією `home` у конфігураційному файлі `fortify` вашого застосунку. Якщо запит на вхід був XHR-запитом, буде повернено HTTP-відповідь 200.

Якщо запит не був успішним, користувача буде перенаправлено назад на екран входу, а помилки валідації стануть доступні через спільну [змінну Blade-шаблону](/docs/{{version}}/validation#quick-displaying-the-validation-errors) `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.

<a name="customizing-user-authentication"></a>
### Налаштування автентифікації користувачів

Fortify автоматично знаходить і автентифікує користувача за наданими обліковими даними й гардом автентифікації, налаштованим для вашого застосунку. Проте іноді вам може знадобитися повний контроль над тим, як перевіряються облікові дані й як дістаються користувачі. На щастя, Fortify дозволяє легко цього досягти методом `Fortify::authenticateUsing`.

Цей метод приймає замикання, яке отримує вхідний HTTP-запит. Замикання відповідає за валідацію облікових даних із запиту й повернення відповідного екземпляра користувача. Якщо облікові дані недійсні або користувача не знайдено, замикання має повернути `null` чи `false`. Зазвичай цей метод викликають у методі `boot` вашого `FortifyServiceProvider`:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```

<a name="authentication-guard"></a>
#### Гард автентифікації

Ви можете налаштувати гард автентифікації, який використовує Fortify, у конфігураційному файлі `fortify` вашого застосунку. Проте переконайтеся, що налаштований гард реалізує `Illuminate\Contracts\Auth\StatefulGuard`. Якщо ви намагаєтеся автентифікувати SPA через Laravel Fortify, скористайтеся стандартним гардом Laravel `web` у поєднанні з [Laravel Sanctum](https://laravel.com/docs/sanctum).

<a name="customizing-the-authentication-pipeline"></a>
### Налаштування конвеєра автентифікації

Laravel Fortify автентифікує запити на вхід через конвеєр викликаних класів. За бажання ви можете описати власний конвеєр класів, через який проходитимуть запити на вхід. Кожен клас має містити метод `__invoke`, який отримує вхідний екземпляр `Illuminate\Http\Request` і, як у [`middleware`](/docs/{{version}}/middleware), змінну `$next`, що викликається, щоб передати запит наступному класу конвеєра.

Щоб описати власний конвеєр, скористайтеся методом `Fortify::authenticateThrough`. Цей метод приймає замикання, яке має повернути масив класів, через які слід пропустити запит на вхід. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку.

Наведений нижче приклад містить стандартне визначення конвеєра, яке можна взяти за відправну точку для власних змін:

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

#### Обмеження спроб автентифікації

За замовчуванням Fortify обмежує спроби автентифікації через `middleware` `EnsureLoginIsNotThrottled`. Це `middleware` обмежує спроби за унікальною комбінацією імені користувача та IP-адреси.

Деяким застосункам може знадобитися інший підхід до обмеження спроб автентифікації - наприклад, лише за IP-адресою. Тому Fortify дозволяє задати власний [обмежувач частоти](/docs/{{version}}/routing#rate-limiting) через опцію конфігурації `fortify.limiters.login`. Звісно, ця опція розташована в конфігураційному файлі `config/fortify.php` вашого застосунку.

> [!NOTE]
> Поєднання обмеження спроб, [двофакторної автентифікації](/docs/{{version}}/fortify#two-factor-authentication) і зовнішнього брандмауера вебзастосунків (WAF) дасть найнадійніший захист вашим справжнім користувачам.

<a name="customizing-authentication-redirects"></a>
### Налаштування перенаправлень

Якщо спроба входу успішна, Fortify перенаправить вас на URI, налаштований опцією `home` у конфігураційному файлі `fortify` вашого застосунку. Якщо запит на вхід був XHR-запитом, буде повернено HTTP-відповідь 200. Після виходу користувача із застосунку його буде перенаправлено на URI `/`.

Якщо вам потрібне складніше налаштування цієї поведінки, ви можете прив'язати реалізації контрактів `LoginResponse` та `LogoutResponse` до [сервіс-контейнера](/docs/{{version}}/container) Laravel. Зазвичай це роблять у методі `register` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```

<a name="two-factor-authentication"></a>
## Двофакторна автентифікація

Коли можливість двофакторної автентифікації Fortify увімкнено, користувач має ввести шестизначний числовий токен під час автентифікації. Цей токен генерується як одноразовий пароль на основі часу (TOTP), який можна отримати з будь-якого сумісного з TOTP мобільного застосунку автентифікації - як-от Google Authenticator.

Перш ніж почати, переконайтеся, що модель `App\Models\User` вашого застосунку використовує трейт `Laravel\Fortify\TwoFactorAuthenticatable`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
```

Далі вам слід побудувати у своєму застосунку екран, де користувачі зможуть керувати налаштуваннями двофакторної автентифікації. Цей екран має дозволяти вмикати й вимикати двофакторну автентифікацію, а також перегенеровувати коди відновлення.

> За замовчуванням масив `features` конфігураційного файлу `fortify` вказує, що налаштування двофакторної автентифікації Fortify вимагають підтвердження пароля перед зміною. Тому, перш ніж рухатися далі, ваш застосунок має реалізувати можливість [підтвердження пароля](#password-confirmation) від Fortify.

<a name="enabling-two-factor-authentication"></a>
### Увімкнення двофакторної автентифікації

Щоб почати вмикати двофакторну автентифікацію, ваш застосунок має зробити POST-запит до ендпоїнта `/user/two-factor-authentication`, визначеного Fortify. Якщо запит успішний, користувача буде перенаправлено назад на попередній URL, а сесійна змінна `status` набуде значення `two-factor-authentication-enabled`. Ви можете відстежити цю сесійну змінну `status` у своїх шаблонах, щоб показати відповідне повідомлення про успіх. Якщо запит був XHR-запитом, буде повернено HTTP-відповідь `200`.

Обравши увімкнення двофакторної автентифікації, користувач має ще «підтвердити» її налаштування, ввівши дійсний код. Тож ваше повідомлення про успіх має пояснити користувачеві, що підтвердження двофакторної автентифікації ще потрібне:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

Далі вам слід показати QR-код двофакторної автентифікації, щоб користувач відсканував його у своєму застосунку-автентифікаторі. Якщо ви рендерите фронтенд застосунку через Blade, отримати SVG із QR-кодом можна методом `twoFactorQrCodeSvg`, доступним на екземплярі користувача:

```php
$request->user()->twoFactorQrCodeSvg();
```

Якщо ви будуєте фронтенд на JavaScript, ви можете зробити XHR GET-запит до ендпоїнта `/user/two-factor-qr-code`, щоб отримати QR-код двофакторної автентифікації користувача. Цей ендпоїнт поверне JSON-об'єкт із ключем `svg`.

<a name="confirming-two-factor-authentication"></a>
#### Підтвердження двофакторної автентифікації

Окрім показу QR-коду двофакторної автентифікації, вам слід дати текстове поле, куди користувач введе дійсний код автентифікації, щоб «підтвердити» налаштування. Цей код має бути переданий застосунку Laravel POST-запитом до ендпоїнта `/user/confirmed-two-factor-authentication`, визначеного Fortify.

Якщо запит успішний, користувача буде перенаправлено назад на попередній URL, а сесійна змінна `status` набуде значення `two-factor-authentication-confirmed`:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

Якщо запит до ендпоїнта підтвердження двофакторної автентифікації був XHR-запитом, буде повернено HTTP-відповідь `200`.

<a name="displaying-the-recovery-codes"></a>
#### Показ кодів відновлення

Вам також слід показати коди відновлення двофакторної автентифікації користувача. Ці коди дозволяють автентифікуватися, якщо користувач втратить доступ до свого мобільного пристрою. Якщо ви рендерите фронтенд застосунку через Blade, до кодів відновлення можна дістатися через екземпляр автентифікованого користувача:

```php
(array) $request->user()->recoveryCodes()
```

Якщо ви будуєте фронтенд на JavaScript, ви можете зробити XHR GET-запит до ендпоїнта `/user/two-factor-recovery-codes`. Цей ендпоїнт поверне JSON-масив із кодами відновлення користувача.

Щоб перегенерувати коди відновлення користувача, ваш застосунок має зробити POST-запит до ендпоїнта `/user/two-factor-recovery-codes`.

<a name="authenticating-with-two-factor-authentication"></a>
### Автентифікація з двофакторною автентифікацією

Під час автентифікації Fortify автоматично перенаправить користувача на екран двофакторного виклику вашого застосунку. Проте якщо ваш застосунок робить XHR-запит на вхід, JSON-відповідь після успішної спроби автентифікації міститиме JSON-об'єкт із булевою властивістю `two_factor`. Перевіряйте це значення, щоб знати, чи слід перенаправляти на екран двофакторного виклику.

Щоб почати реалізацію двофакторної автентифікації, нам треба вказати Fortify, як повертати наше представлення двофакторного виклику. Усю логіку рендерингу представлень автентифікації Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify подбає про визначення маршруту `/two-factor-challenge`, який повертає це представлення. Ваш шаблон `two-factor-challenge` має містити форму, що робить POST-запит до ендпоїнта `/two-factor-challenge`. Дія `/two-factor-challenge` очікує поле `code` з дійсним TOTP-токеном або поле `recovery_code` з одним із кодів відновлення користувача.

Якщо спроба входу успішна, Fortify перенаправить користувача на URI, налаштований опцією `home` у конфігураційному файлі `fortify` вашого застосунку. Якщо запит на вхід був XHR-запитом, буде повернено HTTP-відповідь 204.

Якщо запит не був успішним, користувача буде перенаправлено назад на екран двофакторного виклику, а помилки валідації стануть доступні через спільну [змінну Blade-шаблону](/docs/{{version}}/validation#quick-displaying-the-validation-errors) `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.

<a name="disabling-two-factor-authentication"></a>
### Вимкнення двофакторної автентифікації

Щоб вимкнути двофакторну автентифікацію, ваш застосунок має зробити DELETE-запит до ендпоїнта `/user/two-factor-authentication`. Пам'ятайте: ендпоїнти двофакторної автентифікації Fortify вимагають [підтвердження пароля](#password-confirmation) перед викликом.

<a name="passkeys"></a>
## Passkeys

Fortify підтримує автентифікацію через passkeys на основі WebAuthn. Passkeys дозволяють користувачам автентифікуватися без паролів - через платформні автентифікатори на кшталт Face ID, Touch ID, Windows Hello чи апаратні ключі безпеки.

<a name="enabling-passkeys"></a>
### Увімкнення passkeys

Для початку переконайтеся, що можливість `passkeys` увімкнено в конфігураційному файлі `fortify` вашого застосунку:

```php
use Laravel\Fortify\Features;

'features' => [
    // ...
    Features::passkeys([
        'confirmPassword' => true,
    ]),
],
```

Опція `confirmPassword` визначає, чи вимагає Fortify [підтвердження пароля](#password-confirmation) перед реєстрацією чи видаленням passkeys.

Далі переконайтеся, що модель `App\Models\User` вашого застосунку реалізує `Laravel\Fortify\Contracts\PasskeyUser` і використовує трейт `Laravel\Fortify\PasskeyAuthenticatable`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\Contracts\PasskeyUser;
use Laravel\Fortify\PasskeyAuthenticatable;

class User extends Authenticatable implements PasskeyUser
{
    use Notifiable, PasskeyAuthenticatable;
}
```

Опції конфігурації passkeys у Fortify можна налаштувати через масив конфігурації `passkeys` у файлі `config/fortify.php` вашого застосунку:

```php
'passkeys' => [
    'relying_party_id' => parse_url(config('app.url'), PHP_URL_HOST),
    'allowed_origins' => [config('app.url')],
    'user_handle_secret' => config('app.key'),
    'timeout' => 60000,
],
```

> [!NOTE]
> Fortify обгортає Composer-пакет `laravel/passkeys` і налаштовує його за вас. Якщо ви користуєтеся можливістю passkeys у Fortify, налаштовуйте passkeys через файл `config/fortify.php` вашого застосунку. Публікувати конфігураційний файл `laravel/passkeys` не потрібно, і будь-які задані там значення буде перевизначено Fortify.

`relying_party_id` має збігатися з доменом вашого застосунку. Масив `allowed_origins` перелічує origin браузера, з яких можна завершити реєстрацію та автентифікацію через passkey. `user_handle_secret` використовується для виведення непрозорих ідентифікаторів користувачів, що гарантує впізнавання того самого користувача між реєстраціями passkeys. Опція `timeout` визначає, як довго можуть лишатися активними операції реєстрації та автентифікації passkey.

Fortify застосовує окремий обмежувач частоти passkeys до своїх маршрутів входу, підтвердження та реєстрації passkey. За потреби ви можете налаштувати його через опцію конфігурації `fortify.limiters.passkeys` і відповідне визначення `RateLimiter::for(...)`.

<a name="passkeys-javascript-client"></a>
### JavaScript-клієнт

Якщо ви будуєте власний фронтенд - зокрема застосунок на Blade зі скриптами на боці браузера, - ви можете скористатися офіційним пакетом [`@laravel/passkeys`](https://www.npmjs.com/package/@laravel/passkeys). Цей пакет обробляє церемонії WebAuthn у браузері й надсилає запити до ендпоїнтів passkey у Fortify.

Встановіть пакет через npm:

```shell
npm install @laravel/passkeys
```

Далі ви можете ініціювати реєстрацію та перевірку passkey зі свого фронтенду:

```js
import { Passkeys } from "@laravel/passkeys";

await Passkeys.register({ name: "MacBook Pro" });
await Passkeys.verify();
```

Якщо ваш застосунок використовує власні URI ендпоїнтів passkey, ви можете перевизначити маршрути для кожного виклику окремо:

```js
await Passkeys.verify({
    routes: {
        options: "/passkeys/confirm/options",
        submit: "/passkeys/confirm",
    },
});

await Passkeys.register({
    name: "MacBook Pro",
    routes: {
        options: "/user/passkeys/options",
        submit: "/user/passkeys",
    },
});
```

Пакет також надає хелпери для React, Vue і Svelte через `@laravel/passkeys/react`, `@laravel/passkeys/vue` та `@laravel/passkeys/svelte`.

<a name="authenticating-with-passkeys"></a>
### Автентифікація через passkeys

Щоб автентифікувати користувача через passkey, ваш застосунок має спершу зробити GET-запит до ендпоїнта `/passkeys/login/options`. Цей ендпоїнт повертає опції виклику WebAuthn, які ваш фронтенд має передати до `navigator.credentials.get(...)`.

Коли браузер поверне облікові дані, ваш застосунок має зробити POST-запит до `/passkeys/login` з даними цих облікових даних. Ви також можете додати булеве поле `remember`.

Якщо запит успішний, Fortify виконає вхід користувача в налаштований гард і поверне або:

<div class="content-list" markdown="1">

- Відповідь-перенаправлення до потрібного місця призначення для звичайних запитів.
- HTTP-відповідь `200` із JSON-даними, що містять ключ `redirect`, для XHR-запитів.

</div>

<a name="confirming-password-with-passkeys"></a>
### Підтвердження пароля через passkeys

Для автентифікованих сесій Fortify надає ендпоїнти підтвердження через passkey, які задовольняють вимогу Laravel щодо підтвердження пароля для поточної сесії.

Щоб підтвердити через passkey, ваш застосунок має спершу зробити GET-запит до `/passkeys/confirm/options`. Цей ендпоїнт повертає опції виклику WebAuthn, які ваш фронтенд має передати до `navigator.credentials.get(...)`.

Коли браузер поверне облікові дані, ваш застосунок має зробити POST-запит до `/passkeys/confirm` з даними цих облікових даних.

Якщо запит успішний, Fortify позначає поточну сесію як таку, де пароль підтверджено, і повертає або:

<div class="content-list" markdown="1">

- Відповідь-перенаправлення до потрібного місця призначення для звичайних запитів.
- HTTP-відповідь `200` із JSON-даними, що містять ключ `redirect`, для XHR-запитів.

</div>

<a name="registering-passkeys"></a>
### Реєстрація passkeys

Щоб зареєструвати passkey для автентифікованого користувача, ваш застосунок має спершу зробити GET-запит до `/user/passkeys/options`. Цей ендпоїнт повертає опції створення WebAuthn, які ваш фронтенд має передати до `navigator.credentials.create(...)`.

Коли браузер поверне облікові дані, ваш застосунок має зробити POST-запит до `/user/passkeys` з полем `name` і полем `credential`, що містить серіалізований об'єкт [`PublicKeyCredential`](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential), повернений `navigator.credentials.create(...)`.

Якщо запит успішний, Fortify поверне або:

<div class="content-list" markdown="1">

- Відповідь-перенаправлення назад зі статусом `passkey-registered` у сесії для звичайних запитів.
- HTTP-відповідь `200` із JSON-даними, що містять ключ `status`, а також `id` та `name` щойно зареєстрованого passkey.

</div>

<a name="deleting-passkeys"></a>
### Видалення passkeys

Щоб видалити passkey, ваш застосунок має зробити DELETE-запит до `/user/passkeys/{passkey}`.

Якщо запит успішний, Fortify поверне або:

<div class="content-list" markdown="1">

- Відповідь-перенаправлення назад зі статусом `passkey-deleted` у сесії для звичайних запитів.
- HTTP-відповідь `200` із JSON-даними, що містять ключ `status`, для XHR-запитів.

</div>

<a name="registration"></a>
## Реєстрація

Щоб почати реалізацію реєстрації у нашому застосунку, нам треба вказати Fortify, як повертати наше представлення «register». Пам'ятайте: Fortify - headless-бібліотека автентифікації. Якщо вам потрібна готова фронтенд-реалізація можливостей автентифікації Laravel, скористайтеся [стартовим набором застосунку](/docs/{{version}}/starter-kits).

Усю логіку рендерингу представлень Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` вашого класу `App\Providers\FortifyServiceProvider`:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify подбає про визначення маршруту `/register`, який повертає це представлення. Ваш шаблон `register` має містити форму, що робить POST-запит до ендпоїнта `/register`, визначеного Fortify.

Ендпоїнт `/register` очікує рядок `name`, рядкову адресу пошти / ім'я користувача, а також поля `password` і `password_confirmation`. Ім'я поля пошти / імені користувача має збігатися зі значенням конфігурації `username`, заданим у конфігураційному файлі `fortify` вашого застосунку.

Якщо спроба реєстрації успішна, Fortify перенаправить користувача на URI, налаштований опцією `home` у конфігураційному файлі `fortify` вашого застосунку. Якщо запит був XHR-запитом, буде повернено HTTP-відповідь 201.

Якщо запит не був успішним, користувача буде перенаправлено назад на екран реєстрації, а помилки валідації стануть доступні через спільну [змінну Blade-шаблону](/docs/{{version}}/validation#quick-displaying-the-validation-errors) `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.

<a name="customizing-registration"></a>
### Налаштування реєстрації

Процес валідації та створення користувача можна налаштувати, змінивши дію `App\Actions\Fortify\CreateNewUser`, згенеровану під час встановлення Laravel Fortify.

<a name="password-reset"></a>
## Скидання пароля

<a name="requesting-a-password-reset-link"></a>
### Запит посилання для скидання пароля

Щоб почати реалізацію скидання пароля у нашому застосунку, нам треба вказати Fortify, як повертати наше представлення «forgot password». Пам'ятайте: Fortify - headless-бібліотека автентифікації. Якщо вам потрібна готова фронтенд-реалізація можливостей автентифікації Laravel, скористайтеся [стартовим набором застосунку](/docs/{{version}}/starter-kits).

Усю логіку рендерингу представлень Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify подбає про визначення ендпоїнта `/forgot-password`, який повертає це представлення. Ваш шаблон `forgot-password` має містити форму, що робить POST-запит до ендпоїнта `/forgot-password`.

Ендпоїнт `/forgot-password` очікує рядкове поле `email`. Ім'я цього поля / стовпця бази даних має збігатися зі значенням конфігурації `email` у конфігураційному файлі `fortify` вашого застосунку.

<a name="handling-the-password-reset-link-request-response"></a>
#### Обробка відповіді на запит посилання для скидання пароля

Якщо запит посилання для скидання пароля успішний, Fortify перенаправить користувача назад на ендпоїнт `/forgot-password` і надішле йому лист із безпечним посиланням для скидання пароля. Якщо запит був XHR-запитом, буде повернено HTTP-відповідь 200.

Після перенаправлення назад на ендпоїнт `/forgot-password` після успішного запиту сесійна змінна `status` дозволяє показати стан спроби запиту посилання.

Значення сесійної змінної `$status` збігатиметься з одним із рядків перекладу, визначених у [мовному файлі](/docs/{{version}}/localization) `passwords` вашого застосунку. Якщо ви хочете змінити це значення, а мовні файли Laravel ще не опубліковано, зробіть це артизан-командою `lang:publish`:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

Якщо запит не був успішним, користувача буде перенаправлено назад на екран запиту посилання для скидання пароля, а помилки валідації стануть доступні через спільну [змінну Blade-шаблону](/docs/{{version}}/validation#quick-displaying-the-validation-errors) `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.

<a name="resetting-the-password"></a>
### Скидання пароля

Щоб завершити реалізацію скидання пароля у нашому застосунку, нам треба вказати Fortify, як повертати наше представлення «reset password».

Усю логіку рендерингу представлень Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify подбає про визначення маршруту, що показує це представлення. Ваш шаблон `reset-password` має містити форму, що робить POST-запит до `/reset-password`.

Ендпоїнт `/reset-password` очікує рядкове поле `email`, поле `password`, поле `password_confirmation` і приховане поле `token`, що містить значення `request()->route('token')`. Ім'я поля «email» / стовпця бази даних має збігатися зі значенням конфігурації `email`, заданим у конфігураційному файлі `fortify` вашого застосунку.

<a name="handling-the-password-reset-response"></a>
#### Обробка відповіді на скидання пароля

Якщо запит на скидання пароля успішний, Fortify перенаправить назад на маршрут `/login`, щоб користувач міг увійти з новим паролем. Крім того, буде встановлено сесійну змінну `status`, щоб ви могли показати успішний стан скидання на своєму екрані входу:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

Якщо запит був XHR-запитом, буде повернено HTTP-відповідь 200.

Якщо запит не був успішним, користувача буде перенаправлено назад на екран скидання пароля, а помилки валідації стануть доступні через спільну [змінну Blade-шаблону](/docs/{{version}}/validation#quick-displaying-the-validation-errors) `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.

<a name="customizing-password-resets"></a>
### Налаштування скидання паролів

Процес скидання пароля можна налаштувати, змінивши дію `App\Actions\ResetUserPassword`, згенеровану під час встановлення Laravel Fortify.

<a name="email-verification"></a>
## Підтвердження електронної пошти

Після реєстрації ви можете захотіти, щоб користувачі підтвердили свою адресу електронної пошти, перш ніж продовжити роботу із застосунком. Для початку переконайтеся, що можливість `emailVerification` увімкнено в масиві `features` вашого конфігураційного файлу `fortify`. Далі переконайтеся, що ваш клас `App\Models\User` реалізує інтерфейс `Illuminate\Contracts\Auth\MustVerifyEmail`.

Коли ці два кроки виконано, новозареєстровані користувачі отримуватимуть лист із проханням підтвердити свою адресу. Проте нам треба вказати Fortify, як показувати екран підтвердження пошти, який повідомляє користувачеві, що треба перейти за посиланням із листа.

Усю логіку рендерингу представлень Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify подбає про визначення маршруту, який показує це представлення, коли вбудоване `middleware` Laravel `verified` перенаправляє користувача на ендпоїнт `/email/verify`.

Ваш шаблон `verify-email` має містити інформаційне повідомлення з проханням натиснути посилання для підтвердження, надіслане на адресу користувача.

<a name="resending-email-verification-links"></a>
#### Повторне надсилання посилань для підтвердження пошти

За бажання ви можете додати до шаблону `verify-email` кнопку, що запускає POST-запит до ендпоїнта `/email/verification-notification`. Коли цей ендпоїнт отримує запит, користувачеві надсилається новий лист із посиланням для підтвердження - на випадок, якщо попереднє було випадково видалено чи загублено.

Якщо запит на повторне надсилання листа успішний, Fortify перенаправить користувача назад на ендпоїнт `/email/verify` із сесійною змінною `status`, що дозволить показати інформаційне повідомлення про успіх операції. Якщо запит був XHR-запитом, буде повернено HTTP-відповідь 202:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### Захист маршрутів

Щоб указати, що маршрут чи група маршрутів вимагає підтвердженої адреси електронної пошти, додайте до маршруту вбудоване `middleware` Laravel `verified`. Аліас `middleware` `verified` реєструється Laravel автоматично й слугує аліасом для `middleware` `Illuminate\Auth\Middleware\EnsureEmailIsVerified`:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## Підтвердження пароля

Будуючи застосунок, ви час від часу матимете дії, які вимагають від користувача підтвердити свій пароль, перш ніж дію буде виконано. Зазвичай такі маршрути захищають вбудованим `middleware` Laravel `password.confirm`.

Щоб почати реалізацію підтвердження пароля, нам треба вказати Fortify, як повертати представлення «password confirmation» нашого застосунку. Пам'ятайте: Fortify - headless-бібліотека автентифікації. Якщо вам потрібна готова фронтенд-реалізація можливостей автентифікації Laravel, скористайтеся [стартовим набором застосунку](/docs/{{version}}/starter-kits).

Усю логіку рендерингу представлень Fortify можна налаштувати відповідними методами класу `Laravel\Fortify\Fortify`. Зазвичай цей метод викликають у методі `boot` класу `App\Providers\FortifyServiceProvider` вашого застосунку:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify подбає про визначення ендпоїнта `/user/confirm-password`, який повертає це представлення. Ваш шаблон `confirm-password` має містити форму, що робить POST-запит до ендпоїнта `/user/confirm-password`. Ендпоїнт `/user/confirm-password` очікує поле `password` із поточним паролем користувача.

Якщо пароль збігається з поточним паролем користувача, Fortify перенаправить його на маршрут, до якого він намагався дістатися. Якщо запит був XHR-запитом, буде повернено HTTP-відповідь 201.

Якщо запит не був успішним, користувача буде перенаправлено назад на екран підтвердження пароля, а помилки валідації стануть доступні через спільну змінну Blade-шаблону `$errors`. Або ж, у випадку XHR-запиту, помилки валідації буде повернено з HTTP-відповіддю 422.
