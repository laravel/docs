# 資料庫：資料填充

- [資料庫：資料填充](#資料庫seeding)
  - [介紹](#介紹)
  - [撰寫Seeders](#撰寫seeders)
    - [使用模型工廠](#使用-model-factories)
    - [呼叫額外 Seeders](#呼叫額外-seeders)
    - [關閉模型事件](#關閉-model-events)
  - [執行 Seeders](#執行-seeders)

<a name="introduction"></a>
## 介紹

Laravel提供 Seeder Classes 來為您的資料庫輸入資料，所有的 Seeder Classes 檔案都放置於 `database/seeders` 資料夾下。預設情況下，已經有一個定義好的 `DatabaseSeeder` Class 在該資料夾。透過這個Class，您可以使用 `call` 方法來執行其他 Seeder Classes，藉此您能夠控制建立資料的順序。

> {技巧} 在 Seeder Classes 建立資料的過程中，[Mass assignment protection](/docs/{{version}}/eloquent#mass-assignment)預設是關閉的。


<a name="writing-seeders"></a>
## 撰寫 Seeders

我們可以透過 `make:seeder` [Artisan command](/docs/{{version}}/artisan) 這個指令來撰寫一個 Seeder Class。Laravel 製作的所有 Seeder Classes 都會放在 `database/seeders` 資料夾內。

```shell
php artisan make:seeder UserSeeder
```

一個 Seeder Class 預設只會有一個 `run` 方法。該方法會在輸入 `db:seed` [Artisan command](/docs/{{version}}/artisan) 後執行。
在 `run` 方法內，您可以用任何方式新增您的資料，您可以使用 [query builder](/docs/{{version}}/queries) 來手動輸入資料或使用 [Eloquent model factories](/docs/{{version}}/database-testing#defining-model-factories) 來建立資料。

舉例來說，我們可以修改預設的 `DatabaseSeeder` Class，在 `run` 內寫一個新增資料的語法：

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
         *
         * @return void
         */
        public function run()
        {
            DB::table('users')->insert([
                'name' => Str::random(10),
                'email' => Str::random(10).'@gmail.com',
                'password' => Hash::make('password'),
            ]);
        }
    }

> {技巧} 您可以給 `run` 方法任何您需要的依賴作為參數型態，Laravel 會透過 [服務容器](/docs/{{version}}/container) 自動使用這些參數型態。

<a name="using-model-factories"></a>
### 使用模型工廠

當然，為每個模型手動輸入資料是十分麻煩的。這時您可以使用非常方便的 [模型工廠](/docs/{{version}}/database-testing#defining-model-factories) 來一次產生大量資料。首先，先來複習 [模型工廠文件](/docs/{{version}}/database-testing#defining-model-factories) 來學習如何定義您的工廠。

舉例來說，建立50個使用者且每個使用者都有1篇貼文：

    use App\Models\User;

    /**
     * Run the database seeders.
     *
     * @return void
     */
    public function run()
    {
        User::factory()
                ->count(50)
                ->hasPosts(1)
                ->create();
    }

<a name="calling-additional-seeders"></a>
### 呼叫額外 Seeders

在 `DatabaseSeeder` Class，您可以使用 `call` 來使用額外的 Seeder Classes。這種做法可以幫助您將建立資料的過程分割為數個檔案，不會讓其中一個 Seeder class 變得過大。而 `call` 接受一個陣列作為參數，該陣列內包含要執行的 Seeder Classes。

    /**
     * Run the database seeders.
     *
     * @return void
     */
    public function run()
    {
        $this->call([
            UserSeeder::class,
            PostSeeder::class,
            CommentSeeder::class,
        ]);
    }

<a name="muting-model-events"></a>
### 關閉模型事件

在建立資料的過程中，您也許會想避免模型發送事件，您可使用 `WithoutModelEvents` Trait 來達到該效果。當使用 `WithoutModelEvents` 時，它能保證模型不會發送任何事件，就算是使用 `call` 執行多個 Seeder Classes 也一樣。


    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Console\Seeds\WithoutModelEvents;

    class DatabaseSeeder extends Seeder
    {
        use WithoutModelEvents;

        /**
         * Run the database seeders.
         *
         * @return void
         */
        public function run()
        {
            $this->call([
                UserSeeder::class,
            ]);
        }
    }

<a name="running-seeders"></a>
## 執行 Seeders

您可以透過執行 `db:seed` Artisan command 來建立資料到資料庫內。預設情況下，`db:seed` 會執行 `Database\Seeders\DatabaseSeeder` 這個 Class，而該 Class可以用於呼叫其他 Seeder Classes。然而，您可以使用 `--class` 參數來指定您想執行的 Seeder Class。

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

若您想刪掉現有的資料表並重新建立資料，您也可以使用 `migrate:fresh` 與 `--seed` ，這種做法對於重新建立資料庫是十分方便的。

```shell
php artisan migrate:fresh --seed
```

<a name="forcing-seeding-production"></a>
#### 在正式站環境強制執行 Seeders

有些建立資料的作業可能會導致資料異動或遺失，為了避免在 `production` 環境發生這種情況，在該環境執行 Seeders 時會詢問是否要在該環境執行，這時您可以使用 `--force` 來跳過該詢問過程。

```shell
php artisan db:seed --force
```
