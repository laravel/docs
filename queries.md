# قواعد البيانات: مُنشئ الاستعلام (Query Builder)

- [المقدمة](#introduction)
- [تنفيذ استعلامات قاعدة البيانات](#running-database-queries)
  - [تقسيم النتائج](#chunking-results)
  - [العرض الكسول للنتائج](#streaming-results-lazily)
  - [المجمعات](#aggregates)
- [تحديد البيانات](#select-statements)
- [التعبيرات الصريحة](#raw-expressions)
- [الضم](#joins)
- [الدمج](#unions)
- [جمل where الأساسية](#basic-where-clauses)
  - [جمل Where](#where-clauses)
  - [جمل OrWhere](#or-where-clauses)
  - [جمل JSON Where](#json-where-clauses)
  - [جمل Where إضافية](#additional-where-clauses)
  - [التجميع المنطقي](#logical-grouping)
- [جمل Where المتقدمة](#advanced-where-clauses)
  - [جمل Where Exists](#where-exists-clauses)
  - [جمل Where الفرعية ](#subquery-where-clauses)
  - [جمل Where لكامل النص](#full-text-where-clauses)
- [الترتيب, التجميع, الحد و الإزاحة](#ordering-grouping-limit-and-offset)
  - [الترتيب](#ordering)
  - [التجميع](#grouping)
  - [الحد و الإزاحة](#limit-and-offset)
- [الجمل الشرطية](#conditional-clauses)
- [جمل الإدخال](#insert-statements)
  - [إدخال و تحديث](#upserts)
- [جمل التحديث](#update-statements)
  - [تحديث أعمدة JSON](#updating-json-columns)
  - [الزيادة و الانقاص](#increment-and-decrement)
- [الحذف](#delete-statements)
- [الإقفال المتشائم](#pessimistic-locking)
- [ التشخيص (Debugging)](#debugging)

<a name="introduction"></a>

## المقدمة

يوفر مُنشئ استعلام قاعدة بيانات لارافل (database Query builder) واجهة مريحة وسلسة لإنشاء استعلامات قاعدة البيانات وتنفيذها. يمكن استخدامه لأداء معظم عمليات قاعدة البيانات في تطبيقك ويعمل بشكل مثالي مع جميع أنظمة قواعد البيانات المدعومة من لارافل.

يقوم مُنشئ استعلام لارافل باستخدام ربط المعامل (PDO parameter binding) لحماية تطبيقك من هجمات حقن SQL أو مايعرف ب (SQL injection attacks). لذلك ليست هناك حاجة لتطهير أو تعقيم السلاسل قبل تمريرها إلى مُنشئ الاستعلام كإرتباطات للاستعلام.

> {ملاحظة هامة} لا يدعم PDO ربط أسماء الأعمدة. لذلك ، يجب ألا تسمح أبداً للمستخدم بإدخال أسماء الأعمدة التي تشير إليها الاستعلامات ، بما في ذلك أعمدة "الترتيب حسب" (orderBy).

<a name="running-database-queries"></a>

## تنفيذ استعلامات قاعدة البيانات

<a name="retrieving-all-rows-from-a-table"></a>

#### استرجاع كل الصفوف من الجدول

يمكنك استخدام الطريقة `table` التي توفرها الواجهة `DB` لبدء الاستعلام. يقدم التابع `table` مُنشئ استعلام (Query Builder) سلس ومرن للجدول المحدد ، مما يسمح لك بربط المزيد من القيود بالاستعلام ثم استرداد نتائج الاستعلام في النهاية باستخدام الطريقة `get`:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * عرض قائمة بجميع مستخدمي التطبيق.
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $users = DB::table('users')->get();

            return view('user.index', ['users' => $users]);
        }
    }

يعيد التابع `get` نسخة `Illuminate\Support\Collection` تحتوي على نتائج الاستعلام حيث تكون كل نتيجة عبارة عن نسخة من كائن PHP `stdClass`. يمكنك الوصول إلى قيمة كل عمود من خلال الوصول إلى العمود كخاصية لهذا الكائن:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->get();

    foreach ($users as $user) {
        echo $user->name;
    }

> {معلومة} توفر مجموعات لارافل (Laravel Collections) مجموعة متنوعة من الأساليب الفعالة للغاية لإنشاء خرائط للبيانات وتقليلها. لمزيد من المعلومات حول مجموعات لارافل ، راجع ملف [collection documentation](/docs/{{version}}/collections).

<a name="retrieving-a-single-row-column-from-a-table"></a>

#### استرجاع صف واحد / عمود من جدول

إذا كنت تحتاج إلى استرداد صف واحد فقط من جدول في قاعدة البيانات ، فيمكنك استخدام الطريقة `first` للواجهة` DB`. ستعيد هذه الطريقة كائن `stdClass` واحد:

    $user = DB::table('users')->where('name', 'John')->first();

    return $user->email;

إذا لم تكن بحاجة إلى صف كامل ، فيمكنك استخراج قيمة واحدة من السجل باستخدام الطريقة `value`. ستعيد هذه الطريقة قيمة العمود مباشرة:

    $email = DB::table('users')->where('name', 'John')->value('email');

لاسترداد صف واحد من خلال قيمة عمود المعرف (`id`) ، استخدم الطريقة `find`:

    $user = DB::table('users')->find(3);

<a name="retrieving-a-list-of-column-values"></a>

#### استرداد قائمة بقيم العمود

إذا كنت ترغب باسترداد نسخة `Illuminate\Support\Collection` تحتوي على قيم عمود واحد ، فيمكنك استخدام التابع` pluck`. في هذا المثال ، سنقوم باسترداد مجموعة من عناوين المستخدمين:

    use Illuminate\Support\Facades\DB;

    $titles = DB::table('users')->pluck('title');

    foreach ($titles as $title) {
        echo $title;
    }

يمكنك تحديد العمود الذي يجب أن تستخدمه المجموعة الناتجة كمفاتيح من خلال توفير وسيط ثانٍ للتابع `pluck`:

    $titles = DB::table('users')->pluck('title', 'name');

    foreach ($titles as $name => $title) {
        echo $title;
    }

<a name="chunking-results"></a>

### تقسيم النتائج

إذا كنت بحاجة إلى العمل مع الآلاف من سجلات قاعدة البيانات ، ففكر في استخدام طريقة `chunk` التي توفرها الواجهة `DB`. تسترجع هذه الطريقة جزءاً صغيراً من النتائج في وقت واحد وتضع كل جزء في إغلاق (closure) للمعالجة. على سبيل المثال ، دعنا نسترد جدول `users` بأكمله في أجزاء من 100 سجل في المرة الواحدة:

    use Illuminate\Support\Facades\DB;

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        foreach ($users as $user) {
            //
        }
    });

يمكنك إيقاف معالجة المزيد من الأجزاء عن طريق إرجاع `false` من الإغلاق (closure):

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        // معالجة السجلات...

        return false;
    });

إذا كنت تقوم بتحديث سجلات قاعدة البيانات أثناء تقسيم النتائج ، فقد تتغير نتائجك الجماعية بطرق غير متوقعة. لذلك إذا كنت تخطط لتحديث السجلات المستردة أثناء التقسيم ، فمن الأفضل دائماً استخدام الطريقة `chunkById`. ستعمل هذه الطريقة على ترقيم النتائج تلقائياً بناءً على المفتاح الأساسي للسجل:

    DB::table('users')->where('active', false)
        ->chunkById(100, function ($users) {
            foreach ($users as $user) {
                DB::table('users')
                    ->where('id', $user->id)
                    ->update(['active' => true]);
            }
        });

> {ملاحظة} عند تحديث أو حذف السجلات أثناء تقسيم النتائج، يمكن أن تؤثر أي تغييرات على المفتاح الأساسي أو المفاتيح الأجنبية على الاستعلام المتقطع (chunk query). مما قد يؤدي إلى عدم تضمين السجلات في النتائج المقسمة.

<a name="streaming-results-lazily"></a>

### العرض الكسول للنتائج

تعمل طريقة `lazy` بشكل مشابه للطريقة [`chunk`](#chunking-results) بمعنى أنه ينفذ الاستعلام في أجزاء. ومع ذلك ، بدلاً من تمرير كل جزء إلى استرجاع (Callback)(Callback هو الكود الذي يتم تنفيذه ضمن وسيط لتابع آخر)، فإن الطريقة `()lazy` ترجع [`LazyCollection`](/docs/{{version}}/collections#lazy-collections), مما يتيح لك التفاعل مع النتائج دفعة واحدة:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

كما هو الحال مع `chunk` ، إذا كنت تخطط لتحديث السجلات المستردة أثناء الدوران عليها ، فمن الأفضل استخدام التابعين `lazyById` أو` lazyByIdDesc`. ستقوم هذه الطرق تلقائياً بترقيم النتائج بناءً على المفتاح الأساسي للسجل:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> {ملاحظة} عند تحديث السجلات أو حذفها أثناء الدوران عليها ، يمكن أن تؤثر أي تغييرات على المفتاح الأساسي أو المفاتيح الأجنبية على الاستعلام المتقطع (chunk query). من المحتمل أن يؤدي هذا إلى عدم تضمين بعض السجلات في النتائج.

<a name="aggregates"></a>

### المجمعات (Aggregates)

يوفر مُنشئ الاستعلامات (Query builder) أيضاً مجموعة متنوعة من الطرق لاسترداد القيم الإجمالية مثل `count` , `max` , `min` , `avg` , `sum`. يمكنك استدعاء أي من هذه التوابع بعد إنشاء استعلامك:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->count();

    $price = DB::table('orders')->max('price');

بالطبع ، يمكنك دمج هذه الطرق مع جمل أخرى لضبط كيفية حساب القيمة الإجمالية:

    $price = DB::table('orders')
                    ->where('finalized', 1)
                    ->avg('price');

<a name="determining-if-records-exist"></a>

#### تحديد ما إذا كانت السجلات موجودة

بدلاً من استخدام طريقة `count` لتحديد ما إذا كانت هناك أية سجلات تطابق قيود الاستعلام ، يمكنك استخدام الطريقتين `exists` و `doesntExist`:

    if (DB::table('orders')->where('finalized', 1)->exists()) {
        // ...
    }

    if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
        // ...
    }

<a name="select-statements"></a>

## التحديد Select

<a name="specifying-a-select-clause"></a>

#### وصف جملة select

قد لا ترغب دائماً في تحديد جميع الأعمدة من جدول قاعدة البيانات. باستخدام الطريقة `select` ، يمكنك تخصيص الاستعلام لارجاع أعمدة محددة:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->select('name', 'email as user_email')
                ->get();

تسمح لك الطريقة `distinct` بجعل الاستعلام يجلب البيانات بدون تكرار:

    $users = DB::table('users')->distinct()->get();

إذا كان لديك استعلام منشىء مسبقاً وترغب في إضافة عمود إلى جملة `select` الموجودة به ، فيمكنك استخدام طريقة `addSelect`:

    $query = DB::table('users')->select('name');

    $users = $query->addSelect('age')->get();

<a name="raw-expressions"></a>

## التعبيرات الصريحة

قد تحتاج أحياناً إلى إدخال جملة ما في استعلام لإنشاء تعبير صريح ، للقيام بذلك يمكنك استخدام التابع `raw` الذي توفره الواجهة` DB`:

    $users = DB::table('users')
                 ->select(DB::raw('count(*) as user_count, status'))
                 ->where('status', '<>', 1)
                 ->groupBy('status')
                 ->get();

> {ملاحطة} سيتم إدخال الجمل الصريحة في الاستعلام كسلاسل بدون تطهير. لذلك يجب أن تكون حذراً للغاية لتجنب إنشاء ثغرات أمنية تسمح بهجمات (SQL injection).

<a name="raw-methods"></a>

### الطرق الصريحة

بدلاً من استخدام طريقة `DB::raw` ، يمكنك أيضاً استخدام الطرق التالية لإدراج تعبير صريح في أجزاء مختلفة من استعلامك. ** تذكر أن لارافل لا يضمن أن يكون أي استعلام يستخدم التعبيرات الصريحة محمي ضد ثغرات حقن SQL. **

<a name="selectraw"></a>

#### الطريقة `selectRaw`

يمكن استخدام الطريقة `selectRaw` بدلاً من `addSelect(DB::raw(...))`. يقبل هذا التابع مصفوفة اختيارية من القيم كوسيط ثاني لها:

    $orders = DB::table('orders')
                    ->selectRaw('price * ? as price_with_tax', [1.0825])
                    ->get();

<a name="whereraw-orwhereraw"></a>

#### الطرق `whereRaw / orWhereRaw`

يمكن استخدام الطرق `whereRaw` و `orWhereRaw` لإدخال جملة` where` الصريحة في استعلامك. تقبل هذه التوابع مصفوفة اختيارية من القيم كوسيط ثاني لها:

    $orders = DB::table('orders')
                    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                    ->get();

<a name="havingraw-orhavingraw"></a>

#### الطرق `havingRaw / orHavingRaw`

يمكن استخدام التابعين `havingRaw` و `orHavingRaw` لتقديم جملة صريحة كقيمة لجملة `having`. تقبل هذه التوابع مصفوفة اختيارية من القيم كوسيط ثاني لها:

    $orders = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > ?', [2500])
                    ->get();

<a name="orderbyraw"></a>

#### الطريقة `orderByRaw`

يمكن استخدام طريقة `orderByRaw` لتقديم جملة صريحة كقيمة لجملة `order by`:

    $orders = DB::table('orders')
                    ->orderByRaw('updated_at - created_at DESC')
                    ->get();

<a name="groupbyraw"></a>

### الطريقة `groupByRaw`

يمكن استخدام طريقة `groupByRaw` لتقديم جملة صريحة كقيمة لجملة `group by`:

    $orders = DB::table('orders')
                    ->select('city', 'state')
                    ->groupByRaw('city, state')
                    ->get();

<a name="joins"></a>

## الضم (Joins)

<a name="inner-join-clause"></a>

#### الضم الداخلي (Inner Join)

يمكن أيضاً استخدام مُنشئ الاستعلام (Query builder) لإضافة جمل الضم إلى استعلاماتك. لإجراء الضم الداخلي الأساسي، يمكنك استخدام التابع `Join` في مُنشئ الاستعلام. حيث المعامل الأول االذي يتم تمريره إلى الطريقة `Join` هو اسم الجدول الذي تريد الضم إليه ، بينما تحدد الوسائط المتبقية قيود العمود الخاصة بالضم. يمكنك ضم جداول متعددة في استعلام واحد:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->join('contacts', 'users.id', '=', 'contacts.user_id')
                ->join('orders', 'users.id', '=', 'orders.user_id')
                ->select('users.*', 'contacts.phone', 'orders.price')
                ->get();

<a name="left-join-right-join-clause"></a>

#### الضم اليساري والضم اليميني

إذا كنت ترغب في إجراء الضم اليميني "right join" أو الضم اليساري "left join" بدلاً من الضم الداخلي "inner join" ، فاستخدم أساليب `leftJoin` أو `rightJoin`. هذه التوابع لها نفس وسائط الطريقة `join`:

    $users = DB::table('users')
                ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

    $users = DB::table('users')
                ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

<a name="cross-join-clause"></a>

#### الضم المتقاطع

يمكنك استخدام طريقة `crossJoin` لأداء الضم المتقاطع "cross join". تؤدي هذه الطريقة لإنشاء نتيجة ديكارتيّة (تضم جميع عناصر الجدولين) بين الجدول الأول والجدول المضموم:

    $sizes = DB::table('sizes')
                ->crossJoin('colors')
                ->get();

<a name="advanced-join-clauses"></a>

#### جمل الضم المتقدمة

يمكنك أيضاً تحديد شروط ضم أكثر تقدماً. للبدء ، مرر إغلاقاً (closure) كوسيط ثاني لطريقة `join`. سيتلقى الإغلاق(closure) نسخة من `Illuminate\Database\Query\JoinClause` والتي تسمح لك بتحديد قيود على جملة `join`:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')->orOn(...);
            })
            ->get();

إذا كنت ترغب في استخدام جملة "where" في جمل الضم الخاصة بك ، فيمكنك استخدام التابعين `where` و `orWhere` المقدمين من الغرض `JoinClause`. بدلاً من مقارنة عمودين ، ستقارن هذه التوابع العمود بقيمة محددة:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')
                     ->where('contacts.user_id', '>', 5);
            })
            ->get();

<a name="subquery-joins"></a>

#### الضم الفرعي

يمكنك استخدام أساليب `JoinSub` و `leftJoinSub` و `rightJoinSub` لربط استعلام باستعلام فرعي. تتلقى كل من هذه الطرق ثلاث وسائط: الاستعلام الفرعي والاسم المستعار للجدول الخاص به والإغلاق (closure) الذي يحدد الأعمدة ذات الصلة. في هذا المثال ، سنقوم باسترداد مجموعة من المستخدمين حيث يحتوي كل سجل مستخدم على الطابع الزمني `created_at` لآخر مشاركة مدونة نشرها المستخدم:

    $latestPosts = DB::table('posts')
                       ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                       ->where('is_published', true)
                       ->groupBy('user_id');

    $users = DB::table('users')
            ->joinSub($latestPosts, 'latest_posts', function ($join) {
                $join->on('users.id', '=', 'latest_posts.user_id');
            })->get();

<a name="unions"></a>

## الدمج (Unions)

يوفر مُنشئ الاستعلام أيضاً طريقة مناسبة لدمج استعلامين أو أكثر معاً. على سبيل المثال ، يمكنك إنشاء استعلام أولي واستخدام التابع `union` لربطه بمزيد من الاستعلامات:

    use Illuminate\Support\Facades\DB;

    $first = DB::table('users')
                ->whereNull('first_name');

    $users = DB::table('users')
                ->whereNull('last_name')
                ->union($first)
                ->get();

بالإضافة إلى طريقة `union` ، يوفر مُنشئ الاستعلام طريقة `unionAll`. في هذه الطريقة لا تتم إزالة النتائج المكررة للاستعلامات التي تم دمجها. له نفس وسائط الطريقة `union`.

<a name="basic-where-clauses"></a>

## جمل where الأساسية

<a name="where-clauses"></a>

### جمل Where

يمكنك استخدام الطريقة `where` لإضافة جمل "where" إلى الاستعلام. يتطلب الاستدعاء الأساسي للطريقة `where` ثلاث وسائط. المعامل الأول هو اسم العمود. المعامل الثاني هو المعامل الرياضي ، والذي يمكن أن يكون أياً من العوامل الرياضية المدعومة من قاعدة البيانات. المعامل الثالث هو القيمة المطلوب مقارنتها بقيمة العمود.

على سبيل المثال ، يقوم طلب البحث التالي بإرجاع المستخدمين بحيث تكون قيمة العمود `votes` مساوية لـ `100` وقيمة العمود `age` أكبر من `35` ضمن السجل الخاص بكل مستخدم:

    $users = DB::table('users')
                    ->where('votes', '=', 100)
                    ->where('age', '>', 35)
                    ->get();

للسهولة ، إذا كنت تريد التحقق من أن العمود يساوي `=` قيمة معينة ، فيمكنك تمرير القيمة كمتغير ثانٍ إلى طريقة `where`. سيفترض لارافل أنك تريد استخدام المعامل `=` أي إن المعامل `=` هو المعامل الافتراضي للطريقة "where" في حال عدم تمرير أي معامل:

    $users = DB::table('users')->where('votes', 100)->get();

كما ذكرنا سابقاً ، يمكنك استخدام أي معامل يدعمه نظام قاعدة البيانات الخاص بك:

    $users = DB::table('users')
                    ->where('votes', '>=', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('votes', '<>', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('name', 'like', 'T%')
                    ->get();

يمكنك أيضاً تمرير مصفوفة من الشروط إلى الطريقة `where`. يجب أن يكون كل عنصر في المصفوفة هو مصفوفة تحتوي على الوسائط الثلاثة التي يتم تمريرها عادةً للطريقة `where`:

    $users = DB::table('users')->where([
        ['status', '=', '1'],
        ['subscribed', '<>', '1'],
    ])->get();

> {ملاحظة} لا يدعم PDO ربط أسماء الأعمدة (binding column names). لذلك ، يجب ألا تسمح للمستخدم بإدخال أسماء الأعمدة التي تشير إليها طلبات البحث ، بما في ذلك الأعمدة الخاصة بترتيب النتائج `order by`.

<a name="or-where-clauses"></a>

### جمل Or Where

عند ربط الاستدعاءات معاً بطريقة "where"، يتم ضم جمل "where" معاً باستخدام المعامل `and`. ومع ذلك ، يمكنك استخدام التابع `orWhere` لربط الاستعلامين باستخدام المعامل `or`. يقبل أسلوب `orWhere` نفس الوسائط مثل طريقة` where`:

    $users = DB::table('users')
                        ->where('votes', '>', 100)
                        ->orWhere('name', 'John')
                        ->get();

إذا كنت بحاجة إلى تجميع شرط `or` داخل أقواس ، فيمكنك تمرير إغلاق(closure) كوسيط أول للتابع `orWhere`:

    $users = DB::table('users')
                ->where('votes', '>', 100)
                ->orWhere(function($query) {
                    $query->where('name', 'Abigail')
                          ->where('votes', '>', 50);
                })
                ->get();

المثال أعلاه سيُنتج استعلام SQL التالي:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> {ملاحظة} يجب عليك دائماً تجميع استدعاءات `orWhere` لتجنب السلوك غير المتوقع عند تطبيق النطاقات العامة (global scopes).

<a name="json-where-clauses"></a>

### جمل JSON Where

يدعم لارافل أيضاً الاستعلام عن الأعمدة التي تكون من نوع JSON في قواعد البيانات التي توفر دعماً لأنواع أعمدة JSON. حالياً ، يتضمن هذا MySQL 5.7+ و PostgreSQL و SQL Server 2016 و SQLite 3.9.0 (مع [extension JSON1](https://www.sqlite.org/json1.html)). للاستعلام عن عمود JSON ، استخدم معامل التشغيل `<-`:

    $users = DB::table('users')
                    ->where('preferences->dining->meal', 'salad')
                    ->get();

يمكنك استخدام `whereJsonContains` للاستعلام عن مصفوفات JSON. لا تدعم قاعدة بيانات SQLite هذه الميزة:

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', 'en')
                    ->get();

إذا كان تطبيقك يستخدم قواعد بيانات MySQL أو PostgreSQL ، فيمكنك تمرير مجموعة من القيم للتابع `whereJsonContains`:

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', ['en', 'de'])
                    ->get();

يمكنك استخدام التابع `whereJsonLength` للاستعلام عن مصفوفات JSON حسب طولها:

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', 0)
                    ->get();

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', '>', 1)
                    ->get();

<a name="additional-where-clauses"></a>

### جمل Where إضافية

الطريقتين **whereBetween / orWhereBetween**

تتحقق الطريقة `whereBetween` من أن قيمة العمود تقع بين قيمتين:

    $users = DB::table('users')
               ->whereBetween('votes', [1, 100])
               ->get();

الطريقتين **whereNotBetween / orWhereNotBetween**

تتحقق الطريقة `whereNotBetween` من أن قيمة العمود تقع خارج مجال قيمتين:

    $users = DB::table('users')
                        ->whereNotBetween('votes', [1, 100])
                        ->get();

الطرق **whereIn / whereNotIn / orWhereIn / orWhereNotIn**

تتحقق الطريقة `whereIn` من أن قيمة عمود محدد موجودة ضمن قيم مصفوفة محددة:

    $users = DB::table('users')
                        ->whereIn('id', [1, 2, 3])
                        ->get();

تتحقق الطريقة `whereNotIn` من أن قيمة عمود محدد غير موجودة ضمن قيم مصفوفة محددة:

    $users = DB::table('users')
                        ->whereNotIn('id', [1, 2, 3])
                        ->get();

> {ملاحظة} إذا كنت تضيف مصفوفة كبيرة من روابط الأعداد الصحيحة إلى استعلامك ، فيمكن استخدام الطرق `whereIntegerInRaw` أو `whereIntegerNotInRaw` لتقليل استخدام الذاكرة بشكل كبير.

الطرق **whereNull / whereNotNull / orWhereNull / orWhereNotNull**

تتحقق الطريقة `whereNull` من أن قيمة العمود المحدد هي` NULL`:

    $users = DB::table('users')
                    ->whereNull('updated_at')
                    ->get();

تتحقق الطريقة `whereNotNull` من أن قيمة العمود ليست` NULL`:

    $users = DB::table('users')
                    ->whereNotNull('updated_at')
                    ->get();

الطرق **whereDate / whereMonth / whereDay / whereYear / whereTime**

يمكن استخدام الطريقة `whereDate` لمقارنة قيمة العمود بتاريخ:

    $users = DB::table('users')
                    ->whereDate('created_at', '2016-12-31')
                    ->get();

يمكن استخدام الطريقة `whereMonth` لمقارنة قيمة العمود بشهر معين:

    $users = DB::table('users')
                    ->whereMonth('created_at', '12')
                    ->get();

يمكن استخدام الطريقة `whereDay` لمقارنة قيمة العمود بيوم معين من الشهر:

    $users = DB::table('users')
                    ->whereDay('created_at', '31')
                    ->get();

يمكن استخدام الطريقة `whereYear` لمقارنة قيمة العمود بسنة معينة:

    $users = DB::table('users')
                    ->whereYear('created_at', '2016')
                    ->get();

يمكن استخدام الطريقة `whereTime` لمقارنة قيمة العمود بوقت محدد:

    $users = DB::table('users')
                    ->whereTime('created_at', '=', '11:20:45')
                    ->get();

الطريقتين **whereColumn / orWhereColumn**

يمكن استخدام التابع `whereColumn` للتحقق من تساوي عمودين:

    $users = DB::table('users')
                    ->whereColumn('first_name', 'last_name')
                    ->get();

يمكنك أيضاً تمرير عامل مقارنة إلى الطريقة `whereColumn`:

    $users = DB::table('users')
                    ->whereColumn('updated_at', '>', 'created_at')
                    ->get();

يمكنك أيضاً تمرير مصفوفة من مقارنات الأعمدة إلى الطريقة `whereColumn`. سيتم ضم هذه الشروط باستخدام المعامل `and`:

    $users = DB::table('users')
                    ->whereColumn([
                        ['first_name', '=', 'last_name'],
                        ['updated_at', '>', 'created_at'],
                    ])->get();

<a name="logical-grouping"></a>

### التجميع المنطقي

قد تحتاج أحياناً إلى تجميع عدة جمل "where" داخل أقواس من أجل تحقيق التجميع المنطقي المطلوب للاستعلام. في الواقع ، يجب عليك دائماً تجميع الاستدعاءات بالطريقة `orWhere` بين قوسين لتجنب سلوك غير متوقع للاستعلام. لتحقيق ذلك ، يمكنك تمرير إغلاق(closure) للطريقة `where`:

    $users = DB::table('users')
               ->where('name', '=', 'John')
               ->where(function ($query) {
                   $query->where('votes', '>', 100)
                         ->orWhere('title', '=', 'Admin');
               })
               ->get();

كما ترى ، فإن تمرير إغلاق في طريقة `where` يوجه مُنشئ الاستعلام(Query builder) لبدء مجموعة قيود. سيتلقى الإغلاق كوسيط له نسخة عن مُنشئ الاستعلام يمكنك استخدامه لتعيين القيود التي يجب تضمينها داخل مجموعة الأقواس. المثال أعلاه سينتج جملة SQL التالية:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> {ملاحظة} يجب عليك دائماً تجميع استدعاءات "orWhere" لتجنب السلوك غير المتوقع عند تطبيق النطاقات العامة (global scopes).

<a name="advanced-where-clauses"></a>

### جمل Where المتقدمة

<a name="where-exists-clauses"></a>

### جملة Where Exists

تسمح لك الطريقة `whereExists` بكتابة جمل "where exists" الموجودة في لغة SQL. تقبل الطريقة `whereExists` إغلاقاً (closure) يتلقى كوسيط له نسخة عن مُنشئ الاستعلام ، مما يسمح لك بتعريف الاستعلام الذي يجب وضعه داخل جملة"exists":

    $users = DB::table('users')
               ->whereExists(function ($query) {
                   $query->select(DB::raw(1))
                         ->from('orders')
                         ->whereColumn('orders.user_id', 'users.id');
               })
               ->get();

سينتج الاستعلام أعلاه جملة SQL التالية:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>

### جمل where الفرعية

قد تحتاج في بعض الأحيان إلى إنشاء جملة "where" التي تقارن نتائج استعلام فرعي بقيمة معينة. يمكنك تحقيق ذلك بتمرير إغلاق(closure) وقيمة إلى الطريقة `where`. على سبيل المثال، سيقوم الاستعلام التالي باسترداد جميع المستخدمين الذين لديهم "membership" حديثة من نوع (Pro):

    use App\Models\User;

    $users = User::where(function ($query) {
        $query->select('type')
            ->from('membership')
            ->whereColumn('membership.user_id', 'users.id')
            ->orderByDesc('membership.start_date')
            ->limit(1);
    }, 'Pro')->get();

أو قد تحتاج إلى إنشاء جملة "where" تقارن عموداً بنتائج استعلام فرعي. يمكنك تحقيق ذلك بتمرير اسم العمود ومعامل المقارنة وإغلاق إلى طريقة `where`. على سبيل المثال ، سيقوم الاستعلام التالي باسترداد جميع سجلات الدخل حيث يكون المبلغ أقل من المتوسط ؛

    use App\Models\Income;

    $incomes = Income::where('amount', '<', function ($query) {
        $query->selectRaw('avg(i.amount)')->from('incomes as i');
    })->get();

<a name="full-text-where-clauses"></a>

### جمل Where لكامل النص

> {ملاحظة} الطرق `whereFullText` و `orWhereFullText` مدعومة من MySQL و PostgreSQL حالياً.

يمكن استخدام الطريقتين `whereFullText` و `orWhereFullText` لإضافة جمل "Full text where" إلى طلب البحث للأعمدة التي لديها [full text indexes](/docs/{{version}}/migrations#available-index-types). سيتم تحويل هذه التوابع إلى جملة SQL المناسبة لنظام قاعدة البيانات الأساسي بواسطة لارافل. على سبيل المثال ، سيتم إنشاء جملة `MATCH AGAINST` للتطبيقات التي تستخدم MySQL:

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

<a name="ordering-grouping-limit-and-offset"></a>

## الترتيب, التجميع, الحد و الإزاحة

<a name="ordering"></a>

### الترتيب

<a name="orderby"></a>

#### الطريقة `orderBy`

تسمح لك الطريقة `orderBy` بفرز نتائج الاستعلام حسب عمود معين. يجب أن يكون الوسيط الأول الذي تقبله الطريقة `orderBy` هو العمود الذي تريد الفرز وفقاً له ، بينما يحدد الوسيط الثاني اتجاه الفرز وقد يكون إما تصاعدي `asc` أو تنازلي `desc`:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

للفرز حسب عدة أعمدة ، يمكنك ببساطة استدعاء `orderBy` عدة مرات حسب الضرورة:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->orderBy('email', 'asc')
                    ->get();

<a name="latest-oldest"></a>

#### الطرق `latest` & `oldest`

تسمح لك الطريقتان `latest` و `oldest` بطلب النتائج حسب التاريخ بسهولة. بشكل افتراضي ، سيتم ترتيب النتيجة حسب عمود الجدول "created_at". أو يمكنك تمرير اسم العمود الذي ترغب بالفرز بواسطته:

    $user = DB::table('users')
                    ->latest()
                    ->first();

<a name="random-ordering"></a>

#### الترتيب العشوائي

يمكن استخدام الطريقة `inRandomOrder` لفرز نتائج الاستعلام عشوائياً. على سبيل المثال ، يمكنك استخدام هذا التابع لجلب مستخدم عشوائي:

    $randomUser = DB::table('users')
                    ->inRandomOrder()
                    ->first();

<a name="removing-existing-orderings"></a>

#### إزالة الترتيب المسبق

تزيل الطريقة `reorder` جميع جمل "order by" التي تم تطبيقها مسبقاً على الاستعلام:

    $query = DB::table('users')->orderBy('name');

    $unorderedUsers = $query->reorder()->get();

يمكنك تمرير عمود محدد واتجاه ترتيب تصاعدي(asc) أو تنازلي (desc) عند استدعاء التابع `reorder` لإزالة كل جمل "order by" الحالية وتطبيق ترتيب جديد تماماً على الاستعلام:

    $query = DB::table('users')->orderBy('name');

    $usersOrderedByEmail = $query->reorder('email', 'desc')->get();

<a name="grouping"></a>

### التجميع

<a name="groupby-having"></a>

#### الطرق `groupBy` & `having`

كما قد تتوقع ، يمكن استخدام الطريقتين `groupBy` و `having` لتجميع نتائج الاستعلام. وسائط الطريقة `having` مشابهة لوسائط الطريقة `where`:

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

يمكنك استخدام الطريقة `havingBetween` لتصفية النتائج ضمن مجال معين:

    $report = DB::table('orders')
                    ->selectRaw('count(id) as number_of_orders, customer_id')
                    ->groupBy('customer_id')
                    ->havingBetween('number_of_orders', [5, 15])
                    ->get();

يمكنك تمرير عدة متغيرات للتابع `groupBy` للتجميع حسب عدة أعمدة:

    $users = DB::table('users')
                    ->groupBy('first_name', 'status')
                    ->having('account_id', '>', 100)
                    ->get();

لإنشاء جمل `having` أكثر تقدماً ، راجع طريقة [`havingRaw`](#raw-methods).

<a name="limit-and-offset"></a>

### الحد والإزاحة

<a name="skip-take"></a>

#### الطرق `skip` & `take`

يمكنك استخدام الطريقتين `skip` و `take` للحد من عدد النتائج التي يتم إرجاعها من الاستعلام أو لتخطي عدد معين من النتائج في الاستعلام:

    $users = DB::table('users')->skip(10)->take(5)->get();

بدلاً من ذلك ، يمكنك استخدام الطريقتين `Limit` و `Offset`. هاتان الطريقتان مكافئتان وظيفياً للطريقتين `take` و `skip` ، على التوالي:

    $users = DB::table('users')
                    ->offset(10)
                    ->limit(5)
                    ->get();

<a name="conditional-clauses"></a>

## الجمل الشرطية

قد ترغب أحياناً في تطبيق جمل استعلام معينة على إحدى الاستعلامات بناءً على شرط ما. على سبيل المثال ، قد ترغب في تطبيق جملة `where` فقط إذا كانت هناك قيمة إدخال معينة موجودة في طلب HTTP الوارد. يمكنك القيام بذلك باستخدام الطريقة `when`:

    $role = $request->input('role');

    $users = DB::table('users')
                    ->when($role, function ($query, $role) {
                        return $query->where('role_id', $role);
                    })
                    ->get();

لا تنفذ الطريقة `when` الإغلاق (closure) المحدد إلا عندما يكون تقييم المعامل الأول `true`. أما إذا كان تقييمه `false` ، فلن يتم تنفيذ الإغلاق. لذلك ، في المثال أعلاه ، سيتم استدعاء الإغلاق المعطى للطريقة `when` فقط إذا كان حقل `role` موجوداً في الطلب الوارد وتقييمه `true`.

يمكنك تمرير إغلاق آخر كمعامل ثالث للتابع `when`. لن يتم تنفيذ هذا الإغلاق إلا إذا تم تقييم المعامل الأول على أنه `false`.<br>
أي إنه عندما يكون تقييم المعامل الأول `true` سيتم تنفيذ الإغلاق الأول, وإذا كان تقييم المعامل الأول `false` سيتم تنفيذ الإغلاق الثاني.<br>
لتوضيح كيفية استخدام هذه الميزة ، سنستخدمها لتكوين الترتيب الافتراضي للاستعلام:

    $sortByVotes = $request->input('sort_by_votes');

    $users = DB::table('users')
                    ->when($sortByVotes, function ($query, $sortByVotes) {
                        return $query->orderBy('votes');
                    }, function ($query) {
                        return $query->orderBy('name');
                    })
                    ->get();

<a name="insert-statements"></a>

## جمل الإدخال

يوفر مُنشئ الاستعلام (Query builder) أيضاً الطريقة `insert` يمكن استخدامها لإدراج السجلات في جدول قاعدة البيانات. تقبل الطريقة `insert` مصفوفة من أسماء الأعمدة والقيم:

    DB::table('users')->insert([
        'email' => 'kayla@example.com',
        'votes' => 0
    ]);

يمكنك إدراج عدة سجلات مرة واحدة عن طريق تمرير مصفوفة من المصفوفات. تمثل كل مصفوفة سجلاً تريد إدراجه في الجدول:

    DB::table('users')->insert([
        ['email' => 'picard@example.com', 'votes' => 0],
        ['email' => 'janeway@example.com', 'votes' => 0],
    ]);

الطريقة `insertOrIgnore` تتجاهل الأخطاء أثناء إدراج السجلات في قاعدة البيانات:

    DB::table('users')->insertOrIgnore([
        ['id' => 1, 'email' => 'sisko@example.com'],
        ['id' => 2, 'email' => 'archer@example.com'],
    ]);

> {ملاحظة} ستتجاهل الطريقة `insertOrIgnore` السجلات المكررة وقد تتجاهل أيضاً الأنواع الأخرى من الأخطاء اعتماداً على محرك قاعدة البيانات. على سبيل المثال ، "insertOrIgnore` سوف [يتجاوز الوضع الصارم لـ MySQL](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution).

<a name="auto-incrementing-ids"></a>

#### المعرّفات ذات الزيادة التلقائية

إذا كان الجدول يحتوي على معرّف (ID) يتزايد تلقائياً ، فاستخدم الطريقة `insertGetId` لإدراج سجل ثم استرداد المعرّف:

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

> {ملاحظة} عند استخدام PostgreSQL ، تتوقع طريقة `insertGetId` تسمية عمود الزيادة التلقائية باسم` id`. إذا كنت ترغب في استرداد المعرف من سلسلة مختلفة ، فيمكنك تمرير اسم العمود كمعامل ثاني إلى طريقة `insertGetId`.

<a name="upserts"></a>

### الادخال و التعديل

ستقوم الطريقة `upsert` بإدراج السجلات غير الموجودة وتحديث السجلات الموجودة بالفعل بقيم جديدة تحددها أنت. يتكون المعامل الأول للطريقة من القيم المراد إدراجها أو تحديثها ، بينما يحدد المعامل الثاني العمود (أو الأعمدة) التي تحدد السجلات بشكل فريد ضمن الجدول المرتبط. المعامل الثالث والأخير للطريقة `upsert` عبارة عن مصفوفة من الأعمدة التي يجب تحديثها إذا كان السجل المطابق موجوداً بالفعل في قاعدة البيانات:

    DB::table('flights')->upsert([
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ], ['departure', 'destination'], ['price']);

في المثال أعلاه ، سيحاول لارافل إدخال سجلين. إذا كان السجل موجوداً بالفعل بنفس قيم العمودين `departure` و `destination` ، فسيحدّث لارافل عمود `price` في ذلك السجل.

> {ملاحظة} تتطلب جميع قواعد البيانات باستثناء SQL Server أن يكون للأعمدة الموجودة في المعامل الثاني للطريقة `upsert` فهرس أساسي "primary" أو فريد "unique". بالإضافة إلى ذلك ، يتجاهل مشغل قاعدة بيانات MySQL المعامل الثاني لطريقة `upsert` ويستخدم دائماً الفهارس الأولية والفريدة للجدول لاكتشاف السجلات الموجودة.

<a name="update-statements"></a>

## التحديث

بالإضافة إلى إدراج السجلات في قاعدة البيانات ، يمكن لمُنشئ الاستعلام (Query builder) أيضاً تحديث السجلات الموجودة باستخدام الطريقة `update`. تقبل الطريقة `update` ، مثل الطريقة `insert` مصفوفة من أزواج الأعمدة والقيم التي تشير إلى الأعمدة المراد تحديثها. تعرض الطريقة `update` عدد الصفوف المتأثرة. يمكنك تقييد استعلام `update` باستخدام جمل `where`:

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['votes' => 1]);

<a name="update-or-insert"></a>

#### التحديث أو الإدخال

قد ترغب أحياناً في تحديث سجل موجود في قاعدة البيانات أو إنشائه في حالة عدم وجود سجل مطابق. في هذا السيناريو ، يمكن استخدام الطريقة `updateOrInsert`. تقبل الطريقة `updateOrInsert` وسيطين: مصفوفة من الشروط يمكن من خلالها العثور على السجل ، ومصفوفة من أزواج الأعمدة والقيم التي تشير إلى الأعمدة المراد تحديثها.

ستحاول الطريقة `updateOrInsert` تحديد موقع سجل قاعدة بيانات مطابق باستخدام أزواج العمود و القيمة المحددة في المعامل الأول. إذا كان السجل موجوداً , فسيتم تحديثه بالقيم الموجودة في المعامل الثاني. إذا تعذر العثور على السجل ، فسيتم إدراج سجل جديد بالسمات المدمجة لكل من المعاملين:

    DB::table('users')
        ->updateOrInsert(
            ['email' => 'john@example.com', 'name' => 'John'],
            ['votes' => '2']
        );

<a name="updating-json-columns"></a>

### تحديث أعمدة JSON

عند تحديث عمود JSON ، يجب استخدام `<-` لتحديث المفتاح المناسب في كائن JSON. هذه العملية مدعومة في MySQL 5.7+ و PostgreSQL 9.5+:

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['options->enabled' => true]);

<a name="increment-and-decrement"></a>

### الزيادة و الانقاص

يوفر مُنشئ الاستعلام (Query builder) أيضاً طرقاً ملائمة لزيادة أو إنقاص قيمة عمود معين. تقبل كلتا الطريقتين وسيط واحد على الأقل وهي العمود المراد تعديله. يمكن تقديم وسيط ثاني لتحديد المقدار الذي يجب زيادة العمود به أو إنقاصه:

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

يمكنك أيضاً تحديد أعمدة إضافية لتحديثها أثناء العملية:

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="delete-statements"></a>

## الحذف

يمكن استخدام الطريقة `delete` في مُنشئ الاستعلام (Query builder) لحذف السجلات من الجدول. تعرض الطريقة `delete` عدد الصفوف المتأثرة. يمكنك تقييد جمل `delete` بإضافة جمل `where` قبل استدعاء الطريقة `delete`:

    $deleted = DB::table('users')->delete();

    $deleted = DB::table('users')->where('votes', '>', 100)->delete();

إذا كنت ترغب في اقتطاع جدول بأكمله ، مما سيؤدي إلى إزالة جميع السجلات من الجدول وإعادة تعيين معرف التزايد التلقائي إلى الصفر ، فيمكنك استخدام طريقة `truncate`:

    DB::table('users')->truncate();

<a name="table-truncation-and-postgresql"></a>

#### اقتطاع جدول في PostgreSQL

عند اقتطاع قاعدة بيانات PostgreSQL ، سيتم تطبيق السلوك `CASCADE`. هذا يعني أنه سيتم حذف جميع السجلات ذات الصلة بالمفتاح الأجنبي(foreign key) في الجداول الأخرى أيضاً.

<a name="pessimistic-locking"></a>

## القفل التشاؤمي (Pessimistic Locking)

يتضمن مُنشئ الاستعلام أيضاً بعض الوظائف لمساعدتك على تحقيق "القفل التشاؤمي" عند تنفيذ جمل `select`. لتنفيذ جملة باستخدام "قفل مشترك" (shared lock) ، يمكنك استدعاء طريقة `sharedLock`. يمنع القفل المشترك تعديل الصفوف المحددة حتى يتم تنفيذ معاملتك (transaction):

    DB::table('users')
            ->where('votes', '>', 100)
            ->sharedLock()
            ->get();

بدلاً من ذلك ، يمكنك استخدام طريقة `lockForUpdate`. يمنع قفل "التحديث" تعديل السجلات المحددة أو تحديدها باستخدام قفل مشترك آخر:

    DB::table('users')
            ->where('votes', '>', 100)
            ->lockForUpdate()
            ->get();

<a name="debugging"></a>

## التشخيص (Debugging)

يمكنك استخدام التابعين `dd` و` dump` أثناء بناء استعلام لتفريغ روابط الاستعلام الحالية و SQL. ستعرض الطريقة `dd` معلومات التشخيص ثم تتوقف عن تنفيذ الطلب. ستعرض الطريقة `dump` معلومات التشخيص ولكنه يسمح للطلب بمتابعة التنفيذ:

    DB::table('users')->where('votes', '>', 100)->dd();

    DB::table('users')->where('votes', '>', 100)->dump();
