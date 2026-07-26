---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Pennant

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Конфігурація](#configuration)
- [Визначення можливостей](#defining-features)
    - [Можливості на основі класів](#class-based-features)
- [Перевірка можливостей](#checking-features)
    - [Умовне виконання](#conditional-execution)
    - [Трейт `HasFeatures`](#the-has-features-trait)
    - [Blade-директива](#blade-directive)
    - [Middleware](#middleware)
    - [Перехоплення перевірок можливостей](#intercepting-feature-checks)
    - [Кеш у пам'яті](#in-memory-cache)
- [Скоп](#scope)
    - [Визначення скопу](#specifying-the-scope)
    - [Скоп за замовчуванням](#default-scope)
    - [Скоп, що допускає null](#nullable-scope)
    - [Ідентифікація скопу](#identifying-scope)
    - [Серіалізація скопу](#serializing-scope)
- [Багатші значення можливостей](#rich-feature-values)
- [Отримання кількох можливостей](#retrieving-multiple-features)
- [Жадібне завантаження](#eager-loading)
- [Оновлення значень](#updating-values)
    - [Масові оновлення](#bulk-updates)
    - [Очищення можливостей](#purging-features)
- [Тестування](#testing)
- [Додавання власних драйверів Pennant](#adding-custom-pennant-drivers)
    - [Реалізація драйвера](#implementing-the-driver)
    - [Реєстрація драйвера](#registering-the-driver)
    - [Визначення можливостей ззовні](#defining-features-externally)
- [Події](#events)

<a name="introduction"></a>
## Вступ

[Laravel Pennant](https://github.com/laravel/pennant) - це простий і легкий пакет для feature-прапорців, без зайвого. Feature-прапорці дозволяють упевнено викочувати нові можливості застосунку поступово, проводити A/B-тестування нових дизайнів інтерфейсу, доповнювати стратегію trunk-based development тощо.

<a name="installation"></a>
## Встановлення

Спершу встановіть Pennant у свій проєкт за допомогою менеджера пакетів Composer:

```shell
composer require laravel/pennant
```

Далі вам слід опублікувати конфігураційний файл і файли міграцій Pennant артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

Насамкінець виконайте міграції бази даних вашого застосунку. Це створить таблицю `features`, яку Pennant використовує для роботи свого драйвера `database`:

```shell
php artisan migrate
```

<a name="configuration"></a>
## Конфігурація

Після публікації ассетів Pennant його конфігураційний файл буде розташовано в `config/pennant.php`. Цей конфігураційний файл дозволяє вказати механізм зберігання за замовчуванням, який Pennant використовуватиме для зберігання обчислених значень feature-прапорців.

Pennant підтримує зберігання обчислених значень feature-прапорців у масиві в пам'яті через драйвер `array`. Або ж Pennant може зберігати обчислені значення feature-прапорців постійно в реляційній базі даних через драйвер `database` - механізм зберігання, який Pennant використовує за замовчуванням.

<a name="defining-features"></a>
## Визначення можливостей

Щоб визначити можливість, скористайтеся методом `define`, який надає фасад `Feature`. Вам потрібно буде вказати ім'я можливості, а також замикання, яке буде викликано для обчислення початкового значення можливості.

Зазвичай можливості визначаються в сервіс-провайдері за допомогою фасада `Feature`. Замикання отримає «скоп» для перевірки можливості. Найчастіше скоп - це поточний автентифікований користувач. У цьому прикладі ми визначимо можливість для поступового викочування нового API для користувачів нашого застосунку:

```php
<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Support\Lottery;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', fn (User $user) => match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        });
    }
}
```

Як бачите, для нашої можливості маємо такі правила:

- Усі члени внутрішньої команди мають користуватися новим API.
- Клієнти з високим трафіком не мають користуватися новим API.
- В інших випадках можливість має призначатися користувачам випадково з імовірністю активації 1 до 100.

Коли можливість `new-api` перевіряється для певного користувача вперше, результат замикання буде збережено драйвером сховища. Наступного разу, коли можливість перевірятиметься для того самого користувача, значення буде взято зі сховища, а замикання не викликатиметься.

Для зручності, якщо визначення можливості повертає лише лотерею, ви можете взагалі опустити замикання:

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Можливості на основі класів

Pennant також дозволяє визначати можливості на основі класів. На відміну від визначень можливостей на основі замикань, реєструвати можливість на основі класу в сервіс-провайдері не потрібно. Щоб створити можливість на основі класу, скористайтеся артизан-командою `pennant:feature`. За замовчуванням клас можливості буде розміщено в каталозі `app/Features` вашого застосунку:

```shell
php artisan pennant:feature NewApi
```

Пишучи клас можливості, вам потрібно визначити лише метод `resolve`, який буде викликано для обчислення початкового значення можливості для заданого скопу. Знову ж таки, скопом зазвичай буде поточний автентифікований користувач:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

Якщо ви хочете вручну отримати екземпляр можливості на основі класу, викличте метод `instance` на фасаді `Feature`:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> Класи можливостей створюються через [контейнер](/docs/{{version}}/container), тож за потреби ви можете впроваджувати залежності до конструктора класу можливості.

#### Зміна збереженого імені можливості

За замовчуванням Pennant зберігатиме повністю кваліфіковане ім'я класу можливості. Якщо ви хочете відв'язати збережене ім'я можливості від внутрішньої структури застосунку, додайте до класу можливості атрибут `Name`. Значення цього атрибута буде збережено замість імені класу:

```php
<?php

namespace App\Features;

use Laravel\Pennant\Attributes\Name;

#[Name('new-api')]
class NewApi
{
    // ...
}
```

<a name="checking-features"></a>
## Перевірка можливостей

Щоб визначити, чи можливість активна, скористайтеся методом `active` на фасаді `Feature`. За замовчуванням можливості перевіряються для поточного автентифікованого користувача:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active('new-api')
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

Хоча за замовчуванням можливості перевіряються для поточного автентифікованого користувача, ви легко можете перевірити можливість для іншого користувача чи [скопу](#scope). Для цього скористайтеся методом `for`, який надає фасад `Feature`:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant також пропонує кілька додаткових зручних методів, які можуть стати в пригоді, коли ви визначаєте, активна можливість чи ні:

```php
// Determine if all of the given features are active...
Feature::allAreActive(['new-api', 'site-redesign']);

// Determine if any of the given features are active...
Feature::someAreActive(['new-api', 'site-redesign']);

// Determine if a feature is inactive...
Feature::inactive('new-api');

// Determine if all of the given features are inactive...
Feature::allAreInactive(['new-api', 'site-redesign']);

// Determine if any of the given features are inactive...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Використовуючи Pennant поза HTTP-контекстом, наприклад в артизан-команді чи завданні з черги, вам зазвичай слід [явно вказувати скоп можливості](#specifying-the-scope). Як альтернативу ви можете визначити [скоп за замовчуванням](#default-scope), який враховує як автентифіковані HTTP-контексти, так і неавтентифіковані.

<a name="checking-class-based-features"></a>
#### Перевірка можливостей на основі класів

Для можливостей на основі класів під час перевірки можливості слід передавати ім'я класу:

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active(NewApi::class)
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

<a name="conditional-execution"></a>
### Умовне виконання

Метод `when` можна використати, щоб плавно виконати задане замикання, якщо можливість активна. Крім того, можна передати друге замикання, яке буде виконано, якщо можливість неактивна:

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::when(NewApi::class,
            fn () => $this->resolveNewApiResponse($request),
            fn () => $this->resolveLegacyApiResponse($request),
        );
    }

    // ...
}
```

Метод `unless` є протилежністю методу `when` і виконує перше замикання, якщо можливість неактивна:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### Трейт `HasFeatures`

Трейт `HasFeatures` з Pennant можна додати до моделі `User` вашого застосунку (чи до будь-якої іншої моделі, що має можливості), щоб отримати зручний і плавний спосіб перевіряти можливості безпосередньо з моделі:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Pennant\Concerns\HasFeatures;

class User extends Authenticatable
{
    use HasFeatures;

    // ...
}
```

Щойно трейт буде додано до вашої моделі, ви зможете легко перевіряти можливості, викликаючи метод `features`:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

Звісно, метод `features` дає доступ до багатьох інших зручних методів для роботи з можливостями:

```php
// Values...
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// State...
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// Conditional execution...
$user->features()->when('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);

$user->features()->unless('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);
```

<a name="blade-directive"></a>
### Blade-директива

Щоб перевірка можливостей у Blade була безшовною, Pennant пропонує директиви `@feature` і `@featureany`:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' is active -->
@else
    <!-- 'site-redesign' is inactive -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' or `beta` is active -->
@endfeatureany
```

<a name="middleware"></a>
### Middleware

Pennant також містить [middleware](/docs/{{version}}/middleware), який можна використати, щоб перевірити, чи має поточний автентифікований користувач доступ до можливості, ще до того, як маршрут буде викликано. Ви можете призначити цей `middleware` маршруту й указати можливості, потрібні для доступу до нього. Якщо будь-яка з указаних можливостей неактивна для поточного автентифікованого користувача, маршрут поверне HTTP-відповідь `400 Bad Request`. До статичного методу `using` можна передати кілька можливостей.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### Зміна відповіді

Якщо ви хочете змінити відповідь, яку повертає `middleware`, коли одна з перелічених можливостей неактивна, скористайтеся методом `whenInactive`, який надає `middleware` `EnsureFeaturesAreActive`. Зазвичай цей метод слід викликати в методі `boot` одного із сервіс-провайдерів вашого застосунку:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return new Response(status: 403);
        }
    );

    // ...
}
```

<a name="intercepting-feature-checks"></a>
### Перехоплення перевірок можливостей

Іноді буває корисно виконати певні перевірки в пам'яті, перш ніж діставати збережене значення можливості. Уявіть, що ви розробляєте новий API за feature-прапорцем і хочете мати змогу вимкнути новий API, не втративши жодного з обчислених значень можливості у сховищі. Якщо ви помітите баг у новому API, ви зможете легко вимкнути його для всіх, окрім членів внутрішньої команди, виправити баг, а потім знову увімкнути новий API для користувачів, які раніше мали доступ до можливості.

Досягти цього можна методом `before` у [можливості на основі класу](#class-based-features). Якщо метод `before` присутній, він завжди виконується в пам'яті перед отриманням значення зі сховища. Якщо метод поверне значення, відмінне від `null`, воно буде використане замість збереженого значення можливості на час цього запиту:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

Ви також можете скористатися цією можливістю, щоб запланувати глобальне викочування можливості, яка раніше була за feature-прапорцем:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }

        if (Carbon::parse(Config::get('features.new-api.rollout-date'))->isPast()) {
            return true;
        }
    }

    // ...
}
```

<a name="in-memory-cache"></a>
### Кеш у пам'яті

Перевіряючи можливість, Pennant створить кеш результату в пам'яті. Якщо ви використовуєте драйвер `database`, це означає, що повторна перевірка того самого feature-прапорця в межах одного запиту не спричинить додаткових запитів до бази даних. Це також гарантує, що можливість матиме однаковий результат протягом усього запиту.

Якщо вам потрібно вручну скинути кеш у пам'яті, скористайтеся методом `flushCache`, який надає фасад `Feature`:

```php
Feature::flushCache();
```

<a name="scope"></a>
## Скоп

<a name="specifying-the-scope"></a>
### Визначення скопу

Як ми вже обговорювали, можливості зазвичай перевіряються для поточного автентифікованого користувача. Однак це не завжди відповідає вашим потребам. Тому скоп, для якого ви хочете перевірити певну можливість, можна вказати методом `for` фасада `Feature`:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Звісно, скопи можливостей не обмежуються «користувачами». Уявіть, що ви створили новий досвід білінгу, який викочуєте цілим командам, а не окремим користувачам. Можливо, ви хочете, щоб найстаріші команди отримували його повільніше, ніж новіші. Ваше замикання для обчислення можливості могло б виглядати приблизно так:

```php
use App\Models\Team;
use Illuminate\Support\Carbon;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('billing-v2', function (Team $team) {
    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
        return true;
    }

    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
        return Lottery::odds(1 / 100);
    }

    return Lottery::odds(1 / 1000);
});
```

Ви помітите, що визначене нами замикання очікує не `User`, а модель `Team`. Щоб визначити, чи активна ця можливість для команди користувача, передайте команду до методу `for`, який надає фасад `Feature`:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### Скоп за замовчуванням

Ви також можете змінити скоп за замовчуванням, який Pennant використовує для перевірки можливостей. Наприклад, можливо, усі ваші можливості перевіряються для команди поточного автентифікованого користувача, а не для самого користувача. Замість того щоб щоразу під час перевірки можливості викликати `Feature::for($user->team)`, ви можете вказати команду як скоп за замовчуванням. Зазвичай це слід робити в одному із сервіс-провайдерів вашого застосунку:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

Якщо скоп не передано явно через метод `for`, перевірка можливості тепер використовуватиме команду поточного автентифікованого користувача як скоп за замовчуванням:

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Скоп, що допускає null

Якщо скоп, який ви передаєте під час перевірки можливості, дорівнює `null`, а визначення можливості не підтримує `null` через тип, що допускає null, чи через включення `null` до об'єднаного типу, Pennant автоматично поверне `false` як результат можливості.

Тож, якщо скоп, який ви передаєте до можливості, потенційно може бути `null`, і ви хочете, щоб резолвер значення можливості все ж викликався, врахуйте це у визначенні своєї можливості. Скоп `null` може виникнути, якщо ви перевіряєте можливість в артизан-команді, завданні з черги чи на неавтентифікованому маршруті. Оскільки в цих контекстах автентифікованого користувача зазвичай немає, скопом за замовчуванням буде `null`.

Якщо ви не завжди [явно вказуєте скоп можливості](#specifying-the-scope), вам слід переконатися, що тип скопу «допускає null», і обробити значення скопу `null` у логіці визначення вашої можливості:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User $user) => match (true) {// [tl! remove]
Feature::define('new-api', fn (User|null $user) => match (true) {// [tl! add]
    $user === null => true,// [tl! add]
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### Ідентифікація скопу

Вбудовані драйвери сховища `array` і `database` у Pennant знають, як правильно зберігати ідентифікатори скопу для всіх типів даних PHP, а також для Eloquent-моделей. Однак, якщо ваш застосунок використовує сторонній драйвер Pennant, той драйвер може не знати, як правильно зберегти ідентифікатор Eloquent-моделі чи інших власних типів у вашому застосунку.

З огляду на це Pennant дозволяє форматувати значення скопу для зберігання, реалізувавши контракт `FeatureScopeable` на об'єктах вашого застосунку, які використовуються як скопи Pennant.

Наприклад, уявіть, що ви використовуєте два різні драйвери можливостей в одному застосунку: вбудований драйвер `database` і сторонній драйвер «Flag Rocket». Драйвер «Flag Rocket» не знає, як правильно зберегти Eloquent-модель. Натомість йому потрібен екземпляр `FlagRocketUser`. Реалізувавши метод `toFeatureIdentifier`, визначений контрактом `FeatureScopeable`, ми можемо налаштувати придатне до зберігання значення скопу, яке передається кожному драйверу, що використовує наш застосунок:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * Cast the object to a feature scope identifier for the given driver.
     */
    public function toFeatureIdentifier(string $driver): mixed
    {
        return match($driver) {
            'database' => $this,
            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),
        };
    }
}
```

<a name="serializing-scope"></a>
### Серіалізація скопу

За замовчуванням Pennant використовуватиме повністю кваліфіковане ім'я класу, зберігаючи можливість, пов'язану з Eloquent-моделлю. Якщо ви вже використовуєте [morph-мапу Eloquent](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types), ви можете зробити так, щоб Pennant теж використовував morph-мапу і відв'язав збережену можливість від структури вашого застосунку.

Щоб досягти цього, після визначення morph-мапи Eloquent у сервіс-провайдері викличте метод `useMorphMap` фасада `Feature`:

```php
use Illuminate\Database\Eloquent\Relations\Relation;
use Laravel\Pennant\Feature;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);

Feature::useMorphMap();
```

<a name="rich-feature-values"></a>
## Багатші значення можливостей

Досі ми переважно показували можливості в бінарному стані, тобто вони або «активні», або «неактивні», але Pennant також дозволяє зберігати багатші значення.

Наприклад, уявіть, що ви тестуєте три нові кольори для кнопки «Buy now» у своєму застосунку. Замість того щоб повертати з визначення можливості `true` чи `false`, ви можете повернути рядок:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

Отримати значення можливості `purchase-button` можна методом `value`:

```php
$color = Feature::value('purchase-button');
```

Blade-директива, що входить до Pennant, також дозволяє легко умовно рендерити вміст залежно від поточного значення можливості:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' is active -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' is active -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' is active -->
@endfeature
```

> [!NOTE]
> Використовуючи багатші значення, важливо знати, що можливість вважається «активною», коли вона має будь-яке значення, відмінне від `false`.

Під час виклику [умовного методу `when`](#conditional-execution) багатше значення можливості буде передано до першого замикання:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

Так само, під час виклику умовного методу `unless` багатше значення можливості буде передано до необов'язкового другого замикання:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## Отримання кількох можливостей

Метод `values` дозволяє отримати кілька можливостей для заданого скопу:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

Або ж ви можете скористатися методом `all`, щоб отримати значення всіх визначених можливостей для заданого скопу:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

Однак можливості на основі класів реєструються динамічно і невідомі Pennant, доки їх явно не перевірять. Це означає, що можливості на основі класів вашого застосунку можуть не з'явитися в результатах методу `all`, якщо їх ще не перевіряли протягом поточного запиту.

Якщо ви хочете, щоб класи можливостей завжди потрапляли до результатів методу `all`, скористайтеся можливостями виявлення в Pennant. Для початку викличте метод `discover` в одному із сервіс-провайдерів вашого застосунку:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

Метод `discover` зареєструє всі класи можливостей у каталозі `app/Features` вашого застосунку. Тепер метод `all` включатиме ці класи до своїх результатів незалежно від того, чи перевірялися вони протягом поточного запиту:

```php
Feature::all();

// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<a name="eager-loading"></a>
## Жадібне завантаження

Хоча Pennant тримає в пам'яті кеш усіх обчислених можливостей для одного запиту, проблеми з продуктивністю все одно можливі. Щоб полегшити це, Pennant дає змогу жадібно завантажувати значення можливостей.

Щоб проілюструвати це, уявіть, що ми перевіряємо, чи активна можливість, у циклі:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

Якщо припустити, що ми використовуємо драйвер database, цей код виконає запит до бази даних для кожного користувача в циклі - потенційно сотні запитів. Однак за допомогою методу `load` у Pennant ми можемо усунути це потенційне вузьке місце продуктивності, жадібно завантаживши значення можливостей для колекції користувачів чи скопів:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

Щоб завантажити значення можливостей лише тоді, коли їх ще не завантажено, скористайтеся методом `loadMissing`:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

Завантажити всі визначені можливості можна методом `loadAll`:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## Оновлення значень

Коли значення можливості обчислюється вперше, драйвер, що лежить в основі, збереже результат у сховищі. Часто це потрібно, щоб забезпечити узгоджений досвід для ваших користувачів між запитами. Однак іноді ви можете захотіти вручну оновити збережене значення можливості.

Для цього скористайтеся методами `activate` і `deactivate`, щоб перемкнути можливість «увімкнено» чи «вимкнено»:

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```

Також можна вручну встановити багатше значення для можливості, передавши другий аргумент до методу `activate`:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

Щоб указати Pennant забути збережене значення можливості, скористайтеся методом `forget`. Коли можливість буде перевірено знову, Pennant обчислить її значення з визначення можливості:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### Масові оновлення

Щоб оновити збережені значення можливостей масово, скористайтеся методами `activateForEveryone` і `deactivateForEveryone`.

Наприклад, уявіть, що ви тепер упевнені в стабільності можливості `new-api` і визначилися з найкращим кольором `'purchase-button'` для свого процесу оформлення замовлення - ви можете відповідно оновити збережене значення для всіх користувачів:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

Як альтернативу ви можете вимкнути можливість для всіх користувачів:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> Це оновить лише обчислені значення можливостей, збережені драйвером сховища Pennant. Вам також потрібно буде оновити визначення можливості у своєму застосунку.

<a name="purging-features"></a>
### Очищення можливостей

Іноді буває корисно повністю прибрати можливість зі сховища. Зазвичай це потрібно, якщо ви прибрали можливість зі свого застосунку або внесли у визначення можливості зміни, які хочете викотити для всіх користувачів.

Прибрати всі збережені значення можливості можна методом `purge`:

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```

Якщо ви хочете прибрати зі сховища _всі_ можливості, викличте метод `purge` без аргументів:

```php
Feature::purge();
```

Оскільки очищення можливостей може бути корисним як частина вашого конвеєра розгортання, Pennant містить артизан-команду `pennant:purge`, яка прибере зі сховища вказані можливості:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

Також можна прибрати всі можливості, _окрім_ тих, що є в заданому списку. Наприклад, уявіть, що ви хотіли прибрати всі можливості, але залишити у сховищі значення можливостей «new-api» і «purchase-button». Щоб зробити це, передайте ці імена можливостей до опції `--except`:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

Для зручності команда `pennant:purge` також підтримує прапорець `--except-registered`. Цей прапорець означає, що слід прибрати всі можливості, окрім тих, що явно зареєстровані в сервіс-провайдері:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## Тестування

Тестуючи код, який взаємодіє з feature-прапорцями, найпростіший спосіб керувати значенням, яке повертає feature-прапорець у ваших тестах, - просто перевизначити можливість. Наприклад, уявіть, що у вас в одному із сервіс-провайдерів застосунку визначено таку можливість:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

Щоб змінити значення, яке повертає можливість, у ваших тестах, перевизначте можливість на початку тесту. Наведений нижче тест завжди проходитиме, навіть попри те, що реалізація `Arr::random()` усе ще присутня в сервіс-провайдері:

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define('purchase-button', 'seafoam-green');

    expect(Feature::value('purchase-button'))->toBe('seafoam-green');
});
```

```php tab=PHPUnit
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```

Той самий підхід можна застосувати до можливостей на основі класів:

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define(NewApi::class, true);

    expect(Feature::value(NewApi::class))->toBeTrue();
});
```

```php tab=PHPUnit
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```

Якщо ваша можливість повертає екземпляр `Lottery`, є кілька корисних [хелперів для тестування](/docs/{{version}}/helpers#testing-lotteries).

<a name="store-configuration"></a>
#### Конфігурація сховища

Ви можете налаштувати сховище, яке Pennant використовуватиме під час тестування, визначивши змінну оточення `PENNANT_STORE` у файлі `phpunit.xml` вашого застосунку:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit colors="true">
    <!-- ... -->
    <php>
        <env name="PENNANT_STORE" value="array"/>
        <!-- ... -->
    </php>
</phpunit>
```

<a name="adding-custom-pennant-drivers"></a>
## Додавання власних драйверів Pennant

<a name="implementing-the-driver"></a>
#### Реалізація драйвера

Якщо жоден з наявних драйверів сховища Pennant не задовольняє потреби вашого застосунку, ви можете написати власний драйвер сховища. Ваш власний драйвер має реалізовувати інтерфейс `Laravel\Pennant\Contracts\Driver`:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;

class RedisFeatureDriver implements Driver
{
    public function define(string $feature, callable $resolver): void {}
    public function defined(): array {}
    public function getAll(array $features): array {}
    public function get(string $feature, mixed $scope): mixed {}
    public function set(string $feature, mixed $scope, mixed $value): void {}
    public function setForAllScopes(string $feature, mixed $value): void {}
    public function delete(string $feature, mixed $scope): void {}
    public function purge(array|null $features): void {}
}
```

Тепер нам залишається лише реалізувати кожен із цих методів через підключення Redis. Приклад того, як реалізувати кожен із цих методів, дивіться в `Laravel\Pennant\Drivers\DatabaseDriver` у [вихідному коді Pennant](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)

> [!NOTE]
> Laravel не постачається з каталогом для ваших розширень. Ви можете розміщувати їх де завгодно. У цьому прикладі ми створили каталог `Extensions`, щоб розмістити в ньому `RedisFeatureDriver`.

<a name="registering-the-driver"></a>
#### Реєстрація драйвера

Щойно ваш драйвер буде реалізовано, можна зареєструвати його в Laravel. Щоб додати до Pennant додаткові драйвери, скористайтеся методом `extend`, який надає фасад `Feature`. Викликати метод `extend` слід у методі `boot` одного із [сервіс-провайдерів](/docs/{{version}}/providers) вашого застосунку:

```php
<?php

namespace App\Providers;

use App\Extensions\RedisFeatureDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

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
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

Щойно драйвер буде зареєстровано, ви можете використовувати драйвер `redis` у конфігураційному файлі `config/pennant.php` вашого застосунку:

```php
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```

<a name="defining-features-externally"></a>
### Визначення можливостей ззовні

Якщо ваш драйвер є обгорткою навколо сторонньої платформи feature-прапорців, ви, найімовірніше, визначатимете можливості на самій платформі, а не методом `Feature::define` у Pennant. У такому разі ваш власний драйвер має також реалізовувати інтерфейс `Laravel\Pennant\Contracts\DefinesFeaturesExternally`:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * Get the features defined for the given scope.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

Метод `definedFeaturesForScope` має повертати список імен можливостей, визначених для наданого скопу.

<a name="events"></a>
## Події

Pennant диспетчеризує різноманітні події, які можуть стати в пригоді для відстеження feature-прапорців у вашому застосунку.

### `Laravel\Pennant\Events\FeatureRetrieved`

Ця подія диспетчеризується щоразу, коли [перевіряється можливість](#checking-features). Вона може бути корисною для створення й відстеження метрик використання feature-прапорця у вашому застосунку.

### `Laravel\Pennant\Events\FeatureResolved`

Ця подія диспетчеризується, коли значення можливості обчислюється для конкретного скопу вперше.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

Ця подія диспетчеризується, коли невідома можливість обчислюється для конкретного скопу вперше. Слухати цю подію може бути корисно, якщо ви мали намір прибрати feature-прапорець, але випадково залишили розкидані посилання на нього у своєму застосунку:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnknownFeatureResolved;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::listen(function (UnknownFeatureResolved $event) {
            Log::error("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```

### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

Ця подія диспетчеризується, коли [можливість на основі класу](#class-based-features) динамічно перевіряється вперше протягом запиту.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

Ця подія диспетчеризується, коли скоп `null` передається до визначення можливості, яке [не підтримує null](#nullable-scope).

Ця ситуація обробляється коректно, і можливість поверне `false`. Однак, якщо ви хочете відмовитися від цієї коректної поведінки за замовчуванням, зареєструйте слухача для цієї події в методі `boot` `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

Ця подія диспетчеризується під час оновлення можливості для скопу, зазвичай через виклик `activate` чи `deactivate`.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

Ця подія диспетчеризується під час оновлення можливості для всіх скопів, зазвичай через виклик `activateForEveryone` чи `deactivateForEveryone`.

### `Laravel\Pennant\Events\FeatureDeleted`

Ця подія диспетчеризується під час видалення можливості для скопу, зазвичай через виклик `forget`.

### `Laravel\Pennant\Events\FeaturesPurged`

Ця подія диспетчеризується під час очищення конкретних можливостей.

### `Laravel\Pennant\Events\AllFeaturesPurged`

Ця подія диспетчеризується під час очищення всіх можливостей.
