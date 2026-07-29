---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# HTTP-клієнт

- [Вступ](#introduction)
- [Виконання запитів](#making-requests)
    - [Дані запиту](#request-data)
    - [Заголовки](#headers)
    - [Автентифікація](#authentication)
    - [Таймаут](#timeout)
    - [Повторні спроби](#retries)
    - [Обробка помилок](#error-handling)
    - [Middleware Guzzle](#guzzle-middleware)
    - [Опції Guzzle](#guzzle-options)
- [Паралельні запити](#concurrent-requests)
    - [Пул запитів](#request-pooling)
    - [Пакети запитів](#request-batching)
- [Макроси](#macros)
- [Тестування](#testing)
    - [Підміна відповідей](#faking-responses)
    - [Огляд запитів](#inspecting-requests)
    - [Запобігання «блукаючим» запитам](#preventing-stray-requests)
- [Події](#events)

<a name="introduction"></a>
## Вступ

Laravel надає виразний мінімалістичний API навколо [HTTP-клієнта Guzzle](http://docs.guzzlephp.org/en/stable/), який дозволяє швидко виконувати вихідні HTTP-запити для спілкування з іншими вебзастосунками. Обгортка Laravel навколо Guzzle зосереджена на найпоширеніших сценаріях і чудовому досвіді розробника.

<a name="making-requests"></a>
## Виконання запитів

Щоб виконувати запити, скористайтеся методами `head`, `get`, `post`, `put`, `patch` та `delete` фасаду `Http`. Спершу розгляньмо, як виконати простий `GET`-запит на іншу URL-адресу:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

Метод `get` повертає екземпляр `Illuminate\Http\Client\Response`, який надає низку методів для огляду відповіді:

```php
$response->body() : string;
$response->json($key = null, $default = null, $flags = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

Об'єкт `Illuminate\Http\Client\Response` також реалізує PHP-інтерфейс `ArrayAccess`, тож ви можете звертатися до даних JSON-відповіді безпосередньо на відповіді:

```php
return Http::get('http://example.com/users/1')['name'];
```

Окрім перелічених вище методів відповіді, наступні методи дозволяють визначити, чи має відповідь конкретний статус-код:

```php
$response->ok() : bool;                  // 200 OK
$response->created() : bool;             // 201 Created
$response->accepted() : bool;            // 202 Accepted
$response->noContent() : bool;           // 204 No Content
$response->movedPermanently() : bool;    // 301 Moved Permanently
$response->found() : bool;               // 302 Found
$response->badRequest() : bool;          // 400 Bad Request
$response->unauthorized() : bool;        // 401 Unauthorized
$response->paymentRequired() : bool;     // 402 Payment Required
$response->forbidden() : bool;           // 403 Forbidden
$response->notFound() : bool;            // 404 Not Found
$response->requestTimeout() : bool;      // 408 Request Timeout
$response->conflict() : bool;            // 409 Conflict
$response->unprocessableEntity() : bool; // 422 Unprocessable Entity
$response->tooManyRequests() : bool;     // 429 Too Many Requests
$response->serverError() : bool;         // 500 Internal Server Error
```

<a name="uri-templates"></a>
#### Шаблони URI

HTTP-клієнт також дозволяє будувати URL запитів за [специфікацією шаблонів URI](https://www.rfc-editor.org/rfc/rfc6570). Щоб описати параметри URL, які може розгорнути ваш шаблон URI, скористайтеся методом `withUrlParameters`:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '13.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### Виведення запитів

Якщо ви хочете вивести екземпляр вихідного запиту перед надсиланням і припинити виконання скрипта, додайте метод `dd` на початок опису запиту:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### Дані запиту

Звісно, під час запитів `POST`, `PUT` і `PATCH` часто потрібно надсилати додаткові дані, тому ці методи приймають другим аргументом масив даних. За замовчуванням дані надсилаються з типом вмісту `application/json`:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### Параметри запиту в GET-запитах

Виконуючи `GET`-запити, ви можете або додати рядок запиту до URL напряму, або передати масив пар ключ / значення другим аргументом методу `get`:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

Як варіант, можна скористатися методом `withQueryParameters`:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### Надсилання запитів у форматі form URL encoded

Якщо ви хочете надіслати дані з типом вмісту `application/x-www-form-urlencoded`, викличте перед запитом метод `asForm`:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Надсилання сирого тіла запиту

Якщо під час запиту ви хочете передати сире тіло, скористайтеся методом `withBody`. Тип вмісту можна передати другим аргументом методу:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### Multi-part запити

Якщо ви хочете надсилати файли як multi-part запити, викличте перед запитом метод `attach`. Цей метод приймає ім'я файлу та його вміст. За потреби ви можете передати третій аргумент, який стане ім'ям файлу, а четвертим аргументом - заголовки, пов'язані з файлом:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

Замість сирого вмісту файлу ви можете передати потоковий ресурс:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### Заголовки

Заголовки до запитів додаються методом `withHeaders`. Метод `withHeaders` приймає масив пар ключ / значення:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

Метод `accept` дозволяє вказати тип вмісту, який ваш застосунок очікує у відповідь на запит:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

Для зручності методом `acceptJson` можна швидко вказати, що ваш застосунок очікує у відповідь тип вмісту `application/json`:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

Метод `withHeaders` зливає нові заголовки з наявними заголовками запиту. За потреби ви можете повністю замінити всі заголовки методом `replaceHeaders`:

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<a name="authentication"></a>
### Автентифікація

Облікові дані для basic- і digest-автентифікації можна вказати методами `withBasicAuth` та `withDigestAuth` відповідно:

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer-токени

Якщо ви хочете швидко додати bearer-токен до заголовка `Authorization` запиту, скористайтеся методом `withToken`:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### Таймаут

Метод `timeout` дозволяє вказати максимальну кількість секунд очікування відповіді. За замовчуванням HTTP-клієнт завершиться таймаутом за 30 секунд:

```php
$response = Http::timeout(3)->get(/* ... */);
```

Якщо заданий таймаут перевищено, буде викинуто екземпляр `Illuminate\Http\Client\ConnectionException`.

Максимальну кількість секунд очікування під час спроби підключитися до сервера можна вказати методом `connectTimeout`. За замовчуванням це 10 секунд:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### Повторні спроби

Якщо ви хочете, щоб HTTP-клієнт автоматично повторював запит у разі клієнтської чи серверної помилки, скористайтеся методом `retry`. Метод `retry` приймає максимальну кількість спроб виконати запит і кількість мілісекунд, які Laravel має чекати між спробами:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

Якщо ви хочете вручну обчислювати кількість мілісекунд паузи між спробами, передайте другим аргументом методу `retry` замикання:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

Для зручності ви також можете передати першим аргументом методу `retry` масив. За цим масивом визначатиметься, скільки мілісекунд чекати між наступними спробами:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

За потреби ви можете передати методу `retry` третій аргумент. Ним має бути щось викликаєме, що визначає, чи справді слід робити повторні спроби. Наприклад, ви можете хотіти повторювати запит, лише якщо початковий запит натрапив на `ConnectionException`:

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

Якщо спроба запиту провалилася, ви можете захотіти щось змінити в запиті перед новою спробою. Це робиться зміною аргументу запиту, переданого до того викликаємого, яке ви передали методу `retry`. Наприклад, ви можете захотіти повторити запит з новим токеном авторизації, якщо перша спроба повернула помилку автентифікації:

```php
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;
use Throwable;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Throwable $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

Якщо всі запити провалилися, буде викинуто екземпляр `Illuminate\Http\Client\RequestException`. Якщо ви хочете вимкнути цю поведінку, передайте аргумент `throw` зі значенням `false`. Коли її вимкнено, після всіх спроб буде повернуто останню отриману клієнтом відповідь:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> Якщо всі запити провалилися через проблему зі з'єднанням, `Illuminate\Http\Client\ConnectionException` буде викинуто навіть тоді, коли аргумент `throw` має значення `false`.

<a name="error-handling"></a>
### Обробка помилок

На відміну від типової поведінки Guzzle, обгортка HTTP-клієнта Laravel не викидає винятків на клієнтських чи серверних помилках (відповіді серверів рівня `400` та `500`). Визначити, чи повернуто одну з таких помилок, можна методами `successful`, `clientError` або `serverError`:

```php
// Determine if the status code is >= 200 and < 300...
$response->successful();

// Determine if the status code is >= 400...
$response->failed();

// Determine if the response has a 400 level status code...
$response->clientError();

// Determine if the response has a 500 level status code...
$response->serverError();

// Immediately execute the given callback if there was a client or server error...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### Викидання винятків

Якщо ви маєте екземпляр відповіді й хочете викинути екземпляр `Illuminate\Http\Client\RequestException`, коли статус-код відповіді вказує на клієнтську чи серверну помилку, скористайтеся методами `throw` або `throwIf`:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

// Throw an exception if an error occurred and the given closure resolves to true...
$response->throwIf(fn (Response $response) => true);

// Throw an exception if an error occurred and the given condition is false...
$response->throwUnless($condition);

// Throw an exception if an error occurred and the given closure resolves to false...
$response->throwUnless(fn (Response $response) => false);

// Throw an exception if the response has a specific status code...
$response->throwIfStatus(403);

// Throw an exception unless the response has a specific status code...
$response->throwUnlessStatus(200);

// Throw an exception if a server error occurred (status >500)...
$response->throwIfServerError();

// Throw an exception if a client error occurred (status >400 and <500)...
$response->throwIfClientError();

return $response['user']['id'];
```

Екземпляр `Illuminate\Http\Client\RequestException` має публічну властивість `$response`, яка дозволяє оглянути повернену відповідь.

Метод `throw` повертає екземпляр відповіді, якщо помилки не сталося, тож ви можете додавати до нього ланцюжком інші операції:

```php
return Http::post(/* ... */)->throw()->json();
```

Якщо ви хочете виконати додаткову логіку перед викиданням винятку, передайте методу `throw` замикання. Виняток буде викинуто автоматично після виклику замикання, тож перевикидати його всередині замикання не потрібно:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

За замовчуванням повідомлення `RequestException` обрізаються до 120 символів під час логування чи повідомлення. Щоб змінити чи вимкнути цю поведінку, скористайтеся методами `truncateAt` і `dontTruncate`, налаштовуючи зареєстровану поведінку застосунку у файлі `bootstrap/app.php`:

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```

Як варіант, ви можете налаштувати обрізання винятків для окремого запиту методом `truncateExceptionsAt`:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Middleware Guzzle

Оскільки HTTP-клієнт Laravel працює на Guzzle, ви можете скористатися [middleware Guzzle](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html), щоб змінювати вихідний запит або оглядати вхідну відповідь. Щоб змінювати вихідний запит, зареєструйте middleware Guzzle методом `withRequestMiddleware`:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

Так само ви можете оглядати вхідну HTTP-відповідь, зареєструвавши middleware методом `withResponseMiddleware`:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```

<a name="global-middleware"></a>
#### Глобальні middleware

Інколи вам може захотітися зареєструвати middleware, який застосовується до кожного вихідного запиту й вхідної відповіді. Для цього скористайтеся методами `globalRequestMiddleware` та `globalResponseMiddleware`. Зазвичай ці методи викликають у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a name="guzzle-options"></a>
### Опції Guzzle

Ви можете вказати додаткові [опції запиту Guzzle](http://docs.guzzlephp.org/en/stable/request-options.html) для вихідного запиту методом `withOptions`. Метод `withOptions` приймає масив пар ключ / значення:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### Глобальні опції

Щоб налаштувати опції за замовчуванням для кожного вихідного запиту, скористайтеся методом `globalOptions`. Зазвичай цей метод викликають у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a name="concurrent-requests"></a>
## Паралельні запити

Інколи вам може захотітися виконати кілька HTTP-запитів паралельно. Іншими словами, ви хочете відправити кілька запитів одночасно, а не послідовно. Це може суттєво пришвидшити роботу з повільними HTTP-API.

<a name="request-pooling"></a>
### Пул запитів

На щастя, це можна зробити методом `pool`. Метод `pool` приймає замикання, яке отримує екземпляр `Illuminate\Http\Client\Pool`, - і ви легко додаєте запити до пулу на відправлення:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->get('http://localhost/first'),
    $pool->get('http://localhost/second'),
    $pool->get('http://localhost/third'),
]);

return $responses[0]->ok() &&
       $responses[1]->ok() &&
       $responses[2]->ok();
```

Як бачите, до кожного екземпляра відповіді можна звернутися за порядком, у якому його додано до пулу. За бажанням ви можете назвати запити методом `as`, і тоді звертатися до відповідних відповідей за іменем:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

Максимальною паралельністю пулу запитів можна керувати, передавши методу `pool` аргумент `concurrency`. Це значення визначає максимальну кількість HTTP-запитів, які можуть одночасно виконуватися під час обробки пулу:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### Налаштування паралельних запитів

Метод `pool` не можна поєднувати ланцюжком з іншими методами HTTP-клієнта на кшталт `withHeaders` чи `middleware`. Якщо ви хочете застосувати власні заголовки чи middleware до запитів у пулі, налаштуйте ці опції на кожному запиті пулу:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```

<a name="request-batching"></a>
### Пакети запитів

Ще один спосіб працювати з паралельними запитами в Laravel - метод `batch`. Як і метод `pool`, він приймає замикання, яке отримує екземпляр `Illuminate\Http\Client\Batch`, - і ви легко додаєте запити до пулу на відправлення, але при цьому можете описати колбеки завершення:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // The batch has been created but no requests have been initialized...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // An individual request has completed successfully...
})->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // Batch request failure detected...
})->finally(function (Batch $batch, array $results) {
    // The batch has finished executing...
})->send();
```

Як і з методом `pool`, ви можете скористатися методом `as`, щоб назвати свої запити:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

Щойно пакет запущено викликом методу `send`, додавати до нього нові запити не можна. Спроба зробити це призведе до викидання винятку `Illuminate\Http\Client\BatchInProgressException`.

Максимальною паралельністю пакета запитів можна керувати методом `concurrency`. Це значення визначає максимальну кількість HTTP-запитів, які можуть одночасно виконуватися під час обробки пакета:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### Огляд пакетів

Екземпляр `Illuminate\Http\Client\Batch`, який передається до колбеків завершення пакета, має низку властивостей і методів, що допомагають працювати з пакетом запитів і оглядати його:

```php
// The number of requests assigned to the batch...
$batch->totalRequests;
 
// The number of requests that have not been processed yet...
$batch->pendingRequests;
 
// The number of requests that have failed...
$batch->failedRequests;

// The number of requests that have been processed thus far...
$batch->processedRequests();

// Indicates if the batch has finished executing...
$batch->finished();

// Indicates if the batch has request failures...
$batch->hasFailures();
```
<a name="deferring-batches"></a>
#### Відкладення пакетів

Коли викликано метод `defer`, пакет запитів не виконується негайно. Натомість Laravel виконає пакет після того, як HTTP-відповідь на поточний запит застосунку вже надіслано користувачеві, - і застосунок і далі здається швидким та чуйним:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->defer();
```

<a name="macros"></a>
## Макроси

HTTP-клієнт Laravel дозволяє описувати «макроси», які можуть слугувати плавним і виразним механізмом налаштування типових шляхів і заголовків запитів під час роботи із сервісами у вашому застосунку. Для початку опишіть макрос у методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

Щойно ваш макрос налаштовано, ви можете викликати його звідусіль у застосунку, щоб створити відкладений запит із вказаною конфігурацією:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## Тестування

Багато сервісів Laravel надають можливості, які допомагають легко й виразно писати тести, і HTTP-клієнт Laravel не виняток. Метод `fake` фасаду `Http` дозволяє сказати HTTP-клієнту повертати підставні / фіктивні відповіді на запити.

<a name="faking-responses"></a>
### Підміна відповідей

Наприклад, щоб HTTP-клієнт повертав порожні відповіді зі статус-кодом `200` на кожен запит, викличте метод `fake` без аргументів:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### Підміна конкретних URL

Як варіант, ви можете передати методу `fake` масив. Ключі масиву мають бути шаблонами URL, які ви хочете підмінити, а значення - відповідними відповідями. Символ `*` можна використовувати як підстановку. Щоб побудувати підставні / фейкові відповіді для цих точок, скористайтеся методом `response` фасаду `Http`:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

Будь-які запити на URL, які не підмінено, буде виконано насправді. Якщо ви хочете задати запасний шаблон URL, який підмінить усі неспівпалі URL, скористайтеся єдиним символом `*`:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

Для зручності прості рядкові, JSON- та порожні відповіді можна згенерувати, передавши як відповідь рядок, масив чи ціле число:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### Підміна винятків

Інколи вам може знадобитися перевірити поведінку застосунку, коли HTTP-клієнт натрапляє на `Illuminate\Http\Client\ConnectionException` під час спроби виконати запит. Ви можете сказати HTTP-клієнту викинути виняток з'єднання методом `failedConnection`:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

Щоб перевірити поведінку застосунку, коли викинуто `Illuminate\Http\Client\RequestException`, скористайтеся методом `failedRequest`:

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### Підміна послідовностей відповідей

Інколи вам може знадобитися вказати, що один URL має повертати серію фейкових відповідей у певному порядку. Це робиться методом `Http::sequence`, яким будують відповіді:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

Коли всі відповіді в послідовності спожито, будь-які наступні запити змусять послідовність викинути виняток. Якщо ви хочете задати відповідь за замовчуванням, яку слід повертати, коли послідовність порожня, скористайтеся методом `whenEmpty`:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

Якщо ви хочете підмінити послідовність відповідей, але вам не потрібно вказувати конкретний шаблон URL, скористайтеся методом `Http::fakeSequence`:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### Колбек підміни

Якщо вам потрібна складніша логіка, щоб визначити, які відповіді повертати для певних точок, передайте методу `fake` замикання. Це замикання отримає екземпляр `Illuminate\Http\Client\Request` і має повернути екземпляр відповіді. Усередині замикання ви можете виконати будь-яку логіку, потрібну, щоб визначити, який тип відповіді повернути:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### Огляд запитів

Підміняючи відповіді, ви інколи можете захотіти оглянути запити, які отримує клієнт, аби переконатися, що ваш застосунок надсилає правильні дані чи заголовки. Це робиться викликом методу `Http::assertSent` після виклику `Http::fake`.

Метод `assertSent` приймає замикання, яке отримає екземпляр `Illuminate\Http\Client\Request` і має повернути булеве значення, що вказує, чи відповідає запит вашим очікуванням. Щоб тест пройшов, має бути виконано щонайменше один запит, який відповідає заданим очікуванням:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::withHeaders([
    'X-First' => 'foo',
])->post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertSent(function (Request $request) {
    return $request->hasHeader('X-First', 'foo') &&
           $request->url() == 'http://example.com/users' &&
           $request['name'] == 'Taylor' &&
           $request['role'] == 'Developer';
});
```

За потреби ви можете перевірити, що конкретного запиту не було надіслано, методом `assertNotSent`:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```

Метод `assertSentCount` дозволяє перевірити, скільки запитів було «надіслано» під час тесту:

```php
Http::fake();

Http::assertSentCount(5);
```

Або ж метод `assertNothingSent` дозволяє перевірити, що під час тесту не було надіслано жодного запиту:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### Запис запитів / відповідей

Метод `recorded` дозволяє зібрати всі запити та відповідні їм відповіді. Метод `recorded` повертає колекцію масивів, що містять екземпляри `Illuminate\Http\Client\Request` та `Illuminate\Http\Client\Response`:

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```

Крім того, метод `recorded` приймає замикання, яке отримає екземпляри `Illuminate\Http\Client\Request` та `Illuminate\Http\Client\Response` і дозволяє відфільтрувати пари запит / відповідь за вашими очікуваннями:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```

<a name="preventing-stray-requests"></a>
### Запобігання «блукаючим» запитам

Якщо ви хочете переконатися, що всі запити, надіслані через HTTP-клієнт, підмінено в окремому тесті чи в усьому наборі тестів, викличте метод `preventStrayRequests`. Після виклику цього методу будь-які запити, для яких немає відповідної фейкової відповіді, викидатимуть виняток замість того, щоб виконувати справжній HTTP-запит:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// An "ok" response is returned...
Http::get('https://github.com/laravel/framework');

// An exception is thrown...
Http::get('https://laravel.com');
```

Інколи вам може захотітися заблокувати більшість блукаючих запитів, але дозволити виконання певних. Для цього передайте масив шаблонів URL методу `allowStrayRequests`. Будь-який запит, що відповідає одному із заданих шаблонів, буде дозволено, а всі інші й далі викидатимуть виняток:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// This request is executed...
Http::get('http://127.0.0.1:5000/generate');

// An exception is thrown...
Http::get('https://laravel.com');
```

<a name="events"></a>
## Події

Під час надсилання HTTP-запитів Laravel запускає три події. Подія `RequestSending` запускається перед надсиланням запиту, а подія `ResponseReceived` - після отримання відповіді на запит. Подія `ConnectionFailed` запускається, якщо відповіді на запит не отримано.

Події `RequestSending` та `ConnectionFailed` містять публічну властивість `$request`, яка дозволяє оглянути екземпляр `Illuminate\Http\Client\Request`. Так само подія `ResponseReceived` містить властивість `$request`, а також властивість `$response`, яка дозволяє оглянути екземпляр `Illuminate\Http\Client\Response`. Ви можете створити [слухачів подій](/docs/{{version}}/events) для цих подій у своєму застосунку:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
