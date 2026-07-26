---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Підтвердження електронної пошти

- [Вступ](#introduction)
    - [Підготовка моделі](#model-preparation)
    - [Підготовка бази даних](#database-preparation)
- [Маршрутизація](#verification-routing)
    - [Повідомлення про підтвердження пошти](#the-email-verification-notice)
    - [Обробник підтвердження пошти](#the-email-verification-handler)
    - [Повторне надсилання листа з підтвердженням](#resending-the-verification-email)
    - [Захист маршрутів](#protecting-routes)
- [Налаштування](#customization)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Багато вебзастосунків вимагають, щоб користувачі підтвердили свої адреси електронної пошти, перш ніж почати користуватися застосунком. Замість того щоб змушувати вас реалізовувати цю можливість вручну в кожному новому застосунку, Laravel надає зручні вбудовані сервіси для надсилання та перевірки запитів на підтвердження пошти.

> [!NOTE]
> Хочете швидко почати? Встановіть один зі [стартових наборів застосунку Laravel](/docs/{{version}}/starter-kits) у свіжий застосунок Laravel. Стартові набори створять усю вашу систему автентифікації, зокрема й підтримку підтвердження електронної пошти.

<a name="model-preparation"></a>
### Підготовка моделі

Перш ніж почати, переконайтеся, що ваша модель `App\Models\User` реалізує контракт `Illuminate\Contracts\Auth\MustVerifyEmail`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}
```

Щойно цей інтерфейс додано до вашої моделі, новозареєстрованим користувачам автоматично надсилатиметься лист із посиланням для підтвердження пошти. Це відбувається непомітно, бо Laravel автоматично реєструє [слухач](/docs/{{version}}/events) `Illuminate\Auth\Listeners\SendEmailVerificationNotification` для події `Illuminate\Auth\Events\Registered`.

Якщо ви реалізуєте реєстрацію у своєму застосунку вручну, а не через [стартовий набір](/docs/{{version}}/starter-kits), переконайтеся, що після успішної реєстрації користувача ви відправляєте подію `Illuminate\Auth\Events\Registered`:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### Підготовка бази даних

Далі ваша таблиця `users` має містити стовпець `email_verified_at`, щоб зберігати дату й час підтвердження адреси електронної пошти користувача. Зазвичай він уже є в стандартній міграції Laravel `0001_01_01_000000_create_users_table.php`.

<a name="verification-routing"></a>
## Маршрутизація

Щоб належно реалізувати підтвердження електронної пошти, знадобиться визначити три маршрути. Перший маршрут показуватиме користувачеві повідомлення про те, що йому слід натиснути посилання для підтвердження в листі, який Laravel надіслав після реєстрації.

Другий маршрут оброблятиме запити, що виникають, коли користувач натискає посилання для підтвердження в листі.

Третій маршрут повторно надсилатиме посилання для підтвердження, якщо користувач випадково втратив перше.

<a name="the-email-verification-notice"></a>
### Повідомлення про підтвердження пошти

Як згадувалося раніше, слід визначити маршрут, який повертатиме представлення з проханням натиснути посилання для підтвердження, надіслане користувачеві після реєстрації. Це представлення показуватиметься користувачам, коли вони спробують дістатися інших частин застосунку, не підтвердивши спершу свою адресу електронної пошти. Пам'ятайте: посилання надсилається користувачеві автоматично, якщо ваша модель `App\Models\User` реалізує інтерфейс `MustVerifyEmail`:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

Маршрут, що повертає повідомлення про підтвердження пошти, має називатися `verification.notice`. Важливо дати маршруту саме це ім'я, бо `middleware` `verified` [зі складу Laravel](#protecting-routes) автоматично перенаправлятиме на маршрут із цим іменем, якщо користувач не підтвердив свою адресу електронної пошти.

> [!NOTE]
> Реалізуючи підтвердження пошти вручну, ви маєте самі визначити вміст представлення з повідомленням. Якщо вам потрібен готовий каркас з усіма потрібними представленнями автентифікації та підтвердження, погляньте на [стартові набори застосунку Laravel](/docs/{{version}}/starter-kits).

<a name="the-email-verification-handler"></a>
### Обробник підтвердження пошти

Далі нам треба визначити маршрут, який оброблятиме запити, що виникають, коли користувач натискає надіслане йому посилання для підтвердження. Цей маршрут має називатися `verification.verify` і мати `middleware` `auth` та `signed`:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

Перш ніж рухатися далі, розгляньмо цей маршрут ближче. По-перше, ви помітите, що ми використовуємо тип запиту `EmailVerificationRequest` замість звичного екземпляра `Illuminate\Http\Request`. `EmailVerificationRequest` - це [запит форми](/docs/{{version}}/validation#form-request-validation) зі складу Laravel. Він автоматично подбає про валідацію параметрів запиту `id` та `hash`.

Далі ми можемо одразу викликати на запиті метод `fulfill`. Цей метод викличе метод `markEmailAsVerified` на автентифікованому користувачі й відправить подію `Illuminate\Auth\Events\Verified`. Метод `markEmailAsVerified` доступний стандартній моделі `App\Models\User` через базовий клас `Illuminate\Foundation\Auth\User`. Щойно адресу електронної пошти користувача підтверджено, ви можете перенаправити його куди завгодно.

<a name="resending-the-verification-email"></a>
### Повторне надсилання листа з підтвердженням

Іноді користувач може загубити чи випадково видалити лист із підтвердженням адреси. Про такий випадок варто подбати, визначивши маршрут, який дозволить користувачеві попросити надіслати лист повторно. Далі ви можете звертатися до цього маршруту, розмістивши просту кнопку надсилання форми у вашому [представленні з повідомленням про підтвердження](#the-email-verification-notice):

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### Захист маршрутів

[Маршрутне `middleware`](/docs/{{version}}/middleware) дозволяє пускати на певний маршрут лише користувачів із підтвердженою поштою. Laravel містить [аліас `middleware`](/docs/{{version}}/middleware#middleware-aliases) `verified` - це аліас для класу `middleware` `Illuminate\Auth\Middleware\EnsureEmailIsVerified`. Оскільки Laravel уже реєструє цей аліас автоматично, вам залишається тільки додати `middleware` `verified` до визначення маршруту. Зазвичай його поєднують із `middleware` `auth`:

```php
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);
```

Якщо користувач із непідтвердженою поштою спробує дістатися маршруту з цим `middleware`, його автоматично перенаправить на [іменований маршрут](/docs/{{version}}/routing#named-routes) `verification.notice`.

<a name="customization"></a>
## Налаштування

<a name="verification-email-customization"></a>
#### Налаштування листа з підтвердженням

Хоча стандартне сповіщення про підтвердження пошти задовольняє вимоги більшості застосунків, Laravel дозволяє налаштувати те, як формується поштове повідомлення з підтвердженням.

Для початку передайте замикання методу `toMailUsing`, який надає сповіщення `Illuminate\Auth\Notifications\VerifyEmail`. Замикання отримає екземпляр моделі-отримувача сповіщення, а також підписаний URL підтвердження, за яким користувач має перейти, щоб підтвердити свою адресу. Замикання має повернути екземпляр `Illuminate\Notifications\Messages\MailMessage`. Зазвичай метод `toMailUsing` викликають у методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]
> Щоб дізнатися більше про поштові сповіщення, зверніться до [документації про поштові сповіщення](/docs/{{version}}/notifications#mail-notifications).

<a name="events"></a>
## Події

Коли ви користуєтеся [стартовими наборами застосунку Laravel](/docs/{{version}}/starter-kits), Laravel відправляє [подію](/docs/{{version}}/events) `Illuminate\Auth\Events\Verified` під час процесу підтвердження пошти. Якщо ви обробляєте підтвердження пошти у своєму застосунку вручну, вам може знадобитися відправляти ці події самостійно після завершення підтвердження.
