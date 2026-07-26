---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: фабрики

- [Вступ](#introduction)
- [Опис фабрик моделей](#defining-model-factories)
    - [Створення фабрик](#generating-factories)
    - [Стани фабрик](#factory-states)
    - [Колбеки фабрик](#factory-callbacks)
- [Створення моделей через фабрики](#creating-models-using-factories)
    - [Створення екземплярів моделей](#instantiating-models)
    - [Збереження моделей](#persisting-models)
    - [Послідовності](#sequences)
- [Зв'язки у фабриках](#factory-relationships)
    - [Зв'язки «має багато»](#has-many-relationships)
    - [Зв'язки «належить до»](#belongs-to-relationships)
    - [Зв'язки «багато до багатьох»](#many-to-many-relationships)
    - [Поліморфні зв'язки](#polymorphic-relationships)
    - [Опис зв'язків усередині фабрик](#defining-relationships-within-factories)
    - [Повторне використання наявної моделі у зв'язках](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## Вступ

Тестуючи застосунок чи наповнюючи базу даних, вам може знадобитися вставити в неї кілька записів. Замість того щоб вручну задавати значення кожного стовпця, Laravel дозволяє описати набір атрибутів за замовчуванням для кожної з ваших [моделей Eloquent](/docs/{{version}}/eloquent) - за допомогою фабрик моделей.

Щоб побачити приклад фабрики, погляньте на файл `database/factories/UserFactory.php` у вашому застосунку. Ця фабрика є в усіх нових застосунках Laravel і містить такий опис:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

Як бачите, у найпростішому вигляді фабрики - це класи, що розширюють базовий клас фабрики Laravel і описують метод `definition`. Метод `definition` повертає набір значень атрибутів за замовчуванням, які слід застосувати при створенні моделі через фабрику.

Через хелпер `fake` фабрики мають доступ до PHP-бібліотеки [Faker](https://github.com/FakerPHP/Faker), яка дозволяє зручно генерувати різноманітні випадкові дані для тестування та наповнення бази.

> [!NOTE]
> Ви можете змінити локаль Faker для свого застосунку, оновивши опцію `faker_locale` у файлі конфігурації `config/app.php`.

<a name="defining-model-factories"></a>
## Опис фабрик моделей

<a name="generating-factories"></a>
### Створення фабрик

Щоб створити фабрику, виконайте [artisan-команду](/docs/{{version}}/artisan) `make:factory`:

```shell
php artisan make:factory PostFactory
```

Новий клас фабрики потрапить до каталогу `database/factories`.

<a name="factory-and-model-discovery-conventions"></a>
#### Конвенції пошуку моделей і фабрик

Коли ви описали фабрики, ви можете скористатися статичним методом `factory`, який моделі отримують від трейта `Illuminate\Database\Eloquent\Factories\HasFactory`, щоб створити екземпляр фабрики для цієї моделі.

Метод `factory` трейта `HasFactory` визначає потрібну фабрику за конвенціями. А саме: метод шукає в просторі імен `Database\Factories` фабрику, назва класу якої збігається з назвою моделі та має суфікс `Factory`. Якщо ці конвенції не підходять вашому застосунку чи фабриці, додайте до моделі атрибут `UseFactory`, щоб вказати фабрику вручну:

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

Або ж ви можете перевизначити в моделі метод `newFactory`, щоб він одразу повертав екземпляр відповідної фабрики:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

Далі скористайтеся на відповідній фабриці атрибутом `UseModel`, щоб указати модель:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Attributes\UseModel;
use Illuminate\Database\Eloquent\Factories\Factory;

#[UseModel(Flight::class)]
class FlightFactory extends Factory
{
    // ...
}
```

<a name="factory-states"></a>
### Стани фабрик

Методи маніпуляції станом дозволяють описати окремі зміни, які можна застосовувати до фабрик моделей у будь-яких поєднаннях. Наприклад, ваша фабрика `Database\Factories\UserFactory` може мати метод стану `suspended`, що змінює одне зі значень атрибутів за замовчуванням.

Методи перетворення стану зазвичай викликають метод `state` базового класу фабрики Laravel. Метод `state` приймає замикання, яке отримає масив сирих атрибутів, описаних для фабрики, і має повернути масив атрибутів для зміни:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="trashed-state"></a>
#### Стан «у кошику»

Якщо вашу модель Eloquent можна [м'яко видаляти](/docs/{{version}}/eloquent#soft-deleting), ви можете викликати вбудований метод стану `trashed`, щоб указати: створена модель має бути вже «м'яко видаленою». Описувати стан `trashed` вручну не потрібно - він автоматично доступний усім фабрикам:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### Колбеки фабрик

Колбеки фабрик реєструються методами `afterMaking` та `afterCreating` і дозволяють виконати додаткові завдання після створення моделі. Реєструйте ці колбеки в методі `configure` вашого класу фабрики. Laravel викличе цей метод автоматично при створенні екземпляра фабрики:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```

Ви можете також реєструвати колбеки фабрик у методах станів, щоб виконувати додаткові завдання, специфічні для конкретного стану:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```

<a name="creating-models-using-factories"></a>
## Створення моделей через фабрики

<a name="instantiating-models"></a>
### Створення екземплярів моделей

Коли ви описали фабрики, ви можете скористатися статичним методом `factory`, який моделі отримують від трейта `Illuminate\Database\Eloquent\Factories\HasFactory`, щоб створити екземпляр фабрики для цієї моделі. Погляньмо на кілька прикладів створення моделей. Спершу скористаємося методом `make`, щоб створити моделі, не зберігаючи їх у базі даних:

```php
use App\Models\User;

$user = User::factory()->make();
```

Створити колекцію з багатьох моделей можна методом `count`:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### Застосування станів

Ви можете також застосувати до моделей будь-які зі своїх [станів](#factory-states). Якщо ви хочете застосувати кілька перетворень стану, просто викличте методи перетворення один за одним:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### Перевизначення атрибутів

Якщо ви хочете перевизначити деякі значення моделей за замовчуванням, передайте методу `make` масив значень. Буде замінено лише вказані атрибути, а решта лишиться зі значеннями за замовчуванням, які задає фабрика:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

Або ж метод `state` можна викликати прямо на екземплярі фабрики, щоб виконати інлайнове перетворення стану:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> [Захист від масового призначення](/docs/{{version}}/eloquent#mass-assignment) автоматично вимикається, коли моделі створюються через фабрики.

<a name="persisting-models"></a>
### Збереження моделей

Метод `create` створює екземпляри моделей і зберігає їх у базі даних методом `save` Eloquent:

```php
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

Ви можете перевизначити атрибути моделі за замовчуванням, передавши методу `create` масив атрибутів:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### Послідовності

Іноді вам потрібно чергувати значення певного атрибута для кожної створеної моделі. Це робиться описом перетворення стану як послідовності. Наприклад, ви можете чергувати значення стовпця `admin` між `Y` і `N` для кожного створеного користувача:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```

У цьому прикладі буде створено п'ятьох користувачів зі значенням `admin`, що дорівнює `Y`, і п'ятьох зі значенням `N`.

За потреби ви можете передати як значення послідовності замикання. Його буде викликано щоразу, коли послідовності потрібне нове значення:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

Усередині замикання послідовності ви маєте доступ до властивості `$index` екземпляра послідовності, який передається в замикання. Властивість `$index` містить кількість ітерацій послідовності, що вже відбулися:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

Для зручності послідовності можна застосовувати й методом `sequence`, який усередині просто викликає метод `state`. Метод `sequence` приймає замикання або масиви послідовних атрибутів:

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a name="factory-relationships"></a>
## Зв'язки у фабриках

<a name="has-many-relationships"></a>
### Зв'язки «має багато»

Далі розгляньмо побудову зв'язків моделей Eloquent за допомогою плавних методів фабрик Laravel. Спершу припустімо, що наш застосунок має моделі `App\Models\User` та `App\Models\Post`. Припустімо також, що модель `User` описує зв'язок `hasMany` з `Post`. Ми можемо створити користувача з трьома постами методом `has`, який дають фабрики Laravel. Метод `has` приймає екземпляр фабрики:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

За конвенцією, коли ви передаєте методу `has` модель `Post`, Laravel вважатиме, що модель `User` має метод `posts`, який описує цей зв'язок. За потреби ви можете явно вказати назву зв'язку, з яким хочете працювати:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

Звісно, ви можете виконувати маніпуляції станом і над пов'язаними моделями. Крім того, ви можете передати перетворення стану у вигляді замикання, якщо зміна стану потребує доступу до батьківської моделі:

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
    )
    ->create();
```

<a name="has-many-relationships-using-magic-methods"></a>
#### Використання магічних методів

Для зручності ви можете будувати зв'язки магічними методами фабрик Laravel. Наприклад, у наведеному нижче прикладі за конвенцією буде визначено, що пов'язані моделі слід створити через метод зв'язку `posts` моделі `User`:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

Створюючи зв'язки фабрик магічними методами, ви можете передати масив атрибутів, які слід перевизначити в пов'язаних моделях:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

Ви можете також передати кілька масивів атрибутів, щоб створити пов'язані моделі з різним станом для кожної. Laravel застосує кожен масив по черзі:

```php
$user = User::factory()
    ->hasPosts(
        ['title' => 'First Post'],
        ['title' => 'Second Post'],
        ['title' => 'Third Post'],
    )
    ->create();
```

Ви можете передати перетворення стану у вигляді замикання, якщо зміна стану потребує доступу до батьківської моделі:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Зв'язки «належить до»

Тепер, коли ми розібралися, як будувати зв'язки «має багато» через фабрики, розгляньмо обернений зв'язок. Методом `for` можна вказати батьківську модель, якій належать створені фабрикою моделі. Наприклад, ми можемо створити три екземпляри моделі `App\Models\Post`, що належать одному користувачеві:

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

Якщо у вас уже є екземпляр батьківської моделі, з яким слід пов'язати створювані моделі, передайте його методу `for`:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### Використання магічних методів

Для зручності ви можете описувати зв'язки «належить до» магічними методами фабрик Laravel. Наприклад, у наведеному нижче прикладі за конвенцією буде визначено, що три пости мають належати зв'язку `user` моделі `Post`:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Зв'язки «багато до багатьох»

Як і [зв'язки «має багато»](#has-many-relationships), зв'язки «багато до багатьох» можна створювати методом `has`:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Атрибути проміжної таблиці

Якщо вам потрібно задати атрибути проміжної (pivot) таблиці, що зв'язує моделі, скористайтеся методом `hasAttached`. Другим аргументом він приймає масив назв і значень атрибутів проміжної таблиці:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

Ви можете передати перетворення стану у вигляді замикання, якщо зміна стану потребує доступу до пов'язаної моделі:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```

Ви можете також передати масив масивів проміжних даних, щоб задати унікальні дані для кожної пов'язаної моделі:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory(),
        [
            ['active' => true],
            ['active' => false],
        ]
    )
    ->create();
```

Якщо у вас уже є екземпляри моделей, які ви хочете приєднати до створюваних, передайте їх методу `hasAttached`. У цьому прикладі ті самі три ролі буде приєднано до всіх трьох користувачів:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### Використання магічних методів

Для зручності ви можете описувати зв'язки «багато до багатьох» магічними методами фабрик Laravel. Наприклад, у наведеному нижче прикладі за конвенцією буде визначено, що пов'язані моделі слід створити через метод зв'язку `roles` моделі `User`:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### Поліморфні зв'язки

[Поліморфні зв'язки](/docs/{{version}}/eloquent-relationships#polymorphic-relationships) теж можна створювати через фабрики. Поліморфні зв'язки «morph many» створюються так само, як звичайні зв'язки «має багато». Наприклад, якщо модель `App\Models\Post` має зв'язок `morphMany` з моделлю `App\Models\Comment`:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Зв'язки Morph To

Магічними методами не можна створювати зв'язки `morphTo`. Натомість слід напряму скористатися методом `for` і явно вказати назву зв'язку. Наприклад, уявіть, що модель `Comment` має метод `commentable`, який описує зв'язок `morphTo`. У такому разі ми можемо створити три коментарі, що належать одному посту, скориставшись методом `for` напряму:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### Поліморфні зв'язки «багато до багатьох»

Поліморфні зв'язки «багато до багатьох» (`morphToMany` / `morphedByMany`) створюються так само, як неполіморфні зв'язки «багато до багатьох»:

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

Звісно, магічний метод `has` теж можна використовувати для створення поліморфних зв'язків «багато до багатьох»:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### Опис зв'язків усередині фабрик

Щоб описати зв'язок усередині фабрики моделі, ви зазвичай присвоюєте новий екземпляр фабрики зовнішньому ключу цього зв'язку. Так роблять для «обернених» зв'язків - як-от `belongsTo` та `morphTo`. Наприклад, якщо ви хочете створювати нового користувача разом зі створенням поста, зробіть так:

```php
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

Якщо стовпці зв'язку залежать від фабрики, що його описує, ви можете присвоїти атрибуту замикання. Замикання отримає масив обчислених атрибутів фабрики:

```php
/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
### Повторне використання наявної моделі у зв'язках

Якщо у вас є моделі, що мають спільний зв'язок з іншою моделлю, скористайтеся методом `recycle`, щоб для всіх зв'язків, створених фабрикою, використовувався один екземпляр пов'язаної моделі.

Наприклад, уявіть, що ви маєте моделі `Airline`, `Flight` і `Ticket`, де квиток належить авіакомпанії та рейсу, а рейс теж належить авіакомпанії. Створюючи квитки, ви, найімовірніше, захочете, щоб і квиток, і рейс мали ту саму авіакомпанію, - тож передайте екземпляр авіакомпанії методу `recycle`:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

Метод `recycle` стане особливо в пригоді, якщо ваші моделі належать спільному користувачеві чи команді.

Метод `recycle` приймає також колекцію наявних моделей. Коли ви передаєте методу `recycle` колекцію, фабрика обиратиме з неї випадкову модель щоразу, коли їй знадобиться модель цього типу:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
