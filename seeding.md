# 資料庫: 資料填充

- [簡介](#introduction)
- [撰寫 Seeders](#writing-seeders)
    - [使用模型工廠](#using-model-factories)
    - [呼叫其他的 Seeders](#calling-additional-seeders)
- [執行 Seeders](#running-seeders)

<a name="introduction"></a>
## 簡介

Laravel 可以簡單的使用 seed 類別，填充測試用的資料至資料庫。所有的 seed 類別放在 `database/seeds` 目錄下。你可以任意地為 Seed 類別命名，但是應該遵守某些大小寫規範，像是 `UserTableSeeder` 之類。預設已經為你定義了一個 `DatabaseSeeder` 類別。在這個類別裡，你可以使用 `call` 方法執行其他的 seed 類別，藉此控制資料填充的順序。

<a name="writing-seeders"></a>
## 撰寫資料填充

你可以透過 `make:seeder` [Artisan 指令](/docs/{{version}}/artisan) 來生成一個 Seeder。所有透過框架生成的 Seeder 都將被放置在 `database/seeders` 路徑：

    php artisan make:seeder UsersTableSeeder

在 seeder 類別裡只會預設一個方法：`run`。當執行 `db:seed` [Artisan 指令](/docs/{{version}}/artisan) 時就會呼叫此方法。在 `run` 方法中，你可以新增任何想要的數據至你的資料庫中。你可使用 [查詢產生器](/docs/{{version}}/queries) 手動新增數據或你也可以使用 [Eloquent 模型工廠](/docs/{{version}}/testing#model-factories)。

如同下面的範例，我們修改 Laravel 預先安裝好的 `DatabaseSeeder` 類別。我們在 `run` 方法中添加了一段在資料庫新增數據的語法：

    <?php

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Eloquent\Model;

    class DatabaseSeeder extends Seeder
    {
        /**
         * Run the database seeds.
         *
         * @return void
         */
        public function run()
        {
            DB::table('users')->insert([
                'name' => str_random(10),
                'email' => str_random(10).'@gmail.com',
                'password' => bcrypt('secret'),
            ]);
        }
    }

<a name="using-model-factories"></a>
### 使用模型工廠

當然，手動為每一個 seed 模型一一指定屬性是很麻煩的。作為替代方案，你可以使用 [模型工廠](/docs/{{version}}/testing#model-factories) 幫你便利地生成大量的資料庫數據。首先，閱讀 [模型工廠的文件](/docs/{{version}}/testing#model-factories) 來學習如何定義你的工廠。一旦你定義了你的工廠，你就可以使用 `factory` 這個輔助方法函式來新增數據到資料庫中。

舉例來說，讓我們創建 50 個使用者並為每個用戶建立一個關聯：

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        factory(App\User::class, 50)->create()->each(function($u) {
            $u->posts()->save(factory(App\Post::class)->make());
        });
    }

<a name="calling-additional-seeders"></a>
### 呼叫其他的 Seeders

在 `DatabaseSeeder` 類別，你可以使用 `call` 方法執行其他的 seed 類別。為避免發生單一個 seeder 類別變得壓倒性巨大的情況，使用 `call`方法來將你將資料填充拆分成多個檔案。只需簡單的傳遞你想要運行的 seeder 類別名稱即可：

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Model::unguard();

        $this->call(UsersTableSeeder::class);
        $this->call(PostsTableSeeder::class);
        $this->call(CommentsTableSeeder::class);

        Model::reguard();
    }

<a name="running-seeders"></a>
## 執行資料填充

一旦你撰寫完你的 seeder 類別，可以使用 `db:seed` Artisan 指令來對資料庫進行資料填充。在預設的情況下，`db:seed` 指令將運行 `DatabaseSeeder` 類別，並透過它來呼叫其他的 seed 類別。但是，你也可以使用 `--class` 選項來單獨運行一個特別指定的 seeder 類別：

    php artisan db:seed

    php artisan db:seed --class=UserTableSeeder

你也可以使用 `migrate:refresh` 指令來對資料庫進行資料填充，它會推回並再次執行所有遷移。在完全重建你的資料庫時這個指令是非常有用的：

    php artisan migrate:refresh --seed
