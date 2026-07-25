---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# HTTP-відповіді

- [Створення відповідей](#creating-responses)
    - [Додавання заголовків до відповідей](#attaching-headers-to-responses)
    - [Додавання cookie до відповідей](#attaching-cookies-to-responses)
    - [Cookie та шифрування](#cookies-and-encryption)
- [Перенаправлення](#redirects)
    - [Перенаправлення до іменованих маршрутів](#redirecting-named-routes)
    - [Перенаправлення до дій контролерів](#redirecting-controller-actions)
    - [Перенаправлення до зовнішніх доменів](#redirecting-external-domains)
    - [Перенаправлення з флеш-даними сесії](#redirecting-with-flashed-session-data)
- [Інші типи відповідей](#other-response-types)
    - [Відповіді-представлення](#view-responses)
    - [JSON-відповіді](#json-responses)
    - [Завантаження файлів](#file-downloads)
    - [Файлові відповіді](#file-responses)
- [Потокові відповіді](#streamed-responses)
    - [Споживання потокових відповідей](#consuming-streamed-responses)
    - [Потокові JSON-відповіді](#streamed-json-responses)
    - [Потоки подій (SSE)](#event-streams)
    - [Потокові завантаження](#streamed-downloads)
- [Макроси відповідей](#response-macros)

<a name="creating-responses"></a>
## Створення відповідей

<a name="strings-arrays"></a>
#### Рядки та масиви

Усі маршрути й контролери мають повертати відповідь, яку буде надіслано до браузера користувача. Laravel пропонує кілька різних способів повертати відповіді. Найпростіша відповідь - це рядок, повернений із маршруту чи контролера. Фреймворк автоматично перетворить його на повноцінну HTTP-відповідь:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

Окрім рядків, ви можете повертати з маршрутів і контролерів масиви. Фреймворк автоматично перетворить масив на JSON-відповідь:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> А ви знали, що з маршрутів чи контролерів можна також повертати [колекції Eloquent](/docs/{{version}}/eloquent-collections)? Вони автоматично перетворяться на JSON. Спробуйте!

<a name="response-objects"></a>
#### Об'єкти відповідей

Зазвичай ви не повертатимете з дій маршрутів лише прості рядки чи масиви. Натомість ви повертатимете повноцінні екземпляри `Illuminate\Http\Response` або [представлення](/docs/{{version}}/views).

Повернення повного екземпляра `Response` дозволяє налаштувати HTTP-статус і заголовки відповіді. Екземпляр `Response` успадковує клас `Symfony\Component\HttpFoundation\Response`, що надає різноманітні методи для побудови HTTP-відповідей:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Моделі та колекції Eloquent

Ви також можете повертати моделі й колекції [Eloquent ORM](/docs/{{version}}/eloquent) безпосередньо з маршрутів і контролерів. Тоді Laravel автоматично перетворить їх на JSON-відповіді, враховуючи [приховані атрибути](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) моделі:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### Додавання заголовків до відповідей

Пам'ятайте, що більшість методів відповіді можна об'єднувати в ланцюжок, що дозволяє плинно будувати екземпляри відповідей. Наприклад, метод `header` дозволяє додати до відповіді низку заголовків перед надсиланням її користувачеві:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

Або ж скористайтеся методом `withHeaders`, щоб указати масив заголовків, які слід додати до відповіді:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

Ви можете вилучити конкретні заголовки з вихідної відповіді методом `withoutHeader`:

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
#### Middleware керування кешем

Laravel містить `middleware` `cache.headers`, який дозволяє швидко задати заголовок `Cache-Control` для групи маршрутів. Директиви слід передавати у вигляді «snake case» відповідної директиви cache-control, розділяючи їх крапкою з комою. Якщо в списку директив указано `etag`, як ідентифікатор ETag автоматично буде встановлено MD5-хеш вмісту відповіді:

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
### Додавання cookie до відповідей

Ви можете додати cookie до вихідного екземпляра `Illuminate\Http\Response` методом `cookie`. Передайте цьому методу ім'я, значення та кількість хвилин, протягом яких cookie вважатиметься дійсною:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

Метод `cookie` приймає ще кілька аргументів, які використовують рідше. Загалом вони мають те саме призначення й значення, що й аргументи нативного PHP-методу [setcookie](https://secure.php.net/manual/en/function.setcookie.php):

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

Якщо ви хочете гарантувати, що cookie буде надіслано з вихідною відповіддю, але ще не маєте екземпляра цієї відповіді, скористайтеся фасадом `Cookie`, щоб поставити cookie в «чергу» на прикріплення до відповіді під час надсилання. Метод `queue` приймає аргументи, потрібні для створення екземпляра cookie. Ці cookie буде прикріплено до вихідної відповіді перед надсиланням її до браузера:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### Створення екземплярів cookie

Якщо ви хочете створити екземпляр `Symfony\Component\HttpFoundation\Cookie`, який згодом можна буде прикріпити до екземпляра відповіді, скористайтеся глобальним хелпером `cookie`. Ця cookie не буде надіслана клієнту, доки її не прикріплено до екземпляра відповіді:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### Дострокове завершення дії cookie

Ви можете вилучити cookie, завершивши її дію методом `withoutCookie` вихідної відповіді:

```php
return response('Hello World')->withoutCookie('name');
```

Якщо ви ще не маєте екземпляра вихідної відповіді, скористайтеся методом `expire` фасаду `Cookie`:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### Cookie та шифрування

За замовчуванням, завдяки `middleware` `Illuminate\Cookie\Middleware\EncryptCookies`, усі cookie, згенеровані Laravel, шифруються й підписуються, тож клієнт не може їх змінити чи прочитати. Якщо ви хочете вимкнути шифрування для частини cookie вашого застосунку, скористайтеся методом `encryptCookies` у файлі `bootstrap/app.php`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> Загалом шифрування cookie ніколи не слід вимикати, адже це наражає ваші cookie на потенційне розкриття даних і підробку на боці клієнта.

<a name="redirects"></a>
## Перенаправлення

Відповіді-перенаправлення є екземплярами класу `Illuminate\Http\RedirectResponse` і містять потрібні заголовки для перенаправлення користувача на іншу адресу. Створити екземпляр `RedirectResponse` можна кількома способами. Найпростіший - скористатися глобальним хелпером `redirect`:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

Іноді вам може знадобитися перенаправити користувача на попередню сторінку - наприклад, коли надіслана форма виявилася недійсною. Це робиться глобальною функцією-хелпером `back`. Оскільки ця можливість використовує [сесію](/docs/{{version}}/session), переконайтеся, що маршрут, який викликає `back`, входить до групи `middleware` `web`:

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### Перенаправлення до іменованих маршрутів

Коли ви викликаєте хелпер `redirect` без параметрів, повертається екземпляр `Illuminate\Routing\Redirector`, що дозволяє викликати на ньому будь-який метод. Наприклад, щоб згенерувати `RedirectResponse` до іменованого маршруту, скористайтеся методом `route`:

```php
return redirect()->route('login');
```

Якщо ваш маршрут має параметри, передайте їх другим аргументом методу `route`:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Заповнення параметрів через моделі Eloquent

Якщо ви перенаправляєте до маршруту з параметром «ID», який заповнюється з моделі Eloquent, ви можете передати саму модель. Ідентифікатор буде вилучено автоматично:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

Якщо ви хочете налаштувати значення, що потрапляє в параметр маршруту, вкажіть колонку у визначенні параметра (`/profile/{id:slug}`) або перевизначте метод `getRouteKey` у своїй моделі Eloquent:

```php
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### Перенаправлення до дій контролерів

Ви також можете генерувати перенаправлення до [дій контролерів](/docs/{{version}}/controllers). Для цього передайте методу `action` контролер та ім'я дії:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

Якщо маршрут вашого контролера потребує параметрів, передайте їх другим аргументом методу `action`:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### Перенаправлення до зовнішніх доменів

Іноді вам може знадобитися перенаправлення на домен поза вашим застосунком. Це робиться методом `away`, який створює `RedirectResponse` без додаткового кодування, валідації чи перевірки URL:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### Перенаправлення з флеш-даними сесії

Перенаправлення на нову адресу та [запис флеш-даних до сесії](/docs/{{version}}/session#flash-data) зазвичай виконуються одночасно. Типово це роблять після успішного виконання дії, записуючи до сесії повідомлення про успіх. Для зручності ви можете створити екземпляр `RedirectResponse` і записати дані до сесії одним плинним ланцюжком методів:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

Після перенаправлення користувача ви можете показати збережене повідомлення із [сесії](/docs/{{version}}/session). Наприклад, за допомогою [синтаксису Blade](/docs/{{version}}/blade):

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### Перенаправлення з вхідними даними

Метод `withInput` екземпляра `RedirectResponse` дозволяє записати вхідні дані поточного запиту до сесії перед перенаправленням користувача. Зазвичай це роблять, коли користувач натрапив на помилку валідації. Щойно вхідні дані записано до сесії, ви можете легко [отримати їх](/docs/{{version}}/requests#retrieving-old-input) під час наступного запиту, щоб заново заповнити форму:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## Інші типи відповідей

Хелпер `response` дозволяє генерувати інші типи екземплярів відповідей. Коли його викликають без аргументів, повертається реалізація [контракту](/docs/{{version}}/contracts) `Illuminate\Contracts\Routing\ResponseFactory`. Цей контракт надає кілька корисних методів для генерації відповідей.

<a name="view-responses"></a>
### Відповіді-представлення

Якщо вам потрібен контроль над статусом і заголовками відповіді, але водночас потрібно повернути [представлення](/docs/{{version}}/views) як її вміст, скористайтеся методом `view`:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

Звісно, якщо вам не потрібно передавати власний HTTP-статус чи заголовки, ви можете скористатися глобальною функцією-хелпером `view`.

<a name="json-responses"></a>
### JSON-відповіді

Метод `json` автоматично встановить заголовок `Content-Type` у значення `application/json`, а також перетворить переданий масив на JSON PHP-функцією `json_encode`:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

Якщо ви хочете створити JSONP-відповідь, скористайтеся методом `json` у поєднанні з методом `withCallback`:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### Завантаження файлів

Метод `download` дозволяє згенерувати відповідь, що змусить браузер користувача завантажити файл за вказаним шляхом. Метод `download` приймає ім'я файлу другим аргументом - саме його побачить користувач, який завантажує файл. Нарешті, третім аргументом можна передати масив HTTP-заголовків:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> Symfony HttpFoundation, який керує завантаженням файлів, вимагає, щоб файл мав ім'я з символів ASCII.

<a name="file-responses"></a>
### Файлові відповіді

Метод `file` дозволяє показати файл - як-от зображення чи PDF - безпосередньо в браузері користувача замість того, щоб починати завантаження. Цей метод приймає абсолютний шлях до файлу першим аргументом і масив заголовків другим:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## Потокові відповіді

Передаючи дані клієнту в міру їх генерації, ви можете значно зменшити споживання пам'яті й покращити швидкодію - особливо для дуже великих відповідей. Потокові відповіді дозволяють клієнту почати обробку даних ще до того, як сервер завершить їх надсилання:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // Simulate delay between chunks...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

Для зручності, якщо замикання, передане методу `stream`, повертає [генератор](https://www.php.net/manual/en/language.generators.overview.php), Laravel автоматично скидатиме буфер виводу між рядками, які повертає генератор, а також вимкне буферизацію виводу Nginx:

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a name="consuming-streamed-responses"></a>
### Споживання потокових відповідей

Потокові відповіді можна споживати за допомогою npm-пакета `stream` від Laravel, який надає зручний API для роботи з відповідями та потоками подій Laravel. Щоб почати, встановіть пакет `@laravel/stream-react`, `@laravel/stream-vue` або `@laravel/stream-svelte`:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

Далі скористайтеся `useStream`, щоб споживати потік подій. Після вказання URL потоку хук автоматично оновлюватиме `data` об'єднаною відповіддю в міру її надходження від вашого застосунку Laravel:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");

const sendMessage = () => {
    stream.send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<div>
    <div>{$stream.data}</div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
    <button onclick={sendMessage}>Send Message</button>
</div>
```

Коли ви надсилаєте дані назад у потік через `send`, активне з'єднання з потоком скасовується перед надсиланням нових даних. Усі запити надсилаються як JSON-запити `POST`.

> [!WARNING]
> Оскільки хук `useStream` робить `POST`-запит до вашого застосунку, потрібен дійсний CSRF-токен. Найпростіший спосіб його надати - [додати його через meta-тег у head макета вашого застосунку](/docs/{{version}}/csrf#csrf-x-csrf-token).

Другий аргумент, переданий `useStream`, - це об'єкт опцій, яким можна налаштувати поведінку споживання потоку. Типові значення цього об'єкта наведено нижче:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response) => {},
    onData: (data) => {},
    onCancel: () => {},
    onFinish: () => {},
    onError: (error) => {},
});
</script>

<div>{$stream.data}</div>
```

`onResponse` спрацьовує після успішної початкової відповіді з потоку, і в колбек передається сирий [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response). `onData` викликається для кожного отриманого фрагмента - у колбек передається поточний фрагмент. `onFinish` викликається, коли потік завершився, а також коли під час циклу отримання чи читання виникає помилка.

За замовчуванням під час ініціалізації запит до потоку не робиться. Ви можете передати потоку початкові дані опцією `initialInput`:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<div>{$stream.data}</div>
```

Щоб скасувати потік вручну, скористайтеся методом `cancel`, який повертає хук:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <button onclick={() => stream.cancel()}>Cancel</button>
</div>
```

Щоразу, коли використовується хук `useStream`, генерується випадковий `id` для ідентифікації потоку. Він надсилається на сервер із кожним запитом у заголовку `X-STREAM-ID`. Коли ви споживаєте той самий потік із кількох компонентів, ви можете читати з нього й писати до нього, надавши власний `id`:

```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```

```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

```svelte tab=Svelte
<!-- App.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";
import StreamStatus from "./StreamStatus.svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <StreamStatus id={stream.id} />
</div>

<!-- StreamStatus.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";

let { id } = $props();

const stream = useStream("chat", { id });
</script>

<div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
</div>
```

<a name="streamed-json-responses"></a>
### Потокові JSON-відповіді

Якщо вам потрібно передавати JSON-дані поступово, скористайтеся методом `streamJson`. Він особливо корисний для великих наборів даних, які треба поступово надсилати браузеру у форматі, що легко розбирається JavaScript:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

Хук `useJsonStream` ідентичний [хуку useStream](#consuming-streamed-responses), за винятком того, що він намагатиметься розібрати дані як JSON після завершення потоку:

```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useJsonStream } from "@laravel/stream-svelte";

const stream = useJsonStream("users");

const loadUsers = () => {
    stream.send({
        query: "taylor",
    });
};
</script>

<div>
    <ul>
        {#if $stream.data?.users}
            {#each $stream.data.users as user (user.id)}
                <li>{user.id}: {user.name}</li>
            {/each}
        {/if}
    </ul>
    <button onclick={loadUsers}>Load Users</button>
</div>
```

<a name="event-streams"></a>
### Потоки подій (SSE)

Метод `eventStream` дозволяє повернути потокову відповідь із подіями, надісланими сервером (SSE), із типом вмісту `text/event-stream`. Метод `eventStream` приймає замикання, яке має [віддавати](https://www.php.net/manual/en/language.generators.overview.php) відповіді в потік у міру їх появи:

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

Якщо ви хочете налаштувати ім'я події, віддавайте екземпляр класу `StreamedEvent`:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### Споживання потоків подій

Потоки подій можна споживати за допомогою npm-пакета `stream` від Laravel, який надає зручний API для роботи з потоками подій Laravel. Щоб почати, встановіть пакет `@laravel/stream-react`, `@laravel/stream-vue` або `@laravel/stream-svelte`:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

Далі скористайтеся `useEventStream`, щоб споживати потік подій. Після вказання URL потоку хук автоматично оновлюватиме `message` об'єднаною відповіддю в міру надходження повідомлень від вашого застосунку Laravel:

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat");
</script>

<div>{$eventStream.message}</div>
```

Другий аргумент, переданий `useEventStream`, - це об'єкт опцій, яким можна налаштувати поведінку споживання потоку. Типові значення цього об'єкта наведено нижче:

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  eventName: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat", {
    eventName: "update",
    onMessage: (event) => {
        //
    },
    onError: (error) => {
        //
    },
    onComplete: () => {
        //
    },
    endSignal: "</stream>",
    glue: " ",
    replace: false,
});
</script>
```

Потоки подій можна також споживати вручну через об'єкт [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) на фронтенді вашого застосунку. Метод `eventStream` автоматично надішле в потік оновлення `</stream>`, коли потік завершиться:

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```

Щоб налаштувати останню подію, яку надсилають у потік, передайте екземпляр `StreamedEvent` в аргумент `endStreamWith` методу `eventStream`:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### Потокові завантаження

Іноді ви можете захотіти перетворити рядкову відповідь певної операції на завантажуваний файл, не записуючи її вміст на диск. У такому разі скористайтеся методом `streamDownload`. Він приймає колбек, ім'я файлу та необов'язковий масив заголовків:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## Макроси відповідей

Якщо ви хочете визначити власну відповідь, яку можна повторно використовувати в різних маршрутах і контролерах, скористайтеся методом `macro` фасаду `Response`. Зазвичай цей метод варто викликати з методу `boot` одного із [сервіс-провайдерів](/docs/{{version}}/providers) вашого застосунку - наприклад, `App\Providers\AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

Функція `macro` приймає ім'я першим аргументом і замикання другим. Замикання макроса виконуватиметься під час виклику імені макроса на реалізації `ResponseFactory` чи хелпері `response`:

```php
return response()->caps('foo');
```
