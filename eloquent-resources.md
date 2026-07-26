---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: API-ресурси

- [Вступ](#introduction)
- [Генерування ресурсів](#generating-resources)
- [Огляд концепції](#concept-overview)
    - [Колекції ресурсів](#resource-collections)
- [Написання ресурсів](#writing-resources)
    - [Обгортання даних](#data-wrapping)
    - [Пагінація](#pagination)
    - [Умовні атрибути](#conditional-attributes)
    - [Умовні зв'язки](#conditional-relationships)
    - [Додавання метаданих](#adding-meta-data)
- [Ресурси JSON:API](#jsonapi-resources)
    - [Генерування ресурсів JSON:API](#generating-jsonapi-resources)
    - [Визначення атрибутів](#defining-jsonapi-attributes)
    - [Визначення зв'язків](#defining-jsonapi-relationships)
    - [Тип та ID ресурсу](#jsonapi-resource-type-and-id)
    - [Розріджені набори полів і includes](#jsonapi-sparse-fieldsets-and-includes)
    - [Посилання та метадані](#jsonapi-links-and-meta)
- [Відповіді ресурсів](#resource-responses)

<a name="introduction"></a>
## Вступ

Коли ви будуєте API, вам може знадобитися шар перетворення, який стоїть між вашими моделями Eloquent і JSON-відповідями, що насправді повертаються користувачам застосунку. Наприклад, ви можете захотіти показувати певні атрибути лише частині користувачів, або завжди включати певні зв'язки до JSON-представлення ваших моделей. Класи ресурсів Eloquent дозволяють виразно й легко перетворювати моделі та колекції моделей на JSON.

Звісно, ви завжди можете перетворити моделі чи колекції Eloquent на JSON за допомогою методу `toJson`; проте ресурси Eloquent дають більш гнучкий і надійний контроль над JSON-серіалізацією ваших моделей та їхніх зв'язків.

<a name="generating-resources"></a>
## Генерування ресурсів

Щоб згенерувати клас ресурсу, скористайтеся артизан-командою `make:resource`. За замовчуванням ресурси потрапляють до каталогу `app/Http/Resources` вашого застосунку. Ресурси успадковують клас `Illuminate\Http\Resources\Json\JsonResource`:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### Колекції ресурсів

Окрім ресурсів, які перетворюють окремі моделі, ви можете генерувати ресурси, відповідальні за перетворення колекцій моделей. Це дозволяє вашим JSON-відповідям містити посилання та іншу метаінформацію, що стосується всієї колекції певного ресурсу.

Щоб створити колекцію ресурсів, скористайтеся прапорцем `--collection` під час створення ресурсу. Або ж слово `Collection` в імені ресурсу підкаже Laravel, що потрібно створити саме колекцію. Колекції ресурсів успадковують клас `Illuminate\Http\Resources\Json\ResourceCollection`:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## Огляд концепції

> [!NOTE]
> Це високорівневий огляд ресурсів і колекцій ресурсів. Наполегливо радимо прочитати інші розділи цієї документації, щоб глибше зрозуміти можливості налаштування та всю силу, яку дають ресурси.

Перш ніж заглиблюватися в усі доступні опції написання ресурсів, погляньмо згори на те, як ресурси використовуються в Laravel. Клас ресурсу представляє одну модель, яку потрібно перетворити на JSON-структуру. Ось, наприклад, простий клас ресурсу `UserResource`:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

Кожен клас ресурсу визначає метод `toArray`, який повертає масив атрибутів, що мають бути перетворені на JSON, коли ресурс повертається як відповідь із маршруту чи методу контролера.

Зверніть увагу: ми звертаємося до властивостей моделі напряму через змінну `$this`. Так відбувається тому, що клас ресурсу автоматично проксіює звернення до властивостей і методів до моделі, яка лежить в основі, - для зручності. Коли ресурс визначено, його можна повернути з маршруту чи контролера. Ресурс приймає екземпляр моделі через свій конструктор:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

Для зручності можна скористатися методом моделі `toResource`, який за угодами фреймворку автоматично знайде відповідний ресурс моделі:

```php
return User::findOrFail($id)->toResource();
```

Під час виклику методу `toResource` Laravel спробує знайти ресурс, ім'я якого збігається з іменем моделі та, можливо, має суфікс `Resource`, у просторі імен `Http\Resources`, найближчому до простору імен моделі.

Якщо ваш клас ресурсу не дотримується цієї угоди про іменування або розташований в іншому просторі імен, ви можете вказати ресурс за замовчуванням для моделі за допомогою атрибута `UseResource`:

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserResource;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResource;

#[UseResource(CustomUserResource::class)]
class User extends Model
{
    // ...
}
```

Або ж ви можете вказати клас ресурсу, передавши його до методу `toResource`:

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### Колекції ресурсів

Якщо ви повертаєте колекцію ресурсів або відповідь із пагінацією, під час створення екземпляра ресурсу в маршруті чи контролері скористайтеся методом `collection`, який надає ваш клас ресурсу:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

Або, для зручності, скористайтеся методом колекції Eloquent `toResourceCollection`, який за угодами фреймворку автоматично знайде відповідну колекцію ресурсів моделі:

```php
return User::all()->toResourceCollection();
```

Під час виклику методу `toResourceCollection` Laravel спробує знайти колекцію ресурсів, ім'я якої збігається з іменем моделі та має суфікс `Collection`, у просторі імен `Http\Resources`, найближчому до простору імен моделі.

Якщо ваш клас колекції ресурсів не дотримується цієї угоди про іменування або розташований в іншому просторі імен, ви можете вказати колекцію ресурсів за замовчуванням для моделі за допомогою атрибута `UseResourceCollection`:

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserCollection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResourceCollection;

#[UseResourceCollection(CustomUserCollection::class)]
class User extends Model
{
    // ...
}
```

Або ж ви можете вказати клас колекції ресурсів, передавши його до методу `toResourceCollection`:

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### Власні колекції ресурсів

За замовчуванням колекції ресурсів не дозволяють додавати власні метадані, які може знадобитися повернути разом із колекцією. Якщо ви хочете налаштувати відповідь колекції ресурсів, створіть окремий ресурс, що представлятиме колекцію:

```shell
php artisan make:resource UserCollection
```

Коли клас колекції ресурсів згенеровано, ви можете легко визначити будь-які метадані, що мають потрапити до відповіді:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```

Після визначення колекції ресурсів її можна повернути з маршруту чи контролера:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

Або, для зручності, скористайтеся методом колекції Eloquent `toResourceCollection`, який за угодами фреймворку автоматично знайде відповідну колекцію ресурсів моделі:

```php
return User::all()->toResourceCollection();
```

Під час виклику методу `toResourceCollection` Laravel спробує знайти колекцію ресурсів, ім'я якої збігається з іменем моделі та має суфікс `Collection`, у просторі імен `Http\Resources`, найближчому до простору імен моделі.

<a name="preserving-collection-keys"></a>
#### Збереження ключів колекції

Коли ви повертаєте колекцію ресурсів із маршруту, Laravel скидає ключі колекції так, щоб вони йшли в числовому порядку. Проте ви можете застосувати до класу ресурсу атрибут `PreserveKeys`, що вказує, чи слід зберігати початкові ключі колекції:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\PreserveKeys;
use Illuminate\Http\Resources\Json\JsonResource;

#[PreserveKeys]
class UserResource extends JsonResource
{
    // ...
}
```

Коли властивість `preserveKeys` має значення `true`, ключі колекції зберігатимуться при поверненні колекції з маршруту чи контролера:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### Налаштування базового класу ресурсу

Зазвичай властивість `$this->collection` колекції ресурсів автоматично заповнюється результатом перетворення кожного елемента колекції на його одиничний клас ресурсу. Вважається, що одиничний клас ресурсу - це ім'я класу колекції без кінцевої частини `Collection`. До того ж, залежно від ваших уподобань, одиничний клас ресурсу може мати або не мати суфікс `Resource`.

Наприклад, `UserCollection` спробує перетворити передані екземпляри користувачів на ресурс `UserResource`. Щоб змінити цю поведінку, застосуйте до колекції ресурсів атрибут `Collects`:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\Collects;
use Illuminate\Http\Resources\Json\ResourceCollection;

#[Collects(Member::class)]
class UserCollection extends ResourceCollection
{
    // ...
}
```

<a name="writing-resources"></a>
## Написання ресурсів

> [!NOTE]
> Якщо ви ще не прочитали [огляд концепції](#concept-overview), наполегливо радимо зробити це, перш ніж рухатися далі.

Ресурсам потрібно лише перетворити задану модель на масив. Тож кожен ресурс містить метод `toArray`, який перекладає атрибути вашої моделі на зручний для API масив, що може бути повернений із маршрутів чи контролерів вашого застосунку:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

Коли ресурс визначено, його можна повернути прямо з маршруту чи контролера:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### Зв'язки

Якщо ви хочете включити до відповіді пов'язані ресурси, додайте їх до масиву, який повертає метод `toArray` вашого ресурсу. У цьому прикладі ми скористаємося методом `collection` ресурсу `PostResource`, щоб додати до відповіді ресурсу дописи користувача:

```php
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->posts),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

> [!NOTE]
> Якщо ви хочете включати зв'язки лише тоді, коли їх уже завантажено, перегляньте документацію про [умовні зв'язки](#conditional-relationships).

<a name="writing-resource-collections"></a>
#### Колекції ресурсів

Якщо ресурси перетворюють одну модель на масив, то колекції ресурсів перетворюють на масив колекцію моделей. Проте визначати клас колекції ресурсів для кожної моделі зовсім не обов'язково, адже всі колекції моделей Eloquent мають метод `toResourceCollection`, який на льоту створює «ad-hoc» колекцію ресурсів:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

Однак якщо вам потрібно налаштувати метадані, що повертаються разом із колекцією, доведеться визначити власну колекцію ресурсів:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```

Як і одиничні ресурси, колекції ресурсів можна повертати прямо з маршрутів чи контролерів:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

Або, для зручності, скористайтеся методом колекції Eloquent `toResourceCollection`, який за угодами фреймворку автоматично знайде відповідну колекцію ресурсів моделі:

```php
return User::all()->toResourceCollection();
```

Під час виклику методу `toResourceCollection` Laravel спробує знайти колекцію ресурсів, ім'я якої збігається з іменем моделі та має суфікс `Collection`, у просторі імен `Http\Resources`, найближчому до простору імен моделі.

<a name="data-wrapping"></a>
### Обгортання даних

За замовчуванням найзовнішніший ресурс обгортається в ключ `data`, коли відповідь ресурсу перетворюється на JSON. Тож типова відповідь колекції ресурсів має такий вигляд:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ]
}
```

Якщо ви хочете вимкнути обгортання найзовнішнішого ресурсу, викличте метод `withoutWrapping` на базовому класі `Illuminate\Http\Resources\Json\JsonResource`. Зазвичай цей метод викликають із `AppServiceProvider` або іншого [сервіс-провайдера](/docs/{{version}}/providers), який завантажується на кожному запиті до застосунку:

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

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
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> Метод `withoutWrapping` впливає лише на найзовнішнішу відповідь і не прибирає ключі `data`, які ви вручну додали до власних колекцій ресурсів.

<a name="wrapping-nested-resources"></a>
#### Обгортання вкладених ресурсів

Ви маєте цілковиту свободу визначати, як обгортаються зв'язки вашого ресурсу. Якщо ви хочете, щоб усі колекції ресурсів обгорталися в ключ `data` незалежно від рівня вкладеності, визначте клас колекції ресурсів для кожного ресурсу й повертайте колекцію всередині ключа `data`.

Ви можете замислитися, чи не призведе це до подвійного обгортання найзовнішнішого ресурсу в два ключі `data`. Не хвилюйтеся: Laravel ніколи не дозволить випадково обгорнути ваші ресурси двічі, тож про рівень вкладеності колекції ресурсів, яку ви перетворюєте, можна не турбуватися:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return ['data' => $this->collection];
    }
}
```

<a name="data-wrapping-and-pagination"></a>
#### Обгортання даних і пагінація

Коли ви повертаєте колекції з пагінацією через відповідь ресурсу, Laravel обгортає дані ресурсу в ключ `data`, навіть якщо було викликано метод `withoutWrapping`. Так відбувається тому, що відповіді з пагінацією завжди містять ключі `meta` та `links` з інформацією про стан пагінатора:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="pagination"></a>
### Пагінація

Ви можете передати екземпляр пагінатора Laravel до методу `collection` ресурсу або до власної колекції ресурсів:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

Або, для зручності, скористайтеся методом пагінатора `toResourceCollection`, який за угодами фреймворку автоматично знайде колекцію ресурсів для моделі з пагінацією:

```php
return User::paginate()->toResourceCollection();
```

Відповіді з пагінацією завжди містять ключі `meta` та `links` з інформацією про стан пагінатора:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="customizing-the-pagination-information"></a>
#### Налаштування інформації про пагінацію

Якщо ви хочете налаштувати інформацію, що потрапляє до ключів `links` чи `meta` відповіді з пагінацією, визначте на ресурсі метод `paginationInformation`. Цей метод отримає дані `$paginated` і масив стандартної інформації `$default`, який містить ключі `links` та `meta`:

```php
/**
 * Customize the pagination information for the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array  $paginated
 * @param  array  $default
 * @return array
 */
public function paginationInformation($request, $paginated, $default)
{
    $default['links']['custom'] = 'https://example.com';

    return $default;
}
```

<a name="conditional-attributes"></a>
### Умовні атрибути

Іноді потрібно включати атрибут до відповіді ресурсу лише за певної умови. Наприклад, ви можете захотіти показувати значення лише тоді, коли поточний користувач - «адміністратор». Laravel надає для таких випадків набір допоміжних методів. Метод `when` дозволяє додавати атрибут до відповіді ресурсу за умовою:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

У цьому прикладі ключ `secret` потрапить до підсумкової відповіді ресурсу лише тоді, коли метод `isAdmin` автентифікованого користувача поверне `true`. Якщо метод поверне `false`, ключ `secret` буде видалено з відповіді ресурсу ще до того, як її буде надіслано клієнту. Метод `when` дозволяє виразно описувати ресурси, не вдаючись до умовних конструкцій під час побудови масиву.

Метод `when` також приймає замикання другим аргументом, тож ви можете обчислювати підсумкове значення лише тоді, коли задана умова істинна (`true`):

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

Метод `whenHas` дозволяє включити атрибут, якщо він справді присутній на моделі:

```php
'name' => $this->whenHas('name'),
```

Крім того, метод `whenNotNull` дозволяє включити атрибут до відповіді ресурсу, якщо цей атрибут не є null:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### Об'єднання умовних атрибутів

Іноді у вас є кілька атрибутів, які мають потрапляти до відповіді ресурсу за однією й тією ж умовою. У такому разі скористайтеся методом `mergeWhen`, щоб включити атрибути до відповіді лише тоді, коли задана умова істинна (`true`):

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        $this->mergeWhen($request->user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

І знову: якщо задана умова хибна (`false`), ці атрибути буде видалено з відповіді ресурсу ще до надсилання клієнту.

> [!WARNING]
> Метод `mergeWhen` не слід використовувати всередині масивів, де змішані рядкові та числові ключі. Також його не варто застосовувати в масивах із числовими ключами, що йдуть не послідовно.

<a name="conditional-relationships"></a>
### Умовні зв'язки

Окрім умовного завантаження атрибутів, ви можете умовно включати до відповідей ресурсу зв'язки - залежно від того, чи вже завантажено зв'язок на моделі. Це дозволяє контролеру вирішувати, які зв'язки слід завантажити на моделі, а ресурс легко включить їх лише тоді, коли їх справді завантажено. Зрештою, так простіше уникати проблем із запитами «N+1» усередині ресурсів.

Метод `whenLoaded` дозволяє завантажувати зв'язок за умовою. Щоб не завантажувати зв'язки без потреби, цей метод приймає ім'я зв'язку, а не сам зв'язок:

```php
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->whenLoaded('posts')),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

У цьому прикладі, якщо зв'язок не було завантажено, ключ `posts` буде видалено з відповіді ресурсу ще до надсилання клієнту.

<a name="conditional-relationship-counts"></a>
#### Умовна кількість пов'язаних записів

Окрім умовного включення зв'язків, ви можете умовно включати до відповідей ресурсу «кількість» пов'язаних записів - залежно від того, чи завантажено цю кількість на моделі:

```php
new UserResource($user->loadCount('posts'));
```

Метод `whenCounted` дозволяє умовно включити кількість пов'язаних записів до відповіді ресурсу. Цей метод уникає зайвого додавання атрибута, якщо кількості для зв'язку немає:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts_count' => $this->whenCounted('posts'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

У цьому прикладі, якщо кількість для зв'язку `posts` не було завантажено, ключ `posts_count` буде видалено з відповіді ресурсу ще до надсилання клієнту.

Інші види агрегатів, як-от `avg`, `sum`, `min` і `max`, також можна завантажувати за умовою за допомогою методу `whenAggregated`:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### Умовна інформація з проміжної таблиці

Окрім умовного включення інформації про зв'язки до відповідей ресурсу, ви можете умовно включати дані з проміжних таблиць зв'язків «багато до багатьох» за допомогою методу `whenPivotLoaded`. Метод `whenPivotLoaded` приймає першим аргументом ім'я проміжної таблиці. Другим аргументом має бути замикання, що повертає значення, яке слід повернути, якщо інформація з проміжної таблиці доступна на моделі:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoaded('role_user', function () {
            return $this->pivot->expires_at;
        }),
    ];
}
```

Якщо ваш зв'язок використовує [власну модель проміжної таблиці](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models), ви можете передати екземпляр цієї моделі першим аргументом до методу `whenPivotLoaded`:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

Якщо ваша проміжна таблиця використовує аксесор, відмінний від `pivot`, скористайтеся методом `whenPivotLoadedAs`:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {
            return $this->subscription->expires_at;
        }),
    ];
}
```

<a name="adding-meta-data"></a>
### Додавання метаданих

Деякі стандарти JSON API вимагають додавати метадані до відповідей ресурсів і колекцій ресурсів. Найчастіше це `links` на сам ресурс чи пов'язані ресурси або метадані про сам ресурс. Якщо вам потрібно повернути додаткові метадані про ресурс, включіть їх до методу `toArray`. Наприклад, ви можете додати інформацію `links` під час перетворення колекції ресурсів:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'data' => $this->collection,
        'links' => [
            'self' => 'link-value',
        ],
    ];
}
```

Повертаючи додаткові метадані з ресурсів, ви можете не хвилюватися про випадкове перезаписування ключів `links` чи `meta`, які Laravel автоматично додає до відповідей із пагінацією. Будь-які визначені вами додаткові `links` буде об'єднано з посиланнями, що їх надає пагінатор.

<a name="top-level-meta-data"></a>
#### Метадані верхнього рівня

Іноді потрібно включати певні метадані до відповіді ресурсу лише тоді, коли цей ресурс є найзовнішнішим із тих, що повертаються. Зазвичай це метаінформація про відповідь загалом. Щоб визначити такі метадані, додайте до класу ресурсу метод `with`. Цей метод має повертати масив метаданих, які потрапляють до відповіді ресурсу лише тоді, коли ресурс є найзовнішнішим із тих, що перетворюються:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return parent::toArray($request);
    }

    /**
     * Get additional data that should be returned with the resource array.
     *
     * @return array<string, mixed>
     */
    public function with(Request $request): array
    {
        return [
            'meta' => [
                'key' => 'value',
            ],
        ];
    }
}
```

<a name="adding-meta-data-when-constructing-resources"></a>
#### Додавання метаданих під час створення ресурсів

Ви також можете додавати дані верхнього рівня під час створення екземплярів ресурсів у маршруті чи контролері. Метод `additional`, доступний на всіх ресурсах, приймає масив даних, які слід додати до відповіді ресурсу:

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="jsonapi-resources"></a>
## Ресурси JSON:API

Laravel постачається з `JsonApiResource` - класом ресурсу, який формує відповіді, сумісні зі [специфікацією JSON:API](https://jsonapi.org/). Він успадковує стандартний клас `JsonResource` й автоматично дбає про структуру об'єкта ресурсу, зв'язки, розріджені набори полів, includes, ліниве обчислення атрибутів, а також встановлює заголовок `Content-Type` у значення `application/vnd.api+json`.

> [!NOTE]
> Ресурси JSON:API в Laravel відповідають за серіалізацію ваших відповідей. Якщо вам також потрібно розбирати вхідні параметри запиту JSON:API, як-от фільтри та сортування, чудовим доповненням стане [Laravel Query Builder від Spatie](https://spatie.be/docs/laravel-query-builder).

<a name="generating-jsonapi-resources"></a>
### Генерування ресурсів JSON:API

Щоб згенерувати ресурс JSON:API, скористайтеся артизан-командою `make:resource` із прапорцем `--json-api`:

```shell
php artisan make:resource PostResource --json-api
```

Згенерований клас успадкує `Illuminate\Http\Resources\JsonApi\JsonApiResource` і міститиме властивості `$attributes` та `$relationships`, які вам потрібно заповнити:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

class PostResource extends JsonApiResource
{
    /**
     * The resource's attributes.
     */
    public $attributes = [
        // ...
    ];

    /**
     * The resource's relationships.
     */
    public $relationships = [
        // ...
    ];
}
```

Ресурси JSON:API можна повертати з маршрутів і контролерів так само, як і стандартні ресурси:

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```

Або, для зручності, скористайтеся методом моделі `toResource`:

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```

Це дасть відповідь, сумісну з JSON:API:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World",
            "body": "This is my first post."
        }
    }
}
```

Щоб повернути колекцію ресурсів JSON:API, скористайтеся методом `collection` або зручним методом `toResourceCollection`:

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```

<a name="defining-jsonapi-attributes"></a>
### Визначення атрибутів

Є два способи визначити, які атрибути потраплять до вашого ресурсу JSON:API.

Найпростіший підхід - визначити на ресурсі властивість `$attributes`. Ви можете перелічити імена атрибутів як значення, і їх буде прочитано напряму з моделі:

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```

Якщо обчислення атрибута дороге, поверніть його з `toAttributes` як замикання - тоді його буде обчислено лише тоді, коли атрибут справді знадобиться у відповіді.

Або ж, для повного контролю над атрибутами ресурсу, перевизначте на ресурсі метод `toAttributes`:

```php
/**
 * Get the resource's attributes.
 *
 * @return array<string, mixed>
 */
public function toAttributes(Request $request): array
{
    return [
        'title' => $this->title,
        'body' => $this->body,
        'is_published' => fn () => $this->published_at !== null,
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<a name="defining-jsonapi-relationships"></a>
### Визначення зв'язків

Ресурси JSON:API підтримують визначення зв'язків згідно зі специфікацією JSON:API. Зв'язки серіалізуються лише тоді, коли клієнт запитує їх через параметр запиту `include`.

#### Властивість `$relationships`

Ви можете визначити зв'язки ресурсу, доступні для включення, через властивість `$relationships`:

```php
public $relationships = [
    'author',
    'comments',
];
```

Коли ім'я зв'язку вказано як значення, Laravel визначить відповідний зв'язок Eloquent і автоматично знайде потрібний клас ресурсу. Якщо вам потрібно вказати клас ресурсу явно, визначте зв'язок як пару ключ / клас:

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```

Або ж перевизначте на ресурсі метод `toRelationships`:

```php
/**
 * Get the resource's relationships.
 */
public function toRelationships(Request $request): array
{
    return [
        'author' => UserResource::class,
        'comments' => fn () => CommentResource::collection(
            $request->user()->is($this->resource)
                ? $this->comments
                : $this->comments->where('is_public', true),
        ),
    ];
}
```

Замикання дають більше контролю над даними зв'язку, водночас зв'язок так само розв'язується лише тоді, коли клієнт його запитує.

#### Включення зв'язків

Клієнти можуть запитувати пов'язані ресурси через параметр запиту `include`:

```
GET /api/posts/1?include=author,comments
```

Це дасть відповідь з ідентифікаторами ресурсів у ключі `relationships` і повними об'єктами ресурсів у масиві `included` верхнього рівня:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "relationships": {
            "author": {
                "data": {
                    "id": "1",
                    "type": "users"
                }
            },
            "comments": {
                "data": [
                    {
                        "id": "1",
                        "type": "comments"
                    }
                ]
            }
        }
    },
    "included": [
        {
            "id": "1",
            "type": "users",
            "attributes": {
                "name": "Taylor Otwell"
            }
        },
        {
            "id": "1",
            "type": "comments",
            "attributes": {
                "body": "Great post!"
            }
        }
    ]
}
```

Вкладені зв'язки можна включати через крапкову нотацію:

```
GET /api/posts/1?include=comments.author
```

<a name="jsonapi-relationship-depth"></a>
#### Глибина зв'язків

За замовчуванням включення вкладених зв'язків обмежене максимальною глибиною. Ви можете змінити це обмеження методом `maxRelationshipDepth`, зазвичай в одному із сервіс-провайдерів застосунку:

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```

<a name="jsonapi-resource-type-and-id"></a>
### Тип та ID ресурсу

За замовчуванням `type` ресурсу виводиться з імені класу ресурсу. Наприклад, `PostResource` дає тип `posts`, а `BlogPostResource` - `blog-posts`. `id` ресурсу визначається з первинного ключа моделі.

Якщо вам потрібно змінити ці значення, перевизначте на ресурсі методи `toType` і `toId`:

```php
/**
 * Get the resource's type.
 */
public function toType(Request $request): string
{
    return 'articles';
}

/**
 * Get the resource's ID.
 */
public function toId(Request $request): string
{
    return (string) $this->uuid;
}
```

Це особливо корисно, коли тип ресурсу має відрізнятися від імені класу - наприклад, коли `AuthorResource` обгортає модель `User` і має віддавати тип `authors`.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
### Розріджені набори полів і includes

Ресурси JSON:API підтримують [розріджені набори полів](https://jsonapi.org/format/#fetching-sparse-fieldsets), що дозволяє клієнтам запитувати лише певні атрибути для кожного типу ресурсу через параметр запиту `fields`:

```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

Це включить лише атрибути `title` та `created_at` для ресурсів `posts` і атрибут `name` для ресурсів `users`.

<a name="jsonapi-ignoring-query-string"></a>
#### Ігнорування рядка запиту

Якщо ви хочете вимкнути фільтрацію за розрідженими наборами полів для певної відповіді ресурсу, викличте метод `ignoreFieldsAndIncludesInQueryString`:

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```

<a name="jsonapi-including-previously-loaded-relationships"></a>
#### Включення раніше завантажених зв'язків

За замовчуванням зв'язки потрапляють до відповіді лише тоді, коли їх запитано через параметр запиту `include`. Якщо ви хочете включити всі раніше жадібно завантажені зв'язки незалежно від рядка запиту, викличте метод `includePreviouslyLoadedRelationships`:

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```

<a name="jsonapi-links-and-meta"></a>
### Посилання та метадані

Ви можете додати посилання й метаінформацію до об'єктів ресурсу JSON:API, перевизначивши на ресурсі методи `toLinks` і `toMeta`:

```php
/**
 * Get the resource's links.
 */
public function toLinks(Request $request): array
{
    return [
        'self' => route('api.posts.show', $this->resource),
    ];
}

/**
 * Get the resource's meta information.
 */
public function toMeta(Request $request): array
{
    return [
        'readable_created_at' => $this->created_at->diffForHumans(),
    ];
}
```

Це додасть до об'єкта ресурсу у відповіді ключі `links` та `meta`:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "links": {
            "self": "https://example.com/api/posts/1"
        },
        "meta": {
            "readable_created_at": "2 hours ago"
        }
    }
}
```

<a name="resource-responses"></a>
## Відповіді ресурсів

Як ви вже прочитали, ресурси можна повертати прямо з маршрутів і контролерів:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

Проте іноді потрібно налаштувати вихідну HTTP-відповідь, перш ніж її буде надіслано клієнту. Зробити це можна двома способами. По-перше, ви можете додати до ресурсу ланцюжком метод `response`. Цей метод поверне екземпляр `Illuminate\Http\JsonResponse`, даючи вам повний контроль над заголовками відповіді:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return User::find(1)
        ->toResource()
        ->response()
        ->header('X-Value', 'True');
});
```

Або ж ви можете визначити метод `withResponse` усередині самого ресурсу. Цей метод буде викликано, коли ресурс повертається як найзовнішніший ресурс у відповіді:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * Customize the outgoing response for the resource.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```
