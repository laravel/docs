# 資料庫：資料填充

- [介紹](#introduction)
- [撰寫 Seeders](#writing-seeders)
    - [使用模型工廠](#using-model-factories)
    - [呼叫額外 Seeders](#calling-additional-seeders)
    - [關閉模型事件](#muting-model-events)
- [執行 Seeders](#running-seeders)

<a name="introduction"></a>
## 介紹

Laravel 提供 Seeder 類別來為您的資料庫輸入資料，所有的 Seeder 類別檔案都放置於 `database/seeders` 資料夾下。預設情況下，已經有一個定義好的 `DatabaseSeeder` 類別在該資料夾。透過這個類別，您可以使用 `call` 方法來執行其他 Seeder 類別，藉此您能夠控制建立資料的順序。

> {tip} 在 Seeder 類別建立資料的過程中，[Mass assignment protection](/docs/{{version}}/eloquent#mass-assignment) 預設是關閉的。


<a name="writing-seeders"></a>
## 撰寫 Seeders

我們可以透過 `make:seeder` [Artisan 指令](/docs/{{version}}/artisan) 這個指令來撰寫一個 Seeder 類別。Laravel 製作的所有 Seeder 類別都會放在 `database/seeders` 資料夾內。

```shell
php artisan make:seeder UserSeeder
```

一個 Seeder 類別預設只會有一個 `run` 方法。該方法會在輸入 `db:seed` [Artisan 指令](/docs/{{version}}/artisan) 後執行。
在 `run` 方法內，您可以用任何方式新增您的資料，如使用 [查詢產生器](/docs/{{version}}/queries) 來手動輸入資料或使用 [Eloquent 模型工廠](/docs/{{version}}/database-testing#defining-model-factories) 來建立資料。

舉例來說，我們可以修改預設的 `DatabaseSeeder` 類別，在 `run` 內寫一個新增資料的語法：

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Support\Str;

    Class DatabaseSeeder extends Seeder
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

> {tip} 您可以給 `run` 方法任何您需要的依賴作為參數型態，Laravel 會透過 [服務容器](/docs/{{version}}/container) 自動使用這些參數型態。

<a name="using-model-factories"></a>
### 使用模型工廠

當然，為每個模型手動輸入資料是十分麻煩的。這時您可以使用非常方便的 [模型工廠](/docs/{{version}}/database-testing#defining-model-factories) 來一次產生大量資料。首先，先來複習 [模型工廠文件](/docs/{{version}}/database-testing#defining-model-factories) 來學習如何定義您的工廠。

舉例來說，建立 50 個使用者且每個使用者都有 1 篇貼文：

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

在 `DatabaseSeeder` 類別，您可以使用 `call` 來使用額外的 Seeder 類別。這種做法可以幫助您將 `Seeder 類別` 分成數個檔案，不會讓其中一個 Seeder 類別變得過大。而 `call` 接受一個陣列作為參數，該陣列內包含要執行的 Seeder 類別。

    /**
     * Run the database seeders.
     *
     * @return void
     */
    public function run()
    {
        $this->call([
            UserSeeder::Class,
            PostSeeder::Class,
            CommentSeeder::Class,
        ]);
    }

<a name="muting-model-events"></a>
### 關閉模型事件

在建立資料的過程中，您也許會想避免模型發送事件，您可使用 `WithoutModelEvents` 這個 Trait 來達到該效果。當使用 `WithoutModelEvents` 時，它能保證模型不會發送任何事件，就算是使用 `call` 執行多個 Seeder 類別也一樣。


    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Console\Seeds\WithoutModelEvents;

    Class DatabaseSeeder extends Seeder
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
                UserSeeder::Class,
            ]);
        }
    }

<a name="running-seeders"></a>
## 執行 Seeders

您可以透過執行 `db:seed` Artisan指令 來建立資料到資料庫內。預設情況下，`db:seed` 會執行 `Database\Seeders\DatabaseSeeder` 這個 類別，而該 類別可以用於呼叫其他 Seeder 類別。然而，您可以使用 `--類別` 參數來指定您想執行的 Seeder 類別。

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

該指令可用於重建整個資料庫。

```shell
php artisan migrate:fresh --seed
```

<a name="forcing-seeding-production"></a>
#### 在正式站環境強制執行 Seeders

有些建立資料的作業可能會導致資料異動或遺失，為了避免在 `production` 環境發生這種情況，在該環境執行 Seeders 時會詢問是否要在該環境執行，這時您可以使用 `--force` 來跳過該詢問過程。

```shell
php artisan db:seed --force
```
