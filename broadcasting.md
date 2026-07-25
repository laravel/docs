---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Бродкастинг

- [Вступ](#introduction)
- [Швидкий старт](#quickstart)
- [Встановлення на боці сервера](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [Встановлення на боці клієнта](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [Огляд концепції](#concept-overview)
    - [На прикладі застосунку](#using-example-application)
- [Опис подій для бродкастингу](#defining-broadcast-events)
    - [Ім'я бродкасту](#broadcast-name)
    - [Дані бродкасту](#broadcast-data)
    - [Черга бродкасту](#broadcast-queue)
    - [Умови бродкасту](#broadcast-conditions)
    - [Бродкастинг і транзакції бази даних](#broadcasting-and-database-transactions)
- [Авторизація каналів](#authorizing-channels)
    - [Опис колбеків авторизації](#defining-authorization-callbacks)
    - [Класи каналів](#defining-channel-classes)
- [Бродкастинг подій](#broadcasting-events)
    - [Лише іншим](#only-to-others)
    - [Налаштування підключення](#customizing-the-connection)
    - [Анонімні події](#anonymous-events)
    - [Убезпечення бродкастів](#rescuing-broadcasts)
- [Отримання бродкастів](#receiving-broadcasts)
    - [Прослуховування подій](#listening-for-events)
    - [Вихід з каналу](#leaving-a-channel)
    - [Простори імен](#namespaces)
    - [Використання React, Vue чи Svelte](#using-react-or-vue)
- [Канали присутності](#presence-channels)
    - [Авторизація каналів присутності](#authorizing-presence-channels)
    - [Приєднання до каналів присутності](#joining-presence-channels)
    - [Бродкастинг у канали присутності](#broadcasting-to-presence-channels)
- [Бродкастинг моделей](#model-broadcasting)
    - [Домовленості бродкастингу моделей](#model-broadcasting-conventions)
    - [Прослуховування бродкастів моделей](#listening-for-model-broadcasts)
- [Клієнтські події](#client-events)
- [Сповіщення](#notifications)

<a name="introduction"></a>
## Вступ

У багатьох сучасних вебзастосунках WebSocket використовують, щоб будувати інтерфейси, які оновлюються в реальному часі. Коли на сервері оновлюються якісь дані, через WebSocket-з'єднання зазвичай надсилається повідомлення, яке обробляє клієнт. WebSocket - ефективніша альтернатива постійному опитуванню сервера на предмет змін, які мають відобразитися в інтерфейсі.

Наприклад, уявіть, що ваш застосунок уміє експортувати дані користувача у CSV-файл і надсилати його поштою. Проте створення цього CSV-файлу займає кілька хвилин, тож ви створюєте й надсилаєте CSV у [завданні в черзі](/docs/{{version}}/queues). Коли CSV створено й надіслано користувачеві, ми можемо скористатися бродкастингом подій, щоб диспетчеризувати подію `App\Events\UserDataExported`, яку отримає JavaScript нашого застосунку. Отримавши подію, ми можемо показати користувачеві повідомлення, що його CSV надіслано поштою, - і йому не доведеться оновлювати сторінку.

Щоб допомогти вам будувати такі можливості, Laravel спрощує «бродкастинг» серверних [подій](/docs/{{version}}/events) Laravel через WebSocket-з'єднання. Бродкастинг подій Laravel дозволяє мати спільні імена подій і дані між серверним застосунком Laravel і клієнтським застосунком на JavaScript.

Основні ідеї бродкастингу прості: на фронтенді клієнти підключаються до іменованих каналів, а ваш застосунок Laravel на бекенді надсилає події в ці канали. Ці події можуть містити будь-які додаткові дані, які ви хочете зробити доступними на фронтенді.

<a name="supported-drivers"></a>
#### Підтримувані драйвери

За замовчуванням Laravel містить три серверні драйвери бродкастингу на вибір: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels) та [Ably](https://ably.com).

> [!NOTE]
> Перш ніж занурюватися в бродкастинг подій, обов'язково прочитайте документацію Laravel про [події та слухачів](/docs/{{version}}/events).

<a name="quickstart"></a>
## Швидкий старт

За замовчуванням у нових застосунках Laravel бродкастинг вимкнено. Увімкнути його можна командою Artisan `install:broadcasting`:

```shell
php artisan install:broadcasting
```

Команда `install:broadcasting` запитає, який сервіс бродкастингу подій ви хочете використовувати. Крім того, вона створить файл конфігурації `config/broadcasting.php` і файл `routes/channels.php`, де ви можете реєструвати маршрути та колбеки авторизації бродкастингу вашого застосунку.

Laravel «з коробки» підтримує кілька драйверів бродкастингу: [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), а також драйвер `log` для локальної розробки й налагодження. Крім того, є драйвер `null`, який дозволяє вимкнути бродкастинг під час тестування. Приклад конфігурації для кожного з цих драйверів є у файлі `config/broadcasting.php`.

Уся конфігурація бродкастингу подій вашого застосунку зберігається у файлі `config/broadcasting.php`. Не переймайтеся, якщо цього файлу у вашому застосунку немає, - його буде створено, коли ви виконаєте команду Artisan `install:broadcasting`.

<a name="quickstart-next-steps"></a>
#### Наступні кроки

Щойно ви увімкнули бродкастинг подій, можна вивчати [опис подій для бродкастингу](#defining-broadcast-events) і [прослуховування подій](#listening-for-events). Якщо ви користуєтеся [стартовими наборами](/docs/{{version}}/starter-kits) Laravel для React, Vue чи Svelte, слухати події можна через [хук useEcho](#using-react-or-vue) з Echo.

> [!NOTE]
> Перш ніж надсилати будь-які події, вам слід налаштувати й запустити [воркер черги](/docs/{{version}}/queues). Увесь бродкастинг подій відбувається через завдання в черзі, щоб час відповіді вашого застосунку суттєво не страждав від надсилання подій.

<a name="server-side-installation"></a>
## Встановлення на боці сервера

Щоб почати користуватися бродкастингом подій у Laravel, нам потрібно дещо налаштувати в застосунку Laravel, а також встановити кілька пакетів.

Бродкастинг подій виконує серверний драйвер бродкастингу, який надсилає ваші події Laravel так, щоб Laravel Echo (бібліотека на JavaScript) могла отримати їх у браузері. Не хвилюйтеся - ми пройдемо кожен крок встановлення по черзі.

<a name="reverb"></a>
### Reverb

Щоб швидко увімкнути підтримку бродкастингу в Laravel із Reverb як бродкастером подій, виконайте команду Artisan `install:broadcasting` з опцією `--reverb`. Ця команда встановить потрібні Reverb пакети Composer і NPM та оновить файл `.env` вашого застосунку відповідними змінними:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### Встановлення вручну

Під час виконання команди `install:broadcasting` вам запропонують встановити [Laravel Reverb](/docs/{{version}}/reverb). Звісно, ви можете встановити Reverb і вручну через менеджер пакетів Composer:

```shell
composer require laravel/reverb
```

Щойно пакет встановлено, ви можете виконати команду встановлення Reverb, щоб опублікувати конфігурацію, додати потрібні Reverb змінні середовища й увімкнути бродкастинг подій у застосунку:

```shell
php artisan reverb:install
```

Детальні інструкції зі встановлення та використання Reverb ви знайдете в [документації Reverb](/docs/{{version}}/reverb).

<a name="pusher-channels"></a>
### Pusher Channels

Щоб швидко увімкнути підтримку бродкастингу в Laravel із Pusher як бродкастером подій, виконайте команду Artisan `install:broadcasting` з опцією `--pusher`. Ця команда запитає ваші облікові дані Pusher, встановить PHP- та JavaScript-SDK Pusher і оновить файл `.env` вашого застосунку відповідними змінними:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### Встановлення вручну

Щоб встановити підтримку Pusher вручну, встановіть PHP SDK Pusher Channels через менеджер пакетів Composer:

```shell
composer require pusher/pusher-php-server
```

Далі налаштуйте облікові дані Pusher Channels у файлі конфігурації `config/broadcasting.php`. Приклад конфігурації Pusher Channels уже є в цьому файлі, тож ви можете швидко вказати свої ключ, секрет та ID застосунку. Зазвичай облікові дані Pusher Channels налаштовують у файлі `.env` вашого застосунку:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

Конфігурація `pusher` у файлі `config/broadcasting.php` також дозволяє вказати додаткові `options`, які підтримує Channels, - наприклад, кластер.

Далі задайте змінній середовища `BROADCAST_CONNECTION` значення `pusher` у файлі `.env` вашого застосунку:

```ini
BROADCAST_CONNECTION=pusher
```

Нарешті, ви готові встановити й налаштувати [Laravel Echo](#client-side-installation), яка отримуватиме події бродкастингу на боці клієнта.

<a name="ably"></a>
### Ably

> [!NOTE]
> Документація нижче описує використання Ably в режимі «сумісності з Pusher». Проте команда Ably рекомендує й підтримує власні бродкастер та клієнт Echo, які вміють користуватися унікальними можливостями Ably. Докладніше про драйвери від Ably читайте в [документації бродкастера Ably для Laravel](https://github.com/ably/laravel-broadcaster).

Щоб швидко увімкнути підтримку бродкастингу в Laravel з [Ably](https://ably.com) як бродкастером подій, виконайте команду Artisan `install:broadcasting` з опцією `--ably`. Ця команда запитає ваші облікові дані Ably, встановить PHP- та JavaScript-SDK Ably і оновить файл `.env` вашого застосунку відповідними змінними:

```shell
php artisan install:broadcasting --ably
```

**Перш ніж продовжувати, увімкніть підтримку протоколу Pusher у налаштуваннях вашого застосунку Ably. Зробити це можна в розділі «Protocol Adapter Settings» панелі налаштувань застосунку Ably.**

<a name="ably-manual-installation"></a>
#### Встановлення вручну

Щоб встановити підтримку Ably вручну, встановіть PHP SDK Ably через менеджер пакетів Composer:

```shell
composer require ably/ably-php
```

Далі налаштуйте облікові дані Ably у файлі конфігурації `config/broadcasting.php`. Приклад конфігурації Ably уже є в цьому файлі, тож ви можете швидко вказати свій ключ. Зазвичай це значення задають через [змінну середовища](/docs/{{version}}/configuration#environment-configuration) `ABLY_KEY`:

```ini
ABLY_KEY=your-ably-key
```

Далі задайте змінній середовища `BROADCAST_CONNECTION` значення `ably` у файлі `.env` вашого застосунку:

```ini
BROADCAST_CONNECTION=ably
```

Нарешті, ви готові встановити й налаштувати [Laravel Echo](#client-side-installation), яка отримуватиме події бродкастингу на боці клієнта.

<a name="client-side-installation"></a>
## Встановлення на боці клієнта

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo) - це бібліотека на JavaScript, яка робить підписку на канали й прослуховування подій, надісланих вашим серверним драйвером бродкастингу, безболісними.

Коли ви встановлюєте Laravel Reverb командою Artisan `install:broadcasting`, каркас і конфігурацію Reverb та Echo буде додано до вашого застосунку автоматично. Проте, якщо ви хочете налаштувати Laravel Echo вручну, скористайтеся інструкціями нижче.

<a name="reverb-client-manual-installation"></a>
#### Встановлення вручну

Щоб налаштувати Laravel Echo для фронтенду вашого застосунку вручну, спершу встановіть пакет `pusher-js`, оскільки Reverb використовує протокол Pusher для WebSocket-підписок, каналів і повідомлень:

```shell
npm install --save-dev laravel-echo pusher-js
```

Щойно Echo встановлено, ви можете створити свіжий екземпляр Echo у JavaScript вашого застосунку. Чудове місце для цього - кінець файлу `resources/js/app.js`, який входить до складу фреймворку Laravel:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

Далі скомпілюйте ресурси вашого застосунку:

```shell
npm run build
```

> [!WARNING]
> Бродкастер `reverb` для Laravel Echo потребує laravel-echo v1.16.0+.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo) - це бібліотека на JavaScript, яка робить підписку на канали й прослуховування подій, надісланих вашим серверним драйвером бродкастингу, безболісними.

Коли ви встановлюєте підтримку бродкастингу командою Artisan `install:broadcasting --pusher`, каркас і конфігурацію Pusher та Echo буде додано до вашого застосунку автоматично. Проте, якщо ви хочете налаштувати Laravel Echo вручну, скористайтеся інструкціями нижче.

<a name="pusher-client-manual-installation"></a>
#### Встановлення вручну

Щоб налаштувати Laravel Echo для фронтенду вашого застосунку вручну, спершу встановіть пакети `laravel-echo` та `pusher-js`, які використовують протокол Pusher для WebSocket-підписок, каналів і повідомлень:

```shell
npm install --save-dev laravel-echo pusher-js
```

Щойно Echo встановлено, ви можете створити свіжий екземпляр Echo у файлі `resources/js/app.js` вашого застосунку:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

Далі задайте відповідні значення змінних середовища Pusher у файлі `.env` вашого застосунку. Якщо цих змінних у файлі `.env` ще немає, додайте їх:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

Щойно ви скоригували конфігурацію Echo під потреби свого застосунку, можете скомпілювати його ресурси:

```shell
npm run build
```

> [!NOTE]
> Щоб дізнатися більше про компіляцію JavaScript-ресурсів вашого застосунку, зверніться до документації про [Vite](/docs/{{version}}/vite).

<a name="using-an-existing-client-instance"></a>
#### Використання наявного екземпляра клієнта

Якщо у вас уже є попередньо налаштований екземпляр клієнта Pusher Channels, який ви хочете віддати Echo, передайте його через опцію конфігурації `client`:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
### Ably

> [!NOTE]
> Документація нижче описує використання Ably в режимі «сумісності з Pusher». Проте команда Ably рекомендує й підтримує власні бродкастер та клієнт Echo, які вміють користуватися унікальними можливостями Ably. Докладніше про драйвери від Ably читайте в [документації бродкастера Ably для Laravel](https://github.com/ably/laravel-broadcaster).

[Laravel Echo](https://github.com/laravel/echo) - це бібліотека на JavaScript, яка робить підписку на канали й прослуховування подій, надісланих вашим серверним драйвером бродкастингу, безболісними.

Коли ви встановлюєте підтримку бродкастингу командою Artisan `install:broadcasting --ably`, каркас і конфігурацію Ably та Echo буде додано до вашого застосунку автоматично. Проте, якщо ви хочете налаштувати Laravel Echo вручну, скористайтеся інструкціями нижче.

<a name="ably-client-manual-installation"></a>
#### Встановлення вручну

Щоб налаштувати Laravel Echo для фронтенду вашого застосунку вручну, спершу встановіть пакети `laravel-echo` та `pusher-js`, які використовують протокол Pusher для WebSocket-підписок, каналів і повідомлень:

```shell
npm install --save-dev laravel-echo pusher-js
```

**Перш ніж продовжувати, увімкніть підтримку протоколу Pusher у налаштуваннях вашого застосунку Ably. Зробити це можна в розділі «Protocol Adapter Settings» панелі налаштувань застосунку Ably.**

Щойно Echo встановлено, ви можете створити свіжий екземпляр Echo у файлі `resources/js/app.js` вашого застосунку:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

Ви могли помітити, що наша конфігурація Echo для Ably посилається на змінну середовища `VITE_ABLY_PUBLIC_KEY`. Значенням цієї змінної має бути ваш публічний ключ Ably. Публічний ключ - це частина вашого ключа Ably до символу `:`.

Щойно ви скоригували конфігурацію Echo під свої потреби, можете скомпілювати ресурси застосунку:

```shell
npm run dev
```

> [!NOTE]
> Щоб дізнатися більше про компіляцію JavaScript-ресурсів вашого застосунку, зверніться до документації про [Vite](/docs/{{version}}/vite).

<a name="concept-overview"></a>
## Огляд концепції

Бродкастинг подій у Laravel дозволяє надсилати серверні події Laravel до клієнтського застосунку на JavaScript, використовуючи драйверний підхід до WebSocket. Наразі Laravel постачається з драйверами [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels) та [Ably](https://ably.com). Події легко спожити на боці клієнта за допомогою JavaScript-пакета [Laravel Echo](#client-side-installation).

Події надсилаються через «канали», які можуть бути публічними або приватними. Будь-який відвідувач вашого застосунку може підписатися на публічний канал без автентифікації чи авторизації; натомість, щоб підписатися на приватний канал, користувач має бути автентифікований і авторизований слухати цей канал.

<a name="using-example-application"></a>
### На прикладі застосунку

Перш ніж заглиблюватися в кожен компонент бродкастингу подій, розгляньмо все з висоти пташиного польоту на прикладі інтернет-магазину.

Припустімо, у нашому застосунку є сторінка, на якій користувачі бачать статус доставки своїх замовлень. Припустімо також, що коли застосунок обробляє оновлення статусу доставки, спрацьовує подія `OrderShipmentStatusUpdated`:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### Інтерфейс `ShouldBroadcast`

Коли користувач переглядає одне зі своїх замовлень, ми не хочемо, щоб йому доводилося оновлювати сторінку заради оновлень статусу. Натомість ми хочемо надсилати оновлення в застосунок щойно вони з'являються. Отже, нам потрібно позначити подію `OrderShipmentStatusUpdated` інтерфейсом `ShouldBroadcast`. Це скаже Laravel надсилати подію, коли вона спрацьовує:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

Інтерфейс `ShouldBroadcast` вимагає, щоб наша подія описала метод `broadcastOn`. Цей метод відповідає за повернення каналів, у які має надсилатися подія. Порожня заготовка цього методу вже є у згенерованих класах подій, тож нам залишається лише заповнити її. Ми хочемо, щоб оновлення статусу бачив лише автор замовлення, тому надсилатимемо подію в приватний канал, прив'язаний до замовлення:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

Якщо ви хочете надсилати подію в кілька каналів, поверніть замість цього `array`:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.'.$this->order->id),
        // ...
    ];
}
```

<a name="example-application-authorizing-channels"></a>
#### Авторизація каналів

Пам'ятайте: щоб слухати приватні канали, користувачі мають бути авторизовані. Правила авторизації каналів ми можемо описати у файлі `routes/channels.php` нашого застосунку. У цьому прикладі нам потрібно перевірити, що будь-який користувач, який намагається слухати приватний канал `orders.1`, справді є автором замовлення:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

Метод `channel` приймає два аргументи: ім'я каналу й колбек, який повертає `true` або `false` залежно від того, чи авторизований користувач слухати цей канал.

Усі колбеки авторизації першим аргументом отримують поточного автентифікованого користувача, а наступними - будь-які додаткові підстановочні параметри. У цьому прикладі ми використовуємо плейсхолдер `{orderId}`, щоб позначити, що частина імені каналу з «ID» є підстановкою.

<a name="listening-for-event-broadcasts"></a>
#### Прослуховування бродкастів подій

Далі лишається тільки послухати подію в нашому застосунку на JavaScript. Зробити це можна за допомогою [Laravel Echo](#client-side-installation). Вбудовані в Laravel Echo хуки для React, Vue та Svelte роблять старт простим, і за замовчуванням усі публічні властивості події потраплять до надісланої події:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<a name="defining-broadcast-events"></a>
## Опис подій для бродкастингу

Щоб повідомити Laravel, що певну подію слід надсилати, реалізуйте в класі події інтерфейс `Illuminate\Contracts\Broadcasting\ShouldBroadcast`. Цей інтерфейс уже імпортовано в усі класи подій, згенеровані фреймворком, тож ви легко можете додати його до будь-якої своєї події.

Інтерфейс `ShouldBroadcast` вимагає реалізувати єдиний метод - `broadcastOn`. Метод `broadcastOn` має повернути канал або масив каналів, у які слід надсилати подію. Канали мають бути екземплярами `Channel`, `PrivateChannel` чи `PresenceChannel`. Екземпляри `Channel` представляють публічні канали, на які може підписатися будь-який користувач, а `PrivateChannels` і `PresenceChannels` - приватні канали, які потребують [авторизації каналу](#authorizing-channels):

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.'.$this->user->id),
        ];
    }
}
```

Реалізувавши інтерфейс `ShouldBroadcast`, вам залишається лише [запустити подію](/docs/{{version}}/events) як зазвичай. Щойно подію запущено, [завдання в черзі](/docs/{{version}}/queues) автоматично надішле її через вказаний драйвер бродкастингу.

<a name="broadcast-name"></a>
### Ім'я бродкасту

За замовчуванням Laravel надсилає подію під іменем її класу. Проте ви можете змінити ім'я бродкасту, описавши в події метод `broadcastAs`:

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

Якщо ви змінюєте ім'я бродкасту методом `broadcastAs`, обов'язково реєструйте слухача з провідною крапкою `.`. Це скаже Echo не додавати до події простір імен застосунку:

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### Дані бродкасту

Коли подію надіслано, усі її `public` властивості автоматично серіалізуються й передаються як дані події, тож ви маєте доступ до будь-яких її публічних даних із застосунку на JavaScript. Наприклад, якщо ваша подія має єдину публічну властивість `$user` з моделлю Eloquent, дані бродкасту події будуть такими:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

Проте, якщо ви хочете тонше контролювати дані бродкасту, додайте до події метод `broadcastWith`. Цей метод має повернути масив даних, які ви хочете надіслати як дані події:

```php
/**
 * Get the data to broadcast.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
### Черга бродкасту

За замовчуванням кожна подія бродкастингу потрапляє до черги за замовчуванням для підключення черги за замовчуванням, вказаного у файлі конфігурації `queue.php`. Ви можете змінити підключення й ім'я черги, які використовує бродкастер, за допомогою атрибутів `Connection` та `Queue` у класі події:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('redis')]
#[Queue('default')]
class ServerCreated implements ShouldBroadcast
{
    // ...
}
```

Як варіант, ви можете змінити ім'я черги, описавши в події метод `broadcastQueue`:

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

Якщо ви хочете надсилати подію через чергу `sync` замість драйвера черги за замовчуванням, реалізуйте інтерфейс `ShouldBroadcastNow` замість `ShouldBroadcast`:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
### Умови бродкасту

Інколи потрібно надсилати подію лише за певної умови. Описати такі умови можна, додавши до класу події метод `broadcastWhen`:

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### Бродкастинг і транзакції бази даних

Коли події бродкастингу диспетчеризуються всередині транзакцій бази даних, черга може обробити їх ще до того, як транзакцію буде зафіксовано. Коли таке трапляється, будь-які зміни, які ви внесли до моделей чи записів у базі під час транзакції, ще можуть не бути в базі. Ба більше, будь-які моделі чи записи, створені всередині транзакції, можуть у базі не існувати. Якщо ваша подія залежить від цих моделей, під час обробки завдання, яке надсилає подію, можуть виникнути несподівані помилки.

Якщо опція конфігурації `after_commit` вашого підключення черги має значення `false`, ви все одно можете вказати, що конкретну подію бродкастингу слід диспетчеризувати після фіксації всіх відкритих транзакцій бази даних, - реалізуйте в класі події інтерфейс `ShouldDispatchAfterCommit`:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```

> [!NOTE]
> Щоб дізнатися більше про обхід цих проблем, перегляньте документацію про [завдання в черзі та транзакції бази даних](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="authorizing-channels"></a>
## Авторизація каналів

Приватні канали вимагають перевірити, що поточний автентифікований користувач справді може слухати канал. Це робиться через HTTP-запит до вашого застосунку Laravel з іменем каналу, і застосунок вирішує, чи може користувач слухати цей канал. Коли ви користуєтеся [Laravel Echo](#client-side-installation), HTTP-запит на авторизацію підписок на приватні канали виконується автоматично.

Коли бродкастинг встановлено, Laravel намагається автоматично зареєструвати маршрут `/broadcasting/auth` для обробки запитів авторизації. Якщо Laravel не вдасться зареєструвати ці маршрути автоматично, ви можете зареєструвати їх вручну у файлі `/bootstrap/app.php` вашого застосунку:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
### Опис колбеків авторизації

Далі нам потрібно описати логіку, яка визначатиме, чи може поточний автентифікований користувач слухати певний канал. Це робиться у файлі `routes/channels.php`, який створює команда Artisan `install:broadcasting`. У цьому файлі ви можете реєструвати колбеки авторизації каналів методом `Broadcast::channel`:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

Метод `channel` приймає два аргументи: ім'я каналу й колбек, який повертає `true` або `false` залежно від того, чи авторизований користувач слухати цей канал.

Усі колбеки авторизації першим аргументом отримують поточного автентифікованого користувача, а наступними - будь-які додаткові підстановочні параметри. У цьому прикладі ми використовуємо плейсхолдер `{orderId}`, щоб позначити, що частина імені каналу з «ID» є підстановкою.

Переглянути список колбеків авторизації бродкастингу вашого застосунку можна командою Artisan `channel:list`:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### Прив'язка моделей у колбеках авторизації

Так само як HTTP-маршрути, маршрути каналів можуть користуватися неявною та явною [прив'язкою моделей до маршрутів](/docs/{{version}}/routing#route-model-binding). Наприклад, замість рядкового чи числового ID замовлення ви можете запросити справжній екземпляр моделі `Order`:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> На відміну від прив'язки моделей у HTTP-маршрутах, прив'язка моделей у каналах не підтримує автоматичне [скопування неявної прив'язки моделей](/docs/{{version}}/routing#implicit-model-binding-scoping). Утім, це рідко стає проблемою, бо більшість каналів можна скопувати за унікальним первинним ключем однієї моделі.

<a name="authorization-callback-authentication"></a>
#### Автентифікація в колбеках авторизації

Приватні канали та канали присутності автентифікують поточного користувача через гард автентифікації за замовчуванням вашого застосунку. Якщо користувач не автентифікований, авторизацію каналу буде автоматично відхилено, а колбек авторизації ніколи не виконається. Проте за потреби ви можете призначити кілька власних гардів, які мають автентифікувати вхідний запит:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### Класи каналів

Якщо ваш застосунок споживає багато різних каналів, файл `routes/channels.php` може розростися. Тож замість замикань для авторизації каналів ви можете скористатися класами каналів. Щоб згенерувати клас каналу, скористайтеся командою Artisan `make:channel`. Вона покладе новий клас каналу в каталог `App/Broadcasting`.

```shell
php artisan make:channel OrderChannel
```

Далі зареєструйте свій канал у файлі `routes/channels.php`:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

Нарешті, ви можете розмістити логіку авторизації каналу в методі `join` класу каналу. Цей метод `join` міститиме ту саму логіку, яку ви зазвичай розмістили б у замиканні авторизації каналу. Ви так само можете користуватися прив'язкою моделей у каналах:

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Як і багато інших класів у Laravel, класи каналів автоматично розв'язуються [сервіс-контейнером](/docs/{{version}}/container). Тож ви можете вказати типи будь-яких залежностей, потрібних вашому каналу, у його конструкторі.

<a name="broadcasting-events"></a>
## Бродкастинг подій

Щойно ви описали подію й позначили її інтерфейсом `ShouldBroadcast`, вам залишається лише запустити подію її методом диспетчеризації. Диспетчер подій помітить, що подію позначено інтерфейсом `ShouldBroadcast`, і поставить її в чергу на бродкастинг:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### Лише іншим

Будуючи застосунок з бродкастингом подій, ви інколи можете потребувати надіслати подію всім підписникам каналу, окрім поточного користувача. Зробити це можна за допомогою хелпера `broadcast` і методу `toOthers`:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

Щоб краще зрозуміти, коли вам знадобиться метод `toOthers`, уявімо застосунок зі списком завдань, у якому користувач створює нове завдання, вводячи його назву. Щоб створити завдання, ваш застосунок може надіслати запит на URL `/task`, який надсилає подію про створення завдання й повертає JSON-представлення нового завдання. Коли ваш застосунок на JavaScript отримує відповідь від точки входу, він може одразу вставити нове завдання до свого списку ось так:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

Проте пам'ятайте, що ми також надсилаємо подію про створення завдання. Якщо ваш застосунок на JavaScript теж слухає цю подію, щоб додавати завдання до списку, у списку з'являться дублікати: один із точки входу, другий - з бродкасту. Розв'язати це можна методом `toOthers`, який скаже бродкастеру не надсилати подію поточному користувачеві.

> [!WARNING]
> Щоб викликати метод `toOthers`, ваша подія має використовувати трейт `Illuminate\Broadcasting\InteractsWithSockets`.

<a name="only-to-others-configuration"></a>
#### Конфігурація

Коли ви ініціалізуєте екземпляр Laravel Echo, з'єднанню призначається ID сокета. Якщо ви користуєтеся глобальним екземпляром [Axios](https://github.com/axios/axios) для HTTP-запитів із застосунку на JavaScript, ID сокета автоматично додається до кожного вихідного запиту заголовком `X-Socket-ID`. Тоді, коли ви викликаєте метод `toOthers`, Laravel дістане ID сокета із заголовка й скаже бродкастеру не надсилати подію жодному з'єднанню з цим ID сокета.

Якщо ви не користуєтеся глобальним екземпляром Axios, вам доведеться вручну налаштувати ваш застосунок на JavaScript надсилати заголовок `X-Socket-ID` з усіма вихідними запитами. Отримати ID сокета можна методом `Echo.socketId`:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### Налаштування підключення

Якщо ваш застосунок працює з кількома підключеннями бродкастингу і ви хочете надіслати подію не через бродкастер за замовчуванням, вказати підключення, до якого слід віддати подію, можна методом `via`:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

Як варіант, ви можете вказати підключення бродкастингу події, викликавши метод `broadcastVia` у її конструкторі. Проте перед цим переконайтеся, що клас події використовує трейт `InteractsWithBroadcasting`:

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithBroadcasting;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    use InteractsWithBroadcasting;

    /**
     * Create a new event instance.
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### Анонімні події

Інколи вам може захотітися надіслати просту подію на фронтенд застосунку, не створюючи окремого класу події. Для цього фасад `Broadcast` дозволяє надсилати «анонімні події»:

```php
Broadcast::on('orders.'.$order->id)->send();
```

Приклад вище надішле таку подію:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

Методами `as` і `with` ви можете змінити ім'я та дані події:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

Приклад вище надішле подію на кшталт такої:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

Якщо ви хочете надіслати анонімну подію в приватний канал або канал присутності, скористайтеся методами `private` та `presence`:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

Надсилання анонімної події методом `send` диспетчеризує подію до [черги](/docs/{{version}}/queues) вашого застосунку на обробку. Проте, якщо ви хочете надіслати подію негайно, скористайтеся методом `sendNow`:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

Щоб надіслати подію всім підписникам каналу, окрім поточного автентифікованого користувача, викличте метод `toOthers`:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### Убезпечення бродкастів

Коли сервер черги вашого застосунку недоступний або Laravel натрапляє на помилку під час надсилання події, викидається виняток, через який кінцевий користувач зазвичай бачить помилку застосунку. Оскільки бродкастинг подій часто є доповненням до основної функціональності застосунку, ви можете не дати цим винятками псувати користувацький досвід, - реалізуйте у своїх подіях інтерфейс `ShouldRescue`.

Події, які реалізують інтерфейс `ShouldRescue`, під час спроб бродкастингу автоматично використовують [функцію-хелпер rescue](/docs/{{version}}/helpers#method-rescue) Laravel. Цей хелпер ловить будь-які винятки, повідомляє про них обробнику винятків вашого застосунку для логування й дозволяє застосунку працювати далі, не перериваючи роботу користувача:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```

<a name="receiving-broadcasts"></a>
## Отримання бродкастів

<a name="listening-for-events"></a>
### Прослуховування подій

Щойно ви [встановили та створили екземпляр Laravel Echo](#client-side-installation), можна починати слухати події, які надсилає ваш застосунок Laravel. Спершу отримайте екземпляр каналу методом `channel`, а потім викличте метод `listen`, щоб слухати вказану подію:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

Якщо ви хочете слухати події в приватному каналі, скористайтеся методом `private`. Ви можете й далі ланцюжком викликати метод `listen`, щоб слухати кілька подій в одному каналі:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### Припинення прослуховування подій

Якщо ви хочете перестати слухати певну подію, не [виходячи з каналу](#leaving-a-channel), скористайтеся методом `stopListening`:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### Вихід з каналу

Щоб вийти з каналу, викличте метод `leaveChannel` вашого екземпляра Echo:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

Якщо ви хочете вийти з каналу разом із пов'язаними з ним приватним каналом і каналом присутності, викличте метод `leave`:

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### Простори імен

Ви могли помітити в прикладах вище, що ми не вказували повний простір імен `App\Events` для класів подій. Це тому, що Echo автоматично вважає, що події лежать у просторі імен `App\Events`. Проте ви можете налаштувати кореневий простір імен під час створення екземпляра Echo, передавши опцію конфігурації `namespace`:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

Як варіант, ви можете додавати до класів подій префікс `.`, підписуючись на них через Echo. Це дозволить завжди вказувати повне ім'я класу:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### Використання React, Vue чи Svelte

Laravel Echo містить хуки для React, Vue та Svelte, які роблять прослуховування подій безболісним. Для початку викличте хук `useEcho`, який слухає приватні події. Хук `useEcho` автоматично виходить з каналів, коли компонент, який його використовує, демонтується:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

Ви можете слухати кілька подій, передавши до `useEcho` масив подій:

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

Ви також можете описати форму даних події бродкасту, отримавши кращу типобезпеку й зручність редагування:

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```

Хук `useEcho` автоматично виходить з каналів, коли компонент, який його використовує, демонтується; проте за потреби ви можете скористатися поверненими функціями, щоб програмно зупиняти / поновлювати прослуховування каналів вручну:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### Підключення до публічних каналів

Щоб підключитися до публічного каналу, скористайтеся хуком `useEchoPublic`:

```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoPublic } from "@laravel/echo-svelte";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### Підключення до каналів присутності

Щоб підключитися до каналу присутності, скористайтеся хуком `useEchoPresence`:

```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoPresence } from "@laravel/echo-svelte";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connection-status"></a>
#### Статус з'єднання

Отримати поточний статус WebSocket-з'єднання можна хуком `useConnectionStatus`, який надає реактивний статус, що автоматично оновлюється зі зміною стану з'єднання:

```js tab=React
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useConnectionStatus } from "@laravel/echo-svelte";

const status = useConnectionStatus();
</script>

<div>Connection: {status()}</div>
```

Можливі значення статусу:

<div class="content-list" markdown="1">

- `connected` - успішно підключено до WebSocket-сервера.
- `connecting` - триває початкова спроба підключення.
- `reconnecting` - триває спроба перепідключитися після розриву.
- `disconnected` - не підключено й спроб перепідключитися немає.
- `failed` - підключення не вдалося, повторів не буде.

</div>

<a name="react-vue-socket-id"></a>
#### ID сокета

Отримати поточний ID WebSocket-сокета можна хуком `useSocketId`, який надає реактивне значення, що автоматично оновлюється, коли з'єднання перепідключається з новим ID сокета:

```js tab=React
import { useSocketId } from "@laravel/echo-react";

function SocketIndicator() {
    const socketId = useSocketId();

    return <div>Socket ID: {socketId}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useSocketId } from "@laravel/echo-vue";

const socketId = useSocketId();
</script>

<template>
    <div>Socket ID: {{ socketId }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useSocketId } from "@laravel/echo-svelte";

const socketId = useSocketId();
</script>

<div>Socket ID: {socketId()}</div>
```

<a name="presence-channels"></a>
## Канали присутності

Канали присутності будуються на безпеці приватних каналів, додаючи можливість знати, хто підписаний на канал. Це спрощує створення потужних спільних можливостей - наприклад, сповіщати користувачів, що ту саму сторінку переглядає хтось іще, або показувати список учасників чату.

<a name="authorizing-presence-channels"></a>
### Авторизація каналів присутності

Усі канали присутності є також приватними, тому користувачі мають бути [авторизовані для доступу до них](#authorizing-channels). Проте, описуючи колбеки авторизації для каналів присутності, ви не повертаєте `true`, коли користувач має право приєднатися до каналу. Натомість вам слід повернути масив даних про користувача.

Дані, які повернув колбек авторизації, стануть доступні слухачам подій каналу присутності у вашому застосунку на JavaScript. Якщо користувач не має права приєднатися до каналу присутності, поверніть `false` або `null`:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### Приєднання до каналів присутності

Щоб приєднатися до каналу присутності, скористайтеся методом `join` з Echo. Метод `join` поверне реалізацію `PresenceChannel`, яка, окрім методу `listen`, дозволяє підписатися на події `here`, `joining` та `leaving`.

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
    })
    .joining((user) => {
        console.log(user.name);
    })
    .leaving((user) => {
        console.log(user.name);
    })
    .error((error) => {
        console.error(error);
    });
```

Колбек `here` виконається одразу після успішного приєднання до каналу й отримає масив з інформацією про всіх інших користувачів, які наразі підписані на канал. Метод `joining` виконається, коли до каналу приєднається новий користувач, а метод `leaving` - коли користувач залишить канал. Метод `error` виконається, коли точка автентифікації поверне HTTP-статус, відмінний від 200, або якщо виникне проблема з розбором повернутого JSON.

<a name="broadcasting-to-presence-channels"></a>
### Бродкастинг у канали присутності

Канали присутності можуть отримувати події так само, як публічні чи приватні канали. На прикладі чат-кімнати ми можемо захотіти надсилати події `NewMessage` до каналу присутності кімнати. Для цього повернемо екземпляр `PresenceChannel` з методу `broadcastOn` події:

```php
/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```

Як і з іншими подіями, ви можете скористатися хелпером `broadcast` і методом `toOthers`, щоб виключити поточного користувача з отримувачів бродкасту:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Як і для інших типів подій, слухати події, надіслані до каналів присутності, можна методом `listen` з Echo:

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```

<a name="model-broadcasting"></a>
## Бродкастинг моделей

> [!WARNING]
> Перш ніж читати документацію нижче про бродкастинг моделей, радимо ознайомитися із загальними концепціями сервісів бродкастингу моделей у Laravel, а також із тим, як вручну створювати й слухати події бродкастингу.

Часто буває потрібно надсилати події, коли [моделі Eloquent](/docs/{{version}}/eloquent) вашого застосунку створюються, оновлюються чи видаляються. Звісно, це легко зробити, вручну [описавши власні події для змін стану моделі Eloquent](/docs/{{version}}/eloquent#events) і позначивши ці події інтерфейсом `ShouldBroadcast`.

Проте, якщо ви не використовуєте ці події для чогось іще у своєму застосунку, створювати класи подій лише заради бродкастингу може бути обтяжливо. Щоб зарадити цьому, Laravel дозволяє вказати, що модель Eloquent має автоматично надсилати свої зміни стану.

Для початку ваша модель Eloquent має використовувати трейт `Illuminate\Database\Eloquent\BroadcastsEvents`. Крім того, модель має описати метод `broadcastOn`, який поверне масив каналів, у які слід надсилати події моделі:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

Щойно ваша модель містить цей трейт і описує свої канали бродкастингу, вона почне автоматично надсилати події, коли екземпляр моделі створюється, оновлюється, видаляється, потрапляє в кошик чи відновлюється.

Крім того, ви могли помітити, що метод `broadcastOn` отримує рядковий аргумент `$event`. Цей аргумент містить тип події, що сталася з моделлю, і матиме значення `created`, `updated`, `deleted`, `trashed` або `restored`. Перевіряючи значення цієї змінної, ви можете визначити, у які канали (якщо взагалі в якісь) модель має надсилати конкретну подію:

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>
#### Налаштування створення події бродкастингу моделі

Інколи вам може захотітися змінити те, як Laravel створює подію бродкастингу моделі під капотом. Зробити це можна, описавши в моделі Eloquent метод `newBroadcastableEvent`. Цей метод має повернути екземпляр `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred`:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### Домовленості бродкастингу моделей

<a name="model-broadcasting-channel-conventions"></a>
#### Домовленості щодо каналів

Як ви могли помітити, метод `broadcastOn` у прикладі моделі вище повертав не екземпляри `Channel`. Натомість поверталися самі моделі Eloquent. Якщо метод `broadcastOn` вашої моделі повертає екземпляр моделі Eloquent (або містить його в поверненому масиві), Laravel автоматично створить екземпляр приватного каналу для моделі, використавши як ім'я каналу назву класу моделі та її первинний ключ.

Тож модель `App\Models\User` з `id` `1` перетвориться на екземпляр `Illuminate\Broadcasting\PrivateChannel` з іменем `App.Models.User.1`. Звісно, окрім повернення екземплярів моделей Eloquent із методу `broadcastOn`, ви можете повертати повноцінні екземпляри `Channel`, щоб повністю контролювати імена каналів моделі:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```

Якщо ви плануєте явно повертати екземпляр каналу з методу `broadcastOn` моделі, ви можете передати екземпляр моделі Eloquent у конструктор каналу. У такому разі Laravel скористається домовленостями щодо каналів моделей, описаними вище, щоб перетворити модель Eloquent на рядкове ім'я каналу:

```php
return [new Channel($this->user)];
```

Якщо вам потрібно дізнатися ім'я каналу моделі, викличте метод `broadcastChannel` на будь-якому екземплярі моделі. Наприклад, для моделі `App\Models\User` з `id` `1` цей метод поверне рядок `App.Models.User.1`:

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### Домовленості щодо подій

Оскільки події бродкастингу моделей не пов'язані зі «справжньою» подією в каталозі `App\Events` вашого застосунку, ім'я та дані їм призначаються за домовленостями. Домовленість Laravel така: подія надсилається під назвою класу моделі (без простору імен) і назвою події моделі, яка спричинила бродкаст.

Тож, наприклад, оновлення моделі `App\Models\Post` надішле до вашого клієнтського застосунку подію `PostUpdated` з такими даними:

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```

Видалення моделі `App\Models\User` надішле подію з назвою `UserDeleted`.

За бажанням ви можете описати власні ім'я бродкасту й дані, додавши до моделі методи `broadcastAs` і `broadcastWith`. Ці методи отримують назву події / операції моделі, що відбувається, дозволяючи налаштувати ім'я та дані події для кожної операції з моделлю. Якщо метод `broadcastAs` повертає `null`, надсилаючи подію, Laravel скористається домовленостями щодо імен подій бродкастингу моделей, описаними вище:

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
### Прослуховування бродкастів моделей

Щойно ви додали до моделі трейт `BroadcastsEvents` і описали її метод `broadcastOn`, можна починати слухати надіслані події моделі у клієнтському застосунку. Перш ніж почати, вам може бути корисно переглянути повну документацію про [прослуховування подій](#listening-for-events).

Спершу отримайте екземпляр каналу методом `private`, а потім викличте метод `listen`, щоб слухати вказану подію. Зазвичай ім'я каналу, передане методу `private`, має відповідати [домовленостям бродкастингу моделей](#model-broadcasting-conventions) у Laravel.

Отримавши екземпляр каналу, ви можете слухати конкретну подію методом `listen`. Оскільки події бродкастингу моделей не пов'язані зі «справжньою» подією в каталозі `App\Events` вашого застосунку, [ім'я події](#model-broadcasting-event-conventions) має мати префікс `.`, який вказує, що вона не належить до жодного простору імен. Кожна подія бродкастингу моделі має властивість `model`, яка містить усі властивості моделі, придатні для бродкастингу:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### Використання React, Vue чи Svelte

Якщо ви користуєтеся React, Vue чи Svelte, для зручного прослуховування бродкастів моделей скористайтеся хуком `useEchoModel`, який входить до Laravel Echo:

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

Ви також можете описати форму даних події моделі, отримавши кращу типобезпеку й зручність редагування:

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```

<a name="client-events"></a>
## Клієнтські події

> [!NOTE]
> Користуючись [Pusher Channels](https://pusher.com/channels), ви маєте увімкнути опцію «Client Events» у розділі «App Settings» вашої [панелі застосунку](https://dashboard.pusher.com/), щоб надсилати клієнтські події.

Інколи вам може захотітися надіслати подію іншим підключеним клієнтам, узагалі не звертаючись до застосунку Laravel. Це особливо корисно для речей на кшталт сповіщень «набирає повідомлення», коли ви хочете попередити користувачів застосунку, що інший користувач набирає повідомлення на певному екрані.

Щоб надсилати клієнтські події, скористайтеся методом `whisper` з Echo:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

Щоб слухати клієнтські події, скористайтеся методом `listenForWhisper`:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

<a name="notifications"></a>
## Сповіщення

Поєднавши бродкастинг подій зі [сповіщеннями](/docs/{{version}}/notifications), ваш застосунок на JavaScript зможе отримувати нові сповіщення щойно вони з'являються, без оновлення сторінки. Перш ніж почати, обов'язково прочитайте документацію про [канал сповіщень broadcast](/docs/{{version}}/notifications#broadcast-notifications).

Щойно ви налаштували сповіщення на використання каналу broadcast, слухати події бродкастингу можна методом `notification` з Echo. Пам'ятайте: ім'я каналу має збігатися з назвою класу сутності, яка отримує сповіщення:

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

У цьому прикладі всі сповіщення, надіслані екземплярам `App\Models\User` через канал `broadcast`, отримуватиме колбек. Колбек авторизації каналу `App.Models.User.{id}` уже є у файлі `routes/channels.php` вашого застосунку.

<a name="stop-listening-for-notifications"></a>
#### Припинення прослуховування сповіщень

Якщо ви хочете перестати слухати сповіщення, не [виходячи з каналу](#leaving-a-channel), скористайтеся методом `stopListeningForNotification`:

```js
const callback = (notification) => {
    console.log(notification.type);
}

// Start listening...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// Stop listening (callback must be the same)...
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
