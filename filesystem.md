---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Файлове сховище

- [Вступ](#introduction)
- [Конфігурація](#configuration)
    - [Драйвер local](#the-local-driver)
    - [Публічний диск](#the-public-disk)
    - [Передумови драйверів](#driver-prerequisites)
    - [Скоповані файлові системи й системи лише для читання](#scoped-and-read-only-filesystems)
    - [Файлові системи, сумісні з Amazon S3](#amazon-s3-compatible-filesystems)
- [Отримання екземплярів диска](#obtaining-disk-instances)
    - [Диски на льоту](#on-demand-disks)
- [Отримання файлів](#retrieving-files)
    - [Завантаження файлів](#downloading-files)
    - [URL файлів](#file-urls)
    - [Тимчасові URL](#temporary-urls)
    - [Метадані файлів](#file-metadata)
- [Збереження файлів](#storing-files)
    - [Додавання на початок і в кінець файлів](#prepending-appending-to-files)
    - [Копіювання та переміщення файлів](#copying-moving-files)
    - [Автоматичний потік](#automatic-streaming)
    - [Завантаження файлів на сервер](#file-uploads)
    - [Видимість файлів](#file-visibility)
    - [Обробка зображень](#image-manipulation)
- [Видалення файлів](#deleting-files)
- [Каталоги](#directories)
- [Тестування](#testing)
- [Власні файлові системи](#custom-filesystems)

<a name="introduction"></a>
## Вступ

Laravel надає потужну абстракцію файлової системи завдяки чудовому PHP-пакету [Flysystem](https://github.com/thephpleague/flysystem) від Френка де Йонге. Інтеграція Laravel із Flysystem надає прості драйвери для роботи з локальними файловими системами, SFTP та Amazon S3. Ще краще те, що перемикатися між цими сховищами на локальній машині розробки й на продакшн-сервері напрочуд просто, адже API для кожної системи однаковий.

<a name="configuration"></a>
## Конфігурація

Файл конфігурації файлової системи Laravel лежить у `config/filesystems.php`. У цьому файлі ви можете налаштувати всі свої «диски» файлової системи. Кожен диск представляє певний драйвер сховища й місце зберігання. Приклади конфігурації для кожного підтримуваного драйвера є у файлі конфігурації, тож ви можете змінити її під свої вподобання й облікові дані.

Драйвер `local` працює з файлами, які зберігаються локально на сервері із застосунком Laravel, а драйвер `sftp` використовується для FTP на основі SSH-ключів. Драйвер `s3` використовується для запису в хмарне сховище Amazon S3.

> [!NOTE]
> Ви можете налаштувати скільки завгодно дисків і навіть мати кілька дисків з одним драйвером.

<a name="the-local-driver"></a>
### Драйвер local

Коли ви користуєтеся драйвером `local`, усі операції з файлами відносні до каталогу `root`, заданого у файлі конфігурації `filesystems`. За замовчуванням це значення - каталог `storage/app/private`. Тому метод нижче запише у `storage/app/private/example.txt`:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### Публічний диск

Диск `public`, який є у файлі конфігурації `filesystems` вашого застосунку, призначений для файлів, що мають бути загальнодоступними. За замовчуванням диск `public` використовує драйвер `local` і зберігає файли в `storage/app/public`.

Якщо ваш диск `public` використовує драйвер `local` і ви хочете зробити ці файли доступними з вебу, створіть символічне посилання з вихідного каталогу `storage/app/public` до цільового каталогу `public/storage`:

Щоб створити символічне посилання, скористайтеся командою Artisan `storage:link`:

```shell
php artisan storage:link
```

Щойно файл збережено, а символічне посилання створено, ви можете згенерувати URL до файлів хелпером `asset`:

```php
echo asset('storage/file.txt');
```

Ви можете налаштувати додаткові символічні посилання у файлі конфігурації `filesystems`. Кожне налаштоване посилання буде створено, коли ви виконаєте команду `storage:link`:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

Команда `storage:unlink` дозволяє знищити налаштовані символічні посилання:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### Передумови драйверів

<a name="s3-driver-configuration"></a>
#### Конфігурація драйвера S3

Перш ніж користуватися драйвером S3, вам потрібно встановити пакет Flysystem S3 через менеджер пакетів Composer:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

Масив конфігурації диска S3 лежить у файлі конфігурації `config/filesystems.php`. Зазвичай інформацію й облікові дані S3 налаштовують такими змінними середовища, на які посилається файл `config/filesystems.php`:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

Для зручності ці змінні середовища відповідають домовленостям іменування, які використовує AWS CLI.

<a name="ftp-driver-configuration"></a>
#### Конфігурація драйвера FTP

Перш ніж користуватися драйвером FTP, вам потрібно встановити пакет Flysystem FTP через менеджер пакетів Composer:

```shell
composer require league/flysystem-ftp "^3.0"
```

Інтеграції Laravel із Flysystem чудово працюють з FTP; проте приклад конфігурації не входить до стандартного файлу `config/filesystems.php` фреймворку. Якщо вам потрібно налаштувати файлову систему FTP, скористайтеся прикладом конфігурації нижче:

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // Optional FTP Settings...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### Конфігурація драйвера SFTP

Перш ніж користуватися драйвером SFTP, вам потрібно встановити пакет Flysystem SFTP через менеджер пакетів Composer:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Інтеграції Laravel із Flysystem чудово працюють з SFTP; проте приклад конфігурації не входить до стандартного файлу `config/filesystems.php` фреймворку. Якщо вам потрібно налаштувати файлову систему SFTP, скористайтеся прикладом конфігурації нижче:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key-based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // Settings for file / directory permissions...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // Optional SFTP Settings...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```

<a name="scoped-and-read-only-filesystems"></a>
### Скоповані файлові системи й системи лише для читання

Скоповані диски дозволяють описати файлову систему, у якій усі шляхи автоматично отримують заданий префікс. Перш ніж створювати скопований диск, вам потрібно встановити додатковий пакет Flysystem через менеджер пакетів Composer:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

Ви можете створити скопований за шляхом екземпляр будь-якого наявного диска, описавши диск із драйвером `scoped`. Наприклад, ви можете створити диск, який скопує ваш наявний диск `s3` до певного префікса шляху, - і тоді кожна операція з файлами через скопований диск використовуватиме вказаний префікс:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

Диски «лише для читання» дозволяють створювати диски, які не дозволяють операцій запису. Перш ніж користуватися опцією конфігурації `read-only`, вам потрібно встановити додатковий пакет Flysystem через менеджер пакетів Composer:

```shell
composer require league/flysystem-read-only "^3.0"
```

Далі ви можете додати опцію конфігурації `read-only` до масивів конфігурації одного чи кількох ваших дисків:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Файлові системи, сумісні з Amazon S3

За замовчуванням файл конфігурації `filesystems` вашого застосунку містить конфігурацію диска `s3`. Окрім роботи з [Amazon S3](https://aws.amazon.com/s3/), ви можете скористатися цим диском для будь-якого сумісного з S3 сховища - наприклад, [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/) чи [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/).

Зазвичай, оновивши облікові дані диска відповідно до сервісу, яким плануєте користуватися, вам залишається лише оновити значення опції конфігурації `endpoint`. Значення цієї опції зазвичай задають через змінну середовища `AWS_ENDPOINT`:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a name="obtaining-disk-instances"></a>
## Отримання екземплярів диска

Фасад `Storage` дозволяє працювати з будь-яким із налаштованих дисків. Наприклад, ви можете скористатися методом `put` фасаду, щоб зберегти аватар на диску за замовчуванням. Якщо ви викликаєте методи фасаду `Storage`, не викликавши спершу метод `disk`, метод автоматично буде передано диску за замовчуванням:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

Якщо ваш застосунок працює з кількома дисками, скористайтеся методом `disk` фасаду `Storage`, щоб працювати з файлами на конкретному диску:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### Диски на льоту

Інколи вам може захотітися створити диск під час виконання із заданою конфігурацією, якої немає у файлі конфігурації `filesystems` вашого застосунку. Для цього передайте масив конфігурації методу `build` фасаду `Storage`:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## Отримання файлів

Метод `get` дозволяє отримати вміст файлу. Метод поверне сирий рядковий вміст файлу. Пам'ятайте: усі шляхи до файлів вказуються відносно кореня («root») диска:

```php
$contents = Storage::get('file.jpg');
```

Якщо файл, який ви отримуєте, містить JSON, скористайтеся методом `json`, щоб отримати файл і декодувати його вміст:

```php
$orders = Storage::json('orders.json');
```

Метод `exists` дозволяє визначити, чи існує файл на диску:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

Метод `missing` дозволяє визначити, чи файлу на диску немає:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### Завантаження файлів

Метод `download` дозволяє згенерувати відповідь, яка змусить браузер користувача завантажити файл за заданим шляхом. Другим аргументом метод `download` приймає ім'я файлу, яке побачить користувач, що його завантажує. Нарешті, третім аргументом методу можна передати масив HTTP-заголовків:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### URL файлів

Метод `url` дозволяє отримати URL заданого файлу. Якщо ви користуєтеся драйвером `local`, він зазвичай просто додасть до заданого шляху `/storage` і поверне відносний URL до файлу. Якщо ви користуєтеся драйвером `s3`, буде повернено повний віддалений URL:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

Коли ви користуєтеся драйвером `local`, усі файли, які мають бути загальнодоступними, слід класти в каталог `storage/app/public`. Крім того, вам слід [створити символічне посилання](#the-public-disk) `public/storage`, яке вказує на каталог `storage/app/public`.

> [!WARNING]
> Коли ви користуєтеся драйвером `local`, повернене значення `url` не є URL-кодованим. Тому радимо завжди зберігати файли з іменами, які утворюють коректні URL.

<a name="url-host-customization"></a>
#### Налаштування хоста URL

Якщо ви хочете змінити хост для URL, згенерованих фасадом `Storage`, додайте або змініть опцію `url` у масиві конфігурації диска:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a name="temporary-urls"></a>
### Тимчасові URL

Методом `temporaryUrl` ви можете створювати тимчасові URL до файлів, збережених драйверами `local` та `s3`. Цей метод приймає шлях і екземпляр `DateTime`, який вказує, коли URL має спливти:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### Увімкнення локальних тимчасових URL

Якщо ви почали розробляти застосунок до того, як у драйвері `local` з'явилася підтримка тимчасових URL, вам може знадобитися увімкнути локальні тимчасові URL. Для цього додайте опцію `serve` до масиву конфігурації вашого диска `local` у файлі `config/filesystems.php`:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
#### Параметри запиту S3

Якщо вам потрібно вказати додаткові [параметри запиту S3](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests), передайте масив параметрів запиту третім аргументом методу `temporaryUrl`:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->plus(minutes: 5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a name="customizing-temporary-urls"></a>
#### Налаштування тимчасових URL

Якщо вам потрібно змінити те, як створюються тимчасові URL для конкретного диска, скористайтеся методом `buildTemporaryUrlsUsing`. Наприклад, це може стати в пригоді, якщо у вас є контролер, який дозволяє завантажувати файли з диска, що зазвичай не підтримує тимчасових URL. Зазвичай цей метод викликають у методі `boot` сервіс-провайдера:

```php
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(
            function (string $path, DateTime $expiration, array $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            }
        );
    }
}
```

<a name="temporary-upload-urls"></a>
#### Тимчасові URL для завантаження на сервер

> [!WARNING]
> Можливість генерувати тимчасові URL для завантаження на сервер підтримують лише драйвери `s3` та `local`.

Якщо вам потрібно згенерувати тимчасовий URL, яким можна завантажити файл напряму з вашого клієнтського застосунку, скористайтеся методом `temporaryUploadUrl`. Цей метод приймає шлях і екземпляр `DateTime`, який вказує, коли URL має спливти. Метод `temporaryUploadUrl` повертає асоціативний масив, який можна деструктурувати на URL завантаження та заголовки, які слід додати до запиту:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

Цей метод насамперед корисний у безсерверних середовищах, де клієнтський застосунок має завантажувати файли напряму до хмарного сховища на кшталт Amazon S3.

<a name="file-metadata"></a>
### Метадані файлів

Окрім читання та запису файлів, Laravel може надати інформацію й про самі файли. Наприклад, метод `size` дозволяє отримати розмір файлу в байтах:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

Метод `lastModified` повертає UNIX-мітку часу останньої зміни файлу:

```php
$time = Storage::lastModified('file.jpg');
```

MIME-тип заданого файлу можна отримати методом `mimeType`:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### Шляхи до файлів

Метод `path` дозволяє отримати шлях до заданого файлу. Якщо ви користуєтеся драйвером `local`, він поверне абсолютний шлях до файлу. Якщо ви користуєтеся драйвером `s3`, цей метод поверне відносний шлях до файлу в бакеті S3:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## Збереження файлів

Метод `put` дозволяє зберегти вміст файлу на диску. Ви також можете передати методу `put` PHP-ресурс `resource`, і тоді буде використано підтримку потоків із Flysystem. Пам'ятайте: усі шляхи до файлів вказуються відносно кореня («root»), налаштованого для диска:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### Невдалі записи

Якщо метод `put` (чи інші операції запису) не зможе записати файл на диск, буде повернуто `false`:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

За бажанням ви можете описати опцію `throw` у масиві конфігурації вашого диска. Коли ця опція має значення `true`, методи запису на кшталт `put` викидатимуть екземпляр `League\Flysystem\UnableToWriteFile`, якщо операція запису провалиться:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### Додавання на початок і в кінець файлів

Методи `prepend` і `append` дозволяють писати на початок або в кінець файлу:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### Копіювання та переміщення файлів

Метод `copy` дозволяє скопіювати наявний файл у нове місце на диску, а метод `move` - перейменувати чи перемістити наявний файл у нове місце:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### Автоматичний потік

Передавання файлів у сховище потоком значно знижує споживання пам'яті. Якщо ви хочете, щоб Laravel автоматично керував передаванням заданого файлу до вашого сховища, скористайтеся методом `putFile` чи `putFileAs`. Цей метод приймає екземпляр `Illuminate\Http\File` або `Illuminate\Http\UploadedFile` і автоматично передасть файл потоком у потрібне місце:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

Щодо методу `putFile` варто зауважити кілька важливих речей. Зверніть увагу, що ми вказали лише назву каталогу, а не ім'я файлу. За замовчуванням метод `putFile` згенерує унікальний ID, який стане іменем файлу. Розширення файлу буде визначено за його MIME-типом. Метод `putFile` поверне шлях до файлу, тож ви можете зберегти цей шлях разом зі згенерованим іменем у своїй базі даних.

Методи `putFile` і `putFileAs` також приймають аргумент, який задає «видимість» збереженого файлу. Це особливо корисно, якщо ви зберігаєте файл на хмарному диску на кшталт Amazon S3 і хочете, щоб файл був загальнодоступним за згенерованими URL:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### Завантаження файлів на сервер

У вебзастосунках один із найпоширеніших сценаріїв збереження файлів - зберігати файли, завантажені користувачами: фото й документи. Laravel дуже спрощує збереження завантажених файлів методом `store` на екземплярі завантаженого файлу. Викличте метод `store` зі шляхом, за яким ви хочете зберегти завантажений файл:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * Update the avatar for the user.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

Щодо цього прикладу варто зауважити кілька важливих речей. Зверніть увагу, що ми вказали лише назву каталогу, а не ім'я файлу. За замовчуванням метод `store` згенерує унікальний ID, який стане іменем файлу. Розширення файлу буде визначено за його MIME-типом. Метод `store` поверне шлях до файлу, тож ви можете зберегти цей шлях разом зі згенерованим іменем у своїй базі даних.

Ви також можете викликати метод `putFile` фасаду `Storage`, щоб виконати ту саму операцію збереження файлу, що й у прикладі вище:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### Задання імені файлу

Якщо ви не хочете, щоб збереженому файлу автоматично призначалося ім'я, скористайтеся методом `storeAs`, який приймає аргументами шлях, ім'я файлу і (необов'язково) диск:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

Ви також можете скористатися методом `putFileAs` фасаду `Storage`, який виконає ту саму операцію збереження файлу, що й у прикладі вище:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> Недруковані та некоректні символи Unicode буде автоматично вилучено зі шляхів до файлів. Тому вам, можливо, варто санітизувати шляхи, перш ніж передавати їх методам збереження файлів у Laravel. Шляхи нормалізуються методом `League\Flysystem\WhitespacePathNormalizer::normalizePath`.

<a name="specifying-a-disk"></a>
#### Задання диска

За замовчуванням метод `store` завантаженого файлу використовує ваш диск за замовчуванням. Якщо ви хочете вказати інший диск, передайте його назву другим аргументом методу `store`:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

Якщо ви користуєтеся методом `storeAs`, назву диска можна передати третім аргументом методу:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### Інша інформація про завантажений файл

Якщо ви хочете отримати оригінальні ім'я та розширення завантаженого файлу, скористайтеся методами `getClientOriginalName` і `getClientOriginalExtension`:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

Проте пам'ятайте, що методи `getClientOriginalName` і `getClientOriginalExtension` вважаються небезпечними, адже зловмисник може підробити ім'я й розширення файлу. Тому зазвичай варто віддавати перевагу методам `hashName` та `extension`, щоб отримати ім'я й розширення для завантаженого файлу:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

<a name="file-visibility"></a>
### Видимість файлів

В інтеграції Laravel із Flysystem «видимість» - це абстракція прав доступу до файлів на різних платформах. Файли можуть бути оголошені як `public` або `private`. Коли файл оголошено `public`, ви вказуєте, що він загалом має бути доступним іншим. Наприклад, з драйвером S3 ви можете отримувати URL для файлів `public`.

Задати видимість можна під час запису файлу методом `put`:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

Якщо файл уже збережено, його видимість можна отримати й задати методами `getVisibility` та `setVisibility`:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

Працюючи із завантаженими файлами, ви можете скористатися методами `storePublicly` та `storePubliclyAs`, щоб зберегти завантажений файл з видимістю `public`:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="image-manipulation"></a>
### Обробка зображень

Якщо вам потрібно змінити розмір, обрізати чи конвертувати завантажене зображення перед збереженням, скористайтеся [можливостями обробки зображень](/docs/{{version}}/images) Laravel:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->toWebp()
    ->storePublicly('avatars', 'public');
```

Ви також можете створити екземпляр зображення з файлу, який уже зберігається на одному з ваших дисків:

```php
$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="local-files-and-visibility"></a>
#### Локальні файли та видимість

Коли ви користуєтеся драйвером `local`, [видимість](#file-visibility) `public` перетворюється на права `0755` для каталогів і `0644` для файлів. Ви можете змінити відповідність прав у файлі конфігурації `filesystems` вашого застосунку:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app'),
    'permissions' => [
        'file' => [
            'public' => 0644,
            'private' => 0600,
        ],
        'dir' => [
            'public' => 0755,
            'private' => 0700,
        ],
    ],
    'throw' => false,
],
```

<a name="deleting-files"></a>
## Видалення файлів

Метод `delete` приймає одне ім'я файлу або масив файлів для видалення:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

За потреби ви можете вказати диск, з якого слід видалити файл:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## Каталоги

<a name="get-all-files-within-a-directory"></a>
#### Отримати всі файли в каталозі

Метод `files` повертає масив усіх файлів у заданому каталозі. Якщо ви хочете отримати список усіх файлів у заданому каталозі разом із підкаталогами, скористайтеся методом `allFiles`:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### Отримати всі каталоги в каталозі

Метод `directories` повертає масив усіх каталогів у заданому каталозі. Якщо ви хочете отримати список усіх каталогів у заданому каталозі разом із підкаталогами, скористайтеся методом `allDirectories`:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### Створити каталог

Метод `makeDirectory` створить заданий каталог разом з усіма потрібними підкаталогами:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### Видалити каталог

Нарешті, метод `deleteDirectory` дозволяє видалити каталог і всі його файли:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## Тестування

Метод `fake` фасаду `Storage` дозволяє легко згенерувати фейковий диск, який у поєднанні з утилітами генерації файлів класу `Illuminate\Http\UploadedFile` значно спрощує тестування завантаження файлів. Наприклад:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // Assert one or more files were stored...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // Assert one or more files were not stored...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // Assert that the number of files in a given directory matches the expected count...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // Assert that a given directory is empty...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

    // Assert that the disk contains no files...
    Storage::disk('photos')->assertEmpty();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded(): void
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // Assert one or more files were stored...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // Assert one or more files were not stored...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // Assert that the number of files in a given directory matches the expected count...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // Assert that a given directory is empty...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

        // Assert that the disk contains no files...
        Storage::disk('photos')->assertEmpty();
    }
}
```

За замовчуванням метод `fake` видаляє всі файли у своєму тимчасовому каталозі. Якщо ви хочете зберегти ці файли, скористайтеся натомість методом «persistentFake». Докладніше про тестування завантаження файлів читайте в [документації з HTTP-тестування, розділ про завантаження файлів](/docs/{{version}}/http-tests#testing-file-uploads).

> [!WARNING]
> Метод `image` потребує [розширення GD](https://www.php.net/manual/en/book.image.php).

<a name="custom-filesystems"></a>
## Власні файлові системи

Інтеграція Laravel із Flysystem «з коробки» підтримує кілька «драйверів»; проте Flysystem ними не обмежується й має адаптери для багатьох інших сховищ. Ви можете створити власний драйвер, якщо хочете скористатися одним із цих додаткових адаптерів у своєму застосунку Laravel.

Щоб описати власну файлову систему, вам знадобиться адаптер Flysystem. Додаймо до нашого проєкту адаптер Dropbox, який підтримує спільнота:

```shell
composer require spatie/flysystem-dropbox
```

Далі ви можете зареєструвати драйвер у методі `boot` одного з [сервіс-провайдерів](/docs/{{version}}/providers) вашого застосунку. Для цього скористайтеся методом `extend` фасаду `Storage`:

```php
<?php

namespace App\Providers;

use Illuminate\Contracts\Foundation\Application;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::extend('dropbox', function (Application $app, array $config) {
            $adapter = new DropboxAdapter(new DropboxClient(
                $config['authorization_token']
            ));

            return new FilesystemAdapter(
                new Filesystem($adapter, $config),
                $adapter,
                $config
            );
        });
    }
}
```

Перший аргумент методу `extend` - назва драйвера, другий - замикання, яке отримує змінні `$app` і `$config`. Замикання має повернути екземпляр `Illuminate\Filesystem\FilesystemAdapter`. Змінна `$config` містить значення, задані в `config/filesystems.php` для вказаного диска.

Щойно ви створили й зареєстрували сервіс-провайдер розширення, ви можете користуватися драйвером `dropbox` у файлі конфігурації `config/filesystems.php`.
