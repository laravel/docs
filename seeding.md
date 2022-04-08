# زراعة أو تعبئة قاعدة البيانات

- [المقدمة](#introduction)
- [كتابة الزارعين](#writing-seeders)
    - [استخدام مصانع النموذج](#using-model-factories)
    - [نداء زارعين اضافيين](#calling-additional-seeders)
    - [كتم أحداث الزارعين](#muting-model-events)
- [تشغيل الزارعين](#running-seeders)

<a name="introduction"></a>
## المقدمة 

تتيح لارافل زراعة أو تعبئة قاعدة البيانات عن طريق صفوف الزرع، تتوضع صفوف التعبئة ضمن المجلد `database/seeders` 

افتراضيا تم تعريف الصف `DatabaseSeeder` لنستخدم الطريقة `call` لنداء بقية صفوف التعبئة، 
يسمح لك بالتحكم بأوامر التعبئة

<a name="writing-seeders"></a>
## كتابة الزارعين 

لإنشاء زارع ننفذ الأمر `make:seeder` [Artisan command](/docs/{{version}}/artisan) 

يتوضع الزارعين المنشئين ضمن المجلد `database/seeders` 

```shell
php artisan make:seeder UserSeeder
```


يحتوي صف الزارع افتراضيا على طريقة واحدة `run` تُنفذ هذه الطريقة عند نداء الأمر `db:seed` [Artisan command](/docs/{{version}}/artisan) 

يمكنك إدخال البيانات لقاعدة البيانات ضمن الطريقة `run` 

يمكن إدخال البيانات يدوياً باستخدام [query builder](/docs/{{version}}/queries أو [Eloquent model factories](/docs/{{version}}/database-testing#defining-model-factories) 


في المثال التالي إضافة تعليمة إدخال البيانات لقاعدة البيانات ضمن الطريقة `run`

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


<a name="using-model-factories"></a>
### استخدام مصانع النموذج
تخصيص يدويا واصفات لكل تعبئة نموذج عملية مرهقة

بدلا من ذلك نستخدم [model factories](/docs/{{version}}/database-testing#defining-model-factories) لإنشاء كميات كبيرة من حقول قاعدة البيانات

أولا راجع [model factory documentation](/docs/{{version}}/database-testing#defining-model-factories) لتتعلم كيف تُعرف المصانع

في المثال ننشئ 50 مستخدم لكل مستخدم منشور واحد مرتبط به

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
### نداء زارعين إضافيين


نستخدم الطريقة `call` ضمن الصف `DatabaseSeeder` لتنفيذ صفوف زرع إضافية

يسمح استخدام الطريقة `call` بتقسيم تعبئة قواعد البيانات في عدة ملفات لذلك صف الزرع لا يصبح كبير جداً

تقبل الطريقة `call` مصفوفة من صفوف الزارع التي يجب أن تُنفذ  

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
### كتم أحداث النموذج

لمنع النماذج من إرسال الأحداث عند تشغيل التعبئة نستخدم الميزة `WithoutModelEvents` 


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
## تشغيل الزارعين


لتعبئة قواعد البيانات نستخدم الأمر `db:seed` 

يشغل الأمر `db:seed` الصف  `Database\Seeders\DatabaseSeeder` 

يمكن استخدام الخيار `--class` لتخصيص صف زارع خاص ليعمل بشكل فردي

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

يمكن تعبئة قاعدة البيانات باستخدام الأمر `migrate:fresh` مع الخيار `--seed` 

سوف تحذف كل الجداول وتعيد تشغيل كل الترحيلات

هذا الأمر نافع لإعادة بناء قاعدة البيانات بشكل كامل

```shell
php artisan migrate:fresh --seed
```

<a name="forcing-seeding-production"></a>
#### إجبار الزارعين للتشغيل في الإنتاج

تسبب بعض عمليات التعبئة تعديل أو فقدان البيانات

سوف تقوم بالتلقين للتأكيد قبل تنفيذ الزارعين في بيئة `production` 

لإجبار الزارعين للتشغيل بدون تلقين نستخدم العلم `--force` 

```shell
php artisan db:seed --force
```
