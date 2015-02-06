# 遷移和資料填充

- [介紹](#introduction)
- [建立遷移檔](#creating-migrations)
- [執行遷移](#running-migrations)
- [推回遷移](#rolling-back-migrations)
- [資料填充](#database-seeding)

<a name="introduction"></a>
## 介紹

遷移是一種資料庫的版本控制。可以讓團隊在修改資料庫結構的同時，保持彼此的進度一致。遷移通常會和 [結構生成器](/docs/5.0/schema) 一起使用，可以簡單的管理資料庫結構。

<a name="creating-migrations"></a>
## 建立遷移檔

使用 Artisan CLI 的 `make:migrate` 命令建立遷移檔：

    php artisan make:migration create_users_table

遷移檔會建立在 `database/migrations` 目錄下，檔名會包含時間戳記，在執行遷移時用來決定順序。

你也可以在建立遷移命令加上 `--path` 參數。路徑要相對於應用程式所在的根目錄。

    php artisan make:migration foo --path=app/migrations

`--table` 和 `--create` 參數可以用來指定資料表名稱，以及遷移檔是否要建立新的資料表。

    php artisan make:migration add_votes_to_user_table --table=users

    php artisan make:migration create_users_table --create=users

<a name="running-migrations"></a>
## 執行遷移

#### 執行所有未執行遷移

    php artisan migrate

> **注意:** 如果在執行遷移時發生「class not found」錯誤，試著先執行 `composer dump-autoload` 命令後再進行一次。

### 在上線環境 (Production) 中強制執行遷移

有些遷移操作是具有破壞性的，意味著可能讓你遺失原本儲存的資料。為了防止你在上線環境執行到這些遷移命令，你會被提示要在執行遷移前進行確認。加上 `--force` 參數執行強制遷移：

    php artisan migrate --force

<a name="rolling-back-migrations"></a>
## 推回遷移

#### 推回上一次的遷移

    php artisan migrate:rollback

#### 推回所有遷移

    php artisan migrate:reset

#### 推回所有遷移並且再執行一次

    php artisan migrate:refresh

    php artisan migrate:refresh --seed

<a name="database-seeding"></a>
## 資料填充

Laravel 可以簡單的使用 seed 類別，填充測試資料到資料庫。所有的 seed 類別放在 `database/seeds` 目錄下。可以使用任何你想要的類別名稱，但是應該遵守某些大小寫規範，像是 `UserTableSeeder` 之類。預設已經有一個 `DatabaseSeeder` 類別。在這個類別裡，使用 `call` 方法執行其他的 seed 類別，讓你控制填充的順序。

#### Seed 類別範例

    class DatabaseSeeder extends Seeder {

        public function run()
        {
            $this->call('UserTableSeeder');

            $this->command->info('User table seeded!');
        }

    }

    class UserTableSeeder extends Seeder {

        public function run()
        {
            DB::table('users')->delete();

            User::create(array('email' => 'foo@bar.com'));
        }

    }

要執行資料填充，可以使用 Artisan CLI 的 `db:seed` 命令：

    php artisan db:seed

預設 `db:seed` 命令會執行 `DatabaseSeeder`，可以使用它來呼叫其他 seed 類別，不過，也可以使用 `--class` 參數指定要單獨執行的類別：

    php artisan db:seed --class=UserTableSeeder

你可以也使用 `migrate:refresh` 命令填充資料，它會推回並且再次執行所有遷移：

    php artisan migrate:refresh --seed
