---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Авторизація

- [Вступ](#introduction)
- [Гейти](#gates)
    - [Написання гейтів](#writing-gates)
    - [Авторизація дій](#authorizing-actions-via-gates)
    - [Відповіді гейтів](#gate-responses)
    - [Перехоплення перевірок гейтів](#intercepting-gate-checks)
    - [Вбудована авторизація](#inline-authorization)
- [Створення політик](#creating-policies)
    - [Генерування політик](#generating-policies)
    - [Реєстрація політик](#registering-policies)
- [Написання політик](#writing-policies)
    - [Методи політик](#policy-methods)
    - [Відповіді політик](#policy-responses)
    - [Методи без моделей](#methods-without-models)
    - [Гості](#guest-users)
    - [Фільтри політик](#policy-filters)
- [Авторизація дій через політики](#authorizing-actions-using-policies)
    - [Через модель User](#via-the-user-model)
    - [Через фасад Gate](#via-the-gate-facade)
    - [Через middleware](#via-middleware)
    - [Через Blade-шаблони](#via-blade-templates)
    - [Передавання додаткового контексту](#supplying-additional-context)
- [Авторизація та Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## Вступ

Окрім вбудованих сервісів [автентифікації](/docs/{{version}}/authentication), Laravel надає простий спосіб авторизувати дії користувача щодо заданого ресурсу. Наприклад, навіть якщо користувач автентифікований, він може не мати права оновлювати чи видаляти певні моделі Eloquent або записи в базі даних, якими керує ваш застосунок. Можливості авторизації Laravel дають простий і впорядкований спосіб керувати такими перевірками.

Laravel пропонує два основні способи авторизації дій: [гейти](#gates) та [політики](#creating-policies). Уявіть гейти й політики як маршрути та контролери. Гейти дають простий підхід до авторизації на замиканнях, тоді як політики, подібно до контролерів, групують логіку навколо певної моделі чи ресурсу. У цій документації ми спершу розглянемо гейти, а потім - політики.

Будуючи застосунок, вам не обов'язково обирати щось одне - лише гейти чи лише політики. Більшість застосунків, найімовірніше, поєднуватимуть і те, і те, і це цілком нормально! Гейти найкраще пасують до дій, не пов'язаних із жодною моделлю чи ресурсом, - наприклад, перегляд адміністративної панелі. Натомість політики варто застосовувати, коли ви хочете авторизувати дію щодо конкретної моделі чи ресурсу.

<a name="gates"></a>
## Гейти

<a name="writing-gates"></a>
### Написання гейтів

> [!WARNING]
> Гейти - чудовий спосіб опанувати основи авторизації в Laravel; проте, будуючи серйозні застосунки Laravel, вам варто розглянути [політики](#creating-policies) для впорядкування правил авторизації.

Гейти - це просто замикання, які визначають, чи має користувач право виконати задану дію. Зазвичай гейти визначають у методі `boot` класу `App\Providers\AppServiceProvider` через фасад `Gate`. Гейти завжди отримують першим аргументом екземпляр користувача й можуть за бажанням приймати додаткові аргументи - наприклад, відповідну модель Eloquent.

У цьому прикладі ми визначимо гейт, який вирішує, чи може користувач оновити задану модель `App\Models\Post`. Гейт зробить це, порівнявши `id` користувача з `user_id` того, хто створив допис:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

Як і контролери, гейти можна визначати масивом-колбеком класу:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### Авторизація дій

Щоб авторизувати дію через гейти, скористайтеся методами `allows` чи `denies`, які надає фасад `Gate`. Зверніть увагу: передавати цим методам поточного автентифікованого користувача не потрібно - Laravel сам подбає про передавання користувача в замикання гейта. Зазвичай методи авторизації гейта викликають у контролерах вашого застосунку перед виконанням дії, що вимагає авторизації:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

Якщо ви хочете визначити, чи має право виконати дію користувач, відмінний від поточного автентифікованого, скористайтеся методом `forUser` на фасаді `Gate`:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

Ви можете авторизувати кілька дій одночасно методами `any` чи `none`:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### Авторизація з киданням винятків

Якщо ви хочете спробувати авторизувати дію й автоматично кинути виняток `Illuminate\Auth\Access\AuthorizationException`, коли користувачеві не дозволено її виконати, скористайтеся методом `authorize` фасада `Gate`. Laravel автоматично перетворює екземпляри `AuthorizationException` на HTTP-відповідь 403:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
#### Передавання додаткового контексту

Методи гейтів для авторизації можливостей (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) та [директиви Blade](#via-blade-templates) для авторизації (`@can`, `@cannot`, `@canany`) можуть приймати масив другим аргументом. Елементи цього масиву передаються параметрами до замикання гейта й можуть слугувати додатковим контекстом при ухваленні рішень щодо авторизації:

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, bool $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // The user can create the post...
}
```

<a name="gate-responses"></a>
### Відповіді гейтів

Досі ми розглядали лише гейти, що повертають прості булеві значення. Проте іноді вам може знадобитися повернути докладнішу відповідь із повідомленням про помилку. Для цього поверніть із гейта `Illuminate\Auth\Access\Response`:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('You must be an administrator.');
});
```

Навіть коли ви повертаєте з гейта відповідь авторизації, метод `Gate::allows` усе одно поверне просте булеве значення; проте ви можете скористатися методом `Gate::inspect`, щоб отримати повну відповідь авторизації, яку повернув гейт:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

Коли ви користуєтеся методом `Gate::authorize`, який кидає `AuthorizationException`, якщо дію не авторизовано, повідомлення про помилку з відповіді авторизації буде передано до HTTP-відповіді:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
#### Налаштування статусу HTTP-відповіді

Коли гейт відхиляє дію, повертається HTTP-відповідь `403`; проте іноді буває корисно повернути інший код статусу HTTP. Ви можете налаштувати код статусу HTTP для невдалої перевірки авторизації через статичний конструктор `denyWithStatus` класу `Illuminate\Auth\Access\Response`:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```

Оскільки приховування ресурсів відповіддю `404` - дуже поширений патерн у вебзастосунках, для зручності пропонується метод `denyAsNotFound`:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyAsNotFound();
});
```

<a name="intercepting-gate-checks"></a>
### Перехоплення перевірок гейтів

Іноді вам може знадобитися надати конкретному користувачеві всі можливості. Скористайтеся методом `before`, щоб визначити замикання, яке виконується перед усіма іншими перевірками авторизації:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

Якщо замикання `before` поверне результат, відмінний від null, саме він вважатиметься результатом перевірки авторизації.

Метод `after` дозволяє визначити замикання, яке виконується після всіх інших перевірок авторизації:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

Значення, повернені замиканнями `after`, не перевизначать результат перевірки авторизації, якщо тільки гейт чи політика не повернули `null`.

<a name="inline-authorization"></a>
### Вбудована авторизація

Іноді вам може знадобитися визначити, чи має поточний автентифікований користувач право виконати задану дію, не пишучи для неї окремого гейта. Laravel дозволяє робити такі «вбудовані» перевірки авторизації методами `Gate::allowIf` та `Gate::denyIf`. Вбудована авторизація не виконує жодних визначених [хуків авторизації «before» чи «after»](#intercepting-gate-checks):

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

Якщо дію не авторизовано або якщо наразі жоден користувач не автентифікований, Laravel автоматично кине виняток `Illuminate\Auth\Access\AuthorizationException`. Обробник винятків Laravel автоматично перетворює екземпляри `AuthorizationException` на HTTP-відповідь 403.

<a name="creating-policies"></a>
## Створення політик

<a name="generating-policies"></a>
### Генерування політик

Політики - це класи, що впорядковують логіку авторизації навколо певної моделі чи ресурсу. Наприклад, якщо ваш застосунок - це блог, у вас може бути модель `App\Models\Post` і відповідна `App\Policies\PostPolicy` для авторизації дій користувача на кшталт створення чи оновлення дописів.

Згенерувати політику можна артизан-командою `make:policy`. Згенерована політика потрапить до каталогу `app/Policies`. Якщо цього каталогу у вашому застосунку немає, Laravel створить його за вас:

```shell
php artisan make:policy PostPolicy
```

Команда `make:policy` згенерує порожній клас політики. Якщо ви хочете згенерувати клас із прикладами методів політики для перегляду, створення, оновлення та видалення ресурсу, додайте до команди опцію `--model`:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### Реєстрація політик

<a name="policy-discovery"></a>
#### Автоматичний пошук політик

За замовчуванням Laravel автоматично знаходить політики, якщо модель і політика дотримуються стандартних угод іменування Laravel. Зокрема, політики мають бути в каталозі `Policies` на рівні каталогу з вашими моделями або вище. Тож, наприклад, моделі можуть лежати в каталозі `app/Models`, а політики - у `app/Policies`. У цьому випадку Laravel шукатиме політики спершу в `app/Models/Policies`, а потім у `app/Policies`. Крім того, ім'я політики має збігатися з іменем моделі та мати суфікс `Policy`. Тож моделі `User` відповідатиме клас політики `UserPolicy`.

Якщо ви хочете описати власну логіку пошуку політик, зареєструйте власний колбек методом `Gate::guessPolicyNamesUsing`. Зазвичай цей метод викликають у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
#### Ручна реєстрація політик

Через фасад `Gate` ви можете вручну зареєструвати політики та відповідні їм моделі в методі `boot` вашого `AppServiceProvider`:

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::policy(Order::class, OrderPolicy::class);
}
```

Або ж ви можете застосувати до класу моделі атрибут `UsePolicy`, щоб повідомити Laravel про відповідну політику моделі:

```php
<?php

namespace App\Models;

use App\Policies\OrderPolicy;
use Illuminate\Database\Eloquent\Attributes\UsePolicy;
use Illuminate\Database\Eloquent\Model;

#[UsePolicy(OrderPolicy::class)]
class Order extends Model
{
    //
}
```

<a name="writing-policies"></a>
## Написання політик

<a name="policy-methods"></a>
### Методи політик

Коли клас політики зареєстровано, ви можете додати методи для кожної дії, яку він авторизує. Наприклад, визначмо метод `update` у нашій `PostPolicy`, який вирішує, чи може заданий `App\Models\User` оновити заданий екземпляр `App\Models\Post`.

Метод `update` отримає аргументами екземпляри `User` та `Post` і має повернути `true` чи `false`, вказуючи, чи має користувач право оновити заданий `Post`. Тож у цьому прикладі ми перевіримо, що `id` користувача збігається з `user_id` допису:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

Ви можете й далі визначати в політиці додаткові методи для різних дій, які вона авторизує. Наприклад, ви можете визначити методи `view` чи `delete`, щоб авторизувати різні дії з `Post`, - але пам'ятайте, що ви вільні давати методам політики будь-які імена.

Якщо, генеруючи політику через артизан-консоль, ви скористалися опцією `--model`, вона вже міститиме методи для дій `viewAny`, `view`, `create`, `update`, `delete`, `restore` та `forceDelete`.

> [!NOTE]
> Усі політики розв'язуються через [сервіс-контейнер](/docs/{{version}}/container) Laravel, тож ви можете вказати типи потрібних залежностей у конструкторі політики, і їх буде впроваджено автоматично.

<a name="policy-responses"></a>
### Відповіді політик

Досі ми розглядали лише методи політик, що повертають прості булеві значення. Проте іноді вам може знадобитися повернути докладнішу відповідь із повідомленням про помилку. Для цього поверніть із методу політики екземпляр `Illuminate\Auth\Access\Response`:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('You do not own this post.');
}
```

Коли ви повертаєте з політики відповідь авторизації, метод `Gate::allows` усе одно поверне просте булеве значення; проте ви можете скористатися методом `Gate::inspect`, щоб отримати повну відповідь авторизації, яку повернув гейт:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

Коли ви користуєтеся методом `Gate::authorize`, який кидає `AuthorizationException`, якщо дію не авторизовано, повідомлення про помилку з відповіді авторизації буде передано до HTTP-відповіді:

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
#### Налаштування статусу HTTP-відповіді

Коли метод політики відхиляє дію, повертається HTTP-відповідь `403`; проте іноді буває корисно повернути інший код статусу HTTP. Ви можете налаштувати код статусу HTTP для невдалої перевірки авторизації через статичний конструктор `denyWithStatus` класу `Illuminate\Auth\Access\Response`:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

Оскільки приховування ресурсів відповіддю `404` - дуже поширений патерн у вебзастосунках, для зручності пропонується метод `denyAsNotFound`:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```

<a name="methods-without-models"></a>
### Методи без моделей

Деякі методи політик отримують лише екземпляр поточного автентифікованого користувача. Найчастіше так буває при авторизації дій `create`. Наприклад, якщо ви створюєте блог, вам може знадобитися визначити, чи має користувач право створювати дописи взагалі. У таких випадках ваш метод політики має очікувати лише екземпляр користувача:

```php
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### Гості

За замовчуванням усі гейти й політики автоматично повертають `false`, якщо вхідний HTTP-запит ініціював не автентифікований користувач. Проте ви можете пропускати такі перевірки далі - до ваших гейтів і політик, - оголосивши «необов'язкову» підказку типу або задавши значення `null` за замовчуванням для аргументу користувача:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### Фільтри політик

Для певних користувачів ви можете захотіти авторизувати всі дії в межах заданої політики. Для цього визначте в політиці метод `before`. Метод `before` виконуватиметься перед усіма іншими методами політики, даючи вам змогу авторизувати дію ще до того, як буде викликано потрібний метод. Найчастіше цю можливість використовують, щоб дозволити адміністраторам застосунку виконувати будь-які дії:

```php
use App\Models\User;

/**
 * Perform pre-authorization checks.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

Якщо ви хочете відхилити всі перевірки авторизації для певного типу користувачів, поверніть із методу `before` значення `false`. Якщо повернути `null`, перевірка авторизації перейде до методу політики.

> [!WARNING]
> Метод `before` класу політики не буде викликано, якщо клас не містить методу, ім'я якого збігається з іменем можливості, що перевіряється.

<a name="authorizing-actions-using-policies"></a>
## Авторизація дій через політики

<a name="via-the-user-model"></a>
### Через модель User

Модель `App\Models\User`, що входить до вашого застосунку Laravel, містить два зручні методи для авторизації дій: `can` та `cannot`. Методи `can` і `cannot` приймають ім'я дії, яку ви хочете авторизувати, і відповідну модель. Наприклад, визначмо, чи має користувач право оновити задану модель `App\Models\Post`. Зазвичай це роблять у методі контролера:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

Якщо для заданої моделі [зареєстровано політику](#registering-policies), метод `can` автоматично викличе потрібну політику й поверне булевий результат. Якщо для моделі політики не зареєстровано, метод `can` спробує викликати гейт на замиканні, що відповідає імені заданої дії.

<a name="user-model-actions-that-dont-require-models"></a>
#### Дії, що не потребують моделей

Пам'ятайте: деякі дії відповідають методам політики на кшталт `create`, яким не потрібен екземпляр моделі. У таких випадках ви можете передати методу `can` ім'я класу. За ним буде визначено, яку політику використати для авторизації дії:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // Create the post...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Через фасад `Gate`

Окрім зручних методів моделі `App\Models\User`, ви завжди можете авторизувати дії методом `authorize` фасада `Gate`.

Як і метод `can`, цей метод приймає ім'я дії, яку ви хочете авторизувати, і відповідну модель. Якщо дію не авторизовано, метод `authorize` кине виняток `Illuminate\Auth\Access\AuthorizationException`, який обробник винятків Laravel автоматично перетворить на HTTP-відповідь зі статусом 403:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // The current user can update the blog post...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### Дії, що не потребують моделей

Як уже обговорювалося, деяким методам політики на кшталт `create` не потрібен екземпляр моделі. У таких випадках передайте методу `authorize` ім'я класу. За ним буде визначено, яку політику використати для авторизації дії:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // The current user can create blog posts...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### Через middleware

Laravel містить `middleware`, яке може авторизувати дії ще до того, як вхідний запит дійде до ваших маршрутів чи контролерів. За замовчуванням `middleware` `Illuminate\Auth\Middleware\Authorize` можна додати до маршруту через [аліас `middleware`](/docs/{{version}}/middleware#middleware-aliases) `can`, який Laravel реєструє автоматично. Розгляньмо приклад використання `middleware` `can`, щоб авторизувати оновлення допису користувачем:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

У цьому прикладі ми передаємо `middleware` `can` два аргументи. Перший - ім'я дії, яку ми хочемо авторизувати, другий - параметр маршруту, який ми хочемо передати методу політики. У цьому випадку, оскільки ми користуємося [неявним прив'язуванням моделей](/docs/{{version}}/routing#implicit-binding), методу політики буде передано модель `App\Models\Post`. Якщо користувач не має права виконати задану дію, `middleware` поверне HTTP-відповідь зі статусом 403.

Для зручності ви також можете додати `middleware` `can` до маршруту методом `can`:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

Якщо ви користуєтеся [атрибутами `middleware` контролерів](/docs/{{version}}/controllers#middleware-attributes), ви можете застосувати `middleware` `can` через атрибут `Authorize`:

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;

#[Authorize('update', 'post')]
public function update(Post $post)
{
    // The current user may update the post...
}
```

<a name="middleware-actions-that-dont-require-models"></a>
#### Дії, що не потребують моделей

Знову ж таки: деяким методам політики на кшталт `create` не потрібен екземпляр моделі. У таких випадках ви можете передати `middleware` ім'я класу. За ним буде визначено, яку політику використати для авторизації дії:

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

Указувати повне ім'я класу в рядковому визначенні `middleware` буває незручно. Тому ви можете додати `middleware` `can` до маршруту методом `can`:

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Через Blade-шаблони

Пишучи Blade-шаблони, ви можете захотіти показувати частину сторінки лише тоді, коли користувач має право виконати задану дію. Наприклад, ви можете показувати форму оновлення допису лише тим, хто справді може його оновити. У такому разі скористайтеся директивами `@can` та `@cannot`:

```blade
@can('update', $post)
    <!-- The current user can update the post... -->
@elsecan('create', App\Models\Post::class)
    <!-- The current user can create new posts... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- The current user cannot update the post... -->
@elsecannot('create', App\Models\Post::class)
    <!-- The current user cannot create new posts... -->
@endcannot
```

Ці директиви - зручні скорочення для конструкцій `@if` та `@unless`. Наведені вище конструкції `@can` і `@cannot` рівносильні таким:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

Ви також можете визначити, чи має користувач право виконати будь-яку дію із заданого масиву дій. Для цього скористайтеся директивою `@canany`:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### Дії, що не потребують моделей

Як і в більшості інших методів авторизації, ви можете передати директивам `@can` і `@cannot` ім'я класу, якщо дії не потрібен екземпляр моделі:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### Передавання додаткового контексту

Авторизуючи дії через політики, ви можете передати масив другим аргументом до різних функцій і хелперів авторизації. Перший елемент масиву визначатиме, яку політику викликати, а решта елементів передаються параметрами до методу політики й можуть слугувати додатковим контекстом при ухваленні рішень щодо авторизації. Розгляньмо, наприклад, таке визначення методу `PostPolicy` із додатковим параметром `$category`:

```php
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

Намагаючись визначити, чи може автентифікований користувач оновити заданий допис, ми можемо викликати цей метод політики так:

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // The current user can update the blog post...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## Авторизація та Inertia

Хоча авторизацію завжди слід виконувати на сервері, часто буває зручно передати вашому фронтенду дані авторизації, щоб належно відрендерити UI застосунку. Laravel не встановлює обов'язкової угоди щодо того, як надавати інформацію про авторизацію фронтенду на Inertia.

Проте якщо ви користуєтеся одним зі [стартових наборів](/docs/{{version}}/starter-kits) Laravel на основі Inertia, ваш застосунок уже містить `middleware` `HandleInertiaRequests`. У методі `share` цього `middleware` ви можете повернути спільні дані, які надаватимуться всім сторінкам Inertia у вашому застосунку. Ці спільні дані - зручне місце, щоб описати інформацію про авторизацію користувача:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    // ...

    /**
     * Define the props that are shared by default.
     *
     * @return array<string, mixed>
     */
    public function share(Request $request)
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user(),
                'permissions' => [
                    'post' => [
                        'create' => $request->user()->can('create', Post::class),
                    ],
                ],
            ],
        ];
    }
}
```
