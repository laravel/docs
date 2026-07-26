---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---

# База даних: наповнення

- [Вступ](#introduction)
- [Написання сідерів](#writing-seeders)
    - [Використання фабрик моделей](#using-model-factories)
    - [Виклик додаткових сідерів](#calling-additional-seeders)
    - [Вимкнення подій моделей](#muting-model-events)
- [Запуск сідерів](#running-seeders)

<a name="introduction"></a>
## Вступ

Laravel уміє наповнювати вашу базу даних тестовими даними за допомогою класів-сідерів (seeder). Усі класи сідерів зберігаються в каталозі `database/seeders`. За замовчуванням для вас уже визначено клас `DatabaseSeeder`. З нього ви можете методом `call` запускати інші класи сідерів і таким чином керувати порядком наповнення.

> [!NOTE]
> Під час наповнення бази даних [захист від масового призначення](/docs/{{version}}/eloquent#mass-assignment) автоматично вимикається.

<a name="writing-seeders"></a>
## Написання сідерів

Щоб згенерувати сідер, виконайте [artisan-команду](/docs/{{version}}/artisan) `make:seeder`. Усі згенеровані фреймворком сідери потраплять до каталогу `database/seeders`:

```shell
php artisan make:seeder UserSeeder
```

За замовчуванням клас сідера містить лише один метод - `run`. Він викликається при виконанні [artisan-команди](/docs/{{version}}/artisan) `db:seed`. Усередині методу `run` ви можете наповнювати базу даних як завгодно: вручну вставляти дані через [конструктор запитів](/docs/{{version}}/queries) або скористатися [фабриками моделей Eloquent](/docs/{{version}}/eloquent-factories).

Наприклад, змінімо стандартний клас `DatabaseSeeder` і додаймо до методу `run` вставку даних:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

> [!NOTE]
> У сигнатурі методу `run` ви можете вказати типи будь-яких потрібних вам залежностей. Laravel автоматично отримає їх із [сервіс-контейнера](/docs/{{version}}/container).

<a name="using-model-factories"></a>
### Використання фабрик моделей

Звісно, вручну задавати атрибути для кожної моделі - марудна робота. Замість цього ви можете скористатися [фабриками моделей](/docs/{{version}}/eloquent-factories), щоб зручно згенерувати велику кількість записів. Спершу перегляньте [документацію з фабрик моделей](/docs/{{version}}/eloquent-factories), щоб дізнатися, як їх описувати.

Наприклад, створімо 50 користувачів, кожен із яких має один пов'язаний пост:

```php
use App\Models\User;

/**
 * Run the database seeders.
 */
public function run(): void
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}
```

<a name="calling-additional-seeders"></a>
### Виклик додаткових сідерів

Усередині класу `DatabaseSeeder` ви можете методом `call` запускати додаткові класи сідерів. Метод `call` дозволяє розбити наповнення бази на кілька файлів, щоб жоден клас сідера не розростався надміру. Він приймає масив класів сідерів, які потрібно виконати:

```php
/**
 * Run the database seeders.
 */
public function run(): void
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}
```

<a name="muting-model-events"></a>
### Вимкнення подій моделей

Під час наповнення бази ви можете захотіти, щоб моделі не надсилали події. Цього можна досягти за допомогою трейта `WithoutModelEvents`. Трейт `WithoutModelEvents` гарантує, що жодної події моделі не буде надіслано, навіть якщо через метод `call` виконуються додаткові класи сідерів:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
        ]);
    }
}
```

<a name="running-seeders"></a>
## Запуск сідерів

Щоб наповнити базу даних, виконайте artisan-команду `db:seed`. За замовчуванням команда `db:seed` запускає клас `Database\Seeders\DatabaseSeeder`, який, своєю чергою, може викликати інші класи сідерів. Втім, опцією `--class` ви можете вказати конкретний клас сідера, який слід запустити окремо:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

Ви також можете наповнити базу даних командою `migrate:fresh` з опцією `--seed`: вона видалить усі таблиці та повторно виконає всі ваші міграції. Ця команда стане в пригоді, коли треба повністю перебудувати базу даних. Опцією `--seeder` можна вказати конкретний сідер, який слід запустити:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a name="forcing-seeding-production"></a>
#### Примусовий запуск сідерів на продакшні

Деякі операції наповнення можуть змінити або знищити дані. Щоб убезпечити вас від запуску таких команд на продакшн-базі, у середовищі `production` Laravel запитає підтвердження, перш ніж виконати сідери. Щоб запустити сідери без запитання, скористайтеся прапорцем `--force`:

```shell
php artisan db:seed --force
```
