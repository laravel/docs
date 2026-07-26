---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: зв'язки

- [Вступ](#introduction)
- [Визначення зв'язків](#defining-relationships)
    - [Один до одного / Has One](#one-to-one)
    - [Один до багатьох / Has Many](#one-to-many)
    - [Один до багатьох (зворотний) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Зв'язки зі скопами](#scoped-relationships)
- [Зв'язки «багато до багатьох»](#many-to-many)
    - [Отримання стовпців проміжної таблиці](#retrieving-intermediate-table-columns)
    - [Фільтрація запитів за стовпцями проміжної таблиці](#filtering-queries-via-intermediate-table-columns)
    - [Сортування запитів за стовпцями проміжної таблиці](#ordering-queries-via-intermediate-table-columns)
    - [Визначення власних моделей проміжної таблиці](#defining-custom-intermediate-table-models)
- [Поліморфні зв'язки](#polymorphic-relationships)
    - [Один до одного](#one-to-one-polymorphic-relations)
    - [Один до багатьох](#one-to-many-polymorphic-relations)
    - [Один з багатьох](#one-of-many-polymorphic-relations)
    - [Багато до багатьох](#many-to-many-polymorphic-relations)
    - [Власні поліморфні типи](#custom-polymorphic-types)
- [Динамічні зв'язки](#dynamic-relationships)
- [Запити до зв'язків](#querying-relations)
    - [Методи зв'язків проти динамічних властивостей](#relationship-methods-vs-dynamic-properties)
    - [Запити за наявністю зв'язку](#querying-relationship-existence)
    - [Запити за відсутністю зв'язку](#querying-relationship-absence)
    - [Запити до зв'язків Morph To](#querying-morph-to-relationships)
- [Агрегування пов'язаних моделей](#aggregating-related-models)
    - [Підрахунок пов'язаних моделей](#counting-related-models)
    - [Інші агрегатні функції](#other-aggregate-functions)
    - [Підрахунок пов'язаних моделей у зв'язках Morph To](#counting-related-models-on-morph-to-relationships)
- [Жадібне завантаження](#eager-loading)
    - [Обмеження жадібного завантаження](#constraining-eager-loads)
    - [Відкладене жадібне завантаження](#lazy-eager-loading)
    - [Автоматичне жадібне завантаження](#automatic-eager-loading)
    - [Заборона лінивого завантаження](#preventing-lazy-loading)
- [Вставлення й оновлення пов'язаних моделей](#inserting-and-updating-related-models)
    - [Метод `save`](#the-save-method)
    - [Метод `create`](#the-create-method)
    - [Зв'язки Belongs To](#updating-belongs-to-relationships)
    - [Зв'язки «багато до багатьох»](#updating-many-to-many-relationships)
- [Оновлення часових міток батьківської моделі](#touching-parent-timestamps)

<a name="introduction"></a>
## Вступ

Таблиці бази даних часто пов'язані одна з одною. Наприклад, допис у блозі може мати багато коментарів, а замовлення може бути пов'язане з користувачем, який його зробив. Eloquent робить керування такими зв'язками простим і підтримує різні поширені типи зв'язків:

<div class="content-list" markdown="1">

- [Один до одного](#one-to-one)
- [Один до багатьох](#one-to-many)
- [Багато до багатьох](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [Один до одного (поліморфний)](#one-to-one-polymorphic-relations)
- [Один до багатьох (поліморфний)](#one-to-many-polymorphic-relations)
- [Багато до багатьох (поліморфний)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## Визначення зв'язків

Зв'язки Eloquent визначаються як методи в класах ваших моделей Eloquent. Оскільки зв'язки водночас є потужними [конструкторами запитів](/docs/{{version}}/queries), визначення їх як методів дає широкі можливості для ланцюжків методів і запитів. Наприклад, ми можемо додати додаткові обмеження до цього зв'язку `posts`:

```php
$user->posts()->where('active', 1)->get();
```

Але перш ніж заглиблюватися у використання зв'язків, розберімося, як визначити кожен тип зв'язку, який підтримує Eloquent.

<a name="one-to-one"></a>
### Один до одного / Has One

Зв'язок «один до одного» - це дуже базовий тип зв'язку в базі даних. Наприклад, модель `User` може бути пов'язана з однією моделлю `Phone`. Щоб визначити цей зв'язок, ми додамо до моделі `User` метод `phone`. Метод `phone` має викликати метод `hasOne` і повернути його результат. Метод `hasOne` доступний вашій моделі через базовий клас моделі `Illuminate\Database\Eloquent\Model`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

Перший аргумент, який передається методу `hasOne`, - ім'я класу пов'язаної моделі. Коли зв'язок визначено, ми можемо отримати пов'язаний запис через динамічні властивості Eloquent. Динамічні властивості дозволяють звертатися до методів зв'язків так, ніби це властивості, визначені на моделі:

```php
$phone = User::find(1)->phone;
```

Eloquent визначає зовнішній ключ зв'язку на основі імені батьківської моделі. У цьому випадку автоматично припускається, що модель `Phone` має зовнішній ключ `user_id`. Якщо ви хочете перевизначити цю угоду, передайте методу `hasOne` другий аргумент:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

Крім того, Eloquent припускає, що значення зовнішнього ключа має збігатися зі значенням стовпця первинного ключа батьківської моделі. Інакше кажучи, Eloquent шукатиме значення стовпця `id` користувача у стовпці `user_id` запису `Phone`. Якщо ви хочете, щоб зв'язок використовував значення первинного ключа, відмінне від `id` або від первинного ключа вашої моделі, передайте методу `hasOne` третій аргумент:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### Визначення зворотного зв'язку

Отже, ми можемо звернутися до моделі `Phone` з нашої моделі `User`. Тепер визначмо на моделі `Phone` зв'язок, який дозволить нам отримати користувача - власника телефону. Зворотний до `hasOne` зв'язок визначається методом `belongsTo`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

Під час виклику методу `user` Eloquent спробує знайти модель `User`, чий `id` збігається зі стовпцем `user_id` моделі `Phone`.

Eloquent визначає ім'я зовнішнього ключа, беручи ім'я методу зв'язку та додаючи до нього суфікс `_id`. Тож у цьому випадку Eloquent припускає, що модель `Phone` має стовпець `user_id`. Проте якщо зовнішній ключ на моделі `Phone` називається не `user_id`, ви можете передати власне ім'я ключа другим аргументом до методу `belongsTo`:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

Якщо батьківська модель не використовує `id` як первинний ключ або ви хочете знаходити пов'язану модель за іншим стовпцем, передайте методу `belongsTo` третій аргумент із власним ключем батьківської таблиці:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### Один до багатьох / Has Many

Зв'язок «один до багатьох» використовується, коли одна модель є батьківською для однієї чи кількох дочірніх моделей. Наприклад, допис у блозі може мати нескінченну кількість коментарів. Як і всі інші зв'язки Eloquent, зв'язки «один до багатьох» визначаються методом на вашій моделі Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Пам'ятайте: Eloquent автоматично визначить потрібний стовпець зовнішнього ключа для моделі `Comment`. За угодою Eloquent візьме ім'я батьківської моделі у «snake case» і додасть суфікс `_id`. Тож у цьому прикладі Eloquent припустить, що стовпець зовнішнього ключа на моделі `Comment` - це `post_id`.

Коли метод зв'язку визначено, ми можемо звернутися до [колекції](/docs/{{version}}/eloquent-collections) пов'язаних коментарів через властивість `comments`. Пам'ятайте: оскільки Eloquent надає «динамічні властивості зв'язків», ми можемо звертатися до методів зв'язків так, ніби це властивості моделі:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

Оскільки всі зв'язки водночас є конструкторами запитів, ви можете додати до запиту зв'язку додаткові обмеження, викликавши метод `comments` і продовживши ланцюжок умов:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

Як і в методі `hasOne`, ви можете перевизначити зовнішній і локальний ключі, передавши додаткові аргументи методу `hasMany`:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### Автоматичне заповнення батьківських моделей у дочірніх

Навіть із жадібним завантаженням Eloquent можуть виникати проблеми запитів «N + 1», якщо ви звертаєтеся до батьківської моделі з дочірньої, перебираючи дочірні моделі:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

У прикладі вище виникла проблема запитів «N + 1», бо, хоч коментарі й були жадібно завантажені для кожної моделі `Post`, Eloquent не заповнює автоматично батьківський `Post` у кожній дочірній моделі `Comment`.

Якщо ви хочете, щоб Eloquent автоматично заповнював батьківські моделі в дочірніх, викличте метод `chaperone` під час визначення зв'язку `hasMany`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

Або ж, якщо ви хочете вмикати автоматичне заповнення батьківських моделей під час виконання, викличте метод `chaperone` під час жадібного завантаження зв'язку:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### Один до багатьох (зворотний) / Belongs To

Тепер, коли ми маємо доступ до всіх коментарів допису, визначмо зв'язок, який дозволить коментарю звернутися до свого батьківського допису. Щоб визначити зворотний до `hasMany` зв'язок, оголосіть на дочірній моделі метод зв'язку, який викликає метод `belongsTo`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

Коли зв'язок визначено, ми можемо отримати батьківський допис коментаря через «динамічну властивість зв'язку» `post`:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

У прикладі вище Eloquent спробує знайти модель `Post`, чий `id` збігається зі стовпцем `post_id` моделі `Comment`.

Eloquent визначає ім'я зовнішнього ключа за замовчуванням, беручи ім'я методу зв'язку й додаючи до нього `_`, а далі ім'я стовпця первинного ключа батьківської моделі. Тож у цьому прикладі Eloquent припустить, що зовнішній ключ моделі `Post` у таблиці `comments` - це `post_id`.

Проте якщо зовнішній ключ вашого зв'язку не дотримується цих угод, ви можете передати власне ім'я зовнішнього ключа другим аргументом до методу `belongsTo`:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

Якщо ваша батьківська модель не використовує `id` як первинний ключ або ви хочете знаходити пов'язану модель за іншим стовпцем, передайте методу `belongsTo` третій аргумент із власним ключем батьківської таблиці:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### Моделі за замовчуванням

Зв'язки `belongsTo`, `hasOne`, `hasOneThrough` і `morphOne` дозволяють визначити модель за замовчуванням, яку буде повернено, якщо зв'язок дорівнює `null`. Цей патерн часто називають [патерном Null Object](https://en.wikipedia.org/wiki/Null_Object_pattern), і він допомагає позбутися умовних перевірок у коді. У наступному прикладі зв'язок `user` поверне порожню модель `App\Models\User`, якщо до моделі `Post` не прикріплено жодного користувача:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

Щоб заповнити модель за замовчуванням атрибутами, передайте методу `withDefault` масив або замикання:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Запити до зв'язків Belongs To

Роблячи запит до дочірніх записів зв'язку «belongs to», ви можете вручну побудувати умову `where`, щоб отримати відповідні моделі Eloquent:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

Проте зручнішим може виявитися метод `whereBelongsTo`, який автоматично визначить потрібний зв'язок і зовнішній ключ для заданої моделі:

```php
$posts = Post::whereBelongsTo($user)->get();
```

Ви також можете передати методу `whereBelongsTo` екземпляр [колекції](/docs/{{version}}/eloquent-collections). У такому разі Laravel поверне моделі, що належать будь-якій із батьківських моделей у колекції:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

За замовчуванням Laravel визначає зв'язок, пов'язаний із заданою моделлю, за іменем класу моделі; проте ви можете вказати ім'я зв'язку вручну, передавши його другим аргументом до методу `whereBelongsTo`:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One of Many

Іноді модель має багато пов'язаних моделей, але вам потрібно легко отримати «найновішу» чи «найстарішу» з них. Наприклад, модель `User` може бути пов'язана з багатьма моделями `Order`, але ви хочете мати зручний спосіб працювати з найновішим замовленням користувача. Цього можна досягти зв'язком типу `hasOne` у поєднанні з методами `ofMany`:

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

Так само ви можете визначити метод для отримання «найстарішої», тобто першої, пов'язаної моделі:

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

За замовчуванням методи `latestOfMany` та `oldestOfMany` отримують найновішу чи найстарішу пов'язану модель за первинним ключем моделі, який має бути придатним для сортування. Проте іноді потрібно отримати одну модель із більшого зв'язку за іншим критерієм сортування.

Наприклад, за допомогою методу `ofMany` можна отримати найдорожче замовлення користувача. Метод `ofMany` приймає першим аргументом стовпець для сортування, а другим - агрегатну функцію (`min` чи `max`), яку слід застосувати під час запиту пов'язаної моделі:

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> Оскільки PostgreSQL не підтримує виконання функції `MAX` над стовпцями UUID, наразі неможливо використовувати зв'язки one-of-many разом зі стовпцями UUID у PostgreSQL.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### Перетворення зв'язків «Many» на зв'язки Has One

Часто, отримуючи одну модель за допомогою методів `latestOfMany`, `oldestOfMany` чи `ofMany`, ви вже маєте визначений зв'язок «has many» для тієї самої моделі. Для зручності Laravel дозволяє легко перетворити цей зв'язок на «has one», викликавши на ньому метод `one`:

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

Метод `one` можна також використати, щоб перетворити зв'язки `HasManyThrough` на `HasOneThrough`:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### Складніші зв'язки Has One of Many

Можна будувати й складніші зв'язки «has one of many». Наприклад, модель `Product` може мати багато пов'язаних моделей `Price`, які зберігаються в системі навіть після публікації нових цін. До того ж нові дані про ціни на товар можуть публікуватися заздалегідь і набирати чинності в майбутньому - через стовпець `published_at`.

Тож, підсумовуючи, нам потрібно отримати найновішу опубліковану ціну, дата публікації якої не в майбутньому. Крім того, якщо дві ціни мають однакову дату публікації, ми віддамо перевагу ціні з більшим ID. Щоб цього досягти, ми маємо передати методу `ofMany` масив зі стовпцями для сортування, які визначають найновішу ціну. Також другим аргументом методу `ofMany` буде замикання. Воно відповідатиме за додавання до запиту зв'язку додаткових обмежень за датою публікації:

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through

Зв'язок «has-one-through» визначає зв'язок «один до одного» з іншою моделлю. Проте цей зв'язок вказує, що модель, яка його оголошує, може бути зіставлена з одним екземпляром іншої моделі _через_ третю модель.

Наприклад, у застосунку автомайстерні кожна модель `Mechanic` може бути пов'язана з однією моделлю `Car`, а кожна модель `Car` - з однією моделлю `Owner`. Хоча між механіком і власником немає прямого зв'язку в базі даних, механік може дістатися власника _через_ модель `Car`. Погляньмо на таблиці, потрібні для визначення цього зв'язку:

```text
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

Тепер, коли ми розглянули структуру таблиць для цього зв'язку, визначмо зв'язок на моделі `Mechanic`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

Перший аргумент, переданий методу `hasOneThrough`, - ім'я кінцевої моделі, до якої ми хочемо дістатися, а другий - ім'я проміжної моделі.

Або ж, якщо відповідні зв'язки вже визначені на всіх залучених моделях, ви можете плавно оголосити зв'язок «has-one-through», викликавши метод `through` і передавши імена цих зв'язків. Наприклад, якщо модель `Mechanic` має зв'язок `cars`, а модель `Car` - зв'язок `owner`, ви можете визначити зв'язок «has-one-through» між механіком і власником так:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### Угоди щодо ключів

Під час виконання запитів зв'язку використовуються типові угоди Eloquent щодо зовнішніх ключів. Якщо ви хочете налаштувати ключі зв'язку, передайте їх третім і четвертим аргументами до методу `hasOneThrough`. Третій аргумент - ім'я зовнішнього ключа на проміжній моделі. Четвертий - ім'я зовнішнього ключа на кінцевій моделі. П'ятий аргумент - локальний ключ, а шостий - локальний ключ проміжної моделі:

```php
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```

Або ж, як згадувалося раніше, якщо відповідні зв'язки вже визначені на всіх залучених моделях, ви можете плавно оголосити зв'язок «has-one-through», викликавши метод `through` і передавши імена цих зв'язків. Цей підхід має перевагу: він повторно використовує угоди щодо ключів, уже визначені в наявних зв'язках:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

Зв'язок «has-many-through» дає зручний спосіб дістатися віддалених зв'язків через проміжний зв'язок. Наприклад, уявімо, що ми будуємо платформу для розгортання на кшталт [Laravel Cloud](https://cloud.laravel.com). Модель `Application` може звертатися до багатьох моделей `Deployment` через проміжну модель `Environment`. Із цим прикладом ви легко зберете всі розгортання для заданого застосунку. Погляньмо на таблиці, потрібні для визначення цього зв'язку:

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

Тепер, коли ми розглянули структуру таблиць для цього зв'язку, визначмо зв'язок на моделі `Application`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * Get all of the deployments for the application.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

Перший аргумент, переданий методу `hasManyThrough`, - ім'я кінцевої моделі, до якої ми хочемо дістатися, а другий - ім'я проміжної моделі.

Або ж, якщо відповідні зв'язки вже визначені на всіх залучених моделях, ви можете плавно оголосити зв'язок «has-many-through», викликавши метод `through` і передавши імена цих зв'язків. Наприклад, якщо модель `Application` має зв'язок `environments`, а модель `Environment` - зв'язок `deployments`, ви можете визначити зв'язок «has-many-through» між застосунком і розгортаннями так:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

Хоча таблиця моделі `Deployment` не містить стовпця `application_id`, зв'язок `hasManyThrough` дає доступ до розгортань застосунку через `$application->deployments`. Щоб отримати ці моделі, Eloquent перевіряє стовпець `application_id` у таблиці проміжної моделі `Environment`. Знайшовши потрібні ID середовищ, він використовує їх для запиту до таблиці моделі `Deployment`.

<a name="has-many-through-key-conventions"></a>
#### Угоди щодо ключів

Під час виконання запитів зв'язку використовуються типові угоди Eloquent щодо зовнішніх ключів. Якщо ви хочете налаштувати ключі зв'язку, передайте їх третім і четвертим аргументами до методу `hasManyThrough`. Третій аргумент - ім'я зовнішнього ключа на проміжній моделі. Четвертий - ім'я зовнішнього ключа на кінцевій моделі. П'ятий аргумент - локальний ключ, а шостий - локальний ключ проміжної моделі:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the applications table...
            'id' // Local key on the environments table...
        );
    }
}
```

Або ж, як згадувалося раніше, якщо відповідні зв'язки вже визначені на всіх залучених моделях, ви можете плавно оголосити зв'язок «has-many-through», викликавши метод `through` і передавши імена цих зв'язків. Цей підхід має перевагу: він повторно використовує угоди щодо ключів, уже визначені в наявних зв'язках:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### Зв'язки зі скопами

Часто до моделей додають додаткові методи, які обмежують зв'язки. Наприклад, ви можете додати до моделі `User` метод `featuredPosts`, який обмежує ширший зв'язок `posts` додатковою умовою `where`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

Проте якщо ви спробуєте створити модель через метод `featuredPosts`, її атрибут `featured` не набуде значення `true`. Якщо ви хочете створювати моделі через методи зв'язків і водночас задавати атрибути, які слід додавати до всіх створених через цей зв'язок моделей, скористайтеся методом `withAttributes` під час побудови запиту зв'язку:

```php
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

Метод `withAttributes` додасть до запиту умови `where` із заданими атрибутами, а також додасть ці атрибути до всіх моделей, створених через метод зв'язку:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

Щоб метод `withAttributes` не додавав умов `where` до запиту, встановіть аргумент `asConditions` у значення `false`:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## Зв'язки «багато до багатьох»

Зв'язки «багато до багатьох» дещо складніші за зв'язки `hasOne` та `hasMany`. Приклад такого зв'язку - користувач, який має багато ролей, причому ці самі ролі мають й інші користувачі застосунку. Наприклад, користувачеві можна призначити ролі «Author» та «Editor»; проте ці ролі можуть бути призначені й іншим користувачам. Отже, користувач має багато ролей, а роль - багато користувачів.

<a name="many-to-many-table-structure"></a>
#### Структура таблиць

Щоб визначити цей зв'язок, потрібні три таблиці бази даних: `users`, `roles` і `role_user`. Ім'я таблиці `role_user` походить від імен пов'язаних моделей в алфавітному порядку, і вона містить стовпці `user_id` та `role_id`. Ця таблиця є проміжною й пов'язує користувачів із ролями.

Пам'ятайте: оскільки роль може належати багатьом користувачам, ми не можемо просто додати стовпець `user_id` до таблиці `roles`. Це означало б, що роль може належати лише одному користувачеві. Щоб ролі можна було призначати кільком користувачам, і потрібна таблиця `role_user`. Структуру таблиць цього зв'язку можна підсумувати так:

```text
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a name="many-to-many-model-structure"></a>
#### Структура моделей

Зв'язки «багато до багатьох» визначаються методом, який повертає результат методу `belongsToMany`. Метод `belongsToMany` надає базовий клас `Illuminate\Database\Eloquent\Model`, який використовують усі моделі Eloquent вашого застосунку. Наприклад, визначмо метод `roles` на нашій моделі `User`. Перший аргумент, який передається цьому методу, - ім'я класу пов'язаної моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

Коли зв'язок визначено, ви можете звертатися до ролей користувача через динамічну властивість зв'язку `roles`:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

Оскільки всі зв'язки водночас є конструкторами запитів, ви можете додати до запиту зв'язку додаткові обмеження, викликавши метод `roles` і продовживши ланцюжок умов:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

Щоб визначити ім'я проміжної таблиці зв'язку, Eloquent з'єднає імена двох пов'язаних моделей в алфавітному порядку. Проте ви можете перевизначити цю угоду, передавши другий аргумент до методу `belongsToMany`:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

Окрім імені проміжної таблиці, ви можете налаштувати й імена стовпців-ключів у ній, передавши додаткові аргументи до методу `belongsToMany`. Третій аргумент - ім'я зовнішнього ключа моделі, на якій ви визначаєте зв'язок, а четвертий - ім'я зовнішнього ключа моделі, до якої ви приєднуєтеся:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### Визначення зворотного зв'язку

Щоб визначити «зворотний» бік зв'язку «багато до багатьох», оголосіть на пов'язаній моделі метод, який також повертає результат методу `belongsToMany`. Щоб завершити наш приклад із користувачами й ролями, визначмо метод `users` на моделі `Role`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

Як бачите, зв'язок визначено точно так само, як і його відповідник на моделі `User`, за винятком посилання на модель `App\Models\User`. Оскільки ми повторно використовуємо метод `belongsToMany`, під час визначення «зворотного» боку зв'язків «багато до багатьох» доступні всі звичні опції налаштування таблиці та ключів.

<a name="retrieving-intermediate-table-columns"></a>
### Отримання стовпців проміжної таблиці

Як ви вже дізналися, робота зі зв'язками «багато до багатьох» вимагає наявності проміжної таблиці. Eloquent надає кілька дуже зручних способів взаємодії з нею. Наприклад, припустімо, що наша модель `User` має багато пов'язаних моделей `Role`. Звернувшись до цього зв'язку, ми можемо дістатися проміжної таблиці через атрибут `pivot` на моделях:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

Зверніть увагу: кожній отриманій моделі `Role` автоматично призначається атрибут `pivot`. Цей атрибут містить модель, що представляє проміжну таблицю.

За замовчуванням на моделі `pivot` присутні лише ключі моделей. Якщо ваша проміжна таблиця містить додаткові атрибути, їх треба вказати під час визначення зв'язку:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

Якщо ви хочете, щоб ваша проміжна таблиця мала часові мітки `created_at` та `updated_at`, які Eloquent підтримує автоматично, викличте метод `withTimestamps` під час визначення зв'язку:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Проміжні таблиці, що використовують автоматично підтримувані Eloquent часові мітки, мусять мати обидва стовпці - `created_at` та `updated_at`.

<a name="customizing-the-pivot-attribute-name"></a>
#### Налаштування імені атрибута `pivot`

Як зазначалося раніше, до атрибутів проміжної таблиці можна звертатися на моделях через атрибут `pivot`. Проте ви вільні змінити ім'я цього атрибута, щоб воно краще відображало його призначення у вашому застосунку.

Наприклад, якщо у вашому застосунку користувачі можуть підписуватися на подкасти, то між користувачами й подкастами, найімовірніше, є зв'язок «багато до багатьох». У такому разі ви можете захотіти перейменувати атрибут проміжної таблиці з `pivot` на `subscription`. Це робиться методом `as` під час визначення зв'язку:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

Коли власний атрибут проміжної таблиці задано, ви можете звертатися до її даних за новим іменем:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### Фільтрація запитів за стовпцями проміжної таблиці

Ви також можете фільтрувати результати запитів зв'язку `belongsToMany` методами `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull` та `wherePivotNotNull` під час визначення зв'язку:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```

Метод `wherePivot` додає до запиту обмеження where, але не додає вказаного значення під час створення нових моделей через визначений зв'язок. Якщо вам потрібно і робити запити, і створювати зв'язки з певним значенням pivot, скористайтеся методом `withPivotValue`:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### Сортування запитів за стовпцями проміжної таблиці

Ви можете сортувати результати запитів зв'язку `belongsToMany` методами `orderByPivot` та `orderByPivotDesc`. У наступному прикладі ми отримаємо всі найновіші бейджі користувача:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```

<a name="defining-custom-intermediate-table-models"></a>
### Визначення власних моделей проміжної таблиці

Якщо ви хочете визначити власну модель, що представлятиме проміжну таблицю вашого зв'язку «багато до багатьох», викличте метод `using` під час визначення зв'язку. Власні pivot-моделі дають змогу описати додаткову поведінку на pivot-моделі - наприклад, методи та приведення типів.

Власні pivot-моделі для зв'язків «багато до багатьох» мають успадковувати клас `Illuminate\Database\Eloquent\Relations\Pivot`, а власні pivot-моделі для поліморфних зв'язків «багато до багатьох» - клас `Illuminate\Database\Eloquent\Relations\MorphPivot`. Наприклад, ми можемо визначити модель `Role`, яка використовує власну pivot-модель `RoleUser`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

Визначаючи модель `RoleUser`, ви маєте успадкувати клас `Illuminate\Database\Eloquent\Relations\Pivot`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> [!WARNING]
> Pivot-моделі не можуть використовувати трейт `SoftDeletes`. Якщо вам потрібне м'яке видалення (soft delete) pivot-записів, подумайте про перетворення pivot-моделі на повноцінну модель Eloquent.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### Власні pivot-моделі та інкрементні ID

Якщо ви визначили зв'язок «багато до багатьох», що використовує власну pivot-модель, і ця pivot-модель має автоінкрементний первинний ключ, переконайтеся, що ваш клас pivot-моделі використовує атрибут `Table` зі значенням `incrementing`, встановленим у `true`:

```php
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Relations\Pivot;

#[Table(incrementing: true)]
class RoleUser extends Pivot
{
    // ...
}
```

<a name="polymorphic-relationships"></a>
## Поліморфні зв'язки

Поліморфний зв'язок дозволяє дочірній моделі належати більш ніж одному типу моделей через одну асоціацію. Наприклад, уявіть, що ви будуєте застосунок, у якому користувачі можуть ділитися дописами блогу та відео. У такому застосунку модель `Comment` могла б належати і моделі `Post`, і моделі `Video`.

<a name="one-to-one-polymorphic-relations"></a>
### Один до одного (поліморфний)

<a name="one-to-one-polymorphic-table-structure"></a>
#### Структура таблиць

Поліморфний зв'язок «один до одного» схожий на звичайний зв'язок «один до одного»; проте дочірня модель може належати більш ніж одному типу моделей через одну асоціацію. Наприклад, `Post` блогу та `User` можуть мати спільний поліморфний зв'язок із моделлю `Image`. Поліморфний зв'язок «один до одного» дозволяє мати одну таблицю унікальних зображень, які можуть бути пов'язані з дописами й користувачами. Спершу розгляньмо структуру таблиць:

```text
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_type - string
    imageable_id - integer
```

Зверніть увагу на стовпці `imageable_id` та `imageable_type` у таблиці `images`. Стовпець `imageable_id` міститиме значення ID допису чи користувача, а стовпець `imageable_type` - ім'я класу батьківської моделі. Стовпець `imageable_type` Eloquent використовує, щоб визначити, який «тип» батьківської моделі повернути при зверненні до зв'язку `imageable`. У цьому випадку стовпець міститиме або `App\Models\Post`, або `App\Models\User`.

<a name="one-to-one-polymorphic-model-structure"></a>
#### Структура моделей

Далі розгляньмо визначення моделей, потрібні для побудови цього зв'язку:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### Отримання зв'язку

Коли таблицю бази даних і моделі визначено, ви можете звертатися до зв'язків через свої моделі. Наприклад, щоб отримати зображення допису, звернімося до динамічної властивості зв'язку `image`:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

Батьківську модель поліморфної моделі можна отримати, звернувшись до імені методу, який викликає `morphTo`. У цьому випадку це метод `imageable` на моделі `Image`. Тож ми звернемося до нього як до динамічної властивості зв'язку:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

Зв'язок `imageable` на моделі `Image` поверне екземпляр або `Post`, або `User` - залежно від того, який тип моделі володіє зображенням.

<a name="morph-one-to-one-key-conventions"></a>
#### Угоди щодо ключів

За потреби ви можете вказати імена стовпців «id» та «type», які використовує ваша поліморфна дочірня модель. Якщо ви це робите, завжди передавайте ім'я зв'язку першим аргументом до методу `morphTo`. Зазвичай це значення має збігатися з іменем методу, тож можна скористатися константою PHP `__FUNCTION__`:

```php
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### Один до багатьох (поліморфний)

<a name="one-to-many-polymorphic-table-structure"></a>
#### Структура таблиць

Поліморфний зв'язок «один до багатьох» схожий на звичайний зв'язок «один до багатьох»; проте дочірня модель може належати більш ніж одному типу моделей через одну асоціацію. Наприклад, уявіть, що користувачі вашого застосунку можуть «коментувати» дописи та відео. За допомогою поліморфних зв'язків ви можете тримати коментарі до дописів і до відео в одній таблиці `comments`. Спершу розгляньмо структуру таблиць, потрібну для побудови цього зв'язку:

```text
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_type - string
    commentable_id - integer
```

<a name="one-to-many-polymorphic-model-structure"></a>
#### Структура моделей

Далі розгляньмо визначення моделей, потрібні для побудови цього зв'язку:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### Отримання зв'язку

Коли таблицю бази даних і моделі визначено, ви можете звертатися до зв'язків через динамічні властивості зв'язків ваших моделей. Наприклад, щоб дістатися всіх коментарів допису, скористаймося динамічною властивістю `comments`:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

Ви також можете отримати батьківську модель поліморфної дочірньої моделі, звернувшись до імені методу, який викликає `morphTo`. У цьому випадку це метод `commentable` на моделі `Comment`. Тож ми звернемося до нього як до динамічної властивості зв'язку, щоб дістатися батьківської моделі коментаря:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

Зв'язок `commentable` на моделі `Comment` поверне екземпляр або `Post`, або `Video` - залежно від того, який тип моделі є батьківським для коментаря.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### Автоматичне заповнення батьківських моделей у дочірніх

Навіть із жадібним завантаженням Eloquent можуть виникати проблеми запитів «N + 1», якщо ви звертаєтеся до батьківської моделі з дочірньої, перебираючи дочірні моделі:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

У прикладі вище виникла проблема запитів «N + 1», бо, хоч коментарі й були жадібно завантажені для кожної моделі `Post`, Eloquent не заповнює автоматично батьківський `Post` у кожній дочірній моделі `Comment`.

Якщо ви хочете, щоб Eloquent автоматично заповнював батьківські моделі в дочірніх, викличте метод `chaperone` під час визначення зв'язку `morphMany`:

```php
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

Або ж, якщо ви хочете вмикати автоматичне заповнення батьківських моделей під час виконання, викличте метод `chaperone` під час жадібного завантаження зв'язку:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### Один з багатьох (поліморфний)

Іноді модель має багато пов'язаних моделей, але вам потрібно легко отримати «найновішу» чи «найстарішу» з них. Наприклад, модель `User` може бути пов'язана з багатьма моделями `Image`, але ви хочете мати зручний спосіб працювати з найновішим зображенням, яке завантажив користувач. Цього можна досягти зв'язком типу `morphOne` у поєднанні з методами `ofMany`:

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

Так само ви можете визначити метод для отримання «найстарішого», тобто першого, пов'язаного запису:

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

За замовчуванням методи `latestOfMany` та `oldestOfMany` отримують найновішу чи найстарішу пов'язану модель за первинним ключем моделі, який має бути придатним для сортування. Проте іноді потрібно отримати одну модель із більшого зв'язку за іншим критерієм сортування.

Наприклад, за допомогою методу `ofMany` можна отримати зображення користувача з найбільшою кількістю «вподобань». Метод `ofMany` приймає першим аргументом стовпець для сортування, а другим - агрегатну функцію (`min` чи `max`), яку слід застосувати під час запиту пов'язаної моделі:

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> Можна будувати й складніші зв'язки «один з багатьох». Докладніше читайте в [документації про has one of many](#advanced-has-one-of-many-relationships).

<a name="many-to-many-polymorphic-relations"></a>
### Багато до багатьох (поліморфний)

<a name="many-to-many-polymorphic-table-structure"></a>
#### Структура таблиць

Поліморфні зв'язки «багато до багатьох» дещо складніші за зв'язки «morph one» та «morph many». Наприклад, моделі `Post` та `Video` можуть мати спільний поліморфний зв'язок із моделлю `Tag`. Поліморфний зв'язок «багато до багатьох» у цій ситуації дозволив би вашому застосунку мати одну таблицю унікальних тегів, які можуть бути пов'язані з дописами чи відео. Спершу розгляньмо структуру таблиць, потрібну для побудови цього зв'язку:

```text
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_type - string
    taggable_id - integer
```

> [!NOTE]
> Перш ніж заглиблюватися в поліморфні зв'язки «багато до багатьох», вам може бути корисно прочитати документацію про звичайні [зв'язки «багато до багатьох»](#many-to-many).

<a name="many-to-many-polymorphic-model-structure"></a>
#### Структура моделей

Далі ми готові визначити зв'язки на моделях. Моделі `Post` і `Video` матимуть метод `tags`, який викликає метод `morphToMany`, наданий базовим класом моделі Eloquent.

Метод `morphToMany` приймає ім'я пов'язаної моделі, а також «ім'я зв'язку». Зважаючи на ім'я, яке ми дали проміжній таблиці, та ключі, які вона містить, ми називатимемо цей зв'язок «taggable»:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### Визначення зворотного зв'язку

Далі на моделі `Tag` слід визначити метод для кожної з її можливих батьківських моделей. Тож у цьому прикладі ми визначимо методи `posts` і `videos`. Обидва мають повертати результат методу `morphedByMany`.

Метод `morphedByMany` приймає ім'я пов'язаної моделі, а також «ім'я зв'язку». Зважаючи на ім'я, яке ми дали проміжній таблиці, та ключі, які вона містить, ми називатимемо цей зв'язок «taggable»:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### Отримання зв'язку

Коли таблицю бази даних і моделі визначено, ви можете звертатися до зв'язків через свої моделі. Наприклад, щоб дістатися всіх тегів допису, скористайтеся динамічною властивістю зв'язку `tags`:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

Батьківську модель поліморфного зв'язку можна отримати з поліморфної дочірньої моделі, звернувшись до імені методу, який викликає `morphedByMany`. У цьому випадку це методи `posts` або `videos` на моделі `Tag`:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a name="custom-polymorphic-types"></a>
### Власні поліморфні типи

За замовчуванням Laravel зберігає «тип» пов'язаної моделі як повне ім'я класу. Наприклад, у наведеному вище прикладі зв'язку «один до багатьох», де модель `Comment` може належати моделі `Post` чи `Video`, значенням `commentable_type` за замовчуванням буде відповідно `App\Models\Post` або `App\Models\Video`. Проте ви можете захотіти відв'язати ці значення від внутрішньої структури вашого застосунку.

Наприклад, замість імен моделей ми можемо використовувати як «тип» прості рядки на кшталт `post` і `video`. Завдяки цьому значення поліморфного стовпця «type» у базі даних залишатимуться коректними, навіть якщо моделі перейменують:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

Викликати метод `enforceMorphMap` можна в методі `boot` вашого класу `App\Providers\AppServiceProvider` або, за бажанням, створити окремий сервіс-провайдер.

Морф-аліас заданої моделі можна визначити під час виконання методом моделі `getMorphClass`. І навпаки: повне ім'я класу, пов'язане з морф-аліасом, можна визначити методом `Relation::getMorphedModel`:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> Коли ви додаєте «морф-мапу» до наявного застосунку, кожне значення морфованого стовпця `*_type` у базі даних, яке ще містить повне ім'я класу, доведеться перетворити на його ім'я з «мапи».

<a name="dynamic-relationships"></a>
### Динамічні зв'язки

Метод `resolveRelationUsing` дозволяє визначати зв'язки між моделями Eloquent під час виконання. Хоча для звичайної розробки застосунків це зазвичай не рекомендується, іноді це буває корисно при створенні пакетів для Laravel.

Метод `resolveRelationUsing` приймає бажане ім'я зв'язку першим аргументом. Другим аргументом має бути замикання, що приймає екземпляр моделі й повертає коректне визначення зв'язку Eloquent. Зазвичай динамічні зв'язки налаштовують у методі boot [сервіс-провайдера](/docs/{{version}}/providers):

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> Визначаючи динамічні зв'язки, завжди передавайте методам зв'язків Eloquent явні аргументи з іменами ключів.

<a name="querying-relations"></a>
## Запити до зв'язків

Оскільки всі зв'язки Eloquent визначені через методи, ви можете викликати ці методи, щоб отримати екземпляр зв'язку, не виконуючи запиту для завантаження пов'язаних моделей. До того ж усі типи зв'язків Eloquent водночас є [конструкторами запитів](/docs/{{version}}/queries), тож ви можете й далі додавати обмеження до запиту зв'язку, перш ніж остаточно виконати SQL-запит до вашої бази даних.

Наприклад, уявіть застосунок блогу, у якому модель `User` має багато пов'язаних моделей `Post`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

Ви можете зробити запит до зв'язку `posts` і додати до нього додаткові обмеження ось так:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

На зв'язку можна використовувати будь-які методи [конструктора запитів](/docs/{{version}}/queries) Laravel, тож обов'язково перегляньте його документацію, щоб дізнатися про всі доступні вам методи.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### Ланцюжки умов `orWhere` після зв'язків

Як показано в прикладі вище, ви вільні додавати до зв'язків додаткові обмеження під час запиту. Проте будьте обережні, додаючи до зв'язку умови `orWhere` у ланцюжок: логічно вони згрупуються на тому самому рівні, що й обмеження зв'язку:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

Приклад вище згенерує такий SQL. Як бачите, умова `or` вказує запиту повертати _будь-який_ допис із понад 100 голосами. Запит більше не обмежений конкретним користувачем:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

У більшості випадків варто скористатися [логічними групами](/docs/{{version}}/queries#logical-grouping), щоб згрупувати умовні перевірки в дужках:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

Приклад вище дасть такий SQL. Зверніть увагу, що логічне групування правильно згрупувало обмеження, і запит лишається обмеженим конкретним користувачем:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### Методи зв'язків проти динамічних властивостей

Якщо вам не потрібно додавати до запиту зв'язку Eloquent додаткові обмеження, ви можете звертатися до зв'язку так, ніби це властивість. Наприклад, продовжуючи роботу з моделями `User` і `Post`, ми можемо отримати всі дописи користувача ось так:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

Динамічні властивості зв'язків виконують «ліниве завантаження» (lazy loading): вони завантажують дані зв'язку лише тоді, коли ви до них справді звертаєтеся. Через це розробники часто застосовують [жадібне завантаження](#eager-loading) (eager loading), щоб наперед завантажити зв'язки, до яких вони точно звертатимуться після завантаження моделі. Жадібне завантаження суттєво зменшує кількість SQL-запитів, потрібних для завантаження зв'язків моделі.

<a name="querying-relationship-existence"></a>
### Запити за наявністю зв'язку

Отримуючи записи моделей, ви можете захотіти обмежити результати наявністю зв'язку. Наприклад, уявіть, що вам потрібні всі дописи блогу, які мають щонайменше один коментар. Для цього передайте ім'я зв'язку методам `has` та `orHas`:

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

Ви також можете вказати оператор і значення кількості, щоб додатково налаштувати запит:

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

Вкладені конструкції `has` будуються через «крапкову» нотацію. Наприклад, ви можете отримати всі дописи, які мають щонайменше один коментар, що має щонайменше одне зображення:

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

Якщо вам потрібно ще більше можливостей, скористайтеся методами `whereHas` та `orWhereHas`, щоб додати до ваших запитів `has` додаткові обмеження - наприклад, перевірити вміст коментаря:

```php
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Наразі Eloquent не підтримує запити за наявністю зв'язку між різними базами даних. Зв'язки мають існувати в межах однієї бази даних.

<a name="many-to-many-relationship-existence-queries"></a>
#### Запити за наявністю зв'язку «багато до багатьох»

Метод `whereAttachedTo` дозволяє шукати моделі, приєднані зв'язком «багато до багатьох» до заданої моделі чи колекції моделей:

```php
$users = User::whereAttachedTo($role)->get();
```

Ви також можете передати методу `whereAttachedTo` екземпляр [колекції](/docs/{{version}}/eloquent-collections). У такому разі Laravel поверне моделі, приєднані до будь-якої з моделей у колекції:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### Вбудовані запити за наявністю зв'язку

Якщо ви хочете зробити запит за наявністю зв'язку з однією простою умовою where, приєднаною до запиту зв'язку, зручнішими можуть бути методи `whereRelation`, `orWhereRelation`, `whereMorphRelation` та `orWhereMorphRelation`. Наприклад, ми можемо знайти всі дописи, що мають незатверджені коментарі:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

Звісно, як і у викликах методу `where` конструктора запитів, ви можете вказати оператор:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
### Запити за відсутністю зв'язку

Отримуючи записи моделей, ви можете захотіти обмежити результати відсутністю зв'язку. Наприклад, уявіть, що вам потрібні всі дописи блогу, які **не** мають жодного коментаря. Для цього передайте ім'я зв'язку методам `doesntHave` та `orDoesntHave`:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

Якщо вам потрібно ще більше можливостей, скористайтеся методами `whereDoesntHave` та `orWhereDoesntHave`, щоб додати до ваших запитів `doesntHave` додаткові обмеження - наприклад, перевірити вміст коментаря:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

Ви можете скористатися «крапковою» нотацією, щоб виконати запит до вкладеного зв'язку. Наприклад, наступний запит поверне всі дописи без коментарів, а також дописи з коментарями, жоден із яких не належить заблокованим користувачам:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Запити до зв'язків Morph To

Щоб зробити запит за наявністю зв'язків «morph to», скористайтеся методами `whereHasMorph` та `whereDoesntHaveMorph`. Ці методи приймають ім'я зв'язку першим аргументом. Далі вони приймають імена пов'язаних моделей, які ви хочете включити до запиту. Нарешті, ви можете передати замикання, що налаштує запит зв'язку:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

Іноді вам може знадобитися додати обмеження запиту залежно від «типу» пов'язаної поліморфної моделі. Замикання, передане методу `whereHasMorph`, може приймати другим аргументом значення `$type`. Цей аргумент дозволяє перевірити «тип» запиту, який будується:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

Іноді потрібно зробити запит до дочірніх записів батьківської моделі зв'язку «morph to». Цього можна досягти методами `whereMorphedTo` та `whereNotMorphedTo`, які автоматично визначать правильне зіставлення морф-типу для заданої моделі. Ці методи приймають ім'я зв'язку `morphTo` першим аргументом і пов'язану батьківську модель другим:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### Запит до всіх пов'язаних моделей

Замість масиву можливих поліморфних моделей ви можете передати `*` як символ підстановки. Це вкаже Laravel отримати з бази даних усі можливі поліморфні типи. Для цієї операції Laravel виконає додатковий запит:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## Агрегування пов'язаних моделей

<a name="counting-related-models"></a>
### Підрахунок пов'язаних моделей

Іноді потрібно порахувати кількість пов'язаних моделей для заданого зв'язку, не завантажуючи самі моделі. Для цього скористайтеся методом `withCount`. Метод `withCount` додасть до отриманих моделей атрибут `{relation}_count`:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

Передавши методу `withCount` масив, ви можете додати «кількості» для кількох зв'язків, а також додаткові обмеження до запитів:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

Ви також можете дати результату підрахунку зв'язку аліас, що дозволяє мати кілька підрахунків для того самого зв'язку:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a name="deferred-count-loading"></a>
#### Відкладене завантаження кількості

За допомогою методу `loadCount` ви можете завантажити кількість для зв'язку вже після того, як батьківську модель отримано:

```php
$book = Book::first();

$book->loadCount('genres');
```

Якщо вам потрібно задати додаткові обмеження для запиту підрахунку, передайте масив із ключами-іменами зв'язків, які ви хочете порахувати. Значеннями масиву мають бути замикання, що приймають екземпляр конструктора запитів:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### Підрахунок зв'язків і власні вирази select

Якщо ви поєднуєте `withCount` із виразом `select`, обов'язково викликайте `withCount` після методу `select`:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### Інші агрегатні функції

Окрім методу `withCount`, Eloquent надає методи `withMin`, `withMax`, `withAvg`, `withSum` та `withExists`. Вони додадуть до отриманих моделей атрибут `{relation}_{function}_{column}`:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

Якщо ви хочете звертатися до результату агрегатної функції за іншим іменем, вкажіть власний аліас:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

Як і у випадку з методом `loadCount`, для цих методів також доступні відкладені версії. Ці додаткові агрегатні операції можна виконувати на вже отриманих моделях Eloquent:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

Якщо ви поєднуєте ці агрегатні методи з виразом `select`, обов'язково викликайте їх після методу `select`:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Підрахунок пов'язаних моделей у зв'язках Morph To

Якщо ви хочете жадібно завантажити зв'язок «morph to», а також кількості пов'язаних моделей для різних сутностей, які цей зв'язок може повернути, скористайтеся методом `with` у поєднанні з методом `morphWithCount` зв'язку `morphTo`.

У цьому прикладі припустімо, що моделі `Photo` та `Post` можуть створювати моделі `ActivityFeed`. Припустімо також, що модель `ActivityFeed` визначає зв'язок «morph to» на ім'я `parentable`, який дозволяє отримати батьківську модель `Photo` чи `Post` для заданого екземпляра `ActivityFeed`. Крім того, припустімо, що моделі `Photo` «мають багато» моделей `Tag`, а моделі `Post` - багато моделей `Comment`.

Тепер уявімо, що ми хочемо отримати екземпляри `ActivityFeed` і жадібно завантажити батьківські моделі `parentable` для кожного з них. Крім того, ми хочемо отримати кількість тегів, пов'язаних із кожним батьківським фото, і кількість коментарів, пов'язаних із кожним батьківським дописом:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

<a name="morph-to-deferred-count-loading"></a>
#### Відкладене завантаження кількості

Припустімо, ми вже отримали набір моделей `ActivityFeed` і тепер хочемо завантажити вкладені кількості зв'язків для різних моделей `parentable`, пов'язаних зі стрічкою активності. Зробити це можна методом `loadMorphCount`:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## Жадібне завантаження

Коли ви звертаєтеся до зв'язків Eloquent як до властивостей, пов'язані моделі завантажуються «ліниво» (lazy loading). Це означає, що дані зв'язку не завантажуються, доки ви вперше не звернетеся до властивості. Проте Eloquent уміє «жадібно завантажувати» (eager loading) зв'язки вже під час запиту до батьківської моделі. Жадібне завантаження знімає проблему запитів «N + 1». Щоб проілюструвати цю проблему, розгляньмо модель `Book`, яка «належить» моделі `Author`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

А тепер отримаймо всі книжки та їхніх авторів:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

Цей цикл виконає один запит, щоб отримати всі книжки з таблиці бази даних, а потім ще по одному запиту на кожну книжку, щоб отримати її автора. Тож якщо в нас 25 книжок, наведений код виконає 26 запитів: один по самі книжки і ще 25, щоб отримати автора кожної книжки.

На щастя, ми можемо скористатися жадібним завантаженням і звести цю операцію лише до двох запитів. Будуючи запит, ви можете вказати, які зв'язки слід завантажити жадібно, за допомогою методу `with`:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

Для цієї операції буде виконано лише два запити - один, щоб отримати всі книжки, і один, щоб отримати всіх авторів усіх книжок:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### Жадібне завантаження кількох зв'язків

Іноді потрібно жадібно завантажити кілька різних зв'язків. Для цього просто передайте методу `with` масив зв'язків:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### Вкладене жадібне завантаження

Щоб жадібно завантажити зв'язки зв'язку, скористайтеся «крапковим» синтаксисом. Наприклад, завантажмо жадібно всіх авторів книжки та всі особисті контакти автора:

```php
$books = Book::with('author.contacts')->get();
```

Або ж ви можете задати вкладені жадібно завантажувані зв'язки, передавши методу `with` вкладений масив, - це буває зручно при жадібному завантаженні кількох вкладених зв'язків:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### Вкладене жадібне завантаження зв'язків `morphTo`

Якщо ви хочете жадібно завантажити зв'язок `morphTo`, а також вкладені зв'язки різних сутностей, які цей зв'язок може повернути, скористайтеся методом `with` у поєднанні з методом `morphWith` зв'язку `morphTo`. Щоб проілюструвати цей метод, розгляньмо таку модель:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

У цьому прикладі припустімо, що моделі `Event`, `Photo` та `Post` можуть створювати моделі `ActivityFeed`. Крім того, припустімо, що моделі `Event` належать моделі `Calendar`, моделі `Photo` пов'язані з моделями `Tag`, а моделі `Post` належать моделі `Author`.

З такими визначеннями моделей і зв'язків ми можемо отримати екземпляри моделі `ActivityFeed` і жадібно завантажити всі моделі `parentable` та їхні вкладені зв'язки:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a name="eager-loading-specific-columns"></a>
#### Жадібне завантаження певних стовпців

Не завжди вам потрібні всі стовпці зв'язків, які ви отримуєте. Тому Eloquent дозволяє вказати, які саме стовпці зв'язку ви хочете отримати:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> Користуючись цією можливістю, завжди включайте до списку потрібних стовпців стовпець `id` та всі відповідні стовпці зовнішніх ключів.

<a name="eager-loading-by-default"></a>
#### Жадібне завантаження за замовчуванням

Іноді потрібно завжди завантажувати певні зв'язки під час отримання моделі. Щоб цього досягти, визначте на моделі властивість `$with`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

Якщо ви хочете прибрати елемент із властивості `$with` для одного запиту, скористайтеся методом `without`:

```php
$books = Book::without('author')->get();
```

Якщо ви хочете перевизначити всі елементи властивості `$with` для одного запиту, скористайтеся методом `withOnly`:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### Обмеження жадібного завантаження

Іноді потрібно жадібно завантажити зв'язок, але водночас задати додаткові умови для запиту жадібного завантаження. Цього можна досягти, передавши методу `with` масив зв'язків, де ключ масиву - ім'я зв'язку, а значення - замикання, що додає додаткові обмеження до запиту жадібного завантаження:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

У цьому прикладі Eloquent жадібно завантажить лише ті дописи, чий стовпець `title` містить слово `code`. Ви можете викликати й інші методи [конструктора запитів](/docs/{{version}}/queries), щоб додатково налаштувати операцію жадібного завантаження:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### Обмеження жадібного завантаження зв'язків `morphTo`

Якщо ви жадібно завантажуєте зв'язок `morphTo`, Eloquent виконає кілька запитів, щоб отримати кожен тип пов'язаної моделі. Ви можете додати до кожного з цих запитів додаткові обмеження методом `constrain` зв'язку `MorphTo`:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

У цьому прикладі Eloquent жадібно завантажить лише неприховані дописи та відео зі значенням `type`, що дорівнює «educational».

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### Обмеження жадібного завантаження наявністю зв'язку

Іноді вам може знадобитися перевірити наявність зв'язку й водночас завантажити цей зв'язок за тими самими умовами. Наприклад, ви можете захотіти отримати лише ті моделі `User`, що мають дочірні моделі `Post`, які відповідають заданій умові запиту, і водночас жадібно завантажити ці дописи. Цього можна досягти методом `withWhereHas`:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### Відкладене жадібне завантаження

Іноді потрібно жадібно завантажити зв'язок уже після того, як батьківську модель отримано. Наприклад, це може бути корисно, якщо вам треба динамічно вирішувати, чи завантажувати пов'язані моделі:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

Якщо вам потрібно задати додаткові обмеження для запиту жадібного завантаження, передайте масив із ключами-іменами зв'язків, які ви хочете завантажити. Значеннями масиву мають бути екземпляри замикань, що приймають екземпляр запиту:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

Щоб завантажити зв'язок лише тоді, коли його ще не завантажено, скористайтеся методом `loadMissing`:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### Вкладене відкладене жадібне завантаження та `morphTo`

Якщо ви хочете жадібно завантажити зв'язок `morphTo`, а також вкладені зв'язки різних сутностей, які цей зв'язок може повернути, скористайтеся методом `loadMorph`.

Цей метод приймає ім'я зв'язку `morphTo` першим аргументом і масив пар модель / зв'язок другим. Щоб проілюструвати цей метод, розгляньмо таку модель:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

У цьому прикладі припустімо, що моделі `Event`, `Photo` та `Post` можуть створювати моделі `ActivityFeed`. Крім того, припустімо, що моделі `Event` належать моделі `Calendar`, моделі `Photo` пов'язані з моделями `Tag`, а моделі `Post` належать моделі `Author`.

З такими визначеннями моделей і зв'язків ми можемо отримати екземпляри моделі `ActivityFeed` і жадібно завантажити всі моделі `parentable` та їхні вкладені зв'язки:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="automatic-eager-loading"></a>
### Автоматичне жадібне завантаження

> [!WARNING]
> Ця можливість наразі перебуває в бета-версії, щоб зібрати відгуки спільноти. Її поведінка та функціональність можуть змінитися навіть у патч-випусках.

У багатьох випадках Laravel може автоматично жадібно завантажувати зв'язки, до яких ви звертаєтеся. Щоб увімкнути автоматичне жадібне завантаження, викличте метод `Model::automaticallyEagerLoadRelationships` у методі `boot` вашого `AppServiceProvider`:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

Коли цю можливість увімкнено, Laravel намагатиметься автоматично завантажити будь-які зв'язки, до яких ви звертаєтеся й які ще не було завантажено. Наприклад, розгляньмо такий сценарій:

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```

Зазвичай наведений код виконав би запит для кожного користувача, щоб отримати його дописи, а також запит для кожного допису, щоб отримати його коментарі. Проте коли можливість `automaticallyEagerLoadRelationships` увімкнено, Laravel автоматично [відкладено жадібно завантажить](#lazy-eager-loading) дописи всіх користувачів колекції, щойно ви спробуєте звернутися до дописів будь-кого з отриманих користувачів. Так само, коли ви спробуєте звернутися до коментарів будь-якого отриманого допису, коментарі буде відкладено жадібно завантажено для всіх спочатку отриманих дописів.

Якщо ви не хочете вмикати автоматичне жадібне завантаження глобально, ви все одно можете ввімкнути цю можливість для окремого екземпляра колекції Eloquent, викликавши на колекції метод `withRelationshipAutoloading`:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### Заборона лінивого завантаження

Як уже обговорювалося, жадібне завантаження зв'язків часто дає суттєвий виграш у продуктивності вашого застосунку. Тож, за бажання, ви можете вказати Laravel завжди забороняти ліниве завантаження зв'язків. Для цього викличте метод `preventLazyLoading`, який надає базовий клас моделі Eloquent. Зазвичай цей метод викликають у методі `boot` класу `AppServiceProvider` вашого застосунку.

Метод `preventLazyLoading` приймає необов'язковий булевий аргумент, що вказує, чи слід забороняти ліниве завантаження. Наприклад, ви можете захотіти вимкнути ліниве завантаження лише в непродакшн-середовищах, щоб ваше продакшн-середовище й далі працювало нормально, навіть якщо в продакшн-коді випадково опиниться ліниво завантажений зв'язок:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

Після заборони лінивого завантаження Eloquent кидатиме виняток `Illuminate\Database\LazyLoadingViolationException`, коли ваш застосунок спробує ліниво завантажити будь-який зв'язок Eloquent.

Ви можете налаштувати поведінку при порушеннях лінивого завантаження методом `handleLazyLoadingViolationsUsing`. Наприклад, за допомогою цього методу можна вказати, щоб порушення лише логувалися, а не переривали виконання застосунку винятками:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## Вставлення й оновлення пов'язаних моделей

<a name="the-save-method"></a>
### Метод `save`

Eloquent надає зручні методи для додавання нових моделей до зв'язків. Наприклад, вам може знадобитися додати новий коментар до допису. Замість того щоб вручну встановлювати атрибут `post_id` на моделі `Comment`, ви можете вставити коментар методом `save` зв'язку:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

Зверніть увагу: ми не зверталися до зв'язку `comments` як до динамічної властивості. Натомість ми викликали метод `comments`, щоб отримати екземпляр зв'язку. Метод `save` автоматично додасть новій моделі `Comment` відповідне значення `post_id`.

Якщо вам потрібно зберегти кілька пов'язаних моделей, скористайтеся методом `saveMany`:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

Методи `save` та `saveMany` збережуть передані екземпляри моделей, але не додадуть щойно збережені моделі до вже завантажених у пам'ять зв'язків батьківської моделі. Якщо ви плануєте звертатися до зв'язку після використання `save` чи `saveMany`, вам може знадобитися метод `refresh`, щоб перезавантажити модель та її зв'язки:

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
#### Рекурсивне збереження моделей і зв'язків

Якщо ви хочете зберегти (`save`) свою модель разом з усіма пов'язаними з нею зв'язками, скористайтеся методом `push`. У цьому прикладі буде збережено модель `Post`, а також її коментарі й авторів коментарів:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

Метод `pushQuietly` дозволяє зберегти модель та пов'язані з нею зв'язки, не викликаючи жодних подій:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### Метод `create`

Окрім методів `save` та `saveMany`, ви можете скористатися методом `create`, який приймає масив атрибутів, створює модель і вставляє її в базу даних. Різниця між `save` та `create` полягає в тому, що `save` приймає повний екземпляр моделі Eloquent, а `create` - звичайний PHP-`array`. Щойно створену модель буде повернено методом `create`:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

Щоб створити кілька пов'язаних моделей, скористайтеся методом `createMany`:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

Методи `createQuietly` та `createManyQuietly` дозволяють створити модель (моделі), не відправляючи жодних подій:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```

Ви також можете скористатися методами `findOrNew`, `firstOrNew`, `firstOrCreate` та `updateOrCreate`, щоб [створювати й оновлювати моделі у зв'язках](/docs/{{version}}/eloquent#upserts).

> [!NOTE]
> Перш ніж використовувати метод `create`, обов'язково перегляньте документацію про [масове призначення](/docs/{{version}}/eloquent#mass-assignment).

<a name="updating-belongs-to-relationships"></a>
### Зв'язки Belongs To

Якщо ви хочете призначити дочірню модель новій батьківській, скористайтеся методом `associate`. У цьому прикладі модель `User` визначає зв'язок `belongsTo` із моделлю `Account`. Метод `associate` встановить зовнішній ключ на дочірній моделі:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

Щоб прибрати батьківську модель із дочірньої, скористайтеся методом `dissociate`. Цей метод встановить зовнішній ключ зв'язку в `null`:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### Зв'язки «багато до багатьох»

<a name="attaching-detaching"></a>
#### Приєднання / від'єднання

Eloquent також надає методи, які роблять роботу зі зв'язками «багато до багатьох» зручнішою. Наприклад, уявімо, що користувач може мати багато ролей, а роль - багато користувачів. Метод `attach` дозволяє приєднати роль до користувача, вставивши запис у проміжну таблицю зв'язку:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

Приєднуючи зв'язок до моделі, ви також можете передати масив додаткових даних, які слід вставити до проміжної таблиці:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

Іноді буває потрібно забрати роль у користувача. Щоб видалити запис зв'язку «багато до багатьох», скористайтеся методом `detach`. Метод `detach` видалить відповідний запис із проміжної таблиці; проте обидві моделі залишаться в базі даних:

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

Для зручності `attach` і `detach` також приймають на вхід масиви ID:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### Синхронізація асоціацій

Ви також можете скористатися методом `sync`, щоб побудувати асоціації «багато до багатьох». Метод `sync` приймає масив ID, які слід розмістити в проміжній таблиці. Будь-які ID, яких немає в переданому масиві, буде видалено з проміжної таблиці. Тож після завершення цієї операції в проміжній таблиці залишаться лише ID із переданого масиву:

```php
$user->roles()->sync([1, 2, 3]);
```

Разом з ID ви можете передати й додаткові значення для проміжної таблиці:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

Якщо ви хочете вставити однакові значення проміжної таблиці для кожного із синхронізованих ID моделей, скористайтеся методом `syncWithPivotValues`:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

Якщо ви не хочете від'єднувати наявні ID, яких немає в переданому масиві, скористайтеся методом `syncWithoutDetaching`:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### Перемикання асоціацій

Зв'язок «багато до багатьох» також надає метод `toggle`, який «перемикає» статус приєднання для заданих ID пов'язаних моделей. Якщо заданий ID наразі приєднано, його буде від'єднано. І навпаки: якщо його наразі від'єднано, його буде приєднано:

```php
$user->roles()->toggle([1, 2, 3]);
```

Разом з ID ви можете передати й додаткові значення для проміжної таблиці:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="transactional-pivot-operations"></a>
#### Транзакційні pivot-операції

Кожна з розглянутих вище pivot-операцій має також варіант `OrFail` (`attachOrFail`, `detachOrFail`, `syncOrFail`, `syncWithoutDetachingOrFail` та `toggleOrFail`), який загортає операцію в транзакцію бази даних, тож усі зміни автоматично відкочуються, якщо буде кинуто виняток:

```php
$user->roles()->attachOrFail([1, 2, 3]);

$user->roles()->syncOrFail([1, 2, 3]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### Оновлення запису в проміжній таблиці

Якщо вам потрібно оновити наявний рядок у проміжній таблиці вашого зв'язку, скористайтеся методом `updateExistingPivot`. Цей метод приймає зовнішній ключ проміжного запису та масив атрибутів для оновлення:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## Оновлення часових міток батьківської моделі

Коли модель визначає зв'язок `belongsTo` чи `belongsToMany` з іншою моделлю - наприклад, `Comment`, що належить `Post`, - іноді буває корисно оновлювати часову мітку батьківської моделі при оновленні дочірньої.

Наприклад, коли оновлюється модель `Comment`, ви можете захотіти автоматично «торкнутися» часової мітки `updated_at` допису-власника `Post`, щоб їй було встановлено поточні дату й час. Щоб цього досягти, застосуйте до дочірньої моделі атрибут `Touches` з іменами зв'язків, чиї часові мітки `updated_at` слід оновлювати при оновленні дочірньої моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Touches;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Touches(['post'])]
class Comment extends Model
{
    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> Часові мітки батьківської моделі оновлюватимуться лише тоді, коли дочірню модель оновлено методом `save` Eloquent.
