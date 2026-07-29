---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Автентифікація

- [Вступ](#introduction)
    - [Стартові набори](#starter-kits)
    - [Що врахувати щодо бази даних](#introduction-database-considerations)
    - [Огляд екосистеми](#ecosystem-overview)
- [Швидкий старт автентифікації](#authentication-quickstart)
    - [Встановлення стартового набору](#install-a-starter-kit)
    - [Отримання автентифікованого користувача](#retrieving-the-authenticated-user)
    - [Захист маршрутів](#protecting-routes)
    - [Обмеження спроб входу](#login-throttling)
- [Ручна автентифікація користувачів](#authenticating-users)
    - [Запам'ятовування користувачів](#remembering-users)
    - [Інші методи автентифікації](#other-authentication-methods)
- [HTTP Basic Authentication](#http-basic-authentication)
    - [HTTP Basic Authentication без збереження стану](#stateless-http-basic-authentication)
- [Вихід із системи](#logging-out)
    - [Скасування сесій на інших пристроях](#invalidating-sessions-on-other-devices)
- [Підтвердження пароля](#password-confirmation)
    - [Конфігурація](#password-confirmation-configuration)
    - [Маршрутизація](#password-confirmation-routing)
    - [Захист маршрутів](#password-confirmation-protecting-routes)
- [Додавання власних гардів](#adding-custom-guards)
    - [Гарди на замиканнях запиту](#closure-request-guards)
- [Додавання власних провайдерів користувачів](#adding-custom-user-providers)
    - [Контракт User Provider](#the-user-provider-contract)
    - [Контракт Authenticatable](#the-authenticatable-contract)
- [Автоматичне перехешування паролів](#automatic-password-rehashing)
- [Соціальна автентифікація](/docs/{{version}}/socialite)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Багато вебзастосунків дають користувачам змогу автентифікуватися й «увійти». Реалізація цієї можливості у вебзастосунках може бути складною й потенційно ризикованою справою. Тому Laravel прагне дати вам інструменти, які дозволять реалізувати автентифікацію швидко, безпечно й легко.

За своєю суттю засоби автентифікації Laravel складаються з «гардів» (guards) і «провайдерів». Гарди визначають, як користувачі автентифікуються на кожному запиті. Наприклад, Laravel постачається з гардом `session`, який зберігає стан у сховищі сесій і в cookie.

Провайдери визначають, як користувачі дістаються з вашого постійного сховища. Laravel підтримує отримання користувачів через [Eloquent](/docs/{{version}}/eloquent) і конструктор запитів до бази даних. Проте ви вільні визначати додаткові провайдери відповідно до потреб вашого застосунку.

Конфігураційний файл автентифікації вашого застосунку розташований у `config/auth.php`. Цей файл містить кілька добре задокументованих опцій для налаштування поведінки сервісів автентифікації Laravel.

> [!NOTE]
> Не плутайте гарди й провайдери з «ролями» та «дозволами». Щоб дізнатися більше про авторизацію дій користувача через дозволи, зверніться до документації з [авторизації](/docs/{{version}}/authorization).

<a name="starter-kits"></a>
### Стартові набори

Хочете швидко почати? Встановіть [стартовий набір застосунку Laravel](/docs/{{version}}/starter-kits) у свіжий застосунок Laravel. Після міграції бази даних відкрийте у браузері `/register` чи будь-який інший URL вашого застосунку. Стартові набори створять усю вашу систему автентифікації!

**Навіть якщо ви вирішите не використовувати стартовий набір у своєму фінальному застосунку Laravel, встановлення [стартового набору](/docs/{{version}}/starter-kits) може стати чудовою нагодою навчитися реалізовувати всю функціональність автентифікації Laravel у справжньому проєкті.** Оскільки стартові набори Laravel уже містять контролери, маршрути та представлення автентифікації, ви можете вивчити код цих файлів і зрозуміти, як реалізуються можливості автентифікації в Laravel.

<a name="introduction-database-considerations"></a>
### Що врахувати щодо бази даних

За замовчуванням Laravel містить [модель Eloquent](/docs/{{version}}/eloquent) `App\Models\User` у вашому каталозі `app/Models`. Цю модель можна використовувати зі стандартним драйвером автентифікації Eloquent.

Якщо ваш застосунок не використовує Eloquent, ви можете скористатися провайдером автентифікації `database`, який працює через конструктор запитів Laravel. Якщо ваш застосунок використовує MongoDB, погляньте на офіційну [документацію MongoDB щодо автентифікації користувачів у Laravel](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/).

Будуючи схему бази даних для моделі `App\Models\User`, переконайтеся, що довжина стовпця пароля - щонайменше 60 символів. Звісно, міграція таблиці `users`, що входить до нових застосунків Laravel, уже створює стовпець із більшою довжиною.

Крім того, переконайтеся, що ваша таблиця `users` (або її аналог) містить nullable-стовпець `remember_token` типу string на 100 символів. У цьому стовпці зберігатиметься токен для користувачів, які обрали опцію «запам'ятати мене» під час входу у ваш застосунок. І знову ж таки: стандартна міграція таблиці `users` у нових застосунках Laravel уже містить цей стовпець.

<a name="ecosystem-overview"></a>
### Огляд екосистеми

Laravel пропонує кілька пакетів, пов'язаних з автентифікацією. Перш ніж рухатися далі, розгляньмо загальну екосистему автентифікації в Laravel і обговорімо призначення кожного пакета.

Спершу подумаймо, як працює автентифікація. Користуючись веббраузером, користувач вводить своє ім'я та пароль у формі входу. Якщо ці облікові дані правильні, застосунок збереже інформацію про автентифікованого користувача в [сесії](/docs/{{version}}/session) користувача. Виданий браузеру cookie містить ID сесії, тож наступні запити до застосунку можуть пов'язати користувача з правильною сесією. Отримавши сесійний cookie, застосунок дістане дані сесії за її ID, побачить, що інформацію про автентифікацію збережено в сесії, і вважатиме користувача «автентифікованим».

Коли віддаленому сервісу потрібно автентифікуватися для доступу до API, cookie зазвичай не використовуються, бо немає веббраузера. Натомість віддалений сервіс надсилає до API токен на кожному запиті. Застосунок може перевірити вхідний токен за таблицею дійсних API-токенів і «автентифікувати» запит як виконаний користувачем, пов'язаним із цим токеном.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Вбудовані сервіси браузерної автентифікації Laravel

Laravel містить вбудовані сервіси автентифікації та сесій, до яких зазвичай звертаються через фасади `Auth` і `Session`. Ці можливості забезпечують автентифікацію на основі cookie для запитів, ініційованих із веббраузерів. Вони надають методи, які дозволяють перевірити облікові дані користувача й автентифікувати його. Крім того, ці сервіси автоматично збережуть потрібні дані автентифікації в сесії користувача й видадуть йому сесійний cookie. Про використання цих сервісів ідеться в цій документації.

**Стартові набори застосунку**

Як розповідається в цій документації, ви можете взаємодіяти з цими сервісами автентифікації вручну, щоб побудувати власний шар автентифікації. Проте, щоб допомогти вам почати швидше, ми випустили [безкоштовні стартові набори](/docs/{{version}}/starter-kits), які дають надійний сучасний каркас усього шару автентифікації.

<a name="laravels-api-authentication-services"></a>
#### Сервіси API-автентифікації Laravel

Laravel пропонує два необов'язкові пакети, які допоможуть вам керувати API-токенами й автентифікувати запити з ними: [Passport](/docs/{{version}}/passport) та [Sanctum](/docs/{{version}}/sanctum). Зауважте, що ці бібліотеки й вбудовані бібліотеки автентифікації Laravel на основі cookie не є взаємовиключними. Ці бібліотеки зосереджені передусім на автентифікації через API-токени, тоді як вбудовані сервіси - на браузерній автентифікації через cookie. Багато застосунків використовуватимуть і вбудовані сервіси автентифікації Laravel на основі cookie, і один із пакетів API-автентифікації.

**Passport**

Passport - це провайдер автентифікації OAuth2, який пропонує різні «типи надання» (grant types) OAuth2 і дозволяє видавати різні типи токенів. Загалом це надійний і складний пакет для API-автентифікації. Проте більшості застосунків не потрібні складні можливості специфікації OAuth2, які можуть заплутати і користувачів, і розробників. До того ж розробники історично плуталися в тому, як автентифікувати SPA-застосунки чи мобільні застосунки через провайдери автентифікації OAuth2 на кшталт Passport.

**Sanctum**

У відповідь на складність OAuth2 і плутанину серед розробників ми взялися створити простіший, зручніший пакет автентифікації, який упорався б і з власними вебзапитами з браузера, і з API-запитами через токени. Цю мету втілив випуск [Laravel Sanctum](/docs/{{version}}/sanctum) - його варто вважати кращим і рекомендованим пакетом автентифікації для застосунків, що пропонують власний вебінтерфейс на додачу до API, або працюють на односторінковому застосунку (SPA), який існує окремо від бекенду Laravel, або мають мобільний клієнт.

Laravel Sanctum - це гібридний пакет вебавтентифікації / API-автентифікації, який може керувати всім процесом автентифікації вашого застосунку. Це можливо тому, що коли застосунок на Sanctum отримує запит, Sanctum спершу визначає, чи містить запит сесійний cookie, що вказує на автентифіковану сесію. Для цього Sanctum викликає вбудовані сервіси автентифікації Laravel, які ми обговорювали раніше. Якщо запит автентифікується не через сесійний cookie, Sanctum перевірить його на наявність API-токена. Якщо токен присутній, Sanctum автентифікує запит за ним. Щоб дізнатися більше про цей процес, зверніться до документації Sanctum [«як це працює»](/docs/{{version}}/sanctum#how-it-works).

<a name="summary-choosing-your-stack"></a>
#### Підсумок і вибір свого стека

Підсумовуючи: якщо доступ до вашого застосунку відбувається через браузер і ви будуєте монолітний застосунок Laravel, ваш застосунок використовуватиме вбудовані сервіси автентифікації Laravel.

Далі, якщо ваш застосунок пропонує API, яким користуватимуться треті сторони, ви обиратимете між [Passport](/docs/{{version}}/passport) і [Sanctum](/docs/{{version}}/sanctum) для автентифікації через API-токени. Загалом варто віддавати перевагу Sanctum там, де це можливо, адже це просте й повноцінне рішення для API-автентифікації, автентифікації SPA та мобільної автентифікації, з підтримкою «скопів» (scopes) чи «можливостей» (abilities).

Якщо ви будуєте односторінковий застосунок (SPA) на бекенді Laravel, вам варто скористатися [Laravel Sanctum](/docs/{{version}}/sanctum). Із Sanctum вам доведеться або [реалізувати власні маршрути автентифікації на бекенді вручну](#authenticating-users), або скористатися [Laravel Fortify](/docs/{{version}}/fortify) як headless-бекендом автентифікації, що надає маршрути й контролери для реєстрації, скидання пароля, підтвердження пошти тощо.

Passport варто обрати, коли вашому застосунку конче потрібні всі можливості специфікації OAuth2. Крім того, якщо ви будуєте [MCP-сервер](/docs/{{version}}/mcp), до якого звертатимуться AI-клієнти, вам варто скористатися Passport, адже MCP-клієнти зазвичай очікують [автентифікації через OAuth](/docs/{{version}}/mcp#oauth).

А якщо ви хочете швидко почати, ми радо рекомендуємо [наші стартові набори застосунку](/docs/{{version}}/starter-kits) як швидкий спосіб розпочати новий застосунок Laravel, що вже використовує наш улюблений стек автентифікації на вбудованих сервісах Laravel.

<a name="authentication-quickstart"></a>
## Швидкий старт автентифікації

> [!WARNING]
> У цій частині документації йдеться про автентифікацію користувачів через [стартові набори застосунку Laravel](/docs/{{version}}/starter-kits), які містять каркас UI, щоб допомогти вам швидко почати. Якщо ви хочете інтегруватися із системами автентифікації Laravel напряму, погляньте на документацію про [ручну автентифікацію користувачів](#authenticating-users).

<a name="install-a-starter-kit"></a>
### Встановлення стартового набору

Спершу вам слід [встановити стартовий набір застосунку Laravel](/docs/{{version}}/starter-kits). Наші стартові набори пропонують гарно оформлені відправні точки для впровадження автентифікації у ваш свіжий застосунок Laravel.

<a name="retrieving-the-authenticated-user"></a>
### Отримання автентифікованого користувача

Створивши застосунок зі стартового набору й дозволивши користувачам реєструватися та автентифікуватися, ви часто матимете справу з поточним автентифікованим користувачем. Під час обробки вхідного запиту ви можете дістатися автентифікованого користувача методом `user` фасада `Auth`:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

Або ж, коли користувач автентифікований, ви можете дістатися його через екземпляр `Illuminate\Http\Request`. Пам'ятайте: класи з підказками типів автоматично впроваджуються в методи ваших контролерів. Вказавши тип об'єкта `Illuminate\Http\Request`, ви отримаєте зручний доступ до автентифікованого користувача з будь-якого методу контролера через метод запиту `user`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
#### Визначення, чи автентифікований поточний користувач

Щоб визначити, чи автентифікований користувач, який робить вхідний HTTP-запит, скористайтеся методом `check` на фасаді `Auth`. Цей метод поверне `true`, якщо користувач автентифікований:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> Хоча визначити автентифікованість користувача можна методом `check`, зазвичай ви користуватиметеся `middleware`, щоб перевірити автентифікацію, перш ніж пускати користувача до певних маршрутів чи контролерів. Щоб дізнатися більше, погляньте на документацію про [захист маршрутів](/docs/{{version}}/authentication#protecting-routes).

<a name="protecting-routes"></a>
### Захист маршрутів

[Маршрутне `middleware`](/docs/{{version}}/middleware) дозволяє пускати на певний маршрут лише автентифікованих користувачів. Laravel постачається з `middleware` `auth` - це [аліас `middleware`](/docs/{{version}}/middleware#middleware-aliases) для класу `Illuminate\Auth\Middleware\Authenticate`. Оскільки Laravel уже реєструє цей аліас усередині, вам залишається лише додати `middleware` до визначення маршруту:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### Перенаправлення неавтентифікованих користувачів

Коли `middleware` `auth` виявляє неавтентифікованого користувача, воно перенаправляє його на [іменований маршрут](/docs/{{version}}/routing#named-routes) `login`. Ви можете змінити цю поведінку методом `redirectGuestsTo` у файлі `bootstrap/app.php` вашого застосунку:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### Перенаправлення автентифікованих користувачів

Коли `middleware` `guest` виявляє автентифікованого користувача, воно перенаправляє його на іменований маршрут `dashboard` або `home`. Ви можете змінити цю поведінку методом `redirectUsersTo` у файлі `bootstrap/app.php` вашого застосунку:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### Вказання гарда

Додаючи `middleware` `auth` до маршруту, ви також можете вказати, який «гард» слід використати для автентифікації користувача. Указаний гард має відповідати одному з ключів масиву `guards` у вашому конфігураційному файлі `auth.php`:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### Обмеження спроб входу

Якщо ви користуєтеся одним із наших [стартових наборів застосунку](/docs/{{version}}/starter-kits), обмеження частоти застосовуватиметься до спроб входу автоматично. За замовчуванням користувач не зможе увійти протягом хвилини, якщо після кількох спроб він так і не ввів правильні облікові дані. Обмеження унікальне для комбінації імені користувача / адреси пошти та його IP-адреси.

> [!NOTE]
> Якщо ви хочете обмежити частоту запитів до інших маршрутів вашого застосунку, погляньте на [документацію про обмеження частоти](/docs/{{version}}/routing#rate-limiting).

<a name="authenticating-users"></a>
## Ручна автентифікація користувачів

Вам не обов'язково користуватися каркасом автентифікації зі [стартових наборів застосунку](/docs/{{version}}/starter-kits) Laravel. Якщо ви вирішите не використовувати цей каркас, вам доведеться керувати автентифікацією користувачів безпосередньо через класи автентифікації Laravel. Не хвилюйтеся, це дуже просто!

Ми звертатимемося до сервісів автентифікації Laravel через [фасад](/docs/{{version}}/facades) `Auth`, тож не забудьте імпортувати фасад `Auth` на початку класу. Далі погляньмо на метод `attempt`. Метод `attempt` зазвичай обробляє спроби автентифікації з форми «входу» вашого застосунку. Якщо автентифікація успішна, вам слід перегенерувати [сесію](/docs/{{version}}/session) користувача, щоб запобігти [фіксації сесії](https://en.wikipedia.org/wiki/Session_fixation):

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

Метод `attempt` приймає першим аргументом масив пар ключ / значення. Значення з масиву використовуються для пошуку користувача у вашій таблиці бази даних. Тож у прикладі вище користувача буде знайдено за значенням стовпця `email`. Якщо користувача знайдено, збережений у базі захешований пароль буде порівняно зі значенням `password`, переданим методу в масиві. Вам не слід хешувати значення `password` із вхідного запиту, адже фреймворк автоматично захешує його перед порівнянням із хешем у базі. Якщо два хеші паролів збігаються, для користувача буде розпочато автентифіковану сесію.

Пам'ятайте: сервіси автентифікації Laravel діставатимуть користувачів із вашої бази даних відповідно до конфігурації «провайдера» вашого гарда автентифікації. У стандартному конфігураційному файлі `config/auth.php` вказано провайдер користувачів Eloquent і задано використовувати модель `App\Models\User`. Ви можете змінити ці значення у своєму конфігураційному файлі відповідно до потреб застосунку.

Метод `attempt` поверне `true`, якщо автентифікація успішна. Інакше буде повернено `false`.

Метод `intended` редиректора Laravel перенаправить користувача на URL, до якого він намагався дістатися, перш ніж його перехопило `middleware` автентифікації. Цьому методу можна передати запасний URI на випадок, якщо потрібне місце призначення недоступне.

<a name="specifying-additional-conditions"></a>
#### Вказання додаткових умов

За бажання ви можете додати до запиту автентифікації додаткові умови, окрім пошти й пароля користувача. Для цього просто додайте умови запиту до масиву, переданого методу `attempt`. Наприклад, ми можемо перевірити, що користувач позначений як «активний»:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

Для складних умов запиту ви можете передати в масиві облікових даних замикання. Це замикання буде викликано з екземпляром запиту, тож ви зможете налаштувати запит відповідно до потреб вашого застосунку:

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> У цих прикладах `email` не є обов'язковою опцією - він наведений лише як приклад. Вам слід використовувати те ім'я стовпця, яке відповідає «імені користувача» у вашій таблиці бази даних.

Метод `attemptWhen`, який приймає замикання другим аргументом, дозволяє ретельніше перевірити потенційного користувача, перш ніж власне його автентифікувати. Замикання отримує потенційного користувача й має повернути `true` або `false`, вказуючи, чи можна його автентифікувати:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a name="accessing-specific-guard-instances"></a>
#### Доступ до конкретних екземплярів гардів

Методом `guard` фасада `Auth` ви можете вказати, який екземпляр гарда використати для автентифікації користувача. Це дозволяє керувати автентифікацією окремих частин застосунку через цілком окремі моделі, придатні до автентифікації, чи таблиці користувачів.

Ім'я гарда, передане методу `guard`, має відповідати одному з гардів, налаштованих у вашому конфігураційному файлі `auth.php`:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### Запам'ятовування користувачів

Багато вебзастосунків мають на формі входу чекбокс «запам'ятати мене». Якщо ви хочете реалізувати цю функціональність у своєму застосунку, передайте булеве значення другим аргументом до методу `attempt`.

Коли це значення дорівнює `true`, Laravel триматиме користувача автентифікованим необмежено довго - або доки він не вийде вручну. Ваша таблиця `users` має містити стовпець `remember_token` типу string, у якому зберігатиметься токен «запам'ятати мене». Міграція таблиці `users`, що входить до нових застосунків Laravel, уже містить цей стовпець:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

Якщо ваш застосунок пропонує функціональність «запам'ятати мене», ви можете скористатися методом `viaRemember`, щоб визначити, чи був поточний автентифікований користувач автентифікований саме через cookie «запам'ятати мене»:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### Інші методи автентифікації

<a name="authenticate-a-user-instance"></a>
#### Автентифікація екземпляра користувача

Якщо вам потрібно зробити наявний екземпляр користувача поточним автентифікованим користувачем, передайте цей екземпляр методу `login` фасада `Auth`. Переданий екземпляр має реалізовувати [контракт](/docs/{{version}}/contracts) `Illuminate\Contracts\Auth\Authenticatable`. Модель `App\Models\User`, що входить до Laravel, уже реалізує цей інтерфейс. Такий спосіб автентифікації стає в пригоді, коли ви вже маєте дійсний екземпляр користувача - наприклад, одразу після його реєстрації у вашому застосунку:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

Ви можете передати методу `login` булеве значення другим аргументом. Воно вказує, чи потрібна для автентифікованої сесії функціональність «запам'ятати мене». Пам'ятайте: це означає, що сесія лишатиметься автентифікованою необмежено довго - або доки користувач не вийде із застосунку вручну:

```php
Auth::login($user, $remember = true);
```

За потреби ви можете вказати гард автентифікації перед викликом методу `login`:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### Автентифікація користувача за ID

Щоб автентифікувати користувача за первинним ключем його запису в базі даних, скористайтеся методом `loginUsingId`. Цей метод приймає первинний ключ користувача, якого ви хочете автентифікувати:

```php
Auth::loginUsingId(1);
```

Ви можете передати булеве значення в аргумент `remember` методу `loginUsingId`. Воно вказує, чи потрібна для автентифікованої сесії функціональність «запам'ятати мене». Пам'ятайте: це означає, що сесія лишатиметься автентифікованою необмежено довго - або доки користувач не вийде із застосунку вручну:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### Одноразова автентифікація користувача

Метод `once` дозволяє автентифікувати користувача в застосунку на один-єдиний запит. При виклику цього методу не використовуються ні сесії, ні cookie, а подія `Login` не відправляється:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication

[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) дає швидкий спосіб автентифікувати користувачів вашого застосунку без окремої сторінки «входу». Для початку додайте до маршруту [`middleware`](/docs/{{version}}/middleware) `auth.basic`. `middleware` `auth.basic` входить до фреймворку Laravel, тож визначати його не потрібно:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

Щойно `middleware` додано до маршруту, при зверненні до нього у браузері у вас автоматично запитають облікові дані. За замовчуванням `middleware` `auth.basic` вважатиме «іменем користувача» стовпець `email` у вашій таблиці `users`.

<a name="a-note-on-fastcgi"></a>
#### Зауваження щодо FastCGI

Якщо ви віддаєте свій застосунок Laravel через [PHP FastCGI](https://www.php.net/manual/en/install.fpm.php) та Apache, HTTP Basic Authentication може працювати некоректно. Щоб виправити ці проблеми, додайте до файлу `.htaccess` вашого застосунку такі рядки:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### HTTP Basic Authentication без збереження стану

Ви також можете користуватися HTTP Basic Authentication, не встановлюючи cookie з ідентифікатором користувача в сесії. Це передусім корисно, якщо ви обрали HTTP-автентифікацію для запитів до API вашого застосунку. Щоб цього досягти, [визначте `middleware`](/docs/{{version}}/middleware), яке викликає метод `onceBasic`. Якщо метод `onceBasic` не повертає відповіді, запит можна пропустити далі в застосунок:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

Далі додайте `middleware` до маршруту:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## Вихід із системи

Щоб вручну вивести користувачів із вашого застосунку, скористайтеся методом `logout`, який надає фасад `Auth`. Він прибере інформацію про автентифікацію із сесії користувача, тож наступні запити не будуть автентифікованими.

Окрім виклику методу `logout`, рекомендується скасувати сесію користувача й перегенерувати його [CSRF-токен](/docs/{{version}}/csrf). Після виходу користувача зазвичай перенаправляють у корінь застосунку:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
### Скасування сесій на інших пристроях

Laravel також надає механізм скасування й «виходу» із сесій користувача, активних на інших пристроях, не скасовуючи сесію на його поточному пристрої. Цю можливість зазвичай застосовують, коли користувач змінює чи оновлює свій пароль, і ви хочете скасувати сесії на інших пристроях, залишивши поточний автентифікованим.

Перш ніж почати, переконайтеся, що `middleware` `Illuminate\Session\Middleware\AuthenticateSession` додане до маршрутів, які мають отримувати автентифікацію сесії. Зазвичай це `middleware` розміщують у визначенні групи маршрутів, щоб застосувати його до більшості маршрутів вашого застосунку. За замовчуванням `middleware` `AuthenticateSession` можна додати до маршруту через [аліас `middleware`](/docs/{{version}}/middleware#middleware-aliases) `auth.session`:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

Далі ви можете скористатися методом `logoutOtherDevices`, який надає фасад `Auth`. Цей метод вимагає, щоб користувач підтвердив свій поточний пароль, - ваш застосунок має прийняти його через поле форми:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

Коли викликано метод `logoutOtherDevices`, інші сесії користувача буде повністю скасовано, тобто його «виведе» з усіх гардів, у яких він раніше був автентифікований.

<a name="password-confirmation"></a>
## Підтвердження пароля

Будуючи застосунок, ви час від часу матимете дії, які вимагають від користувача підтвердити свій пароль, перш ніж дію буде виконано або перш ніж користувача буде перенаправлено до чутливої частини застосунку. Laravel містить вбудоване `middleware`, яке робить цей процес легким. Реалізація цієї можливості вимагатиме визначити два маршрути: один - щоб показати представлення з проханням підтвердити пароль, і другий - щоб перевірити пароль і перенаправити користувача до місця призначення.

> [!NOTE]
> Далі йдеться про пряму інтеграцію з можливостями підтвердження пароля в Laravel; проте якщо ви хочете почати швидше, [стартові набори застосунку Laravel](/docs/{{version}}/starter-kits) уже містять підтримку цієї можливості!

<a name="password-confirmation-configuration"></a>
### Конфігурація

Підтвердивши свій пароль, користувач не отримуватиме повторного запиту протягом трьох годин. Проте ви можете налаштувати час до наступного запиту пароля, змінивши значення конфігурації `password_timeout` у файлі `config/auth.php` вашого застосунку.

<a name="password-confirmation-routing"></a>
### Маршрутизація

<a name="the-password-confirmation-form"></a>
#### Форма підтвердження пароля

Спершу визначимо маршрут, який показуватиме представлення з проханням підтвердити пароль:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

Як і слід очікувати, представлення, яке повертає цей маршрут, має містити форму з полем `password`. Крім того, сміливо додайте до представлення текст, який пояснює, що користувач заходить у захищену частину застосунку й має підтвердити свій пароль.

<a name="confirming-the-password"></a>
#### Підтвердження пароля

Далі визначимо маршрут, який оброблятиме запит форми з представлення «підтвердити пароль». Цей маршрут відповідатиме за валідацію пароля й перенаправлення користувача до місця призначення:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

Перш ніж рухатися далі, розгляньмо цей маршрут докладніше. Спершу перевіряється, чи поле `password` запиту справді збігається з паролем автентифікованого користувача. Якщо пароль дійсний, нам треба повідомити сесію Laravel, що користувач підтвердив свій пароль. Метод `passwordConfirmed` запише в сесію користувача часову мітку, за якою Laravel зможе визначити, коли той востаннє підтверджував пароль. Нарешті, ми можемо перенаправити користувача до місця призначення.

<a name="password-confirmation-protecting-routes"></a>
### Захист маршрутів

Переконайтеся, що будь-якому маршруту, який виконує дію, що вимагає нещодавнього підтвердження пароля, призначено `middleware` `password.confirm`. Це `middleware` входить до стандартної установки Laravel і автоматично збереже в сесії місце призначення користувача, щоб перенаправити його туди після підтвердження пароля. Зберігши місце призначення в сесії, `middleware` перенаправить користувача на [іменований маршрут](/docs/{{version}}/routing#named-routes) `password.confirm`:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## Додавання власних гардів

Ви можете визначати власні гарди автентифікації методом `extend` на фасаді `Auth`. Виклик методу `extend` слід розміщувати в [сервіс-провайдері](/docs/{{version}}/providers). Оскільки Laravel уже постачається з `AppServiceProvider`, ми можемо розмістити код саме там:

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

Як видно з прикладу вище, колбек, переданий методу `extend`, має повертати реалізацію `Illuminate\Contracts\Auth\Guard`. Цей інтерфейс містить кілька методів, які вам треба реалізувати, щоб визначити власний гард. Коли ваш гард визначено, ви можете послатися на нього в конфігурації `guards` вашого файлу `auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### Гарди на замиканнях запиту

Найпростіший спосіб реалізувати власну систему автентифікації на основі HTTP-запиту - метод `Auth::viaRequest`. Він дозволяє швидко описати процес автентифікації одним замиканням.

Для початку викличте метод `Auth::viaRequest` у методі `boot` вашого `AppServiceProvider`. Метод `viaRequest` приймає першим аргументом ім'я драйвера автентифікації. Це може бути будь-який рядок, що описує ваш гард. Другим аргументом має бути замикання, яке приймає вхідний HTTP-запит і повертає екземпляр користувача або `null`, якщо автентифікація не вдалася:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

Коли ваш драйвер автентифікації визначено, ви можете вказати його як драйвер у конфігурації `guards` вашого файлу `auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

Нарешті, ви можете послатися на цей гард, призначаючи маршруту `middleware` автентифікації:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## Додавання власних провайдерів користувачів

Якщо ви зберігаєте користувачів не в традиційній реляційній базі даних, вам знадобиться розширити Laravel власним провайдером користувачів для автентифікації. Ми скористаємося методом `provider` на фасаді `Auth`, щоб визначити власний провайдер. Резолвер провайдера має повертати реалізацію `Illuminate\Contracts\Auth\UserProvider`:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

Зареєструвавши провайдер методом `provider`, ви можете перемкнутися на новий провайдер користувачів у своєму конфігураційному файлі `auth.php`. Спершу визначте `provider`, що використовує ваш новий драйвер:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

Нарешті, ви можете послатися на цей провайдер у своїй конфігурації `guards`:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### Контракт User Provider

Реалізації `Illuminate\Contracts\Auth\UserProvider` відповідають за отримання реалізації `Illuminate\Contracts\Auth\Authenticatable` із системи постійного зберігання - MySQL, MongoDB тощо. Ці два інтерфейси дозволяють механізмам автентифікації Laravel працювати незалежно від того, як зберігаються дані користувачів і який клас представляє автентифікованого користувача:

Погляньмо на контракт `Illuminate\Contracts\Auth\UserProvider`:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

Функція `retrieveById` зазвичай отримує ключ, що представляє користувача, - наприклад, автоінкрементний ID із бази MySQL. Метод має знайти й повернути реалізацію `Authenticatable`, що відповідає цьому ID.

Функція `retrieveByToken` знаходить користувача за унікальним `$identifier` і токеном «запам'ятати мене» `$token`, який зазвичай зберігається у стовпці на кшталт `remember_token`. Як і в попередньому методі, він має повернути реалізацію `Authenticatable` із відповідним значенням токена.

Метод `updateRememberToken` оновлює `remember_token` екземпляра `$user` новим значенням `$token`. Новий токен призначається користувачам при успішній спробі автентифікації «запам'ятати мене» або коли користувач виходить із системи.

Метод `retrieveByCredentials` отримує масив облікових даних, переданий методу `Auth::attempt` під час спроби автентифікації в застосунку. Далі метод має «запитати» постійне сховище про користувача з такими обліковими даними. Зазвичай цей метод виконує запит з умовою «where», що шукає запис користувача з «іменем користувача», яке дорівнює значенню `$credentials['username']`. Метод має повернути реалізацію `Authenticatable`. **Цей метод не повинен намагатися перевіряти пароль чи виконувати автентифікацію.**

Метод `validateCredentials` має порівняти заданий `$user` із `$credentials`, щоб автентифікувати користувача. Наприклад, зазвичай цей метод використовує метод `Hash::check`, щоб порівняти значення `$user->getAuthPassword()` зі значенням `$credentials['password']`. Метод має повернути `true` або `false`, вказуючи, чи дійсний пароль.

Метод `rehashPasswordIfRequired` має перехешувати пароль заданого `$user`, якщо це потрібно й підтримується. Наприклад, зазвичай цей метод використовує метод `Hash::needsRehash`, щоб визначити, чи потребує значення `$credentials['password']` перехешування. Якщо пароль потрібно перехешувати, метод має скористатися методом `Hash::make`, щоб перехешувати пароль і оновити запис користувача в постійному сховищі.

<a name="the-authenticatable-contract"></a>
### Контракт Authenticatable

Тепер, коли ми розглянули кожен метод `UserProvider`, погляньмо на контракт `Authenticatable`. Пам'ятайте: провайдери користувачів мають повертати реалізації цього інтерфейсу з методів `retrieveById`, `retrieveByToken` і `retrieveByCredentials`:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

Цей інтерфейс простий. Метод `getAuthIdentifierName` має повертати ім'я стовпця «первинного ключа» користувача, а метод `getAuthIdentifier` - сам «первинний ключ». У випадку бекенду MySQL це, найімовірніше, автоінкрементний первинний ключ, призначений запису користувача. Метод `getAuthPasswordName` має повертати ім'я стовпця з паролем користувача. Метод `getAuthPassword` має повертати захешований пароль користувача.

Цей інтерфейс дозволяє системі автентифікації працювати з будь-яким класом «користувача» - незалежно від того, який ORM чи шар абстракції сховища ви використовуєте. За замовчуванням Laravel містить клас `App\Models\User` у каталозі `app/Models`, який реалізує цей інтерфейс.

<a name="automatic-password-rehashing"></a>
## Автоматичне перехешування паролів

Стандартний алгоритм хешування паролів у Laravel - bcrypt. «Фактор складності» (work factor) для хешів bcrypt можна змінити у файлі `config/hashing.php` вашого застосунку або через змінну оточення `BCRYPT_ROUNDS`.

Зазвичай фактор складності bcrypt варто з часом збільшувати в міру зростання обчислювальної потужності CPU / GPU. Якщо ви збільшите фактор складності bcrypt у своєму застосунку, Laravel плавно й автоматично перехешує паролі користувачів у міру того, як вони автентифікуються через стартові набори Laravel або коли ви [автентифікуєте користувачів вручну](#authenticating-users) методом `attempt`.

Зазвичай автоматичне перехешування паролів не має заважати вашому застосунку; проте ви можете вимкнути цю поведінку, опублікувавши конфігураційний файл `hashing`:

```shell
php artisan config:publish hashing
```

Коли конфігураційний файл опубліковано, ви можете встановити значення конфігурації `rehash_on_login` у `false`:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## Події

Під час процесу автентифікації Laravel відправляє різні [події](/docs/{{version}}/events). Ви можете [визначити слухачів](/docs/{{version}}/events) для будь-якої з наведених нижче подій:

<div class="overflow-auto">

| Ім'я події                                     |
| ---------------------------------------------- |
| `Illuminate\Auth\Events\Registered`            |
| `Illuminate\Auth\Events\Attempting`            |
| `Illuminate\Auth\Events\Authenticated`         |
| `Illuminate\Auth\Events\Login`                 |
| `Illuminate\Auth\Events\Failed`                |
| `Illuminate\Auth\Events\Validated`             |
| `Illuminate\Auth\Events\Verified`              |
| `Illuminate\Auth\Events\Logout`                |
| `Illuminate\Auth\Events\CurrentDeviceLogout`   |
| `Illuminate\Auth\Events\OtherDeviceLogout`     |
| `Illuminate\Auth\Events\Lockout`               |
| `Illuminate\Auth\Events\PasswordReset`         |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>
