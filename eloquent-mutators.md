---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: мутатори та приведення типів

- [Вступ](#introduction)
- [Аксесори та мутатори](#accessors-and-mutators)
    - [Опис аксесора](#defining-an-accessor)
    - [Опис мутатора](#defining-a-mutator)
- [Приведення типів атрибутів](#attribute-casting)
    - [Приведення до масиву та JSON](#array-and-json-casting)
    - [Бінарне приведення](#binary-casting)
    - [Приведення дат](#date-casting)
    - [Приведення до enum](#enum-casting)
    - [Шифроване приведення](#encrypted-casting)
    - [Приведення під час запиту](#query-time-casting)
- [Власні приведення](#custom-casts)
    - [Приведення до об'єктів-значень](#value-object-casting)
    - [Серіалізація в масив / JSON](#array-json-serialization)
    - [Вхідне приведення](#inbound-casting)
    - [Параметри приведення](#cast-parameters)
    - [Порівняння приведених значень](#comparing-cast-values)
    - [Castable-об'єкти](#castables)

<a name="introduction"></a>
## Вступ

Аксесори, мутатори та приведення типів атрибутів дозволяють перетворювати значення атрибутів Eloquent, коли ви їх читаєте чи задаєте на екземплярах моделей. Наприклад, ви можете скористатися [шифрувальником Laravel](/docs/{{version}}/encryption), щоб зашифрувати значення для зберігання в базі даних, а потім автоматично розшифровувати цей атрибут при зверненні до нього на моделі Eloquent. Або ж ви можете перетворювати рядок JSON, що зберігається в базі, на масив при зверненні через модель Eloquent.

<a name="accessors-and-mutators"></a>
## Аксесори та мутатори

<a name="defining-an-accessor"></a>
### Опис аксесора

Аксесор перетворює значення атрибута Eloquent при зверненні до нього. Щоб описати аксесор, створіть у моделі метод `protected`, який представлятиме доступний атрибут. Назва методу має відповідати запису справжнього атрибута моделі чи стовпця бази даних у «camel case» - там, де це доречно.

У цьому прикладі ми опишемо аксесор для атрибута `first_name`. Eloquent автоматично викличе його при спробі отримати значення атрибута `first_name`. Усі методи аксесорів і мутаторів атрибутів мають оголошувати тип, що повертається, - `Illuminate\Database\Eloquent\Casts\Attribute`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

Усі методи аксесорів повертають екземпляр `Attribute`, який описує, як до атрибута звертатимуться і, за бажанням, як його змінюватимуть. У цьому прикладі ми описуємо лише читання атрибута - для цього передаємо аргумент `get` конструктору класу `Attribute`.

Як бачите, початкове значення стовпця передається в аксесор, тож ви можете його змінити й повернути. Щоб отримати значення аксесора, просто зверніться до атрибута `first_name` на екземплярі моделі:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> Якщо ви хочете, щоб ці обчислені значення потрапляли до масиву чи JSON-представлення моделі, [їх потрібно додати](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### Побудова об'єктів-значень із кількох атрибутів

Іноді вашому аксесору потрібно перетворити кілька атрибутів моделі на один «об'єкт-значення». Для цього ваше замикання `get` може приймати другий аргумент - `$attributes`, який буде передано автоматично й який міститиме масив усіх поточних атрибутів моделі:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```

<a name="accessor-caching"></a>
#### Кешування аксесорів

Коли аксесори повертають об'єкти-значення, будь-які зміни такого об'єкта автоматично синхронізуються назад у модель перед її збереженням. Це можливо тому, що Eloquent зберігає екземпляри, повернуті аксесорами, і повертає той самий екземпляр при кожному виклику аксесора:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

Втім, іноді вам може знадобитися кешування й для простих значень - рядків чи булевих, - особливо якщо їх дорого обчислювати. Для цього викличте метод `shouldCache` при описі аксесора:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

Якщо ви хочете вимкнути кешування об'єктів для атрибута, викличте при його описі метод `withoutObjectCaching`:

```php
/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
### Опис мутатора

Мутатор перетворює значення атрибута Eloquent при його задаванні. Щоб описати мутатор, передайте при описі атрибута аргумент `set`. Опишімо мутатор для атрибута `first_name`. Його буде автоматично викликано, коли ми спробуємо задати значення атрибута `first_name` на моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Interact with the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }
}
```

Замикання мутатора отримає значення, яке задають атрибуту, тож ви можете змінити його й повернути змінене. Щоб скористатися нашим мутатором, достатньо задати атрибут `first_name` на моделі Eloquent:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

У цьому прикладі колбек `set` буде викликано зі значенням `Sally`. Далі мутатор застосує до імені функцію `strtolower` і покладе результат у внутрішній масив `$attributes` моделі.

<a name="mutating-multiple-attributes"></a>
#### Зміна кількох атрибутів

Іноді вашому мутатору потрібно задати кілька атрибутів моделі. Для цього поверніть із замикання `set` масив. Кожен ключ масиву має відповідати атрибуту моделі чи стовпцю бази даних:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="attribute-casting"></a>
## Приведення типів атрибутів

Приведення типів атрибутів дає функціональність, схожу на аксесори та мутатори, але не вимагає описувати в моделі додаткові методи. Натомість метод `casts` вашої моделі дає зручний спосіб перетворювати атрибути на поширені типи даних.

Метод `casts` має повертати масив, де ключ - назва атрибута, який приводимо, а значення - тип, до якого ви хочете привести стовпець. Підтримувані типи приведення:

<div class="content-list" markdown="1">

- `array`
- `AsFluent::class`
- `AsStringable::class`
- `AsUri::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `hashed`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

Щоб показати приведення типів у дії, приведімо атрибут `is_admin`, який зберігається в базі як ціле число (`0` або `1`), до булевого значення:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'is_admin' => 'boolean',
        ];
    }
}
```

Після опису приведення атрибут `is_admin` завжди буде приведено до булевого при зверненні до нього - навіть якщо в базі значення зберігається як ціле число:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

Якщо вам потрібно додати нове тимчасове приведення під час виконання, скористайтеся методом `mergeCasts`. Ці описи буде додано до тих, які вже описані в моделі:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> Атрибути зі значенням `null` не приводяться. Крім того, ніколи не описуйте приведення (чи атрибут) з тією самою назвою, що й зв'язок, і не призначайте приведення первинному ключу моделі.

<a name="stringable-casting"></a>
#### Приведення до Stringable

Класом приведення `Illuminate\Database\Eloquent\Casts\AsStringable` можна привести атрибут моделі до [плавного об'єкта Illuminate\Support\Stringable](/docs/{{version}}/strings#fluent-strings-method-list):

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'directory' => AsStringable::class,
        ];
    }
}
```

<a name="array-and-json-casting"></a>
### Приведення до масиву та JSON

Приведення `array` особливо корисне при роботі зі стовпцями, у яких зберігається серіалізований JSON. Наприклад, якщо ваша база має поле типу `JSON` чи `TEXT` із серіалізованим JSON, приведення `array` для цього атрибута автоматично десеріалізує його в PHP-масив при зверненні через модель Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => 'array',
        ];
    }
}
```

Коли приведення описано, ви можете звернутися до атрибута `options`, і його буде автоматично десеріалізовано з JSON у PHP-масив. Коли ви задаєте значення атрибута `options`, переданий масив автоматично серіалізується назад у JSON для зберігання:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

Щоб оновити одне поле атрибута JSON лаконічнішим синтаксисом, ви можете [зробити атрибут доступним для масового призначення](/docs/{{version}}/eloquent#mass-assignment-json-columns) і скористатися оператором `->` при виклику методу `update`:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON та Unicode

Якщо ви хочете зберігати атрибут-масив як JSON з неекранованими символами Unicode, скористайтеся приведенням `json:unicode`:

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => 'json:unicode',
    ];
}
```

<a name="array-object-and-collection-casting"></a>
#### Приведення до ArrayObject та колекції

Хоча стандартного приведення `array` вистачає для багатьох застосунків, воно має свої недоліки. Оскільки приведення `array` повертає примітивний тип, змінити елемент масиву напряму неможливо. Наприклад, такий код спричинить помилку PHP:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

Щоб це розв'язати, Laravel має приведення `AsArrayObject`, яке приводить ваш атрибут JSON до класу [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php). Цю можливість реалізовано через [власні приведення](#custom-casts) Laravel, що дозволяє йому розумно кешувати й перетворювати змінений об'єкт, тож окремі елементи можна змінювати без помилки PHP. Щоб скористатися приведенням `AsArrayObject`, просто призначте його атрибуту:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsArrayObject::class,
    ];
}
```

Так само Laravel має приведення `AsCollection`, яке приводить ваш атрибут JSON до екземпляра [колекції](/docs/{{version}}/collections) Laravel:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::class,
    ];
}
```

Якщо ви хочете, щоб приведення `AsCollection` створювало екземпляр власного класу колекції замість базового класу Laravel, передайте назву класу колекції як аргумент приведення:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
    ];
}
```

Методом `of` можна вказати, що елементи колекції слід перетворити на заданий клас через [метод mapInto](/docs/{{version}}/collections#method-mapinto) колекції:

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::of(Option::class)
    ];
}
```

Перетворюючи колекції на об'єкти, ці об'єкти мають реалізувати інтерфейси `Illuminate\Contracts\Support\Arrayable` та `JsonSerializable`, щоб описати, як їхні екземпляри серіалізуються в базу даних як JSON:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Support\Arrayable;
use JsonSerializable;

class Option implements Arrayable, JsonSerializable
{
    public string $name;
    public mixed $value;
    public bool $isLocked;

    /**
     * Create a new Option instance.
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * Get the instance as an array.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'value' => $this->value,
            'is_locked' => $this->isLocked,
        ];
    }

    /**
     * Specify the data which should be serialized to JSON.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```

<a name="binary-casting"></a>
### Бінарне приведення

Якщо ваша модель Eloquent має стовпець `uuid` чи `ulid` [бінарного типу](/docs/{{version}}/migrations#column-method-binary) на додачу до автоінкрементного стовпця ID, скористайтеся приведенням `AsBinary`, щоб автоматично перетворювати значення в бінарне представлення й назад:

```php
use Illuminate\Database\Eloquent\Casts\AsBinary;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'uuid' => AsBinary::uuid(),
        'ulid' => AsBinary::ulid(),
    ];
}
```

Коли приведення описано в моделі, ви можете задати значення атрибута UUID / ULID як екземпляр об'єкта або рядок. Eloquent автоматично приведе значення до бінарного представлення. Читаючи значення атрибута, ви завжди отримаєте звичайний текстовий рядок:

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### Приведення дат

За замовчуванням Eloquent приводить стовпці `created_at` та `updated_at` до екземплярів [Carbon](https://github.com/briannesbitt/Carbon), що розширює PHP-клас `DateTime` і має цілу низку зручних методів. Ви можете привести й інші атрибути дат, описавши додаткові приведення в методі `casts` вашої моделі. Зазвичай дати приводять типами `datetime` або `immutable_datetime`.

Описуючи приведення `date` чи `datetime`, ви можете також задати формат дати. Його буде використано, коли [модель серіалізується в масив чи JSON](/docs/{{version}}/eloquent-serialization):

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'created_at' => 'datetime:Y-m-d',
    ];
}
```

Коли стовпець приведено як дату, ви можете задати відповідному атрибуту моделі значення у вигляді UNIX-часу, рядка дати (`Y-m-d`), рядка дати з часом або екземпляра `DateTime` / `Carbon`. Значення дати буде правильно перетворено й збережено у вашій базі даних.

Ви можете змінити формат серіалізації за замовчуванням для всіх дат моделі, описавши в ній метод `serializeDate`. Цей метод не впливає на те, як ваші дати форматуються для зберігання в базі даних:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

Щоб задати формат, у якому дати моделі справді зберігаються в базі даних, скористайтеся аргументом `dateFormat` атрибута `Table` вашої моделі:

```php
use Illuminate\Database\Eloquent\Attributes\Table;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

<a name="date-casting-and-timezones"></a>
#### Приведення дат, серіалізація та часові зони

За замовчуванням приведення `date` і `datetime` серіалізують дати в рядок UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`) незалежно від часової зони, заданої в опції конфігурації `timezone` вашого застосунку. Наполегливо радимо завжди користуватися саме цим форматом серіалізації, а також зберігати дати застосунку в часовій зоні UTC, не змінюючи опцію `timezone` з її значення за замовчуванням `UTC`. Послідовне використання UTC в усьому застосунку дасть максимальну сумісність з іншими бібліотеками роботи з датами на PHP та JavaScript.

Якщо до приведення `date` чи `datetime` застосовано власний формат - наприклад, `datetime:Y-m-d H:i:s`, - при серіалізації дати буде використано внутрішню часову зону екземпляра Carbon. Зазвичай це часова зона, задана в опції конфігурації `timezone` вашого застосунку. Проте важливо зауважити: стовпці `timestamp` на кшталт `created_at` та `updated_at` є винятком із цієї поведінки й завжди форматуються в UTC, незалежно від налаштування часової зони застосунку.

<a name="enum-casting"></a>
### Приведення до enum

Eloquent дозволяє також приводити значення атрибутів до PHP-[enum](https://www.php.net/manual/en/language.enumerations.backed.php). Для цього вкажіть атрибут і enum, до якого хочете привести, у методі `casts` вашої моделі:

```php
use App\Enums\ServerStatus;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'status' => ServerStatus::class,
    ];
}
```

Коли ви описали приведення в моделі, указаний атрибут автоматично приводитиметься до enum і назад при роботі з ним:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Приведення масивів enum

Іноді вашій моделі потрібно зберігати масив значень enum в одному стовпці. Для цього скористайтеся приведеннями `AsEnumArrayObject` чи `AsEnumCollection`, які дає Laravel:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'statuses' => AsEnumCollection::of(ServerStatus::class),
    ];
}
```

<a name="encrypted-casting"></a>
### Шифроване приведення

Приведення `encrypted` шифрує значення атрибута моделі вбудованими засобами [шифрування](/docs/{{version}}/encryption) Laravel. Крім того, приведення `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject` та `AsEncryptedCollection` працюють як їхні нешифровані відповідники; проте, як і слід очікувати, значення шифрується при зберіганні в базі даних.

Оскільки кінцева довжина зашифрованого тексту непередбачувана й більша за відкритий текст, переконайтеся, що відповідний стовпець бази даних має тип `TEXT` або більший. Крім того, оскільки значення в базі зашифровані, ви не зможете робити запити чи шукати за зашифрованими атрибутами.

<a name="key-rotation"></a>
#### Ротація ключа

Як ви, можливо, знаєте, Laravel шифрує рядки за допомогою значення конфігурації `key`, заданого у файлі конфігурації `app` вашого застосунку. Зазвичай це значення відповідає змінній оточення `APP_KEY`. Якщо вам потрібно змінити ключ шифрування застосунку, ви можете [зробити це коректно](/docs/{{version}}/encryption#gracefully-rotating-encryption-keys).

<a name="query-time-casting"></a>
### Приведення під час запиту

Іноді вам потрібно застосувати приведення під час виконання запиту - наприклад, коли ви вибираєте сире значення з таблиці. Розгляньмо такий запит:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

Атрибут `last_posted_at` у результатах цього запиту буде звичайним рядком. Було б чудово застосувати до нього приведення `datetime` прямо під час виконання запиту. На щастя, це можна зробити методом `withCasts`:

```php
$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->withCasts([
    'last_posted_at' => 'datetime'
])->get();
```

<a name="custom-casts"></a>
## Власні приведення

Laravel має цілу низку вбудованих корисних типів приведення; проте іноді вам потрібно описати власні. Щоб створити приведення, виконайте artisan-команду `make:cast`. Новий клас приведення потрапить до каталогу `app/Casts`:

```shell
php artisan make:cast AsJson
```

Усі класи власних приведень реалізують інтерфейс `CastsAttributes`. Класи, що його реалізують, мають описати методи `get` і `set`. Метод `get` відповідає за перетворення сирого значення з бази даних на приведене значення, а метод `set` має перетворити приведене значення на сире, яке можна зберегти в базі. Для прикладу ми заново реалізуємо вбудований тип приведення `json` як власний:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return json_encode($value);
    }
}
```

Коли ви описали власний тип приведення, його можна прикріпити до атрибута моделі за назвою класу:

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsJson::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
### Приведення до об'єктів-значень

Ви не обмежені приведенням до примітивних типів - значення можна приводити й до об'єктів. Опис власних приведень до об'єктів дуже схожий на приведення до примітивів; проте, якщо ваш об'єкт-значення охоплює більш ніж один стовпець бази даних, метод `set` має повернути масив пар «ключ - значення», якими буде задано сирі значення для зберігання в моделі. Якщо ваш об'єкт-значення стосується лише одного стовпця, просто поверніть значення для зберігання.

Для прикладу опишімо клас власного приведення, що приводить кілька значень моделі до одного об'єкта-значення `Address`. Припустімо, що об'єкт-значення `Address` має дві публічні властивості: `lineOne` і `lineTwo`:

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class AsAddress implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): Address {
        return new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, string>
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        if (! $value instanceof Address) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

При приведенні до об'єктів-значень будь-які зміни такого об'єкта автоматично синхронізуються назад у модель перед її збереженням:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> Якщо ви плануєте серіалізувати в JSON чи масиви моделі Eloquent, що містять об'єкти-значення, реалізуйте на об'єкті-значенні інтерфейси `Illuminate\Contracts\Support\Arrayable` та `JsonSerializable`.

<a name="value-object-caching"></a>
#### Кешування об'єктів-значень

Коли атрибути, приведені до об'єктів-значень, обчислюються, Eloquent їх кешує. Тому при повторному зверненні до атрибута буде повернуто той самий екземпляр об'єкта.

Якщо ви хочете вимкнути кешування об'єктів у класах власних приведень, оголосіть у своєму класі приведення публічну властивість `withoutObjectCaching`:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### Серіалізація в масив / JSON

Коли модель Eloquent перетворюється на масив чи JSON методами `toArray` і `toJson`, ваші об'єкти-значення з власних приведень зазвичай теж серіалізуються - якщо вони реалізують інтерфейси `Illuminate\Contracts\Support\Arrayable` та `JsonSerializable`. Проте, коли ви користуєтеся об'єктами-значеннями зі сторонніх бібліотек, у вас може не бути змоги додати до них ці інтерфейси.

Тому ви можете вказати, що за серіалізацію об'єкта-значення відповідатиме ваш клас приведення. Для цього він має реалізувати інтерфейс `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes`. Цей інтерфейс вимагає, щоб ваш клас містив метод `serialize`, який повертає серіалізовану форму вашого об'єкта-значення:

```php
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(
    Model $model,
    string $key,
    mixed $value,
    array $attributes,
): string {
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### Вхідне приведення

Іноді вам потрібен клас власного приведення, що перетворює лише значення, які задають моделі, і нічого не робить, коли атрибути з моделі читають.

Приведення лише для вхідних значень мають реалізувати інтерфейс `CastsInboundAttributes`, який вимагає описати тільки метод `set`. Artisan-команду `make:cast` можна викликати з опцією `--inbound`, щоб згенерувати такий клас:

```shell
php artisan make:cast AsHash --inbound
```

Класичний приклад приведення лише для вхідних значень - приведення з хешуванням. Наприклад, ми можемо описати приведення, що хешує вхідні значення заданим алгоритмом:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * Create a new cast class instance.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return is_null($this->algorithm)
            ? bcrypt($value)
            : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
### Параметри приведення

Прикріплюючи власне приведення до моделі, ви можете задати параметри приведення, відділивши їх від назви класу символом `:`, а кілька параметрів - комами. Параметри буде передано в конструктор класу приведення:

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => AsHash::class.':sha256',
    ];
}
```

<a name="comparing-cast-values"></a>
### Порівняння приведених значень

Якщо ви хочете описати, як порівнювати два приведені значення, щоб визначити, чи вони змінилися, ваш клас власного приведення може реалізувати інтерфейс `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes`. Це дає тонкий контроль над тим, які значення Eloquent вважає зміненими й, відповідно, зберігає в базу при оновленні моделі.

Цей інтерфейс вимагає, щоб ваш клас містив метод `compare`, який повертає `true`, якщо задані значення вважаються рівними:

```php
/**
 * Determine if the given values are equal.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $firstValue
 * @param  mixed  $secondValue
 * @return bool
 */
public function compare(
    Model $model,
    string $key,
    mixed $firstValue,
    mixed $secondValue
): bool {
    return $firstValue === $secondValue;
}
```

<a name="castables"></a>
### Castable-об'єкти

Ви можете захотіти, щоб об'єкти-значення вашого застосунку самі описували свої класи приведення. Замість того щоб прикріплювати клас приведення до моделі, ви можете прикріпити клас об'єкта-значення, що реалізує інтерфейс `Illuminate\Contracts\Database\Eloquent\Castable`:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

Об'єкти, що реалізують інтерфейс `Castable`, мають описати метод `castUsing`, який повертає назву класу приведення, відповідального за перетворення до класу `Castable` і назад:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

Користуючись класами `Castable`, ви все одно можете передавати аргументи в описі методу `casts`. Їх буде передано в метод `castUsing`:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class.':argument',
    ];
}
```

<a name="anonymous-cast-classes"></a>
#### Castable-об'єкти та анонімні класи приведення

Поєднавши «castable»-об'єкти з [анонімними класами](https://www.php.net/manual/en/language.oop5.anonymous.php) PHP, ви можете описати об'єкт-значення та логіку його приведення як один castable-об'єкт. Для цього поверніть із методу `castUsing` вашого об'єкта-значення анонімний клас. Він має реалізувати інтерфейс `CastsAttributes`:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * Get the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): CastsAttributes
    {
        return new class implements CastsAttributes
        {
            public function get(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): Address {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): array {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```
