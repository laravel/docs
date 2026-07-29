---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Тестування: перші кроки

- [Вступ](#introduction)
- [Середовище](#environment)
- [Створення тестів](#creating-tests)
- [Запуск тестів](#running-tests)
    - [Паралельний запуск тестів](#running-tests-in-parallel)
    - [Звіт про покриття тестами](#reporting-test-coverage)
    - [Профілювання тестів](#profiling-tests)
- [Кешування конфігурації](#configuration-caching)

<a name="introduction"></a>
## Вступ

Laravel створювався з думкою про тестування. Підтримка тестування через [Pest](https://pestphp.com) та [PHPUnit](https://phpunit.de) доступна одразу з коробки, а файл `phpunit.xml` уже налаштований для вашого застосунку. Фреймворк також містить зручні допоміжні методи, які дозволяють виразно тестувати ваші застосунки.

За замовчуванням каталог `tests` вашого застосунку містить два підкаталоги: `Feature` та `Unit`. Юніт-тести зосереджені на дуже маленькій, ізольованій частині коду. Власне, більшість юніт-тестів, найімовірніше, перевіряють один метод. Тести з каталогу «Unit» не запускають ваш застосунок Laravel, а тому не мають доступу ні до бази даних, ні до інших сервісів фреймворку.

Функціональні тести можуть перевіряти більшу частину вашого коду - зокрема те, як кілька об'єктів взаємодіють між собою, чи навіть повний HTTP-запит до JSON-ендпоїнта. **Загалом більшість ваших тестів мають бути функціональними. Саме такі тести дають найбільшу впевненість, що ваша система працює як задумано.**

Файл `ExampleTest.php` є в обох каталогах - `Feature` та `Unit`. Після встановлення нового застосунку Laravel виконайте команду `vendor/bin/pest`, `vendor/bin/phpunit` чи `php artisan test`, щоб запустити тести.

<a name="environment"></a>
## Середовище

Під час запуску тестів Laravel автоматично встановлює [середовище конфігурації](/docs/{{version}}/configuration#environment-configuration) у `testing` - завдяки змінним оточення, визначеним у файлі `phpunit.xml`. Laravel також автоматично налаштовує сесію та кеш на драйвер `array`, тож під час тестування дані сесії й кешу ніде не зберігатимуться.

Ви вільні задавати за потреби й інші значення конфігурації тестового середовища. Змінні оточення `testing` можна налаштувати у файлі `phpunit.xml` вашого застосунку, але не забудьте скинути кеш конфігурації артизан-командою `config:clear`, перш ніж запускати тести!

<a name="the-env-testing-environment-file"></a>
#### Файл оточення `.env.testing`

Крім того, ви можете створити файл `.env.testing` у корені вашого проєкту. Він використовуватиметься замість файлу `.env` під час запуску тестів Pest і PHPUnit або артизан-команд з опцією `--env=testing`.

<a name="creating-tests"></a>
## Створення тестів

Щоб створити новий тест-кейс, скористайтеся артизан-командою `make:test`. За замовчуванням тести потрапляють до каталогу `tests/Feature`:

```shell
php artisan make:test UserTest
```

Якщо ви хочете створити тест у каталозі `tests/Unit`, додайте до команди `make:test` опцію `--unit`:

```shell
php artisan make:test UserTest --unit
```

Якщо у вас є тестовий клас, який здебільшого спирається на можливості тестування Laravel, але окремому тестовому методу не потрібен запущений фреймворк, застосуйте до цього методу атрибут `#[UnitTest]`, щоб пропустити запуск застосунку саме для нього.

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\Attributes\UnitTest;
use Tests\TestCase;

class LocationServiceTest extends TestCase
{
    public function test_get_coordinates_resolves_address(): void
    {
        // This test uses Laravel's testing features...
    }

    #[UnitTest]
    public function test_get_state_returns_state_from_abbreviation(): void
    {
        // This test runs without booting the application...
    }
}
```

> [!NOTE]
> Заготовки тестів можна налаштувати через [публікацію заготовок](/docs/{{version}}/artisan#stub-customization).

Коли тест згенеровано, ви можете описати його як зазвичай - через Pest чи PHPUnit. Щоб запустити тести, виконайте в терміналі команду `vendor/bin/pest`, `vendor/bin/phpunit` чи `php artisan test`:

```php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> Якщо ви визначаєте у тестовому класі власні методи `setUp` / `tearDown`, обов'язково викликайте відповідні методи батьківського класу `parent::setUp()` / `parent::tearDown()`. Зазвичай `parent::setUp()` викликають на початку власного методу `setUp`, а `parent::tearDown()` - наприкінці методу `tearDown`.

<a name="running-tests"></a>
## Запуск тестів

Як згадувалося раніше, коли ви написали тести, запустити їх можна через `pest` чи `phpunit`:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

Окрім команд `pest` чи `phpunit`, ви можете запускати тести артизан-командою `test`. Артизан-раннер тестів дає докладні звіти, що полегшує розробку й налагодження:

```shell
php artisan test
```

Будь-які аргументи, які можна передати командам `pest` чи `phpunit`, можна передати й артизан-команді `test`:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### Паралельний запуск тестів

За замовчуванням Laravel і Pest / PHPUnit виконують ваші тести послідовно в одному процесі. Проте ви можете суттєво скоротити час прогону, запускаючи тести одночасно в кількох процесах. Для початку встановіть Composer-пакет `brianium/paratest` як «dev»-залежність. Далі додайте опцію `--parallel` до артизан-команди `test`:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

За замовчуванням Laravel створить стільки процесів, скільки ядер CPU доступно на вашій машині. Проте ви можете змінити їхню кількість опцією `--processes`:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> Під час паралельного запуску тестів деякі опції Pest / PHPUnit (наприклад, `--do-not-cache-result`) можуть бути недоступні.

<a name="parallel-testing-and-databases"></a>
#### Паралельне тестування й бази даних

Якщо ви налаштували основне підключення до бази даних, Laravel автоматично подбає про створення та міграцію тестової бази для кожного паралельного процесу, що виконує ваші тести. До імен тестових баз додаватиметься токен процесу, унікальний для кожного з них. Наприклад, якщо у вас два паралельні тестові процеси, Laravel створить і використовуватиме тестові бази `your_db_test_1` та `your_db_test_2`.

За замовчуванням тестові бази зберігаються між викликами артизан-команди `test`, щоб їх можна було використати повторно. Проте ви можете створити їх наново опцією `--recreate-databases`:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### Хуки паралельного тестування

Іноді вам може знадобитися підготувати певні ресурси, які використовують тести вашого застосунку, щоб кілька тестових процесів могли безпечно з ними працювати.

Через фасад `ParallelTesting` ви можете вказати код, який виконуватиметься на `setUp` і `tearDown` процесу чи тест-кейса. Передані замикання отримують змінні `$token` і `$testCase`, що містять токен процесу та поточний тест-кейс відповідно:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function (int $token) {
            // ...
        });
    }
}
```

<a name="accessing-the-parallel-testing-token"></a>
#### Доступ до токена паралельного тестування

Якщо ви хочете дістатися «токена» поточного паралельного процесу з будь-якого іншого місця тестового коду вашого застосунку, скористайтеся методом `token`. Цей токен - унікальний рядковий ідентифікатор окремого тестового процесу, який можна використати, щоб розділити ресурси між паралельними процесами. Наприклад, Laravel автоматично додає цей токен у кінець імен тестових баз, створених кожним паралельним процесом:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### Звіт про покриття тестами

> [!WARNING]
> Ця можливість потребує [Xdebug](https://xdebug.org) або [PCOV](https://pecl.php.net/package/pcov).

Запускаючи тести застосунку, ви можете захотіти дізнатися, чи справді ваші тест-кейси покривають код застосунку і яка його частина задіяна під час прогону. Для цього додайте опцію `--coverage` до команди `test`:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### Установлення мінімального порога покриття

Опція `--min` дозволяє задати мінімальний поріг покриття тестами для вашого застосунку. Якщо цього порога не досягнуто, набір тестів завершиться з помилкою:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### Профілювання тестів

Артизан-раннер тестів має також зручний механізм для показу найповільніших тестів вашого застосунку. Викличте команду `test` з опцією `--profile`, щоб побачити десятку найповільніших тестів і легко з'ясувати, що саме можна поліпшити, аби пришвидшити набір тестів:

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## Кешування конфігурації

Під час запуску тестів Laravel завантажує застосунок для кожного окремого тестового методу. Без кешованого файлу конфігурації кожен конфігураційний файл вашого застосунку доводиться завантажувати на початку кожного тесту. Щоб зібрати конфігурацію один раз і перевикористати її для всіх тестів у межах одного прогону, скористайтеся трейтом `Illuminate\Foundation\Testing\WithCachedConfig`:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}
```
