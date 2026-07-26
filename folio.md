---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Folio

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Шляхи сторінок / URI](#page-paths-uris)
    - [Маршрутизація за піддоменом](#subdomain-routing)
- [Створення маршрутів](#creating-routes)
    - [Вкладені маршрути](#nested-routes)
    - [Індексні маршрути](#index-routes)
- [Параметри маршруту](#route-parameters)
- [Прив'язка моделей до маршруту](#route-model-binding)
    - [М'яко видалені моделі](#soft-deleted-models)
- [Хуки рендерингу](#render-hooks)
- [Іменовані маршрути](#named-routes)
- [Middleware](#middleware)
- [Кешування маршрутів](#route-caching)

<a name="introduction"></a>
## Вступ

[Laravel Folio](https://github.com/laravel/folio) - це потужний посторінковий маршрутизатор, створений, щоб спростити маршрутизацію в Laravel-застосунках. З Laravel Folio створити маршрут так само легко, як створити Blade-шаблон у каталозі `resources/views/pages` вашого застосунку.

Наприклад, щоб створити сторінку, доступну за URL `/greeting`, просто створіть файл `greeting.blade.php` у каталозі `resources/views/pages` вашого застосунку:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## Встановлення

Для початку встановіть Folio у свій проєкт за допомогою менеджера пакетів Composer:

```shell
composer require laravel/folio
```

Після встановлення Folio ви можете виконати артизан-команду `folio:install`, яка встановить сервіс-провайдер Folio у ваш застосунок. Цей провайдер реєструє каталог, у якому Folio шукатиме маршрути / сторінки:

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
### Шляхи сторінок / URI

За замовчуванням Folio віддає сторінки з каталогу `resources/views/pages` вашого застосунку, але ви можете змінити ці каталоги в методі `boot` вашого сервіс-провайдера Folio.

Наприклад, іноді буває зручно вказати кілька шляхів Folio у тому самому Laravel-застосунку. Можливо, ви захочете мати окремий каталог сторінок Folio для «адмінки» вашого застосунку, а для решти сторінок використовувати інший каталог.

Зробити це можна за допомогою методів `Folio::path` і `Folio::uri`. Метод `path` реєструє каталог, який Folio скануватиме в пошуках сторінок під час маршрутизації вхідних HTTP-запитів, а метод `uri` задає «базовий URI» для цього каталогу сторінок:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages/guest'))->uri('/');

Folio::path(resource_path('views/pages/admin'))
    ->uri('/admin')
    ->middleware([
        '*' => [
            'auth',
            'verified',

            // ...
        ],
    ]);
```

<a name="subdomain-routing"></a>
### Маршрутизація за піддоменом

Ви також можете маршрутизувати до сторінок на основі піддомену вхідного запиту. Наприклад, ви можете захотіти спрямувати запити з `admin.example.com` до іншого каталогу сторінок, ніж решта ваших сторінок Folio. Зробити це можна, викликавши метод `domain` після виклику методу `Folio::path`:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

Метод `domain` також дозволяє захоплювати частини домену чи піддомену як параметри. Ці параметри будуть передані до шаблону вашої сторінки:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## Створення маршрутів

Створити маршрут Folio можна, розмістивши Blade-шаблон у будь-якому з підключених до Folio каталогів. За замовчуванням Folio підключає каталог `resources/views/pages`, але ви можете змінити ці каталоги в методі `boot` вашого сервіс-провайдера Folio.

Щойно Blade-шаблон опиниться в підключеному до Folio каталозі, ви одразу зможете відкрити його у браузері. Наприклад, сторінка, розміщена в `pages/schedule.blade.php`, буде доступна у браузері за адресою `http://example.com/schedule`.

Щоб швидко переглянути список усіх ваших сторінок / маршрутів Folio, скористайтеся артизан-командою `folio:list`:

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
### Вкладені маршрути

Вкладений маршрут створюється створенням одного чи кількох каталогів усередині одного з каталогів Folio. Наприклад, щоб створити сторінку, доступну за `/user/profile`, створіть шаблон `profile.blade.php` у каталозі `pages/user`:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### Індексні маршрути

Іноді вам може знадобитися зробити певну сторінку «індексом» каталогу. Якщо розмістити шаблон `index.blade.php` у каталозі Folio, будь-які запити до кореня цього каталогу будуть спрямовані на цю сторінку:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## Параметри маршруту

Часто вам потрібно, щоб сегменти URL вхідного запиту передавалися до сторінки, аби ви могли з ними працювати. Наприклад, вам може знадобитися доступ до «ID» користувача, чий профіль показується. Для цього візьміть сегмент імені файлу сторінки у квадратні дужки:

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

Захоплені сегменти доступні як змінні у вашому Blade-шаблоні:

```html
<div>
    User {{ $id }}
</div>
```

Щоб захопити кілька сегментів, додайте перед узятим у дужки сегментом три крапки `...`:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

Коли захоплюється кілька сегментів, вони передаються до сторінки як масив:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## Прив'язка моделей до маршруту

Якщо сегмент-підстановка в імені файлу шаблону сторінки відповідає одній з Eloquent-моделей вашого застосунку, Folio автоматично скористається можливостями прив'язки моделей до маршруту в Laravel і спробує передати до сторінки знайдений екземпляр моделі:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

Захоплені моделі доступні як змінні у вашому Blade-шаблоні. Ім'я змінної моделі буде переведене в «camel case»:

```html
<div>
    User {{ $user->id }}
</div>
```

#### Зміна ключа

Іноді вам може знадобитися знаходити прив'язані Eloquent-моделі за колонкою, відмінною від `id`. Для цього вкажіть колонку в імені файлу сторінки. Наприклад, сторінка з іменем файлу `[Post:slug].blade.php` шукатиме прив'язану модель за колонкою `slug`, а не `id`.

У Windows для відокремлення імені моделі від ключа слід використовувати `-`: `[Post-slug].blade.php`.

#### Розташування моделі

За замовчуванням Folio шукатиме вашу модель у каталозі `app/Models` вашого застосунку. Однак за потреби ви можете вказати повністю кваліфіковане ім'я класу моделі в імені файлу шаблону:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### М'яко видалені моделі

За замовчуванням м'яко видалені моделі не знаходяться під час неявної прив'язки моделей. Однак, якщо хочете, ви можете вказати Folio знаходити м'яко видалені моделі, викликавши функцію `withTrashed` у шаблоні сторінки:

```php
<?php

use function Laravel\Folio\{withTrashed};

withTrashed();

?>

<div>
    User {{ $user->id }}
</div>
```

<a name="render-hooks"></a>
## Хуки рендерингу

За замовчуванням Folio повертає вміст Blade-шаблону сторінки як відповідь на вхідний запит. Однак ви можете змінити відповідь, викликавши функцію `render` у шаблоні сторінки.

Функція `render` приймає замикання, яке отримає екземпляр `View`, що його рендерить Folio, - це дозволяє додати до представлення додаткові дані або повністю змінити відповідь. Окрім екземпляра `View`, до замикання `render` також передаються будь-які додаткові параметри маршруту чи прив'язані моделі:

```php
<?php

use App\Models\Post;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

use function Laravel\Folio\render;

render(function (View $view, Post $post) {
    if (! Auth::user()->can('view', $post)) {
        return response('Unauthorized', 403);
    }

    return $view->with('photos', $post->author->photos);
}); ?>

<div>
    {{ $post->content }}
</div>

<div>
    This author has also taken {{ count($photos) }} photos.
</div>
```

<a name="named-routes"></a>
## Іменовані маршрути

Задати ім'я маршруту певної сторінки можна за допомогою функції `name`:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Так само як і з іменованими маршрутами Laravel, ви можете скористатися функцією `route`, щоб згенерувати URL до сторінок Folio, яким призначено ім'я:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

Якщо сторінка має параметри, просто передайте їхні значення до функції `route`:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## Middleware

Застосувати `middleware` до конкретної сторінки можна, викликавши функцію `middleware` у шаблоні сторінки:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

Або, щоб призначити `middleware` групі сторінок, додайте метод `middleware` ланцюжком після виклику методу `Folio::path`.

Щоб указати, до яких саме сторінок слід застосувати `middleware`, ключами масиву `middleware` можуть бути відповідні URL-шаблони сторінок, до яких їх треба застосувати. Символ `*` можна використовувати як символ-підстановку:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        // ...
    ],
]);
```

До масиву `middleware` можна додавати замикання, щоб визначити вбудовані анонімні `middleware`:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        function (Request $request, Closure $next) {
            // ...

            return $next($request);
        },
    ],
]);
```

<a name="route-caching"></a>
## Кешування маршрутів

Використовуючи Folio, вам завжди варто користуватися [можливостями кешування маршрутів Laravel](/docs/{{version}}/routing#route-caching). Folio слухає артизан-команду `route:cache`, щоб гарантувати, що визначення сторінок і імена маршрутів Folio будуть належно закешовані для максимальної продуктивності.
