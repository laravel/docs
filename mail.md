---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Пошта

- [Вступ](#introduction)
    - [Конфігурація](#configuration)
    - [Передумови драйверів](#driver-prerequisites)
    - [Конфігурація failover](#failover-configuration)
    - [Конфігурація round robin](#round-robin-configuration)
- [Генерація mailable-класів](#generating-mailables)
- [Написання mailable-класів](#writing-mailables)
    - [Налаштування відправника](#configuring-the-sender)
    - [Налаштування представлення](#configuring-the-view)
    - [Дані представлення](#view-data)
    - [Вкладення](#attachments)
    - [Вбудовані вкладення](#inline-attachments)
    - [Об'єкти, придатні для вкладення](#attachable-objects)
    - [Заголовки](#headers)
    - [Теги й метадані](#tags-and-metadata)
    - [Налаштування повідомлення Symfony](#customizing-the-symfony-message)
- [Markdown-листи](#markdown-mailables)
    - [Генерація Markdown-листів](#generating-markdown-mailables)
    - [Написання Markdown-повідомлень](#writing-markdown-messages)
    - [Налаштування компонентів](#customizing-the-components)
- [Надсилання пошти](#sending-mail)
    - [Пошта в черзі](#queueing-mail)
- [Рендеринг mailable-класів](#rendering-mailables)
    - [Попередній перегляд листів у браузері](#previewing-mailables-in-the-browser)
- [Локалізація листів](#localizing-mailables)
- [Тестування](#testing-mailables)
    - [Тестування вмісту листа](#testing-mailable-content)
    - [Тестування надсилання листа](#testing-mailable-sending)
- [Пошта й локальна розробка](#mail-and-local-development)
- [Події](#events)
- [Власні транспорти](#custom-transports)
    - [Додаткові транспорти Symfony](#additional-symfony-transports)

<a name="introduction"></a>
## Вступ

Надсилання пошти не мусить бути складним. Laravel надає чистий і простий API для електронної пошти, побудований на популярному компоненті [Symfony Mailer](https://symfony.com/doc/current/mailer.html). Laravel і Symfony Mailer надають драйвери для надсилання пошти через SMTP, Cloudflare, Mailgun, Postmark, Resend, Amazon SES та `sendmail`, тож ви можете швидко почати надсилати пошту через локальний чи хмарний сервіс на свій вибір.

<a name="configuration"></a>
### Конфігурація

Поштові сервіси Laravel налаштовуються у файлі `config/mail.php` вашого застосунку. Кожен налаштований у цьому файлі мейлер може мати власну унікальну конфігурацію й навіть власний унікальний «транспорт», що дозволяє застосунку надсилати різні повідомлення через різні поштові сервіси. Наприклад, ваш застосунок може надсилати транзакційні листи через Postmark, а масові розсилки - через Amazon SES.

У файлі конфігурації `mail` ви знайдете масив конфігурації `mailers`. Цей масив містить зразок конфігурації для кожного з основних поштових драйверів / транспортів, які підтримує Laravel, а значення конфігурації `default` визначає, який мейлер використовуватиметься за замовчуванням, коли вашому застосунку треба надіслати листа.

<a name="driver-prerequisites"></a>
### Передумови драйверів / транспортів

Драйвери на основі API - Mailgun, Postmark і Resend - часто простіші та швидші за надсилання пошти через SMTP-сервери. Коли це можливо, ми радимо користуватися одним із них.

<a name="cloudflare-driver"></a>
#### Драйвер Cloudflare

Щоб скористатися драйвером Cloudflare, встановіть HTTP-клієнт Symfony через Composer:

```shell
composer require symfony/http-client
```

Далі вам потрібно внести дві зміни у файл конфігурації `config/mail.php` вашого застосунку. Спершу задайте мейлером за замовчуванням `cloudflare`:

```php
'default' => env('MAIL_MAILER', 'cloudflare'),
```

По-друге, додайте такий масив конфігурації до вашого масиву `mailers`:

```php
'cloudflare' => [
    'transport' => 'cloudflare',
],
```

Налаштувавши мейлер за замовчуванням, додайте такі опції до файлу конфігурації `config/services.php`:

```php
'cloudflare' => [
    'account_id' => env('CLOUDFLARE_ACCOUNT_ID'),
    'key' => env('CLOUDFLARE_KEY'),
],
```

<a name="mailgun-driver"></a>
#### Драйвер Mailgun

Щоб скористатися драйвером Mailgun, встановіть транспорт Mailgun Mailer від Symfony через Composer:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

Далі вам потрібно внести дві зміни у файл конфігурації `config/mail.php` вашого застосунку. Спершу задайте мейлером за замовчуванням `mailgun`:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

По-друге, додайте такий масив конфігурації до вашого масиву `mailers`:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

Налаштувавши мейлер за замовчуванням, додайте такі опції до файлу конфігурації `config/services.php`:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

Якщо ви не користуєтеся [регіоном Mailgun](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview#mailgun-regions) для США, вкажіть точку свого регіону у файлі конфігурації `services`:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```

<a name="postmark-driver"></a>
#### Драйвер Postmark

Щоб скористатися драйвером [Postmark](https://postmarkapp.com/), встановіть транспорт Postmark Mailer від Symfony через Composer:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

Далі задайте опції `default` у файлі `config/mail.php` вашого застосунку значення `postmark`. Налаштувавши мейлер за замовчуванням, переконайтеся, що файл конфігурації `config/services.php` містить такі опції:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

Якщо ви хочете вказати потік повідомлень Postmark, який має використовувати конкретний мейлер, додайте до його масиву конфігурації опцію `message_stream_id`. Цей масив конфігурації лежить у файлі `config/mail.php` вашого застосунку:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

Так ви можете налаштувати й кілька мейлерів Postmark з різними потоками повідомлень.

<a name="resend-driver"></a>
#### Драйвер Resend

Щоб скористатися драйвером [Resend](https://resend.com/), встановіть PHP SDK від Resend через Composer:

```shell
composer require resend/resend-php
```

Далі задайте опції `default` у файлі `config/mail.php` вашого застосунку значення `resend`. Налаштувавши мейлер за замовчуванням, переконайтеся, що файл конфігурації `config/services.php` містить такі опції:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### Драйвер SES

Щоб скористатися драйвером Amazon SES, спершу встановіть Amazon AWS SDK для PHP. Цю бібліотеку можна встановити через менеджер пакетів Composer:

```shell
composer require aws/aws-sdk-php
```

Далі задайте опції `default` у файлі `config/mail.php` значення `ses` і переконайтеся, що файл конфігурації `config/services.php` містить такі опції:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

Щоб скористатися [тимчасовими обліковими даними](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) AWS через токен сесії, додайте ключ `token` до конфігурації SES вашого застосунку:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

Щоб працювати з [можливостями керування підписками](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html) SES, поверніть заголовок `X-Ses-List-Management-Options` у масиві, який повертає метод [headers](#headers) поштового повідомлення:

```php
/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',
        ],
    );
}
```

Якщо ви хочете описати [додаткові опції](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail), які Laravel має передавати методу `SendEmail` з AWS SDK під час надсилання листа, опишіть масив `options` у своїй конфігурації `ses`:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'options' => [
        'ConfigurationSetName' => 'MyConfigurationSet',
        'EmailTags' => [
            ['Name' => 'foo', 'Value' => 'bar'],
        ],
    ],
],
```

<a name="failover-configuration"></a>
### Конфігурація failover

Інколи зовнішній сервіс, який ви налаштували для надсилання пошти, може бути недоступним. У таких випадках корисно описати одну чи кілька резервних конфігурацій доставки, які використовуватимуться, якщо основний драйвер лежить.

Для цього опишіть у файлі конфігурації `mail` мейлер, який використовує транспорт `failover`. Масив конфігурації мейлера `failover` має містити масив `mailers` із порядком, у якому слід обирати налаштовані мейлери для доставки:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

Щойно ви налаштували мейлер із транспортом `failover`, вам потрібно зробити його мейлером за замовчуванням у файлі `.env` вашого застосунку, щоб скористатися цією можливістю:

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### Конфігурація round robin

Транспорт `roundrobin` дозволяє розподілити навантаження з надсилання пошти між кількома мейлерами. Для початку опишіть у файлі конфігурації `mail` мейлер, який використовує транспорт `roundrobin`. Масив конфігурації мейлера `roundrobin` має містити масив `mailers` із переліком налаштованих мейлерів, які слід використовувати для доставки:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

Щойно ваш мейлер round robin описано, зробіть його мейлером за замовчуванням, вказавши його ім'я значенням ключа конфігурації `default` у файлі `mail` вашого застосунку:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

Транспорт round robin обирає випадковий мейлер зі списку налаштованих, а для кожного наступного листа перемикається на наступний доступний. На відміну від транспорту `failover`, який допомагає досягти *[високої доступності](https://en.wikipedia.org/wiki/High_availability)*, транспорт `roundrobin` забезпечує *[балансування навантаження](https://en.wikipedia.org/wiki/Load_balancing_(computing))*.

<a name="generating-mailables"></a>
## Генерація mailable-класів

Створюючи застосунки Laravel, кожен тип листа, який надсилає ваш застосунок, представляють класом «mailable». Ці класи зберігаються в каталозі `app/Mail`. Не переймайтеся, якщо цього каталогу у вашому застосунку немає: його буде згенеровано, коли ви створите свій перший mailable-клас командою Artisan `make:mail`:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Написання mailable-класів

Щойно ви згенерували mailable-клас, відкрийте його, щоб дослідити вміст. Конфігурація mailable-класу відбувається в кількох методах: `envelope`, `content` та `attachments`.

Метод `envelope` повертає об'єкт `Illuminate\Mail\Mailables\Envelope`, який описує тему і, часом, отримувачів повідомлення. Метод `content` повертає об'єкт `Illuminate\Mail\Mailables\Content`, який описує [шаблон Blade](/docs/{{version}}/blade), що згенерує вміст повідомлення.

<a name="configuring-the-sender"></a>
### Налаштування відправника

<a name="using-the-envelope"></a>
#### Через конверт

Спершу розгляньмо налаштування відправника листа. Іншими словами, від кого лист. Налаштувати відправника можна двома способами. По-перше, ви можете вказати адресу «from» у конверті повідомлення:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

За бажанням ви можете вказати й адресу `replyTo`:

```php
return new Envelope(
    from: new Address('jeffrey@example.com', 'Jeffrey Way'),
    replyTo: [
        new Address('taylor@example.com', 'Taylor Otwell'),
    ],
    subject: 'Order Shipped',
);
```

<a name="using-a-global-from-address"></a>
#### Глобальна адреса `from`

Проте, якщо ваш застосунок використовує ту саму адресу «from» для всіх листів, додавати її до кожного згенерованого mailable-класу стає обтяжливо. Натомість ви можете вказати глобальну адресу «from» у файлі конфігурації `config/mail.php`. Ця адреса використовуватиметься, якщо в mailable-класі не вказано іншої адреси «from»:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

Крім того, ви можете описати глобальну адресу «reply_to» у файлі конфігурації `config/mail.php`:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### Налаштування представлення

У методі `content` mailable-класу ви можете описати `view`, тобто шаблон, який слід використати для рендерингу вмісту листа. Оскільки кожен лист зазвичай рендерить свій вміст [шаблоном Blade](/docs/{{version}}/blade), під час створення HTML вашого листа вам доступні вся потуга й зручність шаблонізатора Blade:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]
> Вам може захотітися створити каталог `resources/views/mail`, щоб зібрати там усі шаблони листів; утім, ви вільні класти їх будь-де в каталозі `resources/views`.

<a name="plain-text-emails"></a>
#### Листи у простому тексті

Якщо ви хочете описати текстову версію свого листа, вкажіть текстовий шаблон під час створення опису `Content`. Як і параметр `view`, параметр `text` має бути назвою шаблону, який відрендерить вміст листа. Ви вільні описати і HTML-, і текстову версію свого повідомлення:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

Задля ясності параметр `html` можна використовувати як аліас параметра `view`:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### Дані представлення

<a name="via-public-properties"></a>
#### Через публічні властивості

Зазвичай вам захочеться передати до представлення дані, які можна використати під час рендерингу HTML листа. Зробити дані доступними для представлення можна двома способами. По-перше, будь-яка публічна властивість, описана у вашому mailable-класі, автоматично стане доступною представленню. Тож ви можете передати дані в конструктор mailable-класу й записати їх у публічні властивості класу:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

Щойно дані записано в публічну властивість, вони автоматично стануть доступні у вашому представленні, тож ви можете звертатися до них як до будь-яких інших даних у шаблонах Blade:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### Через параметр `with`:

Якщо ви хочете змінити формат даних листа перед тим, як вони потраплять до шаблону, ви можете передати дані до представлення вручну через параметр `with` опису `Content`. Зазвичай ви все одно передаєте дані в конструктор mailable-класу; проте записуйте їх у властивості `protected` чи `private`, щоб дані не потрапляли до шаблону автоматично:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```

Щойно дані передано через параметр `with`, вони автоматично стануть доступні у вашому представленні, тож ви можете звертатися до них як до будь-яких інших даних у шаблонах Blade:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### Вкладення

Щоб додати вкладення до листа, додайте їх до масиву, який повертає метод `attachments` повідомлення. По-перше, ви можете додати вкладення, передавши шлях до файлу методу `fromPath` класу `Attachment`:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```

Вкладаючи файли до повідомлення, ви можете вказати відображувану назву та / або MIME-тип вкладення методами `as` і `withMime`:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="attaching-files-from-disk"></a>
#### Вкладення файлів з диска

Якщо ви зберегли файл на одному з [дисків файлової системи](/docs/{{version}}/filesystem), вкласти його до листа можна методом `fromStorage`:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

Звісно, ви також можете вказати назву та MIME-тип вкладення:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

Метод `fromStorageDisk` дозволяє вказати диск, відмінний від диска за замовчуванням:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorageDisk('s3', '/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="raw-data-attachments"></a>
#### Вкладення сирих даних

Метод `fromData` дозволяє вкласти сирий рядок байтів як вкладення. Наприклад, ви можете скористатися цим методом, якщо згенерували PDF у пам'яті й хочете вкласти його до листа, не записуючи на диск. Метод `fromData` приймає замикання, яке повертає сирі байти даних, і назву, яку слід призначити вкладенню:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="inline-attachments"></a>
### Вбудовані вкладення

Вбудовувати зображення в листи зазвичай марудно; проте Laravel надає зручний спосіб вкладати зображення до ваших листів. Щоб вбудувати зображення, скористайтеся методом `embed` змінної `$message` у шаблоні листа. Laravel автоматично робить змінну `$message` доступною в усіх ваших шаблонах листів, тож передавати її вручну не потрібно:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> Змінна `$message` недоступна в шаблонах повідомлень у простому тексті, адже такі повідомлення не використовують вбудованих вкладень.

<a name="embedding-raw-data-attachments"></a>
#### Вбудовування вкладень із сирих даних

Якщо ви вже маєте рядок сирих даних зображення, який хочете вбудувати в шаблон листа, викличте метод `embedData` змінної `$message`. Викликаючи метод `embedData`, вам потрібно передати ім'я файлу, яке слід призначити вбудованому зображенню:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Об'єкти, придатні для вкладення

Хоч вкладати файли до повідомлень простими рядковими шляхами часто й достатньо, у багатьох випадках сутності, які ви вкладаєте, представлені у вашому застосунку класами. Наприклад, якщо ваш застосунок вкладає до повідомлення фото, у ньому може бути й модель `Photo`, яка це фото представляє. Хіба не було б зручно просто передати модель `Photo` методу `attach`? Об'єкти, придатні для вкладення, дозволяють саме це.

Для початку реалізуйте інтерфейс `Illuminate\Contracts\Mail\Attachable` в об'єкті, який можна буде вкладати до повідомлень. Цей інтерфейс вимагає, щоб ваш клас описав метод `toMailAttachment`, який повертає екземпляр `Illuminate\Mail\Attachment`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * Get the attachable representation of the model.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

Щойно ви описали свій об'єкт для вкладення, ви можете повертати його екземпляр із методу `attachments` під час побудови листа:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

Звісно, дані вкладення можуть зберігатися у віддаленому файловому сховищі на кшталт Amazon S3. Тож Laravel також дозволяє генерувати екземпляри вкладень із даних, збережених на одному з [дисків файлової системи](/docs/{{version}}/filesystem) вашого застосунку:

```php
// Create an attachment from a file on your default disk...
return Attachment::fromStorage($this->path);

// Create an attachment from a file on a specific disk...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

Крім того, ви можете створювати екземпляри вкладень із даних, які маєте в пам'яті. Для цього передайте замикання методу `fromData`. Замикання має повернути сирі дані, які представляють вкладення:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

Laravel також надає додаткові методи для налаштування ваших вкладень. Наприклад, методами `as` і `withMime` ви можете змінити ім'я файлу та MIME-тип:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### Заголовки

Інколи вам може знадобитися додати до вихідного повідомлення додаткові заголовки. Наприклад, вам може знадобитися задати власний `Message-Id` чи інші довільні текстові заголовки.

Для цього опишіть у своєму mailable-класі метод `headers`. Метод `headers` має повернути екземпляр `Illuminate\Mail\Mailables\Headers`. Цей клас приймає параметри `messageId`, `references` та `text`. Звісно, ви можете передати лише ті параметри, які потрібні для конкретного повідомлення:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        messageId: 'custom-message-id@example.com',
        references: ['previous-message@example.com'],
        text: [
            'X-Custom-Header' => 'Custom Value',
        ],
    );
}
```

<a name="tags-and-metadata"></a>
### Теги й метадані

Деякі сторонні поштові провайдери на кшталт Mailgun і Postmark підтримують «теги» й «метадані» повідомлень, які дозволяють групувати та відстежувати листи, надіслані вашим застосунком. Додати теги й метадані до листа можна через опис `Envelope`:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        tags: ['shipment'],
        metadata: [
            'order_id' => $this->order->id,
        ],
    );
}
```

Якщо ваш застосунок використовує драйвер Mailgun, докладніше про [теги](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) та [метадані](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) читайте в документації Mailgun. Так само в документації Postmark можна знайти більше про їхню підтримку [тегів](https://postmarkapp.com/blog/tags-support-for-smtp) і [метаданих](https://postmarkapp.com/support/article/1125-custom-metadata-faq).

Якщо ваш застосунок надсилає листи через Amazon SES, скористайтеся методом `metadata`, щоб додати до повідомлення [«теги» SES](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html).

<a name="customizing-the-symfony-message"></a>
### Налаштування повідомлення Symfony

Поштові можливості Laravel побудовані на Symfony Mailer. Laravel дозволяє реєструвати власні колбеки, які буде викликано з екземпляром Symfony Message перед надсиланням повідомлення. Це дає вам змогу глибоко налаштувати повідомлення перед відправкою. Для цього опишіть параметр `using` у своєму описі `Envelope`:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        using: [
            function (Email $message) {
                // ...
            },
        ]
    );
}
```

<a name="markdown-mailables"></a>
## Markdown-листи

Markdown-листи дозволяють скористатися готовими шаблонами й компонентами [поштових сповіщень](/docs/{{version}}/notifications#mail-notifications) у ваших mailable-класах. Оскільки повідомлення пишуться в Markdown, Laravel може відрендерити для них гарні адаптивні HTML-шаблони, а заразом автоматично згенерувати текстовий відповідник.

<a name="generating-markdown-mailables"></a>
### Генерація Markdown-листів

Щоб згенерувати mailable-клас із відповідним Markdown-шаблоном, скористайтеся опцією `--markdown` команди Artisan `make:mail`:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

Далі, налаштовуючи опис `Content` у методі `content`, використовуйте параметр `markdown` замість `view`:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        markdown: 'mail.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```

<a name="writing-markdown-messages"></a>
### Написання Markdown-повідомлень

Markdown-листи поєднують компоненти Blade і синтаксис Markdown, що дозволяє легко будувати поштові повідомлення, користуючись готовими UI-компонентами Laravel для листів:

```blade
<x-mail::message>
# Order Shipped

Your order has been shipped!

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> [!NOTE]
> Не робіть зайвих відступів, коли пишете Markdown-листи. За стандартами Markdown парсери рендерять вміст із відступами як блоки коду.

<a name="button-component"></a>
#### Компонент button

Компонент button рендерить відцентроване посилання-кнопку. Компонент приймає два аргументи: `url` та необов'язковий `color`. Підтримувані кольори - `primary`, `success` та `error`. Ви можете додати до повідомлення скільки завгодно компонентів button:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### Компонент panel

Компонент panel рендерить заданий блок тексту в панелі, колір тла якої трохи відрізняється від решти повідомлення. Це дозволяє привернути увагу до певного блоку тексту:

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

Ви можете експортувати всі поштові компоненти Markdown до власного застосунку, щоб їх налаштувати. Щоб експортувати компоненти, опублікуйте тег ресурсів `laravel-mail` командою Artisan `vendor:publish`:

```shell
php artisan vendor:publish --tag=laravel-mail
```

Ця команда опублікує поштові компоненти Markdown до каталогу `resources/views/vendor/mail`. Каталог `mail` міститиме каталоги `html` і `text`, у кожному з яких лежатиме відповідне представлення кожного доступного компонента. Ви вільні налаштовувати ці компоненти як заманеться.

<a name="customizing-the-css"></a>
#### Налаштування CSS

Після експорту компонентів каталог `resources/views/vendor/mail/html/themes` міститиме файл `default.css`. Ви можете змінити CSS у цьому файлі, і ваші стилі автоматично буде перетворено на вбудований CSS у HTML-представленнях ваших Markdown-листів.

Якщо ви хочете створити цілком нову тему для компонентів Markdown у Laravel, покладіть CSS-файл у каталог `html/themes`. Назвавши й зберігши свій CSS-файл, оновіть опцію `theme` у файлі конфігурації `config/mail.php` вашого застосунку відповідно до назви нової теми.

Щоб змінити тему для окремого mailable-класу, задайте властивості `$theme` цього класу назву теми, яку слід використати під час надсилання.

<a name="sending-mail"></a>
## Надсилання пошти

Щоб надіслати повідомлення, скористайтеся методом `to` [фасаду](/docs/{{version}}/facades) `Mail`. Метод `to` приймає адресу електронної пошти, екземпляр користувача або колекцію користувачів. Якщо ви передаєте об'єкт чи колекцію об'єктів, мейлер автоматично використає їхні властивості `email` і `name` для визначення отримувачів листа, тож переконайтеся, що ці атрибути є у ваших об'єктах. Щойно ви вказали отримувачів, передайте екземпляр свого mailable-класу методу `send`:

```php
<?php

namespace App\Http\Controllers;

use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Ship the order...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

Надсилаючи повідомлення, ви не обмежені лише отримувачами «to». Ви вільні задати отримувачів «to», «cc» та «bcc», поєднавши відповідні методи ланцюжком:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### Цикл по отримувачах

Інколи вам може знадобитися надіслати лист списку отримувачів, проходячи масив отримувачів / адрес. Проте, оскільки метод `to` додає адреси до списку отримувачів листа, кожна ітерація циклу надсилатиме ще один лист усім попереднім отримувачам. Тому завжди створюйте екземпляр листа заново для кожного отримувача:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### Надсилання через конкретний мейлер

За замовчуванням Laravel надсилає пошту через мейлер, налаштований як `default` у файлі конфігурації `mail` вашого застосунку. Проте ви можете скористатися методом `mailer`, щоб надіслати повідомлення через конкретну конфігурацію мейлера:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### Пошта в черзі

<a name="queueing-a-mail-message"></a>
#### Постановка листа в чергу

Оскільки надсилання листів може негативно вплинути на час відповіді вашого застосунку, багато розробників ставлять листи в чергу на фонове надсилання. Laravel спрощує це завдяки вбудованому [єдиному API черг](/docs/{{version}}/queues). Щоб поставити лист у чергу, скористайтеся методом `queue` фасаду `Mail` після вказання отримувачів:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

Цей метод автоматично подбає про те, щоб покласти завдання в чергу й надіслати повідомлення у фоні. Перш ніж користуватися цією можливістю, вам потрібно [налаштувати черги](/docs/{{version}}/queues).

<a name="delayed-message-queueing"></a>
#### Відкладена постановка листа в чергу

Якщо ви хочете відкласти доставку листа з черги, скористайтеся методом `later`. Першим аргументом метод `later` приймає екземпляр `DateTime`, який вказує, коли слід надіслати повідомлення:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### Відправка в конкретні черги

Оскільки всі mailable-класи, згенеровані командою `make:mail`, використовують трейт `Illuminate\Bus\Queueable`, ви можете викликати методи `onQueue` та `onConnection` на будь-якому екземплярі mailable-класу, щоб вказати підключення та ім'я черги для повідомлення:

```php
$message = (new OrderShipped($order))
    ->onConnection('sqs')
    ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```

Як варіант, ви можете вказати підключення й чергу атрибутами `Connection` та `Queue` у mailable-класі:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('emails')]
class OrderShipped extends Mailable
{
    // ...
}
```

<a name="queueing-by-default"></a>
#### Постановка в чергу за замовчуванням

Якщо у вас є mailable-класи, які ви хочете завжди ставити в чергу, реалізуйте в них контракт `ShouldQueue`. Тепер, навіть якщо ви викличете метод `send`, лист усе одно потрапить у чергу, адже клас реалізує цей контракт:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### Листи в черзі та транзакції бази даних

Коли листи в черзі диспетчеризуються всередині транзакцій бази даних, черга може обробити їх ще до того, як транзакцію буде зафіксовано. Коли таке трапляється, будь-які зміни, які ви внесли до моделей чи записів у базі під час транзакції, ще можуть не бути в базі. Ба більше, будь-які моделі чи записи, створені всередині транзакції, можуть у базі не існувати. Якщо ваш лист залежить від цих моделей, під час обробки завдання, яке його надсилає, можуть виникнути несподівані помилки.

Якщо опція конфігурації `after_commit` вашого підключення черги має значення `false`, ви все одно можете вказати, що конкретний лист у черзі слід диспетчеризувати після фіксації всіх відкритих транзакцій, - викличте метод `afterCommit` під час надсилання повідомлення:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

Як варіант, ви можете викликати метод `afterCommit` у конструкторі свого mailable-класу:

```php
<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> Щоб дізнатися більше про обхід цих проблем, перегляньте документацію про [завдання в черзі та транзакції бази даних](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="queued-email-failures"></a>
#### Невдачі листів у черзі

Коли лист у черзі зазнає невдачі, у mailable-класі буде викликано метод `failed`, якщо його описано. До методу `failed` буде передано екземпляр `Throwable`, який спричинив невдачу:

```php
<?php

namespace App\Mail;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Throwable;

class OrderDelayed extends Mailable implements ShouldQueue
{
    use SerializesModels;

    /**
     * Handle a queued email's failure.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## Рендеринг mailable-класів

Інколи вам може захотітися отримати HTML-вміст листа, не надсилаючи його. Для цього викличте метод `render` на mailable-класі. Цей метод поверне обчислений HTML-вміст листа рядком:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### Попередній перегляд листів у браузері

Розробляючи шаблон листа, зручно швидко переглядати відрендерений лист у браузері, як звичайний шаблон Blade. Тому Laravel дозволяє повертати будь-який mailable-клас напряму із замикання маршруту чи контролера. Коли повернуто mailable-клас, його буде відрендерено й показано в браузері, тож ви зможете швидко переглянути дизайн, не надсилаючи листа на справжню адресу:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## Локалізація листів

Laravel дозволяє надсилати листи в локалі, відмінній від поточної локалі запиту, і навіть запам'ятає цю локаль, якщо лист поставлено в чергу.

Для цього фасад `Mail` пропонує метод `locale`, щоб задати потрібну мову. Застосунок перейде в цю локаль під час обчислення шаблону листа, а після завершення повернеться до попередньої:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### Бажані локалі користувачів

Інколи застосунки зберігають бажану локаль кожного користувача. Реалізувавши в одній чи кількох своїх моделях контракт `HasLocalePreference`, ви можете сказати Laravel використовувати цю збережену локаль під час надсилання пошти:

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

Щойно ви реалізували цей інтерфейс, Laravel автоматично використовуватиме бажану локаль, надсилаючи моделі листи та сповіщення. Тому викликати метод `locale` при використанні цього інтерфейсу не потрібно:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## Тестування

<a name="testing-mailable-content"></a>
### Тестування вмісту листа

Laravel надає низку методів для огляду структури вашого листа. Крім того, Laravel надає кілька зручних методів, щоб перевірити, що ваш лист містить очікуваний вміст:

```php tab=Pest
use App\Mail\InvoicePaid;
use App\Models\User;

test('mailable content', function () {
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
});
```

```php tab=PHPUnit
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content(): void
{
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```

Як ви й очікуєте, перевірки «HTML» стверджують, що HTML-версія вашого листа містить заданий рядок, а перевірки «text» - що заданий рядок містить текстова версія.

<a name="testing-mailable-sending"></a>
### Тестування надсилання листа

Радимо тестувати вміст ваших листів окремо від тестів, які перевіряють, що конкретний лист було «надіслано» конкретному користувачеві. Зазвичай вміст листів не стосується коду, який ви тестуєте, і достатньо просто перевірити, що Laravel отримав вказівку надіслати заданий лист.

Метод `fake` фасаду `Mail` дозволяє завадити надсиланню пошти. Після виклику методу `fake` фасаду `Mail` ви можете перевіряти, що листи мали бути надіслані користувачам, і навіть оглядати дані, які вони отримали:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // Assert that no mailables were sent...
    Mail::assertNothingSent();

    // Assert that a mailable was sent...
    Mail::assertSent(OrderShipped::class);

    // Assert a mailable was sent twice...
    Mail::assertSent(OrderShipped::class, 2);

    // Assert a mailable was sent to an email address...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // Assert a mailable was sent to multiple email addresses...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // Assert a mailable was not sent...
    Mail::assertNotSent(AnotherMailable::class);

    // Assert a mailable was sent twice...
    Mail::assertSentTimes(OrderShipped::class, 2);

    // Assert 3 total mailables were sent...
    Mail::assertSentCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was sent to an email address...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // Assert a mailable was sent to multiple email addresses...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);

        // Assert a mailable was sent twice...
        Mail::assertSentTimes(OrderShipped::class, 2);

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```

Якщо ви ставите листи в чергу на фонову доставку, користуйтеся методом `assertQueued` замість `assertSent`:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

Ви також можете перевірити загальну кількість надісланих або поставлених у чергу листів методом `assertOutgoingCount`:

```php
Mail::assertOutgoingCount(3);
```

Ви можете передати замикання методам `assertSent`, `assertNotSent`, `assertQueued` чи `assertNotQueued`, щоб перевірити, що було надіслано лист, який проходить заданий тест. Якщо надіслано щонайменше один лист, який проходить цей тест, перевірка буде успішною:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

Коли ви викликаєте методи перевірок фасаду `Mail`, екземпляр листа, який приймає передане замикання, надає корисні методи для його огляду:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->hasMetadata('order_id', $mail->order->id);
           $mail->usesMailer('ses');
});
```

Екземпляр листа також містить кілька корисних методів для огляду вкладень:

```php
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

Ви могли помітити, що є два методи для перевірки, що пошту не надіслано: `assertNotSent` та `assertNotQueued`. Інколи вам може захотітися перевірити, що пошту не було ані надіслано, **ані** поставлено в чергу. Для цього скористайтеся методами `assertNothingOutgoing` та `assertNotOutgoing`:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## Пошта й локальна розробка

Розробляючи застосунок, який надсилає пошту, ви, найімовірніше, не хочете справді надсилати листи на живі адреси. Laravel надає кілька способів «вимкнути» реальне надсилання листів під час локальної розробки.

<a name="log-driver"></a>
#### Драйвер log

Замість надсилати листи, поштовий драйвер `log` записуватиме всі повідомлення до ваших файлів логу для огляду. Зазвичай цей драйвер використовують лише під час локальної розробки. Докладніше про налаштування застосунку залежно від середовища читайте в [документації з конфігурації](/docs/{{version}}/configuration#environment-configuration).

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

Як варіант, ви можете скористатися сервісом на кшталт [HELO](https://usehelo.com) чи [Mailtrap](https://mailtrap.io) і драйвером `smtp`, щоб надсилати листи до «фіктивної» поштової скриньки, де ви зможете переглянути їх у справжньому поштовому клієнті. Перевага цього підходу в тому, що ви можете справді оглянути фінальні листи в переглядачі повідомлень Mailtrap.

Якщо ви користуєтеся [Laravel Sail](/docs/{{version}}/sail), переглядати повідомлення можна через [Mailpit](https://github.com/axllent/mailpit). Коли Sail запущено, інтерфейс Mailpit доступний за адресою: `http://localhost:8025`.

<a name="using-a-global-to-address"></a>
#### Глобальна адреса `to`

Нарешті, ви можете вказати глобальну адресу «to», викликавши метод `alwaysTo` фасаду `Mail`. Зазвичай цей метод викликають у методі `boot` одного із сервіс-провайдерів вашого застосунку:

```php
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

Коли ви користуєтеся методом `alwaysTo`, будь-які додаткові адреси «cc» чи «bcc» у листах буде вилучено.

<a name="events"></a>
## Події

Надсилаючи листи, Laravel диспетчеризує дві події. Подія `MessageSending` диспетчеризується перед надсиланням повідомлення, а подія `MessageSent` - після. Пам'ятайте: ці події диспетчеризуються, коли пошту *надсилають*, а не коли її ставлять у чергу. Ви можете створити [слухачів подій](/docs/{{version}}/events) для цих подій у своєму застосунку:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## Власні транспорти

Laravel містить різноманітні поштові транспорти; проте вам може захотітися написати власний, щоб доставляти пошту через сервіси, які Laravel не підтримує «з коробки». Для початку опишіть клас, який розширює `Symfony\Component\Mailer\Transport\AbstractTransport`. Далі реалізуйте у своєму транспорті методи `doSend` та `__toString`:

```php
<?php

namespace App\Mail;

use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Create a new Mailchimp transport instance.
     */
    public function __construct(
        protected ApiClient $client,
    ) {
        parent::__construct();
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function (Address $email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * Get the string representation of the transport.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

Щойно ви описали власний транспорт, зареєструйте його методом `extend` фасаду `Mail`. Зазвичай це роблять у методі `boot` вашого `AppServiceProvider`. До замикання, переданого методу `extend`, буде передано аргумент `$config`. Він міститиме масив конфігурації, описаний для мейлера у файлі `config/mail.php` вашого застосунку:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        $client = new ApiClient;

        $client->setApiKey($config['key']);

        return new MailchimpTransport($client);
    });
}
```

Щойно ваш власний транспорт описано й зареєстровано, ви можете створити у файлі `config/mail.php` опис мейлера, який використовує новий транспорт:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### Додаткові транспорти Symfony

Laravel підтримує деякі наявні поштові транспорти, які підтримує Symfony, - як-от Mailgun і Postmark. Проте вам може захотітися розширити Laravel підтримкою інших транспортів від Symfony. Це робиться підключенням потрібного мейлера Symfony через Composer і реєстрацією транспорту в Laravel. Наприклад, ви можете встановити й зареєструвати мейлер Symfony «Brevo» (раніше «Sendinblue»):

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Щойно пакет мейлера Brevo встановлено, додайте запис із обліковими даними API Brevo до файлу конфігурації `services` вашого застосунку:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

Далі скористайтеся методом `extend` фасаду `Mail`, щоб зареєструвати транспорт у Laravel. Зазвичай це роблять у методі `boot` сервіс-провайдера:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('brevo', function () {
        return (new BrevoTransportFactory)->create(
            new Dsn(
                'brevo+api',
                'default',
                config('services.brevo.key')
            )
        );
    });
}
```

Щойно ваш транспорт зареєстровано, ви можете створити у файлі `config/mail.php` опис мейлера, який використовує новий транспорт:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
