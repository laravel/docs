---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Cashier (Stripe)

- [Вступ](#introduction)
- [Оновлення Cashier](#upgrading-cashier)
- [Встановлення](#installation)
- [Конфігурація](#configuration)
    - [Модель з білінгом](#billable-model)
    - [API-ключі](#api-keys)
    - [Конфігурація валюти](#currency-configuration)
    - [Конфігурація податків](#tax-configuration)
    - [Логування](#logging)
    - [Використання власних моделей](#using-custom-models)
- [Швидкий старт](#quickstart)
    - [Продаж продуктів](#quickstart-selling-products)
    - [Продаж підписок](#quickstart-selling-subscriptions)
- [Клієнти](#customers)
    - [Отримання клієнтів](#retrieving-customers)
    - [Створення клієнтів](#creating-customers)
    - [Оновлення клієнтів](#updating-customers)
    - [Баланси](#balances)
    - [Податкові номери](#tax-ids)
    - [Синхронізація даних клієнта зі Stripe](#syncing-customer-data-with-stripe)
    - [Портал білінгу](#billing-portal)
- [Платіжні методи](#payment-methods)
    - [Збереження платіжних методів](#storing-payment-methods)
    - [Отримання платіжних методів](#retrieving-payment-methods)
    - [Наявність платіжного методу](#payment-method-presence)
    - [Оновлення платіжного методу за замовчуванням](#updating-the-default-payment-method)
    - [Додавання платіжних методів](#adding-payment-methods)
    - [Видалення платіжних методів](#deleting-payment-methods)
- [Підписки](#subscriptions)
    - [Створення підписок](#creating-subscriptions)
    - [Перевірка стану підписки](#checking-subscription-status)
    - [Зміна цін](#changing-prices)
    - [Кількість у підписці](#subscription-quantity)
    - [Підписки з кількома продуктами](#subscriptions-with-multiple-products)
    - [Кілька підписок](#multiple-subscriptions)
    - [Білінг за використанням](#usage-based-billing)
    - [Податки на підписки](#subscription-taxes)
    - [Опорна дата підписки](#subscription-anchor-date)
    - [Скасування підписок](#cancelling-subscriptions)
    - [Відновлення підписок](#resuming-subscriptions)
- [Пробні періоди підписок](#subscription-trials)
    - [З платіжним методом наперед](#with-payment-method-up-front)
    - [Без платіжного методу наперед](#without-payment-method-up-front)
    - [Продовження пробних періодів](#extending-trials)
- [Обробка вебхуків Stripe](#handling-stripe-webhooks)
    - [Визначення обробників подій вебхуків](#defining-webhook-event-handlers)
    - [Перевірка підписів вебхуків](#verifying-webhook-signatures)
- [Разові списання](#single-charges)
    - [Просте списання](#simple-charge)
    - [Списання з рахунком](#charge-with-invoice)
    - [Створення Payment Intent](#creating-payment-intents)
    - [Повернення коштів за списаннями](#refunding-charges)
- [Рахунки](#invoices)
    - [Отримання рахунків](#retrieving-invoices)
    - [Майбутні рахунки](#upcoming-invoices)
    - [Попередній перегляд рахунків за підпискою](#previewing-subscription-invoices)
    - [Генерація PDF-рахунків](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [Оформлення продуктів](#product-checkouts)
    - [Оформлення разових списань](#single-charge-checkouts)
    - [Оформлення підписок](#subscription-checkouts)
    - [Збір податкових номерів](#collecting-tax-ids)
    - [Гостьове оформлення](#guest-checkouts)
- [Обробка невдалих платежів](#handling-failed-payments)
    - [Підтвердження платежів](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Платежі, що потребують додаткового підтвердження](#payments-requiring-additional-confirmation)
    - [Сповіщення про позасесійні платежі](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) дає виразний, плавний інтерфейс до сервісів білінгу підписок [Stripe](https://stripe.com). Він бере на себе майже весь шаблонний код білінгу підписок, який ви боїтеся писати. Окрім базового керування підписками, Cashier уміє працювати з купонами, змінювати підписки, обробляти «кількості» в підписках, пільгові періоди після скасування і навіть генерувати PDF-рахунки.

<a name="upgrading-cashier"></a>
## Оновлення Cashier

Оновлюючись до нової версії Cashier, важливо уважно переглянути [посібник з оновлення](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md).

> [!WARNING]
> Щоб уникнути ламких змін, Cashier використовує фіксовану версію API Stripe. Cashier 16 використовує версію API Stripe `2025-06-30.basil`. Версію API Stripe оновлюватимуть у мінорних випусках, щоб скористатися новими можливостями й покращеннями Stripe.

<a name="installation"></a>
## Встановлення

Спершу встановіть пакет Cashier для Stripe за допомогою менеджера пакетів Composer:

```shell
composer require laravel/cashier
```

Після встановлення пакета опублікуйте міграції Cashier артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

Далі виконайте міграції своєї бази даних:

```shell
php artisan migrate
```

Міграції Cashier додадуть кілька колонок до вашої таблиці `users`. Вони також створять нову таблицю `subscriptions` для зберігання всіх підписок ваших клієнтів і таблицю `subscription_items` для підписок з кількома цінами.

За бажанням ви також можете опублікувати конфігураційний файл Cashier артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --tag="cashier-config"
```

Насамкінець, щоб Cashier належно обробляв усі події Stripe, не забудьте [налаштувати обробку вебхуків Cashier](#handling-stripe-webhooks).

> [!WARNING]
> Stripe рекомендує, щоб будь-яка колонка для зберігання ідентифікаторів Stripe була чутливою до регістру. Тому вам слід подбати, щоб для колонки `stripe_id` було задано порівняння `utf8_bin`, якщо ви використовуєте MySQL. Докладніше про це - у [документації Stripe](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible).

<a name="configuration"></a>
## Конфігурація

<a name="billable-model"></a>
### Модель з білінгом

Перш ніж користуватися Cashier, додайте трейт `Billable` до визначення своєї моделі з білінгом. Зазвичай це буде модель `App\Models\User`. Цей трейт надає різні методи, що дозволяють виконувати типові завдання білінгу: створювати підписки, застосовувати купони й оновлювати інформацію про платіжний метод:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier припускає, що вашою моделлю з білінгом буде клас `App\Models\User`, який постачається з Laravel. Якщо ви хочете змінити це, вкажіть іншу модель методом `useCustomerModel`. Зазвичай цей метод слід викликати в методі `boot` вашого класу `AppServiceProvider`:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Якщо ви використовуєте модель, відмінну від наданої Laravel моделі `App\Models\User`, вам потрібно буде опублікувати й змінити надані [міграції Cashier](#installation) відповідно до імені таблиці вашої альтернативної моделі.

<a name="api-keys"></a>
### API-ключі

Далі вам слід налаштувати свої API-ключі Stripe у файлі `.env` вашого застосунку. Отримати API-ключі Stripe можна з панелі керування Stripe:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> Вам слід подбати, щоб змінну оточення `STRIPE_WEBHOOK_SECRET` було визначено у файлі `.env` вашого застосунку, оскільки вона використовується, щоб пересвідчитися, що вхідні вебхуки справді надходять від Stripe.

<a name="currency-configuration"></a>
### Конфігурація валюти

Валюта Cashier за замовчуванням - долар США (USD). Ви можете змінити валюту за замовчуванням, встановивши змінну оточення `CASHIER_CURRENCY` у файлі `.env` вашого застосунку:

```ini
CASHIER_CURRENCY=eur
```

Окрім налаштування валюти Cashier, ви також можете вказати локаль, яка використовуватиметься для форматування грошових значень для показу в рахунках. Внутрішньо Cashier використовує [клас PHP `NumberFormatter`](https://www.php.net/manual/en/class.numberformatter.php), щоб задати локаль валюти:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> Щоб використовувати локалі, відмінні від `en`, переконайтеся, що PHP-розширення `ext-intl` встановлено й налаштовано на вашому сервері.

<a name="tax-configuration"></a>
### Конфігурація податків

Завдяки [Stripe Tax](https://stripe.com/tax) можна автоматично обчислювати податки для всіх рахунків, згенерованих Stripe. Увімкнути автоматичне обчислення податків можна, викликавши метод `calculateTaxes` у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

Щойно обчислення податків увімкнено, усі нові підписки й усі разові рахунки, які будуть згенеровані, отримають автоматичне обчислення податків.

Щоб ця можливість працювала належно, платіжні дані вашого клієнта - ім'я, адреса й податковий номер - мають бути синхронізовані зі Stripe. Для цього ви можете скористатися методами [синхронізації даних клієнта](#syncing-customer-data-with-stripe) і [податкових номерів](#tax-ids), які пропонує Cashier.

<a name="logging"></a>
### Логування

Cashier дозволяє вказати канал логування, який використовуватиметься для запису фатальних помилок Stripe. Задати канал логування можна, визначивши змінну оточення `CASHIER_LOGGER` у файлі `.env` вашого застосунку:

```ini
CASHIER_LOGGER=stack
```

Винятки, згенеровані API-викликами до Stripe, логуватимуться через канал логування вашого застосунку за замовчуванням.

<a name="using-custom-models"></a>
### Використання власних моделей

Ви можете розширювати моделі, які Cashier використовує внутрішньо, визначивши власну модель і розширивши відповідну модель Cashier:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

Визначивши свою модель, ви можете вказати Cashier використовувати вашу власну модель через клас `Laravel\Cashier\Cashier`. Зазвичай повідомляти Cashier про ваші власні моделі слід у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="quickstart"></a>
## Швидкий старт

<a name="quickstart-selling-products"></a>
### Продаж продуктів

> [!NOTE]
> Перш ніж користуватися Stripe Checkout, вам слід визначити продукти з фіксованими цінами у своїй панелі Stripe. Крім того, вам слід [налаштувати обробку вебхуків Cashier](#handling-stripe-webhooks).

Пропонувати білінг продуктів і підписок через ваш застосунок може здаватися страшним. Однак завдяки Cashier і [Stripe Checkout](https://stripe.com/payments/checkout) ви можете легко побудувати сучасні, надійні платіжні інтеграції.

Щоб списувати кошти з клієнтів за неперіодичні продукти з разовим списанням, ми скористаємося Cashier, щоб направити клієнтів до Stripe Checkout, де вони нададуть свої платіжні дані й підтвердять покупку. Щойно платіж буде здійснено через Checkout, клієнта буде перенаправлено на обрану вами URL-адресу успіху у вашому застосунку:

```php
use Illuminate\Http\Request;

Route::get('/checkout', function (Request $request) {
    $stripePriceId = 'price_deluxe_album';

    $quantity = 1;

    return $request->user()->checkout([$stripePriceId => $quantity], [
        'success_url' => route('checkout-success'),
        'cancel_url' => route('checkout-cancel'),
    ]);
})->name('checkout');

Route::view('/checkout/success', 'checkout.success')->name('checkout-success');
Route::view('/checkout/cancel', 'checkout.cancel')->name('checkout-cancel');
```

Як бачите в наведеному вище прикладі, ми скористаємося наданим Cashier методом `checkout`, щоб перенаправити клієнта до Stripe Checkout для заданого «ідентифікатора ціни». У Stripe «ціни» - це [визначені ціни для конкретних продуктів](https://stripe.com/docs/products-prices/how-products-and-prices-work).

За потреби метод `checkout` автоматично створить клієнта у Stripe і зв'яже цей запис клієнта Stripe з відповідним користувачем у базі даних вашого застосунку. Після завершення сесії оформлення клієнта буде перенаправлено на спеціальну сторінку успіху чи скасування, де ви можете показати йому інформаційне повідомлення.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Передавання метаданих до Stripe Checkout

Продаючи продукти, зазвичай відстежують завершені замовлення й куплені продукти через моделі `Cart` і `Order`, визначені у вашому власному застосунку. Перенаправляючи клієнтів до Stripe Checkout для завершення покупки, вам може знадобитися передати наявний ідентифікатор замовлення, щоб пов'язати завершену покупку з відповідним замовленням, коли клієнта буде перенаправлено назад до вашого застосунку.

Щоб досягти цього, передайте до методу `checkout` масив `metadata`. Уявімо, що в нашому застосунку створюється незавершене замовлення `Order`, коли користувач починає процес оформлення. Пам'ятайте: моделі `Cart` і `Order` у цьому прикладі є ілюстративними і не надаються Cashier. Ви можете реалізувати ці концепції відповідно до потреб власного застосунку:

```php
use App\Models\Cart;
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/cart/{cart}/checkout', function (Request $request, Cart $cart) {
    $order = Order::create([
        'cart_id' => $cart->id,
        'price_ids' => $cart->price_ids,
        'status' => 'incomplete',
    ]);

    return $request->user()->checkout($order->price_ids, [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
        'metadata' => ['order_id' => $order->id],
    ]);
})->name('checkout');
```

Як бачите в наведеному вище прикладі, коли користувач починає процес оформлення, ми передаємо до методу `checkout` усі пов'язані з кошиком / замовленням ідентифікатори цін Stripe. Звісно, ваш застосунок відповідає за прив'язку цих позицій до «кошика» чи замовлення, коли клієнт їх додає. Ми також передаємо ID замовлення до сесії Stripe Checkout через масив `metadata`. Насамкінець ми додали шаблонну змінну `CHECKOUT_SESSION_ID` до маршруту успіху Checkout. Коли Stripe перенаправить клієнтів назад до вашого застосунку, цю шаблонну змінну буде автоматично заповнено ID сесії Checkout.

Далі побудуймо маршрут успіху Checkout. Це маршрут, на який користувачів буде перенаправлено після завершення покупки через Stripe Checkout. У цьому маршруті ми можемо отримати ID сесії Stripe Checkout і пов'язаний екземпляр Stripe Checkout, щоб звернутися до переданих нами метаданих і відповідно оновити замовлення клієнта:

```php
use App\Models\Order;
use Illuminate\Http\Request;
use Laravel\Cashier\Cashier;

Route::get('/checkout/success', function (Request $request) {
    $sessionId = $request->get('session_id');

    if ($sessionId === null) {
        return;
    }

    $session = Cashier::stripe()->checkout->sessions->retrieve($sessionId);

    if ($session->payment_status !== 'paid') {
        return;
    }

    $orderId = $session['metadata']['order_id'] ?? null;

    $order = Order::findOrFail($orderId);

    $order->update(['status' => 'completed']);

    return view('checkout-success', ['order' => $order]);
})->name('checkout-success');
```

Докладніше про [дані, які містить об'єкт сесії Checkout](https://stripe.com/docs/api/checkout/sessions/object), дивіться в документації Stripe.

<a name="quickstart-selling-subscriptions"></a>
### Продаж підписок

> [!NOTE]
> Перш ніж користуватися Stripe Checkout, вам слід визначити продукти з фіксованими цінами у своїй панелі Stripe. Крім того, вам слід [налаштувати обробку вебхуків Cashier](#handling-stripe-webhooks).

Пропонувати білінг продуктів і підписок через ваш застосунок може здаватися страшним. Однак завдяки Cashier і [Stripe Checkout](https://stripe.com/payments/checkout) ви можете легко побудувати сучасні, надійні платіжні інтеграції.

Щоб дізнатися, як продавати підписки за допомогою Cashier і Stripe Checkout, розгляньмо простий сценарій сервісу підписок з базовим місячним (`price_basic_monthly`) і річним (`price_basic_yearly`) планом. Ці дві ціни можна згрупувати під продуктом «Basic» (`pro_basic`) у нашій панелі Stripe. Крім того, наш сервіс підписок може пропонувати план Expert як `pro_expert`.

Спершу з'ясуймо, як клієнт може підписатися на наші сервіси. Звісно, можна уявити, що клієнт натисне кнопку «subscribe» для плану Basic на сторінці цін нашого застосунку. Ця кнопка чи посилання має направити користувача до маршруту Laravel, який створює сесію Stripe Checkout для обраного плану:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_basic_monthly')
        ->trialDays(5)
        ->allowPromotionCodes()
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

Як бачите в наведеному вище прикладі, ми перенаправимо клієнта до сесії Stripe Checkout, яка дозволить йому підписатися на наш план Basic. Після успішного оформлення чи скасування клієнта буде перенаправлено назад на URL, який ми передали до методу `checkout`. Щоб знати, коли підписка справді почалася (оскільки деяким платіжним методам потрібно кілька секунд на обробку), нам також потрібно [налаштувати обробку вебхуків Cashier](#handling-stripe-webhooks).

Тепер, коли клієнти можуть починати підписки, нам потрібно обмежити певні частини нашого застосунку так, щоб доступ до них мали лише підписані користувачі. Звісно, ми завжди можемо визначити поточний стан підписки користувача методом `subscribed`, який надає трейт `Billable` з Cashier:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

Ми навіть легко можемо визначити, чи підписаний користувач на конкретний продукт чи ціну:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### Створення middleware для підписаних

Для зручності ви можете створити [middleware](/docs/{{version}}/middleware), який визначає, чи надійшов вхідний запит від підписаного користувача. Щойно цей `middleware` буде визначено, ви зможете легко призначити його маршруту, щоб не пускати до нього непідписаних користувачів:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // Redirect user to billing page and ask them to subscribe...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

Щойно `middleware` визначено, ви можете призначити його маршруту:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### Дозвіл клієнтам керувати своїм планом білінгу

Звісно, клієнти можуть захотіти змінити свій план підписки на інший продукт чи «рівень». Найпростіший спосіб це дозволити - направити клієнтів до [порталу білінгу для клієнтів](https://stripe.com/docs/no-code/customer-portal) від Stripe, який надає розміщений інтерфейс, де клієнти можуть завантажувати рахунки, оновлювати платіжний метод і змінювати плани підписки.

Спершу визначте у своєму застосунку посилання чи кнопку, що направляє користувачів до маршруту Laravel, який ми використаємо для ініціації сесії порталу білінгу:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

Далі визначмо маршрут, який ініціює сесію порталу білінгу для клієнтів Stripe і перенаправляє користувача до порталу. Метод `redirectToBillingPortal` приймає URL, на який користувачів слід повернути, коли вони вийдуть з порталу:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Доки ви налаштували обробку вебхуків Cashier, Cashier автоматично підтримуватиме пов'язані з ним таблиці бази даних вашого застосунку синхронізованими, аналізуючи вхідні вебхуки від Stripe. Так, наприклад, коли користувач скасує свою підписку через портал білінгу для клієнтів Stripe, Cashier отримає відповідний вебхук і позначить підписку як «скасовану» в базі даних вашого застосунку.

<a name="customers"></a>
## Клієнти

<a name="retrieving-customers"></a>
### Отримання клієнтів

Ви можете отримати клієнта за його Stripe ID методом `Cashier::findBillable`. Цей метод поверне екземпляр моделі з білінгом:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### Створення клієнтів

Іноді ви можете захотіти створити клієнта Stripe, не починаючи підписки. Зробити це можна методом `createAsStripeCustomer`:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Щойно клієнта створено у Stripe, ви можете почати підписку пізніше. Ви можете передати необов'язковий масив `$options`, щоб указати будь-які додаткові [параметри створення клієнта, які підтримує API Stripe](https://stripe.com/docs/api/customers/create):

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

Ви можете скористатися методом `asStripeCustomer`, якщо хочете повернути об'єкт клієнта Stripe для моделі з білінгом:

```php
$stripeCustomer = $user->asStripeCustomer();
```

Метод `createOrGetStripeCustomer` можна використати, якщо ви хочете отримати об'єкт клієнта Stripe для певної моделі з білінгом, але не впевнені, чи є ця модель уже клієнтом у Stripe. Цей метод створить нового клієнта у Stripe, якщо такого ще немає:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### Оновлення клієнтів

Іноді ви можете захотіти оновити клієнта Stripe напряму, додавши інформацію. Зробити це можна методом `updateStripeCustomer`. Цей метод приймає масив [параметрів оновлення клієнта, які підтримує API Stripe](https://stripe.com/docs/api/customers/update):

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### Баланси

Stripe дозволяє кредитувати чи дебетувати «баланс» клієнта. Згодом цей баланс буде зараховано чи списано в нових рахунках. Щоб перевірити загальний баланс клієнта, скористайтеся методом `balance`, доступним на вашій моделі з білінгом. Метод `balance` поверне відформатований рядок з представленням балансу у валюті клієнта:

```php
$balance = $user->balance();
```

Щоб кредитувати баланс клієнта, передайте значення до методу `creditBalance`. За бажанням ви також можете передати опис:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

Передавання значення до методу `debitBalance` дебетує баланс клієнта:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

Метод `applyBalance` створить для клієнта нові транзакції балансу. Ви можете отримати ці записи транзакцій методом `balanceTransactions`, що може бути корисно, щоб надати клієнту журнал зарахувань і списань для перегляду:

```php
// Retrieve all transactions...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // Transaction amount...
    $amount = $transaction->amount(); // $2.31

    // Retrieve the related invoice when available...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### Податкові номери

Cashier пропонує простий спосіб керувати податковими номерами клієнта. Наприклад, метод `taxIds` можна використати, щоб отримати колекцією всі [податкові номери](https://stripe.com/docs/api/customer_tax_ids/object), призначені клієнту:

```php
$taxIds = $user->taxIds();
```

Ви також можете отримати конкретний податковий номер клієнта за його ідентифікатором:

```php
$taxId = $user->findTaxId('txi_belgium');
```

Ви можете створити новий податковий номер, передавши дійсний [тип](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) і значення до методу `createTaxId`:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

Метод `createTaxId` одразу додасть VAT ID до облікового запису клієнта. [Перевірку VAT ID також виконує Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); однак це асинхронний процес. Ви можете отримувати сповіщення про оновлення перевірки, підписавшись на подію вебхука `customer.tax_id.updated` і перевіряючи [параметр `verification` податкового номера](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). Докладніше про обробку вебхуків дивіться в [документації щодо визначення обробників вебхуків](#handling-stripe-webhooks).

Ви можете видалити податковий номер методом `deleteTaxId`:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Синхронізація даних клієнта зі Stripe

Зазвичай, коли користувачі вашого застосунку оновлюють своє ім'я, адресу електронної пошти чи іншу інформацію, яку також зберігає Stripe, вам слід повідомити Stripe про ці оновлення. Так копія інформації у Stripe буде синхронізована з вашим застосунком.

Щоб автоматизувати це, визначте на своїй моделі з білінгом слухача події, який реагує на подію `updated` моделі. Далі в цьому слухачі викличте на моделі метод `syncStripeCustomerDetails`:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * The "booted" method of the model.
 */
protected static function booted(): void
{
    static::updated(queueable(function (User $customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```

Тепер щоразу, коли вашу модель клієнта буде оновлено, її інформація синхронізуватиметься зі Stripe. Для зручності Cashier автоматично синхронізує інформацію про вашого клієнта зі Stripe під час початкового створення клієнта.

Ви можете налаштувати, які колонки використовуються для синхронізації інформації про клієнта зі Stripe, перевизначивши різні методи, які надає Cashier. Наприклад, ви можете перевизначити метод `stripeName`, щоб указати, який атрибут слід вважати «іменем» клієнта, коли Cashier синхронізує інформацію про клієнта зі Stripe:

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

Так само ви можете перевизначити методи `stripeEmail`, `stripePhone` (максимум 20 символів), `stripeAddress` і `stripePreferredLocales`. Ці методи синхронізуватимуть інформацію з відповідними параметрами клієнта під час [оновлення об'єкта клієнта Stripe](https://stripe.com/docs/api/customers/update). Якщо ви хочете повністю контролювати процес синхронізації інформації про клієнта, перевизначте метод `syncStripeCustomerDetails`.

<a name="billing-portal"></a>
### Портал білінгу

Stripe пропонує [простий спосіб налаштувати портал білінгу](https://stripe.com/docs/billing/subscriptions/customer-portal), щоб ваш клієнт міг керувати своєю підпискою, платіжними методами й переглядати історію білінгу. Ви можете перенаправити своїх користувачів до порталу білінгу, викликавши метод `redirectToBillingPortal` на моделі з білінгом з контролера чи маршруту:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

За замовчуванням, коли користувач завершить керування своєю підпискою, він зможе повернутися до маршруту `home` вашого застосунку за посиланням у порталі білінгу Stripe. Ви можете вказати власний URL, на який слід повернути користувача, передавши URL аргументом до методу `redirectToBillingPortal`:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

Якщо ви хочете згенерувати URL до порталу білінгу без створення HTTP-відповіді з перенаправленням, викличте метод `billingPortalUrl`:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## Платіжні методи

<a name="storing-payment-methods"></a>
### Збереження платіжних методів

Щоб створювати підписки чи виконувати «разові» списання через Stripe, вашому застосунку потрібно безпечно збирати платіжні дані від клієнта. Підхід до цього різниться залежно від того, чи плануєте ви зберігати платіжний метод для майбутніх підписок, чи одразу обробити разове списання, тож розглянемо обидва варіанти нижче.

[Payment Element](https://stripe.com/docs/payments/payment-element) від Stripe можна використати для підтримки кількох платіжних методів: карток, Apple Pay, Google Pay та iDEAL.

<a name="payment-element-for-subscriptions"></a>
#### Payment Element для підписок

Спершу створіть Setup Intent і передайте його до свого представлення:

```php
return view('subscribe', [
    'intent' => $user->createSetupIntent()
]);
```

Змонтуйте Payment Element, використовуючи `client_secret` з Setup Intent:

```html
<div id="payment-element"></div>
<button id="submit">Subscribe</button>

<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements({
        clientSecret: '{{ $intent->client_secret }}'
    });

    const paymentElement = elements.create('payment');

    paymentElement.mount('#payment-element');

    document.getElementById('submit').addEventListener('click', async () => {
        const { error } = await stripe.confirmSetup({
            elements,
            confirmParams: {
                return_url: '{{ route("subscription.complete") }}',
            },
        });

        if (error) {
            // Display "error.message" to the user...
        }
    });
</script>
```

Після того як Stripe перенаправить на ваш `return_url`, ID `setup_intent` буде доступний як параметр рядка запиту. Ви можете скористатися цим значенням, щоб отримати платіжний метод і створити підписку:

```php
use Illuminate\Http\Request;

Route::get('/subscription/complete', function (Request $request) {
    $setupIntent = $request->user()->findSetupIntent(
        $request->setup_intent
    );

    $paymentMethod = $setupIntent->payment_method;

    $request->user()
        ->newSubscription('default', 'price_xxx')
        ->create($paymentMethod);

    return redirect('/dashboard');
})->name('subscription.complete');
```

Якщо ви використовуєте Payment Element, щоб оновити платіжний метод клієнта за замовчуванням, а не створити підписку, передайте ідентифікатор платіжного методу до методу [`updateDefaultPaymentMethod`](#updating-the-default-payment-method).

<a name="payment-element-for-single-charges"></a>
#### Payment Element для разових списань

Для разових платежів створіть Payment Intent методом `pay` з Cashier. Зазвичай вам слід зберегти ID Payment Intent у відповідному замовленні вашого застосунку, щоб замовлення можна було знайти після того, як Stripe перенаправить клієнта назад до вашого застосунку. Наведений нижче приклад припускає, що ваш застосунок має модель `Order` з колонками `user_id`, `amount`, `status` і `stripe_payment_intent_id`:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $amount = 1000;

    $payment = $request->user()->pay($amount);

    $order = Order::create([
        'user_id' => $request->user()->id,
        'amount' => $amount,
        'status' => 'pending',
        'stripe_payment_intent_id' => $payment->id,
    ]);

    return view('checkout', [
        'clientSecret' => $payment->client_secret,
        'order' => $order,
    ]);
});
```

Далі змонтуйте Payment Element і підтвердьте платіж:

```html
<div id="payment-element"></div>
<button id="submit">Pay Now</button>

<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements({
        clientSecret: '{{ $clientSecret }}'
    });

    const paymentElement = elements.create('payment');

    paymentElement.mount('#payment-element');

    document.getElementById('submit').addEventListener('click', async () => {
        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: '{{ route("payment.complete") }}',
            },
        });

        if (error) {
            // Display "error.message" to the user...
        }
    });
</script>
```

Після перенаправлення ви можете скористатися параметром рядка запиту `payment_intent`, щоб знайти відповідне замовлення й Payment Intent. Перш ніж виконувати замовлення, вам слід перевірити, що воно належить автентифікованому клієнту, а Payment Intent належить автентифікованому клієнту й успішно завершився:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/payment/complete', function (Request $request) {
    $order = Order::where('user_id', $request->user()->id)
        ->where('stripe_payment_intent_id', $request->payment_intent)
        ->firstOrFail();

    $paymentIntent = $request->user()
        ->stripe()
        ->paymentIntents
        ->retrieve($request->payment_intent);

    if ($paymentIntent->customer === $request->user()->stripe_id &&
        $paymentIntent->status === 'succeeded') {
        $order->update(['status' => 'paid']);

        // Fulfill the order...
    }

    return redirect('/dashboard');
})->name('payment.complete');
```

<a name="retrieving-payment-methods"></a>
### Отримання платіжних методів

Метод `paymentMethods` на екземплярі моделі з білінгом повертає колекцію екземплярів `Laravel\Cashier\PaymentMethod`:

```php
$paymentMethods = $user->paymentMethods();
```

За замовчуванням цей метод поверне платіжні методи всіх типів. Щоб отримати платіжні методи конкретного типу, передайте `type` аргументом до методу:

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

Щоб отримати платіжний метод клієнта за замовчуванням, скористайтеся методом `defaultPaymentMethod`:

```php
$paymentMethod = $user->defaultPaymentMethod();
```

Ви можете отримати конкретний платіжний метод, прикріплений до моделі з білінгом, методом `findPaymentMethod`:

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### Наявність платіжного методу

Щоб визначити, чи має модель з білінгом прикріплений до облікового запису платіжний метод за замовчуванням, викличте метод `hasDefaultPaymentMethod`:

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

Ви можете скористатися методом `hasPaymentMethod`, щоб визначити, чи має модель з білінгом принаймні один прикріплений до облікового запису платіжний метод:

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

Цей метод визначить, чи має модель з білінгом хоч якийсь платіжний метод. Щоб визначити, чи існує для моделі платіжний метод конкретного типу, передайте `type` аргументом до методу:

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### Оновлення платіжного методу за замовчуванням

Метод `updateDefaultPaymentMethod` можна використати, щоб оновити інформацію про платіжний метод клієнта за замовчуванням. Цей метод приймає ідентифікатор платіжного методу Stripe і призначить новий платіжний метод як платіжний метод для білінгу за замовчуванням:

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

Щоб синхронізувати інформацію про ваш платіжний метод за замовчуванням з інформацією про платіжний метод клієнта за замовчуванням у Stripe, скористайтеся методом `updateDefaultPaymentMethodFromStripe`:

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> Платіжний метод клієнта за замовчуванням можна використовувати лише для виставлення рахунків і створення нових підписок. Через обмеження, накладені Stripe, його не можна використовувати для разових списань.

<a name="adding-payment-methods"></a>
### Додавання платіжних методів

Щоб додати новий платіжний метод, викличте метод `addPaymentMethod` на моделі з білінгом, передавши ідентифікатор платіжного методу:

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> Щоб дізнатися, як отримати ідентифікатори платіжних методів, перегляньте [документацію щодо збереження платіжних методів](#storing-payment-methods).

<a name="deleting-payment-methods"></a>
### Видалення платіжних методів

Щоб видалити платіжний метод, викличте метод `delete` на екземплярі `Laravel\Cashier\PaymentMethod`, який хочете видалити:

```php
$paymentMethod->delete();
```

Метод `deletePaymentMethod` видалить конкретний платіжний метод з моделі з білінгом:

```php
$user->deletePaymentMethod('pm_visa');
```

Метод `deletePaymentMethods` видалить усю інформацію про платіжні методи для моделі з білінгом:

```php
$user->deletePaymentMethods();
```

За замовчуванням цей метод видалить платіжні методи всіх типів. Щоб видалити платіжні методи конкретного типу, передайте `type` аргументом до методу:

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> Якщо користувач має активну підписку, ваш застосунок не має дозволяти йому видаляти платіжний метод за замовчуванням.

<a name="subscriptions"></a>
## Підписки

Підписки дають спосіб налаштувати періодичні платежі для ваших клієнтів. Підписки Stripe, якими керує Cashier, підтримують кілька цін підписки, кількості в підписці, пробні періоди тощо.

<a name="creating-subscriptions"></a>
### Створення підписок

Щоб створити підписку, спершу отримайте екземпляр вашої моделі з білінгом, яким зазвичай буде екземпляр `App\Models\User`. Отримавши екземпляр моделі, ви можете скористатися методом `newSubscription`, щоб створити підписку для моделі:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

Першим аргументом методу `newSubscription` має бути внутрішній тип підписки. Якщо ваш застосунок пропонує лише одну підписку, ви можете назвати її `default` чи `primary`. Цей тип підписки призначений лише для внутрішнього використання застосунком і не має показуватися користувачам. Крім того, він не повинен містити пробілів, і його ніколи не слід змінювати після створення підписки. Другий аргумент - конкретна ціна, на яку підписується користувач. Це значення має відповідати ідентифікатору ціни у Stripe.

Метод `create`, який приймає [ідентифікатор платіжного методу Stripe](#storing-payment-methods) чи об'єкт `PaymentMethod` зі Stripe, розпочне підписку, а також оновить вашу базу даних, записавши ID клієнта Stripe для моделі з білінгом та іншу релевантну платіжну інформацію.

> [!WARNING]
> Передавання ідентифікатора платіжного методу безпосередньо до методу `create` підписки також автоматично додасть його до збережених платіжних методів користувача.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### Збір періодичних платежів через рахунки на пошту

Замість збирати періодичні платежі клієнта автоматично, ви можете вказати Stripe надсилати клієнту рахунок на пошту щоразу, коли настає час періодичного платежу. Далі клієнт зможе оплатити рахунок вручну, щойно отримає його. Клієнту не потрібно надавати платіжний метод наперед, коли періодичні платежі збираються через рахунки:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

Час, який клієнт має на оплату рахунка, перш ніж його підписку буде скасовано, визначається опцією `days_until_due`. За замовчуванням це 30 днів; однак за бажанням ви можете вказати для цієї опції конкретне значення:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### Кількості

Якщо ви хочете задати конкретну [кількість](https://stripe.com/docs/billing/subscriptions/quantities) для ціни під час створення підписки, викличте метод `quantity` на білдері підписки перед її створенням:

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### Додаткові деталі

Якщо ви хочете вказати додаткові опції [клієнта](https://stripe.com/docs/api/customers/create) чи [підписки](https://stripe.com/docs/api/subscriptions/create), які підтримує Stripe, передайте їх другим і третім аргументами до методу `create`:

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### Купони

Якщо ви хочете застосувати купон під час створення підписки, скористайтеся методом `withCoupon`:

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

Або ж, якщо ви хочете застосувати [промокод Stripe](https://stripe.com/docs/billing/subscriptions/discounts/codes), скористайтеся методом `withPromotionCode`:

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

Заданий ID промокоду має бути API ID зі Stripe, призначеним промокоду, а не промокодом, який бачить клієнт. Якщо вам потрібно знайти ID промокоду за промокодом, який бачить клієнт, скористайтеся методом `findPromotionCode`:

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

У наведеному вище прикладі повернутий об'єкт `$promotionCode` є екземпляром `Laravel\Cashier\PromotionCode`. Цей клас декорує об'єкт `Stripe\PromotionCode`, що лежить в основі. Ви можете отримати купон, пов'язаний з промокодом, викликавши метод `coupon`:

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

Екземпляр купона дозволяє визначити розмір знижки й те, чи є купон фіксованою знижкою, чи знижкою у відсотках:

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

Ви також можете отримати знижки, які наразі застосовані до клієнта чи підписки:

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

Повернуті екземпляри `Laravel\Cashier\Discount` декорують екземпляр об'єкта `Stripe\Discount`, що лежить в основі. Ви можете отримати купон, пов'язаний із цією знижкою, викликавши метод `coupon`:

```php
$coupon = $subscription->discount()->coupon();
```

Якщо ви хочете застосувати новий купон чи промокод до клієнта чи підписки, зробіть це методами `applyCoupon` чи `applyPromotionCode`:

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

Пам'ятайте: вам слід використовувати API ID зі Stripe, призначений промокоду, а не промокод, який бачить клієнт. До клієнта чи підписки одночасно можна застосувати лише один купон чи промокод.

Докладніше про це дивіться в документації Stripe щодо [купонів](https://stripe.com/docs/billing/subscriptions/coupons) і [промокодів](https://stripe.com/docs/billing/subscriptions/coupons/codes).

<a name="adding-subscriptions"></a>
#### Додавання підписок

Якщо ви хочете додати підписку клієнту, який уже має платіжний метод за замовчуванням, викличте метод `add` на білдері підписки:

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Створення підписок з панелі Stripe

Ви також можете створювати підписки просто з панелі Stripe. У такому разі Cashier синхронізує щойно додані підписки й призначить їм тип `default`. Щоб змінити тип підписки, який призначається створеним у панелі підпискам, [визначте обробники подій вебхуків](#defining-webhook-event-handlers).

Крім того, через панель Stripe можна створити лише один тип підписки. Якщо ваш застосунок пропонує кілька підписок різних типів, через панель Stripe можна додати лише один тип підписки.

Насамкінець вам слід завжди стежити за тим, щоб додавати лише одну активну підписку на кожен тип підписки, який пропонує ваш застосунок. Якщо клієнт має дві підписки `default`, Cashier використовуватиме лише останню додану, навіть попри те, що обидві синхронізуватимуться з базою даних вашого застосунку.

<a name="checking-subscription-status"></a>
### Перевірка стану підписки

Щойно клієнт підписався на ваш застосунок, ви можете легко перевіряти стан його підписки різними зручними методами. По-перше, метод `subscribed` повертає `true`, якщо клієнт має активну підписку, навіть якщо вона наразі в межах пробного періоду. Метод `subscribed` приймає тип підписки першим аргументом:

```php
if ($user->subscribed('default')) {
    // ...
}
```

Метод `subscribed` також чудово підходить для [middleware маршруту](/docs/{{version}}/middleware), дозволяючи фільтрувати доступ до маршрутів і контролерів на основі стану підписки користувача:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

Якщо ви хочете визначити, чи користувач досі в межах пробного періоду, скористайтеся методом `onTrial`. Цей метод може бути корисним, щоб визначити, чи слід показати користувачеві попередження про те, що він досі на пробному періоді:

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

Метод `subscribedToProduct` можна використати, щоб визначити, чи підписаний користувач на певний продукт на основі заданого ідентифікатора продукту Stripe. У Stripe продукти - це набори цін. У цьому прикладі ми визначимо, чи підписка користувача `default` активно підписана на продукт «premium» застосунку. Заданий ідентифікатор продукту Stripe має відповідати одному з ідентифікаторів ваших продуктів у панелі Stripe:

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

Передавши до методу `subscribedToProduct` масив, ви можете визначити, чи підписка користувача `default` активно підписана на продукт «basic» чи «premium» застосунку:

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

Метод `subscribedToPrice` можна використати, щоб визначити, чи відповідає підписка клієнта заданому ID ціни:

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

Метод `recurring` можна використати, щоб визначити, чи має користувач наразі підписку і чи вийшов він уже за межі пробного періоду:

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> Якщо користувач має дві підписки того самого типу, метод `subscription` завжди повертатиме найновішу з них. Наприклад, користувач може мати два записи підписок з типом `default`; однак одна з них може бути старою, простроченою, а інша - поточною, активною. Завжди повертатиметься найновіша підписка, тоді як старіші зберігаються в базі даних для історичного огляду.

<a name="cancelled-subscription-status"></a>
#### Стан скасованої підписки

Щоб визначити, чи був користувач колись активним підписником, але скасував свою підписку, скористайтеся методом `canceled`:

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

Ви також можете визначити, чи скасував користувач підписку, але досі перебуває в «пільговому періоді», доки підписка повністю не спливе. Наприклад, якщо користувач скасує 5 березня підписку, яка спочатку мала спливти 10 березня, він перебуватиме в «пільговому періоді» до 10 березня. Зауважте, що метод `subscribed` протягом цього часу все ще повертає `true`:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

Щоб визначити, чи скасував користувач підписку і чи вийшов він уже за межі «пільгового періоду», скористайтеся методом `ended`:

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### Стани incomplete і past due

Якщо підписка після створення потребує додаткової платіжної дії, її буде позначено як `incomplete`. Стани підписок зберігаються в колонці `stripe_status` таблиці бази даних `subscriptions` у Cashier.

Так само, якщо додаткова платіжна дія потрібна під час зміни цін, підписку буде позначено як `past_due`. Коли ваша підписка в будь-якому з цих станів, вона не буде активною, доки клієнт не підтвердить свій платіж. Визначити, чи має підписка незавершений платіж, можна методом `hasIncompletePayment` на моделі з білінгом чи на екземплярі підписки:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

Коли підписка має незавершений платіж, вам слід направити користувача на сторінку підтвердження платежу в Cashier, передавши ідентифікатор `latestPayment`. Отримати цей ідентифікатор можна методом `latestPayment`, доступним на екземплярі підписки:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

Якщо ви хочете, щоб підписка все ще вважалася активною у стані `past_due` чи `incomplete`, скористайтеся методами `keepPastDueSubscriptionsActive` і `keepIncompleteSubscriptionsActive`, які надає Cashier. Зазвичай ці методи слід викликати в методі `register` вашого `App\Providers\AppServiceProvider`:

```php
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> Коли підписка у стані `incomplete`, її не можна змінити, доки платіж не буде підтверджено. Тому методи `swap` і `updateQuantity` видадуть виняток, коли підписка у стані `incomplete`.

<a name="subscription-scopes"></a>
#### Скопи підписок

Більшість станів підписки також доступні як скопи запитів, тож ви можете легко шукати у своїй базі даних підписки в певному стані:

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

Повний список доступних скопів наведено нижче:

```php
Subscription::query()->active();
Subscription::query()->canceled();
Subscription::query()->ended();
Subscription::query()->incomplete();
Subscription::query()->notCanceled();
Subscription::query()->notOnGracePeriod();
Subscription::query()->notOnTrial();
Subscription::query()->onGracePeriod();
Subscription::query()->onTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
```

<a name="changing-prices"></a>
### Зміна цін

Після того як клієнт підписався на ваш застосунок, він може час від часу хотіти перейти на нову ціну підписки. Щоб перевести клієнта на нову ціну, передайте ідентифікатор ціни Stripe до методу `swap`. Під час зміни цін припускається, що користувач хотів би повторно активувати свою підписку, якщо її було раніше скасовано. Заданий ідентифікатор ціни має відповідати ідентифікатору ціни Stripe, доступному в панелі Stripe:

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

Якщо клієнт на пробному періоді, пробний період буде збережено. Крім того, якщо для підписки існує «кількість», її також буде збережено.

Якщо ви хочете змінити ціни й скасувати будь-який пробний період, на якому наразі перебуває клієнт, викличте метод `skipTrial`:

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

Якщо ви хочете змінити ціни й одразу виставити рахунок клієнту, не чекаючи наступного розрахункового циклу, скористайтеся методом `swapAndInvoice`:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### Пропорційний перерахунок

За замовчуванням Stripe робить пропорційний перерахунок платежів під час зміни цін. Метод `noProrate` можна використати, щоб оновити ціну підписки без пропорційного перерахунку платежів:

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

Докладніше про пропорційний перерахунок підписок дивіться в [документації Stripe](https://stripe.com/docs/billing/subscriptions/prorations).

> [!WARNING]
> Виконання методу `noProrate` перед методом `swapAndInvoice` не вплине на пропорційний перерахунок. Рахунок буде виставлено в будь-якому разі.

<a name="subscription-quantity"></a>
### Кількість у підписці

Іноді на підписки впливає «кількість». Наприклад, застосунок для керування проєктами може стягувати $10 на місяць за проєкт. Ви можете скористатися методами `incrementQuantity` і `decrementQuantity`, щоб легко збільшити чи зменшити кількість у підписці:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription('default')->decrementQuantity(5);
```

Як альтернативу ви можете задати конкретну кількість методом `updateQuantity`:

```php
$user->subscription('default')->updateQuantity(10);
```

Метод `noProrate` можна використати, щоб оновити кількість у підписці без пропорційного перерахунку платежів:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

Докладніше про кількості в підписках дивіться в [документації Stripe](https://stripe.com/docs/subscriptions/quantities).

<a name="quantities-for-subscription-with-multiple-products"></a>
#### Кількості для підписок з кількома продуктами

Якщо ваша підписка є [підпискою з кількома продуктами](#subscriptions-with-multiple-products), вам слід передати ID ціни, кількість якої ви хочете збільшити чи зменшити, другим аргументом методів increment / decrement:

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### Підписки з кількома продуктами

[Підписка з кількома продуктами](https://stripe.com/docs/billing/subscriptions/multiple-products) дозволяє призначити одній підписці кілька продуктів білінгу. Наприклад, уявіть, що ви створюєте застосунок «служби підтримки» з базовою ціною підписки $10 на місяць, але пропонуєте додатковий продукт живого чату за додаткові $15 на місяць. Інформація про підписки з кількома продуктами зберігається в таблиці бази даних `subscription_items` у Cashier.

Ви можете вказати кілька продуктів для певної підписки, передавши масив цін другим аргументом до методу `newSubscription`:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', [
        'price_monthly',
        'price_chat',
    ])->create($request->paymentMethodId);

    // ...
});
```

У наведеному вище прикладі клієнт матиме дві ціни, прив'язані до його підписки `default`. Обидві ціни стягуватимуться у відповідні розрахункові інтервали. За потреби ви можете скористатися методом `quantity`, щоб указати конкретну кількість для кожної ціни:

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

Якщо ви хочете додати ще одну ціну до наявної підписки, викличте метод `addPrice` підписки:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

Наведений вище приклад додасть нову ціну, і клієнту буде виставлено рахунок за неї в наступному розрахунковому циклі. Якщо ви хочете виставити рахунок клієнту негайно, скористайтеся методом `addPriceAndInvoice`:

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

Якщо ви хочете додати ціну з конкретною кількістю, передайте кількість другим аргументом методів `addPrice` чи `addPriceAndInvoice`:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

Ви можете прибрати ціни з підписок методом `removePrice`:

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> Ви не можете прибрати останню ціну в підписці. Натомість вам слід просто скасувати підписку.

<a name="swapping-prices"></a>
#### Зміна цін

Ви також можете змінювати ціни, прив'язані до підписки з кількома продуктами. Наприклад, уявіть, що клієнт має підписку `price_basic` з додатковим продуктом `price_chat`, і ви хочете підвищити клієнта з ціни `price_basic` до `price_pro`:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

Під час виконання наведеного вище прикладу елемент підписки з `price_basic`, що лежить в основі, буде видалено, а той, що з `price_chat`, - збережено. Крім того, буде створено новий елемент підписки для `price_pro`.

Ви також можете вказати опції елемента підписки, передавши до методу `swap` масив пар ключ / значення. Наприклад, вам може знадобитися вказати кількості для цін підписки:

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

Якщо ви хочете змінити одну ціну в підписці, зробіть це методом `swap` на самому елементі підписки. Такий підхід особливо корисний, якщо ви хочете зберегти всі наявні метадані інших цін підписки:

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### Пропорційний перерахунок

За замовчуванням Stripe робитиме пропорційний перерахунок платежів під час додавання чи прибирання цін у підписці з кількома продуктами. Якщо ви хочете скоригувати ціну без пропорційного перерахунку, додайте метод `noProrate` ланцюжком до своєї операції з ціною:

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### Кількості

Якщо ви хочете оновити кількості для окремих цін підписки, зробіть це [наявними методами кількості](#subscription-quantity), передавши ID ціни додатковим аргументом методу:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> Коли підписка має кілька цін, атрибути `stripe_price` і `quantity` на моделі `Subscription` будуть `null`. Щоб звернутися до атрибутів окремих цін, скористайтеся зв'язком `items`, доступним на моделі `Subscription`.

<a name="subscription-items"></a>
#### Елементи підписки

Коли підписка має кілька цін, вона матиме кілька «елементів» підписки, збережених у таблиці `subscription_items` вашої бази даних. Ви можете звернутися до них через зв'язок `items` на підписці:

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

Ви також можете отримати конкретну ціну методом `findItemOrFail`:

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### Кілька підписок

Stripe дозволяє вашим клієнтам мати кілька підписок одночасно. Наприклад, ви можете керувати спортзалом, який пропонує підписку на плавання й підписку на важку атлетику, і кожна підписка може мати різну ціну. Звісно, клієнти мають мати змогу підписатися на один чи обидва плани.

Коли ваш застосунок створює підписки, ви можете передати тип підписки до методу `newSubscription`. Типом може бути будь-який рядок, що представляє тип підписки, яку починає користувач:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

У цьому прикладі ми розпочали для клієнта місячну підписку на плавання. Однак згодом він може захотіти перейти на річну підписку. Коригуючи підписку клієнта, ми можемо просто змінити ціну в підписці `swimming`:

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

Звісно, ви також можете скасувати підписку повністю:

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### Білінг за використанням

[Білінг за використанням](https://stripe.com/docs/billing/subscriptions/metered-billing) дозволяє стягувати з клієнтів плату на основі того, як вони користувалися продуктом протягом розрахункового циклу. Наприклад, ви можете стягувати плату на основі кількості текстових повідомлень чи листів, які вони надсилають щомісяця.

Щоб почати користуватися білінгом за використанням, вам спершу потрібно створити у своїй панелі Stripe новий продукт з [моделлю білінгу за використанням](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) і [лічильником](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). Створивши лічильник, збережіть пов'язане ім'я події та ID лічильника, які знадобляться вам для звітування й отримання використання. Далі скористайтеся методом `meteredPrice`, щоб додати ID лічильної ціни до підписки клієнта:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

Ви також можете розпочати лічильну підписку через [Stripe Checkout](#checkout):

```php
$checkout = Auth::user()
    ->newSubscription('default', [])
    ->meteredPrice('price_metered')
    ->checkout();

return view('your-checkout-view', [
    'checkout' => $checkout,
]);
```

<a name="reporting-usage"></a>
#### Звітування про використання

Коли ваш клієнт користується вашим застосунком, ви звітуватимете про його використання до Stripe, щоб рахунок був точним. Щоб відзвітувати про використання лічильної події, скористайтеся методом `reportMeterEvent` на своїй моделі `Billable`:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

За замовчуванням до розрахункового періоду додається «кількість використання» 1. Як альтернативу ви можете передати конкретний обсяг «використання», який слід додати до використання клієнта за розрахунковий період:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

Щоб отримати зведення подій клієнта для лічильника, скористайтеся методом `meterEventSummaries` екземпляра `Billable`:

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

Докладніше про зведення подій лічильника дивіться в [документації Stripe щодо об'єкта Meter Event Summary](https://docs.stripe.com/api/billing/meter-event_summary/object).

Щоб [перелічити всі лічильники](https://docs.stripe.com/api/billing/meter/list), скористайтеся методом `meters` екземпляра `Billable`:

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### Податки на підписки

> [!WARNING]
> Замість обчислювати податкові ставки вручну, ви можете [автоматично обчислювати податки за допомогою Stripe Tax](#tax-configuration)

Щоб указати податкові ставки, які користувач сплачує за підпискою, реалізуйте на своїй моделі з білінгом метод `taxRates` і поверніть масив з ID податкових ставок Stripe. Ви можете визначити ці податкові ставки [у своїй панелі Stripe](https://dashboard.stripe.com/test/tax-rates):

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

Метод `taxRates` дозволяє застосовувати податкову ставку до кожного клієнта окремо, що може бути корисно для бази користувачів, яка охоплює кілька країн і податкових ставок.

Якщо ви пропонуєте підписки з кількома продуктами, ви можете визначити різні податкові ставки для кожної ціни, реалізувавши на своїй моделі з білінгом метод `priceTaxRates`:

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<string, array<int, string>>
 */
public function priceTaxRates(): array
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```

> [!WARNING]
> Метод `taxRates` застосовується лише до списань за підписками. Якщо ви користуєтеся Cashier для «разових» списань, вам потрібно буде вказати податкову ставку вручну в той момент.

<a name="syncing-tax-rates"></a>
#### Синхронізація податкових ставок

Коли ви змінюєте жорстко задані ID податкових ставок, які повертає метод `taxRates`, податкові налаштування наявних підписок користувача залишаться незмінними. Якщо ви хочете оновити значення податку для наявних підписок новими значеннями `taxRates`, викличте метод `syncTaxRates` на екземплярі підписки користувача:

```php
$user->subscription('default')->syncTaxRates();
```

Це також синхронізує податкові ставки елементів для підписки з кількома продуктами. Якщо ваш застосунок пропонує підписки з кількома продуктами, переконайтеся, що ваша модель з білінгом реалізує метод `priceTaxRates`, [описаний вище](#subscription-taxes).

<a name="tax-exemption"></a>
#### Звільнення від податку

Cashier також пропонує методи `isNotTaxExempt`, `isTaxExempt` і `reverseChargeApplies`, щоб визначити, чи звільнений клієнт від податку. Ці методи викликатимуть API Stripe, щоб визначити статус звільнення клієнта від податку:

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> Ці методи також доступні на будь-якому об'єкті `Laravel\Cashier\Invoice`. Однак, викликані на об'єкті `Invoice`, вони визначатимуть статус звільнення на момент створення рахунка.

<a name="subscription-anchor-date"></a>
### Опорна дата підписки

За замовчуванням опорною датою розрахункового циклу є дата створення підписки або, якщо використовується пробний період, дата його завершення. Якщо ви хочете змінити опорну дату білінгу, скористайтеся методом `anchorBillingCycleOn`:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $anchor = Carbon::parse('first day of next month');

    $request->user()->newSubscription('default', 'price_monthly')
        ->anchorBillingCycleOn($anchor->startOfDay())
        ->create($request->paymentMethodId);

    // ...
});
```

Докладніше про керування розрахунковими циклами підписок дивіться в [документації Stripe щодо розрахункового циклу](https://stripe.com/docs/billing/subscriptions/billing-cycle)

<a name="cancelling-subscriptions"></a>
### Скасування підписок

Щоб скасувати підписку, викличте метод `cancel` на підписці користувача:

```php
$user->subscription('default')->cancel();
```

Коли підписку скасовано, Cashier автоматично встановить колонку `ends_at` у вашій таблиці бази даних `subscriptions`. Ця колонка використовується, щоб знати, коли метод `subscribed` має почати повертати `false`.

Наприклад, якщо клієнт скасує підписку 1 березня, але її завершення було заплановане лише на 5 березня, метод `subscribed` продовжуватиме повертати `true` до 5 березня. Так зроблено тому, що користувачеві зазвичай дозволено користуватися застосунком до кінця його розрахункового циклу.

Визначити, чи користувач скасував підписку, але досі перебуває в «пільговому періоді», можна методом `onGracePeriod`:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

Якщо ви хочете скасувати підписку негайно, викличте метод `cancelNow` на підписці користувача:

```php
$user->subscription('default')->cancelNow();
```

Якщо ви хочете скасувати підписку негайно і виставити рахунок за будь-яке невиставлене лічильне використання чи нові / очікувані позиції пропорційного перерахунку, викличте метод `cancelNowAndInvoice` на підписці користувача:

```php
$user->subscription('default')->cancelNowAndInvoice();
```

Ви також можете скасувати підписку в конкретний момент часу:

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```

Насамкінець вам слід завжди скасовувати підписки користувача, перш ніж видаляти пов'язану модель користувача:

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### Відновлення підписок

Якщо клієнт скасував свою підписку, а ви хочете її відновити, викличте на підписці метод `resume`. Щоб відновити підписку, клієнт має досі перебувати в «пільговому періоді»:

```php
$user->subscription('default')->resume();
```

Якщо клієнт скасує підписку, а потім відновить її до того, як вона повністю спливе, кошти з нього не спишуть одразу. Натомість його підписку буде повторно активовано, і рахунок виставлять за початковим розрахунковим циклом.

<a name="subscription-trials"></a>
## Пробні періоди підписок

<a name="with-payment-method-up-front"></a>
### З платіжним методом наперед

Якщо ви хочете пропонувати клієнтам пробні періоди, водночас збираючи інформацію про платіжний метод наперед, скористайтеся методом `trialDays` під час створення підписок:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

Цей метод встановить дату завершення пробного періоду в записі підписки в базі даних і вкаже Stripe не починати стягувати кошти з клієнта до цієї дати. Використовуючи метод `trialDays`, Cashier перезапише будь-який пробний період за замовчуванням, налаштований для ціни у Stripe.

> [!WARNING]
> Якщо підписку клієнта не буде скасовано до дати завершення пробного періоду, кошти з нього спишуть одразу після його спливання, тож обов'язково повідомляйте своїх користувачів про дату завершення пробного періоду.

Метод `trialUntil` дозволяє передати екземпляр `DateTime`, який вказує, коли пробний період має завершитися:

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```

Визначити, чи користувач у межах пробного періоду, можна методом `onTrial` екземпляра користувача або методом `onTrial` екземпляра підписки. Два наведені нижче приклади рівнозначні:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

Ви можете скористатися методом `endTrial`, щоб негайно завершити пробний період підписки:

```php
$user->subscription('default')->endTrial();
```

Щоб визначити, чи наявний пробний період сплив, скористайтеся методом `hasExpiredTrial`:

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Визначення днів пробного періоду у Stripe / Cashier

Ви можете визначити, скільки днів пробного періоду отримують ваші ціни, у панелі Stripe або завжди передавати їх явно через Cashier. Якщо ви обрали визначати дні пробного періоду для своїх цін у Stripe, майте на увазі, що нові підписки, включно з новими підписками клієнта, який мав підписку в минулому, завжди отримуватимуть пробний період, доки ви явно не викличете метод `skipTrial()`.

<a name="without-payment-method-up-front"></a>
### Без платіжного методу наперед

Якщо ви хочете пропонувати пробні періоди, не збираючи інформацію про платіжний метод користувача наперед, ви можете встановити колонку `trial_ends_at` у записі користувача на бажану дату завершення пробного періоду. Зазвичай це роблять під час реєстрації користувача:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```

> [!WARNING]
> Обов'язково додайте [приведення до дати](/docs/{{version}}/eloquent-mutators#date-casting) для атрибута `trial_ends_at` у визначенні класу вашої моделі з білінгом.

Cashier називає такий тип пробного періоду «загальним пробним періодом», оскільки він не прив'язаний до жодної наявної підписки. Метод `onTrial` на екземплярі моделі з білінгом поверне `true`, якщо поточна дата не перевищує значення `trial_ends_at`:

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

Щойно ви будете готові створити для користувача справжню підписку, скористайтеся методом `newSubscription` як зазвичай:

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

Щоб отримати дату завершення пробного періоду користувача, скористайтеся методом `trialEndsAt`. Цей метод поверне екземпляр дати Carbon, якщо користувач на пробному періоді, або `null`, якщо ні. Ви також можете передати необов'язковий параметр типу підписки, якщо хочете отримати дату завершення пробного періоду для конкретної підписки, відмінної від типової:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

Ви також можете скористатися методом `onGenericTrial`, якщо хочете дізнатися саме те, що користувач перебуває в «загальному» пробному періоді і ще не створив справжньої підписки:

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extending-trials"></a>
### Продовження пробних періодів

Метод `extendTrial` дозволяє продовжити пробний період підписки після її створення. Якщо пробний період уже сплив і з клієнта вже стягують плату за підписку, ви все одно можете запропонувати йому продовжений пробний період. Час, проведений у межах пробного періоду, буде вирахувано з наступного рахунка клієнта:

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// End the trial 7 days from now...
$subscription->extendTrial(
    now()->plus(days: 7)
);

// Add an additional 5 days to the trial...
$subscription->extendTrial(
    $subscription->trial_ends_at->plus(days: 5)
);
```

<a name="handling-stripe-webhooks"></a>
## Обробка вебхуків Stripe

> [!NOTE]
> Ви можете скористатися [Stripe CLI](https://stripe.com/docs/stripe-cli), щоб тестувати вебхуки під час локальної розробки.

Stripe може сповіщати ваш застосунок про різні події через вебхуки. За замовчуванням сервіс-провайдер Cashier автоматично реєструє маршрут, що вказує на контролер вебхуків Cashier. Цей контролер оброблятиме всі вхідні запити вебхуків.

За замовчуванням контролер вебхуків Cashier автоматично оброблятиме скасування підписок із занадто великою кількістю невдалих списань (як визначено у ваших налаштуваннях Stripe), оновлення клієнтів, видалення клієнтів, оновлення підписок і зміни платіжного методу; однак, як ми невдовзі побачимо, ви можете розширити цей контролер, щоб обробляти будь-яку подію вебхука Stripe, яку забажаєте.

Щоб ваш застосунок міг обробляти вебхуки Stripe, обов'язково налаштуйте URL вебхука в панелі керування Stripe. За замовчуванням контролер вебхуків Cashier відповідає за шляхом URL `/stripe/webhook`. Повний список усіх вебхуків, які вам слід увімкнути в панелі керування Stripe:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

Для зручності Cashier містить артизан-команду `cashier:webhook`. Ця команда створить у Stripe вебхук, який слухає всі події, потрібні Cashier:

```shell
php artisan cashier:webhook
```

За замовчуванням створений вебхук вказуватиме на URL, визначений змінною оточення `APP_URL`, і маршрут `cashier.webhook`, що входить до Cashier. Ви можете передати опцію `--url` під час виклику команди, якщо хочете використати інший URL:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

Створений вебхук використовуватиме версію API Stripe, з якою сумісна ваша версія Cashier. Якщо ви хочете використати іншу версію Stripe, передайте опцію `--api-version`:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

Після створення вебхук одразу стане активним. Якщо ви хочете створити вебхук, але залишити його вимкненим, доки не будете готові, передайте опцію `--disabled` під час виклику команди:

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Обов'язково захистіть вхідні запити вебхуків Stripe за допомогою `middleware` [перевірки підпису вебхука](#verifying-webhook-signatures), що входить до Cashier.

<a name="webhooks-csrf-protection"></a>
#### Вебхуки й захист від CSRF

Оскільки вебхуки Stripe мають обходити [захист від CSRF](/docs/{{version}}/csrf) у Laravel, вам слід подбати, щоб Laravel не намагався перевіряти CSRF-токен для вхідних вебхуків Stripe. Щоб досягти цього, виключіть `stripe/*` із захисту від CSRF у файлі `bootstrap/app.php` вашого застосунку:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### Визначення обробників подій вебхуків

Cashier автоматично обробляє скасування підписок за невдалих списань та інші поширені події вебхуків Stripe. Однак, якщо у вас є додаткові події вебхуків, які ви хочете обробляти, ви можете зробити це, слухаючи такі події, які диспетчеризує Cashier:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

Обидві події містять повні дані вебхука Stripe. Наприклад, якщо ви хочете обробити вебхук `invoice.payment_succeeded`, зареєструйте [слухача](/docs/{{version}}/events#defining-listeners), який оброблятиме подію:

```php
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Handle received Stripe webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // Handle the incoming event...
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
### Перевірка підписів вебхуків

Щоб захистити свої вебхуки, ви можете скористатися [підписами вебхуків Stripe](https://stripe.com/docs/webhooks/signatures). Для зручності Cashier автоматично містить `middleware`, який перевіряє, що вхідний запит вебхука Stripe є дійсним.

Щоб увімкнути перевірку вебхуків, переконайтеся, що змінну оточення `STRIPE_WEBHOOK_SECRET` встановлено у файлі `.env` вашого застосунку. `secret` вебхука можна отримати з панелі вашого облікового запису Stripe.

<a name="single-charges"></a>
## Разові списання

<a name="simple-charge"></a>
### Просте списання

Якщо ви хочете зробити разове списання з клієнта за ідентифікатором платіжного методу, скористайтеся методом `charge` на екземплярі моделі з білінгом. Якщо вам потрібно зібрати платіжні дані від клієнта, перш ніж обробляти разове списання, дивіться документацію щодо [Payment Element для разових списань](#payment-element-for-single-charges):

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $payment = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

Метод `charge` приймає масив третім аргументом, що дозволяє передати будь-які опції до створення Payment Intent у Stripe, яке лежить в основі. Докладніше про доступні вам опції під час створення Payment Intent дивіться в [документації Stripe](https://stripe.com/docs/api/payment_intents/create):

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

Ви також можете скористатися методом `charge` без наявного клієнта чи користувача. Для цього викличте метод `charge` на новому екземплярі моделі з білінгом вашого застосунку:

```php
use App\Models\User;

$payment = (new User)->charge(100, $paymentMethod);
```

Метод `charge` видасть виняток, якщо списання не вдасться. Якщо списання успішне, метод поверне екземпляр `Laravel\Cashier\Payment`:

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> Метод `charge` приймає суму платежу в найменшій одиниці валюти, яку використовує ваш застосунок. Наприклад, якщо клієнти платять у доларах США, суми слід вказувати в центах.

<a name="charge-with-invoice"></a>
### Списання з рахунком

Іноді вам може знадобитися зробити разове списання й запропонувати клієнту PDF-рахунок. Метод `invoicePrice` дозволяє зробити саме це. Наприклад, виставмо клієнту рахунок за п'ять нових футболок:

```php
$user->invoicePrice('price_tshirt', 5);
```

Рахунок буде одразу списано з платіжного методу користувача за замовчуванням. Метод `invoicePrice` також приймає масив третім аргументом. Цей масив містить опції білінгу для позиції рахунка. Четвертий аргумент, який приймає метод, - теж масив, що має містити опції білінгу для самого рахунка:

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

Так само як і `invoicePrice`, ви можете скористатися методом `tabPrice`, щоб створити разове списання за кілька позицій (до 250 позицій на рахунок), додавши їх до «рахунку» клієнта, а потім виставивши рахунок. Наприклад, ми можемо виставити клієнту рахунок за п'ять футболок і два кухлі:

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

Як альтернативу ви можете скористатися методом `invoiceFor`, щоб зробити «разове» списання з платіжного методу клієнта за замовчуванням:

```php
$user->invoiceFor('One Time Fee', 500);
```

Хоча метод `invoiceFor` доступний для використання, рекомендується користуватися методами `invoicePrice` і `tabPrice` із заздалегідь визначеними цінами. Так ви матимете доступ до кращої аналітики й даних у своїй панелі Stripe щодо продажів у розрізі продуктів.

> [!WARNING]
> Методи `invoice`, `invoicePrice` та `invoiceFor` створять рахунок Stripe, який повторюватиме невдалі спроби білінгу. Якщо ви не хочете, щоб рахунки повторювали невдалі списання, вам потрібно буде закрити їх через API Stripe після першого невдалого списання.

<a name="creating-payment-intents"></a>
### Створення Payment Intent

Ви можете створити новий payment intent у Stripe, викликавши метод `pay` на екземплярі моделі з білінгом. Виклик цього методу створить payment intent, загорнутий в екземпляр `Laravel\Cashier\Payment`:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

Створивши payment intent, ви можете повернути client secret до фронтенду свого застосунку, щоб користувач міг завершити платіж у своєму браузері. Докладніше про побудову повних платіжних потоків з payment intent у Stripe дивіться в [документації Stripe](https://stripe.com/docs/payments/accept-a-payment?platform=web).

Використовуючи метод `pay`, клієнту будуть доступні платіжні методи за замовчуванням, увімкнені у вашій панелі Stripe. Як альтернативу, якщо ви хочете дозволити лише певні платіжні методи, скористайтеся методом `payWith`:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```

> [!WARNING]
> Методи `pay` і `payWith` приймають суму платежу в найменшій одиниці валюти, яку використовує ваш застосунок. Наприклад, якщо клієнти платять у доларах США, суми слід вказувати в центах.

<a name="refunding-charges"></a>
### Повернення коштів за списаннями

Якщо вам потрібно повернути кошти за платежем Stripe, скористайтеся методом `refund`. Цей метод приймає ID Payment Intent зі Stripe першим аргументом:

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## Рахунки

<a name="retrieving-invoices"></a>
### Отримання рахунків

Ви можете легко отримати масив рахунків моделі з білінгом методом `invoices`. Метод `invoices` повертає колекцію екземплярів `Laravel\Cashier\Invoice`:

```php
$invoices = $user->invoices();
```

Якщо ви хочете включити до результатів очікувані рахунки, скористайтеся методом `invoicesIncludingPending`:

```php
$invoices = $user->invoicesIncludingPending();
```

Ви можете скористатися методом `findInvoice`, щоб отримати конкретний рахунок за його ID:

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### Показ інформації про рахунок

Перелічуючи рахунки клієнта, ви можете скористатися методами рахунка, щоб показати релевантну інформацію про нього. Наприклад, ви можете захотіти перелічити кожен рахунок у таблиці, дозволивши користувачеві легко завантажити будь-який з них:

```blade
<table>
    @foreach ($invoices as $invoice)
        <tr>
            <td>{{ $invoice->date()->toFormattedDateString() }}</td>
            <td>{{ $invoice->total() }}</td>
            <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
        </tr>
    @endforeach
</table>
```

<a name="upcoming-invoices"></a>
### Майбутні рахунки

Щоб отримати майбутній рахунок клієнта, скористайтеся методом `upcomingInvoice`:

```php
$invoice = $user->upcomingInvoice();
```

Так само, якщо клієнт має кілька підписок, ви можете отримати майбутній рахунок для конкретної підписки:

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### Попередній перегляд рахунків за підпискою

За допомогою методу `previewInvoice` ви можете переглянути рахунок перед зміною цін. Це дозволить визначити, як виглядатиме рахунок вашого клієнта після певної зміни цін:

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

Ви можете передати до методу `previewInvoice` масив цін, щоб переглянути рахунки з кількома новими цінами:

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### Генерація PDF-рахунків

Перш ніж генерувати PDF-рахунки, вам слід встановити через Composer бібліотеку Dompdf - рендерер рахунків за замовчуванням у Cashier:

```shell
composer require dompdf/dompdf
```

З маршруту чи контролера ви можете скористатися методом `downloadInvoice`, щоб згенерувати PDF-завантаження певного рахунка. Цей метод автоматично згенерує належну HTTP-відповідь, потрібну для завантаження рахунка:

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

За замовчуванням усі дані в рахунку беруться з даних клієнта й рахунка, збережених у Stripe. Ім'я файлу базується на значенні вашої конфігурації `app.name`. Однак ви можете змінити частину цих даних, передавши масив другим аргументом до методу `downloadInvoice`. Цей масив дозволяє налаштувати інформацію на кшталт деталей вашої компанії та продукту:

```php
return $request->user()->downloadInvoice($invoiceId, [
    'vendor' => 'Your Company',
    'product' => 'Your Product',
    'street' => 'Main Str. 1',
    'location' => '2000 Antwerp, Belgium',
    'phone' => '+32 499 00 00 00',
    'email' => 'info@example.com',
    'url' => 'https://example.com',
    'vendorVat' => 'BE123456789',
]);
```

Метод `downloadInvoice` також дозволяє задати власне ім'я файлу третім аргументом. До цього імені автоматично додасться суфікс `.pdf`:

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### Власний рендерер рахунків

Cashier також дозволяє використовувати власний рендерер рахунків. За замовчуванням Cashier використовує реалізацію `DompdfInvoiceRenderer`, яка застосовує PHP-бібліотеку [dompdf](https://github.com/dompdf/dompdf) для генерації рахунків Cashier. Однак ви можете використати будь-який рендерер, реалізувавши інтерфейс `Laravel\Cashier\Contracts\InvoiceRenderer`. Наприклад, ви можете захотіти рендерити PDF-рахунок через API-виклик до стороннього сервісу рендерингу PDF:

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Render the given invoice and return the raw PDF bytes.
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

Щойно ви реалізували контракт рендерера рахунків, вам слід оновити значення конфігурації `cashier.invoices.renderer` у конфігураційному файлі `config/cashier.php` вашого застосунку. Це значення має бути іменем класу вашої власної реалізації рендерера.

<a name="checkout"></a>
## Checkout

Cashier Stripe також підтримує [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout знімає біль від створення власних сторінок для приймання платежів, надаючи готову, розміщену сторінку оплати.

Наведена нижче документація містить інформацію про те, як почати користуватися Stripe Checkout з Cashier. Щоб дізнатися більше про Stripe Checkout, вам також варто переглянути [власну документацію Stripe щодо Checkout](https://stripe.com/docs/payments/checkout).

<a name="product-checkouts"></a>
### Оформлення продуктів

Ви можете виконати оформлення для наявного продукту, створеного у вашій панелі Stripe, методом `checkout` на моделі з білінгом. Метод `checkout` ініціює нову сесію Stripe Checkout. За замовчуванням від вас вимагається передати Stripe Price ID:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

За потреби ви також можете вказати кількість продукту:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

Коли клієнт відвідає цей маршрут, його буде перенаправлено на сторінку Checkout від Stripe. За замовчуванням, коли користувач успішно завершує чи скасовує покупку, його буде перенаправлено до маршруту `home` вашого застосунку, але ви можете вказати власні URL зворотного виклику опціями `success_url` і `cancel_url`:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

Визначаючи опцію оформлення `success_url`, ви можете вказати Stripe додавати ID сесії оформлення як параметр рядка запиту під час виклику вашого URL. Для цього додайте буквальний рядок `{CHECKOUT_SESSION_ID}` до рядка запиту `success_url`. Stripe замінить цей плейсхолдер фактичним ID сесії оформлення:

```php
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
    ]);
});

Route::get('/checkout-success', function (Request $request) {
    $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

    return view('checkout.success', ['checkoutSession' => $checkoutSession]);
})->name('checkout-success');
```

<a name="checkout-promotion-codes"></a>
#### Промокоди

За замовчуванням Stripe Checkout не дозволяє [промокоди, які активує користувач](https://stripe.com/docs/billing/subscriptions/discounts/codes). На щастя, увімкнути їх для вашої сторінки Checkout нескладно. Для цього викличте метод `allowPromotionCodes`:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### Оформлення разових списань

Ви також можете виконати просте списання за спонтанний продукт, не створений у вашій панелі Stripe. Для цього скористайтеся методом `checkoutCharge` на моделі з білінгом і передайте йому суму до списання, назву продукту й необов'язкову кількість. Коли клієнт відвідає цей маршрут, його буде перенаправлено на сторінку Checkout від Stripe:

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> Використовуючи метод `checkoutCharge`, Stripe завжди створюватиме новий продукт і ціну у вашій панелі Stripe. Тому ми рекомендуємо створювати продукти заздалегідь у панелі Stripe і використовувати натомість метод `checkout`.

<a name="subscription-checkouts"></a>
### Оформлення підписок

> [!WARNING]
> Використання Stripe Checkout для підписок вимагає увімкнути вебхук `customer.subscription.created` у вашій панелі Stripe. Цей вебхук створить запис підписки у вашій базі даних і збереже всі релевантні елементи підписки.

Ви також можете скористатися Stripe Checkout, щоб ініціювати підписки. Визначивши свою підписку методами білдера підписок у Cashier, викличте метод `checkout`. Коли клієнт відвідає цей маршрут, його буде перенаправлено на сторінку Checkout від Stripe:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

Так само як і з оформленням продуктів, ви можете налаштувати URL успіху та скасування:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

Звісно, ви також можете увімкнути промокоди для оформлення підписок:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!WARNING]
> На жаль, Stripe Checkout не підтримує всі опції білінгу підписок під час їх започаткування. Використання методу `anchorBillingCycleOn` на білдері підписок, налаштування поведінки пропорційного перерахунку чи поведінки платежу не матиме жодного ефекту під час сесій Stripe Checkout. Перегляньте [документацію API Stripe Checkout Session](https://stripe.com/docs/api/checkout/sessions/create), щоб дізнатися, які параметри доступні.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout і пробні періоди

Звісно, ви можете визначити пробний період, створюючи підписку, яку буде завершено через Stripe Checkout:

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

Однак пробний період має тривати щонайменше 48 годин - це мінімальний час пробного періоду, який підтримує Stripe Checkout.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### Підписки й вебхуки

Пам'ятайте: Stripe і Cashier оновлюють стани підписок через вебхуки, тож існує ймовірність, що підписка ще не буде активною, коли клієнт повернеться до застосунку після введення платіжних даних. Щоб обробити цей сценарій, ви можете захотіти показати повідомлення, яке інформує користувача, що його платіж чи підписка в обробці.

<a name="collecting-tax-ids"></a>
### Збір податкових номерів

Checkout також підтримує збір податкового номера клієнта. Щоб увімкнути це для сесії оформлення, викличте метод `collectTaxIds` під час її створення:

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

Коли цей метод викликано, клієнту стане доступним новий чекбокс, який дозволяє вказати, що він купує як компанія. Якщо так, він матиме змогу надати свій податковий номер.

> [!WARNING]
> Якщо ви вже налаштували [автоматичний збір податків](#tax-configuration) у сервіс-провайдері свого застосунку, ця можливість буде увімкнена автоматично, і викликати метод `collectTaxIds` не потрібно.

<a name="guest-checkouts"></a>
### Гостьове оформлення

За допомогою методу `Checkout::guest` ви можете ініціювати сесії оформлення для гостей вашого застосунку, які не мають «облікового запису»:

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()->create('price_tshirt', [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

Так само як і під час створення сесій оформлення для наявних користувачів, ви можете скористатися додатковими методами, доступними на екземплярі `Laravel\Cashier\CheckoutBuilder`, щоб налаштувати гостьову сесію оформлення:

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()
        ->withPromotionCode('promo-code')
        ->create('price_tshirt', [
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

Після завершення гостьового оформлення Stripe може надіслати подію вебхука `checkout.session.completed`, тож обов'язково [налаштуйте свій вебхук Stripe](https://dashboard.stripe.com/webhooks), щоб ця подія справді надсилалася до вашого застосунку. Щойно вебхук увімкнено в панелі Stripe, ви можете [обробити його за допомогою Cashier](#handling-stripe-webhooks). Об'єкт у даних вебхука буде [об'єктом оформлення](https://stripe.com/docs/api/checkout/sessions/object), який ви можете оглянути, щоб виконати замовлення свого клієнта.

<a name="handling-failed-payments"></a>
## Обробка невдалих платежів

Іноді платежі за підписками чи разові списання можуть не вдатися. Коли це стається, Cashier видасть виняток `Laravel\Cashier\Exceptions\IncompletePayment`, який повідомляє вас про це. Перехопивши цей виняток, ви маєте два варіанти дій.

По-перше, ви можете перенаправити клієнта на спеціальну сторінку підтвердження платежу, що входить до Cashier. Ця сторінка вже має пов'язаний іменований маршрут, зареєстрований через сервіс-провайдер Cashier. Тож ви можете перехопити виняток `IncompletePayment` і перенаправити користувача на сторінку підтвердження платежу:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $subscription = $user->newSubscription('default', 'price_monthly')
        ->create($paymentMethod);
} catch (IncompletePayment $exception) {
    return redirect()->route(
        'cashier.payment',
        [$exception->payment->id, 'redirect' => route('home')]
    );
}
```

На сторінці підтвердження платежу клієнту буде запропоновано ввести дані своєї картки ще раз і виконати будь-які додаткові дії, потрібні Stripe, як-от підтвердження «3D Secure». Після підтвердження платежу користувача буде перенаправлено на URL, указаний у параметрі `redirect` вище. Під час перенаправлення до URL буде додано змінні рядка запиту `message` (рядок) і `success` (ціле число). Сторінка оплати наразі підтримує такі типи платіжних методів:

<div class="content-list" markdown="1">

- Credit Cards
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

</div>

Як альтернативу ви можете дозволити Stripe обробляти підтвердження платежу за вас. У цьому разі замість перенаправлення на сторінку підтвердження платежу ви можете [налаштувати автоматичні листи білінгу Stripe](https://dashboard.stripe.com/account/billing/automatic) у своїй панелі Stripe. Однак, якщо виняток `IncompletePayment` перехоплено, вам усе одно слід повідомити користувача, що він отримає лист з подальшими інструкціями щодо підтвердження платежу.

Платіжні винятки можуть видаватися такими методами: `charge`, `invoiceFor` та `invoice` на моделях, що використовують трейт `Billable`. Працюючи з підписками, метод `create` на `SubscriptionBuilder`, а також методи `incrementAndInvoice` і `swapAndInvoice` на моделях `Subscription` і `SubscriptionItem` можуть видавати винятки незавершеного платежу.

Визначити, чи має наявна підписка незавершений платіж, можна методом `hasIncompletePayment` на моделі з білінгом чи на екземплярі підписки:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

Ви можете з'ясувати конкретний стан незавершеного платежу, оглянувши властивість `payment` на екземплярі винятку:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // Get the payment intent status...
    $exception->payment->status;

    // Check specific conditions...
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
### Підтвердження платежів

Деякі платіжні методи потребують додаткових даних для підтвердження платежів. Наприклад, платіжні методи SEPA потребують додаткових даних «mandate» під час процесу оплати. Ви можете передати ці дані до Cashier методом `withPaymentConfirmationOptions`:

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

Ви можете переглянути [документацію API Stripe](https://stripe.com/docs/api/payment_intents/confirm), щоб побачити всі опції, які приймаються під час підтвердження платежів.

<a name="strong-customer-authentication"></a>
## Strong Customer Authentication

Якщо ваш бізнес чи хтось із ваших клієнтів базується в Європі, вам потрібно дотримуватися правил Strong Customer Authentication (SCA) від ЄС. Ці правила запровадив Європейський Союз у вересні 2019 року, щоб запобігти платіжному шахрайству. На щастя, Stripe і Cashier готові до створення застосунків, сумісних із SCA.

> [!WARNING]
> Перш ніж почати, перегляньте [посібник Stripe щодо PSD2 і SCA](https://stripe.com/guides/strong-customer-authentication), а також їхню [документацію щодо нових API SCA](https://stripe.com/docs/strong-customer-authentication).

<a name="payments-requiring-additional-confirmation"></a>
### Платежі, що потребують додаткового підтвердження

Правила SCA часто вимагають додаткової перевірки для підтвердження й обробки платежу. Коли це стається, Cashier видасть виняток `Laravel\Cashier\Exceptions\IncompletePayment`, який повідомляє вас, що потрібна додаткова перевірка. Докладніше про обробку цих винятків дивіться в документації щодо [обробки невдалих платежів](#handling-failed-payments).

Екрани підтвердження платежу, які показують Stripe чи Cashier, можуть бути адаптовані до платіжного потоку конкретного банку чи емітента картки і можуть містити додаткове підтвердження картки, тимчасове невелике списання, окрему автентифікацію пристрою чи інші форми перевірки.

<a name="incomplete-and-past-due-state"></a>
#### Стани incomplete і past due

Коли платіж потребує додаткового підтвердження, підписка залишатиметься у стані `incomplete` чи `past_due`, як указано в її колонці бази даних `stripe_status`. Cashier автоматично активує підписку клієнта, щойно підтвердження платежу буде завершено, а ваш застосунок отримає від Stripe сповіщення про це через вебхук.

Докладніше про стани `incomplete` і `past_due` дивіться в [нашій додатковій документації щодо цих станів](#incomplete-and-past-due-status).

<a name="off-session-payment-notifications"></a>
### Сповіщення про позасесійні платежі

Оскільки правила SCA вимагають від клієнтів час від часу підтверджувати свої платіжні дані навіть тоді, коли їхня підписка активна, Cashier може надіслати клієнту сповіщення, коли потрібне позасесійне підтвердження платежу. Наприклад, це може статися під час поновлення підписки. Сповіщення про платіж у Cashier можна увімкнути, встановивши змінну оточення `CASHIER_PAYMENT_NOTIFICATION` у клас сповіщення. За замовчуванням це сповіщення вимкнено. Звісно, Cashier містить клас сповіщення, який ви можете використати для цього, але за бажанням ви можете надати власний клас сповіщення:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

Щоб сповіщення про позасесійне підтвердження платежу доставлялися, переконайтеся, що [вебхуки Stripe налаштовано](#handling-stripe-webhooks) для вашого застосунку і що вебхук `invoice.payment_action_required` увімкнено у вашій панелі Stripe. Крім того, ваша модель `Billable` має також використовувати трейт `Illuminate\Notifications\Notifiable` з Laravel.

> [!WARNING]
> Сповіщення надсилатимуться навіть тоді, коли клієнти вручну роблять платіж, що потребує додаткового підтвердження. На жаль, Stripe не може знати, що платіж було зроблено вручну чи «поза сесією». Але клієнт просто побачить повідомлення «Payment Successful», якщо відвідає сторінку оплати після того, як уже підтвердив свій платіж. Клієнту не дозволять випадково підтвердити той самий платіж двічі й отримати випадкове друге списання.

<a name="stripe-sdk"></a>
## Stripe SDK

Багато об'єктів Cashier є обгортками навколо об'єктів Stripe SDK. Якщо ви хочете працювати з об'єктами Stripe напряму, ви можете зручно отримати їх методом `asStripe`:

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

Ви також можете скористатися методом `updateStripeSubscription`, щоб оновити підписку Stripe напряму:

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

Ви можете викликати метод `stripe` на класі `Cashier`, якщо хочете використати клієнт `Stripe\StripeClient` напряму. Наприклад, цим методом можна звернутися до екземпляра `StripeClient` і отримати список цін зі свого облікового запису Stripe:

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## Тестування

Тестуючи застосунок, що використовує Cashier, ви можете мокати фактичні HTTP-запити до API Stripe; однак це вимагатиме від вас частково перереалізувати власну поведінку Cashier. Тому ми рекомендуємо дозволити вашим тестам звертатися до справжнього API Stripe. Хоча це повільніше, воно дає більше впевненості, що ваш застосунок працює як очікується, а будь-які повільні тести можна винести до окремої тестової групи Pest / PHPUnit.

Тестуючи, пам'ятайте, що сам Cashier уже має чудовий набір тестів, тож вам слід зосередитися лише на тестуванні потоку підписок і платежів вашого власного застосунку, а не кожної поведінки Cashier, що лежить в основі.

Для початку додайте **тестову** версію свого секрету Stripe до файлу `phpunit.xml`:

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

Тепер щоразу, коли ви взаємодіятимете з Cashier під час тестування, він надсилатиме справжні API-запити до вашого тестового середовища Stripe. Для зручності вам слід заздалегідь наповнити свій тестовий обліковий запис Stripe підписками / цінами, які ви можете використовувати під час тестування.

> [!NOTE]
> Щоб протестувати різноманітні сценарії білінгу, як-от відмови й збої кредитних карток, ви можете скористатися широким набором [тестових номерів карток і токенів](https://stripe.com/docs/testing), які надає Stripe.
