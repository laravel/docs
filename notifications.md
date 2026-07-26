---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Сповіщення

- [Вступ](#introduction)
- [Генерація сповіщень](#generating-notifications)
- [Надсилання сповіщень](#sending-notifications)
    - [Через трейт Notifiable](#using-the-notifiable-trait)
    - [Через фасад Notification](#using-the-notification-facade)
    - [Задання каналів доставки](#specifying-delivery-channels)
    - [Сповіщення в черзі](#queueing-notifications)
    - [Сповіщення на льоту](#on-demand-notifications)
- [Поштові сповіщення](#mail-notifications)
    - [Форматування поштових повідомлень](#formatting-mail-messages)
    - [Налаштування відправника](#customizing-the-sender)
    - [Налаштування отримувача](#customizing-the-recipient)
    - [Налаштування теми](#customizing-the-subject)
    - [Налаштування мейлера](#customizing-the-mailer)
    - [Налаштування шаблонів](#customizing-the-templates)
    - [Вкладення](#mail-attachments)
    - [Додавання тегів і метаданих](#adding-tags-metadata)
    - [Налаштування повідомлення Symfony](#customizing-the-symfony-message)
    - [Використання mailable-класів](#using-mailables)
    - [Попередній перегляд поштових сповіщень](#previewing-mail-notifications)
- [Поштові сповіщення в Markdown](#markdown-mail-notifications)
    - [Генерація повідомлення](#generating-the-message)
    - [Написання повідомлення](#writing-the-message)
    - [Налаштування компонентів](#customizing-the-components)
- [Сповіщення в базі даних](#database-notifications)
    - [Передумови](#database-prerequisites)
    - [Форматування сповіщень у базі даних](#formatting-database-notifications)
    - [Доступ до сповіщень](#accessing-the-notifications)
    - [Позначення сповіщень прочитаними](#marking-notifications-as-read)
- [Сповіщення через бродкастинг](#broadcast-notifications)
    - [Передумови](#broadcast-prerequisites)
    - [Форматування сповіщень бродкастингу](#formatting-broadcast-notifications)
    - [Прослуховування сповіщень](#listening-for-notifications)
- [SMS-сповіщення](#sms-notifications)
    - [Передумови](#sms-prerequisites)
    - [Форматування SMS-сповіщень](#formatting-sms-notifications)
    - [Налаштування номера «From»](#customizing-the-from-number)
    - [Додавання клієнтського посилання](#adding-a-client-reference)
    - [Маршрутизація SMS-сповіщень](#routing-sms-notifications)
- [Сповіщення в Slack](#slack-notifications)
    - [Передумови](#slack-prerequisites)
    - [Форматування сповіщень Slack](#formatting-slack-notifications)
    - [Інтерактивність Slack](#slack-interactivity)
    - [Маршрутизація сповіщень Slack](#routing-slack-notifications)
    - [Сповіщення зовнішніх робочих просторів Slack](#notifying-external-slack-workspaces)
- [Локалізація сповіщень](#localizing-notifications)
- [Тестування](#testing)
- [Події сповіщень](#notification-events)
- [Власні канали](#custom-channels)

<a name="introduction"></a>
## Вступ

Окрім підтримки [надсилання пошти](/docs/{{version}}/mail), Laravel підтримує надсилання сповіщень різними каналами доставки: електронною поштою, SMS (через [Vonage](https://www.vonage.com/communications-apis/), раніше відомий як Nexmo) та [Slack](https://slack.com). Крім того, спільнота створила чимало [каналів сповіщень](https://laravel-notification-channels.com/about/#suggesting-a-new-channel), які дозволяють надсилати сповіщення десятками різних каналів! Сповіщення можна також зберігати в базі даних, щоб показувати їх у вебінтерфейсі.

Зазвичай сповіщення мають бути короткими інформаційними повідомленнями, які розповідають користувачам про щось, що сталося у вашому застосунку. Наприклад, якщо ви пишете застосунок для виставлення рахунків, ви можете надсилати користувачам сповіщення «Рахунок оплачено» каналами пошти та SMS.

<a name="generating-notifications"></a>
## Генерація сповіщень

У Laravel кожне сповіщення представлено окремим класом, який зазвичай зберігається в каталозі `app/Notifications`. Не переймайтеся, якщо цього каталогу у вашому застосунку немає - його буде створено, коли ви виконаєте команду Artisan `make:notification`:

```shell
php artisan make:notification InvoicePaid
```

Ця команда покладе свіжий клас сповіщення до каталогу `app/Notifications`. Кожен клас сповіщення містить метод `via` і змінну кількість методів побудови повідомлення - на кшталт `toMail` чи `toDatabase`, - які перетворюють сповіщення на повідомлення, придатне для конкретного каналу.

<a name="sending-notifications"></a>
## Надсилання сповіщень

<a name="using-the-notifiable-trait"></a>
### Через трейт Notifiable

Сповіщення можна надсилати двома способами: методом `notify` трейта `Notifiable` або через [фасад](/docs/{{version}}/facades) `Notification`. Трейт `Notifiable` за замовчуванням підключено до моделі `App\Models\User` вашого застосунку:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

Метод `notify`, який надає цей трейт, очікує екземпляр сповіщення:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> Пам'ятайте: ви можете використовувати трейт `Notifiable` у будь-якій зі своїх моделей. Ви не обмежені лише моделлю `User`.

<a name="using-the-notification-facade"></a>
### Через фасад Notification

Як варіант, ви можете надсилати сповіщення через [фасад](/docs/{{version}}/facades) `Notification`. Цей підхід корисний, коли треба надіслати сповіщення кільком сутностям - наприклад, колекції користувачів. Щоб надіслати сповіщення через фасад, передайте всі сутності та екземпляр сповіщення методу `send`:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

Ви також можете надіслати сповіщення негайно методом `sendNow`. Цей метод надішле сповіщення одразу, навіть якщо воно реалізує інтерфейс `ShouldQueue`:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### Задання каналів доставки

Кожен клас сповіщення має метод `via`, який визначає, якими каналами буде доставлено сповіщення. Сповіщення можна надсилати каналами `mail`, `database`, `broadcast`, `vonage` та `slack`.

> [!NOTE]
> Якщо ви хочете скористатися іншими каналами доставки - наприклад, Telegram чи Pusher, - погляньте на [сайт Laravel Notification Channels](http://laravel-notification-channels.com), який веде спільнота.

Метод `via` отримує екземпляр `$notifiable` - екземпляр класу, якому надсилається сповіщення. Ви можете скористатися `$notifiable`, щоб визначити, якими каналами слід доставити сповіщення:

```php
/**
 * Get the notification's delivery channels.
 *
 * @return array<int, string>
 */
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### Сповіщення в черзі

> [!WARNING]
> Перш ніж ставити сповіщення в чергу, налаштуйте чергу й [запустіть воркер](/docs/{{version}}/queues#running-the-queue-worker).

Надсилання сповіщень може забирати час, особливо якщо каналу треба зробити зовнішній виклик API. Щоб пришвидшити час відповіді вашого застосунку, дозвольте ставити сповіщення в чергу, додавши до класу інтерфейс `ShouldQueue` і трейт `Queueable`. Інтерфейс і трейт уже імпортовано в усі сповіщення, згенеровані командою `make:notification`, тож ви можете одразу додати їх до свого класу:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```

Щойно до сповіщення додано інтерфейс `ShouldQueue`, ви можете надсилати його як зазвичай. Laravel помітить інтерфейс `ShouldQueue` у класі й автоматично поставить доставку сповіщення в чергу:

```php
$user->notify(new InvoicePaid($invoice));
```

Коли сповіщення ставлять у чергу, для кожної комбінації отримувача й каналу створюється окреме завдання. Наприклад, якщо ваше сповіщення має трьох отримувачів і два канали, у чергу потрапить шість завдань.

<a name="delaying-notifications"></a>
#### Затримка сповіщень

Якщо ви хочете відкласти доставку сповіщення, додайте ланцюжком метод `delay` під час його створення:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

Ви можете передати методу `delay` масив, щоб задати затримку для конкретних каналів:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

Як варіант, ви можете описати метод `withDelay` у самому класі сповіщення. Метод `withDelay` має повернути масив назв каналів і значень затримки:

```php
/**
 * Determine the notification's delivery delay.
 *
 * @return array<string, \Illuminate\Support\Carbon>
 */
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->plus(minutes: 5),
        'sms' => now()->plus(minutes: 10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### Налаштування підключення черги сповіщень

За замовчуванням сповіщення потрапляють у чергу через підключення черги за замовчуванням вашого застосунку. Якщо ви хочете вказати інше підключення для конкретного сповіщення, викличте метод `onConnection` у його конструкторі:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

Або ж, якщо ви хочете вказати конкретне підключення черги для кожного каналу, який підтримує сповіщення, опишіть у сповіщенні метод `viaConnections`. Цей метод має повернути масив пар «назва каналу - назва підключення черги»:

```php
/**
 * Determine which connections should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaConnections(): array
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```

<a name="customizing-notification-channel-queues"></a>
#### Налаштування черг каналів сповіщень

Якщо ви хочете вказати конкретну чергу для кожного каналу, який підтримує сповіщення, опишіть у сповіщенні метод `viaQueues`. Цей метод має повернути масив пар «назва каналу - назва черги»:

```php
/**
 * Determine which queues should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaQueues(): array
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="customizing-queued-notification-job-properties"></a>
#### Налаштування атрибутів завдання сповіщення в черзі

Ви можете налаштувати поведінку завдання в черзі, описавши атрибути черги у класі сповіщення. Ці атрибути успадкує завдання, яке надсилатиме сповіщення:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Timeout;
use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
#[Timeout(120)]
#[MaxExceptions(3)]
class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```

Якщо ви хочете забезпечити приватність і цілісність даних сповіщення в черзі за допомогою [шифрування](/docs/{{version}}/encryption), додайте до класу сповіщення інтерфейс `ShouldBeEncrypted`:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue, ShouldBeEncrypted
{
    use Queueable;

    // ...
}
```

Окрім опису цих атрибутів безпосередньо у класі сповіщення, ви можете описати методи `backoff` та `retryUntil`, щоб задати стратегію відступу й таймаут повторів для завдання сповіщення в черзі:

```php
use DateTime;

/**
 * Calculate the number of seconds to wait before retrying the notification.
 */
public function backoff(): int
{
    return 3;
}

/**
 * Determine the time at which the notification should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> Докладніше про ці атрибути й методи завдань читайте в документації про [завдання в черзі](/docs/{{version}}/queues#max-job-attempts-and-timeout).

<a name="queued-notification-middleware"></a>
#### Middleware сповіщень у черзі

Сповіщення в черзі можуть описувати middleware [так само, як завдання в черзі](/docs/{{version}}/queues#job-middleware). Для початку опишіть у класі сповіщення метод `middleware`. Метод `middleware` отримає змінні `$notifiable` та `$channel`, що дозволяє налаштувати повернений middleware залежно від призначення сповіщення:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the notification job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(object $notifiable, string $channel)
{
    return match ($channel) {
        'mail' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### Сповіщення в черзі та транзакції бази даних

Коли сповіщення в черзі диспетчеризуються всередині транзакцій бази даних, черга може обробити їх ще до того, як транзакцію буде зафіксовано. Коли таке трапляється, будь-які зміни, які ви внесли до моделей чи записів у базі під час транзакції, ще можуть не бути в базі. Ба більше, будь-які моделі чи записи, створені всередині транзакції, можуть у базі не існувати. Якщо ваше сповіщення залежить від цих моделей, під час обробки завдання, яке його надсилає, можуть виникнути несподівані помилки.

Якщо опція конфігурації `after_commit` вашого підключення черги має значення `false`, ви все одно можете вказати, що конкретне сповіщення в черзі слід диспетчеризувати після фіксації всіх відкритих транзакцій, - викличте метод `afterCommit` під час надсилання сповіщення:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

Як варіант, ви можете викликати метод `afterCommit` у конструкторі свого сповіщення:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> Щоб дізнатися більше про обхід цих проблем, перегляньте документацію про [завдання в черзі та транзакції бази даних](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### Визначення, чи слід надсилати сповіщення з черги

Після того, як сповіщення в черзі диспетчеризовано на фонову обробку, його зазвичай підхопить воркер черги й надішле призначеному отримувачу.

Проте, якщо ви хочете ухвалити остаточне рішення про надсилання сповіщення вже під час обробки воркером, опишіть у класі сповіщення метод `shouldSend`. Якщо цей метод поверне `false`, сповіщення не буде надіслано:

```php
/**
 * Determine if the notification should be sent.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="after-sending-notifications"></a>
#### Після надсилання сповіщень

Якщо ви хочете виконати код після того, як сповіщення надіслано, опишіть у класі сповіщення метод `afterSending`. Цей метод отримає сутність-отримувача, назву каналу та відповідь від каналу:

```php
/**
 * Handle the notification after it has been sent.
 */
public function afterSending(object $notifiable, string $channel, mixed $response): void
{
    // ...
}
```

<a name="on-demand-notifications"></a>
### Сповіщення на льоту

Інколи вам може знадобитися надіслати сповіщення комусь, хто не зберігається як «користувач» вашого застосунку. Метод `route` фасаду `Notification` дозволяє вказати разову інформацію маршрутизації сповіщення перед надсиланням:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

Якщо, надсилаючи сповіщення на льоту маршрутом `mail`, ви хочете передати ім'я отримувача, передайте масив, у якому ключем першого елемента є адреса, а значенням - ім'я:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

Метод `routes` дозволяє передати разову інформацію маршрутизації одразу для кількох каналів сповіщень:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## Поштові сповіщення

<a name="formatting-mail-messages"></a>
### Форматування поштових повідомлень

Якщо сповіщення можна надсилати поштою, опишіть у класі сповіщення метод `toMail`. Цей метод отримає сутність `$notifiable` і має повернути екземпляр `Illuminate\Notifications\Messages\MailMessage`.

Клас `MailMessage` містить кілька простих методів, які допомагають будувати транзакційні листи. Поштові повідомлення можуть містити рядки тексту, а також «заклик до дії». Погляньмо на приклад методу `toMail`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->greeting('Hello!')
        ->line('One of your invoices has been paid!')
        ->lineIf($this->amount > 0, "Amount paid: {$this->amount}")
        ->action('View Invoice', $url)
        ->line('Thank you for using our application!');
}
```

> [!NOTE]
> Зверніть увагу: у методі `toMail` ми використовуємо `$this->invoice->id`. Ви можете передати в конструктор сповіщення будь-які дані, потрібні йому для формування повідомлення.

У цьому прикладі ми реєструємо привітання, рядок тексту, заклик до дії й ще один рядок тексту. Ці методи об'єкта `MailMessage` роблять форматування невеликих транзакційних листів простим і швидким. Далі поштовий канал перетворить складові повідомлення на гарний адаптивний HTML-шаблон із текстовим відповідником. Ось приклад листа, згенерованого каналом `mail`:

<img src="https://laravel.com/img/docs/notification-example-2.png">

> [!NOTE]
> Надсилаючи поштові сповіщення, обов'язково задайте опцію конфігурації `name` у файлі `config/app.php`. Це значення використовуватиметься в шапці та підвалі ваших поштових сповіщень.

<a name="error-messages"></a>
#### Повідомлення про помилки

Деякі сповіщення інформують користувачів про помилки - наприклад, про невдалу оплату рахунка. Ви можете вказати, що поштове повідомлення стосується помилки, викликавши метод `error` під час його побудови. Коли ви користуєтеся методом `error`, кнопка заклику до дії буде червоною, а не чорною:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->error()
        ->subject('Invoice Payment Failed')
        ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
#### Інші варіанти форматування поштових сповіщень

Замість описувати «рядки» тексту у класі сповіщення, ви можете скористатися методом `view`, щоб указати власний шаблон для рендерингу листа сповіщення:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

Текстове представлення поштового повідомлення можна вказати, передавши назву представлення другим елементом масиву, який передається методу `view`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

Або ж, якщо ваше повідомлення має лише текстове представлення, скористайтеся методом `text`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### Налаштування відправника

За замовчуванням відправника / адресу «from» листа задано у файлі конфігурації `config/mail.php`. Проте ви можете вказати адресу «from» для конкретного сповіщення методом `from`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### Налаштування отримувача

Надсилаючи сповіщення каналом `mail`, система сповіщень автоматично шукає властивість `email` у вашій сутності-отримувачі. Ви можете змінити адресу, на яку доставляється сповіщення, описавши в цій сутності метод `routeNotificationForMail`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the mail channel.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // Return email address only...
        return $this->email_address;

        // Return email address and name...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### Налаштування теми

За замовчуванням темою листа є назва класу сповіщення, відформатована в «Title Case». Тож, якщо ваш клас сповіщення називається `InvoicePaid`, темою листа буде `Invoice Paid`. Якщо ви хочете вказати іншу тему, викличте метод `subject` під час побудови повідомлення:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### Налаштування мейлера

За замовчуванням поштове сповіщення надсилається мейлером за замовчуванням, описаним у файлі `config/mail.php`. Проте ви можете вказати інший мейлер під час виконання, викликавши метод `mailer` під час побудови повідомлення:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### Налаштування шаблонів

Ви можете змінити HTML- і текстовий шаблони, які використовують поштові сповіщення, опублікувавши ресурси пакета сповіщень. Після виконання цієї команди шаблони поштових сповіщень опиняться в каталозі `resources/views/vendor/notifications`:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### Вкладення

Щоб додати вкладення до поштового сповіщення, скористайтеся методом `attach` під час побудови повідомлення. Метод `attach` приймає першим аргументом абсолютний шлях до файлу:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> Метод `attach` поштових повідомлень сповіщень також приймає [об'єкти, придатні для вкладення](/docs/{{version}}/mail#attachable-objects). Щоб дізнатися більше, перегляньте вичерпну [документацію про такі об'єкти](/docs/{{version}}/mail#attachable-objects).

Вкладаючи файли до повідомлення, ви можете вказати відображувану назву та / або MIME-тип, передавши `array` другим аргументом методу `attach`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file', [
            'as' => 'name.pdf',
            'mime' => 'application/pdf',
        ]);
}
```

За потреби до повідомлення можна вкласти кілька файлів методом `attachMany`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachMany([
            '/path/to/forge.svg',
            '/path/to/vapor.svg' => [
                'as' => 'Logo.svg',
                'mime' => 'image/svg+xml',
            ],
        ]);
}
```

Метод `attachFromStorageDisk` дозволяє вкласти файл, що лежить на конкретному [диску файлової системи](/docs/{{version}}/filesystem). Цей метод приймає назву диска й шлях до файлу на ньому:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorageDisk('s3', '/path/to/file', 'invoice.pdf', [
            'mime' => 'application/pdf',
        ]);
}
```

<a name="raw-data-attachments"></a>
#### Вкладення сирих даних

Метод `attachData` дозволяє вкласти сирий рядок байтів як вкладення. Викликаючи метод `attachData`, передайте ім'я файлу, яке слід призначити вкладенню:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachData($this->pdf, 'name.pdf', [
            'mime' => 'application/pdf',
        ]);
}
```

<a name="adding-tags-metadata"></a>
### Додавання тегів і метаданих

Деякі сторонні поштові провайдери на кшталт Mailgun і Postmark підтримують «теги» й «метадані» повідомлень, які дозволяють групувати та відстежувати листи, надіслані вашим застосунком. Додати теги й метадані до листа можна методами `tag` та `metadata`:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Якщо ваш застосунок використовує драйвер Mailgun, докладніше про [теги](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) та [метадані](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) читайте в документації Mailgun. Так само в документації Postmark можна знайти більше про їхню підтримку [тегів](https://postmarkapp.com/blog/tags-support-for-smtp) і [метаданих](https://postmarkapp.com/support/article/1125-custom-metadata-faq).

Якщо ваш застосунок надсилає листи через Amazon SES, скористайтеся методом `metadata`, щоб додати до повідомлення [«теги» SES](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html).

<a name="customizing-the-symfony-message"></a>
### Налаштування повідомлення Symfony

Метод `withSymfonyMessage` класу `MailMessage` дозволяє зареєструвати замикання, яке буде викликано з екземпляром Symfony Message перед надсиланням повідомлення. Це дає вам змогу глибоко налаштувати повідомлення перед доставкою:

```php
use Symfony\Component\Mime\Email;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->withSymfonyMessage(function (Email $message) {
            $message->getHeaders()->addTextHeader(
                'Custom-Header', 'Header Value'
            );
        });
}
```

<a name="using-mailables"></a>
### Використання mailable-класів

За потреби ви можете повернути з методу `toMail` свого сповіщення повноцінний [mailable-об'єкт](/docs/{{version}}/mail). Коли ви повертаєте `Mailable` замість `MailMessage`, вам потрібно вказати отримувача методом `to` mailable-об'єкта:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailable-класи та сповіщення на льоту

Якщо ви надсилаєте [сповіщення на льоту](#on-demand-notifications), екземпляр `$notifiable`, переданий методу `toMail`, буде екземпляром `Illuminate\Notifications\AnonymousNotifiable`, який пропонує метод `routeNotificationFor` для отримання адреси, на яку слід надіслати сповіщення:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    $address = $notifiable instanceof AnonymousNotifiable
        ? $notifiable->routeNotificationFor('mail')
        : $notifiable->email;

    return (new InvoicePaidMailable($this->invoice))
        ->to($address);
}
```

<a name="previewing-mail-notifications"></a>
### Попередній перегляд поштових сповіщень

Розробляючи шаблон поштового сповіщення, зручно швидко переглядати відрендерене повідомлення в браузері, як звичайний шаблон Blade. Тому Laravel дозволяє повертати будь-яке поштове повідомлення, згенероване поштовим сповіщенням, напряму із замикання маршруту чи контролера. Коли повернуто `MailMessage`, його буде відрендерено й показано в браузері, тож ви зможете швидко переглянути дизайн, не надсилаючи листа на справжню адресу:

```php
use App\Models\Invoice;
use App\Notifications\InvoicePaid;

Route::get('/notification', function () {
    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))
        ->toMail($invoice->user);
});
```

<a name="markdown-mail-notifications"></a>
## Поштові сповіщення в Markdown

Поштові сповіщення в Markdown дозволяють скористатися готовими шаблонами поштових сповіщень і водночас дають більше свободи писати довші, налаштовані повідомлення. Оскільки повідомлення пишуться в Markdown, Laravel може відрендерити для них гарні адаптивні HTML-шаблони, а заразом автоматично згенерувати текстовий відповідник.

<a name="generating-the-message"></a>
### Генерація повідомлення

Щоб згенерувати сповіщення з відповідним Markdown-шаблоном, скористайтеся опцією `--markdown` команди Artisan `make:notification`:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

Як і всі інші поштові сповіщення, сповіщення з Markdown-шаблонами мають описувати у своєму класі метод `toMail`. Проте замість методів `line` та `action` для побудови сповіщення скористайтеся методом `markdown`, щоб указати назву Markdown-шаблону. Масив даних, які ви хочете зробити доступними шаблону, можна передати другим аргументом методу:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
### Написання повідомлення

Поштові сповіщення в Markdown поєднують компоненти Blade і синтаксис Markdown, що дозволяє легко будувати сповіщення, користуючись готовими компонентами сповіщень Laravel:

```blade
<x-mail::message>
# Invoice Paid

Your invoice has been paid!

<x-mail::button :url="$url">
View Invoice
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> [!NOTE]
> Не робіть зайвих відступів, коли пишете Markdown-листи. За стандартами Markdown парсери рендерять вміст із відступами як блоки коду.

<a name="button-component"></a>
#### Компонент button

Компонент button рендерить відцентроване посилання-кнопку. Компонент приймає два аргументи: `url` та необов'язковий `color`. Підтримувані кольори - `primary`, `green` та `red`. Ви можете додати до сповіщення скільки завгодно компонентів button:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### Компонент panel

Компонент panel рендерить заданий блок тексту в панелі, колір тла якої трохи відрізняється від решти сповіщення. Це дозволяє привернути увагу до певного блоку тексту:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### Компонент table

Компонент table дозволяє перетворити таблицю Markdown на HTML-таблицю. Компонент приймає таблицю Markdown як свій вміст. Вирівнювання стовпців підтримується стандартним синтаксисом вирівнювання таблиць Markdown:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### Налаштування компонентів

Ви можете експортувати всі компоненти сповіщень Markdown до власного застосунку, щоб їх налаштувати. Щоб експортувати компоненти, опублікуйте тег ресурсів `laravel-mail` командою Artisan `vendor:publish`:

```shell
php artisan vendor:publish --tag=laravel-mail
```

Ця команда опублікує поштові компоненти Markdown до каталогу `resources/views/vendor/mail`. Каталог `mail` міститиме каталоги `html` і `text`, у кожному з яких лежатиме відповідне представлення кожного доступного компонента. Ви вільні налаштовувати ці компоненти як заманеться.

<a name="customizing-the-css"></a>
#### Налаштування CSS

Після експорту компонентів каталог `resources/views/vendor/mail/html/themes` міститиме файл `default.css`. Ви можете змінити CSS у цьому файлі, і ваші стилі автоматично буде вбудовано в HTML-представлення ваших Markdown-сповіщень.

Якщо ви хочете створити цілком нову тему для компонентів Markdown у Laravel, покладіть CSS-файл у каталог `html/themes`. Назвавши й зберігши свій CSS-файл, оновіть опцію `theme` у файлі конфігурації `mail` відповідно до назви нової теми.

Щоб змінити тему для окремого сповіщення, викличте метод `theme` під час побудови його поштового повідомлення. Метод `theme` приймає назву теми, яку слід використати під час надсилання сповіщення:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->theme('invoice')
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="database-notifications"></a>
## Сповіщення в базі даних

<a name="database-prerequisites"></a>
### Передумови

Канал сповіщень `database` зберігає інформацію про сповіщення в таблиці бази даних. Ця таблиця міститиме тип сповіщення, а також JSON-структуру даних, яка його описує.

Ви можете робити запити до цієї таблиці, щоб показувати сповіщення в інтерфейсі вашого застосунку. Проте спершу вам потрібно створити таблицю, яка їх зберігатиме. Скористайтеся командою `make:notifications-table`, щоб згенерувати [міграцію](/docs/{{version}}/migrations) з належною схемою таблиці:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> Якщо ваші моделі-отримувачі використовують [первинні ключі UUID чи ULID](/docs/{{version}}/eloquent#uuid-and-ulid-keys), замініть у міграції таблиці сповіщень метод `morphs` на [uuidMorphs](/docs/{{version}}/migrations#column-method-uuidMorphs) або [ulidMorphs](/docs/{{version}}/migrations#column-method-ulidMorphs).

<a name="formatting-database-notifications"></a>
### Форматування сповіщень у базі даних

Якщо сповіщення можна зберігати в таблиці бази даних, опишіть у класі сповіщення метод `toDatabase` або `toArray`. Цей метод отримає сутність `$notifiable` і має повернути звичайний PHP-масив. Повернений масив буде закодовано в JSON і збережено у стовпці `data` вашої таблиці `notifications`. Погляньмо на приклад методу `toArray`:

```php
/**
 * Get the array representation of the notification.
 *
 * @return array<string, mixed>
 */
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

Коли сповіщення збережено в базі вашого застосунку, стовпцю `type` за замовчуванням присвоюється назва класу сповіщення, а стовпець `read_at` матиме значення `null`. Проте ви можете змінити цю поведінку, описавши у класі сповіщення методи `databaseType` та `initialDatabaseReadAtValue`:

```php
use Illuminate\Support\Carbon;

/**
 * Get the notification's database type.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * Get the initial value for the "read_at" column.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` проти `toArray`

Метод `toArray` використовує й канал `broadcast`, щоб визначити, які дані надсилати вашому фронтенду на JavaScript. Якщо ви хочете мати два різні масиви для каналів `database` і `broadcast`, опишіть метод `toDatabase` замість `toArray`.

<a name="accessing-the-notifications"></a>
### Доступ до сповіщень

Щойно сповіщення зберігаються в базі, вам потрібен зручний спосіб звертатися до них із ваших сутностей-отримувачів. Трейт `Illuminate\Notifications\Notifiable`, який підключено до стандартної моделі `App\Models\User` у Laravel, містить [зв'язок Eloquent](/docs/{{version}}/eloquent-relationships) `notifications`, що повертає сповіщення сутності. Щоб дістати сповіщення, звертайтеся до цього методу як до будь-якого іншого зв'язку Eloquent. За замовчуванням сповіщення сортуються за міткою часу `created_at`, і найновіші стоять на початку колекції:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

Якщо ви хочете дістати лише «непрочитані» сповіщення, скористайтеся зв'язком `unreadNotifications`. Знову ж таки, ці сповіщення сортуються за міткою часу `created_at`, і найновіші стоять на початку колекції:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

Якщо ви хочете дістати лише «прочитані» сповіщення, скористайтеся зв'язком `readNotifications`:

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> Щоб звертатися до сповіщень із клієнта на JavaScript, опишіть у застосунку контролер сповіщень, який повертає сповіщення сутності-отримувача - наприклад, поточного користувача. Далі ви можете робити HTTP-запит на URL цього контролера зі свого JavaScript-клієнта.

<a name="marking-notifications-as-read"></a>
### Позначення сповіщень прочитаними

Зазвичай вам захочеться позначати сповіщення «прочитаним», коли користувач його переглядає. Трейт `Illuminate\Notifications\Notifiable` надає метод `markAsRead`, який оновлює стовпець `read_at` у записі сповіщення:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

Проте, замість проходити кожне сповіщення в циклі, ви можете викликати метод `markAsRead` безпосередньо на колекції сповіщень:

```php
$user->unreadNotifications->markAsRead();
```

Ви також можете скористатися масовим оновленням, щоб позначити всі сповіщення прочитаними, не діставши їх із бази:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

Щоб цілком вилучити сповіщення з таблиці, ви можете їх видалити методом `delete`:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## Сповіщення через бродкастинг

<a name="broadcast-prerequisites"></a>
### Передумови

Перш ніж надсилати сповіщення бродкастингом, налаштуйте сервіси [бродкастингу подій](/docs/{{version}}/broadcasting) Laravel і ознайомтеся з ними. Бродкастинг подій дає спосіб реагувати на серверні події Laravel із вашого фронтенду на JavaScript.

<a name="formatting-broadcast-notifications"></a>
### Форматування сповіщень бродкастингу

Канал `broadcast` надсилає сповіщення через сервіси [бродкастингу подій](/docs/{{version}}/broadcasting) Laravel, дозволяючи вашому фронтенду на JavaScript ловити сповіщення в реальному часі. Якщо сповіщення підтримує бродкастинг, опишіть у його класі метод `toBroadcast`. Цей метод отримає сутність `$notifiable` і має повернути екземпляр `BroadcastMessage`. Якщо методу `toBroadcast` немає, дані для надсилання буде зібрано методом `toArray`. Повернені дані буде закодовано в JSON і надіслано вашому фронтенду. Погляньмо на приклад методу `toBroadcast`:

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the broadcastable representation of the notification.
 */
public function toBroadcast(object $notifiable): BroadcastMessage
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
#### Конфігурація черги бродкастингу

Усі сповіщення бродкастингу потрапляють у чергу. Якщо ви хочете налаштувати підключення чи ім'я черги, яку використовує операція бродкастингу, скористайтеся методами `onConnection` та `onQueue` класу `BroadcastMessage`:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### Налаштування типу сповіщення

Окрім вказаних вами даних, усі сповіщення бродкастингу мають поле `type` із повною назвою класу сповіщення. Якщо ви хочете змінити `type` сповіщення, опишіть у його класі метод `broadcastType`:

```php
/**
 * Get the type of the notification being broadcast.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### Прослуховування сповіщень

Сповіщення надсилаються в приватний канал, назва якого будується за домовленістю `{notifiable}.{id}`. Тож, якщо ви надсилаєте сповіщення екземпляру `App\Models\User` з ID `1`, сповіщення буде надіслано в приватний канал `App.Models.User.1`. Користуючись [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation), ви можете легко слухати сповіщення в каналі методом `notification`:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### Використання React, Vue чи Svelte

Laravel Echo містить хуки для React, Vue та Svelte, які роблять прослуховування сповіщень безболісним. Для початку викличте хук `useEchoNotification`, який слухає сповіщення. Хук `useEchoNotification` автоматично виходить з каналів, коли компонент, який його використовує, демонтується:

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEchoNotification } from "@laravel/echo-svelte";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```

За замовчуванням хук слухає всі сповіщення. Щоб указати типи сповіщень, які ви хочете слухати, передайте до `useEchoNotification` рядок або масив типів:

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```

```svelte tab=Svelte
<script>
import { useEchoNotification } from "@laravel/echo-svelte";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```

Ви також можете описати форму даних сповіщення, отримавши кращу типобезпеку й зручність редагування:

```ts
type InvoicePaidNotification = {
    invoice_id: number;
    created_at: string;
};

useEchoNotification<InvoicePaidNotification>(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.invoice_id);
        console.log(notification.created_at);
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

<a name="customizing-the-notification-channel"></a>
#### Налаштування каналу сповіщень

Якщо ви хочете змінити канал, у який надсилаються сповіщення бродкастингу для сутності, опишіть у цій сутності метод `receivesBroadcastNotificationsOn`:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The channels the user receives notification broadcasts on.
     */
    public function receivesBroadcastNotificationsOn(): string
    {
        return 'users.'.$this->id;
    }
}
```

<a name="sms-notifications"></a>
## SMS-сповіщення

<a name="sms-prerequisites"></a>
### Передумови

Надсилання SMS-сповіщень у Laravel працює на [Vonage](https://www.vonage.com/) (раніше відомий як Nexmo). Перш ніж надсилати сповіщення через Vonage, вам потрібно встановити пакети `laravel/vonage-notification-channel` та `guzzlehttp/guzzle`:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

Пакет містить [файл конфігурації](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php). Проте експортувати цей файл до свого застосунку не обов'язково. Ви можете просто скористатися змінними середовища `VONAGE_KEY` та `VONAGE_SECRET`, щоб задати свої публічний і секретний ключі Vonage.

Задавши ключі, встановіть змінну середовища `VONAGE_SMS_FROM`, яка визначає номер телефону, з якого за замовчуванням надсилатимуться ваші SMS. Цей номер можна згенерувати в панелі керування Vonage:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### Форматування SMS-сповіщень

Якщо сповіщення можна надсилати як SMS, опишіть у класі сповіщення метод `toVonage`. Цей метод отримає сутність `$notifiable` і має повернути екземпляр `Illuminate\Notifications\Messages\VonageMessage`:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### Вміст у Unicode

Якщо ваше SMS міститиме символи Unicode, викличте метод `unicode` під час створення екземпляра `VonageMessage`:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### Налаштування номера «From»

Якщо ви хочете надсилати деякі сповіщення з номера, відмінного від указаного змінною середовища `VONAGE_SMS_FROM`, викличте метод `from` на екземплярі `VonageMessage`:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### Додавання клієнтського посилання

Якщо ви хочете відстежувати витрати за користувачем, командою чи клієнтом, додайте до сповіщення «клієнтське посилання». Vonage дозволить будувати звіти за цим посиланням, щоб ви краще розуміли, скільки SMS витрачає конкретний клієнт. Клієнтське посилання може бути будь-яким рядком до 40 символів:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### Маршрутизація SMS-сповіщень

Щоб спрямувати сповіщення Vonage на потрібний номер телефону, опишіть у своїй сутності-отримувачі метод `routeNotificationForVonage`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Vonage channel.
     */
    public function routeNotificationForVonage(Notification $notification): string
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
## Сповіщення в Slack

<a name="slack-prerequisites"></a>
### Передумови

Перш ніж надсилати сповіщення в Slack, встановіть канал сповіщень Slack через Composer:

```shell
composer require laravel/slack-notification-channel
```

Крім того, вам потрібно створити [застосунок Slack](https://api.slack.com/apps?new_app=1) для свого робочого простору Slack.

Якщо вам треба надсилати сповіщення лише до того робочого простору, у якому створено застосунок, переконайтеся, що ваш застосунок має скопи `chat:write`, `chat:write.public` та `chat:write.customize`. Ці скопи додаються на вкладці керування застосунком «OAuth & Permissions» у Slack.

Далі скопіюйте «Bot User OAuth Token» застосунку й покладіть його в масив конфігурації `slack` у файлі `services.php` вашого застосунку. Цей токен можна знайти на вкладці «OAuth & Permissions» у Slack:

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### Розповсюдження застосунку

Якщо ваш застосунок надсилатиме сповіщення до зовнішніх робочих просторів Slack, які належать вашим користувачам, вам потрібно «розповсюдити» свій застосунок через Slack. Розповсюдженням керують на вкладці «Manage Distribution» вашого застосунку в Slack. Щойно застосунок розповсюджено, ви можете скористатися [Socialite](/docs/{{version}}/socialite), щоб [отримувати бот-токени Slack](/docs/{{version}}/socialite#slack-bot-scopes) від імені користувачів вашого застосунку.

<a name="formatting-slack-notifications"></a>
### Форматування сповіщень Slack

Якщо сповіщення можна надсилати як повідомлення Slack, опишіть у класі сповіщення метод `toSlack`. Цей метод отримає сутність `$notifiable` і має повернути екземпляр `Illuminate\Notifications\Slack\SlackMessage`. Ви можете будувати насичені сповіщення за допомогою [Block Kit API від Slack](https://api.slack.com/block-kit). Приклад нижче можна переглянути в [конструкторі Block Kit від Slack](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D):

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
            $block->field("*Invoice No:*\n1000")->markdown();
            $block->field("*Invoice Recipient:*\ntaylor@laravel.com")->markdown();
        })
        ->dividerBlock()
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('Congratulations!');
        });
}
```

<a name="using-slacks-block-kit-builder-template"></a>
#### Використання шаблону з конструктора Block Kit

Замість плавних методів побудови повідомлення ви можете передати сирі JSON-дані, згенеровані конструктором Block Kit від Slack, методу `usingBlockKitTemplate`:

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    $template = <<<JSON
        {
          "blocks": [
            {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": "Team Announcement"
              }
            },
            {
              "type": "section",
              "text": {
                "type": "plain_text",
                "text": "We are hiring!"
              }
            }
          ]
        }
    JSON;

    return (new SlackMessage)
        ->usingBlockKitTemplate($template);
}
```

<a name="slack-interactivity"></a>
### Інтерактивність Slack

Система сповіщень Block Kit від Slack надає потужні можливості для [обробки взаємодії з користувачем](https://api.slack.com/interactivity/handling). Щоб ними скористатися, у вашому застосунку Slack має бути увімкнено «Interactivity» і налаштовано «Request URL», який вказує на URL вашого застосунку. Ці налаштування керуються на вкладці «Interactivity & Shortcuts» вашого застосунку в Slack.

У прикладі нижче, який використовує метод `actionsBlock`, Slack надішле `POST`-запит на ваш «Request URL» із даними про користувача Slack, який натиснув кнопку, ID натиснутої кнопки тощо. Далі ваш застосунок може визначити, яку дію виконати, на основі цих даних. Вам також слід [перевіряти, що запит](https://api.slack.com/authentication/verifying-requests-from-slack) справді надійшов від Slack:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
             // ID defaults to "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // Manually configure the ID...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### Модальні вікна підтвердження

Якщо ви хочете, щоб користувачі підтверджували дію перед її виконанням, викличте метод `confirm` під час опису кнопки. Метод `confirm` приймає повідомлення й замикання, яке отримує екземпляр `ConfirmObject`:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
            $block->button('Acknowledge Invoice')
                ->primary()
                ->confirm(
                    'Acknowledge the payment and send a thank you email?',
                    function (ConfirmObject $dialog) {
                        $dialog->confirm('Yes');
                        $dialog->deny('No');
                    }
                );
        });
}
```

<a name="inspecting-slack-blocks"></a>
#### Огляд блоків Slack

Якщо ви хочете швидко оглянути блоки, які будуєте, викличте метод `dd` на екземплярі `SlackMessage`. Метод `dd` згенерує й виведе URL до [конструктора Block Kit](https://app.slack.com/block-kit-builder/) від Slack, який покаже попередній перегляд даних і сповіщення у вашому браузері. Ви можете передати методу `dd` значення `true`, щоб вивести сирі дані:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Маршрутизація сповіщень Slack

Щоб спрямувати сповіщення Slack до потрібної команди й каналу, опишіть у своїй моделі-отримувачі метод `routeNotificationForSlack`. Цей метод може повернути одне з трьох значень:

- `null` - тоді маршрутизацію віддано каналу, налаштованому в самому сповіщенні. Ви можете скористатися методом `to` під час побудови `SlackMessage`, щоб налаштувати канал у сповіщенні.
- Рядок із каналом Slack, до якого слід надіслати сповіщення, наприклад `#support-channel`.
- Екземпляр `SlackRoute`, який дозволяє вказати OAuth-токен і назву каналу, наприклад `SlackRoute::make($this->slack_channel, $this->slack_token)`. Цей спосіб слід використовувати для надсилання сповіщень до зовнішніх робочих просторів.

Наприклад, якщо метод `routeNotificationForSlack` поверне `#support-channel`, сповіщення буде надіслано в канал `#support-channel` того робочого простору, який пов'язано з токеном Bot User OAuth із файлу `services.php` вашого застосунку:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```

<a name="notifying-external-slack-workspaces"></a>
### Сповіщення зовнішніх робочих просторів Slack

> [!NOTE]
> Перш ніж надсилати сповіщення до зовнішніх робочих просторів Slack, ваш застосунок Slack має бути [розповсюджено](#slack-app-distribution).

Звісно, часто вам захочеться надсилати сповіщення до робочих просторів Slack, які належать користувачам вашого застосунку. Для цього спершу потрібно отримати OAuth-токен Slack для користувача. На щастя, [Laravel Socialite](/docs/{{version}}/socialite) містить драйвер Slack, який дозволяє легко автентифікувати користувачів вашого застосунку в Slack і [отримати бот-токен](/docs/{{version}}/socialite#slack-bot-scopes).

Щойно ви отримали бот-токен і зберегли його в базі даних свого застосунку, скористайтеся методом `SlackRoute::make`, щоб спрямувати сповіщення до робочого простору користувача. Крім того, вашому застосунку, найімовірніше, треба буде дати користувачеві змогу вказати, до якого каналу надсилати сповіщення:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Slack\SlackRoute;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## Локалізація сповіщень

Laravel дозволяє надсилати сповіщення в локалі, відмінній від поточної локалі HTTP-запиту, і навіть запам'ятає цю локаль, якщо сповіщення поставлено в чергу.

Для цього клас `Illuminate\Notifications\Notification` пропонує метод `locale`, щоб задати потрібну мову. Застосунок перейде в цю локаль під час обчислення сповіщення, а після завершення повернеться до попередньої:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

Локалізації для кількох отримувачів можна досягти й через фасад `Notification`:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### Бажані локалі користувачів

Інколи застосунки зберігають бажану локаль кожного користувача. Реалізувавши у своїй моделі-отримувачі контракт `HasLocalePreference`, ви можете сказати Laravel використовувати цю збережену локаль під час надсилання сповіщення:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

Щойно ви реалізували цей інтерфейс, Laravel автоматично використовуватиме бажану локаль, надсилаючи моделі сповіщення та листи. Тому викликати метод `locale` при використанні цього інтерфейсу не потрібно:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## Тестування

Метод `fake` фасаду `Notification` дозволяє завадити надсиланню сповіщень. Зазвичай надсилання сповіщень не стосується коду, який ви насправді тестуєте. Найімовірніше, достатньо просто перевірити, що Laravel отримав вказівку надіслати задане сповіщення.

Після виклику методу `fake` фасаду `Notification` ви можете перевіряти, що сповіщення мали бути надіслані користувачам, і навіть оглядати дані, які вони отримали:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // Perform order shipping...

    // Assert that no notifications were sent...
    Notification::assertNothingSent();

    // Assert a notification was sent to the given users...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // Assert a notification was not sent...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // Assert a notification was sent twice...
    Notification::assertSentTimes(WeeklyReminder::class, 2);

    // Assert that a given number of notifications were sent...
    Notification::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Notification::fake();

        // Perform order shipping...

        // Assert that no notifications were sent...
        Notification::assertNothingSent();

        // Assert a notification was sent to the given users...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // Assert a notification was not sent...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // Assert a notification was sent twice...
        Notification::assertSentTimes(WeeklyReminder::class, 2);

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```

Ви можете передати замикання методам `assertSentTo` чи `assertNotSentTo`, щоб перевірити, що було надіслано сповіщення, яке проходить заданий тест. Якщо надіслано щонайменше одне сповіщення, яке проходить цей тест, перевірка буде успішною:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="testing-on-demand-notifications"></a>
#### Сповіщення на льоту

Якщо код, який ви тестуєте, надсилає [сповіщення на льоту](#on-demand-notifications), перевірити це можна методом `assertSentOnDemand`:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

Передавши замикання другим аргументом методу `assertSentOnDemand`, ви можете визначити, чи надіслано сповіщення на льоту за правильною «маршрутною» адресою:

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="notification-events"></a>
## Події сповіщень

<a name="notification-sending-event"></a>
#### Подія надсилання сповіщення

Коли сповіщення надсилається, система сповіщень диспетчеризує подію `Illuminate\Notifications\Events\NotificationSending`. Вона містить сутність-отримувача та сам екземпляр сповіщення. Ви можете створити [слухачів подій](/docs/{{version}}/events) для цієї події у своєму застосунку:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

Сповіщення не буде надіслано, якщо слухач події `NotificationSending` поверне зі свого методу `handle` значення `false`:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

Усередині слухача ви можете звернутися до властивостей події `notifiable`, `notification` і `channel`, щоб дізнатися більше про отримувача сповіщення чи саме сповіщення:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### Подія надісланого сповіщення

Коли сповіщення надіслано, система сповіщень диспетчеризує [подію](/docs/{{version}}/events) `Illuminate\Notifications\Events\NotificationSent`. Вона містить сутність-отримувача та сам екземпляр сповіщення. Ви можете створити [слухачів подій](/docs/{{version}}/events) для цієї події у своєму застосунку:

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

Усередині слухача ви можете звернутися до властивостей події `notifiable`, `notification`, `channel` та `response`, щоб дізнатися більше про отримувача сповіщення чи саме сповіщення:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSent $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
## Власні канали

Laravel постачається з кількома каналами сповіщень, але ви можете захотіти написати власні драйвери для доставки сповіщень іншими каналами. Laravel це спрощує. Для початку опишіть клас, який містить метод `send`. Цей метод має приймати два аргументи: `$notifiable` та `$notification`.

У методі `send` ви можете викликати методи сповіщення, щоб отримати об'єкт повідомлення, зрозумілий вашому каналу, а потім надіслати сповіщення екземпляру `$notifiable` як заманеться:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * Send the given notification.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // Send notification to the $notifiable instance...
    }
}
```

Щойно клас вашого каналу сповіщень описано, ви можете повертати його назву з методу `via` будь-якого зі своїх сповіщень. У цьому прикладі метод `toVoice` вашого сповіщення може повертати будь-який об'єкт на ваш вибір, який представляє голосові повідомлення. Наприклад, ви можете описати власний клас `VoiceMessage`:

```php
<?php

namespace App\Notifications;

use App\Notifications\Messages\VoiceMessage;
use App\Notifications\VoiceChannel;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification
{
    use Queueable;

    /**
     * Get the notification channels.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * Get the voice representation of the notification.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```
