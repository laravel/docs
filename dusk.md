---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Dusk

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Керування встановленням ChromeDriver](#managing-chromedriver-installations)
    - [Використання інших браузерів](#using-other-browsers)
- [Перші кроки](#getting-started)
    - [Генерування тестів](#generating-tests)
    - [Скидання бази даних після кожного тесту](#resetting-the-database-after-each-test)
    - [Запуск тестів](#running-tests)
    - [Робота із середовищем](#environment-handling)
- [Основи роботи з браузером](#browser-basics)
    - [Створення браузерів](#creating-browsers)
    - [Навігація](#navigation)
    - [Зміна розміру вікна браузера](#resizing-browser-windows)
    - [Макроси браузера](#browser-macros)
    - [Автентифікація](#authentication)
    - [Cookie](#cookies)
    - [Виконання JavaScript](#executing-javascript)
    - [Знімок екрана](#taking-a-screenshot)
    - [Збереження виводу консолі на диск](#storing-console-output-to-disk)
    - [Збереження коду сторінки на диск](#storing-page-source-to-disk)
- [Взаємодія з елементами](#interacting-with-elements)
    - [Селектори Dusk](#dusk-selectors)
    - [Текст, значення та атрибути](#text-values-and-attributes)
    - [Робота з формами](#interacting-with-forms)
    - [Прикріплення файлів](#attaching-files)
    - [Натискання кнопок](#pressing-buttons)
    - [Клацання по посиланнях](#clicking-links)
    - [Використання клавіатури](#using-the-keyboard)
    - [Використання миші](#using-the-mouse)
    - [Діалоги JavaScript](#javascript-dialogs)
    - [Робота з вбудованими фреймами](#interacting-with-iframes)
    - [Обмеження селекторів](#scoping-selectors)
    - [Очікування елементів](#waiting-for-elements)
    - [Прокручування до елемента](#scrolling-an-element-into-view)
- [Доступні твердження](#available-assertions)
- [Сторінки](#pages)
    - [Генерування сторінок](#generating-pages)
    - [Налаштування сторінок](#configuring-pages)
    - [Перехід до сторінок](#navigating-to-pages)
    - [Скорочені селектори](#shorthand-selectors)
    - [Методи сторінок](#page-methods)
- [Компоненти](#components)
    - [Генерування компонентів](#generating-components)
    - [Використання компонентів](#using-components)
- [Неперервна інтеграція](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## Вступ

> [!WARNING]
> [Pest 4](https://pestphp.com/) тепер містить автоматизоване тестування у браузері, яке суттєво виграє в продуктивності та зручності порівняно з Laravel Dusk. Для нових проєктів ми рекомендуємо тестувати у браузері саме через Pest.

[Laravel Dusk](https://github.com/laravel/dusk) надає виразний і простий у користуванні API для автоматизації браузера й тестування. За замовчуванням Dusk не вимагає встановлювати JDK чи Selenium на ваш комп'ютер. Натомість Dusk використовує окремо встановлений [ChromeDriver](https://sites.google.com/chromium.org/driver). Проте ви вільні скористатися будь-яким іншим сумісним із Selenium драйвером.

<a name="installation"></a>
## Встановлення

Для початку встановіть [Google Chrome](https://www.google.com/chrome) і додайте до свого проєкту Composer-залежність `laravel/dusk`:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Якщо ви реєструєте сервіс-провайдер Dusk вручну, **ніколи** не реєструйте його у продакшн-середовищі: це може призвести до того, що будь-хто зможе автентифікуватися у вашому застосунку.

Після встановлення пакета Dusk виконайте артизан-команду `dusk:install`. Команда `dusk:install` створить каталог `tests/Browser`, приклад тесту Dusk і встановить бінарник Chrome Driver для вашої операційної системи:

```shell
php artisan dusk:install
```

Далі задайте змінну оточення `APP_URL` у файлі `.env` вашого застосунку. Це значення має збігатися з URL, за яким ви звертаєтеся до застосунку у браузері.

> [!NOTE]
> Якщо ви користуєтеся [Laravel Sail](/docs/{{version}}/sail) для керування локальним середовищем розробки, зверніться також до документації Sail щодо [налаштування й запуску тестів Dusk](/docs/{{version}}/sail#laravel-dusk).

<a name="managing-chromedriver-installations"></a>
### Керування встановленням ChromeDriver

Якщо ви хочете встановити версію ChromeDriver, відмінну від тієї, яку встановлює Laravel Dusk командою `dusk:install`, скористайтеся командою `dusk:chrome-driver`:

```shell
# Install the latest version of ChromeDriver for your OS...
php artisan dusk:chrome-driver

# Install a given version of ChromeDriver for your OS...
php artisan dusk:chrome-driver 86

# Install a given version of ChromeDriver for all supported OSs...
php artisan dusk:chrome-driver --all

# Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk вимагає, щоб бінарники `chromedriver` були виконуваними. Якщо у вас виникають проблеми із запуском Dusk, переконайтеся, що бінарники виконувані, такою командою: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### Використання інших браузерів

За замовчуванням Dusk запускає ваші браузерні тести в Google Chrome через окремо встановлений [ChromeDriver](https://sites.google.com/chromium.org/driver). Проте ви можете запустити власний сервер Selenium і виконувати тести в будь-якому браузері.

Для початку відкрийте файл `tests/DuskTestCase.php` - це базовий тест-кейс Dusk для вашого застосунку. У ньому ви можете прибрати виклик методу `startChromeDriver`. Це зупинить автоматичний запуск ChromeDriver у Dusk:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

Далі ви можете змінити метод `driver`, щоб підключитися до потрібних вам URL і порту. Крім того, ви можете змінити «бажані можливості» (desired capabilities), які передаються до WebDriver:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a name="getting-started"></a>
## Перші кроки

<a name="generating-tests"></a>
### Генерування тестів

Щоб згенерувати тест Dusk, скористайтеся артизан-командою `dusk:make`. Згенерований тест потрапить до каталогу `tests/Browser`:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### Скидання бази даних після кожного тесту

Більшість ваших тестів працюватимуть зі сторінками, які отримують дані з бази даних застосунку; проте ваші тести Dusk ніколи не повинні використовувати трейт `RefreshDatabase`. Трейт `RefreshDatabase` спирається на транзакції бази даних, які не застосовні й недоступні між HTTP-запитами. Натомість у вас є два варіанти: трейт `DatabaseMigrations` і трейт `DatabaseTruncation`.

<a name="reset-migrations"></a>
#### Використання міграцій бази даних

Трейт `DatabaseMigrations` запускатиме ваші міграції перед кожним тестом. Проте видалення й повторне створення таблиць для кожного тесту зазвичай повільніше за їх очищення:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    //
}
```

> [!WARNING]
> Бази даних SQLite в пам'яті не можна використовувати під час прогону тестів Dusk. Оскільки браузер виконується у власному процесі, він не матиме доступу до баз даних у пам'яті інших процесів.

<a name="reset-truncation"></a>
#### Використання очищення бази даних

Трейт `DatabaseTruncation` мігрує вашу базу даних на першому тесті, щоб переконатися, що таблиці створено належним чином. Проте в наступних тестах таблиці бази просто очищатимуться - це швидше, ніж щоразу проганяти всі міграції:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

pest()->use(DatabaseTruncation::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;

    //
}
```

За замовчуванням цей трейт очищає всі таблиці, окрім `migrations`. Якщо ви хочете вказати, які саме таблиці слід очищати, визначте у своєму тестовому класі властивість `$tablesToTruncate`:

> [!NOTE]
> Якщо ви користуєтеся Pest, визначайте властивості чи методи в базовому класі `DuskTestCase` або в будь-якому класі, який успадковує ваш тестовий файл.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

Або ж ви можете визначити у своєму тестовому класі властивість `$exceptTables`, щоб указати, які таблиці слід виключити з очищення:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

Щоб указати підключення до баз даних, чиї таблиці слід очищати, визначте у своєму тестовому класі властивість `$connectionsToTruncate`:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

Якщо ви хочете виконати код до або після очищення бази даних, визначте у своєму тестовому класі методи `beforeTruncatingDatabase` чи `afterTruncatingDatabase`:

```php
/**
 * Perform any work that should take place before the database has started truncating.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Perform any work that should take place after the database has finished truncating.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### Запуск тестів

Щоб запустити ваші браузерні тести, виконайте артизан-команду `dusk`:

```shell
php artisan dusk
```

Якщо під час останнього запуску команди `dusk` у вас були провалені тести, ви можете заощадити час, спершу перезапустивши саме їх командою `dusk:fails`:

```shell
php artisan dusk:fails
```

Команда `dusk` приймає будь-який аргумент, який зазвичай приймає раннер тестів Pest / PHPUnit, - наприклад, щоб запустити лише тести певної [групи](https://docs.phpunit.de/en/10.5/annotations.html#group):

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> Якщо ви користуєтеся [Laravel Sail](/docs/{{version}}/sail) для керування локальним середовищем розробки, зверніться до документації Sail щодо [налаштування й запуску тестів Dusk](/docs/{{version}}/sail#laravel-dusk).

<a name="manually-starting-chromedriver"></a>
#### Ручний запуск ChromeDriver

За замовчуванням Dusk автоматично намагається запустити ChromeDriver. Якщо у вашій системі це не працює, ви можете запустити ChromeDriver вручну перед виконанням команди `dusk`. Якщо ви вирішите запускати ChromeDriver вручну, закоментуйте такий рядок у файлі `tests/DuskTestCase.php`:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

Крім того, якщо ви запускаєте ChromeDriver на порту, відмінному від 9515, змініть метод `driver` того самого класу, щоб указати правильний порт:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### Робота із середовищем

Щоб змусити Dusk використовувати власний файл оточення під час прогону тестів, створіть у корені проєкту файл `.env.dusk.{environment}`. Наприклад, якщо ви запускатимете команду `dusk` із середовища `local`, створіть файл `.env.dusk.local`.

Під час прогону тестів Dusk створить резервну копію вашого файлу `.env` і перейменує ваше оточення Dusk на `.env`. Коли тести завершаться, ваш файл `.env` буде відновлено.

<a name="browser-basics"></a>
## Основи роботи з браузером

<a name="creating-browsers"></a>
### Створення браузерів

Для початку напишімо тест, який перевіряє, що ми можемо увійти до нашого застосунку. Згенерувавши тест, ми можемо змінити його так, щоб перейти на сторінку входу, ввести облікові дані й натиснути кнопку «Login». Щоб створити екземпляр браузера, викличте метод `browse` усередині вашого тесту Dusk:

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $user = User::factory()->create([
        'email' => 'taylor@laravel.com',
    ]);

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/login')
            ->type('email', $user->email)
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * A basic browser test example.
     */
    public function test_basic_example(): void
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/home');
        });
    }
}
```

Як видно з прикладу вище, метод `browse` приймає замикання. Dusk автоматично передасть до нього екземпляр браузера - це головний об'єкт для взаємодії з вашим застосунком і тверджень щодо нього.

<a name="creating-multiple-browsers"></a>
#### Створення кількох браузерів

Іноді для належного виконання тесту вам може знадобитися кілька браузерів. Наприклад, вони можуть знадобитися, щоб протестувати екран чату, який працює через вебсокети. Щоб створити кілька браузерів, просто додайте більше аргументів-браузерів до сигнатури замикання, переданого методу `browse`:

```php
$this->browse(function (Browser $first, Browser $second) {
    $first->loginAs(User::find(1))
        ->visit('/home')
        ->waitForText('Message');

    $second->loginAs(User::find(2))
        ->visit('/home')
        ->waitForText('Message')
        ->type('message', 'Hey Taylor')
        ->press('Send');

    $first->waitForText('Hey Taylor')
        ->assertSee('Jeffrey Way');
});
```

<a name="navigation"></a>
### Навігація

Метод `visit` дозволяє перейти до заданого URI у вашому застосунку:

```php
$browser->visit('/login');
```

Метод `visitRoute` дозволяє перейти до [іменованого маршруту](/docs/{{version}}/routing#named-routes):

```php
$browser->visitRoute($routeName, $parameters);
```

Ви можете переходити «назад» і «вперед» методами `back` та `forward`:

```php
$browser->back();

$browser->forward();
```

Метод `refresh` дозволяє оновити сторінку:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### Зміна розміру вікна браузера

Метод `resize` дозволяє змінити розмір вікна браузера:

```php
$browser->resize(1920, 1080);
```

Метод `maximize` дозволяє розгорнути вікно браузера на весь екран:

```php
$browser->maximize();
```

Метод `fitContent` змінить розмір вікна браузера так, щоб він відповідав розміру вмісту:

```php
$browser->fitContent();
```

Коли тест провалюється, Dusk автоматично змінює розмір браузера під вміст перед знімком екрана. Ви можете вимкнути цю поведінку, викликавши у своєму тесті метод `disableFitOnFailure`:

```php
$browser->disableFitOnFailure();
```

Метод `move` дозволяє перемістити вікно браузера в інше місце екрана:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### Макроси браузера

Якщо ви хочете визначити власний метод браузера, який можна перевикористовувати в різних тестах, скористайтеся методом `macro` класу `Browser`. Зазвичай цей метод викликають у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Browser::macro('scrollToElement', function (string $element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

Функція `macro` приймає першим аргументом ім'я, а другим - замикання. Замикання макроса виконається, коли ви викличете макрос як метод на екземплярі `Browser`:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### Автентифікація

Часто ви тестуватимете сторінки, які вимагають автентифікації. Щоб не взаємодіяти з екраном входу вашого застосунку в кожному тесті, скористайтеся методом Dusk `loginAs`. Метод `loginAs` приймає первинний ключ вашої моделі, придатної до автентифікації, або сам її екземпляр:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> Після використання методу `loginAs` сесія користувача зберігатиметься для всіх тестів у межах файлу.

<a name="cookies"></a>
### Cookie

Метод `cookie` дозволяє отримати чи задати значення зашифрованого cookie. За замовчуванням усі створені Laravel cookie зашифровані:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

Метод `plainCookie` дозволяє отримати чи задати значення незашифрованого cookie:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

Метод `deleteCookie` дозволяє видалити заданий cookie:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### Виконання JavaScript

Метод `script` дозволяє виконати у браузері довільні інструкції JavaScript:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### Знімок екрана

Метод `screenshot` дозволяє зробити знімок екрана й зберегти його із заданим іменем файлу. Усі знімки зберігаються в каталозі `tests/Browser/screenshots`:

```php
$browser->screenshot('filename');
```

Метод `responsiveScreenshots` дозволяє зробити серію знімків на різних брейкпоїнтах:

```php
$browser->responsiveScreenshots('filename');
```

Метод `screenshotElement` дозволяє зробити знімок конкретного елемента на сторінці:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### Збереження виводу консолі на диск

Метод `storeConsoleLog` дозволяє записати вивід консолі поточного браузера на диск під заданим іменем файлу. Вивід консолі зберігається в каталозі `tests/Browser/console`:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### Збереження коду сторінки на диск

Метод `storeSource` дозволяє записати код поточної сторінки на диск під заданим іменем файлу. Код сторінки зберігається в каталозі `tests/Browser/source`:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## Взаємодія з елементами

<a name="dusk-selectors"></a>
### Селектори Dusk

Вибір хороших CSS-селекторів для взаємодії з елементами - одна з найскладніших частин написання тестів Dusk. З часом зміни у фронтенді можуть зламати ваші тести через CSS-селектори на кшталт такого:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Селектори Dusk дозволяють зосередитися на написанні ефективних тестів, а не на запам'ятовуванні CSS-селекторів. Щоб визначити селектор, додайте до свого HTML-елемента атрибут `dusk`. Далі, взаємодіючи з браузером Dusk, додайте до селектора префікс `@`, щоб працювати з цим елементом у тесті:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

За бажання ви можете змінити HTML-атрибут, який використовує селектор Dusk, методом `selectorHtmlAttribute`. Зазвичай цей метод викликають у методі `boot` вашого `AppServiceProvider`:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### Текст, значення та атрибути

<a name="retrieving-setting-values"></a>
#### Отримання та задавання значень

Dusk надає кілька методів для роботи з поточним значенням, видимим текстом та атрибутами елементів на сторінці. Наприклад, щоб отримати «значення» елемента, який відповідає заданому CSS- чи Dusk-селектору, скористайтеся методом `value`:

```php
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

Метод `inputValue` дозволяє отримати «значення» елемента input із заданим іменем поля:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### Отримання тексту

Метод `text` дозволяє отримати видимий текст елемента, який відповідає заданому селектору:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### Отримання атрибутів

Нарешті, метод `attribute` дозволяє отримати значення атрибута елемента, який відповідає заданому селектору:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### Робота з формами

<a name="typing-values"></a>
#### Введення значень

Dusk надає різні методи для роботи з формами й полями введення. Спершу погляньмо на приклад введення тексту в поле:

```php
$browser->type('email', 'taylor@laravel.com');
```

Зверніть увагу: хоча метод за потреби приймає CSS-селектор, передавати його до методу `type` не обов'язково. Якщо CSS-селектор не задано, Dusk шукатиме поле `input` чи `textarea` із заданим атрибутом `name`.

Щоб додати текст до поля, не очищаючи його вмісту, скористайтеся методом `append`:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

Очистити значення поля можна методом `clear`:

```php
$browser->clear('email');
```

Ви можете вказати Dusk вводити текст повільно методом `typeSlowly`. За замовчуванням Dusk робить паузу 100 мілісекунд між натисканнями клавіш. Щоб змінити цей час, передайте потрібну кількість мілісекунд третім аргументом методу:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

Метод `appendSlowly` дозволяє повільно додавати текст:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### Випадні списки

Щоб обрати значення в елементі `select`, скористайтеся методом `select`. Як і методу `type`, методу `select` не потрібен повний CSS-селектор. Передаючи значення методу `select`, передавайте саме значення опції, а не видимий текст:

```php
$browser->select('size', 'Large');
```

Ви можете обрати випадкову опцію, не передаючи другого аргументу:

```php
$browser->select('size');
```

Передавши масив другим аргументом до методу `select`, ви можете вказати методу обрати кілька опцій:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### Чекбокси

Щоб «поставити галочку» в чекбоксі, скористайтеся методом `check`. Як і багатьом іншим методам для полів введення, повний CSS-селектор тут не потрібен. Якщо збігу за CSS-селектором не знайдено, Dusk шукатиме чекбокс із відповідним атрибутом `name`:

```php
$browser->check('terms');
```

Метод `uncheck` дозволяє «зняти галочку» з чекбокса:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### Радіокнопки

Щоб «обрати» опцію `radio`, скористайтеся методом `radio`. Як і багатьом іншим методам для полів введення, повний CSS-селектор тут не потрібен. Якщо збігу за CSS-селектором не знайдено, Dusk шукатиме поле `radio` з відповідними атрибутами `name` та `value`:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### Прикріплення файлів

Метод `attach` дозволяє прикріпити файл до елемента `file`. Як і багатьом іншим методам для полів введення, повний CSS-селектор тут не потрібен. Якщо збігу за CSS-селектором не знайдено, Dusk шукатиме поле `file` з відповідним атрибутом `name`:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> Функція attach вимагає, щоб на вашому сервері було встановлено й увімкнено розширення PHP `Zip`.

<a name="pressing-buttons"></a>
### Натискання кнопок

Метод `press` дозволяє клацнути по кнопці на сторінці. Аргументом методу `press` може бути або видимий текст кнопки, або CSS- чи Dusk-селектор:

```php
$browser->press('Login');
```

Надсилаючи форми, багато застосунків вимикають кнопку надсилання після натискання й вмикають її знову, коли HTTP-запит завершується. Щоб натиснути кнопку й дочекатися, доки її знову ввімкнуть, скористайтеся методом `pressAndWaitFor`:

```php
// Press the button and wait a maximum of 5 seconds for it to be enabled...
$browser->pressAndWaitFor('Save');

// Press the button and wait a maximum of 1 second for it to be enabled...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### Клацання по посиланнях

Щоб клацнути по посиланню, скористайтеся методом `clickLink` на екземплярі браузера. Метод `clickLink` клацне по посиланню із заданим видимим текстом:

```php
$browser->clickLink($linkText);
```

Метод `seeLink` дозволяє визначити, чи видиме на сторінці посилання із заданим видимим текстом:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> Ці методи працюють через jQuery. Якщо jQuery на сторінці немає, Dusk автоматично впровадить його, щоб він був доступний на час тесту.

<a name="using-the-keyboard"></a>
### Використання клавіатури

Метод `keys` дозволяє передавати елементу складніші послідовності введення, ніж дозволяє метод `type`. Наприклад, ви можете вказати Dusk утримувати клавіші-модифікатори під час введення значень. У цьому прикладі клавішу `shift` буде утримувано, доки в елемент, що відповідає заданому селектору, вводиться `taylor`. Після `taylor` буде введено `swift` уже без модифікаторів:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

Ще один корисний випадок для методу `keys` - надсилання комбінації «гарячих клавіш» до основного CSS-селектора вашого застосунку:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> Усі клавіші-модифікатори на кшталт `{command}` беруться у фігурні дужки `{}` і відповідають константам, визначеним у класі `Facebook\WebDriver\WebDriverKeys`, який можна [знайти на GitHub](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="fluent-keyboard-interactions"></a>
#### Плавна робота з клавіатурою

Dusk також надає метод `withKeyboard`, який дозволяє плавно виконувати складні взаємодії з клавіатурою через клас `Laravel\Dusk\Keyboard`. Клас `Keyboard` надає методи `press`, `release`, `type` та `pause`:

```php
use Laravel\Dusk\Keyboard;

$browser->withKeyboard(function (Keyboard $keyboard) {
    $keyboard->press('c')
        ->pause(1000)
        ->release('c')
        ->type(['c', 'e', 'o']);
});
```

<a name="keyboard-macros"></a>
#### Макроси клавіатури

Якщо ви хочете визначити власні взаємодії з клавіатурою, які легко перевикористовувати в усьому наборі тестів, скористайтеся методом `macro`, який надає клас `Keyboard`. Зазвичай цей метод викликають у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
<?php

namespace App\Providers;

use Facebook\WebDriver\WebDriverKeys;
use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Keyboard;
use Laravel\Dusk\OperatingSystem;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Keyboard::macro('copy', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'c',
            ]);

            return $this;
        });

        Keyboard::macro('paste', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'v',
            ]);

            return $this;
        });
    }
}
```

Функція `macro` приймає першим аргументом ім'я, а другим - замикання. Замикання макроса виконається, коли ви викличете макрос як метод на екземплярі `Keyboard`:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### Використання миші

<a name="clicking-on-elements"></a>
#### Клацання по елементах

Метод `click` дозволяє клацнути по елементу, який відповідає заданому CSS- чи Dusk-селектору:

```php
$browser->click('.selector');
```

Метод `clickAtXPath` дозволяє клацнути по елементу, який відповідає заданому виразу XPath:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

Метод `clickAtPoint` дозволяє клацнути по найвищому елементу за заданою парою координат відносно видимої області браузера:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

Метод `doubleClick` дозволяє симулювати подвійне клацання мишею:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

Метод `rightClick` дозволяє симулювати клацання правою кнопкою миші:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

Метод `clickAndHold` дозволяє симулювати натискання й утримування кнопки миші. Наступний виклик методу `releaseMouse` скасує цю поведінку й відпустить кнопку:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

Метод `controlClick` дозволяє симулювати у браузері подію `ctrl+click`:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

Методи `clickWhenVisible` чи `clickWhenEnabled` дозволяють дочекатися готовності елемента, перш ніж клацнути по ньому рівно один раз:

```php
$browser->clickWhenVisible('@save-button');
$browser->clickWhenEnabled('@submit-button');
```

<a name="mouseover"></a>
#### Наведення миші

Метод `mouseover` стане в пригоді, коли вам треба навести мишу на елемент, що відповідає заданому CSS- чи Dusk-селектору:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### Перетягування

Метод `drag` дозволяє перетягнути елемент, що відповідає заданому селектору, до іншого елемента:

```php
$browser->drag('.from-selector', '.to-selector');
```

Або ж ви можете перетягнути елемент в одному напрямку:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

Нарешті, ви можете перетягнути елемент на заданий зсув:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### Діалоги JavaScript

Dusk надає різні методи для роботи з діалогами JavaScript. Наприклад, метод `waitForDialog` дозволяє дочекатися появи діалогу JavaScript. Цей метод приймає необов'язковий аргумент - скільки секунд чекати на появу діалогу:

```php
$browser->waitForDialog($seconds = null);
```

Метод `assertDialogOpened` дозволяє перевірити, що діалог було показано і що він містить задане повідомлення:

```php
$browser->assertDialogOpened('Dialog message');
```

Якщо діалог JavaScript містить поле введення, ви можете скористатися методом `typeInDialog`, щоб ввести туди значення:

```php
$browser->typeInDialog('Hello World');
```

Щоб закрити відкритий діалог JavaScript натисканням кнопки «OK», викличте метод `acceptDialog`:

```php
$browser->acceptDialog();
```

Щоб закрити відкритий діалог JavaScript натисканням кнопки «Cancel», викличте метод `dismissDialog`:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### Робота з вбудованими фреймами

Якщо вам потрібно взаємодіяти з елементами всередині iframe, скористайтеся методом `withinFrame`. Усі взаємодії з елементами всередині замикання, переданого методу `withinFrame`, будуть обмежені контекстом указаного iframe:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### Обмеження селекторів

Іноді вам може знадобитися виконати кілька операцій, обмеживши їх усі заданим селектором. Наприклад, ви можете захотіти перевірити, що певний текст є лише в таблиці, а потім клацнути по кнопці всередині цієї таблиці. Для цього скористайтеся методом `with`. Усі операції всередині замикання, переданого методу `with`, будуть обмежені початковим селектором:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

Іноді вам може знадобитися виконати твердження поза межами поточного обмеження. Для цього скористайтеся методами `elsewhere` та `elsewhereWhenAvailable`:

```php
$browser->with('.table', function (Browser $table) {
    // Current scope is `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### Очікування елементів

Тестуючи застосунки, які активно використовують JavaScript, часто доводиться «чекати» на доступність певних елементів чи даних, перш ніж рухатися далі. Dusk робить це дуже просто. За допомогою різних методів ви можете дочекатися, доки елементи стануть видимими на сторінці, або навіть доки заданий вираз JavaScript не набуде значення `true`.

<a name="waiting"></a>
#### Очікування

Якщо вам просто треба призупинити тест на задану кількість мілісекунд, скористайтеся методом `pause`:

```php
$browser->pause(1000);
```

Якщо тест треба призупинити лише за умови, що задана умова істинна (`true`), скористайтеся методом `pauseIf`:

```php
$browser->pauseIf(App::environment('production'), 1000);
```

Так само, якщо тест треба призупинити, доки задана умова не стане істинною (`true`), скористайтеся методом `pauseUnless`:

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### Очікування селекторів

Метод `waitFor` дозволяє призупинити виконання тесту, доки на сторінці не з'явиться елемент, що відповідає заданому CSS- чи Dusk-селектору. За замовчуванням тест буде призупинено максимум на п'ять секунд, після чого буде кинуто виняток. За потреби ви можете передати власний поріг очікування другим аргументом методу:

```php
// Wait a maximum of five seconds for the selector...
$browser->waitFor('.selector');

// Wait a maximum of one second for the selector...
$browser->waitFor('.selector', 1);
```

Ви також можете дочекатися, доки елемент, що відповідає заданому селектору, не міститиме заданий текст:

```php
// Wait a maximum of five seconds for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World');

// Wait a maximum of one second for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

Ви також можете дочекатися, доки елемент, що відповідає заданому селектору, зникне зі сторінки:

```php
// Wait a maximum of five seconds until the selector is missing...
$browser->waitUntilMissing('.selector');

// Wait a maximum of one second until the selector is missing...
$browser->waitUntilMissing('.selector', 1);
```

Або ж ви можете дочекатися, доки елемент, що відповідає заданому селектору, стане увімкненим чи вимкненим:

```php
// Wait a maximum of five seconds until the selector is enabled...
$browser->waitUntilEnabled('.selector');

// Wait a maximum of one second until the selector is enabled...
$browser->waitUntilEnabled('.selector', 1);

// Wait a maximum of five seconds until the selector is disabled...
$browser->waitUntilDisabled('.selector');

// Wait a maximum of one second until the selector is disabled...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### Обмеження селекторів за доступністю

Іноді вам може знадобитися дочекатися появи елемента, що відповідає заданому селектору, а потім із ним попрацювати. Наприклад, дочекатися появи модального вікна й натиснути в ньому кнопку «OK». Для цього скористайтеся методом `whenAvailable`. Усі операції з елементами всередині заданого замикання будуть обмежені початковим селектором:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### Очікування тексту

Метод `waitForText` дозволяє дочекатися, доки на сторінці не з'явиться заданий текст:

```php
// Wait a maximum of five seconds for the text...
$browser->waitForText('Hello World');

// Wait a maximum of one second for the text...
$browser->waitForText('Hello World', 1);
```

Метод `waitUntilMissingText` дозволяє дочекатися, доки показаний текст не зникне зі сторінки:

```php
// Wait a maximum of five seconds for the text to be removed...
$browser->waitUntilMissingText('Hello World');

// Wait a maximum of one second for the text to be removed...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### Очікування посилань

Метод `waitForLink` дозволяє дочекатися, доки на сторінці не з'явиться заданий текст посилання:

```php
// Wait a maximum of five seconds for the link...
$browser->waitForLink('Create');

// Wait a maximum of one second for the link...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### Очікування полів введення

Метод `waitForInput` дозволяє дочекатися, доки задане поле введення стане видимим на сторінці:

```php
// Wait a maximum of five seconds for the input...
$browser->waitForInput($field);

// Wait a maximum of one second for the input...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### Очікування розташування сторінки

Коли ви робите твердження щодо шляху на кшталт `$browser->assertPathIs('/home')`, воно може провалитися, якщо `window.location.pathname` оновлюється асинхронно. Скористайтеся методом `waitForLocation`, щоб дочекатися, доки розташування набуде заданого значення:

```php
$browser->waitForLocation('/secret');
```

Метод `waitForLocation` можна також використати, щоб дочекатися, доки поточне розташування вікна стане повним URL:

```php
$browser->waitForLocation('https://example.com/path');
```

Ви також можете дочекатися розташування [іменованого маршруту](/docs/{{version}}/routing#named-routes):

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### Очікування перезавантаження сторінки

Якщо після виконання дії вам треба дочекатися перезавантаження сторінки, скористайтеся методом `waitForReload`:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

Оскільки потреба дочекатися перезавантаження зазвичай виникає після натискання кнопки, для зручності ви можете скористатися методом `clickAndWaitForReload`:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### Очікування виразів JavaScript

Іноді вам може знадобитися призупинити виконання тесту, доки заданий вираз JavaScript не набуде значення `true`. Легко зробити це можна методом `waitUntil`. Передаючи цьому методу вираз, вам не треба додавати ключове слово `return` чи крапку з комою в кінці:

```php
// Wait a maximum of five seconds for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0');

// Wait a maximum of one second for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Очікування виразів Vue

Методи `waitUntilVue` та `waitUntilVueIsNot` дозволяють дочекатися, доки атрибут [компонента Vue](https://vuejs.org) набуде заданого значення:

```php
// Wait until the component attribute contains the given value...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// Wait until the component attribute doesn't contain the given value...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### Очікування подій JavaScript

Метод `waitForEvent` дозволяє призупинити виконання тесту, доки не станеться подія JavaScript:

```php
$browser->waitForEvent('load');
```

Слухач події прикріплюється до поточного обмеження, яким за замовчуванням є елемент `body`. Якщо ви користуєтеся обмеженим селектором, слухач буде прикріплено до відповідного елемента:

```php
$browser->with('iframe', function (Browser $iframe) {
    // Wait for the iframe's load event...
    $iframe->waitForEvent('load');
});
```

Ви також можете передати селектор другим аргументом до методу `waitForEvent`, щоб прикріпити слухач до конкретного елемента:

```php
$browser->waitForEvent('load', '.selector');
```

Ви також можете чекати на події об'єктів `document` та `window`:

```php
// Wait until the document is scrolled...
$browser->waitForEvent('scroll', 'document');

// Wait a maximum of five seconds until the window is resized...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### Очікування з колбеком

Багато методів очікування в Dusk спираються на метод `waitUsing`. Ви можете скористатися ним напряму, щоб дочекатися, доки задане замикання поверне `true`. Метод `waitUsing` приймає максимальну кількість секунд очікування, інтервал перевірки замикання, саме замикання та необов'язкове повідомлення про помилку:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### Прокручування до елемента

Іноді ви не зможете клацнути по елементу, бо він поза видимою областю браузера. Метод `scrollIntoView` прокрутить вікно браузера, доки елемент за заданим селектором не потрапить у поле зору:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## Доступні твердження

Dusk надає різні твердження, які ви можете робити щодо свого застосунку. Усі доступні твердження задокументовані в списку нижче:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[assertTitle](#assert-title)
[assertTitleContains](#assert-title-contains)
[assertUrlIs](#assert-url-is)
[assertSchemeIs](#assert-scheme-is)
[assertSchemeIsNot](#assert-scheme-is-not)
[assertHostIs](#assert-host-is)
[assertHostIsNot](#assert-host-is-not)
[assertPortIs](#assert-port-is)
[assertPortIsNot](#assert-port-is-not)
[assertPathBeginsWith](#assert-path-begins-with)
[assertPathEndsWith](#assert-path-ends-with)
[assertPathContains](#assert-path-contains)
[assertPathIs](#assert-path-is)
[assertPathIsNot](#assert-path-is-not)
[assertRouteIs](#assert-route-is)
[assertQueryStringHas](#assert-query-string-has)
[assertQueryStringMissing](#assert-query-string-missing)
[assertFragmentIs](#assert-fragment-is)
[assertFragmentBeginsWith](#assert-fragment-begins-with)
[assertFragmentIsNot](#assert-fragment-is-not)
[assertHasCookie](#assert-has-cookie)
[assertHasPlainCookie](#assert-has-plain-cookie)
[assertCookieMissing](#assert-cookie-missing)
[assertPlainCookieMissing](#assert-plain-cookie-missing)
[assertCookieValue](#assert-cookie-value)
[assertPlainCookieValue](#assert-plain-cookie-value)
[assertSee](#assert-see)
[assertDontSee](#assert-dont-see)
[assertSeeIn](#assert-see-in)
[assertDontSeeIn](#assert-dont-see-in)
[assertSeeAnythingIn](#assert-see-anything-in)
[assertSeeNothingIn](#assert-see-nothing-in)
[assertCount](#assert-count)
[assertScript](#assert-script)
[assertSourceHas](#assert-source-has)
[assertSourceMissing](#assert-source-missing)
[assertSeeLink](#assert-see-link)
[assertDontSeeLink](#assert-dont-see-link)
[assertInputValue](#assert-input-value)
[assertInputValueIsNot](#assert-input-value-is-not)
[assertChecked](#assert-checked)
[assertNotChecked](#assert-not-checked)
[assertIndeterminate](#assert-indeterminate)
[assertRadioSelected](#assert-radio-selected)
[assertRadioNotSelected](#assert-radio-not-selected)
[assertSelected](#assert-selected)
[assertNotSelected](#assert-not-selected)
[assertSelectHasOptions](#assert-select-has-options)
[assertSelectMissingOptions](#assert-select-missing-options)
[assertSelectHasOption](#assert-select-has-option)
[assertSelectMissingOption](#assert-select-missing-option)
[assertValue](#assert-value)
[assertValueIsNot](#assert-value-is-not)
[assertAttribute](#assert-attribute)
[assertAttributeMissing](#assert-attribute-missing)
[assertAttributeContains](#assert-attribute-contains)
[assertAttributeDoesntContain](#assert-attribute-doesnt-contain)
[assertAriaAttribute](#assert-aria-attribute)
[assertDataAttribute](#assert-data-attribute)
[assertVisible](#assert-visible)
[assertPresent](#assert-present)
[assertNotPresent](#assert-not-present)
[assertMissing](#assert-missing)
[assertInputPresent](#assert-input-present)
[assertInputMissing](#assert-input-missing)
[assertDialogOpened](#assert-dialog-opened)
[assertEnabled](#assert-enabled)
[assertDisabled](#assert-disabled)
[assertButtonEnabled](#assert-button-enabled)
[assertButtonDisabled](#assert-button-disabled)
[assertFocused](#assert-focused)
[assertNotFocused](#assert-not-focused)
[assertAuthenticated](#assert-authenticated)
[assertGuest](#assert-guest)
[assertAuthenticatedAs](#assert-authenticated-as)
[assertVue](#assert-vue)
[assertVueIsNot](#assert-vue-is-not)
[assertVueContains](#assert-vue-contains)
[assertVueDoesntContain](#assert-vue-doesnt-contain)

</div>

<a name="assert-title"></a>
#### assertTitle

Перевіряє, що заголовок сторінки збігається із заданим текстом:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

Перевіряє, що заголовок сторінки містить заданий текст:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

Перевіряє, що поточний URL (без рядка запиту) збігається із заданим рядком:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

Перевіряє, що схема поточного URL збігається із заданою:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

Перевіряє, що схема поточного URL не збігається із заданою:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

Перевіряє, що хост поточного URL збігається із заданим:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

Перевіряє, що хост поточного URL не збігається із заданим:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

Перевіряє, що порт поточного URL збігається із заданим:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

Перевіряє, що порт поточного URL не збігається із заданим:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

Перевіряє, що шлях поточного URL починається із заданого:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

Перевіряє, що шлях поточного URL закінчується заданим:

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

Перевіряє, що шлях поточного URL містить заданий:

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

Перевіряє, що поточний шлях збігається із заданим:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

Перевіряє, що поточний шлях не збігається із заданим:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

Перевіряє, що поточний URL збігається з URL заданого [іменованого маршруту](/docs/{{version}}/routing#named-routes):

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

Перевіряє, що заданий параметр рядка запиту присутній:

```php
$browser->assertQueryStringHas($name);
```

Перевіряє, що заданий параметр рядка запиту присутній і має задане значення:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

Перевіряє, що заданого параметра рядка запиту немає:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

Перевіряє, що поточний хеш-фрагмент URL збігається із заданим:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

Перевіряє, що поточний хеш-фрагмент URL починається із заданого:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

Перевіряє, що поточний хеш-фрагмент URL не збігається із заданим:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

Перевіряє, що заданий зашифрований cookie присутній:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

Перевіряє, що заданий незашифрований cookie присутній:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

Перевіряє, що заданого зашифрованого cookie немає:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

Перевіряє, що заданого незашифрованого cookie немає:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

Перевіряє, що зашифрований cookie має задане значення:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

Перевіряє, що незашифрований cookie має задане значення:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

Перевіряє, що заданий текст присутній на сторінці:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

Перевіряє, що заданого тексту немає на сторінці:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

Перевіряє, що заданий текст присутній усередині селектора:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

Перевіряє, що заданого тексту немає всередині селектора:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

Перевіряє, що всередині селектора є будь-який текст:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

Перевіряє, що всередині селектора немає жодного тексту:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### assertCount

Перевіряє, що елементи, які відповідають заданому селектору, трапляються вказану кількість разів:

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### assertScript

Перевіряє, що заданий вираз JavaScript обчислюється в задане значення:

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

Перевіряє, що заданий код присутній на сторінці:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

Перевіряє, що заданого коду немає на сторінці:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

Перевіряє, що задане посилання присутнє на сторінці:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

Перевіряє, що заданого посилання немає на сторінці:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

Перевіряє, що задане поле введення має задане значення:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

Перевіряє, що задане поле введення не має заданого значення:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

Перевіряє, що заданий чекбокс позначено:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

Перевіряє, що заданий чекбокс не позначено:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

Перевіряє, що заданий чекбокс перебуває в невизначеному стані:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

Перевіряє, що задану радіокнопку обрано:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

Перевіряє, що задану радіокнопку не обрано:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

Перевіряє, що в заданому випадному списку обрано задане значення:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

Перевіряє, що в заданому випадному списку не обрано заданого значення:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

Перевіряє, що заданий масив значень доступний для вибору:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

Перевіряє, що заданий масив значень недоступний для вибору:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

Перевіряє, що задане значення доступне для вибору в заданому полі:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

Перевіряє, що задане значення недоступне для вибору:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

Перевіряє, що елемент, який відповідає заданому селектору, має задане значення:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

Перевіряє, що елемент, який відповідає заданому селектору, не має заданого значення:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

Перевіряє, що елемент, який відповідає заданому селектору, має задане значення у вказаному атрибуті:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

Перевіряє, що в елемента, який відповідає заданому селектору, немає вказаного атрибута:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

Перевіряє, що елемент, який відповідає заданому селектору, містить задане значення у вказаному атрибуті:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

Перевіряє, що елемент, який відповідає заданому селектору, не містить заданого значення у вказаному атрибуті:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

Перевіряє, що елемент, який відповідає заданому селектору, має задане значення у вказаному атрибуті aria:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

Наприклад, для розмітки `<button aria-label="Add"></button>` ви можете зробити твердження щодо атрибута `aria-label` ось так:

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

Перевіряє, що елемент, який відповідає заданому селектору, має задане значення у вказаному атрибуті data:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

Наприклад, для розмітки `<tr id="row-1" data-content="attendees"></tr>` ви можете зробити твердження щодо атрибута `data-content` ось так:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

Перевіряє, що елемент, який відповідає заданому селектору, видимий:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

Перевіряє, що елемент, який відповідає заданому селектору, присутній у коді сторінки:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

Перевіряє, що елемента, який відповідає заданому селектору, немає в коді сторінки:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

Перевіряє, що елемент, який відповідає заданому селектору, не видимий:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

Перевіряє, що поле введення із заданим іменем присутнє:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

Перевіряє, що поля введення із заданим іменем немає в коді сторінки:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

Перевіряє, що діалог JavaScript із заданим повідомленням було відкрито:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

Перевіряє, що задане поле увімкнене:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

Перевіряє, що задане поле вимкнене:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

Перевіряє, що задана кнопка увімкнена:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

Перевіряє, що задана кнопка вимкнена:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

Перевіряє, що задане поле у фокусі:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

Перевіряє, що задане поле не у фокусі:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

Перевіряє, що користувач автентифікований:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

Перевіряє, що користувач не автентифікований:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

Перевіряє, що користувач автентифікований як заданий користувач:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk дозволяє навіть робити твердження щодо стану даних [компонента Vue](https://vuejs.org). Уявіть, наприклад, що ваш застосунок містить такий компонент Vue:

    // HTML...

    <profile dusk="profile-component"></profile>

    // Component Definition...

    Vue.component('profile', {
        template: '<div>{{ user.name }}</div>',

        data: function () {
            return {
                user: {
                    name: 'Taylor'
                }
            };
        }
    });

Ви можете зробити твердження щодо стану компонента Vue ось так:

```php tab=Pest
test('vue', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
});
```

```php tab=PHPUnit
/**
 * A basic Vue test example.
 */
public function test_vue(): void
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
#### assertVueIsNot

Перевіряє, що задана властивість даних компонента Vue не збігається із заданим значенням:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Перевіряє, що задана властивість даних компонента Vue є масивом і містить задане значення:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

Перевіряє, що задана властивість даних компонента Vue є масивом і не містить заданого значення:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## Сторінки

Іноді тести вимагають виконати послідовно кілька складних дій. Через це тести стає важче читати й розуміти. Сторінки Dusk дозволяють описати виразні дії, які потім можна виконати на заданій сторінці одним методом. Сторінки також дозволяють описати скорочення для поширених селекторів вашого застосунку або окремої сторінки.

<a name="generating-pages"></a>
### Генерування сторінок

Щоб згенерувати об'єкт сторінки, виконайте артизан-команду `dusk:page`. Усі об'єкти сторінок потраплять до каталогу `tests/Browser/Pages` вашого застосунку:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### Налаштування сторінок

За замовчуванням сторінки мають три методи: `url`, `assert` та `elements`. Методи `url` та `assert` ми розглянемо зараз. Метод `elements` буде [докладніше розглянуто нижче](#shorthand-selectors).

<a name="the-url-method"></a>
#### Метод `url`

Метод `url` має повертати шлях URL, що представляє сторінку. Dusk використовуватиме цей URL, переходячи до сторінки у браузері:

```php
/**
 * Get the URL for the page.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### Метод `assert`

Метод `assert` може містити будь-які твердження, потрібні, щоб переконатися, що браузер справді на заданій сторінці. Розміщувати щось у цьому методі не обов'язково; проте ви вільні робити такі твердження за бажання. Ці твердження виконуватимуться автоматично при переході до сторінки:

```php
/**
 * Assert that the browser is on the page.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### Перехід до сторінок

Коли сторінку визначено, ви можете перейти до неї методом `visit`:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

Іноді ви вже перебуваєте на заданій сторінці, і вам треба «завантажити» її селектори й методи до поточного контексту тесту. Так буває, коли ви натискаєте кнопку й вас перенаправляє на сторінку без явного переходу до неї. У такому разі скористайтеся методом `on`, щоб завантажити сторінку:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### Скорочені селектори

Метод `elements` у класах сторінок дозволяє описати швидкі й легкі для запам'ятовування скорочення для будь-якого CSS-селектора на вашій сторінці. Наприклад, визначмо скорочення для поля «email» на сторінці входу застосунку:

```php
/**
 * Get the element shortcuts for the page.
 *
 * @return array<string, string>
 */
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

Коли скорочення визначено, ви можете використовувати скорочений селектор усюди, де зазвичай використовували б повний CSS-селектор:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### Глобальні скорочені селектори

Після встановлення Dusk базовий клас `Page` потрапить до вашого каталогу `tests/Browser/Pages`. Цей клас містить метод `siteElements`, який дозволяє описати глобальні скорочені селектори, доступні на кожній сторінці вашого застосунку:

```php
/**
 * Get the global element shortcuts for the site.
 *
 * @return array<string, string>
 */
public static function siteElements(): array
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### Методи сторінок

Окрім стандартних методів сторінок, ви можете визначити додаткові методи, якими користуватиметеся у своїх тестах. Уявімо, наприклад, що ми будуємо застосунок для керування музикою. Поширеною дією на одній зі сторінок може бути створення плейлиста. Замість того щоб переписувати логіку створення плейлиста в кожному тесті, ви можете визначити метод `createPlaylist` у класі сторінки:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // Other page methods...

    /**
     * Create a new playlist.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

Коли метод визначено, ви можете скористатися ним у будь-якому тесті, що використовує цю сторінку. Екземпляр браузера автоматично передається першим аргументом до власних методів сторінки:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## Компоненти

Компоненти схожі на «об'єкти сторінок» Dusk, але призначені для частин UI та функціональності, які перевикористовуються в усьому застосунку, - наприклад, панель навігації чи вікно сповіщень. Тому компоненти не прив'язані до конкретних URL.

<a name="generating-components"></a>
### Генерування компонентів

Щоб згенерувати компонент, виконайте артизан-команду `dusk:component`. Нові компоненти потрапляють до каталогу `tests/Browser/Components`:

```shell
php artisan dusk:component DatePicker
```

Як показано вище, «вибір дати» - приклад компонента, який може траплятися в усьому застосунку на різних сторінках. Писати вручну логіку автоматизації браузера для вибору дати в десятках тестів стає обтяжливо. Натомість ми можемо описати компонент Dusk, який представлятиме вибір дати, і інкапсулювати цю логіку в ньому:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * Get the root selector for the component.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * Assert that the browser page contains the component.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * Get the element shortcuts for the component.
     *
     * @return array<string, string>
     */
    public function elements(): array
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

    /**
     * Select the given date.
     */
    public function selectDate(Browser $browser, int $year, int $month, int $day): void
    {
        $browser->click('@date-field')
            ->within('@year-list', function (Browser $browser) use ($year) {
                $browser->click($year);
            })
            ->within('@month-list', function (Browser $browser) use ($month) {
                $browser->click($month);
            })
            ->within('@day-list', function (Browser $browser) use ($day) {
                $browser->click($day);
            });
    }
}
```

<a name="using-components"></a>
### Використання компонентів

Коли компонент визначено, ми можемо легко обрати дату у виборі дати з будь-якого тесту. І якщо логіка вибору дати зміниться, нам треба буде оновити лише компонент:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->within(new DatePicker, function (Browser $browser) {
                $browser->selectDate(2019, 1, 30);
            })
            ->assertSee('January');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    /**
     * A basic component test example.
     */
    public function test_basic_example(): void
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                ->within(new DatePicker, function (Browser $browser) {
                    $browser->selectDate(2019, 1, 30);
                })
                ->assertSee('January');
        });
    }
}
```

Метод `component` дозволяє отримати екземпляр браузера, обмежений заданим компонентом:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## Неперервна інтеграція

> [!WARNING]
> Більшість конфігурацій неперервної інтеграції для Dusk очікують, що ваш застосунок Laravel віддається вбудованим сервером розробки PHP на порту 8000. Тому, перш ніж рухатися далі, переконайтеся, що у вашому середовищі неперервної інтеграції змінна оточення `APP_URL` має значення `http://127.0.0.1:8000`.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

Щоб запускати тести Dusk на [Heroku CI](https://www.heroku.com/continuous-integration), додайте до свого файлу `app.json` для Heroku такий buildpack для Google Chrome і скрипти:

```json
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-chrome-for-testing" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux --port=9515 > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
### Travis CI

Щоб запускати ваші тести Dusk на [Travis CI](https://travis-ci.org), скористайтеся такою конфігурацією `.travis.yml`. Оскільки Travis CI не є графічним середовищем, нам знадобиться кілька додаткових кроків, щоб запустити браузер Chrome. Крім того, ми скористаємося `php artisan serve`, щоб запустити вбудований вебсервер PHP:

```yaml
language: php

php:
  - 8.2

addons:
  chrome: stable

install:
  - cp .env.testing .env
  - travis_retry composer install --no-interaction --prefer-dist
  - php artisan key:generate
  - php artisan dusk:chrome-driver

before_script:
  - google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
  - php artisan serve --no-reload &

script:
  - php artisan dusk
```

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Якщо ви запускаєте свої тести Dusk через [GitHub Actions](https://github.com/features/actions), можете взяти за відправну точку такий конфігураційний файл. Як і у випадку з TravisCI, ми скористаємося командою `php artisan serve`, щоб запустити вбудований вебсервер PHP:

```yaml
name: CI
on: [push]
jobs:

  dusk-php:
    runs-on: ubuntu-latest
    env:
      APP_URL: "http://127.0.0.1:8000"
      DB_USERNAME: root
      DB_PASSWORD: root
      MAIL_MAILER: log
    steps:
      - uses: actions/checkout@v5
      - name: Prepare The Environment
        run: cp .env.example .env
      - name: Create Database
        run: |
          sudo systemctl start mysql
          mysql --user="root" --password="root" -e "CREATE DATABASE \`my-database\` character set UTF8mb4 collate utf8mb4_bin;"
      - name: Install Composer Dependencies
        run: composer install --no-progress --prefer-dist --optimize-autoloader
      - name: Generate Application Key
        run: php artisan key:generate
      - name: Upgrade Chrome Driver
        run: php artisan dusk:chrome-driver --detect
      - name: Start Chrome Driver
        run: ./vendor/laravel/dusk/bin/chromedriver-linux --port=9515 &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: console
          path: tests/Browser/console
```

<a name="running-tests-on-chipper-ci"></a>
### Chipper CI

Якщо ви запускаєте свої тести Dusk через [Chipper CI](https://chipperci.com), можете взяти за відправну точку такий конфігураційний файл. Ми скористаємося вбудованим сервером PHP, щоб запустити Laravel і слухати запити:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Include Chrome in the build environment
services:
  - dusk

# Build all commits
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Create a dusk env file, ensuring APP_URL uses BUILD_HOST
      cp -v .env .env.dusk.ci
      sed -i "s@APP_URL=.*@APP_URL=http://$BUILD_HOST:8000@g" .env.dusk.ci

  - name: Compile Assets
    cmd: |
      npm ci --no-audit
      npm run build

  - name: Browser Tests
    cmd: |
      php -S [::0]:8000 -t public 2>server.log &
      sleep 2
      php artisan dusk:chrome-driver $CHROME_DRIVER
      php artisan dusk --env=ci
```

Щоб дізнатися більше про запуск тестів Dusk на Chipper CI, зокрема про роботу з базами даних, зверніться до [офіційної документації Chipper CI](https://chipperci.com/docs/testing/laravel-dusk-new/).
