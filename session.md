---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# HTTP-сесія

- [Вступ](#introduction)
    - [Конфігурація](#configuration)
    - [Передумови драйверів](#driver-prerequisites)
- [Робота із сесією](#interacting-with-the-session)
    - [Отримання даних](#retrieving-data)
    - [Збереження даних](#storing-data)
    - [Флеш-дані](#flash-data)
    - [Видалення даних](#deleting-data)
    - [Регенерація ідентифікатора сесії](#regenerating-the-session-id)
- [Кеш сесії](#session-cache)
- [Блокування сесії](#session-blocking)
- [Додавання власних драйверів сесії](#adding-custom-session-drivers)
    - [Реалізація драйвера](#implementing-the-driver)
    - [Реєстрація драйвера](#registering-the-driver)

<a name="introduction"></a>
## Вступ

Оскільки застосунки на основі HTTP є безстановими, сесії дають спосіб зберігати інформацію про користувача між кількома запитами. Зазвичай ця інформація розміщується в постійному сховищі, доступному з наступних запитів.

Laravel постачається з різноманітними бекендами сесій, доступними через виразний уніфікований API. Підтримку популярних бекендів, як-от [Memcached](https://memcached.org), [Redis](https://redis.io) і баз даних, уже вбудовано.

<a name="configuration"></a>
### Конфігурація

Конфігураційний файл сесій вашого застосунку зберігається за шляхом `config/session.php`. Обов'язково перегляньте доступні в ньому опції. За замовчуванням Laravel налаштовано на драйвер сесій `database`.

Опція конфігурації `driver` визначає, де зберігатимуться дані сесії для кожного запиту. Laravel містить кілька драйверів:

<div class="content-list" markdown="1">

- `file` - сесії зберігаються в `storage/framework/sessions`.
- `cookie` - сесії зберігаються в захищених зашифрованих cookie.
- `database` - сесії зберігаються в реляційній базі даних.
- `memcached` / `redis` - сесії зберігаються в одному з цих швидких сховищ на основі кешу.
- `dynamodb` - сесії зберігаються в AWS DynamoDB.
- `array` - сесії зберігаються в PHP-масиві і не є постійними.

</div>

> [!NOTE]
> Драйвер array використовується насамперед під час [тестування](/docs/{{version}}/testing) і не дає даним сесії зберігатися постійно.

<a name="driver-prerequisites"></a>
### Передумови драйверів

<a name="database"></a>
#### База даних

Використовуючи драйвер сесій `database`, вам потрібно переконатися, що у вас є таблиця бази даних для зберігання даних сесії. Зазвичай її створює типова [міграція](/docs/{{version}}/migrations) Laravel `0001_01_01_000000_create_users_table.php`; однак якщо з якоїсь причини таблиці `sessions` у вас немає, ви можете згенерувати цю міграцію командою Artisan `make:session-table`:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Перш ніж використовувати сесії Redis із Laravel, вам потрібно встановити PHP-розширення PhpRedis через PECL або пакет `predis/predis` через Composer. Докладніше про налаштування Redis дивіться в [документації Laravel щодо Redis](/docs/{{version}}/redis#configuration).

> [!NOTE]
> Змінна середовища `SESSION_CONNECTION` або опція `connection` у конфігураційному файлі `session.php` дозволяють вказати, яке підключення Redis використовується для зберігання сесій.

<a name="interacting-with-the-session"></a>
## Робота із сесією

<a name="retrieving-data"></a>
### Отримання даних

Є два основні способи роботи з даними сесії в Laravel: глобальний хелпер `session` і екземпляр `Request`. Спершу розгляньмо доступ до сесії через екземпляр `Request`, тип якого можна вказати в замиканні маршруту чи методі контролера. Пам'ятайте: залежності методів контролера автоматично впроваджуються через [сервіс-контейнер](/docs/{{version}}/container) Laravel:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(Request $request, string $id): View
    {
        $value = $request->session()->get('key');

        // ...

        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

Отримуючи елемент із сесії, ви також можете передати значення за замовчуванням другим аргументом методу `get`. Воно повернеться, якщо вказаного ключа в сесії немає. Якщо ви передасте методу `get` замикання як значення за замовчуванням і запитаного ключа не існує, замикання буде виконано, а його результат повернуто:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### Глобальний хелпер session

Ви також можете скористатися глобальною PHP-функцією `session`, щоб отримувати та зберігати дані в сесії. Коли хелпер `session` викликається з одним рядковим аргументом, він повертає значення відповідного ключа сесії. Коли ж його викликають із масивом пар «ключ - значення», ці значення зберігаються в сесії:

```php
Route::get('/home', function () {
    // Retrieve a piece of data from the session...
    $value = session('key');

    // Specifying a default value...
    $value = session('key', 'default');

    // Store a piece of data in the session...
    session(['key' => 'value']);
});
```

> [!NOTE]
> Практичної різниці між використанням сесії через екземпляр HTTP-запиту та через глобальний хелпер `session` майже немає. Обидва підходи можна [тестувати](/docs/{{version}}/testing) методом `assertSessionHas`, доступним у всіх ваших тестах.

<a name="retrieving-all-session-data"></a>
#### Отримання всіх даних сесії

Якщо ви хочете отримати всі дані сесії, скористайтеся методом `all`:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### Отримання частини даних сесії

Методи `only` та `except` дозволяють отримати підмножину даних сесії:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### Визначення наявності елемента в сесії

Щоб визначити, чи присутній елемент у сесії, скористайтеся методом `has`. Він повертає `true`, якщо елемент присутній і не дорівнює `null`:

```php
if ($request->session()->has('users')) {
    // ...
}
```

Щоб визначити, чи присутній елемент у сесії, навіть якщо його значення `null`, скористайтеся методом `exists`:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

Щоб визначити, що елемента в сесії немає, скористайтеся методом `missing`. Він повертає `true`, якщо елемент відсутній:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### Збереження даних

Щоб зберегти дані в сесії, ви зазвичай використовуватимете метод `put` екземпляра запиту або глобальний хелпер `session`:

```php
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### Додавання до значень-масивів у сесії

Метод `push` дозволяє додати нове значення до значення сесії, що є масивом. Наприклад, якщо ключ `user.teams` містить масив назв команд, ви можете додати до нього нове значення так:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### Отримання та видалення елемента

Метод `pull` отримає й видалить елемент із сесії однією інструкцією:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### Збільшення та зменшення значень сесії

Якщо дані вашої сесії містять ціле число, яке ви хочете збільшити чи зменшити, скористайтеся методами `increment` і `decrement`:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### Флеш-дані

Іноді вам може знадобитися зберегти елементи в сесії лише для наступного запиту. Це робиться методом `flash`. Дані, збережені в сесії цим методом, будуть доступні одразу й протягом наступного HTTP-запиту. Після нього флеш-дані буде видалено. Флеш-дані насамперед корисні для короткочасних повідомлень про стан:

```php
$request->session()->flash('status', 'Task was successful!');
```

Якщо вам потрібно зберегти флеш-дані на кілька запитів, скористайтеся методом `reflash`, який залишить усі флеш-дані ще на один запит. Якщо ж потрібно зберегти лише певні дані, скористайтеся методом `keep`:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

Щоб зберегти флеш-дані лише для поточного запиту, скористайтеся методом `now`:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### Видалення даних

Метод `forget` вилучить фрагмент даних із сесії. Якщо ви хочете вилучити всі дані, скористайтеся методом `flush`:

```php
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### Регенерація ідентифікатора сесії

Регенерацію ідентифікатора сесії часто виконують, щоб завадити зловмисникам скористатися атакою [фіксації сесії](https://owasp.org/www-community/attacks/Session_fixation) на ваш застосунок.

Laravel автоматично регенерує ідентифікатор сесії під час автентифікації, якщо ви використовуєте один зі [стартових наборів](/docs/{{version}}/starter-kits) чи [Laravel Fortify](/docs/{{version}}/fortify); однак якщо вам потрібно зробити це вручну, скористайтеся методом `regenerate`:

```php
$request->session()->regenerate();
```

Якщо вам потрібно регенерувати ідентифікатор сесії й вилучити всі дані однією інструкцією, скористайтеся методом `invalidate`:

```php
$request->session()->invalidate();
```

<a name="session-cache"></a>
## Кеш сесії

Кеш сесії Laravel дає зручний спосіб кешувати дані в межах окремої сесії користувача. На відміну від глобального кешу застосунку, дані кешу сесії автоматично ізольовані для кожної сесії й очищаються, коли сесія спливає або знищується. Кеш сесії підтримує всі звичні [методи кешу Laravel](/docs/{{version}}/cache) - `get`, `put`, `remember`, `forget` тощо, - але в межах поточної сесії.

Кеш сесії чудово підходить для зберігання тимчасових даних, специфічних для користувача, які ви хочете зберегти між кількома запитами в межах однієї сесії, але не потребуєте зберігати назавжди. Це можуть бути дані форм, тимчасові обчислення, відповіді API чи будь-які інші ефемерні дані, прив'язані до сесії конкретного користувача.

Доступ до кешу сесії можна отримати методом `cache` на сесії:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);
```

Докладніше про методи кешу Laravel дивіться в [документації з кешу](/docs/{{version}}/cache).

<a name="session-blocking"></a>
## Блокування сесії

> [!WARNING]
> Щоб скористатися блокуванням сесії, ваш застосунок має використовувати драйвер кешу з підтримкою [атомарних блокувань](/docs/{{version}}/cache#atomic-locks). Наразі це драйвери `memcached`, `dynamodb`, `redis`, `mongodb` (входить до офіційного пакета `mongodb/laravel-mongodb`), `database`, `file` та `array`. Крім того, ви не можете використовувати драйвер сесій `cookie`.

За замовчуванням Laravel дозволяє запитам однієї сесії виконуватися паралельно. Тож, наприклад, якщо ви використовуєте JavaScript-бібліотеку HTTP, щоб зробити два запити до вашого застосунку, вони виконуватимуться одночасно. Для багатьох застосунків це не проблема; однак втрата даних сесії може статися в невеликій частині застосунків, які роблять паралельні запити до двох різних точок, що обидві пишуть у сесію.

Щоб цьому запобігти, Laravel надає можливість обмежити паралельні запити для певної сесії. Щоб почати, просто додайте метод `block` до визначення маршруту. У цьому прикладі вхідний запит до точки `/profile` отримає блокування сесії. Поки воно триває, будь-які вхідні запити до `/profile` чи `/order` із тим самим ідентифікатором сесії чекатимуть завершення першого запиту, перш ніж продовжити виконання:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

Метод `block` приймає два необов'язкові аргументи. Перший - максимальна кількість секунд, протягом яких блокування сесії має утримуватися перед звільненням. Звісно, якщо запит завершиться раніше, блокування буде знято раніше.

Другий аргумент - кількість секунд, які запит має чекати, намагаючись отримати блокування сесії. Якщо запит не зможе отримати блокування за вказану кількість секунд, буде викинуто `Illuminate\Contracts\Cache\LockTimeoutException`.

Якщо не передати жодного з цих аргументів, блокування отримають максимум на 10 секунд, і запити чекатимуть на нього максимум 10 секунд:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## Додавання власних драйверів сесії

<a name="implementing-the-driver"></a>
### Реалізація драйвера

Якщо жоден із наявних драйверів сесій не відповідає потребам вашого застосунку, Laravel дозволяє написати власний обробник сесій. Ваш драйвер має реалізувати вбудований у PHP інтерфейс `SessionHandlerInterface`, що містить лише кілька простих методів. Заготовка реалізації для MongoDB виглядає так:

```php
<?php

namespace App\Extensions;

class MongoSessionHandler implements \SessionHandlerInterface
{
    public function open($savePath, $sessionName) {}
    public function close() {}
    public function read($sessionId) {}
    public function write($sessionId, $data) {}
    public function destroy($sessionId) {}
    public function gc($lifetime) {}
}
```

Оскільки Laravel не має типового каталогу для ваших розширень, ви вільні розміщувати їх де завгодно. У цьому прикладі ми створили каталог `Extensions` для `MongoSessionHandler`.

Оскільки призначення цих методів не є очевидним, ось огляд кожного з них:

<div class="content-list" markdown="1">

- Метод `open` зазвичай використовується у файлових системах зберігання сесій. Оскільки Laravel постачається з драйвером сесій `file`, вам рідко доведеться щось у нього додавати. Ви можете просто залишити його порожнім.
- Метод `close`, як і `open`, зазвичай теж можна не враховувати. Для більшості драйверів він не потрібен.
- Метод `read` має повертати рядкову версію даних сесії, пов'язаних із переданим `$sessionId`. Виконувати серіалізацію чи інше кодування під час отримання чи збереження даних сесії у вашому драйвері не потрібно - Laravel зробить це за вас.
- Метод `write` має записати переданий рядок `$data`, пов'язаний із `$sessionId`, до якогось постійного сховища - MongoDB чи іншого на ваш вибір. Знову ж таки, серіалізацію виконувати не потрібно: Laravel уже подбав про це.
- Метод `destroy` має вилучити з постійного сховища дані, пов'язані з `$sessionId`.
- Метод `gc` має знищити всі дані сесій, старші за переданий `$lifetime`, що є міткою часу UNIX. Для систем із самостійним спливанням, як-от Memcached і Redis, цей метод можна лишити порожнім.

</div>

<a name="registering-the-driver"></a>
### Реєстрація драйвера

Щойно ваш драйвер реалізовано, ви готові зареєструвати його в Laravel. Щоб додати драйвери до бекенду сесій Laravel, скористайтеся методом `extend` [фасаду](/docs/{{version}}/facades) `Session`. Викликати `extend` слід із методу `boot` [сервіс-провайдера](/docs/{{version}}/providers). Ви можете зробити це з наявного `App\Providers\AppServiceProvider` або створити цілком новий провайдер:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
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
        Session::extend('mongo', function (Application $app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}
```

Щойно драйвер сесій зареєстровано, ви можете вказати драйвер `mongo` як драйвер сесій вашого застосунку через змінну середовища `SESSION_DRIVER` або в конфігураційному файлі `config/session.php`.
