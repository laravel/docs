---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Valet

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Оновлення Valet](#upgrading-valet)
- [Віддача сайтів](#serving-sites)
    - [Команда «park»](#the-park-command)
    - [Команда «link»](#the-link-command)
    - [Захист сайтів через TLS](#securing-sites)
    - [Віддача сайту за замовчуванням](#serving-a-default-site)
    - [Версії PHP для окремих сайтів](#per-site-php-versions)
- [Публічний доступ до сайтів](#sharing-sites)
    - [Доступ до сайтів у локальній мережі](#sharing-sites-on-your-local-network)
- [Змінні оточення для окремих сайтів](#site-specific-environment-variables)
- [Проксіювання сервісів](#proxying-services)
- [Власні драйвери Valet](#custom-valet-drivers)
    - [Локальні драйвери](#local-drivers)
- [Інші команди Valet](#other-valet-commands)
- [Каталоги й файли Valet](#valet-directories-and-files)
    - [Доступ до диска](#disk-access)

<a name="introduction"></a>
## Вступ

> [!NOTE]
> Шукаєте ще простіший спосіб розробляти застосунки Laravel на macOS чи Windows? Погляньте на [Laravel Herd](https://herd.laravel.com). Herd містить усе потрібне, щоб почати розробку на Laravel, - зокрема Valet, PHP і Composer.

[Laravel Valet](https://github.com/laravel/valet) - середовище розробки для мінімалістів на macOS. Laravel Valet налаштовує ваш Mac так, щоб [Nginx](https://www.nginx.com/) завжди працював у фоні від старту системи. Далі, через [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet проксіює всі запити на домен `*.test` до сайтів, встановлених на вашій машині.

Іншими словами, Valet - це блискавично швидке середовище розробки Laravel, яке з'їдає приблизно 7 МБ RAM. Valet не є повною заміною [Sail](/docs/{{version}}/sail) чи [Homestead](/docs/{{version}}/homestead), але стане чудовою альтернативою, якщо вам потрібна гнучка основа, ви цінуєте граничну швидкість або працюєте на машині з обмеженою кількістю RAM.

Одразу з коробки Valet підтримує - зокрема, але не лише:

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Статичний HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

Проте ви можете розширити Valet власними [драйверами](#custom-valet-drivers).

<a name="installation"></a>
## Встановлення

> [!WARNING]
> Valet вимагає macOS і [Homebrew](https://brew.sh/). Перед встановленням переконайтеся, що жодна інша програма - як-от Apache чи Nginx - не займає порт 80 на вашій машині.

Для початку переконайтеся, що Homebrew оновлено, командою `update`:

```shell
brew update
```

Далі встановіть PHP через Homebrew:

```shell
brew install php
```

Після встановлення PHP ви готові встановити [менеджер пакетів Composer](https://getcomposer.org). Крім того, переконайтеся, що каталог `$HOME/.composer/vendor/bin` є у «PATH» вашої системи. Коли Composer встановлено, ви можете встановити Laravel Valet як глобальний пакет Composer:

```shell
composer global require laravel/valet
```

Нарешті, виконайте команду Valet `install`. Вона налаштує й встановить Valet і DnsMasq. Крім того, демони, від яких залежить Valet, буде налаштовано на запуск разом із системою:

```shell
valet install
```

Коли Valet встановлено, спробуйте пропінгувати будь-який домен `*.test` у терміналі - наприклад, командою `ping foobar.test`. Якщо Valet встановлено правильно, ви побачите, що цей домен відповідає на `127.0.0.1`.

Valet автоматично запускатиме потрібні йому сервіси при кожному старті машини.

<a name="php-versions"></a>
#### Версії PHP

> [!NOTE]
> Замість того щоб змінювати глобальну версію PHP, ви можете вказати Valet використовувати різні версії PHP для окремих сайтів через [команду](#per-site-php-versions) `isolate`.

Valet дозволяє перемикати версії PHP командою `valet use php@version`. Valet встановить указану версію PHP через Homebrew, якщо її ще не встановлено:

```shell
valet use php@8.2

valet use php
```

Ви також можете створити файл `.valetrc` у корені свого проєкту. Файл `.valetrc` має містити версію PHP, яку слід використовувати для сайту:

```shell
php=php@8.2
```

Коли цей файл створено, ви можете просто виконати команду `valet use` - і вона визначить бажану версію PHP для сайту, прочитавши цей файл.

> [!WARNING]
> Valet віддає сайти лише однією версією PHP за раз, навіть якщо у вас встановлено кілька версій PHP.

<a name="database"></a>
#### База даних

Якщо вашому застосунку потрібна база даних, погляньте на [DBngin](https://dbngin.com) - безкоштовний універсальний інструмент керування базами, що містить MySQL, PostgreSQL і Redis. Коли DBngin встановлено, ви можете підключитися до бази на `127.0.0.1` з іменем користувача `root` і порожнім рядком як паролем.

<a name="resetting-your-installation"></a>
#### Скидання вашої установки

Якщо у вас проблеми з правильною роботою Valet, виконання команди `composer global require laravel/valet` з наступним `valet install` скине вашу установку й може розв'язати різні проблеми. У рідкісних випадках може знадобитися «жорстке скидання» Valet: виконайте `valet uninstall --force`, а потім `valet install`.

<a name="upgrading-valet"></a>
### Оновлення Valet

Ви можете оновити свою установку Valet, виконавши в терміналі команду `composer global require laravel/valet`. Після оновлення варто запустити команду `valet install`, щоб Valet за потреби вніс додаткові оновлення до ваших конфігураційних файлів.

<a name="upgrading-to-valet-4"></a>
#### Оновлення до Valet 4

Якщо ви оновлюєтеся з Valet 3 до Valet 4, виконайте такі кроки, щоб оновити установку правильно:

<div class="content-list" markdown="1">

- Якщо ви додавали файли `.valetphprc`, щоб задати версію PHP для сайту, перейменуйте кожен файл `.valetphprc` на `.valetrc`. Далі додайте `php=` перед наявним вмістом файлу `.valetrc`.
- Оновіть усі власні драйвери, щоб вони відповідали простору імен, розширенню, підказкам типів і типам, що повертаються, у новій системі драйверів. Як приклад можна взяти [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) від Valet.
- Якщо ви віддаєте сайти на PHP 7.1 - 7.4, обов'язково встановіть через Homebrew також версію PHP 8.0 чи вище: Valet використовуватиме її для деяких своїх скриптів, навіть якщо вона не є вашою основною прив'язаною версією.

</div>

<a name="serving-sites"></a>
## Віддача сайтів

Коли Valet встановлено, ви готові віддавати свої застосунки Laravel. Valet надає для цього дві команди: `park` і `link`.

<a name="the-park-command"></a>
### Команда `park`

Команда `park` реєструє на вашій машині каталог, що містить ваші застосунки. Коли каталог «припарковано» у Valet, усі каталоги всередині нього стануть доступні у браузері за адресою `http://<directory-name>.test`:

```shell
cd ~/Sites

valet park
```

Ось і все. Тепер будь-який застосунок, створений у вашому «припаркованому» каталозі, автоматично віддаватиметься за угодою `http://<directory-name>.test`. Тож якщо ваш припаркований каталог містить каталог «laravel», застосунок усередині нього буде доступний за адресою `http://laravel.test`. Крім того, Valet автоматично дозволяє звертатися до сайту через піддомени-джокери (`http://foo.laravel.test`).

<a name="the-link-command"></a>
### Команда `link`

Команда `link` також дозволяє віддавати ваші застосунки Laravel. Вона стає в пригоді, коли ви хочете віддати один сайт у каталозі, а не весь каталог:

```shell
cd ~/Sites/laravel

valet link
```

Коли застосунок прив'язано до Valet командою `link`, ви можете звертатися до нього за іменем його каталогу. Тож сайт, прив'язаний у прикладі вище, буде доступний за адресою `http://laravel.test`. Крім того, Valet автоматично дозволяє звертатися до сайту через піддомени-джокери (`http://foo.laravel.test`).

Якщо ви хочете віддавати застосунок за іншим іменем хоста, передайте це ім'я команді `link`. Наприклад, ви можете виконати таку команду, щоб застосунок став доступний за адресою `http://application.test`:

```shell
cd ~/Sites/laravel

valet link application
```

Звісно, командою `link` можна віддавати застосунки й на піддоменах:

```shell
valet link api.application
```

Ви можете виконати команду `links`, щоб побачити список усіх ваших прив'язаних каталогів:

```shell
valet links
```

Команда `unlink` дозволяє знищити символічне посилання для сайту:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### Захист сайтів через TLS

За замовчуванням Valet віддає сайти через HTTP. Проте якщо ви хочете віддавати сайт через шифрований TLS із HTTP/2, скористайтеся командою `secure`. Наприклад, якщо Valet віддає ваш сайт на домені `laravel.test`, виконайте таку команду, щоб захистити його:

```shell
valet secure laravel
```

Щоб «зняти захист» із сайту й повернутися до звичайного HTTP, скористайтеся командою `unsecure`. Як і команда `secure`, вона приймає ім'я хоста, з якого ви хочете зняти захист:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### Віддача сайту за замовчуванням

Іноді вам може знадобитися налаштувати Valet віддавати сайт «за замовчуванням» замість `404` при зверненні до невідомого домену `test`. Для цього додайте до конфігураційного файлу `~/.config/valet/config.json` опцію `default` зі шляхом до сайту, який має слугувати сайтом за замовчуванням:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### Версії PHP для окремих сайтів

За замовчуванням Valet віддає ваші сайти через глобально встановлений PHP. Проте якщо вам треба підтримувати кілька версій PHP для різних сайтів, скористайтеся командою `isolate`, щоб указати, яку версію PHP має використовувати конкретний сайт. Команда `isolate` налаштовує Valet використовувати вказану версію PHP для сайту, що лежить у вашому поточному робочому каталозі:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

Якщо ім'я сайту не збігається з іменем каталогу, що його містить, вкажіть ім'я сайту опцією `--site`:

```shell
valet isolate php@8.0 --site="site-name"
```

Для зручності ви можете скористатися командами `valet php`, `composer` та `which-php`, щоб проксіювати виклики до відповідного PHP CLI чи інструмента, зважаючи на налаштовану для сайту версію PHP:

```shell
valet php
valet composer
valet which-php
```

Ви можете виконати команду `isolated`, щоб побачити список усіх ваших ізольованих сайтів і їхніх версій PHP:

```shell
valet isolated
```

Щоб повернути сайт до глобально встановленої у Valet версії PHP, викличте команду `unisolate` з кореневого каталогу сайту:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## Публічний доступ до сайтів

Valet містить команду, щоб відкрити ваші локальні сайти світові, - це простий спосіб протестувати сайт на мобільних пристроях або показати його колегам і клієнтам.

Одразу з коробки Valet підтримує відкриття сайтів через ngrok чи Expose. Перш ніж відкривати сайт, оновіть конфігурацію Valet командою `share-tool`, указавши `ngrok`, `expose` чи `cloudflared`:

```shell
valet share-tool ngrok
```

Якщо ви оберете інструмент, який не встановлено через Homebrew (для ngrok і cloudflared) чи Composer (для Expose), Valet автоматично запропонує його встановити. Звісно, обидва інструменти вимагають автентифікації у вашому обліковому записі ngrok чи Expose, перш ніж ви зможете відкривати сайти.

Щоб відкрити сайт, перейдіть у терміналі до його каталогу й виконайте команду Valet `share`. Публічно доступний URL потрапить до вашого буфера обміну - його можна одразу вставити у браузер чи надіслати команді:

```shell
cd ~/Sites/laravel

valet share
```

Щоб припинити відкритий доступ до сайту, натисніть `Control + C`.

> [!WARNING]
> Якщо ви користуєтеся власним DNS-сервером (як-от `1.1.1.1`), відкриття через ngrok може працювати некоректно. Якщо це ваш випадок, відкрийте системні налаштування Mac, перейдіть до налаштувань мережі, відкрийте додаткові налаштування, перейдіть на вкладку DNS і додайте `127.0.0.1` як перший DNS-сервер.

<a name="sharing-sites-via-ngrok"></a>
#### Відкриття сайтів через Ngrok

Щоб відкрити сайт через ngrok, вам треба [створити обліковий запис ngrok](https://dashboard.ngrok.com/signup) і [налаштувати токен автентифікації](https://dashboard.ngrok.com/get-started/your-authtoken). Коли токен у вас є, оновіть конфігурацію Valet цим токеном:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> Ви можете передати команді share додаткові параметри ngrok - наприклад, `valet share --region=eu`. Докладніше читайте в [документації ngrok](https://ngrok.com/docs).

<a name="sharing-sites-via-expose"></a>
#### Відкриття сайтів через Expose

Щоб відкрити сайт через Expose, вам треба [створити обліковий запис Expose](https://expose.dev/register) та [автентифікуватися в Expose через свій токен](https://expose.dev/docs/getting-started/getting-your-token).

Інформацію про додаткові параметри командного рядка, які він підтримує, шукайте в [документації Expose](https://expose.dev/docs).

<a name="sharing-sites-on-your-local-network"></a>
### Доступ до сайтів у локальній мережі

За замовчуванням Valet обмежує вхідний трафік внутрішнім інтерфейсом `127.0.0.1`, щоб ваша машина для розробки не наражалася на загрози з інтернету.

Якщо ви хочете дозволити іншим пристроям у локальній мережі звертатися до сайтів Valet на вашій машині за її IP-адресою (наприклад, `192.168.1.10/application.test`), вам треба вручну відредагувати відповідний конфігураційний файл Nginx для цього сайту й прибрати обмеження в директиві `listen`. Приберіть префікс `127.0.0.1:` у директиві `listen` для портів 80 і 443.

Якщо ви не виконували `valet secure` для проєкту, ви можете відкрити мережевий доступ до всіх не-HTTPS сайтів, відредагувавши файл `/usr/local/etc/nginx/valet/valet.conf`. Проте якщо ви віддаєте сайт проєкту через HTTPS (тобто виконали для нього `valet secure`), редагуйте файл `~/.config/valet/Nginx/app-name.test`.

Оновивши конфігурацію Nginx, виконайте команду `valet restart`, щоб зміни набрали чинності.

<a name="site-specific-environment-variables"></a>
## Змінні оточення для окремих сайтів

Деякі застосунки на інших фреймворках можуть залежати від серверних змінних оточення, але не давати способу налаштувати ці змінні всередині проєкту. Valet дозволяє задати змінні оточення для окремих сайтів, додавши файл `.valet-env.php` у корінь вашого проєкту. Цей файл має повертати масив пар «сайт / змінна оточення», які буде додано до глобального масиву `$_SERVER` для кожного вказаного в ньому сайту:

```php
<?php

return [
    // Set $_SERVER['key'] to "value" for the laravel.test site...
    'laravel' => [
        'key' => 'value',
    ],

    // Set $_SERVER['key'] to "value" for all sites...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## Проксіювання сервісів

Іноді вам може знадобитися проксіювати домен Valet до іншого сервісу на вашій машині. Наприклад, вам час від часу треба запускати Valet, водночас маючи окремий сайт у Docker; проте Valet і Docker не можуть одночасно займати порт 80.

Щоб це розв'язати, скористайтеся командою `proxy`, щоб створити проксі. Наприклад, ви можете проксіювати весь трафік із `http://elasticsearch.test` до `http://127.0.0.1:9200`:

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

Прибрати проксі можна командою `unproxy`:

```shell
valet unproxy elasticsearch
```

Команда `proxies` дозволяє побачити список усіх проксійованих конфігурацій сайтів:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## Власні драйвери Valet

Ви можете написати власний «драйвер» Valet, щоб віддавати застосунки PHP на фреймворку чи CMS, які Valet не підтримує нативно. Під час встановлення Valet створюється каталог `~/.config/valet/Drivers`, що містить файл `SampleValetDriver.php`. Цей файл містить приклад реалізації драйвера, який демонструє, як написати власний. Написання драйвера вимагає реалізувати лише три методи: `serves`, `isStaticFile` та `frontControllerPath`.

Усі три методи отримують аргументами значення `$sitePath`, `$siteName` та `$uri`. `$sitePath` - повний шлях до сайту, який віддається на вашій машині, - наприклад, `/Users/Lisa/Sites/my-project`. `$siteName` - частина домену з «хостом» / «іменем сайту» (`my-project`). `$uri` - URI вхідного запиту (`/foo/bar`).

Коли ви завершите свій драйвер Valet, покладіть його до каталогу `~/.config/valet/Drivers`, дотримуючись угоди іменування `FrameworkValetDriver.php`. Наприклад, якщо ви пишете власний драйвер valet для WordPress, ім'я файлу має бути `WordPressValetDriver.php`.

Погляньмо на приклад реалізації кожного методу, який має містити ваш драйвер Valet.

<a name="the-serves-method"></a>
#### Метод `serves`

Метод `serves` має повертати `true`, якщо ваш драйвер повинен обробити вхідний запит. Інакше метод має повертати `false`. Тож усередині цього методу вам слід спробувати визначити, чи містить заданий `$sitePath` проєкт того типу, який ви намагаєтеся віддавати.

Уявімо, наприклад, що ми пишемо `WordPressValetDriver`. Наш метод `serves` міг би мати такий вигляд:

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### Метод `isStaticFile`

Метод `isStaticFile` має визначити, чи стосується вхідний запит «статичного» файлу - як-от зображення чи стилю. Якщо файл статичний, метод має повернути повний шлях до нього на диску. Якщо вхідний запит не стосується статичного файлу, метод має повернути `false`:

```php
/**
 * Determine if the incoming request is for a static file.
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!WARNING]
> Метод `isStaticFile` буде викликано лише тоді, коли метод `serves` повертає `true` для вхідного запиту, а URI запиту не дорівнює `/`.

<a name="the-frontcontrollerpath-method"></a>
#### Метод `frontControllerPath`

Метод `frontControllerPath` має повертати повний шлях до «фронт-контролера» вашого застосунку - зазвичай це файл «index.php» чи його аналог:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### Локальні драйвери

Якщо ви хочете описати власний драйвер Valet для одного застосунку, створіть файл `LocalValetDriver.php` у кореневому каталозі застосунку. Ваш драйвер може успадковувати базовий клас `ValetDriver` або наявний драйвер для конкретного застосунку - як-от `LaravelValetDriver`:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
## Інші команди Valet

<div class="overflow-auto">

| Команда | Опис |
| --- | --- |
| `valet list` | Показує список усіх команд Valet. |
| `valet diagnose` | Виводить діагностику, що допомагає налагоджувати Valet. |
| `valet directory-listing` | Визначає поведінку показу вмісту каталогів. За замовчуванням «off», що віддає для каталогів сторінку 404. |
| `valet forget` | Виконайте цю команду з «припаркованого» каталогу, щоб прибрати його зі списку припаркованих. |
| `valet log` | Показує список логів, які пишуть сервіси Valet. |
| `valet paths` | Показує всі ваші «припарковані» шляхи. |
| `valet restart` | Перезапускає демони Valet. |
| `valet start` | Запускає демони Valet. |
| `valet stop` | Зупиняє демони Valet. |
| `valet trust` | Додає файли sudoers для Brew і Valet, щоб команди Valet виконувалися без запиту пароля. |
| `valet uninstall` | Видаляє Valet: показує інструкції для ручного видалення. Додайте опцію `--force`, щоб агресивно видалити всі ресурси Valet. |

</div>

<a name="valet-directories-and-files"></a>
## Каталоги й файли Valet

Наведена нижче інформація про каталоги й файли може стати в пригоді, коли ви розбираєтеся з проблемами у вашому середовищі Valet:

#### `~/.config/valet`

Містить усю конфігурацію Valet. Вам, можливо, варто зробити резервну копію цього каталогу.

#### `~/.config/valet/dnsmasq.d/`

Цей каталог містить конфігурацію DNSMasq.

#### `~/.config/valet/Drivers/`

Цей каталог містить драйвери Valet. Драйвери визначають, як віддається конкретний фреймворк чи CMS.

#### `~/.config/valet/Nginx/`

Цей каталог містить усі конфігурації сайтів Nginx у Valet. Ці файли перезбираються під час виконання команд `install` і `secure`.

#### `~/.config/valet/Sites/`

Цей каталог містить усі символічні посилання на ваші [прив'язані проєкти](#the-link-command).

#### `~/.config/valet/config.json`

Цей файл - головний конфігураційний файл Valet.

#### `~/.config/valet/valet.sock`

Цей файл - сокет PHP-FPM, який використовує встановлений Valet Nginx. Він існуватиме, лише якщо PHP працює належно.

#### `~/.config/valet/Log/fpm-php.www.log`

Цей файл - користувацький лог помилок PHP.

#### `~/.config/valet/Log/nginx-error.log`

Цей файл - користувацький лог помилок Nginx.

#### `/usr/local/var/log/php-fpm.log`

Цей файл - системний лог помилок PHP-FPM.

#### `/usr/local/var/log/nginx`

Цей каталог містить логи доступу та помилок Nginx.

#### `/usr/local/etc/php/X.X/conf.d`

Цей каталог містить файли `*.ini` з різними налаштуваннями конфігурації PHP.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

Цей файл - конфігураційний файл пулу PHP-FPM.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

Цей файл - стандартна конфігурація Nginx, яка використовується для створення SSL-сертифікатів для ваших сайтів.

<a name="disk-access"></a>
### Доступ до диска

Починаючи з macOS 10.14, [доступ до деяких файлів і каталогів обмежено за замовчуванням](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). Ці обмеження стосуються каталогів Desktop, Documents і Downloads. Крім того, обмежено доступ до мережевих і знімних томів. Тому Valet рекомендує тримати каталоги ваших сайтів поза цими захищеними розташуваннями.

Проте якщо ви хочете віддавати сайти з одного з таких розташувань, вам треба надати Nginx «Full Disk Access». Інакше ви можете натрапити на помилки сервера чи іншу непередбачувану поведінку Nginx - особливо при віддачі статичних ресурсів. Зазвичай macOS автоматично запропонує надати Nginx повний доступ до цих розташувань. Або ж ви можете зробити це вручну через `System Preferences` > `Security & Privacy` > `Privacy`, обравши `Full Disk Access`. Далі увімкніть усі записи `nginx` у головній панелі вікна.
