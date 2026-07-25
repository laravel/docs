---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Контролери

- [Вступ](#introduction)
- [Написання контролерів](#writing-controllers)
    - [Базові контролери](#basic-controllers)
    - [Контролери однієї дії](#single-action-controllers)
- [Middleware контролерів](#controller-middleware)
    - [Атрибути middleware](#middleware-attributes)
    - [Атрибути авторизації](#authorization-attributes)
- [Ресурсні контролери](#resource-controllers)
    - [Часткові ресурсні маршрути](#restful-partial-resource-routes)
    - [Вкладені ресурси](#restful-nested-resources)
    - [Іменування ресурсних маршрутів](#restful-naming-resource-routes)
    - [Іменування параметрів ресурсних маршрутів](#restful-naming-resource-route-parameters)
    - [Обмеження області ресурсних маршрутів](#restful-scoping-resource-routes)
    - [Локалізація URI ресурсів](#restful-localizing-resource-uris)
    - [Доповнення ресурсних контролерів](#restful-supplementing-resource-controllers)
    - [Синглтон-ресурсні контролери](#singleton-resource-controllers)
    - [Middleware та ресурсні контролери](#middleware-and-resource-controllers)
- [Впровадження залежностей і контролери](#dependency-injection-and-controllers)

<a name="introduction"></a>
## Вступ

Замість визначати всю логіку обробки запитів замиканнями у файлах маршрутів, ви можете організувати цю поведінку класами-«контролерами». Контролери групують пов'язану логіку обробки запитів в одному класі. Наприклад, клас `UserController` може обробляти всі вхідні запити, пов'язані з користувачами: показ, створення, оновлення та видалення. За замовчуванням контролери зберігаються в каталозі `app/Http/Controllers`.

<a name="writing-controllers"></a>
## Написання контролерів

<a name="basic-controllers"></a>
### Базові контролери

Щоб швидко згенерувати новий контролер, виконайте команду Artisan `make:controller`. За замовчуванням усі контролери вашого застосунку зберігаються в каталозі `app/Http/Controllers`:

```shell
php artisan make:controller UserController
```

Погляньмо на приклад базового контролера. Контролер може мати будь-яку кількість публічних методів, які відповідатимуть на вхідні HTTP-запити:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Написавши клас контролера та метод, ви можете визначити маршрут до методу контролера так:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

Коли вхідний запит збігається з указаним URI маршруту, буде викликано метод `show` класу `App\Http\Controllers\UserController`, а параметри маршруту буде передано методу.

> [!NOTE]
> Контролери **не зобов'язані** успадковувати базовий клас. Утім, іноді зручно успадкувати базовий контролер із методами, спільними для всіх ваших контролерів.

<a name="single-action-controllers"></a>
### Контролери однієї дії

Якщо дія контролера особливо складна, вам може бути зручно виділити для неї цілий клас контролера. Для цього визначте в контролері єдиний метод `__invoke`:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     */
    public function __invoke()
    {
        // ...
    }
}
```

Реєструючи маршрути для контролерів однієї дії, вам не потрібно вказувати метод контролера. Натомість просто передайте маршрутизатору ім'я контролера:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

Ви можете згенерувати викликаний контролер за допомогою опції `--invokable` команди Artisan `make:controller`:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> Заготовки контролерів можна налаштувати через [публікацію заготовок](/docs/{{version}}/artisan#stub-customization).

<a name="controller-middleware"></a>
## Middleware контролерів

[`Middleware`](/docs/{{version}}/middleware) можна призначати маршрутам контролера у файлах маршрутів:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

Або ж вам може бути зручно вказати `middleware` у самому класі контролера. Для цього ваш контролер має реалізувати інтерфейс `HasMiddleware`, який вимагає наявності статичного методу `middleware`. З цього методу ви можете повернути масив `middleware`, які слід застосувати до дій контролера:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    /**
     * Get the middleware that should be assigned to the controller.
     */
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }

    // ...
}
```

Ви також можете визначати `middleware` контролера як замикання - це зручний спосіб задати вбудований `middleware`, не пишучи цілого класу:

```php
use Closure;
use Illuminate\Http\Request;

/**
 * Get the middleware that should be assigned to the controller.
 */
public static function middleware(): array
{
    return [
        function (Request $request, Closure $next) {
            return $next($request);
        },
    ];
}
```

<a name="middleware-attributes"></a>
### Атрибути middleware

Ви також можете призначати `middleware` контролерам за допомогою атрибутів PHP:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
#[Middleware('log', only: ['index'])]
#[Middleware('subscribed', except: ['store'])]
class UserController
{
    // ...
}
```

Атрибути `middleware` можна розміщувати й на окремих методах контролера. `Middleware`, призначені методам, буде об'єднано з тими, що призначені на рівні класу:

```php
<?php

namespace App\Http\Controllers;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class UserController
{
    #[Middleware('log')]
    #[Middleware('subscribed')]
    public function index()
    {
        // ...
    }

    #[Middleware(static function (Request $request, Closure $next) {
        // ...

        return $next($request);
    })]
    public function store()
    {
        // ...
    }
}
```

Щоб виключити `middleware` з контролера чи окремих його методів, скористайтеся атрибутом `WithoutMiddleware`. Аргументи `only` та `except` дозволяють обмежити атрибут рівня класу конкретними методами:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Middleware\EnsureTokenIsValid;
use Illuminate\Routing\Attributes\Controllers\WithoutMiddleware;

#[WithoutMiddleware('subscribed', except: ['index'])]
class UserController
{
    #[WithoutMiddleware(EnsureTokenIsValid::class)]
    public function index()
    {
        // ...
    }

    public function show()
    {
        // ...
    }
}
```

Атрибути `WithoutMiddleware` рівня класу успадковуються дочірніми контролерами. Атрибут може прибирати лише `middleware` маршрутів і не діє на [глобальні `middleware`](/docs/{{version}}/middleware#global-middleware).

<a name="authorization-attributes"></a>
### Атрибути авторизації

Якщо ви авторизуєте дії контролера через політики, скористайтеся атрибутом `Authorize` як зручним скороченням для `middleware` `can`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;

class CommentController
{
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }

    #[Authorize('delete', 'comment')]
    public function destroy(Comment $comment)
    {
        // ...
    }
}
```

Перший аргумент - здатність (ability), яку ви хочете авторизувати. Другий - клас моделі, параметр маршруту чи параметри, які слід передати політиці.

<a name="resource-controllers"></a>
## Ресурсні контролери

Якщо уявляти кожну модель Eloquent у вашому застосунку як «ресурс», то типово над кожним ресурсом виконуються одні й ті самі набори дій. Наприклад, уявіть, що ваш застосунок містить моделі `Photo` і `Movie`. Найімовірніше, користувачі можуть створювати, читати, оновлювати чи видаляти ці ресурси.

Через цей поширений сценарій ресурсна маршрутизація Laravel призначає контролеру типові маршрути створення, читання, оновлення та видалення («CRUD») одним рядком коду. Щоб почати, скористаймося опцією `--resource` команди Artisan `make:controller`, аби швидко створити контролер для цих дій:

```shell
php artisan make:controller PhotoController --resource
```

Ця команда згенерує контролер за шляхом `app/Http/Controllers/PhotoController.php`. Контролер міститиме метод для кожної доступної операції над ресурсом. Далі ви можете зареєструвати ресурсний маршрут, що вказує на контролер:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

Це єдине оголошення маршруту створює кілька маршрутів для різних дій над ресурсом. Згенерований контролер уже матиме заготовки методів для кожної з цих дій. Пам'ятайте: ви завжди можете швидко переглянути маршрути свого застосунку командою Artisan `route:list`.

Ви навіть можете зареєструвати багато ресурсних контролерів одразу, передавши масив методу `resources`:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

Метод `softDeletableResources` реєструє багато ресурсних контролерів, які всі використовують метод `withTrashed`:

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### Дії, які обробляють ресурсні контролери

<div class="overflow-auto">

| Метод     | URI                    | Дія     | Ім'я маршруту  |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

</div>

<a name="customizing-missing-model-behavior"></a>
#### Налаштування поведінки для відсутньої моделі

Зазвичай, якщо неявно прив'язану модель ресурсу не знайдено, генерується HTTP-відповідь 404. Утім, ви можете налаштувати цю поведінку, викликавши метод `missing` під час визначення ресурсного маршруту. Метод `missing` приймає замикання, яке буде викликано, якщо неявно прив'язану модель не вдалося знайти для будь-якого з маршрутів ресурсу:

```php
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
    ->missing(function (Request $request) {
        return Redirect::route('photos.index');
    });
```

<a name="soft-deleted-models"></a>
#### М'яко видалені моделі

Зазвичай неявна прив'язка моделей не отримує [м'яко видалені](/docs/{{version}}/eloquent#soft-deleting) моделі, а натомість повертає HTTP-відповідь 404. Однак ви можете вказати фреймворку дозволити м'яко видалені моделі, викликавши метод `withTrashed` під час визначення ресурсного маршруту:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

Виклик `withTrashed` без аргументів дозволить м'яко видалені моделі для ресурсних маршрутів `show`, `edit` та `update`. Ви можете вказати підмножину цих маршрутів, передавши масив методу `withTrashed`:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### Вказання моделі ресурсу

Якщо ви використовуєте [прив'язку моделей до маршрутів](/docs/{{version}}/routing#route-model-binding) і хочете, щоб методи ресурсного контролера вказували тип екземпляра моделі, скористайтеся опцією `--model` під час генерації контролера:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### Генерація запитів форм

Ви можете передати опцію `--requests` під час генерації ресурсного контролера, щоб Artisan згенерував [класи запитів форм](/docs/{{version}}/validation#form-request-validation) для методів збереження та оновлення:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### Часткові ресурсні маршрути

Оголошуючи ресурсний маршрут, ви можете вказати підмножину дій, які має обробляти контролер, замість повного набору типових дій:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->only([
    'index', 'show'
]);

Route::resource('photos', PhotoController::class)->except([
    'create', 'store', 'update', 'destroy'
]);
```

<a name="api-resource-routes"></a>
#### Ресурсні маршрути API

Оголошуючи ресурсні маршрути, які споживатимуть API, ви зазвичай захочете виключити маршрути, що показують HTML-шаблони, - як-от `create` та `edit`. Для зручності скористайтеся методом `apiResource`, який автоматично виключає ці два маршрути:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

Ви можете зареєструвати багато ресурсних контролерів API одразу, передавши масив методу `apiResources`:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

Щоб швидко згенерувати ресурсний контролер API без методів `create` та `edit`, скористайтеся перемикачем `--api` під час виконання команди `make:controller`:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### Вкладені ресурси

Іноді вам може знадобитися визначити маршрути до вкладеного ресурсу. Наприклад, ресурс фотографії може мати кілька коментарів, прикріплених до неї. Щоб вкласти ресурсні контролери, скористайтеся «крапковою» нотацією в оголошенні маршруту:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

Цей маршрут зареєструє вкладений ресурс, доступний за URI на кшталт такого:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### Обмеження області вкладених ресурсів

Можливість [неявної прив'язки моделей](/docs/{{version}}/routing#implicit-model-binding-scoping) Laravel може автоматично обмежувати область вкладених прив'язок так, щоб розв'язана дочірня модель гарантовано належала батьківській. Скориставшись методом `scoped` під час визначення вкладеного ресурсу, ви можете увімкнути автоматичне обмеження області, а також вказати Laravel, за яким полем слід отримувати дочірній ресурс. Докладніше про це дивіться в документації з [обмеження області ресурсних маршрутів](#restful-scoping-resource-routes).

<a name="shallow-nesting"></a>
#### Поверхневе вкладення

Часто мати в URI одночасно ідентифікатори батька й дитини зовсім не обов'язково, адже ідентифікатор дитини вже унікальний. Використовуючи унікальні ідентифікатори на кшталт автоінкрементних первинних ключів для позначення моделей у сегментах URI, ви можете обрати «поверхневе вкладення»:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

Це визначення маршруту створить такі маршрути:

<div class="overflow-auto">

| Метод     | URI                               | Дія     | Ім'я маршруту          |
| --------- | --------------------------------- | ------- | ---------------------- |
| GET       | `/photos/{photo}/comments`        | index   | photos.comments.index  |
| GET       | `/photos/{photo}/comments/create` | create  | photos.comments.create |
| POST      | `/photos/{photo}/comments`        | store   | photos.comments.store  |
| GET       | `/comments/{comment}`             | show    | comments.show          |
| GET       | `/comments/{comment}/edit`        | edit    | comments.edit          |
| PUT/PATCH | `/comments/{comment}`             | update  | comments.update        |
| DELETE    | `/comments/{comment}`             | destroy | comments.destroy       |

</div>

<a name="restful-naming-resource-routes"></a>
### Іменування ресурсних маршрутів

За замовчуванням усі дії ресурсного контролера мають ім'я маршруту; утім, ви можете перевизначити ці імена, передавши масив `names` із бажаними іменами:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### Іменування параметрів ресурсних маршрутів

За замовчуванням `Route::resource` створює параметри ваших ресурсних маршрутів на основі форми однини від імені ресурсу. Ви можете легко перевизначити це для кожного ресурсу окремо методом `parameters`. Масив, переданий методу `parameters`, має бути асоціативним масивом імен ресурсів та імен параметрів:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

Наведений вище приклад генерує такий URI для маршруту `show` цього ресурсу:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### Обмеження області ресурсних маршрутів

Можливість [неявної прив'язки моделей з обмеженням області](/docs/{{version}}/routing#implicit-model-binding-scoping) Laravel може автоматично обмежувати область вкладених прив'язок так, щоб розв'язана дочірня модель гарантовано належала батьківській. Скориставшись методом `scoped` під час визначення вкладеного ресурсу, ви можете увімкнути автоматичне обмеження області, а також вказати Laravel, за яким полем слід отримувати дочірній ресурс:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

Цей маршрут зареєструє вкладений ресурс з обмеженою областю, доступний за URI на кшталт такого:

```text
/photos/{photo}/comments/{comment:slug}
```

Коли ви використовуєте неявну прив'язку з власним ключем як параметр вкладеного маршруту, Laravel автоматично обмежить запит так, щоб отримати вкладену модель через її батька, використовуючи домовленості для вгадування імені зв'язку на батьківській моделі. У цьому випадку припускатиметься, що модель `Photo` має зв'язок `comments` (множина від імені параметра маршруту), через який можна отримати модель `Comment`.

<a name="restful-localizing-resource-uris"></a>
### Локалізація URI ресурсів

За замовчуванням `Route::resource` створює URI ресурсів, використовуючи англійські дієслова та правила множини. Якщо вам потрібно локалізувати дієслова дій `create` та `edit`, скористайтеся методом `Route::resourceVerbs`. Це можна зробити на початку методу `boot` у `App\Providers\AppServiceProvider` вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

Плюралізатор Laravel підтримує [кілька різних мов, які ви можете налаштувати за потреби](/docs/{{version}}/localization#pluralization-language). Щойно дієслова та мову множини налаштовано, реєстрація ресурсного маршруту на кшталт `Route::resource('publicacion', PublicacionController::class)` створить такі URI:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### Доповнення ресурсних контролерів

Якщо вам потрібно додати до ресурсного контролера маршрути поза типовим набором ресурсних маршрутів, визначайте їх **до** виклику методу `Route::resource`; інакше маршрути, визначені методом `resource`, можуть ненавмисно взяти гору над вашими додатковими маршрутами:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> Пам'ятайте: тримайте свої контролери зосередженими. Якщо ви регулярно потребуєте методів поза типовим набором ресурсних дій, подумайте про поділ контролера на два менші.

<a name="singleton-resource-controllers"></a>
### Синглтон-ресурсні контролери

Іноді ваш застосунок матиме ресурси, які можуть існувати лише в одному екземплярі. Наприклад, «профіль» користувача можна редагувати чи оновлювати, але користувач не може мати більш ніж один «профіль». Так само зображення може мати одну «мініатюру». Такі ресурси називають «синглтон-ресурсами»: існує один і тільки один екземпляр ресурсу. У цих сценаріях ви можете зареєструвати «синглтон»-ресурсний контролер:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

Наведене вище визначення синглтон-ресурсу зареєструє такі маршрути. Як бачите, маршрути «створення» для синглтон-ресурсів не реєструються, а зареєстровані маршрути не приймають ідентифікатора, адже може існувати лише один екземпляр ресурсу:

<div class="overflow-auto">

| Метод     | URI             | Дія    | Ім'я маршруту  |
| --------- | --------------- | ------ | -------------- |
| GET       | `/profile`      | show   | profile.show   |
| GET       | `/profile/edit` | edit   | profile.edit   |
| PUT/PATCH | `/profile`      | update | profile.update |

</div>

Синглтон-ресурси можна також вкладати у стандартний ресурс:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

У цьому прикладі ресурс `photos` отримає всі [стандартні ресурсні маршрути](#actions-handled-by-resource-controllers); однак ресурс `thumbnail` буде синглтон-ресурсом із такими маршрутами:

<div class="overflow-auto">

| Метод     | URI                              | Дія    | Ім'я маршруту           |
| --------- | -------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
#### Синглтон-ресурси зі створенням

Подекуди ви можете захотіти визначити маршрути створення та збереження для синглтон-ресурсу. Для цього викличте метод `creatable` під час реєстрації маршруту синглтон-ресурсу:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

У цьому прикладі буде зареєстровано такі маршрути. Як бачите, для синглтон-ресурсів зі створенням реєструється також маршрут `DELETE`:

<div class="overflow-auto">

| Метод     | URI                                | Дія     | Ім'я маршруту            |
| --------- | ---------------------------------- | ------- | ------------------------ |
| GET       | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy |

</div>

Якщо ви хочете, щоб Laravel зареєстрував для синглтон-ресурсу маршрут `DELETE`, але не реєстрував маршрутів створення чи збереження, скористайтеся методом `destroyable`:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### Синглтон-ресурси API

Метод `apiSingleton` дозволяє зареєструвати синглтон-ресурс, яким керуватимуть через API, роблячи маршрути `create` та `edit` непотрібними:

```php
Route::apiSingleton('profile', ProfileController::class);
```

Звісно, синглтон-ресурси API також можуть бути `creatable`, що зареєструє для ресурсу маршрути `store` та `destroy`:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```
<a name="middleware-and-resource-controllers"></a>
### Middleware та ресурсні контролери

Laravel дозволяє призначати `middleware` всім або лише певним методам ресурсних маршрутів за допомогою методів `middleware`, `middlewareFor` і `withoutMiddlewareFor`. Ці методи дають тонкий контроль над тим, який `middleware` застосовується до кожної ресурсної дії.

#### Застосування middleware до всіх методів

Скористайтеся методом `middleware`, щоб призначити `middleware` всім маршрутам, згенерованим ресурсним чи синглтон-ресурсним маршрутом:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### Застосування middleware до конкретних методів

Скористайтеся методом `middlewareFor`, щоб призначити `middleware` одному чи кільком конкретним методам ресурсного контролера:

```php
Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```

Метод `middlewareFor` можна також використовувати разом із синглтон-ресурсними контролерами та їхніми API-варіантами:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### Виключення middleware з конкретних методів

Скористайтеся методом `withoutMiddlewareFor`, щоб виключити `middleware` з конкретних методів ресурсного контролера:

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

<a name="dependency-injection-and-controllers"></a>
## Впровадження залежностей і контролери

<a name="constructor-injection"></a>
#### Впровадження через конструктор

[Сервіс-контейнер](/docs/{{version}}/container) Laravel використовується для розв'язання всіх контролерів Laravel. Завдяки цьому ви можете вказати типи будь-яких потрібних контролеру залежностей у його конструкторі. Оголошені залежності буде автоматично розв'язано й впроваджено в екземпляр контролера:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### Впровадження через метод

Крім впровадження через конструктор, ви можете вказувати типи залежностей у методах контролера. Поширений сценарій - впровадження екземпляра `Illuminate\Http\Request` у методи контролера:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // Store the user...

        return redirect('/users');
    }
}
```

Якщо ваш метод контролера також очікує вхідні дані з параметра маршруту, перелічуйте аргументи маршруту після інших залежностей. Наприклад, якщо ваш маршрут визначено так:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

Ви все одно можете вказати тип `Illuminate\Http\Request` і звертатися до параметра `id`, визначивши метод контролера так:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```
