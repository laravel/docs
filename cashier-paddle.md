---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Cashier (Paddle)

- [Вступ](#introduction)
- [Оновлення Cashier](#upgrading-cashier)
- [Встановлення](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [Конфігурація](#configuration)
    - [Модель з білінгом](#billable-model)
    - [API-ключі](#api-keys)
    - [Paddle JS](#paddle-js)
    - [Конфігурація валюти](#currency-configuration)
    - [Заміна моделей за замовчуванням](#overriding-default-models)
- [Швидкий старт](#quickstart)
    - [Продаж продуктів](#quickstart-selling-products)
    - [Продаж підписок](#quickstart-selling-subscriptions)
- [Сесії оформлення](#checkout-sessions)
    - [Overlay-оформлення](#overlay-checkout)
    - [Вбудоване оформлення](#inline-checkout)
    - [Гостьове оформлення](#guest-checkouts)
- [Попередній перегляд цін](#price-previews)
    - [Попередній перегляд цін для клієнта](#customer-price-previews)
    - [Знижки](#price-discounts)
- [Клієнти](#customers)
    - [Значення за замовчуванням для клієнта](#customer-defaults)
    - [Отримання клієнтів](#retrieving-customers)
    - [Створення клієнтів](#creating-customers)
- [Підписки](#subscriptions)
    - [Створення підписок](#creating-subscriptions)
    - [Перевірка стану підписки](#checking-subscription-status)
    - [Разові списання за підпискою](#subscription-single-charges)
    - [Оновлення платіжної інформації](#updating-payment-information)
    - [Зміна планів](#changing-plans)
    - [Кількість у підписці](#subscription-quantity)
    - [Підписки з кількома продуктами](#subscriptions-with-multiple-products)
    - [Кілька підписок](#multiple-subscriptions)
    - [Призупинення підписок](#pausing-subscriptions)
    - [Скасування підписок](#canceling-subscriptions)
- [Пробні періоди підписок](#subscription-trials)
    - [З платіжним методом наперед](#with-payment-method-up-front)
    - [Без платіжного методу наперед](#without-payment-method-up-front)
    - [Продовження чи активація пробного періоду](#extend-or-activate-a-trial)
- [Обробка вебхуків Paddle](#handling-paddle-webhooks)
    - [Визначення обробників подій вебхуків](#defining-webhook-event-handlers)
    - [Перевірка підписів вебхуків](#verifying-webhook-signatures)
- [Разові списання](#single-charges)
    - [Списання за продукти](#charging-for-products)
    - [Повернення коштів за транзакціями](#refunding-transactions)
    - [Кредитування транзакцій](#crediting-transactions)
- [Транзакції](#transactions)
    - [Минулі та майбутні платежі](#past-and-upcoming-payments)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

> [!WARNING]
> Ця документація стосується інтеграції Cashier Paddle 2.x з Paddle Billing. Якщо ви досі користуєтеся Paddle Classic, вам слід використовувати [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x).

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) дає виразний, плавний інтерфейс до сервісів білінгу підписок [Paddle](https://paddle.com). Він бере на себе майже весь шаблонний код білінгу підписок, якого ви так боїтеся. Окрім базового керування підписками, Cashier уміє: змінювати підписки, працювати з «кількостями» в підписках, призупиняти підписки, обробляти пільгові періоди після скасування тощо.

Перш ніж заглиблюватися в Cashier Paddle, радимо також переглянути [концептуальні посібники](https://developer.paddle.com/concepts/overview) та [документацію API](https://developer.paddle.com/api-reference/overview) від Paddle.

<a name="upgrading-cashier"></a>
## Оновлення Cashier

Оновлюючись до нової версії Cashier, важливо уважно переглянути [посібник з оновлення](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md).

<a name="installation"></a>
## Встановлення

Спершу встановіть пакет Cashier для Paddle за допомогою менеджера пакетів Composer:

```shell
composer require laravel/cashier-paddle
```

Далі вам слід опублікувати файли міграцій Cashier артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

Потім виконайте міграції бази даних вашого застосунку. Міграції Cashier створять нову таблицю `customers`. Крім того, буде створено нові таблиці `subscriptions` і `subscription_items` для зберігання всіх підписок ваших клієнтів. Насамкінець буде створено нову таблицю `transactions` для зберігання всіх транзакцій Paddle, пов'язаних з вашими клієнтами:

```shell
php artisan migrate
```

> [!WARNING]
> Щоб Cashier належно обробляв усі події Paddle, не забудьте [налаштувати обробку вебхуків Cashier](#handling-paddle-webhooks).

<a name="paddle-sandbox"></a>
### Paddle Sandbox

Під час локальної розробки та на staging вам слід [зареєструвати обліковий запис Paddle Sandbox](https://sandbox-login.paddle.com/signup). Цей обліковий запис дасть вам пісочницю для тестування й розробки застосунків без реальних платежів. Ви можете скористатися [тестовими номерами карток](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method) Paddle, щоб змоделювати різні платіжні сценарії.

Використовуючи середовище Paddle Sandbox, вам слід встановити змінну оточення `PADDLE_SANDBOX` у `true` у файлі `.env` вашого застосунку:

```ini
PADDLE_SANDBOX=true
```

Завершивши розробку застосунку, ви можете [подати заявку на обліковий запис вендора Paddle](https://paddle.com). Перш ніж ваш застосунок потрапить у продакшен, Paddle має схвалити домен вашого застосунку.

<a name="configuration"></a>
## Конфігурація

<a name="billable-model"></a>
### Модель з білінгом

Перш ніж користуватися Cashier, вам потрібно додати трейт `Billable` до визначення вашої моделі користувача. Цей трейт надає різні методи, що дозволяють виконувати типові завдання білінгу, як-от створення підписок і оновлення інформації про платіжний метод:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Якщо у вас є сутності з білінгом, які не є користувачами, ви можете додати трейт і до цих класів:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API-ключі

Далі вам слід налаштувати свої ключі Paddle у файлі `.env` вашого застосунку. Отримати API-ключі Paddle можна з панелі керування Paddle:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

Змінну оточення `PADDLE_SANDBOX` слід встановити в `true`, коли ви використовуєте [середовище Sandbox від Paddle](#paddle-sandbox). Змінну `PADDLE_SANDBOX` слід встановити в `false`, якщо ви розгортаєте застосунок у продакшені й використовуєте живе вендорське середовище Paddle.

`PADDLE_RETAIN_KEY` необов'язковий, і його слід встановлювати, лише якщо ви використовуєте Paddle із [Retain](https://developer.paddle.com/concepts/retain/overview).

<a name="paddle-js"></a>
### Paddle JS

Paddle покладається на власну JavaScript-бібліотеку, щоб запустити віджет оформлення Paddle. Завантажити цю бібліотеку можна, розмістивши Blade-директиву `@paddleJS` безпосередньо перед закривальним тегом `</head>` у макеті вашого застосунку:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### Конфігурація валюти

Ви можете вказати локаль, яка використовуватиметься для форматування грошових значень для показу в рахунках. Внутрішньо Cashier використовує [клас PHP `NumberFormatter`](https://www.php.net/manual/en/class.numberformatter.php), щоб задати локаль валюти:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> Щоб використовувати локалі, відмінні від `en`, переконайтеся, що PHP-розширення `ext-intl` встановлено й налаштовано на вашому сервері.

<a name="overriding-default-models"></a>
### Заміна моделей за замовчуванням

Ви можете розширювати моделі, які Cashier використовує внутрішньо, визначивши власну модель і розширивши відповідну модель Cashier:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

Визначивши свою модель, ви можете вказати Cashier використовувати вашу власну модель через клас `Laravel\Paddle\Cashier`. Зазвичай повідомляти Cashier про ваші власні моделі слід у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useTransactionModel(Transaction::class);
}
```

<a name="quickstart"></a>
## Швидкий старт

<a name="quickstart-selling-products"></a>
### Продаж продуктів

> [!NOTE]
> Перш ніж користуватися Paddle Checkout, вам слід визначити продукти з фіксованими цінами у своїй панелі Paddle. Крім того, вам слід [налаштувати обробку вебхуків Paddle](#handling-paddle-webhooks).

Пропонувати білінг продуктів і підписок через ваш застосунок може здаватися страшним. Однак завдяки Cashier та [Checkout Overlay від Paddle](https://developer.paddle.com/concepts/sell/overlay-checkout) ви можете легко побудувати сучасні, надійні платіжні інтеграції.

Щоб списувати кошти з клієнтів за неперіодичні продукти з разовим списанням, ми скористаємося Cashier для списання через Checkout Overlay від Paddle, де клієнти нададуть свої платіжні дані й підтвердять покупку. Щойно платіж буде здійснено через Checkout Overlay, клієнта буде перенаправлено на обрану вами URL-адресу успіху у вашому застосунку:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

Як бачите в наведеному вище прикладі, ми скористаємося наданим Cashier методом `checkout`, щоб створити об'єкт оформлення й показати клієнту Checkout Overlay від Paddle для заданого «ідентифікатора ціни». У Paddle «ціни» - це [визначені ціни для конкретних продуктів](https://developer.paddle.com/build/products/create-products-prices).

За потреби метод `checkout` автоматично створить клієнта в Paddle і зв'яже цей запис клієнта Paddle з відповідним користувачем у базі даних вашого застосунку. Після завершення сесії оформлення клієнта буде перенаправлено на спеціальну сторінку успіху, де ви можете показати йому інформаційне повідомлення.

У представленні `buy` ми додамо кнопку для показу Checkout Overlay. Blade-компонент `paddle-button` входить до Cashier Paddle; однак ви також можете [відрендерити overlay-оформлення вручну](#manually-rendering-an-overlay-checkout):

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Передавання метаданих до Paddle Checkout

Продаючи продукти, зазвичай відстежують завершені замовлення й куплені продукти через моделі `Cart` і `Order`, визначені у вашому власному застосунку. Перенаправляючи клієнтів до Checkout Overlay від Paddle для завершення покупки, вам може знадобитися передати наявний ідентифікатор замовлення, щоб пов'язати завершену покупку з відповідним замовленням, коли клієнта буде перенаправлено назад до вашого застосунку.

Щоб досягти цього, передайте до методу `checkout` масив власних даних. Уявімо, що в нашому застосунку створюється незавершене замовлення `Order`, коли користувач починає процес оформлення. Пам'ятайте: моделі `Cart` і `Order` у цьому прикладі є ілюстративними і не надаються Cashier. Ви можете реалізувати ці концепції відповідно до потреб власного застосунку:

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

    $checkout = $request->user()->checkout($order->price_ids)
        ->customData(['order_id' => $order->id]);

    return view('billing', ['checkout' => $checkout]);
})->name('checkout');
```

Як бачите в наведеному вище прикладі, коли користувач починає процес оформлення, ми передаємо до методу `checkout` усі пов'язані з кошиком / замовленням ідентифікатори цін Paddle. Звісно, ваш застосунок відповідає за прив'язку цих позицій до «кошика» чи замовлення, коли клієнт їх додає. Ми також передаємо ID замовлення до Checkout Overlay від Paddle методом `customData`.

Звісно, ви, найімовірніше, захочете позначити замовлення як «завершене», щойно клієнт завершить процес оформлення. Щоб досягти цього, ви можете слухати вебхуки, які надсилає Paddle і які Cashier здіймає у вигляді подій, і зберігати інформацію про замовлення у своїй базі даних.

Для початку слухайте подію `TransactionCompleted`, яку диспетчеризує Cashier. Зазвичай реєструвати слухача події слід у методі `boot` `AppServiceProvider` вашого застосунку:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

У цьому прикладі слухач `CompleteOrder` міг би виглядати так:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * Handle the incoming Cashier webhook event.
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

Докладніше про [дані, які містить подія `transaction.completed`](https://developer.paddle.com/webhooks/transactions/transaction-completed), дивіться в документації Paddle.

<a name="quickstart-selling-subscriptions"></a>
### Продаж підписок

> [!NOTE]
> Перш ніж користуватися Paddle Checkout, вам слід визначити продукти з фіксованими цінами у своїй панелі Paddle. Крім того, вам слід [налаштувати обробку вебхуків Paddle](#handling-paddle-webhooks).

Пропонувати білінг продуктів і підписок через ваш застосунок може здаватися страшним. Однак завдяки Cashier та [Checkout Overlay від Paddle](https://developer.paddle.com/concepts/sell/overlay-checkout) ви можете легко побудувати сучасні, надійні платіжні інтеграції.

Щоб дізнатися, як продавати підписки за допомогою Cashier і Checkout Overlay від Paddle, розгляньмо простий сценарій сервісу підписок з базовим місячним (`price_basic_monthly`) і річним (`price_basic_yearly`) планом. Ці дві ціни можна згрупувати під продуктом «Basic» (`pro_basic`) у нашій панелі Paddle. Крім того, наш сервіс підписок може пропонувати план «Expert» як `pro_expert`.

Спершу з'ясуймо, як клієнт може підписатися на наші сервіси. Звісно, можна уявити, що клієнт натисне кнопку «subscribe» для плану Basic на сторінці цін нашого застосунку. Ця кнопка викличе Checkout Overlay від Paddle для обраного плану. Для початку ініціюймо сесію оформлення методом `checkout`:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

У представленні `subscribe` ми додамо кнопку для показу Checkout Overlay. Blade-компонент `paddle-button` входить до Cashier Paddle; однак ви також можете [відрендерити overlay-оформлення вручну](#manually-rendering-an-overlay-checkout):

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

Тепер, коли натиснуто кнопку Subscribe, клієнт зможе ввести свої платіжні дані й розпочати підписку. Щоб знати, коли підписка справді почалася (оскільки деяким платіжним методам потрібно кілька секунд на обробку), вам також слід [налаштувати обробку вебхуків Cashier](#handling-paddle-webhooks).

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
            return redirect('/subscribe');
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

Звісно, клієнти можуть захотіти змінити свій план підписки на інший продукт чи «рівень». У нашому прикладі вище ми хотіли б дозволити клієнту змінити план з місячної підписки на річну. Для цього вам потрібно буде реалізувати щось на кшталт кнопки, яка веде до наведеного нижче маршруту:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

Окрім зміни планів, вам також потрібно буде дозволити клієнтам скасовувати підписку. Як і зі зміною планів, надайте кнопку, що веде до такого маршруту:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

І тепер вашу підписку буде скасовано наприкінці її розрахункового періоду.

> [!NOTE]
> Доки ви налаштували обробку вебхуків Cashier, Cashier автоматично підтримуватиме пов'язані з ним таблиці бази даних вашого застосунку синхронізованими, аналізуючи вхідні вебхуки від Paddle. Так, наприклад, коли ви скасуєте підписку клієнта через панель Paddle, Cashier отримає відповідний вебхук і позначить підписку як «скасовану» в базі даних вашого застосунку.

<a name="checkout-sessions"></a>
## Сесії оформлення

Більшість операцій білінгу для клієнтів виконуються через «оформлення» за допомогою [віджета Checkout Overlay](https://developer.paddle.com/build/checkout/build-overlay-checkout) від Paddle або за допомогою [вбудованого оформлення](https://developer.paddle.com/build/checkout/build-branded-inline-checkout).

Перш ніж обробляти платежі оформлення через Paddle, вам слід визначити [посилання на оплату за замовчуванням](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) для вашого застосунку в панелі налаштувань оформлення Paddle.

<a name="overlay-checkout"></a>
### Overlay-оформлення

Перш ніж показувати віджет Checkout Overlay, вам потрібно згенерувати сесію оформлення за допомогою Cashier. Сесія оформлення повідомить віджету оформлення, яку операцію білінгу слід виконати:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier містить [Blade-компонент](/docs/{{version}}/blade#components) `paddle-button`. Ви можете передати сесію оформлення до цього компонента як «проп». Далі, коли цю кнопку буде натиснуто, з'явиться віджет оформлення Paddle:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

За замовчуванням це покаже віджет зі стандартною стилізацією Paddle. Ви можете налаштувати віджет, додавши до компонента [атрибути, які підтримує Paddle](https://developer.paddle.com/paddlejs/html-data-attributes), як-от атрибут `data-theme='light'`:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Віджет оформлення Paddle асинхронний. Щойно користувач створить підписку у віджеті, Paddle надішле вашому застосунку вебхук, щоб ви могли належно оновити стан підписки в базі даних вашого застосунку. Тому важливо, щоб ви правильно [налаштували вебхуки](#handling-paddle-webhooks) для врахування змін стану з боку Paddle.

> [!WARNING]
> Після зміни стану підписки затримка отримання відповідного вебхука зазвичай мінімальна, але вам слід урахувати це у своєму застосунку, зважаючи на те, що підписка вашого користувача може бути недоступною одразу після завершення оформлення.

<a name="manually-rendering-an-overlay-checkout"></a>
#### Ручний рендеринг overlay-оформлення

Ви також можете відрендерити overlay-оформлення вручну, не використовуючи вбудовані Blade-компоненти Laravel. Для початку згенеруйте сесію оформлення [як показано в попередніх прикладах](#overlay-checkout):

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Далі ви можете скористатися Paddle.js, щоб ініціалізувати оформлення. У цьому прикладі ми створимо посилання з класом `paddle_button`. Paddle.js виявить цей клас і покаже overlay-оформлення, коли посилання буде натиснуто:

```blade
<?php
$items = $checkout->getItems();
$customer = $checkout->getCustomer();
$custom = $checkout->getCustomData();
?>

<a
    href='#!'
    class='paddle_button'
    data-items='{!! json_encode($items) !!}'
    @if ($customer) data-customer-id='{{ $customer->paddle_id }}' @endif
    @if ($custom) data-custom-data='{{ json_encode($custom) }}' @endif
    @if ($returnUrl = $checkout->getReturnUrl()) data-success-url='{{ $returnUrl }}' @endif
>
    Buy Product
</a>
```

<a name="inline-checkout"></a>
### Вбудоване оформлення

Якщо ви не хочете користуватися віджетом оформлення в стилі «overlay» від Paddle, Paddle також пропонує можливість показати віджет вбудовано. Хоча цей підхід не дозволяє змінювати HTML-поля оформлення, він дає змогу вбудувати віджет у ваш застосунок.

Щоб вам було легко почати з вбудованим оформленням, Cashier містить Blade-компонент `paddle-checkout`. Для початку вам слід [згенерувати сесію оформлення](#overlay-checkout):

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Далі ви можете передати сесію оформлення до атрибута `checkout` компонента:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

Щоб змінити висоту компонента вбудованого оформлення, передайте Blade-компоненту атрибут `height`:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

Докладніше про можливості налаштування вбудованого оформлення дивіться в [посібнику Paddle щодо вбудованого оформлення](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) і [доступних налаштуваннях оформлення](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings).

<a name="manually-rendering-an-inline-checkout"></a>
#### Ручний рендеринг вбудованого оформлення

Ви також можете відрендерити вбудоване оформлення вручну, не використовуючи вбудовані Blade-компоненти Laravel. Для початку згенеруйте сесію оформлення [як показано в попередніх прикладах](#inline-checkout):

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Далі ви можете скористатися Paddle.js, щоб ініціалізувати оформлення. У цьому прикладі ми продемонструємо це за допомогою [Alpine.js](https://github.com/alpinejs/alpine); однак ви можете змінити цей приклад під свій фронтенд-стек:

```blade
<?php
$options = $checkout->options();

$options['settings']['frameTarget'] = 'paddle-checkout';
$options['settings']['frameInitialHeight'] = 366;
?>

<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open(@json($options));
">
</div>
```

<a name="guest-checkouts"></a>
### Гостьове оформлення

Іноді вам може знадобитися створити сесію оформлення для користувачів, яким не потрібен обліковий запис у вашому застосунку. Для цього скористайтеся методом `guest`:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

Далі ви можете передати сесію оформлення до Blade-компонентів [кнопки Paddle](#overlay-checkout) чи [вбудованого оформлення](#inline-checkout).

<a name="price-previews"></a>
## Попередній перегляд цін

Paddle дозволяє налаштовувати ціни для кожної валюти, тобто фактично задавати різні ціни для різних країн. Cashier Paddle дозволяє отримати всі ці ціни методом `previewPrices`. Цей метод приймає ID цін, для яких ви хочете отримати ціни:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

Валюту буде визначено на основі IP-адреси запиту; однак ви можете за бажанням указати конкретну країну, для якої отримати ціни:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

Отримавши ціни, ви можете показати їх як завгодно:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

Ви також можете показати проміжну суму й суму податку окремо:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

Докладніше дивіться в [документації API Paddle щодо попереднього перегляду цін](https://developer.paddle.com/api-reference/pricing-preview/preview-prices).

<a name="customer-price-previews"></a>
### Попередній перегляд цін для клієнта

Якщо користувач уже є клієнтом і ви хочете показати ціни, що застосовуються саме до нього, отримайте ціни безпосередньо з екземпляра клієнта:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Внутрішньо Cashier використає ID клієнта, щоб отримати ціни в його валюті. Так, наприклад, користувач зі США побачить ціни в доларах США, а користувач з Бельгії - у євро. Якщо відповідної валюти не знайдено, буде використано валюту продукту за замовчуванням. Усі ціни продукту чи плану підписки можна налаштувати в панелі керування Paddle.

<a name="price-discounts"></a>
### Знижки

Ви також можете показувати ціни зі знижкою. Викликаючи метод `previewPrices`, передайте ID знижки через опцію `discount_id`:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

Далі покажіть обчислені ціни:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## Клієнти

<a name="customer-defaults"></a>
### Значення за замовчуванням для клієнта

Cashier дозволяє визначити кілька корисних значень за замовчуванням для ваших клієнтів під час створення сесій оформлення. Ці значення дозволяють заздалегідь заповнити адресу електронної пошти та ім'я клієнта, щоб той міг одразу перейти до платіжної частини віджета оформлення. Задати ці значення можна, перевизначивши такі методи на своїй моделі з білінгом:

```php
/**
 * Get the customer's name to associate with Paddle.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Get the customer's email address to associate with Paddle.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

Ці значення за замовчуванням використовуватимуться для кожної дії в Cashier, яка генерує [сесію оформлення](#checkout-sessions).

<a name="retrieving-customers"></a>
### Отримання клієнтів

Ви можете отримати клієнта за його Paddle Customer ID методом `Cashier::findBillable`. Цей метод поверне екземпляр моделі з білінгом:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### Створення клієнтів

Іноді ви можете захотіти створити клієнта Paddle, не починаючи підписки. Зробити це можна методом `createAsCustomer`:

```php
$customer = $user->createAsCustomer();
```

Повертається екземпляр `Laravel\Paddle\Customer`. Щойно клієнта створено в Paddle, ви можете почати підписку пізніше. Ви можете передати необов'язковий масив `$options`, щоб указати будь-які додаткові [параметри створення клієнта, які підтримує API Paddle](https://developer.paddle.com/api-reference/customers/create-customer):

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## Підписки

<a name="creating-subscriptions"></a>
### Створення підписок

Щоб створити підписку, спершу отримайте з бази даних екземпляр вашої моделі з білінгом, яким зазвичай буде екземпляр `App\Models\User`. Отримавши екземпляр моделі, ви можете скористатися методом `subscribe`, щоб створити сесію оформлення для моделі:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

Перший аргумент методу `subscribe` - конкретна ціна, на яку підписується користувач. Це значення має відповідати ідентифікатору ціни в Paddle. Метод `returnTo` приймає URL, на який буде перенаправлено вашого користувача після успішного завершення оформлення. Другим аргументом методу `subscribe` має бути внутрішній «тип» підписки. Якщо ваш застосунок пропонує лише одну підписку, ви можете назвати її `default` чи `primary`. Цей тип підписки призначений лише для внутрішнього використання застосунком і не має показуватися користувачам. Крім того, він не повинен містити пробілів, і його ніколи не слід змінювати після створення підписки.

Ви також можете передати масив власних метаданих щодо підписки методом `customData`:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

Щойно сесію оформлення підписки створено, її можна передати до [Blade-компонента](#overlay-checkout) `paddle-button`, який входить до Cashier Paddle:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

Після того як користувач завершить оформлення, Paddle надішле вебхук `subscription_created`. Cashier отримає цей вебхук і налаштує підписку для вашого клієнта. Щоб переконатися, що всі вебхуки належно отримуються й обробляються вашим застосунком, переконайтеся, що ви правильно [налаштували обробку вебхуків](#handling-paddle-webhooks).

<a name="checking-subscription-status"></a>
### Перевірка стану підписки

Щойно користувач підписався на ваш застосунок, ви можете перевіряти стан його підписки різними зручними методами. По-перше, метод `subscribed` повертає `true`, якщо користувач має дійсну підписку, навіть якщо вона наразі в межах пробного періоду:

```php
if ($user->subscribed()) {
    // ...
}
```

Якщо ваш застосунок пропонує кілька підписок, ви можете вказати підписку під час виклику методу `subscribed`:

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
        if ($request->user() && ! $request->user()->subscribed()) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

Якщо ви хочете визначити, чи користувач досі в межах пробного періоду, скористайтеся методом `onTrial`. Цей метод може бути корисним, щоб визначити, чи слід показати користувачеві попередження про те, що він досі на пробному періоді:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

Метод `subscribedToPrice` можна використати, щоб визначити, чи підписаний користувач на певний план на основі заданого ID ціни Paddle. У цьому прикладі ми визначимо, чи підписка користувача `default` активно підписана на місячну ціну:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

Метод `recurring` можна використати, щоб визначити, чи має користувач наразі активну підписку і чи вийшов він уже за межі пробного чи пільгового періоду:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### Стан скасованої підписки

Щоб визначити, чи був користувач колись активним підписником, але скасував свою підписку, скористайтеся методом `canceled`:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

Ви також можете визначити, чи скасував користувач підписку, але досі перебуває в «пільговому періоді», доки підписка повністю не спливе. Наприклад, якщо користувач скасує 5 березня підписку, яка спочатку мала спливти 10 березня, він перебуватиме в «пільговому періоді» до 10 березня. Крім того, метод `subscribed` протягом цього часу все ще повертатиме `true`:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### Стан простроченої оплати

Якщо платіж за підпискою не пройде, її буде позначено як `past_due`. Коли ваша підписка в цьому стані, вона не буде активною, доки клієнт не оновить свою платіжну інформацію. Визначити, чи підписка прострочена, можна методом `pastDue` на екземплярі підписки:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

Коли підписка прострочена, вам слід указати користувачеві [оновити свою платіжну інформацію](#updating-payment-information).

Якщо ви хочете, щоб підписки все ще вважалися дійсними у стані `past_due`, скористайтеся методом `keepPastDueSubscriptionsActive`, який надає Cashier. Зазвичай цей метод слід викликати в методі `register` вашого `AppServiceProvider`:

```php
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]
> Коли підписка у стані `past_due`, її не можна змінити, доки платіжну інформацію не буде оновлено. Тому методи `swap` і `updateQuantity` видадуть виняток, коли підписка у стані `past_due`.

<a name="subscription-scopes"></a>
#### Скопи підписок

Більшість станів підписки також доступні як скопи запитів, тож ви можете легко шукати у своїй базі даних підписки в певному стані:

```php
// Get all valid subscriptions...
$subscriptions = Subscription::query()->valid()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```

Повний список доступних скопів наведено нижче:

```php
Subscription::query()->valid();
Subscription::query()->onTrial();
Subscription::query()->expiredTrial();
Subscription::query()->notOnTrial();
Subscription::query()->active();
Subscription::query()->recurring();
Subscription::query()->pastDue();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->canceled();
Subscription::query()->notCanceled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```

<a name="subscription-single-charges"></a>
### Разові списання за підпискою

Разові списання за підпискою дозволяють стягнути з підписників одноразову плату понад їхні підписки. Викликаючи метод `charge`, ви маєте вказати один чи кілька ID цін:

```php
// Charge a single price...
$response = $user->subscription()->charge('pri_123');

// Charge multiple prices at once...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

Метод `charge` фактично не стягне кошти з клієнта до наступного розрахункового інтервалу його підписки. Якщо ви хочете виставити рахунок клієнту негайно, скористайтеся натомість методом `chargeAndInvoice`:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### Оновлення платіжної інформації

Paddle завжди зберігає платіжний метод для кожної підписки. Якщо ви хочете оновити платіжний метод за замовчуванням для підписки, вам слід перенаправити клієнта на розміщену в Paddle сторінку оновлення платіжного методу методом `redirectToUpdatePaymentMethod` на моделі підписки:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

Коли користувач завершить оновлення своєї інформації, Paddle надішле вебхук `subscription_updated`, і деталі підписки буде оновлено в базі даних вашого застосунку.

<a name="changing-plans"></a>
### Зміна планів

Після того як користувач підписався на ваш застосунок, він може час від часу хотіти перейти на новий план підписки. Щоб оновити план підписки для користувача, передайте ідентифікатор ціни Paddle до методу `swap` підписки:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

Якщо ви хочете змінити план і одразу виставити рахунок користувачеві, не чекаючи наступного розрахункового циклу, скористайтеся методом `swapAndInvoice`:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### Пропорційний перерахунок

За замовчуванням Paddle робить пропорційний перерахунок платежів під час зміни планів. Метод `noProrate` можна використати, щоб оновити підписки без пропорційного перерахунку платежів:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

Якщо ви хочете вимкнути пропорційний перерахунок і одразу виставити рахунок клієнтам, скористайтеся методом `swapAndInvoice` у поєднанні з `noProrate`:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

Або ж, щоб не стягувати з клієнта плату за зміну підписки, скористайтеся методом `doNotBill`:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Докладніше про політики пропорційного перерахунку в Paddle дивіться в [документації Paddle щодо пропорційного перерахунку](https://developer.paddle.com/concepts/subscriptions/proration).

<a name="subscription-quantity"></a>
### Кількість у підписці

Іноді на підписки впливає «кількість». Наприклад, застосунок для керування проєктами може стягувати $10 на місяць за проєкт. Щоб легко збільшити чи зменшити кількість у підписці, скористайтеся методами `incrementQuantity` і `decrementQuantity`:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription()->decrementQuantity(5);
```

Як альтернативу ви можете задати конкретну кількість методом `updateQuantity`:

```php
$user->subscription()->updateQuantity(10);
```

Метод `noProrate` можна використати, щоб оновити кількість у підписці без пропорційного перерахунку платежів:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### Кількості для підписок з кількома продуктами

Якщо ваша підписка є [підпискою з кількома продуктами](#subscriptions-with-multiple-products), вам слід передати ID ціни, кількість якої ви хочете збільшити чи зменшити, другим аргументом методів increment / decrement:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### Підписки з кількома продуктами

[Підписка з кількома продуктами](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) дозволяє призначити одній підписці кілька продуктів білінгу. Наприклад, уявіть, що ви створюєте застосунок «служби підтримки» з базовою ціною підписки $10 на місяць, але пропонуєте додатковий продукт живого чату за додаткові $15 на місяць.

Створюючи сесії оформлення підписки, ви можете вказати кілька продуктів для певної підписки, передавши масив цін першим аргументом методу `subscribe`:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe([
        'price_monthly',
        'price_chat',
    ]);

    return view('billing', ['checkout' => $checkout]);
});
```

У наведеному вище прикладі клієнт матиме дві ціни, прив'язані до його підписки `default`. Обидві ціни стягуватимуться у відповідні розрахункові інтервали. За потреби ви можете передати асоціативний масив пар ключ / значення, щоб указати конкретну кількість для кожної ціни:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

Якщо ви хочете додати ще одну ціну до наявної підписки, вам потрібно скористатися методом `swap` підписки. Викликаючи метод `swap`, вам слід також включити поточні ціни й кількості підписки:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

Наведений вище приклад додасть нову ціну, але клієнту не буде виставлено рахунок за неї до наступного розрахункового циклу. Якщо ви хочете виставити рахунок клієнту негайно, скористайтеся методом `swapAndInvoice`:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

Ви можете прибрати ціни з підписок методом `swap`, опустивши ціну, яку хочете прибрати:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> Ви не можете прибрати останню ціну в підписці. Натомість вам слід просто скасувати підписку.

<a name="multiple-subscriptions"></a>
### Кілька підписок

Paddle дозволяє вашим клієнтам мати кілька підписок одночасно. Наприклад, ви можете керувати спортзалом, який пропонує підписку на плавання й підписку на важку атлетику, і кожна підписка може мати різну ціну. Звісно, клієнти мають мати змогу підписатися на один чи обидва плани.

Коли ваш застосунок створює підписки, ви можете передати тип підписки до методу `subscribe` другим аргументом. Типом може бути будь-який рядок, що представляє тип підписки, яку починає користувач:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

У цьому прикладі ми розпочали для клієнта місячну підписку на плавання. Однак згодом він може захотіти перейти на річну підписку. Коригуючи підписку клієнта, ми можемо просто змінити ціну в підписці `swimming`:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

Звісно, ви також можете скасувати підписку повністю:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### Призупинення підписок

Щоб призупинити підписку, викличте метод `pause` на підписці користувача:

```php
$user->subscription()->pause();
```

Коли підписку призупинено, Cashier автоматично встановить колонку `paused_at` у вашій базі даних. Ця колонка використовується, щоб визначити, коли метод `paused` має почати повертати `true`. Наприклад, якщо клієнт призупинить підписку 1 березня, але поновлення підписки було заплановане лише на 5 березня, метод `paused` продовжуватиме повертати `false` до 5 березня. Так відбувається тому, що користувачеві зазвичай дозволено користуватися застосунком до кінця його розрахункового циклу.

За замовчуванням призупинення відбувається в наступному розрахунковому інтервалі, тож клієнт може використати залишок оплаченого періоду. Якщо ви хочете призупинити підписку негайно, скористайтеся методом `pauseNow`:

```php
$user->subscription()->pauseNow();
```

За допомогою методу `pauseUntil` ви можете призупинити підписку до конкретного моменту часу:

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```

Або ж ви можете скористатися методом `pauseNowUntil`, щоб негайно призупинити підписку до заданого моменту часу:

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

Визначити, чи користувач призупинив підписку, але досі перебуває в «пільговому періоді», можна методом `onPausedGracePeriod`:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

Щоб відновити призупинену підписку, викличте на ній метод `resume`:

```php
$user->subscription()->resume();
```

> [!WARNING]
> Підписку не можна змінювати, доки її призупинено. Якщо ви хочете перейти на інший план чи оновити кількості, спершу потрібно відновити підписку.

<a name="canceling-subscriptions"></a>
### Скасування підписок

Щоб скасувати підписку, викличте метод `cancel` на підписці користувача:

```php
$user->subscription()->cancel();
```

Коли підписку скасовано, Cashier автоматично встановить колонку `ends_at` у вашій базі даних. Ця колонка використовується, щоб визначити, коли метод `subscribed` має почати повертати `false`. Наприклад, якщо клієнт скасує підписку 1 березня, але завершення підписки було заплановане лише на 5 березня, метод `subscribed` продовжуватиме повертати `true` до 5 березня. Так зроблено тому, що користувачеві зазвичай дозволено користуватися застосунком до кінця його розрахункового циклу.

Визначити, чи користувач скасував підписку, але досі перебуває в «пільговому періоді», можна методом `onGracePeriod`:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

Якщо ви хочете скасувати підписку негайно, викличте на ній метод `cancelNow`:

```php
$user->subscription()->cancelNow();
```

Щоб зупинити скасування підписки, яка перебуває в пільговому періоді, викличте метод `stopCancelation`:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Підписки Paddle не можна відновити після скасування. Якщо ваш клієнт захоче відновити свою підписку, йому доведеться створити нову.

<a name="subscription-trials"></a>
## Пробні періоди підписок

<a name="with-payment-method-up-front"></a>
### З платіжним методом наперед

Якщо ви хочете пропонувати клієнтам пробні періоди, водночас збираючи інформацію про платіжний метод наперед, вам слід задати тривалість пробного періоду в панелі Paddle для ціни, на яку підписується ваш клієнт. Далі ініціюйте сесію оформлення як зазвичай:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

Коли ваш застосунок отримає подію `subscription_created`, Cashier встановить дату завершення пробного періоду в записі підписки в базі даних вашого застосунку, а також вкаже Paddle не починати стягувати кошти з клієнта до цієї дати.

> [!WARNING]
> Якщо підписку клієнта не буде скасовано до дати завершення пробного періоду, кошти з нього спишуть одразу після його спливання, тож обов'язково повідомляйте своїх користувачів про дату завершення пробного періоду.

Визначити, чи користувач у межах пробного періоду, можна методом `onTrial` на екземплярі користувача:

```php
if ($user->onTrial()) {
    // ...
}
```

Щоб визначити, чи наявний пробний період сплив, скористайтеся методом `hasExpiredTrial`:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

Щоб визначити, чи користувач на пробному періоді для конкретного типу підписки, передайте тип до методів `onTrial` чи `hasExpiredTrial`:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### Без платіжного методу наперед

Якщо ви хочете пропонувати пробні періоди, не збираючи інформацію про платіжний метод користувача наперед, ви можете встановити колонку `trial_ends_at` у записі клієнта, прив'язаному до вашого користувача, на бажану дату завершення пробного періоду. Зазвичай це роблять під час реєстрації користувача:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

Cashier називає такий тип пробного періоду «загальним пробним періодом», оскільки він не прив'язаний до жодної наявної підписки. Метод `onTrial` на екземплярі `User` поверне `true`, якщо поточна дата не перевищує значення `trial_ends_at`:

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```

Щойно ви будете готові створити для користувача справжню підписку, скористайтеся методом `subscribe` як зазвичай:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

Щоб отримати дату завершення пробного періоду користувача, скористайтеся методом `trialEndsAt`. Цей метод поверне екземпляр дати Carbon, якщо користувач на пробному періоді, або `null`, якщо ні. Ви також можете передати необов'язковий параметр типу підписки, якщо хочете отримати дату завершення пробного періоду для конкретної підписки, відмінної від типової:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

Ви можете скористатися методом `onGenericTrial`, якщо хочете дізнатися саме те, що користувач перебуває в «загальному» пробному періоді і ще не створив справжньої підписки:

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```

<a name="extend-or-activate-a-trial"></a>
### Продовження чи активація пробного періоду

Ви можете продовжити наявний пробний період підписки, викликавши метод `extendTrial` і вказавши момент часу, коли пробний період має завершитися:

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

Або ж ви можете негайно активувати підписку, завершивши її пробний період, викликавши на ній метод `activate`:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Обробка вебхуків Paddle

Paddle може сповіщати ваш застосунок про різні події через вебхуки. За замовчуванням сервіс-провайдер Cashier реєструє маршрут, що вказує на контролер вебхуків Cashier. Цей контролер оброблятиме всі вхідні запити вебхуків.

За замовчуванням цей контролер автоматично оброблятиме скасування підписок із занадто великою кількістю невдалих списань, оновлення підписок і зміни платіжного методу; однак, як ми невдовзі побачимо, ви можете розширити цей контролер, щоб обробляти будь-яку подію вебхука Paddle, яку забажаєте.

Щоб ваш застосунок міг обробляти вебхуки Paddle, обов'язково [налаштуйте URL вебхука в панелі керування Paddle](https://vendors.paddle.com/notifications-v2). За замовчуванням контролер вебхуків Cashier відповідає за шляхом URL `/paddle/webhook`. Повний список усіх вебхуків, які вам слід увімкнути в панелі керування Paddle:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Обов'язково захистіть вхідні запити за допомогою `middleware` [перевірки підпису вебхука](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures), що входить до Cashier.

<a name="webhooks-csrf-protection"></a>
#### Вебхуки й захист від CSRF

Оскільки вебхуки Paddle мають обходити [захист від CSRF](/docs/{{version}}/csrf) у Laravel, вам слід подбати, щоб Laravel не намагався перевіряти CSRF-токен для вхідних вебхуків Paddle. Щоб досягти цього, виключіть `paddle/*` із захисту від CSRF у файлі `bootstrap/app.php` вашого застосунку:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### Вебхуки й локальна розробка

Щоб Paddle міг надсилати вашому застосунку вебхуки під час локальної розробки, вам потрібно буде відкрити свій застосунок через сервіс спільного доступу до сайтів, як-от [Ngrok](https://ngrok.com/) чи [Expose](https://expose.dev/docs/introduction). Якщо ви розробляєте застосунок локально за допомогою [Laravel Sail](/docs/{{version}}/sail), ви можете скористатися [командою спільного доступу до сайту](/docs/{{version}}/sail#sharing-your-site) в Sail.

<a name="defining-webhook-event-handlers"></a>
### Визначення обробників подій вебхуків

Cashier автоматично обробляє скасування підписки за невдалих списань та інші поширені вебхуки Paddle. Однак, якщо у вас є додаткові події вебхуків, які ви хочете обробляти, ви можете зробити це, слухаючи такі події, які диспетчеризує Cashier:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

Обидві події містять повні дані вебхука Paddle. Наприклад, якщо ви хочете обробити вебхук `transaction.billed`, зареєструйте [слухача](/docs/{{version}}/events#defining-listeners), який оброблятиме подію:

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // Handle the incoming event...
        }
    }
}
```

Cashier також випромінює події, присвячені типу отриманого вебхука. Окрім повних даних від Paddle, вони також містять релевантні моделі, які було використано для обробки вебхука, як-от модель з білінгом, підписку чи квитанцію:

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

Ви також можете перевизначити вбудований маршрут вебхука за замовчуванням, визначивши змінну оточення `CASHIER_WEBHOOK` у файлі `.env` вашого застосунку. Це значення має бути повним URL до вашого маршруту вебхука і має збігатися з URL, заданим у вашій панелі керування Paddle:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Перевірка підписів вебхуків

Щоб захистити свої вебхуки, ви можете скористатися [підписами вебхуків Paddle](https://developer.paddle.com/webhooks/signature-verification). Для зручності Cashier автоматично містить `middleware`, який перевіряє, що вхідний запит вебхука Paddle є дійсним.

Щоб увімкнути перевірку вебхуків, переконайтеся, що змінну оточення `PADDLE_WEBHOOK_SECRET` визначено у файлі `.env` вашого застосунку. Секрет вебхука можна отримати з панелі вашого облікового запису Paddle.

<a name="single-charges"></a>
## Разові списання

<a name="charging-for-products"></a>
### Списання за продукти

Якщо ви хочете ініціювати купівлю продукту для клієнта, скористайтеся методом `checkout` на екземплярі моделі з білінгом, щоб згенерувати сесію оформлення для покупки. Метод `checkout` приймає один чи кілька ID цін. За потреби можна скористатися асоціативним масивом, щоб указати кількість продукту, який купують:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

Згенерувавши сесію оформлення, ви можете скористатися наданим Cashier [Blade-компонентом](#overlay-checkout) `paddle-button`, щоб дозволити користувачеві переглянути віджет оформлення Paddle і завершити покупку:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

Сесія оформлення має метод `customData`, який дозволяє передати будь-які власні дані до створення транзакції, що лежить в основі. Докладніше про доступні вам опції під час передавання власних даних дивіться в [документації Paddle](https://developer.paddle.com/build/transactions/custom-data):

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### Повернення коштів за транзакціями

Повернення коштів за транзакціями поверне повернуту суму на платіжний метод вашого клієнта, який використовувався під час покупки. Якщо вам потрібно повернути кошти за покупку в Paddle, скористайтеся методом `refund` на моделі `Cashier\Paddle\Transaction`. Цей метод приймає причину як перший аргумент, а також один чи кілька ID цін для повернення з необов'язковими сумами у вигляді асоціативного масиву. Отримати транзакції для певної моделі з білінгом можна методом `transactions`.

Наприклад, уявімо, що ми хочемо повернути кошти за конкретною транзакцією для цін `pri_123` і `pri_456`. Ми хочемо повністю повернути `pri_123`, але повернути лише два долари за `pri_456`:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // Fully refund this price...
    'pri_456' => 200, // Only partially refund this price...
]);
```

Наведений вище приклад повертає кошти за конкретні позиції транзакції. Якщо ви хочете повернути кошти за всю транзакцію, просто вкажіть причину:

```php
$response = $transaction->refund('Accidental charge');
```

Докладніше про повернення коштів дивіться в [документації Paddle щодо повернень](https://developer.paddle.com/build/transactions/create-transaction-adjustments).

> [!WARNING]
> Повернення коштів завжди має бути схвалене Paddle, перш ніж буде оброблене повністю.

<a name="crediting-transactions"></a>
### Кредитування транзакцій

Так само як і повертати кошти, ви можете кредитувати транзакції. Кредитування транзакцій додасть кошти на баланс клієнта, щоб їх можна було використати для майбутніх покупок. Кредитувати можна лише транзакції, зібрані вручну, а не автоматично зібрані транзакції (як-от підписки), оскільки Paddle обробляє кредити за підписками автоматично:

```php
$transaction = $user->transactions()->first();

// Credit a specific line item fully...
$response = $transaction->credit('Compensation', 'pri_123');
```

Докладніше [дивіться в документації Paddle щодо кредитування](https://developer.paddle.com/build/transactions/create-transaction-adjustments).

> [!WARNING]
> Кредити можна застосувати лише до зібраних вручну транзакцій. Автоматично зібрані транзакції кредитує сам Paddle.

<a name="transactions"></a>
## Транзакції

Ви можете легко отримати масив транзакцій моделі з білінгом через властивість `transactions`:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

Транзакції представляють платежі за ваші продукти й покупки і супроводжуються рахунками. У базі даних вашого застосунку зберігаються лише завершені транзакції.

Перелічуючи транзакції клієнта, ви можете скористатися методами екземпляра транзакції, щоб показати релевантну платіжну інформацію. Наприклад, ви можете захотіти перелічити кожну транзакцію в таблиці, дозволивши користувачеві легко завантажити будь-який із рахунків:

```html
<table>
    @foreach ($transactions as $transaction)
        <tr>
            <td>{{ $transaction->billed_at->toFormattedDateString() }}</td>
            <td>{{ $transaction->total() }}</td>
            <td>{{ $transaction->tax() }}</td>
            <td><a href="{{ route('download-invoice', $transaction->id) }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```

Маршрут `download-invoice` може виглядати так:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### Минулі та майбутні платежі

Ви можете скористатися методами `lastPayment` і `nextPayment`, щоб отримати й показати минулі чи майбутні платежі клієнта за періодичними підписками:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

Обидва ці методи повернуть екземпляр `Laravel\Paddle\Payment`; однак `lastPayment` поверне `null`, коли транзакції ще не синхронізовано вебхуками, а `nextPayment` поверне `null`, коли розрахунковий цикл завершився (наприклад, коли підписку скасовано):

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## Тестування

Під час тестування вам слід вручну перевірити свій потік білінгу, щоб переконатися, що ваша інтеграція працює як очікується.

Для автоматизованих тестів, зокрема тих, що виконуються в CI-середовищі, ви можете скористатися [HTTP-клієнтом Laravel](/docs/{{version}}/http-client#testing), щоб підробити HTTP-виклики до Paddle. Хоча це не тестує фактичні відповіді від Paddle, воно дає спосіб тестувати ваш застосунок, не викликаючи API Paddle насправді.
