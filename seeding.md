# 数据填充(Database: Seeding)

- [介绍](#introduction)
- [编写填充](#writing-seeders)
    - [使用模型工厂](#using-model-factories)
    - [调用附加填充](#calling-additional-seeders)
- [执行填充](#running-seeders)

<a name="introduction"></a>
## 介绍(Introduction)

Laravel 可以简单的使用 seed 类，填充测试数据到数据库。所有的`seed`类存放在`database/seeds`目录下,可以使用任何你想要的类名称，但是应该遵守某些大小写规范，如 `UserTableSeeder` 等等。默认已经有一个 DatabaseSeeder 类。在这个类里，使用 call 方法执行其他的 seed 类，让你控制填充的顺序。

<a name="writing-seeders"></a>
## 编写填充(Writing Seeders)

想要创建一个 seeder，你得能在 Laravel 根目录下运行[Artisan 命令](/docs/{{version}}/artisan)才可以。所有的 seeder 被框架成功创建后会放在 `database/seeders` 目录下：

    php artisan make:seeder UserTableSeeder

默认的，一个 seeder 类只能包含一个方法：`run`，当你成功运行`db:seed` [Artisan 命令](/docs/{{version}}/artisan)时，这个方法就会被调用了。在 `run` 方法里，你可以插入任何你像要插入的数据到你的数据库
你可以用[query builder](/docs/{{version}}/queries)或[Eloquent model factories](/docs/{{version}}/testing#model-factories)手动的插入数据。
例如，我们修改一个安装 Laravel 时默认会在 `database/seeds/` 目录下包含的`DatabaseSeeder`类，我们来为 `run` 方法添加一个数据库插入声明：

    <?php

    use DB;
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
### 使用模型工厂(Using Model Factories)

当然，手动指定每一个模型的 seed 的属性是很累的，更好的办法是用[模型工厂](/docs/{{version}}/testing#model-factories)来生成大量的数据库记录。
首先，回顾下[模型工厂文档](/docs/{{version}}/testing#model-factories)来学会怎么去定义你自己的工厂。一旦你定义好了你的工厂，你可以利用`factory`帮助函数插入数据到你的数据库。
例如，我们创建50个用户并为每个用户添加一个关系：
For example, let's create 50 users and attach a relationship to each user:

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        factory('App\User', 50)->create()->each(function($u) {
            $u->posts()->save(factory('App\Post')->make());
        });
    }

<a name="calling-additional-seeders"></a>
### 调用附加填充(Calling Additional Seeders)

在 `DatabaseSeeder` 类里面，你可以通过`call` 方法来执行附加的 seed 类。`call`方法允许你将数据库填充 seeder 分开写在不同的文件中，这样就不会出现一个 seeder 文件类文件变的特别大，可以简单的通过 seeder 名称,只运行你想运行的 seeder：

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Model::unguard();

        $this->call(UserTableSeeder::class);
        $this->call(PostsTableSeeder::class);
        $this->call(CommentsTableSeeder::class);
    }

<a name="running-seeders"></a>
## 执行填充(Running Seeders)

当你写好你的填充类(seeder)，你可以通过Artisan命令 `db:seed` 来填充数据到数据库。默认情况下，`db:seed` 命令会执行 `DatabaseSeeder`，可以使用它来调用其他 seed 类，不过，也可以使用 `--class` 参数指定要单独执行的类：

    php artisan db:seed

    php artisan db:seed --class=UserTableSeeder

你也可以使用 `migrate:refresh` 命令填充数据，它会回滚并且再次执行所有迁移，这个命令往往在你彻底重数据库的时候用：

    php artisan migrate:refresh --seed
