---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Події

- [Вступ](#introduction)
- [Генерація подій і слухачів](#generating-events-and-listeners)
- [Реєстрація подій і слухачів](#registering-events-and-listeners)
    - [Виявлення подій](#event-discovery)
    - [Реєстрація подій вручну](#manually-registering-events)
    - [Слухачі на замиканнях](#closure-listeners)
- [Опис подій](#defining-events)
- [Опис слухачів](#defining-listeners)
- [Слухачі подій у черзі](#queued-event-listeners)
    - [Ручна взаємодія з чергою](#manually-interacting-with-the-queue)
    - [Слухачі в черзі та транзакції бази даних](#queued-event-listeners-and-database-transactions)
    - [Middleware слухачів у черзі](#queued-listener-middleware)
    - [Зашифровані слухачі в черзі](#encrypted-queued-listeners)
    - [Унікальні слухачі подій](#unique-event-listeners)
        - [Тримати слухачів унікальними до початку обробки](#keeping-listeners-unique-until-processing-begins)
        - [Блокування унікальних слухачів](#unique-listener-locks)
    - [Обробка невдалих завдань](#handling-failed-jobs)
- [Диспетчеризація подій](#dispatching-events)
    - [Диспетчеризація подій після транзакцій бази даних](#dispatching-events-after-database-transactions)
    - [Відкладення подій](#deferring-events)
- [Підписники подій](#event-subscribers)
    - [Написання підписників подій](#writing-event-subscribers)
    - [Реєстрація підписників подій](#registering-event-subscribers)
- [Тестування](#testing)
    - [Підміна частини подій](#faking-a-subset-of-events)
    - [Обмежені підміни подій](#scoped-event-fakes)

<a name="introduction"></a>
## Вступ

Події Laravel надають просту реалізацію патерну «спостерігач», яка дозволяє підписуватися на різні події вашого застосунку й слухати їх. Класи подій зазвичай зберігаються в каталозі `app/Events`, а їхні слухачі - в `app/Listeners`. Не переймайтеся, якщо цих каталогів у вашому застосунку немає: їх буде створено, коли ви генеруватимете події та слухачів консольними командами Artisan.

Події - чудовий спосіб розчепити різні частини застосунку, адже одна подія може мати кілька слухачів, які не залежать одне від одного. Наприклад, ви можете хотіти надсилати користувачеві сповіщення у Slack щоразу, коли замовлення відправлено. Замість зчіплювати код обробки замовлень із кодом сповіщень у Slack, ви можете підняти подію `App\Events\OrderShipped`, яку отримає слухач і надішле сповіщення у Slack.

<a name="generating-events-and-listeners"></a>
## Генерація подій і слухачів

Щоб швидко згенерувати події та слухачів, скористайтеся командами Artisan `make:event` і `make:listener`:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

Для зручності ви можете викликати команди Artisan `make:event` і `make:listener` і без додаткових аргументів. Тоді Laravel сам запитає назву класу, а для слухача - подію, яку той має слухати:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## Реєстрація подій і слухачів

<a name="event-discovery"></a>
### Виявлення подій

За замовчуванням Laravel автоматично знаходить і реєструє ваших слухачів подій, скануючи каталог `Listeners` вашого застосунку. Коли Laravel знаходить у класі слухача метод, назва якого починається з `handle` або `__invoke`, він реєструє ці методи як слухачів події, тип якої вказано в сигнатурі методу:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

Ви можете слухати кілька подій за допомогою об'єднаних типів PHP:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

Якщо ви плануєте зберігати слухачів в іншому каталозі чи в кількох каталогах, вкажіть Laravel сканувати ці каталоги методом `withEvents` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

Ви можете шукати слухачів у кількох схожих каталогах, скориставшись символом `*` як підстановкою:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

Команда `event:list` дозволяє переглянути всіх слухачів, зареєстрованих у вашому застосунку:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### Виявлення подій у продакшені

Щоб пришвидшити застосунок, вам варто закешувати маніфест усіх слухачів командами Artisan `optimize` або `event:cache`. Зазвичай цю команду виконують у межах [процесу розгортання](/docs/{{version}}/deployment#optimization) вашого застосунку. Фреймворк використовуватиме цей маніфест, щоб пришвидшити реєстрацію подій. Команда `event:clear` дозволяє знищити кеш подій.

<a name="dynamic-event-discovery"></a>
#### Динамічне виявлення подій

Щоб динамічно керувати тим, чи буде виявлено конкретного слухача, реалізуйте в класі слухача інтерфейс `ShouldBeDiscovered` і опишіть метод `shouldBeDiscovered`, який повертає булеве значення. Якщо метод поверне `false`, слухача не буде зареєстровано під час виявлення подій:

```php
use Illuminate\Contracts\Events\ShouldBeDiscovered;

class SendPodcastNotification implements ShouldBeDiscovered
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }

    /**
     * Determine if the listener should be discovered.
     */
    public static function shouldBeDiscovered(): bool
    {
        return app()->environment('production');
    }
}
```

<a name="manually-registering-events"></a>
### Реєстрація подій вручну

За допомогою фасаду `Event` ви можете вручну реєструвати події та відповідних слухачів у методі `boot` вашого `AppServiceProvider`:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

Команда `event:list` дозволяє переглянути всіх слухачів, зареєстрованих у вашому застосунку:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### Слухачі на замиканнях

Зазвичай слухачів описують класами; проте ви можете вручну зареєструвати й слухачів подій на замиканнях у методі `boot` вашого `AppServiceProvider`:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queueable-anonymous-event-listeners"></a>
#### Анонімні слухачі подій у черзі

Реєструючи слухачів подій на замиканнях, ви можете загорнути замикання слухача у функцію `Illuminate\Events\queueable`, щоб Laravel виконував слухача через [чергу](/docs/{{version}}/queues):

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

Як і для завдань у черзі, ви можете скористатися методами `onConnection`, `onQueue` та `delay`, щоб налаштувати виконання слухача в черзі:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

Якщо ви хочете обробляти невдачі анонімних слухачів у черзі, передайте замикання методу `catch` під час опису слухача `queueable`. Це замикання отримає екземпляр події та екземпляр `Throwable`, який спричинив невдачу слухача:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="wildcard-event-listeners"></a>
#### Слухачі подій з підстановкою

Ви також можете реєструвати слухачів, використовуючи символ `*` як підстановочний параметр, - це дозволяє ловити кілька подій одним слухачем. Слухачі з підстановкою першим аргументом отримують ім'я події, а другим - увесь масив даних події:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## Опис подій

Клас події - це, по суті, контейнер даних, який містить інформацію, пов'язану з подією. Наприклад, припустімо, що подія `App\Events\OrderShipped` отримує об'єкт [Eloquent ORM](/docs/{{version}}/eloquent):

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

Як бачите, цей клас події не містить логіки. Це контейнер для екземпляра `App\Models\Order`, який було куплено. Трейт `SerializesModels`, який використовує подія, коректно серіалізує будь-які моделі Eloquent, якщо об'єкт події серіалізується PHP-функцією `serialize`, - наприклад, коли ви користуєтеся [слухачами в черзі](#queued-event-listeners).

<a name="defining-listeners"></a>
## Опис слухачів

Далі погляньмо на слухача для нашої прикладної події. Слухачі подій отримують екземпляри подій у своєму методі `handle`. Команда Artisan `make:listener`, викликана з опцією `--event`, автоматично імпортує потрібний клас події й вкаже тип події в методі `handle`. У методі `handle` ви можете виконати будь-які дії, потрібні для реакції на подію:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct() {}

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Access the order using $event->order...
    }
}
```

> [!NOTE]
> Ваші слухачі подій можуть також вказувати типи потрібних їм залежностей у конструкторах. Усі слухачі подій розв'язуються через [сервіс-контейнер](/docs/{{version}}/container) Laravel, тож залежності буде впроваджено автоматично.

<a name="stopping-the-propagation-of-an-event"></a>
#### Припинення поширення події

Інколи вам може захотітися припинити поширення події до інших слухачів. Для цього поверніть `false` з методу `handle` вашого слухача.

<a name="queued-event-listeners"></a>
## Слухачі подій у черзі

Ставити слухачів у чергу корисно, якщо слухач виконуватиме повільну задачу - наприклад, надсилатиме лист чи робитиме HTTP-запит. Перш ніж користуватися слухачами в черзі, обов'язково [налаштуйте чергу](/docs/{{version}}/queues) і запустіть воркер черги на сервері чи в локальному середовищі розробки.

Щоб вказати, що слухача слід ставити в чергу, додайте до класу слухача інтерфейс `ShouldQueue`. Слухачі, згенеровані командами Artisan `make:listener`, уже мають цей інтерфейс імпортованим у поточний простір імен, тож ви можете одразу ним скористатися:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

Ось і все! Тепер, коли диспетчеризується подія, яку обробляє цей слухач, диспетчер подій автоматично поставить слухача в чергу через [систему черг](/docs/{{version}}/queues) Laravel. Якщо під час виконання слухача чергою не викинуто винятків, завдання в черзі буде автоматично видалено після завершення обробки.

<a name="customizing-the-queue-connection-queue-name"></a>
#### Налаштування підключення, імені та затримки черги

Якщо ви хочете змінити підключення черги, ім'я черги чи час затримки для слухача подій, скористайтеся атрибутами `Connection`, `Queue` та `Delay` у класі слухача:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Delay;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('listeners')]
#[Delay(60)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```
Якщо ви хочете задати підключення черги, ім'я черги чи затримку слухача під час виконання, опишіть у слухачі методи `viaConnection`, `viaQueue` або `withDelay`:

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### Умовна постановка слухачів у чергу

Інколи вам може знадобитися визначити, чи слід ставити слухача в чергу, на основі даних, доступних лише під час виконання. Для цього до слухача можна додати метод `shouldQueue`, який визначатиме, чи ставити слухача в чергу. Якщо метод `shouldQueue` поверне `false`, слухача в чергу не поставлять:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### Ручна взаємодія з чергою

Якщо вам потрібен ручний доступ до методів `delete` і `release` завдання черги, що стоїть за слухачем, скористайтеся трейтом `Illuminate\Queue\InteractsWithQueue`. Цей трейт імпортується у згенерованих слухачах за замовчуванням і надає доступ до цих методів:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        if ($condition) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
### Слухачі в черзі та транзакції бази даних

Коли слухачі в черзі диспетчеризуються всередині транзакцій бази даних, черга може обробити їх ще до того, як транзакцію буде зафіксовано. Коли таке трапляється, будь-які зміни, які ви внесли до моделей чи записів у базі під час транзакції, ще можуть не бути в базі. Ба більше, будь-які моделі чи записи, створені всередині транзакції, можуть у базі не існувати. Якщо ваш слухач залежить від цих моделей, під час обробки завдання, яке диспетчеризує слухача в черзі, можуть виникнути несподівані помилки.

Якщо опція конфігурації `after_commit` вашого підключення черги має значення `false`, ви все одно можете вказати, що конкретного слухача в черзі слід диспетчеризувати після фіксації всіх відкритих транзакцій бази даних, - реалізуйте в класі слухача інтерфейс `ShouldQueueAfterCommit`:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueueAfterCommit
{
    use InteractsWithQueue;
}
```

> [!NOTE]
> Щоб дізнатися більше про обхід цих проблем, перегляньте документацію про [завдання в черзі та транзакції бази даних](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="queued-listener-middleware"></a>
### Middleware слухачів у черзі

Слухачі в черзі можуть також користуватися [middleware завдань](/docs/{{version}}/queues#job-middleware). Middleware завдань дозволяє огорнути виконання слухачів у черзі власною логікою, зменшивши кількість шаблонного коду в самих слухачах. Створивши middleware завдання, ви можете причепити його до слухача, повернувши з методу `middleware` слухача:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```

<a name="encrypted-queued-listeners"></a>
#### Зашифровані слухачі в черзі

Laravel дозволяє забезпечити приватність і цілісність даних слухача в черзі за допомогою [шифрування](/docs/{{version}}/encryption). Для початку просто додайте до класу слухача інтерфейс `ShouldBeEncrypted`. Щойно цей інтерфейс додано до класу, Laravel автоматично зашифрує вашого слухача перед тим, як покласти його в чергу:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="unique-event-listeners"></a>
### Унікальні слухачі подій

> [!WARNING]
> Унікальні слухачі потребують драйвера кешу, який підтримує [блокування](/docs/{{version}}/cache#atomic-locks). Наразі атомарні блокування підтримують драйвери кешу `memcached`, `redis`, `dynamodb`, `database`, `file` та `array`.

Інколи вам може знадобитися гарантувати, що в черзі одночасно перебуває лише один екземпляр конкретного слухача. Для цього реалізуйте в класі слухача інтерфейс `ShouldBeUnique`:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }
}
```

У прикладі вище слухач `AcquireProductKey` є унікальним. Тож слухача не поставлять у чергу, якщо інший його екземпляр уже в черзі й не завершив обробку. Це гарантує, що для кожної ліцензії буде отримано лише один ключ продукту, навіть якщо ліцензію збережено кілька разів поспіль.

У певних випадках вам може знадобитися задати конкретний «ключ», який робить слухача унікальним, або вказати таймаут, після якого слухач перестає бути унікальним. Для цього опишіть у класі слухача властивості або методи `uniqueId` та `uniqueFor`. Методи отримують екземпляр події, тож ви можете скористатися даними події, щоб побудувати повернене значення:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    /**
     * The number of seconds after which the listener's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }

    /**
     * Get the unique ID for the listener.
     */
    public function uniqueId(LicenseSaved $event): string
    {
        return 'listener:'.$event->license->id;
    }
}
```

У прикладі вище слухач `AcquireProductKey` унікальний за ID ліцензії. Тож будь-які нові диспетчеризації слухача для тієї самої ліцензії ігноруватимуться, доки наявний слухач не завершить обробку. Це не дає отримати дублікати ключів продукту для однієї ліцензії. Крім того, якщо наявного слухача не оброблено протягом години, унікальне блокування буде звільнено, і в чергу можна буде поставити іншого слухача з тим самим унікальним ключем.

> [!WARNING]
> Якщо ваш застосунок диспетчеризує події з кількох вебсерверів чи контейнерів, подбайте, щоб усі сервери спілкувалися з одним центральним сервером кешу, - тоді Laravel зможе точно визначити, чи є слухач унікальним.

<a name="keeping-listeners-unique-until-processing-begins"></a>
#### Тримати слухачів унікальними до початку обробки

За замовчуванням унікальні слухачі «розблоковуються» після того, як слухач завершить обробку або вичерпає всі спроби. Проте бувають ситуації, коли ви хочете, щоб слухач розблоковувався безпосередньо перед обробкою. Для цього ваш слухач має реалізувати контракт `ShouldBeUniqueUntilProcessing` замість `ShouldBeUnique`:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-listener-locks"></a>
#### Блокування унікальних слухачів

Під капотом, коли диспетчеризується слухач `ShouldBeUnique`, Laravel намагається отримати [блокування](/docs/{{version}}/cache#atomic-locks) з ключем `uniqueId`. Якщо блокування вже утримується, слухача не диспетчеризують. Це блокування звільняється, коли слухач завершує обробку або вичерпує всі спроби. За замовчуванням Laravel використовує для цього блокування драйвер кешу за замовчуванням. Проте, якщо ви хочете отримувати блокування іншим драйвером, опишіть метод `uniqueVia`, який поверне потрібний драйвер кешу:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique listener lock.
     */
    public function uniqueVia(LicenseSaved $event): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> Якщо вам потрібно лише обмежити одночасну обробку слухача, скористайтеся натомість middleware завдання [WithoutOverlapping](/docs/{{version}}/queues#preventing-job-overlaps).

<a name="handling-failed-jobs"></a>
### Обробка невдалих завдань

Інколи ваші слухачі подій у черзі можуть зазнавати невдачі. Якщо слухач у черзі перевищить максимальну кількість спроб, задану вашим воркером черги, у слухачі буде викликано метод `failed`. Метод `failed` отримує екземпляр події та `Throwable`, який спричинив невдачу:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### Задання максимальної кількості спроб для слухача в черзі

Якщо один з ваших слухачів у черзі натрапляє на помилку, ви навряд чи хочете, щоб він повторював спроби нескінченно. Тому Laravel надає різні способи вказати, скільки разів або як довго можна намагатися виконати слухача.

Ви можете скористатися атрибутом `Tries` у класі слухача, щоб вказати, скільки разів можна намагатися виконати слухача, перш ніж він вважатиметься невдалим:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(5)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    // ...
}
```

Як альтернативу заданню кількості спроб перед невдачею ви можете вказати момент, після якого спроби виконати слухача припиняються. Це дозволяє виконувати слухача будь-яку кількість разів у межах заданого проміжку часу. Щоб задати момент, після якого слухача більше не намагатимуться виконати, додайте до класу слухача метод `retryUntil`. Цей метод має повернути екземпляр `DateTimeInterface`:

```php
use DateTimeInterface;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTimeInterface
{
    return now()->plus(minutes: 5);
}
```

Якщо описано і `retryUntil`, і `tries`, Laravel віддає перевагу методу `retryUntil`.

<a name="specifying-queued-listener-backoff"></a>
#### Задання відступу для слухача в черзі

Якщо ви хочете налаштувати, скільки секунд Laravel має чекати перед повторною спробою виконати слухача, який натрапив на виняток, скористайтеся атрибутом `Backoff` у класі слухача:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

Якщо для визначення часу відступу слухача вам потрібна складніша логіка, опишіть у класі слухача метод `backoff`:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

Ви легко можете налаштувати «експоненційні» відступи, повернувши з методу `backoff` масив значень. У цьому прикладі затримка перед повтором становитиме 1 секунду для першого повтору, 5 секунд для другого, 10 секунд для третього і 10 секунд для кожного наступного, якщо спроби ще лишилися:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### Задання максимальної кількості винятків для слухача в черзі

Інколи вам може знадобитися вказати, що слухача в черзі можна намагатися виконати багато разів, але він має зазнати невдачі, якщо повтори спричинено заданою кількістю необроблених винятків (на відміну від звільнення методом `release` напряму). Для цього скористайтеся атрибутами `Tries` і `MaxExceptions` у класі слухача:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(25)]
#[MaxExceptions(3)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

У цьому прикладі слухача буде повторено до 25 разів. Проте слухач зазнає невдачі, якщо викине три необроблені винятки.

<a name="specifying-queued-listener-timeout"></a>
#### Задання таймауту для слухача в черзі

Часто ви приблизно знаєте, скільки часу мають виконуватися ваші слухачі в черзі. Тому Laravel дозволяє задати значення «таймауту». Якщо слухач обробляється довше за вказану кількість секунд, воркер, який його обробляє, завершиться з помилкою. Задати максимальну кількість секунд, яку дозволено виконуватися слухачеві, можна атрибутом `Timeout` у класі слухача:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

Якщо ви хочете, щоб слухача позначало як невдалого після таймауту, скористайтеся атрибутом `FailOnTimeout` у класі слухача:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<a name="dispatching-events"></a>
## Диспетчеризація подій

Щоб диспетчеризувати подію, викличте на ній статичний метод `dispatch`. Цей метод стає доступним у події завдяки трейту `Illuminate\Foundation\Events\Dispatchable`. Будь-які аргументи, передані методу `dispatch`, буде передано в конструктор події:

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

Якщо ви хочете диспетчеризувати подію умовно, скористайтеся методами `dispatchIf` та `dispatchUnless`:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> Під час тестування буває корисно перевірити, що певні події було диспетчеризовано, не запускаючи їхніх слухачів. [Вбудовані тестові хелпери](#testing) Laravel роблять це елементарним.

<a name="dispatching-events-after-database-transactions"></a>
### Диспетчеризація подій після транзакцій бази даних

Інколи вам може захотітися сказати Laravel диспетчеризувати подію лише після фіксації активної транзакції бази даних. Для цього реалізуйте в класі події інтерфейс `ShouldDispatchAfterCommit`.

Цей інтерфейс каже Laravel не диспетчеризувати подію, доки поточну транзакцію бази даних не зафіксовано. Якщо транзакція провалиться, подію буде відкинуто. Якщо на момент диспетчеризації події жодної транзакції не відкрито, подію буде диспетчеризовано негайно:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldDispatchAfterCommit
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="deferring-events"></a>
### Відкладення подій

Відкладені події дозволяють затримати диспетчеризацію подій моделей і виконання слухачів подій до завершення певного блоку коду. Це особливо корисно, коли вам потрібно переконатися, що всі пов'язані записи створено, перш ніж спрацюють слухачі подій.

Щоб відкласти події, передайте замикання методу `Event::defer()`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

Усі події, спричинені всередині замикання, буде диспетчеризовано після його виконання. Це гарантує, що слухачі подій матимуть доступ до всіх пов'язаних записів, створених під час відкладеного виконання. Якщо всередині замикання станеться виняток, відкладені події не буде диспетчеризовано.

Щоб відкласти лише певні події, передайте масив подій другим аргументом методу `defer`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## Підписники подій

<a name="writing-event-subscribers"></a>
### Написання підписників подій

Підписники подій - це класи, які можуть підписуватися на кілька подій зсередини самого класу підписника, дозволяючи описати кілька обробників подій в одному класі. Підписники мають описувати метод `subscribe`, який отримує екземпляр диспетчера подій. Щоб зареєструвати слухачів подій, викличте на переданому диспетчері метод `listen`:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     */
    public function subscribe(Dispatcher $events): void
    {
        $events->listen(
            Login::class,
            [UserEventSubscriber::class, 'handleUserLogin']
        );

        $events->listen(
            Logout::class,
            [UserEventSubscriber::class, 'handleUserLogout']
        );
    }
}
```

Якщо методи-слухачі подій описано в самому підписнику, вам може бути зручніше повернути з методу `subscribe` масив подій і назв методів. Реєструючи слухачів подій, Laravel автоматично визначить назву класу підписника:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     *
     * @return array<string, string>
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            Login::class => 'handleUserLogin',
            Logout::class => 'handleUserLogout',
        ];
    }
}
```

<a name="registering-event-subscribers"></a>
### Реєстрація підписників подій

Коли підписника написано, Laravel автоматично зареєструє його методи-обробники, якщо ті відповідають [домовленостям виявлення подій](#event-discovery) Laravel. Інакше ви можете зареєструвати підписника вручну методом `subscribe` фасаду `Event`. Зазвичай це роблять у методі `boot` вашого `AppServiceProvider`:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## Тестування

Тестуючи код, який диспетчеризує події, ви можете захотіти сказати Laravel не виконувати слухачів події, адже код слухача можна протестувати напряму й окремо від коду, який диспетчеризує відповідну подію. Звісно, щоб протестувати самого слухача, ви можете створити його екземпляр і викликати метод `handle` напряму у вашому тесті.

За допомогою методу `fake` фасаду `Event` ви можете завадити виконанню слухачів, виконати тестований код, а потім перевірити, які події диспетчеризував ваш застосунок, методами `assertDispatched`, `assertNotDispatched` та `assertNothingDispatched`:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
    Event::assertNothingDispatched();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

Ви можете передати замикання методам `assertDispatched` чи `assertNotDispatched`, щоб перевірити, що було диспетчеризовано подію, яка проходить заданий тест. Якщо диспетчеризовано щонайменше одну подію, яка проходить заданий тест, перевірка буде успішною:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

Якщо ви просто хочете перевірити, що слухач подій слухає задану подію, скористайтеся методом `assertListening`:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> Після виклику `Event::fake()` жоден слухач подій не виконуватиметься. Тож, якщо ваші тести використовують фабрики моделей, які покладаються на події - наприклад, створення UUID під час події `creating` моделі, - викликайте `Event::fake()` **після** використання фабрик.

<a name="faking-a-subset-of-events"></a>
### Підміна частини подій

Якщо ви хочете підмінити слухачів подій лише для певного набору подій, передайте їх методу `fake` або `fakeFor`:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```

Ви можете підмінити всі події, окрім заданого набору, методом `except`:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### Обмежені підміни подій

Якщо ви хочете підмінити слухачів подій лише для частини вашого тесту, скористайтеся методом `fakeFor`:

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // Events are dispatched as normal and observers will run...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```
