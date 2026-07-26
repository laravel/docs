---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: серіалізація

- [Вступ](#introduction)
- [Серіалізація моделей і колекцій](#serializing-models-and-collections)
    - [Серіалізація в масиви](#serializing-to-arrays)
    - [Серіалізація в JSON](#serializing-to-json)
- [Приховування атрибутів у JSON](#hiding-attributes-from-json)
- [Додавання значень до JSON](#appending-values-to-json)
- [Серіалізація дат](#date-serialization)

<a name="introduction"></a>
## Вступ

Створюючи API на Laravel, ви часто перетворюватимете свої моделі та зв'язки на масиви чи JSON. Eloquent має для цього зручні методи, а також дозволяє керувати тим, які атрибути потрапляють до серіалізованого представлення ваших моделей.

> [!NOTE]
> Про ще потужніший спосіб серіалізувати моделі та колекції Eloquent у JSON читайте в документації з [ресурсів API Eloquent](/docs/{{version}}/eloquent-resources).

<a name="serializing-models-and-collections"></a>
## Серіалізація моделей і колекцій

<a name="serializing-to-arrays"></a>
### Серіалізація в масиви

Щоб перетворити модель і завантажені [зв'язки](/docs/{{version}}/eloquent-relationships) на масив, скористайтеся методом `toArray`. Метод рекурсивний, тож усі атрибути й усі зв'язки (включно зі зв'язками зв'язків) буде перетворено на масиви:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

Метод `attributesToArray` перетворює на масив атрибути моделі, але не її зв'язки:

```php
$user = User::first();

return $user->attributesToArray();
```

Ви можете також перетворити на масиви цілі [колекції](/docs/{{version}}/eloquent-collections) моделей, викликавши метод `toArray` на екземплярі колекції:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### Серіалізація в JSON

Щоб перетворити модель на JSON, скористайтеся методом `toJson`. Як і `toArray`, метод `toJson` рекурсивний, тож усі атрибути й зв'язки буде перетворено на JSON. Ви можете також задати будь-які опції кодування JSON, [що їх підтримує PHP](https://secure.php.net/manual/en/function.json-encode.php):

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

Або ж ви можете привести модель чи колекцію до рядка - тоді метод `toJson` буде викликано автоматично:

```php
return (string) User::find(1);
```

Оскільки при приведенні до рядка моделі й колекції перетворюються на JSON, ви можете повертати об'єкти Eloquent прямо з маршрутів чи контролерів вашого застосунку. Laravel автоматично серіалізує ваші моделі та колекції Eloquent у JSON, коли їх повертають із маршруту чи контролера:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### Зв'язки

Коли модель Eloquent перетворюється на JSON, її завантажені зв'язки автоматично потрапляють до JSON-об'єкта як атрибути. Крім того, хоча методи зв'язків в Eloquent описують у «camel case», атрибут зв'язку в JSON буде в «snake case».

<a name="hiding-attributes-from-json"></a>
## Приховування атрибутів у JSON

Іноді вам потрібно обмежити атрибути - наприклад, паролі, - які потрапляють до масиву чи JSON-представлення моделі. Для цього скористайтеся на моделі атрибутом `Hidden`. Атрибути, перелічені в `Hidden`, не потраплять до серіалізованого представлення вашої моделі:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> [!NOTE]
> Щоб приховати зв'язки, додайте назву методу зв'язку до атрибута `Hidden` вашої моделі Eloquent.

Або ж ви можете скористатися атрибутом `Visible`, щоб описати «білий список» атрибутів, які мають потрапляти до масиву та JSON-представлення моделі. Усі атрибути, яких немає в `Visible`, буде приховано при перетворенні моделі на масив чи JSON:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### Тимчасова зміна видимості атрибутів

Якщо ви хочете зробити видимими на конкретному екземплярі моделі кілька зазвичай прихованих атрибутів, скористайтеся методами `makeVisible` чи `mergeVisible`. Метод `makeVisible` повертає екземпляр моделі:

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

Так само, якщо ви хочете приховати кілька зазвичай видимих атрибутів, скористайтеся методами `makeHidden` чи `mergeHidden`:

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

Якщо ви хочете тимчасово перевизначити всі видимі чи приховані атрибути, скористайтеся методами `setVisible` та `setHidden` відповідно:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## Додавання значень до JSON

Іноді, перетворюючи моделі на масиви чи JSON, ви хочете додати атрибути, яким не відповідає жоден стовпець у вашій базі даних. Для цього спершу опишіть для значення [аксесор](/docs/{{version}}/eloquent-mutators):

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

Якщо ви хочете, щоб аксесор завжди додавався до масиву та JSON-представлення моделі, скористайтеся на моделі атрибутом `Appends`. Зверніть увагу: на назви атрибутів зазвичай посилаються в їхньому серіалізованому вигляді «snake case», хоча PHP-метод аксесора описано в «camel case»:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

Коли атрибут додано до списку `appends`, він потраплятиме і до масиву, і до JSON-представлення моделі. Атрибути з масиву `appends` також враховують налаштування `visible` та `hidden` вашої моделі.

<a name="appending-at-run-time"></a>
#### Додавання під час виконання

Під час виконання ви можете наказати екземпляру моделі додати додаткові атрибути методами `append` чи `mergeAppends`. Або ж методом `setAppends` можна перевизначити цілий масив доданих властивостей для конкретного екземпляра моделі:

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

Так само, якщо ви хочете прибрати з моделі всі додані властивості, скористайтеся методом `withoutAppends`:

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## Серіалізація дат

<a name="customizing-the-default-date-format"></a>
#### Зміна формату дати за замовчуванням

Ви можете змінити формат серіалізації за замовчуванням, перевизначивши метод `serializeDate`. Цей метод не впливає на те, як ваші дати форматуються для зберігання в базі даних:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### Зміна формату дати для окремого атрибута

Ви можете змінити формат серіалізації окремих атрибутів дати в Eloquent, задавши формат дати в [оголошеннях приведення типів](/docs/{{version}}/eloquent-mutators#attribute-casting) моделі:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
