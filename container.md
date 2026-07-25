---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Сервіс-контейнер

- [Вступ](#introduction)
    - [Розв'язання без конфігурації](#zero-configuration-resolution)
    - [Коли використовувати контейнер](#when-to-use-the-container)
- [Прив'язка](#binding)
    - [Основи прив'язки](#binding-basics)
    - [Прив'язка інтерфейсів до реалізацій](#binding-interfaces-to-implementations)
    - [Контекстна прив'язка](#contextual-binding)
    - [Контекстні атрибути](#contextual-attributes)
    - [Прив'язка примітивів](#binding-primitives)
    - [Прив'язка типізованих варіативних параметрів](#binding-typed-variadics)
    - [Теги](#tagging)
    - [Розширення прив'язок](#extending-bindings)
- [Розв'язання](#resolving)
    - [Метод make](#the-make-method)
    - [Автоматичне впровадження](#automatic-injection)
- [Виклик методів і впровадження](#method-invocation-and-injection)
- [Події контейнера](#container-events)
    - [Повторна прив'язка](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## Вступ

Сервіс-контейнер Laravel - потужний інструмент для керування залежностями класів і виконання впровадження залежностей (dependency injection). Впровадження залежностей - гучна назва, що по суті означає таке: залежності класу «впроваджуються» в клас через конструктор або, подекуди, через методи-сетери.

Погляньмо на простий приклад:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

У цьому прикладі `PodcastController` має отримувати подкасти з джерела даних - наприклад, Apple Music. Тож ми **впровадимо** сервіс, здатний отримувати подкасти. Оскільки сервіс впроваджено, ми можемо легко «замокати» чи створити фіктивну реалізацію сервісу `AppleMusic` під час тестування застосунку.

Глибоке розуміння сервіс-контейнера Laravel - необхідна умова для створення потужного великого застосунку, а також для внеску в саме ядро Laravel.

<a name="zero-configuration-resolution"></a>
### Розв'язання без конфігурації

Якщо клас не має залежностей або залежить лише від інших конкретних класів (не інтерфейсів), контейнеру не потрібно пояснювати, як розв'язувати цей клас. Наприклад, ви можете розмістити такий код у файлі `routes/web.php`:

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    dd($service::class);
});
```

У цьому прикладі звернення до маршруту `/` вашого застосунку автоматично розв'яже клас `Service` і впровадить його в обробник маршруту. Це змінює правила гри: ви можете розробляти застосунок і користуватися впровадженням залежностей, не турбуючись про роздуті конфігураційні файли.

На щастя, багато класів, які ви писатимете, створюючи застосунок Laravel, автоматично отримують свої залежності через контейнер - зокрема [контролери](/docs/{{version}}/controllers), [слухачі подій](/docs/{{version}}/events), [`middleware`](/docs/{{version}}/middleware) тощо. Крім того, ви можете вказувати типи залежностей у методі `handle` [завдань у черзі](/docs/{{version}}/queues). Щойно ви відчуєте смак автоматичного впровадження залежностей без конфігурації, розробляти без нього здаватиметься неможливим.

<a name="when-to-use-the-container"></a>
### Коли використовувати контейнер

Завдяки розв'язанню без конфігурації ви часто вказуватимете типи залежностей у маршрутах, контролерах, слухачах подій та інших місцях, жодного разу не звертаючись до контейнера вручну. Наприклад, ви можете вказати тип `Illuminate\Http\Request` у визначенні маршруту, щоб мати легкий доступ до поточного запиту. Хоча для написання цього коду нам не доводиться взаємодіяти з контейнером, саме він за лаштунками керує впровадженням цих залежностей:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

У багатьох випадках завдяки автоматичному впровадженню залежностей і [фасадам](/docs/{{version}}/facades) ви можете створювати застосунки Laravel, **жодного разу** не прив'язуючи й не розв'язуючи нічого з контейнера вручну. **То коли ж вам доведеться взаємодіяти з контейнером вручну?** Розгляньмо дві ситуації.

По-перше, якщо ви пишете клас, що реалізує інтерфейс, і хочете вказати цей інтерфейс як тип у маршруті чи конструкторі класу, вам потрібно [пояснити контейнеру, як розв'язувати цей інтерфейс](#binding-interfaces-to-implementations). По-друге, якщо ви [пишете пакет Laravel](/docs/{{version}}/packages), яким плануєте поділитися з іншими розробниками, вам може знадобитися прив'язати сервіси свого пакета до контейнера.

<a name="binding"></a>
## Прив'язка

<a name="binding-basics"></a>
### Основи прив'язки

<a name="simple-bindings"></a>
#### Прості прив'язки

Майже всі прив'язки сервіс-контейнера реєструються в [сервіс-провайдерах](/docs/{{version}}/providers), тож більшість цих прикладів демонструватимуть використання контейнера саме в такому контексті.

У сервіс-провайдері вам завжди доступний контейнер через властивість `$this->app`. Зареєструвати прив'язку можна методом `bind`, передавши ім'я класу чи інтерфейсу, який ви хочете зареєструвати, разом із замиканням, що повертає екземпляр класу:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Зверніть увагу, що ми отримуємо сам контейнер як аргумент резолвера. Далі ми можемо використати контейнер, щоб розв'язати підзалежності об'єкта, який будуємо.

Як згадувалося, зазвичай ви взаємодієте з контейнером усередині сервіс-провайдерів; однак якщо вам потрібно звернутися до контейнера поза сервіс-провайдером, це можна зробити через [фасад](/docs/{{version}}/facades) `App`:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

Метод `bindIf` дозволяє зареєструвати прив'язку контейнера лише тоді, коли для цього типу її ще не зареєстровано:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Для зручності ви можете не передавати ім'я класу чи інтерфейсу окремим аргументом, а дозволити Laravel вивести тип із типу повернення замикання, яке ви передаєте методу `bind`:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> Немає потреби прив'язувати класи до контейнера, якщо вони не залежать від жодних інтерфейсів. Контейнеру не потрібно пояснювати, як будувати такі об'єкти, адже він може розв'язати їх автоматично за допомогою рефлексії.

<a name="binding-a-singleton"></a>
#### Прив'язка синглтона

Метод `singleton` прив'язує до контейнера клас чи інтерфейс, який має розв'язуватися лише один раз. Щойно прив'язку-синглтон розв'язано, на подальші звернення до контейнера повертатиметься той самий екземпляр об'єкта:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Метод `singletonIf` дозволяє зареєструвати прив'язку-синглтон лише тоді, коли для цього типу її ще не зареєстровано:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="singleton-attribute"></a>
#### Атрибут Singleton

Як альтернативу ви можете позначити інтерфейс чи клас атрибутом `#[Singleton]`, вказавши контейнеру, що його слід розв'язувати один раз:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Singleton;

#[Singleton]
class Transistor
{
    // ...
}
```

<a name="binding-scoped"></a>
#### Прив'язка scoped-синглтонів

Метод `scoped` прив'язує до контейнера клас чи інтерфейс, який має розв'язуватися лише один раз у межах певного життєвого циклу запиту чи завдання Laravel. Хоча цей метод схожий на `singleton`, екземпляри, зареєстровані через `scoped`, скидатимуться щоразу, коли застосунок Laravel починає новий «життєвий цикл» - наприклад, коли воркер [Laravel Octane](/docs/{{version}}/octane) обробляє новий запит або коли [воркер черги](/docs/{{version}}/queues) Laravel обробляє нове завдання:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Метод `scopedIf` дозволяє зареєструвати scoped-прив'язку лише тоді, коли для цього типу її ще не зареєстровано:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="scoped-attribute"></a>
#### Атрибут Scoped

Як альтернативу ви можете позначити інтерфейс чи клас атрибутом `#[Scoped]`, вказавши контейнеру, що його слід розв'язувати один раз у межах певного життєвого циклу запиту чи завдання Laravel:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Scoped;

#[Scoped]
class Transistor
{
    // ...
}
```

<a name="binding-instances"></a>
#### Прив'язка екземплярів

Ви також можете прив'язати до контейнера наявний екземпляр об'єкта методом `instance`. Переданий екземпляр завжди повертатиметься на подальші звернення до контейнера:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### Прив'язка інтерфейсів до реалізацій

Дуже потужна можливість сервіс-контейнера - здатність прив'язати інтерфейс до певної реалізації. Наприклад, припустімо, що ми маємо інтерфейс `EventPusher` і реалізацію `RedisEventPusher`. Написавши реалізацію `RedisEventPusher` цього інтерфейсу, ми можемо зареєструвати її в сервіс-контейнері так:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

Ця інструкція каже контейнеру впроваджувати `RedisEventPusher`, коли класу потрібна реалізація `EventPusher`. Тепер ми можемо вказати інтерфейс `EventPusher` як тип у конструкторі класу, який розв'язує контейнер. Пам'ятайте: контролери, слухачі подій, `middleware` та різні інші типи класів у застосунках Laravel завжди розв'язуються через контейнер:

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="bind-attribute"></a>
#### Атрибут Bind

Для більшої зручності Laravel також надає атрибут `Bind`. Ви можете застосувати його до будь-якого інтерфейсу, щоб вказати Laravel, яку реалізацію слід автоматично впроваджувати щоразу, коли цей інтерфейс запитують. Використовуючи атрибут `Bind`, вам не потрібно додатково реєструвати сервіс у сервіс-провайдерах застосунку.

Ба більше, на інтерфейс можна розмістити кілька атрибутів `Bind`, щоб налаштувати різні реалізації для різних наборів середовищ:

```php
<?php

namespace App\Contracts;

use App\Services\FakeEventPusher;
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;

#[Bind(RedisEventPusher::class)]
#[Bind(FakeEventPusher::class, environments: ['local', 'testing'])]
interface EventPusher
{
    // ...
}
```

Крім того, можна застосувати атрибути [Singleton](#singleton-attribute) і [Scoped](#scoped-attribute), щоб вказати, чи мають прив'язки контейнера розв'язуватися один раз, чи один раз на життєвий цикл запиту або завдання:

```php
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;
use Illuminate\Container\Attributes\Singleton;

#[Bind(RedisEventPusher::class)]
#[Singleton]
interface EventPusher
{
    // ...
}
```

<a name="contextual-binding"></a>
### Контекстна прив'язка

Іноді ви можете мати два класи, що використовують той самий інтерфейс, але хочете впровадити в кожен із них різні реалізації. Наприклад, два контролери можуть залежати від різних реалізацій [контракту](/docs/{{version}}/contracts) `Illuminate\Contracts\Filesystem\Filesystem`. Laravel надає простий плинний інтерфейс для визначення такої поведінки:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\UploadController;
use App\Http\Controllers\VideoController;
use Illuminate\Contracts\Filesystem\Filesystem;
use Illuminate\Support\Facades\Storage;

$this->app->when(PhotoController::class)
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('local');
    });

$this->app->when([VideoController::class, UploadController::class])
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('s3');
    });
```

<a name="contextual-attributes"></a>
### Контекстні атрибути

Оскільки контекстну прив'язку часто використовують для впровадження реалізацій драйверів чи значень конфігурації, Laravel пропонує різноманітні атрибути контекстної прив'язки, які дозволяють впроваджувати такі значення, не визначаючи контекстних прив'язок у сервіс-провайдерах вручну.

Наприклад, атрибут `Storage` дозволяє впровадити конкретний [диск сховища](/docs/{{version}}/filesystem):

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    ) {
        // ...
    }
}
```

Крім атрибута `Storage`, Laravel пропонує атрибути `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RequestAttribute`, `RouteParameter` і [Tag](#tagging):

```php
<?php

namespace App\Http\Controllers;

use App\Contracts\UserRepository;
use App\Models\Organization;
use App\Models\Photo;
use App\Repositories\DatabaseRepository;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
use Illuminate\Container\Attributes\DB;
use Illuminate\Container\Attributes\Give;
use Illuminate\Container\Attributes\Log;
use Illuminate\Container\Attributes\RequestAttribute;
use Illuminate\Container\Attributes\RouteParameter;
use Illuminate\Container\Attributes\Tag;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Database\Connection;
use Psr\Log\LoggerInterface;

class PhotoController extends Controller
{
    public function __construct(
        #[Auth('web')] protected Guard $auth,
        #[Cache('redis')] protected Repository $cache,
        #[Config('app.timezone')] protected string $timezone,
        #[Context('uuid')] protected string $uuid,
        #[Context('ulid', hidden: true)] protected string $ulid,
        #[DB('mysql')] protected Connection $connection,
        #[Give(DatabaseRepository::class)] protected UserRepository $users,
        #[Log('daily')] protected LoggerInterface $log,
        #[RequestAttribute('organization')] protected Organization $organization,
        #[RouteParameter] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

Атрибут `RouteParameter` розв'яже параметр маршруту, що відповідає імені змінної. За потреби ви можете вказати ім'я параметра явно: `#[RouteParameter('photo')]`.

Атрибут `RequestAttribute` розв'яже значення, збережене за вказаним ключем у [наборі атрибутів](https://symfony.com/doc/current/components/http_foundation.html#accessing-request-data) поточного запиту: `#[RequestAttribute('organization')]`.

Крім того, Laravel надає атрибут `CurrentUser` для впровадження поточного автентифікованого користувача в маршрут чи клас:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### Визначення власних атрибутів

Ви можете створювати власні контекстні атрибути, реалізувавши контракт `Illuminate\Contracts\Container\ContextualAttribute`. Контейнер викличе метод `resolve` вашого атрибута, який має розв'язати значення для впровадження в клас, що використовує цей атрибут. У прикладі нижче ми заново реалізуємо вбудований атрибут `Config` від Laravel:

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;
use ReflectionParameter;

#[Attribute(Attribute::TARGET_PARAMETER)]
class Config implements ContextualAttribute
{
    /**
     * Create a new attribute instance.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * Resolve the configuration value.
     *
     * @param  self  $attribute
     * @param  \Illuminate\Contracts\Container\Container  $container
     * @param  \ReflectionParameter  $parameter
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container, ReflectionParameter $parameter)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```

<a name="binding-primitives"></a>
### Прив'язка примітивів

Іноді ви можете мати клас, який отримує кілька впроваджених класів, але також потребує впровадженого примітивного значення - наприклад, цілого числа. За допомогою контекстної прив'язки ви можете легко впровадити будь-яке потрібне класу значення:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

Іноді клас може залежати від масиву [позначених тегом](#tagging) екземплярів. За допомогою методу `giveTagged` ви можете легко впровадити всі прив'язки контейнера з цим тегом:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

Якщо вам потрібно впровадити значення з одного з конфігураційних файлів застосунку, скористайтеся методом `giveConfig`:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### Прив'язка типізованих варіативних параметрів

Подекуди ви можете мати клас, що приймає масив типізованих об'єктів через варіативний аргумент конструктора:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * The filter instances.
     *
     * @var array
     */
    protected $filters;

    /**
     * Create a new class instance.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

За допомогою контекстної прив'язки ви можете розв'язати цю залежність, передавши методу `give` замикання, що повертає масив розв'язаних екземплярів `Filter`:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give(function (Application $app) {
          return [
              $app->make(NullFilter::class),
              $app->make(ProfanityFilter::class),
              $app->make(TooLongFilter::class),
          ];
    });
```

Для зручності ви можете просто передати масив імен класів, які контейнер розв'язуватиме щоразу, коли `Firewall` потребуватиме екземплярів `Filter`:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give([
        NullFilter::class,
        ProfanityFilter::class,
        TooLongFilter::class,
    ]);
```

<a name="variadic-tag-dependencies"></a>
#### Варіативні залежності з тегом

Іноді клас може мати варіативну залежність, тип якої вказано як певний клас (`Report ...$reports`). За допомогою методів `needs` і `giveTagged` ви можете легко впровадити для цієї залежності всі прив'язки контейнера з відповідним [тегом](#tagging):

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### Теги

Подекуди вам може знадобитися розв'язати всі прив'язки певної «категорії». Наприклад, ви створюєте аналізатор звітів, що приймає масив із багатьма різними реалізаціями інтерфейсу `Report`. Зареєструвавши реалізації `Report`, ви можете призначити їм тег методом `tag`:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

Щойно сервіси позначено тегом, ви можете легко розв'язати їх усі методом `tagged` контейнера:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### Розширення прив'язок

Метод `extend` дозволяє змінювати розв'язані сервіси. Наприклад, коли сервіс розв'язано, ви можете виконати додатковий код, щоб декорувати чи налаштувати його. Метод `extend` приймає два аргументи: клас сервісу, який ви розширюєте, і замикання, що має повернути змінений сервіс. Замикання отримує сервіс, який розв'язується, та екземпляр контейнера:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## Розв'язання

<a name="the-make-method"></a>
### Метод `make`

Ви можете скористатися методом `make`, щоб розв'язати екземпляр класу з контейнера. Метод `make` приймає ім'я класу чи інтерфейсу, який ви хочете розв'язати:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

Якщо деякі залежності вашого класу не можна розв'язати через контейнер, ви можете впровадити їх, передавши асоціативним масивом у метод `makeWith`. Наприклад, ми можемо вручну передати аргумент конструктора `$id`, потрібний сервісу `Transistor`:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

Метод `bound` дозволяє визначити, чи було явно прив'язано клас або інтерфейс у контейнері:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

Якщо ви перебуваєте поза сервіс-провайдером у місці коду, де немає доступу до змінної `$app`, ви можете скористатися [фасадом](/docs/{{version}}/facades) `App` або [хелпером](/docs/{{version}}/helpers#method-app) `app`, щоб розв'язати екземпляр класу з контейнера:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

Якщо ви хочете, щоб у клас, який розв'язує контейнер, було впроваджено сам екземпляр контейнера Laravel, вкажіть у конструкторі свого класу тип `Illuminate\Container\Container`:

```php
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### Автоматичне впровадження

Як альтернативу - і це важливо - ви можете вказати тип залежності в конструкторі класу, який розв'язує контейнер, зокрема [контролерів](/docs/{{version}}/controllers), [слухачів подій](/docs/{{version}}/events), [`middleware`](/docs/{{version}}/middleware) тощо. Крім того, ви можете вказувати типи залежностей у методі `handle` [завдань у черзі](/docs/{{version}}/queues). На практиці саме так контейнер і має розв'язувати більшість ваших об'єктів.

Наприклад, ви можете вказати в конструкторі контролера тип сервісу, визначеного вашим застосунком. Сервіс буде автоматично розв'язано й впроваджено в клас:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## Виклик методів і впровадження

Іноді ви можете захотіти викликати метод на екземплярі об'єкта, дозволивши контейнеру автоматично впровадити залежності цього методу. Наприклад, маючи такий клас:

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * Generate a new podcast stats report.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

Ви можете викликати метод `generate` через контейнер так:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

Метод `call` приймає будь-який PHP callable. Метод `call` контейнера можна навіть використати для виклику замикання з автоматичним впровадженням його залежностей:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## Події контейнера

Сервіс-контейнер запускає подію щоразу, коли розв'язує об'єкт. Ви можете слухати цю подію методом `resolving`:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // Called when container resolves objects of type "Transistor"...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // Called when container resolves object of any type...
});
```

Як бачите, об'єкт, що розв'язується, передається до колбека, дозволяючи вам задати будь-які додаткові властивості перед тим, як його буде передано споживачеві.

<a name="rebinding"></a>
### Повторна прив'язка

Метод `rebinding` дозволяє слухати момент, коли сервіс повторно прив'язується до контейнера, тобто реєструється знову чи перевизначається після початкової прив'язки. Це може бути корисно, коли вам потрібно оновлювати залежності чи змінювати поведінку щоразу, коли конкретну прив'язку оновлено:

```php
use App\Contracts\PodcastPublisher;
use App\Services\SpotifyPublisher;
use App\Services\TransistorPublisher;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(PodcastPublisher::class, SpotifyPublisher::class);

$this->app->rebinding(
    PodcastPublisher::class,
    function (Application $app, PodcastPublisher $newInstance) {
        //
    },
);

// New binding will trigger rebinding closure...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Сервіс-контейнер Laravel реалізує інтерфейс [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md). Тому ви можете вказати тип контейнера PSR-11, щоб отримати екземпляр контейнера Laravel:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

Якщо переданий ідентифікатор не вдається розв'язати, буде викинуто виняток. Це буде екземпляр `Psr\Container\NotFoundExceptionInterface`, якщо ідентифікатор ніколи не прив'язували. Якщо ідентифікатор було прив'язано, але розв'язати його не вдалося, буде викинуто екземпляр `Psr\Container\ContainerExceptionInterface`.
