---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# База даних: конструктор запитів

- [Вступ](#introduction)
- [Виконання запитів до бази даних](#running-database-queries)
    - [Обробка результатів частинами](#chunking-results)
    - [Ліниве потокове читання результатів](#streaming-results-lazily)
    - [Агрегати](#aggregates)
- [Запити SELECT](#select-statements)
- [Сирі вирази](#raw-expressions)
- [Джойни](#joins)
- [Об'єднання запитів](#unions)
- [Базові умови WHERE](#basic-where-clauses)
    - [Умови WHERE](#where-clauses)
    - [Умови OR WHERE](#or-where-clauses)
    - [Умови WHERE NOT](#where-not-clauses)
    - [Умови Any / All / None](#where-any-all-none-clauses)
    - [Умови WHERE для JSON](#json-where-clauses)
    - [Додаткові умови WHERE](#additional-where-clauses)
    - [Логічне групування](#logical-grouping)
- [Складніші умови WHERE](#advanced-where-clauses)
    - [Умови WHERE EXISTS](#where-exists-clauses)
    - [Умови WHERE з підзапитом](#subquery-where-clauses)
    - [Умови повнотекстового пошуку](#full-text-where-clauses)
    - [Умови векторної схожості](#vector-similarity-clauses)
- [Сортування, групування, limit та offset](#ordering-grouping-limit-and-offset)
    - [Сортування](#ordering)
    - [Групування](#grouping)
    - [Limit та offset](#limit-and-offset)
- [Умовні вирази](#conditional-clauses)
- [Запити INSERT](#insert-statements)
    - [Upsert](#upserts)
- [Запити UPDATE](#update-statements)
    - [Оновлення стовпців JSON](#updating-json-columns)
    - [Збільшення та зменшення](#increment-and-decrement)
- [Запити DELETE](#delete-statements)
- [Песимістичне блокування](#pessimistic-locking)
- [Повторно використовувані компоненти запитів](#reusable-query-components)
- [Налагодження](#debugging)

<a name="introduction"></a>
## Вступ

Конструктор запитів Laravel дає зручний, плавний інтерфейс для створення й виконання запитів до бази даних. Ним можна виконати більшість операцій з базою у вашому застосунку, і він бездоганно працює з усіма підтримуваними Laravel системами баз даних.

Конструктор запитів Laravel використовує прив'язку параметрів PDO, щоб захистити ваш застосунок від атак SQL-ін'єкцією. Немає потреби чистити чи екранувати рядки, які ви передаєте конструктору як прив'язки.

> [!WARNING]
> PDO не підтримує прив'язку назв стовпців. Тому ніколи не дозволяйте користувацькому вводу визначати назви стовпців у ваших запитах, зокрема стовпці для «order by».

<a name="running-database-queries"></a>
## Виконання запитів до бази даних

<a name="retrieving-all-rows-from-a-table"></a>
#### Отримання всіх рядків таблиці

Щоб почати запит, скористайтеся методом `table` фасаду `DB`. Метод `table` повертає плавний екземпляр конструктора запитів для вказаної таблиці, тож ви можете додавати до запиту обмеження ланцюжком, а вкінці отримати результати методом `get`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

Метод `get` повертає екземпляр `Illuminate\Support\Collection` з результатами запиту, де кожен результат - це екземпляр PHP-об'єкта `stdClass`. Значення кожного стовпця доступне як властивість об'єкта:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Колекції Laravel мають цілу низку надзвичайно потужних методів для перетворення та згортання даних. Детальніше про них читайте в [документації з колекцій](/docs/{{version}}/collections).

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### Отримання одного рядка чи стовпця з таблиці

Якщо вам потрібен лише один рядок із таблиці, скористайтеся методом `first` фасаду `DB`. Він повертає один об'єкт `stdClass`:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

Якщо ви хочете отримати один рядок, але викинути `Illuminate\Database\RecordNotFoundException`, коли відповідного рядка немає, скористайтеся методом `firstOrFail`. Якщо `RecordNotFoundException` не перехоплено, клієнту автоматично надсилається HTTP-відповідь 404:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

Якщо вам не потрібен цілий рядок, ви можете дістати одне значення із запису методом `value`. Він повертає значення стовпця напряму:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

Щоб отримати один рядок за значенням стовпця `id`, скористайтеся методом `find`:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### Отримання списку значень стовпця

Якщо ви хочете отримати екземпляр `Illuminate\Support\Collection` зі значеннями одного стовпця, скористайтеся методом `pluck`. У цьому прикладі ми отримаємо колекцію посад користувачів:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

Другим аргументом методу `pluck` можна вказати стовпець, значення якого стануть ключами колекції:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### Обробка результатів частинами

Якщо вам потрібно опрацювати тисячі записів, розгляньте метод `chunk` фасаду `DB`. Він дістає з бази невелику частину результатів за раз і передає кожну частину в замикання для обробки. Наприклад, пройдімо всю таблицю `users` частинами по 100 записів:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

Щоб зупинити обробку наступних частин, поверніть із замикання `false`:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

Якщо під час обробки частинами ви оновлюєте записи, результати можуть змінитися неочікуваним чином. Коли ви плануєте оновлювати отримані записи, завжди краще скористатися методом `chunkById`. Він автоматично розбиває результати на сторінки за первинним ключем запису:

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

Оскільки методи `chunkById` і `lazyById` додають до запиту власні умови «where», свої умови варто [логічно згрупувати](#logical-grouping) в замиканні:

```php
DB::table('users')->where(function ($query) {
    $query->where('credits', 1)->orWhere('credits', 2);
})->chunkById(100, function (Collection $users) {
    foreach ($users as $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['credits' => 3]);
    }
});
```

> [!WARNING]
> Коли ви оновлюєте або видаляєте записи всередині колбека, будь-які зміни первинного чи зовнішніх ключів можуть вплинути на запит, що дістає частини. Через це частина записів може не потрапити до результатів.

<a name="streaming-results-lazily"></a>
### Ліниве потокове читання результатів

Метод `lazy` працює схоже на [метод chunk](#chunking-results) - він теж виконує запит частинами. Але замість того щоб передавати кожну частину в колбек, метод `lazy()` повертає [LazyCollection](/docs/{{version}}/collections#lazy-collections), і ви працюєте з результатами як з єдиним потоком:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

І знову ж таки: якщо ви плануєте оновлювати отримані записи під час обходу, краще скористатися методами `lazyById` або `lazyByIdDesc`. Вони автоматично розбивають результати на сторінки за первинним ключем запису:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> Коли ви оновлюєте або видаляєте записи під час обходу, будь-які зміни первинного чи зовнішніх ключів можуть вплинути на запит, що дістає частини. Через це частина записів може не потрапити до результатів.

<a name="aggregates"></a>
### Агрегати

Конструктор запитів має також низку методів для отримання агрегатних значень: `count`, `max`, `min`, `avg` і `sum`. Викликати будь-який із них можна після того, як ви побудували запит:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

Звісно, ці методи можна поєднувати з іншими умовами, щоб точніше визначити, як обчислюється агрегат:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### Перевірка існування записів

Замість методу `count` для перевірки, чи є записи, що відповідають обмеженням запиту, скористайтеся методами `exists` і `doesntExist`:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Запити SELECT

<a name="specifying-a-select-clause"></a>
#### Задання виразу SELECT

Не завжди потрібно вибирати з таблиці всі стовпці. Методом `select` ви можете задати для запиту власний вираз «select»:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

Метод `distinct` змушує запит повертати лише унікальні результати:

```php
$users = DB::table('users')->distinct()->get();
```

Якщо у вас уже є екземпляр конструктора запитів і ви хочете додати стовпець до наявного виразу select, скористайтеся методом `addSelect`:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Сирі вирази

Іноді вам потрібно вставити в запит довільний рядок. Щоб створити сирий рядковий вираз, скористайтеся методом `raw` фасаду `DB`:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Сирі вирази підставляються в запит як рядки, тому будьте надзвичайно уважні, щоб не створити вразливість до SQL-ін'єкції.

<a name="raw-methods"></a>
### Сирі методи

Замість методу `DB::raw` ви можете скористатися наведеними нижче методами, щоб вставити сирий вираз у різні частини запиту. **Пам'ятайте: Laravel не може гарантувати, що запит із сирими виразами захищений від SQL-ін'єкцій.**

<a name="selectraw"></a>
#### `selectRaw`

Метод `selectRaw` можна використати замість `addSelect(DB::raw(/* ... */))`. Другим аргументом він приймає необов'язковий масив прив'язок:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

Методи `whereRaw` і `orWhereRaw` вставляють у ваш запит сирий вираз «where». Другим аргументом вони приймають необов'язковий масив прив'язок:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

Методи `havingRaw` і `orHavingRaw` задають сирий рядок як значення виразу «having». Другим аргументом вони приймають необов'язковий масив прив'язок:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

Метод `orderByRaw` задає сирий рядок як значення виразу «order by»:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

Метод `groupByRaw` задає сирий рядок як значення виразу `group by`:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## Джойни

<a name="inner-join-clause"></a>
#### Вираз INNER JOIN

Конструктором запитів можна додавати до запитів і джойни. Щоб виконати базовий «inner join», скористайтеся методом `join` на екземплярі конструктора. Перший аргумент методу `join` - назва таблиці, яку потрібно приєднати, а решта аргументів задають умови для стовпців. Ви можете приєднати навіть кілька таблиць в одному запиті:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Вирази LEFT JOIN / RIGHT JOIN

Якщо замість «inner join» вам потрібен «left join» чи «right join», скористайтеся методами `leftJoin` або `rightJoin`. Вони мають ту саму сигнатуру, що й метод `join`:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Вираз CROSS JOIN

Щоб виконати «cross join», скористайтеся методом `crossJoin`. Cross join утворює декартовий добуток першої таблиці та приєднаної:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### Складніші вирази джойнів

Ви можете задавати й складніші умови джойну. Для цього передайте замикання другим аргументом методу `join`. Замикання отримає екземпляр `Illuminate\Database\Query\JoinClause`, у якому ви задаєте обмеження виразу «join»:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

Якщо в джойні вам потрібен вираз «where», скористайтеся методами `where` і `orWhere` екземпляра `JoinClause`. Замість порівняння двох стовпців вони порівнюють стовпець зі значенням:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### Джойни з підзапитом

Методами `joinSub`, `leftJoinSub` і `rightJoinSub` ви можете приєднати до запиту підзапит. Кожен із них приймає три аргументи: підзапит, його псевдонім таблиці та замикання, що визначає пов'язані стовпці. У цьому прикладі ми отримаємо колекцію користувачів, де кожен запис також містить час `created_at` останнього опублікованого поста цього користувача:

```php
$latestPosts = DB::table('posts')
    ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
    ->where('is_published', true)
    ->groupBy('user_id');

$users = DB::table('users')
    ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
        $join->on('users.id', '=', 'latest_posts.user_id');
    })->get();
```

<a name="lateral-joins"></a>
#### Латеральні джойни

> [!WARNING]
> Латеральні джойни наразі підтримують PostgreSQL, MySQL >= 8.0.14 і SQL Server.

Методами `joinLateral` і `leftJoinLateral` можна виконати «lateral join» із підзапитом. Кожен із них приймає два аргументи: підзапит і його псевдонім таблиці. Умови джойну слід задати у виразі `where` самого підзапиту. Латеральні джойни обчислюються для кожного рядка й можуть посилатися на стовпці за межами підзапиту.

У цьому прикладі ми отримаємо колекцію користувачів разом із трьома їхніми останніми постами. Кожен користувач може дати до трьох рядків у результаті - по одному на кожен останній пост. Умову джойну задано виразом `whereColumn` усередині підзапиту, який посилається на поточний рядок користувача:

```php
$latestPosts = DB::table('posts')
    ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
    ->whereColumn('user_id', 'users.id')
    ->orderBy('created_at', 'desc')
    ->limit(3);

$users = DB::table('users')
    ->joinLateral($latestPosts, 'latest_posts')
    ->get();
```

<a name="unions"></a>
## Об'єднання запитів

Конструктор запитів має також зручний метод для об'єднання («union») двох чи більше запитів. Наприклад, ви можете створити початковий запит і методом `union` об'єднати його з іншими:

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```

Крім методу `union`, конструктор запитів має метод `unionAll`. Запити, об'єднані через `unionAll`, не втрачають дублікати результатів. Сигнатура `unionAll` така сама, як у `union`.

<a name="basic-where-clauses"></a>
## Базові умови WHERE

<a name="where-clauses"></a>
### Умови WHERE

Щоб додати до запиту умови «where», скористайтеся методом `where` конструктора запитів. Найпростіший виклик `where` вимагає трьох аргументів. Перший - назва стовпця. Другий - оператор, будь-який із підтримуваних вашою базою даних. Третій - значення, з яким порівнюється значення стовпця.

Наприклад, цей запит дістає користувачів, у яких значення стовпця `votes` дорівнює `100`, а значення стовпця `age` більше за `35`:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

Для зручності, якщо ви перевіряєте стовпець на рівність `=` заданому значенню, передайте це значення другим аргументом методу `where`. Laravel вважатиме, що ви хочете оператор `=`:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

Ви також можете передати методу `where` асоціативний масив, щоб швидко зробити запит за кількома стовпцями:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

Як уже згадувалося, ви можете використовувати будь-який оператор, що його підтримує ваша система баз даних:

```php
$users = DB::table('users')
    ->where('votes', '>=', 100)
    ->get();

$users = DB::table('users')
    ->where('votes', '<>', 100)
    ->get();

$users = DB::table('users')
    ->where('name', 'like', 'T%')
    ->get();
```

Функції `where` можна також передати масив умов. Кожен елемент масиву має бути масивом із трьох аргументів, які зазвичай передають методу `where`:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO не підтримує прив'язку назв стовпців. Тому ніколи не дозволяйте користувацькому вводу визначати назви стовпців у ваших запитах, зокрема стовпці для «order by».

> [!WARNING]
> MySQL і MariaDB автоматично приводять рядки до цілих чисел, коли порівнюють рядок із числом. При цьому нечислові рядки перетворюються на `0`, що може дати неочікуваний результат. Наприклад, якщо у вашій таблиці є стовпець `secret` зі значенням `aaa` і ви виконаєте `User::where('secret', 0)`, цей рядок буде повернуто. Щоб такого не сталося, приводьте всі значення до належних типів, перш ніж використовувати їх у запитах.

<a name="or-where-clauses"></a>
### Умови OR WHERE

Коли ви ланцюжком викликаєте метод `where`, умови «where» з'єднуються оператором `and`. Втім, методом `orWhere` ви можете приєднати умову оператором `or`. Метод `orWhere` приймає ті самі аргументи, що й `where`:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

Якщо вам потрібно згрупувати умову «or» у дужках, передайте замикання першим аргументом методу `orWhere`:

```php
use Illuminate\Database\Query\Builder;

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```

Наведений вище приклад дасть такий SQL:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> Завжди групуйте виклики `orWhere`, щоб уникнути неочікуваної поведінки, коли застосовуються глобальні скопи.

<a name="where-not-clauses"></a>
### Умови WHERE NOT

Методами `whereNot` і `orWhereNot` можна заперечити задану групу обмежень запиту. Наприклад, цей запит виключає товари, які продаються за акцією або дешевші за десять:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### Умови Any / All / None

Іноді вам потрібно застосувати ті самі обмеження до кількох стовпців. Наприклад, ви хочете дістати всі записи, у яких будь-який зі стовпців зі списку `LIKE` задане значення. Це робить метод `whereAny`:

```php
$users = DB::table('users')
    ->where('active', true)
    ->whereAny([
        'name',
        'email',
        'phone',
    ], 'like', 'Example%')
    ->get();
```

Наведений вище запит дасть такий SQL:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

Аналогічно, метод `whereAll` дістає записи, у яких усі задані стовпці відповідають обмеженню:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

Наведений вище запит дасть такий SQL:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

Метод `whereNone` дістає записи, у яких жоден із заданих стовпців не відповідає обмеженню:

```php
$albums = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

Наведений вище запит дасть такий SQL:

```sql
SELECT *
FROM albums
WHERE published = true AND NOT (
    title LIKE '%explicit%' OR
    lyrics LIKE '%explicit%' OR
    tags LIKE '%explicit%'
)
```

<a name="json-where-clauses"></a>
### Умови WHERE для JSON

Laravel підтримує запити до стовпців типу JSON у базах даних, які мають підтримку таких стовпців. Наразі це MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+ і SQLite 3.39.0+. Щоб звернутися до стовпця JSON, скористайтеся оператором `->`:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

Щоб робити запити до масивів JSON, скористайтеся методами `whereJsonContains` і `whereJsonDoesntContain`:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

Якщо ваш застосунок працює з MariaDB, MySQL або PostgreSQL, методам `whereJsonContains` і `whereJsonDoesntContain` можна передати масив значень:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

Крім того, методами `whereJsonContainsKey` і `whereJsonDoesntContainKey` ви можете дістати результати, які містять або не містять певний ключ JSON:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

Нарешті, методом `whereJsonLength` можна робити запити до масивів JSON за їхньою довжиною:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### Додаткові умови WHERE

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

Метод `whereLike` додає до запиту умови «LIKE» для пошуку за шаблоном. Ці методи дають незалежний від бази даних спосіб порівнювати рядки з можливістю керувати чутливістю до регістру. За замовчуванням порівняння рядків не чутливе до регістру:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

Увімкнути чутливий до регістру пошук можна аргументом `caseSensitive`:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

Метод `orWhereLike` додає умову «or» з умовою LIKE:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

Метод `whereNotLike` додає до запиту умови «NOT LIKE»:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

Аналогічно, `orWhereNotLike` додає умову «or» з умовою NOT LIKE:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> Опція чутливого до регістру пошуку в `whereLike` наразі не підтримується на SQL Server.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

Метод `whereIn` перевіряє, що значення заданого стовпця міститься в заданому масиві:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

Метод `whereNotIn` перевіряє, що значення заданого стовпця не міститься в заданому масиві:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

Другим аргументом методу `whereIn` можна також передати об'єкт запиту:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

Наведений вище приклад дасть такий SQL:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> Якщо ви додаєте до запиту великий масив цілочисельних прив'язок, методи `whereIntegerInRaw` або `whereIntegerNotInRaw` допоможуть значно зменшити споживання пам'яті.

**whereBetween / orWhereBetween**

Метод `whereBetween` перевіряє, що значення стовпця лежить між двома значеннями:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

Метод `whereNotBetween` перевіряє, що значення стовпця лежить за межами двох значень:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

Метод `whereBetweenColumns` перевіряє, що значення стовпця лежить між значеннями двох стовпців того самого рядка таблиці:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

Метод `whereNotBetweenColumns` перевіряє, що значення стовпця лежить за межами значень двох стовпців того самого рядка таблиці:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

Метод `whereValueBetween` перевіряє, що задане значення лежить між значеннями двох стовпців того самого типу в тому самому рядку таблиці:

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

Метод `whereValueNotBetween` перевіряє, що значення лежить за межами значень двох стовпців того самого рядка таблиці:

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

Метод `whereNull` перевіряє, що значення заданого стовпця дорівнює `NULL`:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

Метод `whereNotNull` перевіряє, що значення стовпця не дорівнює `NULL`:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereNullSafeEquals / orWhereNullSafeEquals**

Методами `whereNullSafeEquals` і `orWhereNullSafeEquals` можна порівняти значення стовпця із заданим значенням, вважаючи два значення `NULL` рівними:

```php
$lastLoginIp = $request->input('last_login_ip');

$users = DB::table('users')
    ->whereNullSafeEquals('last_login_ip', $lastLoginIp)
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

Метод `whereDate` порівнює значення стовпця з датою:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

Метод `whereMonth` порівнює значення стовпця з конкретним місяцем:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

Метод `whereDay` порівнює значення стовпця з конкретним днем місяця:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

Метод `whereYear` порівнює значення стовпця з конкретним роком:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

Метод `whereTime` порівнює значення стовпця з конкретним часом:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

Методами `wherePast` і `whereFuture` можна визначити, чи значення стовпця в минулому або майбутньому:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

Методами `whereNowOrPast` і `whereNowOrFuture` можна визначити, чи значення стовпця в минулому або майбутньому, включно з поточними датою та часом:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

Методами `whereToday`, `whereBeforeToday` і `whereAfterToday` можна визначити, чи значення стовпця припадає на сьогодні, до сьогодні або після сьогодні відповідно:

```php
$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();
```

Аналогічно, методами `whereTodayOrBefore` і `whereTodayOrAfter` можна визначити, чи значення стовпця припадає на час до сьогодні або після сьогодні, включно з сьогоднішньою датою:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

Методом `whereColumn` можна перевірити, що два стовпці рівні:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

Методу `whereColumn` можна також передати оператор порівняння:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

Методу `whereColumn` можна передати й масив порівнянь стовпців. Ці умови з'єднаються оператором `and`:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### Логічне групування

Іноді вам потрібно згрупувати кілька умов «where» у дужках, щоб досягти потрібної логіки запиту. Власне, виклики методу `orWhere` варто завжди брати в дужки, щоб запит не поводився неочікувано. Для цього передайте методу `where` замикання:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

Як бачите, передане в метод `where` замикання наказує конструктору запитів почати групу обмежень. Замикання отримає екземпляр конструктора, у якому ви задаєте обмеження, що мають опинитися в дужках. Наведений вище приклад дасть такий SQL:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> Завжди групуйте виклики `orWhere`, щоб уникнути неочікуваної поведінки, коли застосовуються глобальні скопи.

<a name="advanced-where-clauses"></a>
## Складніші умови WHERE

<a name="where-exists-clauses"></a>
### Умови WHERE EXISTS

Метод `whereExists` дозволяє писати SQL-вирази «where exists». Він приймає замикання, яке отримає екземпляр конструктора запитів, - у ньому ви описуєте запит, що має опинитися всередині виразу «exists»:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

Замість замикання методу `whereExists` можна передати об'єкт запиту:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

Обидва наведені вище приклади дадуть такий SQL:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### Умови WHERE з підзапитом

Іноді вам потрібно побудувати умову «where», яка порівнює результат підзапиту із заданим значенням. Для цього передайте методу `where` замикання і значення. Наприклад, цей запит дістане всіх користувачів, які мають нещодавнє «membership» заданого типу;

```php
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

Або вам може знадобитися умова «where», яка порівнює стовпець із результатом підзапиту. Для цього передайте методу `where` стовпець, оператор і замикання. Наприклад, цей запит дістане всі записи про дохід, де сума менша за середню;

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### Умови повнотекстового пошуку

> [!WARNING]
> Умови повнотекстового пошуку наразі підтримують MariaDB, MySQL і PostgreSQL.

Методами `whereFullText` і `orWhereFullText` можна додати до запиту повнотекстові умови «where» для стовпців, що мають [повнотекстові індекси](/docs/{{version}}/migrations#available-index-types). Laravel перетворить їх на відповідний SQL для вашої системи баз даних. Наприклад, для застосунків на MariaDB чи MySQL буде згенеровано вираз `MATCH AGAINST`:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### Умови векторної схожості

> [!NOTE]
> Умови векторної схожості наразі підтримуються лише на підключеннях PostgreSQL із розширенням `pgvector`. Про те, як описувати векторні стовпці та індекси, читайте в [документації з міграцій](/docs/{{version}}/migrations#available-column-types).

Метод `whereVectorSimilarTo` фільтрує результати за косинусною схожістю до заданого вектора й сортує їх за релевантністю. Поріг `minSimilarity` має бути значенням між `0.0` і `1.0`, де `1.0` - повна ідентичність:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

Якщо як вектор передано звичайний рядок, Laravel автоматично згенерує для нього ембединги за допомогою [Laravel AI SDK](/docs/{{version}}/ai-sdk#embeddings):

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

За замовчуванням `whereVectorSimilarTo` також сортує результати за відстанню (найсхожіші спершу). Вимкнути це сортування можна, передавши `false` в аргументі `order`:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

Якщо вам потрібно більше контролю, скористайтеся методами `selectVectorDistance`, `whereVectorDistanceLessThan` і `orderByVectorDistance` окремо:

```php
$documents = DB::table('documents')
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

На PostgreSQL розширення `pgvector` має бути завантажене, перш ніж можна створювати стовпці `vector`:

```php
Schema::ensureVectorExtensionExists();
```

<a name="ordering-grouping-limit-and-offset"></a>
## Сортування, групування, limit та offset

<a name="ordering"></a>
### Сортування

<a name="orderby"></a>
#### Метод `orderBy`

Метод `orderBy` сортує результати запиту за заданим стовпцем. Перший аргумент - стовпець, за яким сортувати, а другий визначає напрямок сортування: `asc` або `desc`:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

Щоб сортувати за кількома стовпцями, просто викличте `orderBy` стільки разів, скільки потрібно:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

Напрямок сортування необов'язковий, за замовчуванням - за зростанням. Щоб сортувати за спаданням, задайте другий параметр методу `orderBy` або просто скористайтеся `orderByDesc`:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

Нарешті, за допомогою оператора `->` результати можна сортувати за значенням усередині стовпця JSON:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### Методи `latest` і `oldest`

Методи `latest` і `oldest` дозволяють легко сортувати результати за датою. За замовчуванням результати сортуються за стовпцем `created_at` таблиці. Або ви можете передати назву стовпця, за яким хочете сортувати:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### Випадкове сортування

Метод `inRandomOrder` сортує результати запиту випадковим чином. Наприклад, так можна дістати випадкового користувача:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### Скидання наявного сортування

Метод `reorder` прибирає всі вирази «order by», які раніше застосували до запиту:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

Викликаючи `reorder`, ви можете передати стовпець і напрямок, щоб прибрати всі наявні вирази «order by» й задати запиту цілком нове сортування:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

Для зручності є метод `reorderDesc`, який перевпорядковує результати за спаданням:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### Групування

<a name="groupby-having"></a>
#### Методи `groupBy` і `having`

Як і слід очікувати, методи `groupBy` і `having` групують результати запиту. Сигнатура методу `having` схожа на сигнатуру `where`:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

Методом `havingBetween` можна відфільтрувати результати в заданому діапазоні:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

Щоб групувати за кількома стовпцями, передайте методу `groupBy` кілька аргументів:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

Щоб будувати складніші вирази `having`, дивіться метод [havingRaw](#raw-methods).

<a name="limit-and-offset"></a>
### Limit та offset

Методами `limit` і `offset` можна обмежити кількість результатів запиту або пропустити задану кількість результатів:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## Умовні вирази

Іноді вам потрібно, щоб певні умови застосовувалися до запиту залежно від іншої умови. Наприклад, ви хочете додати вираз `where`, лише якщо у вхідному HTTP-запиті є певне значення. Це робить метод `when`:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

Метод `when` виконує задане замикання лише тоді, коли перший аргумент - `true`. Якщо перший аргумент `false`, замикання не виконається. Тож у прикладі вище замикання буде викликано лише за умови, що поле `role` є у вхідному запиті й дає `true`.

Третім аргументом методу `when` можна передати ще одне замикання. Воно виконається лише тоді, коли перший аргумент дає `false`. Щоб показати, як це працює, налаштуємо сортування запиту за замовчуванням:

```php
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
    ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
        $query->orderBy('votes');
    }, function (Builder $query) {
        $query->orderBy('name');
    })
    ->get();
```

<a name="insert-statements"></a>
## Запити INSERT

Конструктор запитів має також метод `insert` для вставки записів у таблицю. Метод `insert` приймає масив назв стовпців і значень:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

Ви можете вставити кілька записів одразу, передавши масив масивів. Кожен масив - це запис, який слід вставити в таблицю:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

Метод `insertOrIgnore` ігнорує помилки під час вставки записів. Використовуючи його, зважте: ігноруються не лише помилки дублювання записів - залежно від рушія бази даних можуть ігноруватися й інші типи помилок. Наприклад, `insertOrIgnore` [обходить strict mode у MySQL](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution):

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

Метод `insertUsing` вставляє в таблицю нові записи, визначаючи дані для вставки підзапитом:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### Автоінкрементні ID

Якщо таблиця має автоінкрементний id, скористайтеся методом `insertGetId`, щоб вставити запис і одразу отримати його ID:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> На PostgreSQL метод `insertGetId` очікує, що автоінкрементний стовпець називається `id`. Якщо ви хочете отримати ID з іншої «послідовності», передайте назву стовпця другим параметром методу `insertGetId`.

<a name="upserts"></a>
### Upsert

Метод `upsert` вставляє записи, яких немає, і оновлює наявні заданими вами новими значеннями. Перший аргумент методу - значення для вставки чи оновлення, другий - стовпці, які унікально ідентифікують записи у відповідній таблиці. Третій і останній аргумент - масив стовпців, які слід оновити, якщо відповідний запис у базі вже є:

```php
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

У прикладі вище Laravel спробує вставити два записи. Якщо запис із такими самими значеннями стовпців `departure` і `destination` уже існує, Laravel оновить його стовпець `price`.

> [!WARNING]
> Усі бази даних, окрім SQL Server, вимагають, щоб стовпці з другого аргументу методу `upsert` мали індекс «primary» або «unique». Крім того, драйвери MariaDB і MySQL ігнорують другий аргумент `upsert` і завжди використовують індекси «primary» та «unique» таблиці, щоб виявити наявні записи.

<a name="update-statements"></a>
## Запити UPDATE

Крім вставки записів, конструктор запитів може оновлювати наявні - методом `update`. Як і `insert`, метод `update` приймає масив пар «стовпець - значення», які вказують, що саме оновити. Метод `update` повертає кількість зачеплених рядків. Обмежити запит `update` можна виразами `where`:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Оновити або вставити

Іноді вам потрібно оновити наявний запис у базі даних або створити його, якщо відповідного немає. У такому разі скористайтеся методом `updateOrInsert`. Він приймає два аргументи: масив умов, за якими шукати запис, і масив пар «стовпець - значення», які вказують, що оновити.

Метод `updateOrInsert` спробує знайти відповідний запис за парами «стовпець - значення» з першого аргументу. Якщо запис існує, його буде оновлено значеннями з другого аргументу. Якщо запису немає, буде вставлено новий зі об'єднаними атрибутами обох аргументів:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

Методу `updateOrInsert` можна передати замикання, щоб задати атрибути для оновлення чи вставки залежно від того, чи знайдено відповідний запис:

```php
DB::table('users')->updateOrInsert(
    ['user_id' => $user_id],
    fn ($exists) => $exists ? [
        'name' => $data['name'],
        'email' => $data['email'],
    ] : [
        'name' => $data['name'],
        'email' => $data['email'],
        'marketable' => true,
    ],
);
```

<a name="updating-json-columns"></a>
### Оновлення стовпців JSON

Оновлюючи стовпець JSON, використовуйте синтаксис `->`, щоб оновити потрібний ключ в об'єкті JSON. Ця операція підтримується на MariaDB 10.3+, MySQL 5.7+ і PostgreSQL 9.5+:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### Збільшення та зменшення

Конструктор запитів має також зручні методи для збільшення та зменшення значення заданого стовпця. Обидва приймають щонайменше один аргумент - стовпець, який змінюємо. Другим аргументом можна задати величину, на яку слід збільшити чи зменшити значення:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

За потреби ви можете вказати й додаткові стовпці, які слід оновити під час збільшення чи зменшення:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

Крім того, методами `incrementEach` і `decrementEach` можна збільшити або зменшити кілька стовпців одразу:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Запити DELETE

Методом `delete` конструктора запитів можна видаляти записи з таблиці. Метод `delete` повертає кількість зачеплених рядків. Обмежити запит `delete` можна, додавши умови «where» перед викликом `delete`:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## Песимістичне блокування

Конструктор запитів має також кілька функцій, які допомагають реалізувати «песимістичне блокування» під час виконання запитів `select`. Щоб виконати запит зі «спільним блокуванням» (shared lock), викличте метод `sharedLock`. Спільне блокування не дає змінювати вибрані рядки, поки ваша транзакція не завершиться комітом:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

Або ви можете скористатися методом `lockForUpdate`. Блокування «for update» не дає змінювати вибрані записи й вибирати їх з іншим спільним блокуванням:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

Це не обов'язково, але песимістичні блокування радимо обгортати в [транзакцію](/docs/{{version}}/database#database-transactions). Так отримані дані лишаються незмінними в базі, поки вся операція не завершиться. У разі збою транзакція відкотить усі зміни й автоматично звільнить блокування:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate()
        ->find(2);

    if ($sender->balance < 100) {
        throw new RuntimeException('Balance too low.');
    }

    DB::table('users')
        ->where('id', $sender->id)
        ->update([
            'balance' => $sender->balance - 100
        ]);

    DB::table('users')
        ->where('id', $receiver->id)
        ->update([
            'balance' => $receiver->balance + 100
        ]);
});
```

<a name="reusable-query-components"></a>
## Повторно використовувані компоненти запитів

Якщо у вашому застосунку повторюється однакова логіка запитів, ви можете винести її в повторно використовувані об'єкти за допомогою методів `tap` і `pipe` конструктора запитів. Уявіть, що у вас є два такі різні запити:

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->orderByDesc('price')
    ->get();

// ...

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

Спільну для обох запитів фільтрацію за призначенням варто винести в повторно використовуваний об'єкт:

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Query\Builder;

class DestinationFilter
{
    public function __construct(
        private ?string $destination,
    ) {
        //
    }

    public function __invoke(Builder $query): void
    {
        $query->when($this->destination, function (Builder $query) {
            $query->where('destination', $this->destination);
        });
    }
}
```

Далі ви можете застосувати логіку об'єкта до запиту методом `tap` конструктора запитів:

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### Пайпи запитів

Метод `tap` завжди повертає конструктор запитів. Якщо ви хочете винести об'єкт, який виконує запит і повертає інше значення, скористайтеся методом `pipe`.

Розгляньмо об'єкт запиту зі спільною логікою [пагінації](/docs/{{version}}/pagination), яка використовується в усьому застосунку. На відміну від `DestinationFilter`, що додає до запиту умови, об'єкт `Paginate` виконує запит і повертає екземпляр пагінатора:

```php
<?php

namespace App\Scopes;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Query\Builder;

class Paginate
{
    public function __construct(
        private string $sortBy = 'timestamp',
        private string $sortDirection = 'desc',
        private int $perPage = 25,
    ) {
        //
    }

    public function __invoke(Builder $query): LengthAwarePaginator
    {
        return $query->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage, pageName: 'p');
    }
}
```

За допомогою методу `pipe` конструктора запитів ми можемо застосувати цей об'єкт зі спільною логікою пагінації:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## Налагодження

Під час побудови запиту ви можете скористатися методами `dd` і `dump`, щоб вивести поточні прив'язки та SQL. Метод `dd` покаже інформацію для налагодження й зупинить виконання запиту. Метод `dump` покаже цю інформацію, але дозволить запиту виконуватися далі:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

Методи `dumpRawSql` і `ddRawSql` виводять SQL запиту з усіма належно підставленими прив'язками параметрів:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
