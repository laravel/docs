---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Черги

- [Вступ](#introduction)
    - [Підключення проти черг](#connections-vs-queues)
    - [Нотатки та передумови драйверів](#driver-prerequisites)
- [Створення завдань](#creating-jobs)
    - [Генерація класів завдань](#generating-job-classes)
    - [Структура класу](#class-structure)
    - [Унікальні завдання](#unique-jobs)
    - [Завдання з дебаунсом](#debounced-jobs)
    - [Зашифровані завдання](#encrypted-jobs)
- [Middleware завдань](#job-middleware)
    - [Обмеження частоти](#rate-limiting)
    - [Запобігання накладанню завдань](#preventing-job-overlaps)
    - [Тротлінг винятків](#throttling-exceptions)
    - [Звільнення завдань](#releasing-jobs)
    - [Пропуск завдань](#skipping-jobs)
- [Диспетчеризація завдань](#dispatching-jobs)
    - [Відкладена диспетчеризація](#delayed-dispatching)
    - [Синхронна диспетчеризація](#synchronous-dispatching)
    - [Масова диспетчеризація](#bulk-dispatching)
    - [Підготовка завдань перед диспетчеризацією](#preparing-jobs-before-dispatch)
    - [Завдання й транзакції бази даних](#jobs-and-database-transactions)
    - [Ланцюжки завдань](#job-chaining)
    - [Налаштування черги та підключення](#customizing-the-queue-and-connection)
    - [Задання максимуму спроб / таймауту](#max-job-attempts-and-timeout)
    - [SQS FIFO та справедливі черги](#sqs-fifo-and-fair-queues)
    - [Failover черги](#queue-failover)
    - [Обробка помилок](#error-handling)
- [Пакети завдань](#job-batching)
    - [Опис пакетованих завдань](#defining-batchable-jobs)
    - [Диспетчеризація пакетів](#dispatching-batches)
    - [Ланцюжки й пакети](#chains-and-batches)
    - [Додавання завдань до пакетів](#adding-jobs-to-batches)
    - [Огляд пакетів](#inspecting-batches)
    - [Скасування пакетів](#cancelling-batches)
    - [Невдачі пакетів](#batch-failures)
    - [Очищення пакетів](#pruning-batches)
    - [Зберігання пакетів у DynamoDB](#storing-batches-in-dynamodb)
- [Замикання в черзі](#queueing-closures)
- [Запуск воркера черги](#running-the-queue-worker)
    - [Команда `queue:work`](#the-queue-work-command)
    - [Пріоритети черг](#queue-priorities)
    - [Воркери черги й розгортання](#queue-workers-and-deployment)
    - [Реакція на сигнали воркера](#reacting-to-worker-signals)
    - [Спливання й таймаути завдань](#job-expirations-and-timeouts)
    - [Призупинення й поновлення воркерів черги](#pausing-and-resuming-queue-workers)
- [Конфігурація Supervisor](#supervisor-configuration)
- [Робота з невдалими завданнями](#dealing-with-failed-jobs)
    - [Прибирання після невдалих завдань](#cleaning-up-after-failed-jobs)
    - [Повторний запуск невдалих завдань](#retrying-failed-jobs)
    - [Ігнорування відсутніх моделей](#ignoring-missing-models)
    - [Очищення невдалих завдань](#pruning-failed-jobs)
    - [Зберігання невдалих завдань у DynamoDB](#storing-failed-jobs-in-dynamodb)
    - [Вимкнення зберігання невдалих завдань](#disabling-failed-job-storage)
    - [Події невдалих завдань](#failed-job-events)
- [Очищення черг від завдань](#clearing-jobs-from-queues)
- [Моніторинг черг](#monitoring-your-queues)
- [Тестування](#testing)
    - [Підміна частини завдань](#faking-a-subset-of-jobs)
    - [Тестування ланцюжків завдань](#testing-job-chains)
    - [Тестування пакетів завдань](#testing-job-batches)
    - [Тестування взаємодії завдання з чергою](#testing-job-queue-interactions)
- [Події завдань](#job-events)

<a name="introduction"></a>
## Вступ

Створюючи вебзастосунок, ви можете мати задачі - як-от розбір і збереження завантаженого CSV-файлу, - які виконуються надто довго для звичайного вебзапиту. На щастя, Laravel дозволяє легко створювати завдання в черзі, які обробляються у фоні. Перенісши тривалі задачі до черги, ваш застосунок відповідатиме на вебзапити блискавично й дасть клієнтам кращий досвід.

Черги Laravel надають єдиний API для черг поверх різних бекендів - [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) чи навіть реляційної бази даних.

Опції конфігурації черг Laravel зберігаються у файлі `config/queue.php` вашого застосунку. У цьому файлі ви знайдете конфігурації підключень для кожного драйвера черги, що входить до фреймворку, - database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) та [Beanstalkd](https://beanstalkd.github.io/), - а також синхронний драйвер, який виконує завдання негайно (для розробки чи тестування). Є й драйвер `null`, який відкидає завдання з черги.

> [!NOTE]
> Laravel Horizon - гарна панель керування й система конфігурації для ваших черг на Redis. Докладніше читайте в повній [документації Horizon](/docs/{{version}}/horizon).

<a name="connections-vs-queues"></a>
### Підключення проти черг

Перш ніж братися до черг Laravel, важливо зрозуміти різницю між «підключеннями» та «чергами». У файлі конфігурації `config/queue.php` є масив `connections`. Ця опція описує підключення до бекендів черг - на кшталт Amazon SQS, Beanstalk чи Redis. Проте кожне підключення може мати кілька «черг», які можна уявляти як різні стоси чи купи завдань.

Зверніть увагу: кожен приклад конфігурації підключення у файлі `queue` містить атрибут `queue`. Це черга за замовчуванням, до якої потраплятимуть завдання, надіслані цьому підключенню. Іншими словами, якщо ви диспетчеризуєте завдання, явно не вказавши черги, воно потрапить до черги, заданої атрибутом `queue` конфігурації підключення:

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

Деяким застосункам ніколи не знадобиться класти завдання в кілька черг - їм досить однієї простої черги. Проте кілька черг особливо корисні застосункам, які хочуть пріоритезувати чи сегментувати обробку завдань, адже воркер черги Laravel дозволяє вказати, які черги й у якому пріоритеті йому обробляти. Наприклад, якщо ви кладете завдання в чергу `high`, ви можете запустити воркер, який надасть їм вищий пріоритет обробки:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### Нотатки та передумови драйверів

<a name="database"></a>
#### Database

Щоб скористатися драйвером черги `database`, вам потрібна таблиця для зберігання завдань. Зазвичай вона входить до стандартної [міграції](/docs/{{version}}/migrations) Laravel `0001_01_01_000002_create_jobs_table.php`; проте, якщо у вашому застосунку цієї міграції немає, створити її можна командою Artisan `make:queue-table`:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Щоб скористатися драйвером черги `redis`, налаштуйте підключення до бази Redis у файлі конфігурації `config/database.php`.

> [!WARNING]
> Опції Redis `serializer` та `compression` драйвер черги `redis` не підтримує.

<a name="redis-cluster"></a>
##### Redis Cluster

Якщо ваше підключення черги Redis використовує [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering), назви ваших черг мають містити [хеш-тег ключа](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags). Це потрібно, щоб усі ключі Redis для конкретної черги потрапили в один хеш-слот:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

<a name="blocking"></a>
##### Блокування

Користуючись чергою Redis, ви можете скористатися опцією конфігурації `block_for`, щоб указати, як довго драйвер має чекати на появу завдання, перш ніж пройти цикл воркера й знову опитати базу Redis.

Підбір цього значення під ваше навантаження може бути ефективнішим, ніж постійне опитування Redis на предмет нових завдань. Наприклад, ви можете задати значення `5`, щоб драйвер блокувався на п'ять секунд, чекаючи на завдання:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => 5,
    'after_commit' => false,
],
```

> [!WARNING]
> Значення `block_for`, рівне `0`, змусить воркери черги блокуватися нескінченно, доки не з'явиться завдання. Це також завадить обробляти сигнали на кшталт `SIGTERM`, доки не буде оброблено наступне завдання.

<a name="sqs-overflow-storage"></a>
#### Сховище переповнення SQS

Amazon SQS обмежує максимальний розмір даних повідомлення в черзі. Якщо вам потрібно диспетчеризувати завдання з даними, які можуть перевищити цей ліміт, ви можете налаштувати Laravel зберігати завеликі дані SQS у сховищі кешу й надсилати через SQS лише вказівник. Щоб увімкнути цю можливість, додайте масив `overflow` до конфігурації підключення черги SQS:

```php
'sqs' => [
    'driver' => 'sqs',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'prefix' => env('SQS_PREFIX', 'https://sqs.us-east-1.amazonaws.com/your-account-id'),
    'queue' => env('SQS_QUEUE', 'default'),
    'suffix' => env('SQS_SUFFIX'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'after_commit' => false,
    'overflow' => [
        'enabled' => env('SQS_OVERFLOW_ENABLED', false),
        'store' => env('SQS_OVERFLOW_STORE'),
        'always' => false,
        'delete_after_processing' => true,
        'flush_on_clear' => env('SQS_OVERFLOW_FLUSH_ON_CLEAR', false),
    ],
],
```

Коли сховище переповнення увімкнено, Laravel зберігатиме в налаштованому сховищі кешу дані розміром від 1 МБ. Якщо опція `always` має значення `true`, у сховищі кешу опинятимуться всі дані SQS, незалежно від розміру. Оскільки завданням у черзі доведеться діставати свої дані зі сховища кешу під час обробки, обирайте сховище, яке здатне зберігати ці дані, доки ваші воркери їх не обробили. За замовчуванням збережені дані видаляються після успішної обробки завдань і їх видалення з SQS.

Якщо опція `flush_on_clear` має значення `true`, налаштоване сховище кешу переповнення буде очищено, коли команда `queue:clear` очищає чергу SQS. Оскільки очищення сховища кешу може вилучити з нього всі елементи, вмикаючи цю опцію, налаштуйте для сховища переповнення SQS окреме сховище кешу.

<a name="other-driver-prerequisites"></a>
#### Передумови інших драйверів

Для перелічених драйверів черг потрібні такі залежності. Їх можна встановити через менеджер пакетів Composer:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~3.0` або PHP-розширення phpredis
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## Створення завдань

<a name="generating-job-classes"></a>
### Генерація класів завдань

За замовчуванням усі завдання для черги зберігаються в каталозі `app/Jobs`. Якщо каталогу `app/Jobs` не існує, його буде створено, коли ви виконаєте команду Artisan `make:job`:

```shell
php artisan make:job ProcessPodcast
```

Згенерований клас реалізує інтерфейс `Illuminate\Contracts\Queue\ShouldQueue`, повідомляючи Laravel, що завдання слід покласти в чергу для асинхронного виконання.

> [!NOTE]
> Стаби завдань можна налаштувати через [публікацію стабів](/docs/{{version}}/artisan#stub-customization).

<a name="class-structure"></a>
### Структура класу

Класи завдань дуже прості: зазвичай вони містять лише метод `handle`, який викликається під час обробки завдання чергою. Для початку погляньмо на приклад класу завдання. У цьому прикладі уявімо, що ми керуємо сервісом публікації подкастів і маємо обробляти завантажені файли подкастів перед публікацією:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }
}
```

Зверніть увагу: у цьому прикладі ми змогли передати [модель Eloquent](/docs/{{version}}/eloquent) прямо в конструктор завдання. Завдяки трейту `Queueable`, який використовує завдання, моделі Eloquent та їхні завантажені зв'язки коректно серіалізуються й десеріалізуються під час обробки завдання.

Якщо ваше завдання в черзі приймає модель Eloquent у конструкторі, у чергу серіалізується лише її ідентифікатор. Коли завдання справді обробляється, система черг автоматично дістане з бази повний екземпляр моделі та її завантажені зв'язки. Такий підхід до серіалізації моделей дозволяє надсилати драйверу черги значно менші дані завдань.

<a name="handle-method-dependency-injection"></a>
#### Впровадження залежностей у метод `handle`

Метод `handle` викликається, коли завдання обробляє черга. Зверніть увагу: ми можемо вказати типи залежностей у методі `handle` завдання. [Сервіс-контейнер](/docs/{{version}}/container) Laravel автоматично їх впровадить.

Якщо ви хочете повністю контролювати, як контейнер впроваджує залежності в метод `handle`, скористайтеся методом контейнера `bindMethod`. Метод `bindMethod` приймає колбек, який отримує завдання й контейнер. У колбеку ви вільні викликати метод `handle` як заманеться. Зазвичай цей метод викликають у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers) `App\Providers\AppServiceProvider`:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> Бінарні дані - наприклад, сирий вміст зображень - слід пропускати через функцію `base64_encode`, перш ніж передавати завданню в черзі. Інакше завдання може некоректно серіалізуватися в JSON під час потрапляння в чергу.

<a name="handling-relationships"></a>
#### Зв'язки в черзі

Оскільки всі завантажені зв'язки моделей Eloquent теж серіалізуються, коли завдання потрапляє в чергу, серіалізований рядок завдання інколи стає доволі великим. Ба більше, коли завдання десеріалізується й зв'язки моделей дістаються з бази наново, вони дістаються повністю. Будь-які обмеження зв'язку, застосовані до серіалізації моделі під час постановки завдання в чергу, після десеріалізації вже не діятимуть. Тому, якщо ви хочете працювати з підмножиною зв'язку, обмежте його заново всередині свого завдання.

Або ж, щоб зв'язки не серіалізувалися, викличте на моделі метод `withoutRelations`, задаючи значення властивості. Цей метод поверне екземпляр моделі без завантажених зв'язків:

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

Якщо вам потрібно вилучити лише певні зв'язки, лишивши решту, скористайтеся методом `withoutRelation`:

```php
$this->podcast = $podcast->withoutRelation('comments');
```

Якщо ви користуєтеся [просуванням властивостей конструктора PHP](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion) і хочете вказати, що зв'язки моделі Eloquent не слід серіалізувати, скористайтеся атрибутом `WithoutRelations`:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

Для зручності, якщо ви хочете серіалізувати всі моделі без зв'язків, застосуйте атрибут `WithoutRelations` до всього класу, а не до кожної моделі окремо:

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

Якщо завдання отримує колекцію чи масив моделей Eloquent замість однієї моделі, зв'язки моделей у цій колекції не буде відновлено під час десеріалізації та виконання завдання. Це запобігає надмірному споживанню ресурсів у завданнях, які працюють з великою кількістю моделей.

<a name="unique-jobs"></a>
### Унікальні завдання

> [!WARNING]
> Унікальні завдання потребують драйвера кешу, який підтримує [блокування](/docs/{{version}}/cache#atomic-locks). Наразі атомарні блокування підтримують драйвери кешу `memcached`, `redis`, `dynamodb`, `database`, `file` та `array`.

> [!WARNING]
> Обмеження унікальності не діють для завдань усередині пакетів.

Інколи вам може знадобитися гарантувати, що в черзі одночасно перебуває лише один екземпляр конкретного завдання. Для цього реалізуйте у класі завдання інтерфейс `ShouldBeUnique`. Цей інтерфейс не вимагає описувати у класі жодних додаткових методів:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

У прикладі вище завдання `UpdateSearchIndex` є унікальним. Тож його не буде диспетчеризовано, якщо інший його екземпляр уже в черзі й не завершив обробку.

У певних випадках вам може знадобитися задати конкретний «ключ», який робить завдання унікальним, або вказати таймаут, після якого завдання перестає бути унікальним. Для цього скористайтеся атрибутом `UniqueFor` і опишіть у класі завдання метод `uniqueId`:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Queue\Attributes\UniqueFor;

#[UniqueFor(3600)]
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```
У прикладі вище завдання `UpdateSearchIndex` унікальне за ID продукту. Тож будь-які нові диспетчеризації завдання з тим самим ID продукту ігноруватимуться, доки наявне завдання не завершить обробку. Крім того, якщо наявне завдання не оброблено протягом години, унікальне блокування буде звільнено, і в чергу можна буде диспетчеризувати інше завдання з тим самим унікальним ключем.

> [!WARNING]
> Якщо ваш застосунок диспетчеризує завдання з кількох вебсерверів чи контейнерів, подбайте, щоб усі сервери спілкувалися з одним центральним сервером кешу, - тоді Laravel зможе точно визначити, чи є завдання унікальним.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### Тримати завдання унікальними до початку обробки

За замовчуванням унікальні завдання «розблоковуються» після того, як завдання завершить обробку або вичерпає всі спроби. Проте бувають ситуації, коли ви хочете, щоб завдання розблоковувалося безпосередньо перед обробкою. Для цього ваше завдання має реалізувати контракт `ShouldBeUniqueUntilProcessing` замість `ShouldBeUnique`:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### Блокування унікальних завдань

Під капотом, коли диспетчеризується завдання `ShouldBeUnique`, Laravel намагається отримати [блокування](/docs/{{version}}/cache#atomic-locks) з ключем `uniqueId`. Якщо блокування вже утримується, завдання не диспетчеризують. Це блокування звільняється, коли завдання завершує обробку або вичерпує всі спроби. За замовчуванням Laravel використовує для цього блокування драйвер кешу за замовчуванням. Проте, якщо ви хочете отримувати блокування іншим драйвером, опишіть метод `uniqueVia`, який поверне потрібний драйвер кешу:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> Якщо вам потрібно лише обмежити одночасну обробку завдання, скористайтеся натомість middleware завдання [WithoutOverlapping](/docs/{{version}}/queues#preventing-job-overlaps).

<a name="debounced-jobs"></a>
### Завдання з дебаунсом

Інколи вам може знадобитися гарантувати, що коли те саме завдання диспетчеризують багато разів за короткий проміжок, виконається лише остання диспетчеризація. Для цього додайте до свого завдання атрибут `DebounceFor`:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(public int $productId)
    {
    }

    /**
     * Get the debounce ID for the job.
     */
    public function debounceId(): string
    {
        return (string) $this->productId;
    }
}
```

У прикладі вище повторні диспетчеризації `UpdateSearchIndex` для того самого продукту протягом `30` секунд дебаунсуватимуть завдання так, що виконається лише остання.

Якщо ви хочете обмежити, як довго можна відкладати завдання, яке часто передиспетчеризують, передайте атрибуту `DebounceFor` аргумент `maxWait`:

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    // ...
}
```

Ви можете змінити сховище кешу, яке використовується для відстеження дебаунсу, описавши у своєму завданні метод `debounceVia`:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(): Repository
{
    return Cache::driver('redis');
}
```

Якщо завдання з дебаунсом витіснено новішою диспетчеризацією, Laravel диспетчеризує подію `Illuminate\Queue\Events\JobDebounced` і вилучить витіснене завдання з черги.

> [!WARNING]
> Завдання з дебаунсом і унікальні завдання взаємно виключні. Завдання з атрибутом `DebounceFor` не має реалізовувати `ShouldBeUnique`.

> [!WARNING]
> Якщо ваш застосунок диспетчеризує завдання з дебаунсом з кількох вебсерверів чи контейнерів, подбайте, щоб усі сервери спілкувалися з одним центральним сервером кешу.

<a name="encrypted-jobs"></a>
### Зашифровані завдання

Laravel дозволяє забезпечити приватність і цілісність даних завдання за допомогою [шифрування](/docs/{{version}}/encryption). Для початку просто додайте до класу завдання інтерфейс `ShouldBeEncrypted`. Щойно цей інтерфейс додано до класу, Laravel автоматично зашифрує ваше завдання перед тим, як покласти його в чергу:

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="job-middleware"></a>
## Middleware завдань

Middleware завдань дозволяє огорнути виконання завдань у черзі власною логікою, зменшивши кількість шаблонного коду в самих завданнях. Наприклад, погляньте на метод `handle` нижче, який використовує можливості обмеження частоти через Redis, щоб дозволити обробляти лише одне завдання кожні п'ять секунд:

```php
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // Handle job...
    }, function () {
        // Could not obtain lock...

        return $this->release(5);
    });
}
```

Хоч цей код і робочий, реалізація методу `handle` стає галасливою, бо захаращена логікою обмеження частоти через Redis. Ба більше, цю логіку доведеться дублювати в кожному завданні, частоту якого ми хочемо обмежити. Замість обмежувати частоту в методі handle, ми могли б описати middleware завдання, який цим займеться:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```

Як бачите, подібно до [middleware маршрутів](/docs/{{version}}/middleware), middleware завдань отримує завдання, яке обробляється, і колбек, який слід викликати, щоб продовжити обробку.

Згенерувати новий клас middleware завдання можна командою Artisan `make:job-middleware`. Створивши middleware завдання, ви можете причепити його до завдання, повернувши з методу `middleware` завдання. Цього методу немає в завданнях, згенерованих командою Artisan `make:job`, тож вам доведеться додати його до свого класу вручну:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> Middleware завдань можна також призначати [слухачам подій у черзі](/docs/{{version}}/events#queued-event-listeners), [mailable-класам](/docs/{{version}}/mail#queueing-mail) та [сповіщенням](/docs/{{version}}/notifications#queueing-notifications).

<a name="rate-limiting"></a>
### Обмеження частоти

Хоч ми щойно показали, як написати власний middleware обмеження частоти, Laravel насправді містить готовий middleware, яким можна обмежувати частоту завдань. Як і [обмежувачі частоти маршрутів](/docs/{{version}}/routing#defining-rate-limiters), обмежувачі частоти завдань описують методом `for` фасаду `RateLimiter`.

Наприклад, ви можете хотіти дозволити користувачам робити резервну копію своїх даних раз на годину, не накладаючи такого обмеження на преміум-клієнтів. Для цього опишіть `RateLimiter` у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('backups', function (object $job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```

У прикладі вище ми описали погодинне обмеження; проте ви легко можете описати обмеження за хвилинами методом `perMinute`. Крім того, методу `by` обмеження можна передати будь-яке значення; проте найчастіше його використовують, щоб сегментувати обмеження за клієнтом:

```php
return Limit::perMinute(50)->by($job->user->id);
```

Описавши обмеження, причепіть обмежувач до свого завдання через middleware `Illuminate\Queue\Middleware\RateLimited`. Щоразу, коли завдання перевищить обмеження, цей middleware поверне його до черги з відповідною затримкою на основі тривалості обмеження:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

Повернення обмеженого за частотою завдання до черги все одно збільшує загальну кількість його спроб `attempts`. Тож вам, можливо, варто відповідно налаштувати атрибути `Tries` і `MaxExceptions` у класі завдання. Або ж скористатися [методом retryUntil](#time-based-attempts), щоб задати час, після якого спроби виконати завдання припиняються.

Методом `releaseAfter` ви можете вказати кількість секунд, які мають минути, перш ніж повернене завдання спробують виконати знову:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

Якщо ви не хочете, щоб обмежене за частотою завдання повторювали, скористайтеся методом `dontRelease`:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a name="rate-limiting-with-redis"></a>
#### Обмеження частоти через Redis

Якщо ви користуєтеся Redis, скористайтеся middleware `Illuminate\Queue\Middleware\RateLimitedWithRedis`, який заточено під Redis і який ефективніший за базовий middleware обмеження частоти:

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

Метод `connection` дозволяє вказати, яке підключення Redis має використовувати middleware:

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### Запобігання накладанню завдань

Laravel містить middleware `Illuminate\Queue\Middleware\WithoutOverlapping`, який дозволяє запобігти накладанню завдань за довільним ключем. Це може стати в пригоді, коли завдання в черзі змінює ресурс, який має змінювати лише одне завдання за раз.

Наприклад, уявімо, що у вас є завдання в черзі, яке оновлює кредитний рейтинг користувача, і ви хочете запобігти накладанню таких завдань для того самого ID користувача. Для цього поверніть middleware `WithoutOverlapping` з методу `middleware` вашого завдання:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

Повернення завдання, що накладається, до черги все одно збільшує загальну кількість його спроб. Тож вам, можливо, варто відповідно налаштувати атрибути `Tries` і `MaxExceptions` у класі завдання. Наприклад, якщо лишити `Tries` рівним 1, як за замовчуванням, жодне завдання, що накладається, не буде повторено пізніше.

Будь-які завдання того самого типу, що накладаються, буде повернуто до черги. Ви також можете вказати кількість секунд, які мають минути, перш ніж повернене завдання спробують виконати знову:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

Якщо ви хочете негайно видаляти завдання, що накладаються, аби їх не повторювали, скористайтеся методом `dontRelease`:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

Middleware `WithoutOverlapping` побудовано на можливості атомарних блокувань Laravel. Інколи ваше завдання може несподівано провалитися чи вичерпати таймаут так, що блокування не звільниться. Тому ви можете явно задати час спливання блокування методом `expireAfter`. Наприклад, код нижче скаже Laravel звільнити блокування `WithoutOverlapping` через три хвилини після початку обробки завдання:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> Middleware `WithoutOverlapping` потребує драйвера кешу, який підтримує [блокування](/docs/{{version}}/cache#atomic-locks). Наразі атомарні блокування підтримують драйвери кешу `memcached`, `redis`, `dynamodb`, `database`, `file` та `array`.

<a name="sharing-lock-keys"></a>
#### Спільні ключі блокувань між класами завдань

За замовчуванням middleware `WithoutOverlapping` запобігає накладанню лише завдань того самого класу. Тож, хоч два різні класи завдань і можуть використовувати той самий ключ блокування, їм ніщо не завадить накластися. Проте ви можете сказати Laravel застосовувати ключ між класами завдань методом `shared`:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
### Тротлінг винятків

Laravel містить middleware `Illuminate\Queue\Middleware\ThrottlesExceptions`, який дозволяє тротлити винятки. Щойно завдання викине задану кількість винятків, усі подальші спроби його виконати відкладаються, доки не мине вказаний проміжок часу. Цей middleware особливо корисний для завдань, які працюють із нестабільними сторонніми сервісами.

Наприклад, уявімо завдання в черзі, яке працює зі стороннім API, що почав викидати винятки. Щоб тротлити винятки, поверніть middleware `ThrottlesExceptions` із методу `middleware` вашого завдання. Зазвичай цей middleware поєднують із завданням, що реалізує [спроби на основі часу](#time-based-attempts):

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```

Перший аргумент конструктора middleware - кількість винятків, які завдання може викинути, перш ніж його затротлять, а другий - кількість секунд, які мають минути, перш ніж завдання спробують знову після тротлінгу. У прикладі коду вище, якщо завдання викине 10 винятків поспіль, ми чекатимемо 5 хвилин перед наступною спробою - у межах 30-хвилинного ліміту.

Коли завдання викидає виняток, але порога ще не досягнуто, завдання зазвичай повторюють негайно. Проте ви можете вказати кількість хвилин затримки для такого завдання, викликавши метод `backoff` під час чіпляння middleware до завдання:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

Метод `backoff` також приймає замикання, яке отримує викинутий виняток, - тож затримку можна визначати динамічно:

```php
use App\Exceptions\RateLimitedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;
use Throwable;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(
        fn (Throwable $throwable) => $throwable instanceof RateLimitedException
            ? $throwable->retryAfterMinutes()
            : 5
    )];
}
```

Під капотом цей middleware реалізує обмеження частоти через систему кешу Laravel, а «ключем» кешу слугує назва класу завдання. Ви можете перевизначити цей ключ, викликавши метод `by` під час чіпляння middleware до завдання. Це стане в пригоді, якщо у вас кілька завдань працюють з тим самим стороннім сервісом і ви хочете, щоб вони мали спільний «кошик» тротлінгу й дотримувалися єдиного спільного ліміту:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

За замовчуванням цей middleware тротлить кожен виняток. Ви можете змінити цю поведінку, викликавши метод `when` під час чіпляння middleware до завдання. Тоді виняток тротлитимуть, лише якщо замикання, передане методу `when`, поверне `true`:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

На відміну від методу `when`, який повертає завдання до черги або викидає виняток, метод `deleteWhen` дозволяє повністю видалити завдання, коли трапляється заданий виняток:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

Якщо ви хочете, щоб про затротлені винятки повідомляли обробнику винятків вашого застосунку, викличте метод `report` під час чіпляння middleware до завдання. За бажанням ви можете передати методу `report` замикання, і тоді про виняток повідомлятимуть, лише якщо це замикання поверне `true`:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

<a name="throttling-exceptions-with-redis"></a>
#### Тротлінг винятків через Redis

Якщо ви користуєтеся Redis, скористайтеся middleware `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis`, який заточено під Redis і який ефективніший за базовий middleware тротлінгу винятків:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

Метод `connection` дозволяє вказати, яке підключення Redis має використовувати middleware:

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="releasing-jobs"></a>
### Звільнення завдань

Middleware `Release` дозволяє повернути завдання до черги, не виконуючи його. Метод `Release::when` поверне завдання, якщо задана умова дає `true`, а метод `Release::unless` - якщо умова дає `false`:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when($condition, releaseAfter: 60),
    ];
}
```

Повернення завдання до черги все одно збільшує загальну кількість його спроб. Тож вам, можливо, варто відповідно налаштувати атрибути `Tries` і `MaxExceptions` у класі завдання.

Для складніших умов ви можете передати методам `when` та `unless` `Closure`:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when(function (): bool {
            return ! $this->order->isPaid();
        }, releaseAfter: 60),
    ];
}
```

<a name="skipping-jobs"></a>
### Пропуск завдань

Middleware `Skip` дозволяє вказати, що завдання слід пропустити / видалити, не змінюючи його логіки. Метод `Skip::when` видалить завдання, якщо задана умова дає `true`, а метод `Skip::unless` - якщо умова дає `false`:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

Для складніших умов ви можете передати методам `when` та `unless` `Closure`:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<a name="dispatching-jobs"></a>
## Диспетчеризація завдань

Щойно ви написали клас завдання, ви можете диспетчеризувати його методом `dispatch` на самому завданні. Аргументи, передані методу `dispatch`, потраплять до конструктора завдання:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```

Якщо ви хочете диспетчеризувати завдання умовно, скористайтеся методами `dispatchIf` та `dispatchUnless`:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

У нових застосунках Laravel чергою за замовчуванням задано підключення `database`. Ви можете вказати інше підключення за замовчуванням, змінивши змінну середовища `QUEUE_CONNECTION` у файлі `.env` вашого застосунку.

<a name="delayed-dispatching"></a>
### Відкладена диспетчеризація

Якщо ви хочете вказати, що завдання не має одразу ставати доступним для обробки воркером, скористайтеся методом `delay` під час диспетчеризації. Наприклад, укажімо, що завдання не має бути доступним для обробки протягом 10 хвилин після диспетчеризації:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
            ->delay(now()->plus(minutes: 10));

        return redirect('/podcasts');
    }
}
```

Інколи завдання можуть мати налаштовану затримку за замовчуванням. Якщо вам потрібно обійти цю затримку й диспетчеризувати завдання на негайну обробку, скористайтеся методом `withoutDelay`:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Максимальний час затримки в сервісі черг Amazon SQS - 15 хвилин.

<a name="synchronous-dispatching"></a>
### Синхронна диспетчеризація

Якщо ви хочете диспетчеризувати завдання негайно (синхронно), скористайтеся методом `dispatchSync`. За такого підходу завдання не потрапить у чергу, а виконається одразу в поточному процесі:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="deferred-dispatching"></a>
#### Відкладена диспетчеризація

За допомогою відкладеної синхронної диспетчеризації ви можете диспетчеризувати завдання на обробку в поточному процесі, але вже після того, як HTTP-відповідь надіслано користувачеві. Це дозволяє обробляти завдання «з черги» синхронно, не сповільнюючи роботу застосунку для користувача. Щоб відкласти виконання синхронного завдання, диспетчеризуйте його до підключення `deferred`:

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

Підключення `deferred` також слугує [резервною чергою](#queue-failover) за замовчуванням.

Так само підключення `background` обробляє завдання після надсилання HTTP-відповіді користувачеві; проте завдання обробляється в окремо породженому процесі PHP, тож PHP-FPM / воркер застосунку лишається вільним для обробки наступного вхідного HTTP-запиту:

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="bulk-dispatching"></a>
### Масова диспетчеризація

Якщо вам треба диспетчеризувати багато незалежних завдань одразу й вам не потрібне відстеження [пакетів](#job-batching) чи колбеки, скористайтеся методом `bulk` фасаду `Bus`. Laravel згрупує завдання за налаштованим підключенням і назвою черги й покладе кожну групу до відповідної черги гуртом:

```php
use App\Jobs\ProcessUser;
use Illuminate\Support\Facades\Bus;

Bus::bulk(
    $users->map(fn ($user) => new ProcessUser($user))
);
```

<a name="preparing-jobs-before-dispatch"></a>
### Підготовка завдань перед диспетчеризацією

Якщо завданню потрібно підготуватися чи оглянути свій стан перед потраплянням у чергу, воно може реалізувати інтерфейс `Illuminate\Contracts\Queue\PreparesForDispatch`. Laravel викличе метод `prepareForDispatch` завдання перед його диспетчеризацією. Якщо цей метод поверне `false`, завдання не буде диспетчеризовано:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\PreparesForDispatch;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Cache;

class SyncPodcasts implements PreparesForDispatch, ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public array $podcastIds,
    ) {}

    /**
     * Prepare the job before dispatching.
     */
    public function prepareForDispatch(): bool
    {
        return collect($this->podcastIds)
            ->reject(fn (int $id) => Cache::has("podcast-syncing:{$id}"))
            ->isNotEmpty();
    }
}
```

<a name="jobs-and-database-transactions"></a>
### Завдання й транзакції бази даних

Хоч диспетчеризувати завдання всередині транзакцій бази даних цілком нормально, вам варто подбати, щоб ваше завдання справді змогло успішно виконатися. Коли ви диспетчеризуєте завдання всередині транзакції, можливо, що воркер обробить його ще до фіксації батьківської транзакції. Коли таке трапляється, будь-які зміни, які ви внесли до моделей чи записів у базі під час транзакції (транзакцій), ще можуть не бути в базі. Ба більше, будь-які моделі чи записи, створені всередині транзакції (транзакцій), можуть у базі не існувати.

На щастя, Laravel надає кілька способів обійти цю проблему. По-перше, ви можете задати опцію `after_commit` у масиві конфігурації свого підключення черги:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

Коли опція `after_commit` має значення `true`, ви можете диспетчеризувати завдання всередині транзакцій; проте Laravel зачекає, доки відкриті батьківські транзакції не буде зафіксовано, і лише тоді справді диспетчеризує завдання. Звісно, якщо жодної транзакції наразі не відкрито, завдання буде диспетчеризовано негайно.

Якщо транзакцію відкочено через виняток, що стався під час неї, завдання, диспетчеризовані в межах цієї транзакції, буде відкинуто.

> [!NOTE]
> Значення `true` для опції конфігурації `after_commit` також змусить усі слухачі подій у черзі, mailable-класи, сповіщення та події бродкастингу диспетчеризуватися після фіксації всіх відкритих транзакцій бази даних.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### Задання поведінки фіксації на місці

Якщо ви не задаєте опції конфігурації `after_commit` значення `true`, ви все одно можете вказати, що конкретне завдання слід диспетчеризувати після фіксації всіх відкритих транзакцій. Для цього додайте ланцюжком метод `afterCommit` до операції диспетчеризації:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

Так само, якщо опція конфігурації `after_commit` має значення `true`, ви можете вказати, що конкретне завдання слід диспетчеризувати негайно, не чекаючи фіксації відкритих транзакцій:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### Ланцюжки завдань

Ланцюжки завдань дозволяють задати список завдань у черзі, які слід виконати послідовно після успішного виконання основного завдання. Якщо одне завдання в послідовності провалиться, решта не виконається. Щоб виконати ланцюжок завдань у черзі, скористайтеся методом `chain` фасаду `Bus`. Командна шина Laravel - це нижчорівневий компонент, поверх якого побудовано диспетчеризацію завдань у черзі:

```php
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```

Окрім екземплярів класів завдань, ви можете додавати в ланцюжок і замикання:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> [!WARNING]
> Видалення завдання методом `$this->delete()` усередині завдання не завадить обробці завдань з ланцюжка. Ланцюжок зупиниться, лише якщо завдання в ньому провалиться.

<a name="chain-connection-queue"></a>
#### Підключення та черга ланцюжка

Якщо ви хочете вказати підключення й чергу для завдань ланцюжка, скористайтеся методами `onConnection` та `onQueue`. Ці методи задають підключення й назву черги, які буде використано, якщо завданню явно не призначено інших:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### Додавання завдань до ланцюжка

Інколи вам може знадобитися додати завдання на початок чи в кінець наявного ланцюжка зсередини іншого завдання цього ланцюжка. Це робиться методами `prependToChain` та `appendToChain`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    // Prepend to the current chain, run job immediately after current job...
    $this->prependToChain(new TranscribePodcast);

    // Append to the current chain, run job at end of chain...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### Невдачі ланцюжка

Будуючи ланцюжок завдань, ви можете скористатися методом `catch`, щоб задати замикання, яке буде викликано, якщо завдання в ланцюжку провалиться. Цей колбек отримає екземпляр `Throwable`, що спричинив невдачу:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // A job within the chain has failed...
})->dispatch();
```

> [!WARNING]
> Оскільки колбеки ланцюжка серіалізуються й виконуються пізніше чергою Laravel, не використовуйте в них змінну `$this`.

<a name="customizing-the-queue-and-connection"></a>
### Налаштування черги та підключення

<a name="dispatching-to-a-particular-queue"></a>
#### Диспетчеризація до конкретної черги

Кладучи завдання в різні черги, ви можете «категоризувати» їх і навіть пріоритезувати, скільки воркерів призначити різним чергам. Пам'ятайте: це кладе завдання не в різні «підключення» черг, описані у вашому файлі конфігурації, а лише в конкретні черги в межах одного підключення. Щоб указати чергу, скористайтеся методом `onQueue` під час диспетчеризації завдання:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

Як варіант, ви можете вказати чергу завдання, викликавши метод `onQueue` у його конструкторі:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### Диспетчеризація до конкретного підключення

Якщо ваш застосунок працює з кількома підключеннями черг, вказати, до якого з них покласти завдання, можна методом `onConnection`:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

Ви можете поєднати методи `onConnection` та `onQueue` ланцюжком, щоб задати завданню й підключення, і чергу:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

Як варіант, ви можете вказати підключення завдання, викликавши метод `onConnection` у його конструкторі:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="queue-routing"></a>
#### Маршрутизація черг

Метод `route` фасаду `Queue` дозволяє описати підключення й чергу за замовчуванням для конкретних класів завдань. Це корисно, коли ви хочете, щоб певні завдання завжди йшли в конкретні черги, не вказуючи підключення чи черги в самому завданні.

Окрім конкретних класів завдань, методу `route` можна передати інтерфейс, трейт чи батьківський клас. Тоді будь-яке завдання, яке реалізує цей інтерфейс, використовує трейт чи розширює батьківський клас, автоматично використовуватиме налаштовані підключення й чергу.

Зазвичай метод `route` викликають у методі `boot` сервіс-провайдера:

```php
use App\Concerns\RequiresVideo;
use App\Jobs\ProcessPodcast;
use App\Jobs\ProcessVideo;
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
    Queue::route(RequiresVideo::class, queue: 'video');
}
```

Коли вказано підключення без черги, завдання потрапить до черги за замовчуванням:

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

Ви також можете маршрутизувати кілька класів завдань одразу, передавши методу `route` масив:

```php
Queue::route([
    ProcessPodcast::class => ['podcasts', 'redis'], // Queue and connection
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```

> [!NOTE]
> Маршрутизацію черг усе одно можна перевизначити на рівні окремого завдання.

<a name="max-job-attempts-and-timeout"></a>
### Задання максимуму спроб / таймауту

<a name="max-attempts"></a>
#### Максимум спроб

Спроби завдань - ключове поняття системи черг Laravel, на якому побудовано багато просунутих можливостей. Хоч спершу вони й можуть здаватися заплутаними, важливо зрозуміти, як вони працюють, перш ніж змінювати конфігурацію за замовчуванням.

Коли завдання диспетчеризовано, воно потрапляє в чергу. Далі воркер бере його й намагається виконати. Це і є спроба завдання.

Проте спроба не обов'язково означає, що метод `handle` завдання виконався. Спроби можуть «витрачатися» й кількома іншими способами:

<div class="content-list" markdown="1">

- Завдання натрапило на необроблений виняток під час виконання.
- Завдання вручну повернуто до черги через `$this->release()`.
- Middleware на кшталт `WithoutOverlapping` чи `RateLimited` не зміг отримати блокування й повернув завдання.
- Завдання вичерпало таймаут.
- Метод `handle` завдання виконався й завершився без винятків.

</div>

Ви навряд чи хочете намагатися виконати завдання нескінченно. Тому Laravel надає різні способи вказати, скільки разів або як довго можна намагатися виконати завдання.

> [!NOTE]
> За замовчуванням Laravel намагається виконати завдання лише один раз. Якщо ваше завдання використовує middleware на кшталт `WithoutOverlapping` чи `RateLimited` або якщо ви вручну повертаєте завдання до черги, вам, найімовірніше, доведеться збільшити кількість дозволених спроб опцією `tries`.

Один зі способів задати максимальну кількість спроб - перемикач `--tries` у командному рядку Artisan. Він застосується до всіх завдань, які обробляє воркер, якщо саме завдання не вказує кількості спроб:

```shell
php artisan queue:work --tries=3
```

Якщо завдання перевищить максимальну кількість спроб, воно вважатиметься «невдалим». Докладніше про роботу з невдалими завданнями читайте в [документації про невдалі завдання](#dealing-with-failed-jobs). Якщо команді `queue:work` передано `--tries=0`, завдання повторюватимуть нескінченно.

Ви можете підійти тонше й задати максимальну кількість спроб у самому класі завдання атрибутом `Tries`. Якщо максимум спроб указано в завданні, він матиме перевагу над значенням `--tries` із командного рядка:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Якщо вам потрібен динамічний контроль над максимумом спроб конкретного завдання, опишіть у ньому метод `tries`:

```php
/**
 * Determine number of times the job may be attempted.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### Спроби на основі часу

Як альтернативу заданню кількості спроб перед невдачею ви можете вказати момент, після якого спроби виконати завдання припиняються. Це дозволяє виконувати завдання будь-яку кількість разів у межах заданого проміжку часу. Щоб задати момент, після якого завдання більше не намагатимуться виконати, додайте до класу завдання метод `retryUntil`. Цей метод має повернути екземпляр `DateTime`:

```php
use DateTime;

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 10);
}
```

Якщо описано і `retryUntil`, і `tries`, Laravel віддає перевагу методу `retryUntil`.

> [!NOTE]
> Ви можете описати атрибут `Tries` чи метод `retryUntil` і у своїх [слухачах подій у черзі](/docs/{{version}}/events#queued-event-listeners) та [сповіщеннях у черзі](/docs/{{version}}/notifications#queueing-notifications).

<a name="max-exceptions"></a>
#### Максимум винятків

Інколи вам може знадобитися вказати, що завдання можна намагатися виконати багато разів, але воно має зазнати невдачі, якщо повтори спричинено заданою кількістю необроблених винятків (на відміну від звільнення методом `release` напряму). Для цього скористайтеся атрибутами `Tries` і `MaxExceptions` у класі завдання:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Support\Facades\Redis;

#[Tries(25)]
#[MaxExceptions(3)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // Lock obtained, process the podcast...
        }, function () {
            // Unable to obtain lock...
            return $this->release(10);
        });
    }
}
```

У цьому прикладі завдання повертається до черги на десять секунд, якщо застосунку не вдалося отримати блокування Redis, і повторюватиметься до 25 разів. Проте завдання зазнає невдачі, якщо викине три необроблені винятки.

<a name="stopping-retries-by-exception"></a>
#### Припинення повторів через виняток

Інколи виняток означає, що завдання в черзі має негайно зазнати невдачі, а не повертатися на нову спробу. Ви можете налаштувати типи винятків, які припиняють повтори, методом винятків `dontRetry` у файлі `bootstrap/app.php` вашого застосунку:

```php
use App\Exceptions\InvalidPodcastSourceException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetry([
        InvalidPodcastSourceException::class,
    ]);
})
```

Якщо вам потрібен тонший контроль над тим, коли припиняти повтори, передайте замикання методу `dontRetryWhen`. Коли замикання повертає `true`, завдання буде позначено невдалим і не повторюватиметься:

```php
use App\Exceptions\PodcastProcessingException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetryWhen(function (PodcastProcessingException $e) {
        return $e->reason() === 'Subscription expired';
    });
})
```

<a name="timeout"></a>
#### Таймаут

Часто ви приблизно знаєте, скільки часу мають виконуватися ваші завдання в черзі. Тому Laravel дозволяє задати значення «таймауту». За замовчуванням таймаут становить 60 секунд. Якщо завдання обробляється довше за вказану кількість секунд, воркер, який його обробляє, завершиться з помилкою. Зазвичай воркер автоматично перезапустить [менеджер процесів, налаштований на вашому сервері](#supervisor-configuration).

Максимальну кількість секунд, які можуть виконуватися завдання, можна задати перемикачем `--timeout` у командному рядку Artisan:

```shell
php artisan queue:work --timeout=30
```

Якщо завдання перевищить максимум спроб через постійні таймаути, його буде позначено невдалим.

Ви також можете задати максимальну кількість секунд, які дозволено виконуватися завданню, атрибутом `Timeout` у класі завдання. Якщо таймаут указано в завданні, він матиме перевагу над таймаутом із командного рядка:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Інколи процеси, що блокуються на введенні-виведенні - сокети чи вихідні HTTP-з'єднання, - можуть не зважати на вказаний вами таймаут. Тому, користуючись цими можливостями, завжди намагайтеся задати таймаут і через їхні API. Наприклад, працюючи з [Guzzle](https://docs.guzzlephp.org), завжди вказуйте таймаути з'єднання та запиту.

> [!WARNING]
> Щоб задавати таймаути завдань, має бути встановлено PHP-розширення [PCNTL](https://www.php.net/manual/en/book.pcntl.php). Крім того, «таймаут» завдання завжди має бути меншим за його значення [«retry after»](#job-expiration). Інакше завдання можуть спробувати виконати знову, перш ніж воно справді завершиться чи вичерпає таймаут. Опція `--timeout` не діє, коли команду `queue:work` викликано з опцією `--once`.

<a name="failing-on-timeout"></a>
#### Невдача за таймаутом

Якщо ви хочете, щоб завдання позначалося [невдалим](#dealing-with-failed-jobs) за таймаутом, скористайтеся атрибутом `FailOnTimeout` у класі завдання:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

> [!NOTE]
> За замовчуванням, коли завдання вичерпує таймаут, воно витрачає одну спробу й повертається до черги (якщо повтори дозволено). Проте, якщо ви налаштували завдання зазнавати невдачі за таймаутом, його не повторюватимуть, незалежно від значення tries.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO та справедливі черги

Laravel підтримує черги [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) та [справедливі](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html) черги. Черги FIFO дозволяють обробляти завдання точно в тому порядку, у якому їх надіслано, забезпечуючи обробку рівно один раз завдяки дедуплікації повідомлень.

Черги FIFO потребують ID групи повідомлень, щоб визначити, які завдання можна обробляти паралельно. Завдання з однаковим ID групи обробляються послідовно, а повідомлення з різними ID груп - паралельно.

Laravel надає плавний метод `onGroup`, щоб указати ID групи повідомлень під час диспетчеризації завдань:

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

Черги SQS FIFO підтримують дедуплікацію повідомлень, щоб забезпечити обробку рівно один раз. Реалізуйте у класі завдання метод `deduplicationId`, щоб задати власний ID дедуплікації:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessSubscriptionRenewal implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "renewal-{$this->subscription->id}";
    }
}
```

<a name="fair-queues"></a>
#### Справедливі черги

Якщо ви користуєтеся стандартною чергою SQS, задання групи повідомлень вмикає справедливе розподілення. Іншими словами, щойно ви призначаєте групи, SQS використовує їх, щоб забезпечити справедливу доставку між орендарями / навантаженнями. Додаткова конфігурація Laravel не потрібна.

Замість викликати `onGroup` під час диспетчеризації, ви можете описати метод `messageGroup` безпосередньо в завданні:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessOrder implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return "customer-{$this->order->customer_id}";
    }
}
```

<a name="fifo-listeners-mail-and-notifications"></a>
#### FIFO для слухачів, пошти та сповіщень

Користуючись чергами FIFO, вам також доведеться описати групи повідомлень у слухачах, пошті та сповіщеннях. Як варіант, ви можете диспетчеризувати ці об'єкти в чергу, відмінну від FIFO.

Щоб задати групу повідомлень для [слухача подій у черзі](/docs/{{version}}/events#queued-event-listeners), опишіть у слухачі метод `messageGroup`. За бажанням ви можете описати й метод `deduplicationId`:

```php
<?php

namespace App\Listeners;

class SendShipmentNotification
{
    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return 'shipments';
    }

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "shipment-notification-{$this->shipment->id}";
    }
}
```

Надсилаючи [поштове повідомлення](/docs/{{version}}/mail), яке потрапить у чергу FIFO, викличте метод `onGroup` і, за бажанням, метод `withDeduplicator`:

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

Надсилаючи [сповіщення](/docs/{{version}}/notifications), яке потрапить у чергу FIFO, викличте метод `onGroup` і, за бажанням, метод `withDeduplicator`:

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
### Failover черги

Драйвер черги `failover` забезпечує автоматичне перемикання під час покладання завдань у чергу. Якщо основне підключення черги з конфігурації `failover` з якоїсь причини провалиться, Laravel автоматично спробує покласти завдання до наступного підключення зі списку. Це особливо корисно для забезпечення високої доступності в продакшн-середовищах, де надійність черг критична.

Щоб налаштувати підключення `failover`, укажіть драйвер `failover` і передайте масив назв підключень, які слід пробувати по черзі. За замовчуванням Laravel містить приклад конфігурації failover у файлі `config/queue.php` вашого застосунку:

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'redis',
        'database',
        'sync',
    ],
],
```

Щойно ви налаштували підключення з драйвером `failover`, вам потрібно зробити його підключенням черги за замовчуванням у файлі `.env` вашого застосунку, щоб скористатися цією можливістю:

```ini
QUEUE_CONNECTION=failover
```

Далі запустіть щонайменше один воркер для кожного підключення зі свого списку failover:

```bash
php artisan queue:work redis
php artisan queue:work database
```

> [!NOTE]
> Запускати воркер для підключень із драйверами черг `sync`, `background` чи `deferred` не потрібно, адже ці драйвери обробляють завдання в поточному процесі PHP.

Коли операція з підключенням черги провалюється й активується failover, Laravel диспетчеризує подію `Illuminate\Queue\Events\QueueFailedOver`, тож ви можете повідомити про це чи залогувати, що підключення черги провалилося.

> [!NOTE]
> Якщо ви користуєтеся Laravel Horizon, пам'ятайте: Horizon керує лише чергами Redis. Якщо ваш список failover містить `database`, вам слід запустити звичайний процес `php artisan queue:work database` поряд із Horizon.

<a name="error-handling"></a>
### Обробка помилок

Якщо під час обробки завдання викинуто виняток, завдання автоматично повернеться до черги, щоб його спробували виконати знову. Завдання повертатимуть, доки не буде вичерпано максимальну кількість спроб, дозволену вашим застосунком. Максимум спроб задають перемикачем `--tries` команди Artisan `queue:work`. Як варіант, максимум спроб можна задати в самому класі завдання. Докладніше про запуск воркера черги [читайте нижче](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### Ручне звільнення завдання

Інколи вам може захотітися вручну повернути завдання до черги, щоб його спробували виконати пізніше. Це робиться викликом методу `release`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

За замовчуванням метод `release` поверне завдання до черги на негайну обробку. Проте ви можете сказати черзі не робити завдання доступним для обробки, доки не мине задана кількість секунд, - передайте методу `release` ціле число чи екземпляр дати:

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a name="manually-failing-a-job"></a>
#### Ручне позначення завдання невдалим

Інколи вам може знадобитися вручну позначити завдання «невдалим». Для цього викличте метод `fail`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

Якщо ви хочете позначити завдання невдалим через спійманий виняток, передайте цей виняток методу `fail`. Або, для зручності, передайте рядок із повідомленням про помилку, який буде перетворено на виняток за вас:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> Докладніше про невдалі завдання читайте в [документації про роботу з невдалими завданнями](#dealing-with-failed-jobs).

<a name="fail-jobs-on-exceptions"></a>
#### Невдача завдань на конкретних винятках

[Middleware завдання](#job-middleware) `FailOnException` дозволяє припинити повтори, коли викинуто конкретні винятки. Це дозволяє повторювати спроби на тимчасових винятках - наприклад, помилках зовнішнього API, - але остаточно провалювати завдання на стійких, як-от відкликанні прав користувача:

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

#[Tries(3)]
class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $this->user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$this->user->uuid}"
        );

        // ...
    }

    /**
     * Get the middleware the job should pass through.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a name="job-batching"></a>
## Пакети завдань

Пакети завдань у Laravel дозволяють легко виконати групу завдань паралельно, а потім зробити щось, коли пакет завершив виконання.

Перш ніж почати, створіть міграцію бази даних, яка збудує таблицю з метаінформацією про ваші пакети завдань - наприклад, відсотком виконання. Цю міграцію можна згенерувати командою Artisan `make:queue-batches-table`:

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### Опис пакетованих завдань

Щоб описати пакетоване завдання, [створіть завдання для черги](#creating-jobs) як зазвичай; проте додайте до класу завдання трейт `Illuminate\Bus\Batchable`. Цей трейт надає доступ до методу `batch`, яким можна дістати поточний пакет, у межах якого виконується завдання:

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // Determine if the batch has been cancelled...

            return;
        }

        // Import a portion of the CSV file...
    }
}
```

<a name="dispatching-batches"></a>
### Диспетчеризація пакетів

Щоб диспетчеризувати пакет завдань, скористайтеся методом `batch` фасаду `Bus`. Звісно, пакети насамперед корисні в поєднанні з колбеками завершення. Тож ви можете скористатися методами `then`, `catch` та `finally`, щоб описати колбеки завершення пакета. Кожен із них отримає екземпляр `Illuminate\Bus\Batch` під час виклику.

Коли працює кілька воркерів черги, завдання пакета обробляються паралельно. Тому порядок їх завершення може не збігатися з порядком, у якому їх додано до пакета. Про те, як виконати серію завдань послідовно, читайте в нашій документації про [ланцюжки й пакети](#chains-and-batches).

У цьому прикладі уявімо, що ми ставимо в чергу пакет завдань, кожне з яких обробляє задану кількість рядків CSV-файлу:

```php
use App\Jobs\ImportCsv;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ImportCsv(1, 100),
    new ImportCsv(101, 200),
    new ImportCsv(201, 300),
    new ImportCsv(301, 400),
    new ImportCsv(401, 500),
])->before(function (Batch $batch) {
    // The batch has been created but no jobs have been added...
})->progress(function (Batch $batch) {
    // A single job has completed successfully...
})->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // Batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```

ID пакета, доступний через властивість `$batch->id`, дозволяє [запитувати командну шину Laravel](#inspecting-batches) про інформацію щодо пакета після його диспетчеризації.

> [!WARNING]
> Оскільки колбеки пакета серіалізуються й виконуються пізніше чергою Laravel, не використовуйте в них змінну `$this`. Крім того, оскільки пакетовані завдання огорнуто транзакціями бази даних, усередині них не слід виконувати SQL-інструкцій, які спричиняють неявну фіксацію.

<a name="naming-batches"></a>
#### Іменування пакетів

Деякі інструменти - як-от [Laravel Horizon](/docs/{{version}}/horizon) та [Laravel Telescope](/docs/{{version}}/telescope) - можуть давати зручнішу налагоджувальну інформацію про пакети, якщо ті мають назви. Щоб призначити пакету довільну назву, викличте метод `name` під час його опису:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### Підключення та черга пакета

Якщо ви хочете вказати підключення й чергу для пакетованих завдань, скористайтеся методами `onConnection` та `onQueue`. Усі пакетовані завдання мають виконуватися в межах одного підключення й однієї черги:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### Ланцюжки й пакети

Ви можете описати набір [завдань у ланцюжку](#job-chaining) усередині пакета, поклавши ці завдання в масив. Наприклад, ми можемо виконати два ланцюжки завдань паралельно й виконати колбек, коли обидва завершать обробку:

```php
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

Bus::batch([
    [
        new ReleasePodcast(1),
        new SendPodcastReleaseNotification(1),
    ],
    [
        new ReleasePodcast(2),
        new SendPodcastReleaseNotification(2),
    ],
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->dispatch();
```

І навпаки, ви можете виконувати пакети завдань усередині [ланцюжка](#job-chaining), описавши пакети в ньому. Наприклад, ви могли б спершу виконати пакет завдань, який публікує кілька подкастів, а потім пакет, який надсилає сповіщення про публікацію:

```php
use App\Jobs\FlushPodcastCache;
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new FlushPodcastCache,
    Bus::batch([
        new ReleasePodcast(1),
        new ReleasePodcast(2),
    ]),
    Bus::batch([
        new SendPodcastReleaseNotification(1),
        new SendPodcastReleaseNotification(2),
    ]),
])->dispatch();
```

<a name="adding-jobs-to-batches"></a>
### Додавання завдань до пакетів

Інколи буває корисно додати до пакета додаткові завдання зсередини пакетованого завдання. Цей патерн стане в пригоді, коли вам треба запакувати тисячі завдань, диспетчеризація яких зайняла б надто багато часу під час вебзапиту. Тож натомість ви можете диспетчеризувати початковий пакет «завантажувальних» завдань, які наповнять пакет іще більшою кількістю завдань:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```

У цьому прикладі ми скористаємося завданням `LoadImportBatch`, щоб наповнити пакет додатковими завданнями. Для цього ми можемо скористатися методом `add` на екземплярі пакета, доступному через метод `batch` завдання:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> [!WARNING]
> Додавати завдання до пакета можна лише зсередини завдання, яке належить до цього самого пакета.

<a name="inspecting-batches"></a>
### Огляд пакетів

Екземпляр `Illuminate\Bus\Batch`, який передається до колбеків завершення пакета, має низку властивостей і методів, що допомагають працювати з пакетом завдань і оглядати його:

```php
// The UUID of the batch...
$batch->id;

// The name of the batch (if applicable)...
$batch->name;

// The number of jobs assigned to the batch...
$batch->totalJobs;

// The number of jobs that have not been processed by the queue...
$batch->pendingJobs;

// The number of jobs that have failed...
$batch->failedJobs;

// The number of jobs that have been processed thus far...
$batch->processedJobs();

// The completion percentage of the batch (0-100)...
$batch->progress();

// Indicates if the batch has finished executing...
$batch->finished();

// Cancel the execution of the batch...
$batch->cancel();

// Indicates if the batch has been cancelled...
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### Повернення пакетів із маршрутів

Усі екземпляри `Illuminate\Bus\Batch` серіалізуються в JSON, тож ви можете повертати їх напряму з маршрутів свого застосунку, щоб отримати JSON-дані з інформацією про пакет, включно з прогресом виконання. Це зручно, щоб показувати прогрес пакета в інтерфейсі вашого застосунку.

Щоб дістати пакет за його ID, скористайтеся методом `findBatch` фасаду `Bus`:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### Скасування пакетів

Інколи вам може знадобитися скасувати виконання пакета. Це робиться викликом методу `cancel` на екземплярі `Illuminate\Bus\Batch`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        $this->batch()->cancel();

        return;
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

Як ви могли помітити в попередніх прикладах, пакетовані завдання зазвичай мають перевіряти, чи не скасовано відповідний пакет, перш ніж продовжувати виконання. Проте для зручності ви можете натомість призначити завданню [middleware](#job-middleware) `SkipIfBatchCancelled`. Як випливає з назви, цей middleware скаже Laravel не обробляти завдання, якщо відповідний пакет скасовано:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### Невдачі пакетів

Коли пакетоване завдання зазнає невдачі, буде викликано колбек `catch` (якщо його призначено). Цей колбек викликається лише для першого завдання, що провалилося в пакеті.

<a name="allowing-failures"></a>
#### Дозвіл на невдачі

Коли завдання в пакеті провалюється, Laravel автоматично позначає пакет «скасованим». За бажанням ви можете вимкнути цю поведінку, щоб невдача завдання не скасовувала пакет автоматично. Це робиться викликом методу `allowFailures` під час диспетчеризації пакета:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

За бажанням ви можете передати методу `allowFailures` замикання, яке виконуватиметься на кожній невдачі завдання:

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### Повторний запуск невдалих завдань пакета

Для зручності Laravel надає команду Artisan `queue:retry-batch`, яка дозволяє легко повторити всі невдалі завдання конкретного пакета. Ця команда приймає UUID пакета, невдалі завдання якого слід повторити:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### Очищення пакетів

Без очищення таблиця `job_batches` дуже швидко накопичує записи. Щоб цьому зарадити, [заплануйте](/docs/{{version}}/scheduling) щоденне виконання команди Artisan `queue:prune-batches`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

За замовчуванням буде очищено всі завершені пакети, старші за 24 години. Ви можете скористатися опцією `hours` під час виклику команди, щоб визначити, як довго зберігати дані пакетів. Наприклад, команда нижче видалить усі пакети, які завершилися понад 48 годин тому:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

Інколи ваша таблиця `job_batches` може накопичувати записи пакетів, які так і не завершилися успішно, - наприклад, пакетів, у яких завдання провалилося й так і не було успішно повторено. Ви можете сказати команді `queue:prune-batches` очищати такі незавершені записи опцією `unfinished`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

Так само ваша таблиця `job_batches` може накопичувати записи скасованих пакетів. Ви можете сказати команді `queue:prune-batches` очищати такі записи опцією `cancelled`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### Зберігання пакетів у DynamoDB

Laravel також підтримує зберігання метаінформації пакетів у [DynamoDB](https://aws.amazon.com/dynamodb) замість реляційної бази даних. Проте вам доведеться вручну створити таблицю DynamoDB для зберігання всіх записів пакетів.

Зазвичай цю таблицю називають `job_batches`, але вам слід назвати її відповідно до значення конфігурації `queue.batching.table` у файлі конфігурації `queue` вашого застосунку.

<a name="dynamodb-batch-table-configuration"></a>
#### Конфігурація таблиці пакетів у DynamoDB

Таблиця `job_batches` має мати рядковий первинний ключ розділу `application` і рядковий первинний ключ сортування `id`. Частина ключа `application` міститиме назву вашого застосунку, задану значенням конфігурації `name` у файлі конфігурації `app`. Оскільки назва застосунку є частиною ключа таблиці DynamoDB, ви можете зберігати в одній таблиці пакети завдань кількох застосунків Laravel.

Крім того, ви можете описати для своєї таблиці атрибут `ttl`, якщо хочете скористатися [автоматичним очищенням пакетів](#pruning-batches-in-dynamodb).

<a name="dynamodb-configuration"></a>
#### Конфігурація DynamoDB

Далі встановіть AWS SDK, щоб ваш застосунок Laravel міг спілкуватися з Amazon DynamoDB:

```shell
composer require aws/aws-sdk-php
```

Потім задайте опції конфігурації `queue.batching.driver` значення `dynamodb`. Крім того, опишіть у масиві конфігурації `batching` опції `key`, `secret` та `region`. Вони використовуватимуться для автентифікації в AWS. Коли ви користуєтеся драйвером `dynamodb`, опція конфігурації `queue.batching.database` не потрібна:

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

<a name="pruning-batches-in-dynamodb"></a>
#### Очищення пакетів у DynamoDB

Коли ви зберігаєте інформацію про пакети завдань у [DynamoDB](https://aws.amazon.com/dynamodb), звичайні команди очищення, які працюють із реляційною базою, не діятимуть. Натомість ви можете скористатися [рідною функціональністю TTL у DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html), щоб автоматично вилучати записи старих пакетів.

Якщо ви описали свою таблицю DynamoDB з атрибутом `ttl`, ви можете задати параметри конфігурації, які скажуть Laravel, як очищати записи пакетів. Значення конфігурації `queue.batching.ttl_attribute` задає назву атрибута з TTL, а значення `queue.batching.ttl` - кількість секунд, після яких запис пакета можна вилучити з таблиці DynamoDB, відлічуючи від останнього оновлення запису:

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7 days...
],
```

<a name="queueing-closures"></a>
## Замикання в черзі

Замість диспетчеризувати в чергу клас завдання, ви можете диспетчеризувати замикання. Це чудово підходить для швидких простих задач, які треба виконати поза поточним циклом запиту. Коли ви диспетчеризуєте замикання в чергу, його код криптографічно підписується, щоб його не можна було змінити в дорозі:

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

Щоб призначити замиканню в черзі назву, яку зможуть використовувати панелі звітності черг і яку показуватиме команда `queue:work`, скористайтеся методом `name`:

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

Методом `catch` ви можете передати замикання, яке слід виконати, якщо замикання в черзі не завершиться успішно, вичерпавши всі [налаштовані спроби](#max-job-attempts-and-timeout) вашої черги:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> Оскільки колбеки `catch` серіалізуються й виконуються пізніше чергою Laravel, не використовуйте в них змінну `$this`.

<a name="running-the-queue-worker"></a>
## Запуск воркера черги

<a name="the-queue-work-command"></a>
### Команда `queue:work`

Laravel містить команду Artisan, яка запускає воркер черги й обробляє нові завдання, щойно вони потрапляють у чергу. Запустити воркер можна командою Artisan `queue:work`. Зверніть увагу: щойно команду `queue:work` запущено, вона працюватиме, доки ви не зупините її вручну чи не закриєте термінал:

```shell
php artisan queue:work
```

> [!NOTE]
> Щоб процес `queue:work` постійно працював у фоні, скористайтеся монітором процесів на кшталт [Supervisor](#supervisor-configuration), який подбає, щоб воркер черги не зупинявся.

Ви можете додати прапорець `-v` під час виклику команди `queue:work`, якщо хочете, щоб у виводі команди були ID оброблених завдань, назви підключень і черг:

```shell
php artisan queue:work -v
```

Пам'ятайте: воркери черги - це довгограючі процеси, які тримають завантажений стан застосунку в пам'яті. Тому вони не помітять змін у вашій кодовій базі після запуску. Отже, під час розгортання обов'язково [перезапускайте свої воркери черги](#queue-workers-and-deployment). Крім того, пам'ятайте, що будь-який статичний стан, створений чи змінений вашим застосунком, не скидатиметься автоматично між завданнями.

Як варіант, ви можете виконати команду `queue:listen`. Коли ви користуєтеся `queue:listen`, вам не доводиться вручну перезапускати воркер, щоб підхопити оновлений код чи скинути стан застосунку; проте ця команда значно менш ефективна за `queue:work`:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### Запуск кількох воркерів черги

Щоб призначити черзі кілька воркерів і обробляти завдання паралельно, просто запустіть кілька процесів `queue:work`. Це можна зробити локально в кількох вкладках термінала або в продакшені через налаштування вашого менеджера процесів. [Користуючись Supervisor](#supervisor-configuration), скористайтеся значенням конфігурації `numprocs`.

<a name="specifying-the-connection-queue"></a>
#### Задання підключення та черги

Ви також можете вказати, яке підключення черги має використовувати воркер. Назва підключення, передана команді `work`, має відповідати одному з підключень, описаних у файлі `config/queue.php`:

```shell
php artisan queue:work redis
```

За замовчуванням команда `queue:work` обробляє завдання лише з черги за замовчуванням заданого підключення. Проте ви можете налаштувати воркер іще тонше, обробляючи лише певні черги конкретного підключення. Наприклад, якщо всі ваші листи обробляються в черзі `emails` на підключенні `redis`, ви можете виконати таку команду, щоб запустити воркер, який обробляє лише цю чергу:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### Обробка заданої кількості завдань

Опція `--once` дозволяє сказати воркеру обробити з черги лише одне завдання:

```shell
php artisan queue:work --once
```

Опція `--max-jobs` дозволяє сказати воркеру обробити задану кількість завдань і завершитися. Ця опція стане в пригоді в поєднанні із [Supervisor](#supervisor-configuration), щоб ваші воркери автоматично перезапускалися після обробки певної кількості завдань, звільняючи накопичену пам'ять:

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### Обробка всіх завдань у черзі й завершення

Опція `--stop-when-empty` дозволяє сказати воркеру обробити всі завдання й коректно завершитися. Ця опція стане в пригоді під час обробки черг Laravel у Docker-контейнері, якщо ви хочете зупинити контейнер, коли черга спорожніє:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### Обробка завдань протягом заданої кількості секунд

Опція `--max-time` дозволяє сказати воркеру обробляти завдання протягом заданої кількості секунд і завершитися. Ця опція стане в пригоді в поєднанні із [Supervisor](#supervisor-configuration), щоб ваші воркери автоматично перезапускалися після певного часу роботи, звільняючи накопичену пам'ять:

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### Тривалість сну воркера

Коли в черзі є завдання, воркер оброблятиме їх без затримок між ними. Проте опція `sleep` визначає, скільки секунд воркер «спатиме», якщо завдань немає. Звісно, поки він спить, нові завдання не оброблятимуться:

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### Режим обслуговування й черги

Доки ваш застосунок у [режимі обслуговування](/docs/{{version}}/configuration#maintenance-mode), жодне завдання з черги не оброблятиметься. Завдання оброблятимуться як зазвичай, щойно застосунок вийде з режиму обслуговування.

Щоб змусити воркери обробляти завдання навіть у режимі обслуговування, скористайтеся опцією `--force`:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### Міркування щодо ресурсів

Демонізовані воркери черги не «перезавантажують» фреймворк перед обробкою кожного завдання. Тому вам слід звільняти важкі ресурси після завершення кожного завдання. Наприклад, якщо ви робите [обробку зображень](/docs/{{version}}/images) [бібліотекою GD](https://www.php.net/manual/en/book.image.php), звільняйте пам'ять через `imagedestroy`, коли завершили роботу із зображенням.

<a name="queue-priorities"></a>
### Пріоритети черг

Інколи вам може захотітися пріоритезувати обробку своїх черг. Наприклад, у файлі `config/queue.php` ви можете задати чергою `queue` за замовчуванням для підключення `redis` значення `low`. Проте інколи вам може захотітися покласти завдання в чергу високого пріоритету `high` ось так:

```php
dispatch((new Job)->onQueue('high'));
```

Щоб запустити воркер, який гарантує, що всі завдання черги `high` оброблено перед переходом до завдань черги `low`, передайте команді `work` список назв черг через кому:

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### Воркери черги й розгортання

Оскільки воркери черги - довгограючі процеси, вони не помітять змін у вашому коді без перезапуску. Тож найпростіший спосіб розгортати застосунок із воркерами черги - перезапускати їх під час розгортання. Коректно перезапустити всі воркери можна командою `queue:restart`:

```shell
php artisan queue:restart
```

Ця команда скаже всім воркерам черги коректно завершитися після обробки поточного завдання, щоб жодне наявне завдання не було втрачено. Оскільки воркери завершаться під час виконання `queue:restart`, вам слід мати менеджер процесів на кшталт [Supervisor](#supervisor-configuration), який автоматично їх перезапустить.

> [!NOTE]
> Черга використовує [кеш](/docs/{{version}}/cache) для зберігання сигналів перезапуску, тож перед використанням цієї можливості переконайтеся, що драйвер кешу належно налаштовано у вашому застосунку.

<a name="reacting-to-worker-signals"></a>
### Реакція на сигнали воркера

Коли воркер черги отримує сигнал завершення - `SIGQUIT`, `SIGTERM` чи `SIGINT` - під час обробки завдання, він завершить поточне завдання й лише тоді вийде. Проте вашому завданню може знадобитися відреагувати на сигнал, перш ніж сервер чи оркестратор контейнерів зупинить процес. Наприклад, довготривале завдання імпорту може мати припинити діставати нові записи й зберегти поточний прогрес.

Щоб реагувати на сигнали воркера зсередини завдання, реалізуйте інтерфейс `Illuminate\Contracts\Queue\Interruptible` й опишіть у завданні метод `interrupted`. Номер сигналу, отриманого воркером, буде передано до методу `interrupted`:

```php
<?php

namespace App\Jobs;

use App\Models\Import;
use Illuminate\Contracts\Queue\Interruptible;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportProducts implements ShouldQueue, Interruptible
{
    use Queueable;

    protected bool $shouldStop = false;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Import $import,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        foreach ($this->import->pendingRows() as $row) {
            if ($this->shouldStop) {
                break;
            }

            // Import the product row...
        }

        $this->import->saveProgress();
    }

    /**
     * Handle a signal received by the queue worker.
     */
    public function interrupted(int $signal): void
    {
        $this->shouldStop = true;
    }
}
```

Метод `interrupted` викликається лише тоді, коли воркер отримує сигнал процесу під час виконання завдання. Він не замінює [таймаутів](#worker-timeouts) чи [методу `failed`](#cleaning-up-after-failed-jobs) завдання.

<a name="job-expirations-and-timeouts"></a>
### Спливання й таймаути завдань

<a name="job-expiration"></a>
#### Спливання завдання

У файлі конфігурації `config/queue.php` кожне підключення черги описує опцію `retry_after`. Ця опція задає, скільки секунд підключення має чекати, перш ніж повторити завдання, яке обробляється. Наприклад, якщо значення `retry_after` дорівнює `90`, завдання повернеться до черги, якщо воно оброблялося 90 секунд і не було звільнене чи видалене. Зазвичай значення `retry_after` варто задавати рівним максимальній кількості секунд, яку ваші завдання розумно можуть обробляти.

> [!WARNING]
> Єдине підключення черги, яке не має значення `retry_after`, - Amazon SQS. SQS повторить завдання на основі [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html), яким керують у консолі AWS.

<a name="worker-timeouts"></a>
#### Таймаути воркера

Команда Artisan `queue:work` має опцію `--timeout`. За замовчуванням значення `--timeout` становить 60 секунд. Якщо завдання обробляється довше за вказану кількість секунд, воркер, який його обробляє, завершиться з помилкою. Зазвичай воркер автоматично перезапустить [менеджер процесів, налаштований на вашому сервері](#supervisor-configuration):

```shell
php artisan queue:work --timeout=60
```

Опція конфігурації `retry_after` та CLI-опція `--timeout` різні, але працюють разом, щоб завдання не губилися й оброблялися успішно лише один раз.

> [!WARNING]
> Значення `--timeout` завжди має бути щонайменше на кілька секунд меншим за значення конфігурації `retry_after`. Це гарантує, що воркер, який обробляє зависле завдання, завжди завершиться до того, як завдання повторять. Якщо ваша опція `--timeout` довша за значення `retry_after`, ваші завдання можуть оброблятися двічі.

<a name="pausing-and-resuming-queue-workers"></a>
### Призупинення й поновлення воркерів черги

Інколи вам може знадобитися тимчасово завадити воркеру обробляти нові завдання, не зупиняючи його повністю. Наприклад, ви можете хотіти призупинити обробку завдань під час обслуговування системи. Laravel надає команди Artisan `queue:pause` та `queue:continue`, щоб призупиняти й поновлювати воркери черги.

Щоб призупинити конкретну чергу, передайте назву підключення й назву черги:

```shell
php artisan queue:pause database:default
```

У цьому прикладі `database` - назва підключення черги, а `default` - назва черги. Щойно чергу призупинено, воркери, які обробляють з неї завдання, завершать поточне завдання, але не візьмуть нових, доки чергу не поновлять.

Щоб поновити обробку завдань у призупиненій черзі, скористайтеся командою `queue:continue`:

```shell
php artisan queue:continue database:default
```

Після поновлення черги воркери одразу почнуть обробляти з неї нові завдання. Зверніть увагу: призупинення черги не зупиняє самого процесу воркера - воно лише не дає воркеру брати нові завдання з указаної черги.

<a name="worker-restart-and-pause-signals"></a>
#### Сигнали перезапуску й призупинення воркера

За замовчуванням воркери черги опитують драйвер кешу на предмет сигналів перезапуску й призупинення на кожній ітерації завдання. Хоч це опитування й потрібне для реакції на команди `queue:restart` і `queue:pause`, воно додає невеликі накладні витрати.

Якщо вам треба оптимізувати швидкодію й ці можливості переривання не потрібні, ви можете вимкнути опитування глобально, викликавши метод `withoutInterruptionPolling` фасаду `Queue`. Зазвичай це роблять у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::withoutInterruptionPolling();
}
```

Як варіант, ви можете вимкнути опитування перезапуску чи призупинення окремо, задавши статичні властивості `$restartable` або `$pausable` класу `Illuminate\Queue\Worker`:

```php
use Illuminate\Queue\Worker;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Worker::$restartable = false;
    Worker::$pausable = false;
}
```

> [!WARNING]
> Коли опитування переривань вимкнено, воркери не реагуватимуть на команди `queue:restart` чи `queue:pause` (залежно від того, які можливості вимкнено).

<a name="supervisor-configuration"></a>
## Конфігурація Supervisor

У продакшені вам потрібен спосіб тримати процеси `queue:work` запущеними. Процес `queue:work` може зупинитися з різних причин - через перевищений таймаут воркера чи виконання команди `queue:restart`.

Тому вам потрібно налаштувати монітор процесів, який виявляє, коли ваші процеси `queue:work` завершуються, і автоматично їх перезапускає. Крім того, монітори процесів дозволяють указати, скільки процесів `queue:work` ви хочете запускати паралельно. Supervisor - монітор процесів, який часто використовують у Linux-середовищах, і далі ми розглянемо, як його налаштувати.

<a name="installing-supervisor"></a>
#### Встановлення Supervisor

Supervisor - монітор процесів для операційної системи Linux, який автоматично перезапустить ваші процеси `queue:work`, якщо вони провалилися. Щоб встановити Supervisor в Ubuntu, скористайтеся такою командою:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Якщо налаштовувати Supervisor і керувати ним самотужки звучить надто складно, розгляньте [Laravel Cloud](https://cloud.laravel.com) - повністю керовану платформу для запуску воркерів черг Laravel.

<a name="configuring-supervisor"></a>
#### Налаштування Supervisor

Файли конфігурації Supervisor зазвичай зберігаються в каталозі `/etc/supervisor/conf.d`. У цьому каталозі ви можете створити скільки завгодно файлів конфігурації, які кажуть supervisor, як стежити за вашими процесами. Наприклад, створімо файл `laravel-worker.conf`, який запускає процеси `queue:work` і стежить за ними:

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=forge
numprocs=8
redirect_stderr=true
stdout_logfile=/home/forge/app.com/worker.log
stopwaitsecs=3600
```

У цьому прикладі директива `numprocs` скаже Supervisor запустити вісім процесів `queue:work` і стежити за всіма, автоматично перезапускаючи їх у разі падіння. Змініть директиву `command` конфігурації відповідно до потрібного вам підключення черги й опцій воркера.

> [!WARNING]
> Подбайте, щоб значення `stopwaitsecs` було більшим за кількість секунд, які триває ваше найдовше завдання. Інакше Supervisor може вбити завдання, перш ніж воно завершить обробку.

<a name="starting-supervisor"></a>
#### Запуск Supervisor

Щойно файл конфігурації створено, ви можете оновити конфігурацію Supervisor і запустити процеси такими командами:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Докладніше про Supervisor читайте в [документації Supervisor](http://supervisord.org/index.html).

<a name="dealing-with-failed-jobs"></a>
## Робота з невдалими завданнями

Інколи ваші завдання в черзі провалюються. Не переймайтеся, не все й не завжди йде за планом! Laravel містить зручний спосіб [задати максимальну кількість спроб виконати завдання](#max-job-attempts-and-timeout). Коли асинхронне завдання перевищить цю кількість спроб, його буде вставлено до таблиці `failed_jobs`. [Синхронно диспетчеризовані завдання](/docs/{{version}}/queues#synchronous-dispatching), які провалилися, у цій таблиці не зберігаються, а їхні винятки одразу обробляє застосунок.

Міграція для створення таблиці `failed_jobs` зазвичай уже є в нових застосунках Laravel. Проте, якщо у вашому застосунку її немає, створити міграцію можна командою `make:queue-failed-table`:

```shell
php artisan make:queue-failed-table

php artisan migrate
```

Запускаючи процес [воркера черги](#running-the-queue-worker), ви можете задати максимальну кількість спроб виконати завдання перемикачем `--tries` команди `queue:work`. Якщо ви не вкажете значення опції `--tries`, завдання виконуватимуться лише раз або стільки разів, скільки задано атрибутом `Tries` класу завдання:

```shell
php artisan queue:work redis --tries=3
```

Опцією `--backoff` ви можете вказати, скільки секунд Laravel має чекати перед повторною спробою виконати завдання, яке натрапило на виняток. За замовчуванням завдання одразу повертається до черги, щоб його спробували знову:

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

Якщо ви хочете налаштувати, скільки секунд Laravel має чекати перед повтором завдання, що натрапило на виняток, для кожного завдання окремо, скористайтеся атрибутом `Backoff` у класі завдання:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Якщо для визначення часу відступу завдання вам потрібна складніша логіка, опишіть у класі завдання метод `backoff`:

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 */
public function backoff(): int
{
    return 3;
}
```

Ви легко можете налаштувати «експоненційні» відступи, описавши масив значень. У цьому прикладі затримка перед повтором становитиме 1 секунду для першого повтору, 5 секунд для другого, 10 секунд для третього і 10 секунд для кожного наступного, якщо спроби ще лишилися:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff([1, 5, 10])]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### Прибирання після невдалих завдань

Коли конкретне завдання провалюється, вам може захотітися надіслати сповіщення користувачам або відкотити дії, які завдання виконало частково. Для цього опишіть у класі завдання метод `failed`. До методу `failed` буде передано екземпляр `Throwable`, який спричинив невдачу:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }

    /**
     * Handle a job failure.
     */
    public function failed(?Throwable $exception): void
    {
        // Send user notification of failure, etc...
    }
}
```

> [!WARNING]
> Перед викликом методу `failed` створюється новий екземпляр завдання; тому будь-які зміни властивостей класу, зроблені в методі `handle`, буде втрачено.

Невдале завдання - не обов'язково те, що натрапило на необроблений виняток. Завдання може вважатися невдалим і тоді, коли воно вичерпало всі дозволені спроби. Ці спроби можуть витрачатися кількома способами:

<div class="content-list" markdown="1">

- Завдання вичерпало таймаут.
- Завдання натрапило на необроблений виняток під час виконання.
- Завдання повернуто до черги вручну або middleware.

</div>

Якщо остання спроба провалилася через виняток, викинутий під час виконання завдання, цей виняток буде передано до методу `failed`. Проте, якщо завдання провалилося, бо досягло максимальної кількості дозволених спроб, `$exception` буде екземпляром `Illuminate\Queue\MaxAttemptsExceededException`. Так само, якщо завдання провалилося через перевищення налаштованого таймауту, `$exception` буде екземпляром `Illuminate\Queue\TimeoutExceededException`.

<a name="retrying-failed-jobs"></a>
### Повторний запуск невдалих завдань

Щоб переглянути всі невдалі завдання, які потрапили до таблиці `failed_jobs`, скористайтеся командою Artisan `queue:failed`:

```shell
php artisan queue:failed
```

Команда `queue:failed` виведе ID завдання, підключення, чергу, час невдачі та іншу інформацію. ID завдання дозволяє повторити невдале завдання. Наприклад, щоб повторити невдале завдання з ID `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`, виконайте таку команду:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

За потреби ви можете передати команді кілька ID:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

Ви також можете повторити всі невдалі завдання конкретної черги:

```shell
php artisan queue:retry --queue=name
```

Щоб повторити всі свої невдалі завдання, виконайте команду `queue:retry` і передайте `all` як ID:

```shell
php artisan queue:retry all
```

Якщо ви хочете видалити невдале завдання, скористайтеся командою `queue:forget`:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> Користуючись [Horizon](/docs/{{version}}/horizon), видаляйте невдалі завдання командою `horizon:forget`, а не `queue:forget`.

Щоб видалити всі свої невдалі завдання з таблиці `failed_jobs`, скористайтеся командою `queue:flush`:

```shell
php artisan queue:flush
```

Команда `queue:flush` вилучає з вашої черги всі записи невдалих завдань, незалежно від їхнього віку. Ви можете скористатися опцією `--hours`, щоб видалити лише завдання, які провалилися певну кількість годин тому чи раніше:

```shell
php artisan queue:flush --hours=48
```

<a name="ignoring-missing-models"></a>
### Ігнорування відсутніх моделей

Коли ви впроваджуєте модель Eloquent у завдання, вона автоматично серіалізується перед потраплянням у чергу й дістається з бази наново під час обробки завдання. Проте, якщо модель було видалено, доки завдання чекало на обробку воркером, ваше завдання може провалитися з `ModelNotFoundException`.

Для зручності ви можете автоматично видаляти завдання з відсутніми моделями за допомогою атрибута `DeleteWhenMissingModels` у класі завдання. Коли цей атрибут присутній, Laravel тихо відкине завдання, не викидаючи винятку:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\DeleteWhenMissingModels;

#[DeleteWhenMissingModels]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<a name="pruning-failed-jobs"></a>
### Очищення невдалих завдань

Ви можете очищати записи в таблиці `failed_jobs` вашого застосунку командою Artisan `queue:prune-failed`:

```shell
php artisan queue:prune-failed
```

За замовчуванням буде очищено всі записи невдалих завдань, старші за 24 години. Якщо ви передасте команді опцію `--hours`, буде збережено лише записи невдалих завдань, вставлені за останні N годин. Наприклад, команда нижче видалить усі записи невдалих завдань, вставлені понад 48 годин тому:

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### Зберігання невдалих завдань у DynamoDB

Laravel також підтримує зберігання записів невдалих завдань у [DynamoDB](https://aws.amazon.com/dynamodb) замість таблиці реляційної бази даних. Проте вам доведеться вручну створити таблицю DynamoDB для зберігання всіх записів невдалих завдань. Зазвичай цю таблицю називають `failed_jobs`, але вам слід назвати її відповідно до значення конфігурації `queue.failed.table` у файлі конфігурації `queue` вашого застосунку.

Таблиця `failed_jobs` має мати рядковий первинний ключ розділу `application` і рядковий первинний ключ сортування `uuid`. Частина ключа `application` міститиме назву вашого застосунку, задану значенням конфігурації `name` у файлі конфігурації `app`. Оскільки назва застосунку є частиною ключа таблиці DynamoDB, ви можете зберігати в одній таблиці невдалі завдання кількох застосунків Laravel.

Крім того, встановіть AWS SDK, щоб ваш застосунок Laravel міг спілкуватися з Amazon DynamoDB:

```shell
composer require aws/aws-sdk-php
```

Далі задайте опції конфігурації `queue.failed.driver` значення `dynamodb`. Крім того, опишіть у масиві конфігурації невдалих завдань опції `key`, `secret` та `region`. Вони використовуватимуться для автентифікації в AWS. Коли ви користуєтеся драйвером `dynamodb`, опція конфігурації `queue.failed.database` не потрібна:

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

<a name="disabling-failed-job-storage"></a>
### Вимкнення зберігання невдалих завдань

Ви можете сказати Laravel відкидати невдалі завдання, не зберігаючи їх, задавши опції конфігурації `queue.failed.driver` значення `null`. Зазвичай це роблять через змінну середовища `QUEUE_FAILED_DRIVER`:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### Події невдалих завдань

Якщо ви хочете зареєструвати слухача події, який буде викликано, коли завдання провалюється, скористайтеся методом `failing` фасаду `Queue`. Наприклад, ми можемо причепити до цієї події замикання в методі `boot` класу `AppServiceProvider`, який входить до Laravel:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

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
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>
## Очищення черг від завдань

> [!NOTE]
> Користуючись [Horizon](/docs/{{version}}/horizon), очищайте чергу від завдань командою `horizon:clear`, а не `queue:clear`.

Якщо ви хочете видалити всі завдання з черги за замовчуванням підключення за замовчуванням, скористайтеся командою Artisan `queue:clear`:

```shell
php artisan queue:clear
```

Ви також можете передати аргумент `connection` та опцію `queue`, щоб видалити завдання з конкретного підключення й черги:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> Очищення черг від завдань доступне лише для драйверів черг SQS, Redis і database. Крім того, процес видалення повідомлень у SQS триває до 60 секунд, тож завдання, надіслані до черги SQS протягом 60 секунд після очищення, теж можуть бути видалені.

<a name="monitoring-your-queues"></a>
## Моніторинг черг

Якщо ваша черга раптово отримує напливи завдань, вона може перевантажитися, і завдання довго чекатимуть на завершення. За бажанням Laravel може сповіщати вас, коли кількість завдань у черзі перевищує заданий поріг.

Для початку заплануйте [щохвилинне виконання](/docs/{{version}}/scheduling) команди `queue:monitor`. Команда приймає назви черг, за якими ви хочете стежити, а також бажаний поріг кількості завдань:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

Самого лише планування цієї команди недостатньо, щоб отримати сповіщення про перевантаження черги. Коли команда натрапляє на чергу, кількість завдань у якій перевищує ваш поріг, буде диспетчеризовано подію `Illuminate\Queue\Events\QueueBusy`. Ви можете слухати цю подію у своєму `AppServiceProvider`, щоб надіслати сповіщення собі чи своїй команді розробників:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (QueueBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new QueueHasLongWaitTime(
                $event->connectionName,
                $event->queue,
                $event->size
            ));
    });
}
```

<a name="testing"></a>
## Тестування

Тестуючи код, який диспетчеризує завдання, ви можете захотіти сказати Laravel не виконувати самого завдання, адже його код можна протестувати напряму й окремо від коду, який його диспетчеризує. Звісно, щоб протестувати саме завдання, ви можете створити його екземпляр і викликати метод `handle` напряму у своєму тесті.

Метод `fake` фасаду `Queue` дозволяє завадити реальному потраплянню завдань у чергу. Після виклику методу `fake` фасаду `Queue` ви можете перевіряти, що застосунок намагався покласти завдання в чергу:

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed
    Queue::assertPushed(ShipOrder::class);

    // Assert a job was pushed exactly once...
    Queue::assertPushedOnce(ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert that a closure was not pushed...
    Queue::assertClosureNotPushed();

    // Assert the total number of jobs that were pushed...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Queue::fake();

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed
        Queue::assertPushed(ShipOrder::class);

        // Assert a job was pushed exactly once...
        Queue::assertPushedOnce(ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushedTimes(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert that a closure was not pushed...
        Queue::assertClosureNotPushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

Ви можете передати замикання методам `assertPushed`, `assertNotPushed`, `assertClosurePushed` чи `assertClosureNotPushed`, щоб перевірити, що покладено завдання, яке проходить заданий тест. Якщо покладено щонайменше одне завдання, яке проходить цей тест, перевірка буде успішною:

```php
use Illuminate\Queue\CallQueuedClosure;

Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});

Queue::assertClosurePushed(function (CallQueuedClosure $job) {
    return $job->name === 'validate-order';
});
```

<a name="faking-a-subset-of-jobs"></a>
### Підміна частини завдань

Якщо вам потрібно підмінити лише конкретні завдання, дозволивши іншим виконуватися як зазвичай, передайте методу `fake` назви класів завдань, які слід підмінити:

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);
}
```

Ви можете підмінити всі завдання, окрім заданого набору, методом `except`:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### Тестування ланцюжків завдань

Щоб тестувати ланцюжки завдань, вам знадобляться можливості підміни фасаду `Bus`. Метод `assertChained` фасаду `Bus` дозволяє перевірити, що [ланцюжок завдань](/docs/{{version}}/queues#job-chaining) було диспетчеризовано. Метод `assertChained` приймає першим аргументом масив завдань ланцюжка:

```php
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```

Як бачите в прикладі вище, масив завдань ланцюжка може бути масивом назв класів. Проте ви можете передати й масив справжніх екземплярів завдань. У такому разі Laravel переконається, що екземпляри належать до тих самих класів і мають ті самі значення властивостей, що й завдання ланцюжка, диспетчеризовані вашим застосунком:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

Метод `assertDispatchedWithoutChain` дозволяє перевірити, що завдання покладено без ланцюжка:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### Тестування змін ланцюжка

Якщо завдання ланцюжка [додає завдання на початок чи в кінець наявного ланцюжка](#adding-jobs-to-the-chain), скористайтеся методом завдання `assertHasChain`, щоб перевірити, що воно має очікуваний ланцюжок решти завдань:

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

Метод `assertDoesntHaveChain` дозволяє перевірити, що решта ланцюжка завдання порожня:

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### Тестування пакетів у ланцюжку

Якщо ваш ланцюжок завдань [містить пакет завдань](#chains-and-batches), ви можете перевірити, що цей пакет відповідає вашим очікуванням, вставивши опис `Bus::chainedBatch` у свою перевірку ланцюжка:

```php
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    new ShipOrder,
    Bus::chainedBatch(function (PendingBatch $batch) {
        return $batch->jobs->count() === 3;
    }),
    new UpdateInventory,
]);
```

<a name="testing-job-batches"></a>
### Тестування пакетів завдань

Метод `assertBatched` фасаду `Bus` дозволяє перевірити, що [пакет завдань](/docs/{{version}}/queues#job-batching) було диспетчеризовано. Замикання, передане методу `assertBatched`, отримує екземпляр `Illuminate\Bus\PendingBatch`, який дозволяє оглянути завдання в пакеті:

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'Import CSV' &&
           $batch->jobs->count() === 10;
});
```

Метод `hasJobs` на відкладеному пакеті дозволяє перевірити, що пакет містить очікувані завдання. Метод приймає масив екземплярів завдань, назв класів чи замикань:

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        new ProcessCsvRow(row: 1),
        new ProcessCsvRow(row: 2),
        new ProcessCsvRow(row: 3),
    ]);
});
```

Коли ви користуєтеся замиканнями, замикання отримає екземпляр завдання. Очікуваний тип завдання буде виведено з типу в сигнатурі замикання:

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        fn (ProcessCsvRow $job) => $job->row === 1,
        fn (ProcessCsvRow $job) => $job->row === 2,
        fn (ProcessCsvRow $job) => $job->row === 3,
    ]);
});
```

Метод `assertBatchCount` дозволяє перевірити, що диспетчеризовано задану кількість пакетів:

```php
Bus::assertBatchCount(3);
```

Метод `assertNothingBatched` дозволяє перевірити, що жодного пакета не диспетчеризовано:

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### Тестування взаємодії завдання з пакетом

Крім того, вам інколи може знадобитися протестувати взаємодію окремого завдання з його пакетом. Наприклад, вам може знадобитися перевірити, чи скасувало завдання подальшу обробку свого пакета. Для цього призначте завданню фейковий пакет методом `withFakeBatch`. Метод `withFakeBatch` повертає кортеж з екземпляра завдання й фейкового пакета:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### Тестування взаємодії завдання з чергою

Інколи вам може знадобитися перевірити, що завдання в черзі [повертає себе до черги](#manually-releasing-a-job). Або що завдання видалило себе. Ви можете протестувати ці взаємодії, створивши екземпляр завдання й викликавши метод `withFakeQueueInteractions`.

Щойно взаємодії завдання з чергою підмінено, ви можете викликати на завданні метод `handle`. Після виклику завдання вам доступні різні методи перевірок, щоб пересвідчитися у взаємодіях завдання з чергою:

```php
use App\Exceptions\CorruptedAudioException;
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
$job->assertDeleted();
$job->assertNotDeleted();
$job->assertFailed();
$job->assertFailedWith(CorruptedAudioException::class);
$job->assertNotFailed();
```

<a name="job-events"></a>
## Події завдань

Методами `before` та `after` [фасаду](/docs/{{version}}/facades) `Queue` ви можете задати колбеки, які виконуватимуться до чи після обробки завдання з черги. Ці колбеки - чудова нагода додатково логувати чи збільшувати лічильники для панелі. Зазвичай ці методи викликають у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers). Наприклад, ми можемо скористатися `AppServiceProvider`, який входить до Laravel:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

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
        Queue::before(function (JobProcessing $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });

        Queue::after(function (JobProcessed $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });
    }
}
```

Методом `looping` [фасаду](/docs/{{version}}/facades) `Queue` ви можете задати колбеки, які виконуються, перш ніж воркер спробує взяти завдання з черги. Наприклад, ви можете зареєструвати замикання, яке відкочує транзакції, залишені відкритими попереднім невдалим завданням:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```

Laravel також диспетчеризує подію `Illuminate\Queue\Events\WorkerIdle`, коли воркер черги не може дістати завдання з черги:

```php
use Illuminate\Queue\Events\WorkerIdle;
use Illuminate\Support\Facades\Event;

Event::listen(function (WorkerIdle $event) {
    // $event->connectionName
    // $event->queue
    // $event->workerOptions
});
```
