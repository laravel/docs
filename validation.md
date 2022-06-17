# Validation

- [مقدمة](#introduction)
- [مقدمة سريعة للتحقق (Validation)](#validation-quickstart)
    - [إعداد التوجيه](#quick-defining-the-routes)
    - [إنشاء المتحكم](#quick-creating-the-controller)
    - [كتابة منطق التحقّق](#quick-writing-the-validation-logic)
    - [عرض أخطأ التحقق](#quick-displaying-the-validation-errors)
    - [إعادة تعبئة النموذج](#repopulating-forms)
    - [ملاحظة حول الحقوق الإختيارية](#a-note-on-optional-fields)
- [التحقق من صحة طلب النموذج](#form-request-validation)
    - [إنشاء طلبات النماذج](#creating-form-requests)
    - [قبول طلبات النماذج](#authorizing-form-requests)
    - [تخصص رسائل الأخطاء](#customizing-the-error-messages)
    - [تهيئة المدخلات للتحقق منها](#preparing-input-for-validation)
- [إنشاء التحققات بشكل يدوي](#manually-creating-validators)
    - [إعادة التوجيه التلقائي](#automatic-redirection)
    - [مجموعة أخطأ مسماة](#named-error-bags)
    - [تخصص رسائل الأخطاء ](#manual-customizing-the-error-messages)
    - [بعد خطاف  التحقق](#after-validation-hook)
- [العمل مع المدخلات التي تم التحقق من صحتها](#working-with-validated-input)
- [التعامل مع رسائل الأخطاء ](#working-with-error-messages)
    - [تعيين رسائل مخصصة في ملفات اللغة](#specifying-custom-messages-in-language-files)
    - [تعيين رسائل تحوي سمات العناصر في ملفات اللغة](#specifying-attribute-in-language-files)
    - [تحديد القيم في ملفات اللغة](#specifying-values-in-language-files)
- [قواعد التحقق المتوفرة](#available-validation-rules)
- [إضافة القواعد بشكل شرط](#conditionally-adding-rules)
- [التحقق من صحة المصفوفات](#validating-arrays)
    - [التحقق من صحة إدخال مصفوفة متداخلة](#validating-nested-array-input)
- [التحقق من صحة كلمات المرور](#validating-passwords)
- [قواعد التحقق المخصصة](#custom-validation-rules)
    - [استخدام كائنات عامة](#using-rule-objects)
    - [استخدام الإغلاق](#using-closures)
    - [القواعد المضمنة](#implicit-rules)

<a name="introduction"></a>
## مقدمة

توفر Laravel عدة طرق مختلفة للتحقق من صحة البيانات الواردة لمشروعك. من الشائع استخدام طريق "التحقق" (Validation) المتوفرة في جميع طلبات HTTP الواردة. ومع ذلك ، سنتحدث عن الطرق الأخرى للتحقق أيضًا.

يتضمن Laravel مجموعة متنوعة من قواعد التحقق الملائمة التي يمكنك تطبيقها على البيانات (Data) ، حتى أنه يوفر القدرة على التحقق من صحة القيم الفريدة في جدول من قاعدة بيانات معينة. سنغطي كل قواعد التحقق هذه بالتفصيل حتى تكون على علم بجميع ميزات التحقق من الصحة الخاصة ب Laravel.

<a name="validation-quickstart"></a>
## مقدمة سريعة للتحقق (Validation)

للتعرف على ميزات التحقق القوية من Laravel ، دعنا نلقي نظرة على مثال كامل للتحقق من صحة نموذج وعرض رسائل الخطأ مرة أخرى للمستخدم. من خلال قراءة هذه الكود العام عالي المستوى ، ستتمكن من اكتساب فهم عام جيد لكيفية التحقق من صحة بيانات الطلبات الواردة باستخدام Laravel:

<a name="quick-defining-the-routes"></a>
### إعداد التوجيه

أولاً ، لنفترض أن لدينا المسارات التالية المحددة في ملف `routes/web.php`:

    use App\Http\Controllers\PostController;

    Route::get('/post/create', [PostController::class, 'create']); // مسار عرض النموذج
    Route::post('/post', [PostController::class, 'store']); // مسار إستقبال البياتات

سيعرض المسار "/post/create" بالطريقة "GET" نموذجًا للمستخدم لإنشاء منشور مدونة جديد ، بينما يقوم المسار "/post" بالطريقة "POST" بتخزين منشور المدونة الجديد في قاعدة البيانات.

<a name="quick-creating-the-controller"></a>
### إنشاء المتحكم

بعد ذلك ، دعنا نلقي نظرة على وحدة تحكم (Controller) بسيطة تتعامل مع الطلبات الواردة إلى هذه المسارات. سنترك تابع (function) `store` فارغة في الوقت الحالي:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class PostController extends Controller
    {
        /**
         * Show the form to create a new blog post.
         *
         * @return \Illuminate\View\View
         */
        public function create()
        {
            return view('post.create');
        }

        /**
         * Store a new blog post.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            // Validate and store the blog post...
        }
    }

<a name="quick-writing-the-validation-logic"></a>
### كتابة منطق التحقّق

نحن الآن جاهزون لملء تابع `store` بالمنطق للتحقق من صحة منشور المدونة الجديد. للقيام بذلك ، سنستخدم التابع `validate` الذي يوفره الكائن` Illuminate\Http\Request`. إذا نجحت قواعد التحقق من الصحة ، فسيستمر تنفيذ التعليمات البرمجية بشكل طبيعي ؛ ومع ذلك ، إذا فشل التحقق من الصحة ، فسيتم طرح استثناء `Illuminate\Validation\ValidationException` وسيتم تلقائيًا إرسال استجابة الخطأ المناسبة إلى المستخدم.

إذا فشل التحقق من الصحة أثناء طلب HTTP تقليدي ، فسيتم إنشاء استجابة إعادة توجيه إلى عنوان URL السابق. إذا كان الطلب الوارد هو طلب XHR (XML Http Request) اي `AJAX` ، فسيتم إرجاع استجابة JSON التي تحتوي على رسائل خطأ التحقق من الصحة.

لفهم طريقة "التحقق" بشكل أفضل ، دعنا ننتقل مرة أخرى إلى تابع "store":

    /**
     * Store a new blog post.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        // The blog post is valid...
    }

كما ترى ، يتم تمرير قواعد التحقق إلى طرق "التحقق". لا تقلق - جميع قواعد التحقق المتاحة موثقة  [موجدة هنا](#available-validation-rules). مرة أخرى ، إذا فشل التحقق من الصحة ، فسيتم إنشاء استجابة مناسبة تلقائيًا. إذا تم التحقق من الصحة ، فسوف يستمر التابع الخاص بنا في التنفيذ بشكل طبيعي.

بدلاً من ذلك ، يمكن تحديد قواعد التحقق كمصفوفات من القواعد بدلاً من نص واحدة نفصله ب `|` محدّدة:


    $validatedData = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

بالإضافة إلى ذلك ، يمكنك استخدام التابع "validateWithBag" للتحقق من صحة الطلب وتخزين أي رسائل خطأ داخل [مجموعة أخطأ مسماة](#named-error-bags):

    $validatedData = $request->validateWithBag('post', [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

<a name="stopping-on-first-validation-failure"></a>
#### التوقف عند أول فشل في التحقق من الصحة
قد ترغب أحيانًا في إيقاف تشغيل قواعد التحقق من الصحة على إحدى السمات (Attributes) بعد فشل أول تحقق. للقيام بذلك ، عيِّن قاعدة "bail" للسمة:

    $request->validate([
        'title' => 'bail|required|unique:posts|max:255',
        'body' => 'required',
    ]);

في هذا المثال ، إذا فشلت القاعدة الفردية "unique" في سمة "title" ، فلن يتم التحقق من قاعدة "max". سيتم التحقق من القواعد بالترتيب الذي تم تعيينها به.

<a name="a-note-on-nested-attributes"></a>
#### ملاحظة حول السمات المتداخلة

إذا احتوى طلب HTTP الوارد على بيانات حقل متداخلة "nested" ، فيمكنك تحديد هذه الحقول في قواعد التحقق باستخدام صيغة النقطة "dot":

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'author.name' => 'required',
        'author.description' => 'required',
    ]);

من ناحية أخرى ، إذا كان اسم الحقل الخاص بك يحتوي على نقطة حرفية `.` ، فيمكنك تصريح منع تفسير ذلك على أنه بناء جملة "نقطة" عن طريق تخطي النقطة بشرطة مائلة `\` للخلف:

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'v1\.0' => 'required',
    ]);

<a name="quick-displaying-the-validation-errors"></a>
### عرض أخطأ التحقق

لذا ، ماذا لو لم تجتاز حقول الطلب الواردة لقواعد التحقق المحددة؟ كما ذكرنا سابقًا ، سيعيد Laravel توجيه المستخدم تلقائيًا إلى موقعه السابق. بالإضافة إلى ذلك ، سيتم تلقائيًا تلقي جميع أخطاء التحقق من الصحة و [إعادة طلب الإدخال](/docs/{{version}}/request#recovery-old-input) [إلى الجلسة](/docs/{{version}}/session#flash-data).

تتم مشاركة المتغير `errors$` مع جميع واجهات تطبيقك بواسطة البرنامج الوسيط `Illuminate\View\Middleware\ShareErrorsFromSession` ، والذي يتم توفيره بواسطة مجموعة البرامج ` web`. عند تطبيق هذه البرمجيات الوسيطة ، سيكون المتغير `$errors`متاحًا دائمًا في واجهة العرض الخاصة بك ، مما يتيح لك افتراض أن المتغير `$errors` مُعرّف دائمًا ويمكن استخدامه بأمان. سيكون المتغير `errors$` نسخة من` Illuminate\Support\MessageBag`. لمزيد من المعلومات حول العمل مع هذا الكائن ، راجع وثائقه [Error Messages](#working-with-error-messages).


لذلك ، في مثالنا ، ستتم إعادة توجيه المستخدم إلى التابع `create` في المتحكم الخاص بنا عندما يفشل التحقق من الصحة ، مما يسمح لنا بعرض رسائل الخطأ في طريقة العرض:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>إنشاء منشور</h1>

@if ($errors->any()) // التحقق من وجود أي خطء
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error) // $errors->all() لجلب كل الأخطاء بشكل مصفوفة
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a name="quick-customizing-the-error-messages"></a>
#### تخصيص رسائل الخطأ

تحتوي كل قواعد التحقق من الصحة المضمنة في Laravel على رسالة خطأ موجودة في ملف `lang/en/validation.php` الخاص بمشروعك. في هذا الملف ، ستجد إدخال ترجمة لكل قاعدة تحقق من الصحة. أنت حر في تغيير أو تعديل هذه الرسائل بناءً على احتياجات مشروعك.

بالإضافة إلى ذلك ، يمكنك نسخ هذا الملف إلى مجلد لغة ترجمة آخر لترجمة الرسائل للغة المشروع الخاص بك. لمعرفة المزيد حول اللغات في Laravel ، تحقق من [وثائق الترجمة](/docs/{{version}}/localization).

<a name="quick-xhr-requests-and-validation"></a>
#### طلبات XHR والتحقق من صحتها (AJAX)

في هذا المثال ، استخدمنا نموذجًا تقليديًا لإرسال البيانات إلى التطبيق. ومع ذلك ، تتلقى العديد من التطبيقات طلبات XHR (AJAX) من الواجهة الأمامية التي تعمل بنظام JavaScript. عند استخدام التابع "validate" أثناء طلب XHR ، لن يُنشئ Laravel استجابة إعادة توجيه. بدلاً من ذلك ، يُنشئ Laravel استجابة JSON تحتوي على جميع أخطاء التحقق من الصحة. سيتم إرسال استجابة JSON مع رمز حالة HTTP 422.

<a name="the-at-error-directive"></a>
#### توجيه `@error` 

يمكنك استخدام التوجيه `@error` [Blade](/docs/{{version}}/blade) لتحديد ما إذا كانت هناك رسائل خطأ تتعلق بالتحقق من الصحة لسمة معينة. ضمن التوجيه `@error` ، يمكنك تكرار المتغير `$message` لعرض رسالة الخطأ:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

إذا كنت تستخدم [مجموعة أخطأ مسماة](#named-error-bags) ، يمكنك تمرير اسم الخطأ باعتباره الوسيط الثاني إلى التوجيه `@error`:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### إعادة تعبئة النموذج

عندما يُنشئ Laravel استجابة إعادة توجيه بسبب خطأ في التحقق من الصحة ، سيعمل إطار العمل تلقائيًا [تعيين كل مدخلات الطلب إلى الجلسة](/docs/{{version}}/session#flash-data). يتم ذلك حتى تتمكن من الوصول بسهولة إلى المدخلات أثناء الطلب التالي وإعادة ملء النموذج الذي يحاول المستخدم إرساله.

لاسترداد المدخلات العأدة من الطلب السابق ، استدعِ التابع `old` في نسخة` Illuminate\Http\Request`. ستسحب الطريقة "old" لبيانات الإدخال التي تم إعادتها مسبقًا من ملف [الجلسة](/docs/{{version}}/session):

    $title = $request->old('title');

يوفر Laravel أيضًا مساعدًا عالميًا `old`. إذا كنت تعرض إدخالًا قديمًا داخل [نموذج في Blade](/docs/{{version}}/blade) ، فمن الملائم أكثر استخدام المساعد `old` لإعادة ملء النموذج. في حالة عدم وجود إدخال قديم للحقل المحدد ، فسيتم إرجاع `null` أي لا قيمة:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### ملاحظة حول الحقوق الإختيارية

بشكل افتراضي ، يشمل Laravel على البرامج الوسيطة `TrimStrings` و `ConvertEmptyStringsToNull` في حزمة البرامج الوسيطة العامة لتطبيقك. يتم سرد هذه البرامج الوسيطة في الحزم بواسطة فئة `App\Http\Kernel`. لهذا السبب ، ستحتاج غالبًا إلى وضع علامة على حقول الطلب الاختيارية "optional" على أنها "null" إذا كنت لا تريد أن يعتبر المدقق القيم "null" غير صالحة. علي سبيل المثال:

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
        'publish_at' => 'nullable|date',
    ]);

في هذا المثال ، نحدد أن الحقل `publish_at` قد يكون إما فارغ `null` أو يمثيل تاريخ صالح. إذا لم تتم إضافة تحقق `nullable` إلى تعريف القاعدة ، فإن المتحقق سيعتبر أن القيمة الفارغة `null` تاريخ غير صالح.

<a name="form-request-validation"></a>
## التحقق من صحة طلب النموذج

<a name="creating-form-requests"></a>
### إنشاء نموذج الإتصال

لأمثلة التحقق الأكثر تعقيدًا ، قد ترغب في إنشاء طلب نموذج `form request`. طلبات النموذج هي فئات طلبات مخصصة تلخص منطق التحقق من الصحة والتفويض الخاص بها. لإنشاء فئة طلب نموذج ، يمكنك استخدام الأمر `make: request`Artisan CLI:

```shell
php artisan make:request StorePostRequest
```

سيتم وضع فئة طلب النموذج الذي تم إنشاؤه في دليل `app/Http/Orders`. إذا كان هذا الدليل غير موجود ، فسيتم إنشاؤه عند تشغيل الأمر `make: request`. كل طلب نموذج تم إنشاؤه بواسطة Laravel له طريقتان: التفويض `authorize` و القواعد `rules`.

كما قد تكون خمنت ، فإن طريقة التفويض `authorize` مسؤولة عن تحديد ما إذا كان المستخدم المصادق عليه حاليًا يمكنه تنفيذ الإجراء الذي يمثله الطلب ، بينما تعرض طريقة القواعد `rules` قواعد التحقق التي يجب أن تنطبق على بيانات الطلب:

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ];
    }

> {نصيحة} يمكنك كتابة تلميح لأي تابع تطلبها ضمن توقيع أسلوب القواعد `rules`. سيتم حله تلقائيًا عبر Laravel 
شرح خدمة [service container](/docs/{{version}}/container).

إذن ، كيف يتم تقييم قواعد التحقق من الصحة؟ كل ما عليك فعله هو كتابة تلميح للطلب في تابع المتحكم الخاص بك. يتم التحقق من صحة طلب النموذج الوارد قبل استدعاء تابع وحدة التحكم ، مما يعني أنك لست بحاجة إلى ضغط المتحكم الخاص بك بأي منطق تحقق:

    /**
     * Store a new blog post.
     *
     * @param  \App\Http\Requests\StorePostRequest  $request
     * @return Illuminate\Http\Response
     */
    public function store(StorePostRequest $request)
    {
        // The incoming request is valid...

        // Retrieve the validated input data...
        $validated = $request->validated();

        // Retrieve a portion of the validated input data...
        $validated = $request->safe()->only(['name', 'email']);
        $validated = $request->safe()->except(['name', 'email']);
    }

إذا فشل التحقق من الصحة ، فسيتم إنشاء استجابة إعادة توجيه لإعادة المستخدم إلى موقعه السابق. ستعرض الأخطاء أيضًا للجلسة حتى تكون متاحة للعرض. إذا كان الطلب عبارة عن طلب XHR ، فسيتم إرجاع استجابة HTTP برمز الحالة 422 إلى المستخدم بما في ذلك نتيجة JSON لأخطاء التحقق من الصحة.

<a name="adding-after-hooks-to-form-requests"></a>
#### إضافة بعد الخطافات لتشكيل الطلبات

إذا كنت ترغب في إضافة خطاف التحقق `بعد` طلب النموذج ، فيمكنك استخدام التابع `withValidator`. يتلقى هذا التابع أداة التحقق المنشأة بالكامل ، مما يسمح لك باستدعاء أي من توابعها قبل أن يتم تقييم قواعد التحقق فعليًا:

    /**
     * Configure the validator instance.
     *
     * @param  \Illuminate\Validation\Validator  $validator
     * @return void
     */
    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add('field', 'Something is wrong with this field!');
            }
        });
    }


<a name="request-stopping-on-first-validation-rule-failure"></a>
#### التوقف عند فشل التحقق باول سمة

من خلال إضافة خاصية `stopOnFirstFailure` إلى فئة الطلب الخاصة بك ، يمكنك إبلاغ المتحقق بأنه يجب عليه التوقف عن التحقق من صحة جميع السمات (Attributes) بمجرد حدوث فشل واحد في التحقق من الصحة:

    /**
     * Indicates if the validator should stop on the first rule failure.
     *
     * @var bool
     */
    protected $stopOnFirstFailure = true;

<a name="customizing-the-redirect-location"></a>
#### تخصيص موقع إعادة التوجيه

كما تمت مناقشته سابقًا ، سيتم إنشاء استجابة إعادة التوجيه لإرسال المستخدم مرة أخرى إلى موقعه السابق عند فشل التحقق من صحة طلب النموذج. ومع ذلك ، فأنت حر في تخصيص موقع التوجيه. للقيام بذلك ، حدد خاصية `$redirect` في طلب النموذج الخاص بك:

    /**
     * The URI that users should be redirected to if validation fails.
     *
     * @var string
     */
    protected $redirect = '/dashboard';

أو ، إذا كنت ترغب في إعادة توجيه المستخدمين إلى مسار مسمى ، يمكنك تحديد خاصية `redirectRoute` بدلاً من ذلك:

    /**
     * The route that users should be redirected to if validation fails.
     *
     * @var string
     */
    protected $redirectRoute = 'dashboard';

<a name="authorizing-form-requests"></a>
### قبول طلبات النماذج

تحتوي فئة طلب النموذج أيضًا على طريقة التفويض `authorize`. ضمن هذه الطريقة ، يمكنك تحديد ما إذا كان المستخدم المقبولة لديه بالفعل صلاحية تحديث معلومات معينة. على سبيل المثال ، يمكنك تحديد ما إذا كان المستخدم يمتلك بالفعل تعليق مدونة يحاول تحديثه. على الأرجح ، ستتفاعل مع بوابات التفويض والسياسات [authorization gates and policies](/docs/{{version}}/authorization)من خلال هذه الطريقة:

    use App\Models\Comment;

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        $comment = Comment::find($this->route('comment'));

        return $comment && $this->user()->can('update', $comment);
    }

نظرًا لأن جميع طلبات النموذج توسع فئة طلب Laravel الأساسية ، فقد نستخدم التابع `user` للوصول إلى المستخدم المصادق عليه حاليًا. لاحظ أيضًا استدعاء طريقة المسار `route` في المثال أعلاه. تمنحك هذه الطريقة الوصول إلى معلمات URI (معرف الموارد الموحد - Uniform Resource Identifier) المحددة في المسار الذي يتم استدعاؤه ، مثل المعلمة `{comment}` في المثال أدناه:

    Route::post('/comment/{comment}');

لذلك ، إذا كان تطبيقك يستفيد من ربط نموذج المسار [route model binding](/docs/{{version}}/routing#route-model-binding) ، فقد يصبح كودك أكثر إيجازًا من خلال الوصول إلى النموذج الذي تم جعله كملك الطلب:

    return $this->user()->can('update', $this->comment);

إذا عرضت طريقة التفويض `authorize` خطأ `error` ، فسيتم إرجاع استجابة HTTP برمز الحالة 403 تلقائيًا ولن يتم تنفيذ التابع في المتحكم.

إذا كنت تخطط للتعامل مع منطق التفويض للطلب في جزء آخر من التطبيق الخاص بك ، فيمكنك ببساطة إرجاع نتيجة صحيحة `true` من طريقة التفويض `authorize`:

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

> {نصيحة} يمكنك كتابة تعليق لأي تابع تحتاجه ضمن توقيع أسلوب التفويض `authorize`. سيتم حلها تلقائيًا عبر  Laravel بحاوية المتحكم [service container](/docs/{{version}}/container).

<a name="customizing-the-error-messages"></a>
### تخصيص رسائل الخطأ

يمكنك تخصيص رسائل الخطأ المستخدمة في طلب النموذج عن طريق تجاوز طريقة `messages`. يجب أن يُرجع هذا التابع مصفوفة من أزواج السمات / القواعد ورسائل الخطأ المقابلة لها:

    /**
     * Get the error messages for the defined validation rules.
     *
     * @return array
     */
    public function messages()
    {
        return [
            'title.required' => 'A title is required',
            'body.required' => 'A message is required',
        ];
    }

<a name="customizing-the-validation-attributes"></a>
#### تخصيص سمات التحقق من الصحة

تحتوي العديد من رسائل الاخطأ قاعدة التحقق من الصحة المضمنة في Laravel على العنصر النائب `:attribute`. إذا كنت ترغب في استبدال العنصر النائب `:attribute` لرسالة التحقق باسم سمة مخصصة ، فيمكنك تحديد الأسماء المخصصة عن طريق تجاوز طريقة `attribute`. يجب أن يُعيد هذا التابع مصفوفة من أزواج السمات / الاسم:

    /**
     * Get custom attributes for validator errors.
     *
     * @return array
     */
    public function attributes()
    {
        return [
            'email' => 'email address',
        ];
    }

<a name="preparing-input-for-validation"></a>
### تحضير المدخلات للتحقق من صحتها

إذا كنت بحاجة إلى إعداد أو تصفية أي بيانات من الطلب قبل تطبيق قواعد التحقق الخاصة بك ، فيمكنك استخدام تابع `PreparForValidation`:

    use Illuminate\Support\Str;

    /**
     * Prepare the data for validation.
     *
     * @return void
     */
    protected function prepareForValidation()
    {
        $this->merge([
            'slug' => Str::slug($this->slug),
        ]);
    }

<a name="manually-creating-validators"></a>
## إنشاء التحقق يدويًا

إذا كنت لا تريد استخدام التابع `validate` في الطلب ، فيمكنك إنشاء نسخة محقق يدويًا باستخدام `Validator` [الواجهة](/docs/{{version}}/facades). تابع `make` على الواجهة تنشئ نسخة مدقق جديدة:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Validator;

    class PostController extends Controller
    {
        /**
         * Store a new blog post.
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $validator = Validator::make($request->all(), [
                'title' => 'required|unique:posts|max:255',
                'body' => 'required',
            ]);

            if ($validator->fails()) {
                return redirect('post/create')
                            ->withErrors($validator)
                            ->withInput();
            }

            // Retrieve the validated input...
            $validated = $validator->validated();

            // Retrieve a portion of the validated input...
            $validated = $validator->safe()->only(['name', 'email']);
            $validated = $validator->safe()->except(['name', 'email']);

            // Store the blog post...
        }
    }

الطريقة الأولى التي تم تمريرها إلى الأسلوب `make` هي البيانات التي قيد التحقق. الطريقة الثانية عبارة عن مجموعة من قواعد التحقق من الصحة التي يجب تطبيقها على البيانات.

بعد تحديد ما إذا كان التحقق من صحة الطلب قد فشل ، يمكنك استخدام التابع `withErrors` لإرسال رسائل الخطأ إلى الجلسة. عند استخدام هذا التابع ، ستتم مشاركة المتغير `$errors` تلقائيًا مع طرق العرض الخاصة بك بعد إعادة التوجيه ، مما يتيح لك عرضها بسهولة مرة أخرى للمستخدم. يقبل التابع `withError` مدققًا أو `MessageBag` أو PHP `array`.

#### التوقف عند أول فشل في التحقق من الصحة

سيُعلم التابع `stopOnFirstFailure` المحقق بأنه يجب عليه التوقف عن التحقق من صحة جميع السمات بمجرد حدوث فشل واحد في التحقق من الصحة:

    if ($validator->stopOnFirstFailure()->fails()) {
        // ...
    }

<a name="automatic-redirection"></a>
### إعادة التوجيه التلقائي

إذا كنت ترغب في إنشاء طلب يدقق يدويًا ولكنك لا تزال تستفيد من إعادة التوجيه التلقائي التي توفرها طريقة التحقق `validate` لطلب HTTP ، فيمكنك استدعاء التابع `validate` على مثيل مدقق موجود. إذا فشل التحقق من الصحة ، فسيتم إعادة توجيه المستخدم تلقائيًا أو ، في حالة طلب XHR ، سيتم إرجاع استجابة JSON:

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validate();

يمكنك استخدام التابع `validateWithBag` لتخزين رسائل الخطأ في [مجموعة أخطأ مسماة](#named-error-bags) إذا فشل التحقق من الصحة:

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validateWithBag('post');

<a name="named-error-bags"></a>
### مجموعة أخطأ مسماة

إذا كانت لديك عدة نماذج في صفحة واحدة ، فقد ترغب في تسمية مجموعة أخطاء `MessageBag` التي تحتوي على أخطاء التحقق من الصحة ، مما يسمح لك باسترداد رسائل الخطأ لنموذج معين. لتحقيق ذلك ، مرر اسمًا باعتباره الوسيطة الثانية إلى `withErrors`:

    return redirect('register')->withErrors($validator, 'login');

يمكنك بعد ذلك الوصول إلى نتائج `MessageBag` من المتغير `$errors`:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### تخصيص رسائل الخطأ

إذا لزم الأمر ، يمكنك تقديم رسائل خطأ مخصصة يجب أن يستخدمها نموذج المدقق بدلاً من رسائل الخطأ الافتراضية التي يوفرها Laravel. هناك عدة طرق لتحديد الرسائل المخصصة. أولاً ، يمكنك تمرير الرسائل المخصصة كمعامل ثالث إلى التابع `Validator::make`:

    $validator = Validator::make($input, $rules, $messages = [
        'required' => 'The :attribute field is required.',
    ]);

في هذا المثال ، سيتم استبدال العنصر النائب `:attribute` بالاسم الفعلي للحقل أثناء التحقق. يمكنك أيضًا استخدام عناصر بديلة أخرى في رسائل التحقق من الصحة. فمثلا:

    $messages = [
        'same' => 'The :attribute and :other must match.',
        'size' => 'The :attribute must be exactly :size.',
        'between' => 'The :attribute value :input is not between :min - :max.',
        'in' => 'The :attribute must be one of the following types: :values',
    ];

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### تحديد رسالة مخصصة لسمة معينة

قد ترغب أحيانًا في تحديد رسالة خطأ مخصصة لسمة معينة فقط. يمكنك القيام بذلك باستخدام وضع النقطة `dot`. حدد اسم السمة أولاً ، متبوعًا بالقاعدة:

    $messages = [
        'email.required' => 'We need to know your email address!',
    ];

<a name="specifying-custom-attribute-values"></a>
#### تحديد قيم السمات المخصصة

تتضمن العديد من رسائل الخطأ المضمنة في Laravel العنصر النائب `:attribute` الذي تم استبداله باسم الحقل أو السمة أثناء التحقق. لتخصيص القيم المستخدمة لاستبدال هذه العناصر النائبة لحقول معينة ، يمكنك تمرير مصفوفة من السمات المخصصة كمتغير رابع للتابع `Validator::make`:

    $validator = Validator::make($input, $rules, $messages, [
        'email' => 'email address',
    ]);

<a name="after-validation-hook"></a>
### بعد خطاف  التحقق

يمكنك أيضًا إرفاق عمليات الاسترجاعات ليتم تشغيلها بعد اكتمال التحقق. يتيح لك ذلك إجراء مزيد من التحقق بسهولة وإضافة المزيد من رسائل الخطأ إلى مجموعة الرسائل. للبدء ، استدع التابع `after` في نسخة المحقق:

    $validator = Validator::make(...);

    $validator->after(function ($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add(
                'field', 'Something is wrong with this field!'
            );
        }
    });

    if ($validator->fails()) {
        //
    }

<a name="working-with-validated-input"></a>
## العمل مع المدخلات التي تم التحقق من صحتها

بعد التحقق من صحة بيانات الطلب الوارد باستخدام طلب نموذج أو مثيل مدقق تم إنشاؤه يدويًا ، قد ترغب في استرداد بيانات الطلب الواردة التي خضعت بالفعل لعملية التحقق من الصحة. هذا يمكن أن يكون إنجاز بطرق متعددة. أولاً ، يمكنك استدعاء التابع `validate` في طلب نموذج أو نسخة مدقق. تقوم هذه الطريقة بإرجاع مصفوفة من البيانات التي تم التحقق من صحتها:

    $validated = $request->validated();

    $validated = $validator->validated();

بدلاً من ذلك ، يمكنك استدعاء التابع `safe` في طلب نموذج أو نسخة مدقق. تُرجع هذه الطريقة نسخة من `Illuminate\Support\ValidatedInput`. يعرض هذا الكائن الأساليب `فقط` (only) و` باستثناء` (except) و` الكل` (all) لاسترداد مجموعة فرعية من البيانات التي تم التحقق من صحتها أو مجموعة البيانات التي تم التحقق من صحتها بالكامل:

    $validated = $request->safe()->only(['name', 'email']);

    $validated = $request->safe()->except(['name', 'email']);

    $validated = $request->safe()->all();

بالإضافة إلى ذلك ، يمكن تكرار مثيل `Illuminate\Support\ValidateInput` والوصول إليه مثل المصفوفة:

    // Validated data may be iterated...
    foreach ($request->safe() as $key => $value) {
        //
    }

    // Validated data may be accessed as an array...
    $validated = $request->safe();

    $email = $validated['email'];

إذا كنت ترغب في إضافة حقول إضافية إلى البيانات التي تم التحقق من صحتها ، يمكنك استدعاء التابع `merge`:

    $validated = $request->safe()->merge(['name' => 'Taylor Otwell']);

إذا كنت ترغب في استرداد البيانات التي تم التحقق من صحتها كمثال [collection](/docs/{{version}}/collections) ، فيمكنك استدعاء التابع `collection`:

    $collection = $request->safe()->collect();

<a name="working-with-error-messages"></a>
## التعامل مع رسائل الخطأ

بعد استدعاء التابع `errors` في مثيل `Validator` ، ستتلقى نتيجة من `Illuminate\Support\MessageBag` ، والذي يحتوي على مجموعة متنوعة من التوابع الملائمة للتعامل مع رسائل الخطأ. المتغير `$errors` الذي يتم إتاحته تلقائيًا لجميع طرق العرض هو أيضًا مثيل لفئة `MessageBag`.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### استرجاع رسالة الخطأ الأولى لحقول الإدخال

لاسترداد رسالة الخطأ الأولى لحقل معين، استخدم التابع `first`:

    $errors = $validator->errors();

    echo $errors->first('email');

<a name="retrieving-all-error-messages-for-a-field"></a>
#### استرداد كافة رسائل الخطأ للحقل

إذا كنت بحاجة إلى استرداد مصفوفة من جميع الرسائل لحقل معين ، فاستخدم التابع `get`:

    foreach ($errors->get('email') as $message) {
        //
    }

إذا كنت تتحقق من صحة حقل نموذج كمصفوفة ، فيمكنك استرداد جميع الرسائل لكل عنصر من عناصر المصفوفة باستخدام الحرف `*`:

    foreach ($errors->get('attachments.*') as $message) {
        //
    }

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### استرداد كافة رسائل الخطأ لكافة الحقول

لاسترداد مصفوفة من جميع الرسائل لجميع الحقول ، استخدم التابع `all`:

    foreach ($errors->all() as $message) {
        //
    }

<a name="determining-if-messages-exist-for-a-field"></a>
#### تحديد ما إذا كانت الرسائل موجودة في أحد الحقول

يمكن استخدام التابع `has` لتحديد ما إذا كانت هناك أية رسائل خطأ لحقل معين:

    if ($errors->has('email')) {
        //
    }

<a name="specifying-custom-messages-in-language-files"></a>
### تحديد الرسائل المخصصة في ملفات اللغة

تحتوي كل قواعد التحقق من الصحة المضمنة في Laravel على رسالة خطأ موجودة في ملف `lang/en/validation.php` الخاص بتطبيقك. في هذا الملف ، ستجد إدخال ترجمة لكل قاعدة تحقق من الصحة. أنت حر في تغيير أو تعديل هذه الرسائل بناءً على احتياجات تطبيقك.

بالإضافة إلى ذلك ، يمكنك نسخ هذا الملف إلى دليل لغة ترجمة آخر لترجمة الرسائل للغة التطبيق الخاص بك. لمعرفة المزيد حول الترجمة في Laravel ، تحقق من [وثائق الترجمة](/docs/{{version}}/localization).

<a name="custom-messages-for-specific-attributes"></a>
#### رسائل مخصصة لسمات محددة

يمكنك تخصيص رسائل الخطأ المستخدمة في مجموعات القواعد والسمات المحددة ضمن ملفات لغة التحقق من صحة التطبيق الخاص بك. للقيام بذلك ، أضف تخصيصات رسالتك إلى المصفوفة المخصصة `custom` لملف اللغة `lang/xx/validation.php` الخاص بتطبيقك:

    'custom' => [
        'email' => [
            'required' => 'We need to know your email address!',
            'max' => 'Your email address is too long!'
        ],
    ],

<a name="specifying-attribute-in-language-files"></a>
### تحديد السمات في ملفات اللغة

تتضمن العديد من رسائل الخطأ المضمنة في Laravel العنصر النائب `: attribute` الذي تم استبداله باسم الحقل أو السمة تحت التحقق. إذا كنت ترغب في استبدال جزء `: attribute` من رسالة التحقق بقيمة مخصصة ، يمكنك تحديد اسم السمة المخصصة في مصفوفة` attributes` لملف اللغة `lang/xx/validation.php`:

    'attributes' => [
        'email' => 'email address',
    ],

<a name="specifying-values-in-language-files"></a>
### تحديد القيم في ملفات اللغة

تحتوي بعض رسائل خطأ في قاعدة التحقق المضمنة في Laravel على عنصر نائب `:value` يتم استبداله بالقيمة الحالية لسمة الطلب. ومع ذلك ، قد تحتاج أحيانًا إلى استبدال الجزء `:value` من رسالة التحقق بتمثيل مخصص للقيمة. على سبيل المثال ، ضع في اعتبارك القاعدة التالية التي تحدد أن رقم بطاقة الائتمان مطلوب إذا كان نوع الدفع `payment_type` له قيمة نسخة أولية `cc`:

    Validator::make($request->all(), [
        'credit_card_number' => 'required_if:payment_type,cc'
    ]);

إذا فشلت قاعدة التحقق من الصحة ، فستظهر رسالة الخطأ التالية:

```none
مطلوب حقل رقم بطاقة الائتمان عندما يكون نوع الدفع cc.
```

بدلاً من عرض `cc` كقيمة لنوع الدفع ، يمكنك تحديد تمثيل أكثر سهولة في الاستخدام في ملف اللغة `lang/xx/validation.php` عن طريق تحديد مصفوفة القيم `values` :

    'values' => [
        'payment_type' => [
            'cc' => 'credit card'
        ],
    ],

بعد تحديد هذه القيمة ، ستُظهر قاعدة التحقق رسالة الخطأ التالية:

```none
حقل رقم بطاقة الائتمان مطلوب عندما يكون نوع الدفع هو بطاقة ائتمان.c
```

<a name="available-validation-rules"></a>
## قواعد التحقق المتوفرة

فيما يلي قائمة بجميع قواعد التحقق المتاحة ووظائفها:

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">

[مقبول](#rule-accepted)
[مقبول بشرط](#rule-accepted-if)
[رابط نشط](#rule-active-url)
[بعد تاريخ](#rule-after)
[بعد او بنفس التاريخ](#rule-after-or-equal)
[بدون فراغات للأحرف](#rule-alpha)
[السماح بالشارطة السفلية (_) مع الأحرف](#rule-alpha-dash)
[أحرف رقمية](#rule-alpha-num)
[مصفوفة](#rule-array)
[التوقف عند أول خطأ](#rule-bail)
[قبل تاريخ](#rule-before)
[قبل أو بنفس التاريخ](#rule-before-or-equal)
[بين قيمتين](#rule-between)
[قيمة منطقية](#rule-boolean)
[مؤكد](#rule-confirmed)
[كلمة المرور الحالية](#rule-current-password)
[التاريخ](#rule-date)
[التاريخ يساوي](#rule-date-equals)
[صيغة التاريخ](#rule-date-format)
[قيمة مرفوضة](#rule-declined)
[شرط الرفض](#rule-declined-if)
[الاختلاف](#rule-different)
[أرقام](#rule-digits)
[بين رقمين](#rule-digits-between)
[الأبعاد (للصور)](#rule-dimensions)
[قيم غير مكررة](#rule-distinct)
[الإيميل](#rule-email)
[ينتهي في](#rule-ends-with)
[التعداد](#rule-enum)
[إستبعاد](#rule-exclude)
[إستبعاد بشرط](#rule-exclude-if)
[استبعاد ما لم](#rule-exclude-unless)
[إستبعاد بدون](#rule-exclude-without)
[موجود بقاعدة البيانات](#rule-exists)
[ملفق](#rule-file)
[مملؤ](#rule-filled)
[أكثر من](#rule-gt)
[أكثر من أو يساوي](#rule-gte)
[ملف صورة](#rule-image)
[في](#rule-in)
[في مصفوفة](#rule-in-array)
[عدد صحيح](#rule-integer)
[IP Address](#rule-ip)
[MAC Address](#rule-mac)
[JSON](#rule-json)
[أقل من ](#rule-lt)
[أقل من أو يساوي](#rule-lte)
[الأكبر](#rule-max)
[أنواع MIME](#rule-mimetypes)
[نوع MIME حسب امتداد الملف](#rule-mimes)
[الأقل](#rule-min)
[مضاعفات](#multiple-of)
[ليس في](#rule-not-in)
[لا يطابق القيم المنطقية](#rule-not-regex)
[غير صالح](#rule-nullable)
[رقم](#rule-numeric)
[كلمة سر](#rule-password)
[الحاضر](#rule-present)
[محظور](#rule-prohibited)
[محظور بشرط](#rule-prohibited-if)
[محظور ما لم](#rule-prohibited-unless)
[يحظر](#rule-prohibits)
[مطابقة القيم المنطقية](#rule-regex)
[مطلوب](#rule-required)
[مطلوب بشرط](#rule-required-if)
[مطلوب مالم](#rule-required-unless)
[مطلوب مع](#rule-required-with)
[مطللوب مع الكل](#rule-required-with-all)
[مطلوب بدون](#rule-required-without)
[مطلوب بدون الكل](#rule-required-without-all)
[مطلوب مفاتيح المصفوفة](#rule-required-array-keys)
[يساوي](#rule-same)
[حجم](#rule-size)
[بعض الأحيان](#validating-when-present)
[ابدا ب](#rule-starts-with)
[نص](#rule-string)
[وحدة زمنية](#rule-timezone)
[غير موجود بقواعد البيانات](#rule-unique)
[رابط](#rule-url)
[UUID](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted (قبول)

يجب أن يكون الحقل تحت التحقق `"yes"` أو `"on"` أو `1`, أو `true`. هذا مفيد للتحقق من قبول "شروط الخدمة" (Terms of Service) أو الحقول المماثلة.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,... (قبول شرطي)

يجب أن يكون الحقل تحت التحقق `"yes"` أو `"on"` أو `1`, أو `true` إذا كان حقل آخر تحت التحقق مساويًا لقيمة محددة. هذا مفيد للتحقق من قبول "شروط الخدمة" (Terms of Service) أو الحقول المماثلة.

<a name="rule-active-url"></a>
#### active_url (عنوان url نشط)

يجب أن يحتوي الحقل تحت التحقق على سجل A أو AAAA صالح وفقًا لتابع PHP `dns_get_record`. يتم استخراج اسم المضيف لعنوان URL المقدم باستخدام تابع `parse_url` PHP قبل أن يتم تمريره إلى تابع `dns_get_record`.

<a name="rule-after"></a>
#### after:_date_ (بعد تاريخ)

يجب أن يكون الحقل تحت التحقق يحوي قيمة بعد تاريخ معين. سيتم تمرير التواريخ إلى دالة PHP `strtotime` ليتم تحويلها إلى نسخة `DateTime` صالحة:

    'start_date' => 'required|date|after:tomorrow'

بدلاً من تمرير نص تاريخ ليتم تقييمها بواسطة `strtotime` ، يمكنك تحديد حقل آخر للمقارنة مع التاريخ:

    'finish_date' => 'required|date|after:start_date'

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_ (يعد أو بنفس التاريخ)

يجب أن تكون قيمة الحقل تحت التحقق بعد التاريخ المحدد أو مساوية له. لمزيد من المعلومات ، راجع قاعدة [بعد التاريخ](#rule-after).

<a name="rule-alpha"></a>
#### alpha (حروف فقط)

يجب أن يكون الحقل تحت التحقق أحرفًا أبجدية بالكامل.

<a name="rule-alpha-dash"></a>
#### alpha_dash (السماح بالشارطة السفلية (_) مع الأحرف)

قد يحتوي الحقل تحت التحقق على أحرف أبجدية رقمية ، بالإضافة إلى شرطات وشرطات سفلية.

<a name="rule-alpha-num"></a>
#### alpha_num (أحرف رقمية)

يجب أن يتألف الحقل تحت التحقق من أحرف أبجدية رقمية بالكامل.

<a name="rule-array"></a>
#### array (مصفوفات)

يجب أن يكون الحقل تحت التحقق من PHP `array`.

عند توفير قيم إضافية لقاعدة `array` ، يجب أن يكون كل مفتاح في مصفوفة الإدخال موجودًا ضمن قائمة القيم المقدمة للقاعدة. في المثال التالي ، المفتاح `admin` في مصفوفة الإدخال غير صالح لأنه غير مضمن في قائمة القيم المقدمة لقاعدة `array`:

    use Illuminate\Support\Facades\Validator;

    $input = [
        'user' => [
            'name' => 'Taylor Otwell',
            'username' => 'taylorotwell',
            'admin' => true,
        ],
    ];

    Validator::make($input, [
        'user' => 'array:username,locale',
    ]);

بشكل عام ، يجب عليك دائمًا تحديد مفاتيح المصفوفة المسموح لها بالتواجد داخل المصفوفة الخاصة بك.

<a name="rule-bail"></a>
#### bail (التوقف عند أول خطأ)

توقف عن تشغيل قواعد التحقق من الصحة للحقل بعد فشل التحقق الأول.

بينما ستتوقف قاعدة `bail` عن التحقق من صحة حقل معين فقط عندما يواجه خطأً في التحقق من الصحة ، فإن تابع `stopOnFirstFailure` ستبلغ المدقق بأنه يجب أن يتوقف عن التحقق من صحة جميع السمات بمجرد حدوث فشل واحد في التحقق من الصحة:

    if ($validator->stopOnFirstFailure()->fails()) {
        // ...
    }

<a name="rule-before"></a>
#### before:_date_ (قبل تاريخ)

يجب أن يكون الحقل تحت التحقق قيمة تسبق التاريخ المحدد. سيتم تمرير التواريخ إلى دالة `strtotime` في PHP ليتم تحويلها إلى نسخة `DateTime` صالحة. بالإضافة إلى ذلك ، مثل قاعدة [`after`](#rule-after) ، قد يتم تقديم اسم حقل آخر تحت التحقق كقيمة التاريخ `date`.

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_ (قبل أو بنفس التاريخ)

يجب أن يكون الحقل تحت التحقق قيمة تسبق أو تسبق التاريخ المحدد. سيتم تمرير التواريخ إلى دالة `strtotime` في PHP ليتم تحويلها إلى نسخة `DateTime` صالحة. بالإضافة إلى ذلك ، مثل قاعدة [`after`](#rule-after) ، قد يتم تقديم اسم حقل آخر تحت التحقق كقيمة التاريخ `date`.

<a name="rule-between"></a>
#### between:_min_,_max_ (بين رقمين)

يجب أن يكون للحقل تحت التحقق حجم بين _min_ (أقل قيمة) محدد و _max_ (أكبر قيمة). يتم تقييم السلاسل والأرقام والمصفوفات والملفات بنفس طريقة تقييم قاعدة [`الحجم`](#rule-size).

<a name="rule-boolean"></a>
#### boolean (قيم منطقية)

يجب أن يكون الحقل تحت التحقق قادرًا على أن يكون منطقيًا. الإدخال المقبول هو
 `true` أو `false` أو `1` أو `0` أو `1` أو `0`.

<a name="rule-confirmed"></a>
#### confirmed

يجب أن يحتوي الحقل تحت التحقق على حقل مطابق لـ `{field}_confirmation`.  على سبيل المثال ، إذا كان الحقل الخاص بالتحقق هو كلمة المرور `password` ، فيجب أن يكون حقل `password_confirmation` موجودًا في الإدخال.

<a name="rule-current-password"></a>
#### current_password (كلمة المرور الحالية)

يجب أن يتطابق الحقل تحت التحقق مع كلمة مرور المستخدم المصادق عليه. يمكنك تحديد [طريقة التأكد](/docs/{{version}}/authentication) باستخدام المعامل الأولى للقاعدة:

    'password' => 'current_password:api'

<a name="rule-date"></a>
#### التاريخ

يجب أن يكون الحقل تحت التحقق تاريخًا صالحًا وغير نسبي وفقًا لتابع PHP `strtotime`.

<a name="rule-date-equals"></a>
#### التاريخ يساوي

يجب أن يكون الحقل تحت التحقق مساوياً لتاريخ المحدد. سيتم تمرير التواريخ في تابع PHP `Strtotime` من أجل تحويلها إلى مساوة صالحة `DateTime`.

<a name="rule-date-format"></a>
#### صيغة التاريخ

يجب أن يتطابق الحقل تحت التحقق مع `_format_` الصيغة المحددة .  يجب عليك استخدام **إما** تاريخ `date` أو تنسيق التاريخ `date_format` عند التحقق من صحة أحد الحقول ، وليس كليهما.  تدعم قاعدة التحقق هذه جميع التنسيقات التي تدعمها فئة الخاصة بـ PHP [DateTime](https://www.php.net/manual/en/class.datetime.php).

<a name="rule-declined"></a>
#### قيمة مرفوضة

يجب أن يكون الحقل تحت التحقق `"no"`, `"off"`, `0`, او `false`.

<a name="rule-declined-if"></a>
#### شرط الرفض

يجب أن يكون الحقل تحت التحقق `"no"`, `"off"`, `0`, او `false` إذا كان حقل آخر تحت التحقق يساوي قيمة محددة.

<a name="rule-different"></a>
#### الاختلاف

يجب أن يكون للحقل تحت التحقق قيمة مختلفة عن _field_.

<a name="rule-digits"></a>
#### القيمة أرقام

يجب أن يكون الحقل تحت التحقق _numeric_ ويجب أن يكون بطول _value_ بالضبط.

<a name="rule-digits-between"></a>
#### بين رقمين (أصغري،أغظمي)

يجب أن يكون الحقل تحت التحقق _numeric_ ويجب أن يكون بطول يتراوح بين _min_ المحدد و _ الحد الأقصى_.

<a name="rule-dimensions"></a>
#### الأبعاد (للصور)

يجب أن يكون الملف قيد التحقق صورة تفي بقيود الأبعاد كما هو محدد بواسطة معلمات القاعدة:

    'avatar' => 'dimensions:min_width=100,min_height=200'

القيود المتاحة هي: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

يجب تمثيل القيد _ratio_ بالعرض مقسومًا على الارتفاع. يمكن تحديد ذلك إما بكسر مثل `3/2` أو عدد عشري مثل `1.5`:

    'avatar' => 'dimensions:ratio=3/2'

نظرًا لأن هذه القاعدة تتطلب عدة وسيطات ، يمكنك استخدام التابع `Rule :: features` لإنشاء القاعدة بطلاقة:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'avatar' => [
            'required',
            Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
        ],
    ]);

<a name="rule-distinct"></a>
#### distinct

When validating arrays, the field under validation must not have any duplicate values:

    'foo.*.id' => 'distinct'

Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition:

    'foo.*.id' => 'distinct:strict'

You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences:

    'foo.*.id' => 'distinct:ignore_case'

<a name="rule-email"></a>
#### email

The field under validation must be formatted as an email address. This validation rule utilizes the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well:

    'email' => 'email:rfc,dns'

The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`

</div>

The `filter` validator, which uses PHP's `filter_var` function, ships with Laravel and was Laravel's default email validation behavior prior to Laravel version 5.8.

> {note} The `dns` and `spoof` validators require the PHP `intl` extension.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

The field under validation must end with one of the given values.

<a name="rule-enum"></a>
#### enum

The `Enum` rule is a class based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument:

    use App\Enums\ServerStatus;
    use Illuminate\Validation\Rules\Enum;

    $request->validate([
        'status' => [new Enum(ServerStatus::class)],
    ]);

> {note} Enums are only available on PHP 8.1+.

<a name="rule-exclude"></a>
#### exclude

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_.

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_'s field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present.

<a name="rule-exists"></a>
#### exists:_table_,_column_

The field under validation must exist in a given database table.

<a name="basic-usage-of-exists-rule"></a>
#### Basic Usage Of Exists Rule

    'state' => 'exists:states'

If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value.

<a name="specifying-a-custom-column-name"></a>
#### Specifying A Custom Column Name

You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name:

    'state' => 'exists:states,abbreviation'

Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name:

    'email' => 'exists:connection.staff,email'

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

    'user_id' => 'exists:App\Models\User,id'

If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::exists('staff')->where(function ($query) {
                return $query->where('account_id', 1);
            }),
        ],
    ]);

<a name="rule-file"></a>
#### file

The field under validation must be a successfully uploaded file.

<a name="rule-filled"></a>
#### filled

The field under validation must not be empty when it is present.

<a name="rule-gt"></a>
#### gt:_field_

The field under validation must be greater than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule.

<a name="rule-gte"></a>
#### gte:_field_

The field under validation must be greater than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule.

<a name="rule-image"></a>
#### image

The file under validation must be an image (jpg, jpeg, png, bmp, gif, svg, or webp).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'zones' => [
            'required',
            Rule::in(['first-zone', 'second-zone']),
        ],
    ]);

When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    $input = [
        'airports' => ['NYC', 'LAS'],
    ];

    Validator::make($input, [
        'airports' => [
            'required',
            'array',
            Rule::in(['NYC', 'LIT']),
        ],
    ]);

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

The field under validation must exist in _anotherfield_'s values.

<a name="rule-integer"></a>
#### integer

The field under validation must be an integer.

> {note} This validation rule does not verify that the input is of the "integer" variable type, only that the input is of a type accepted by PHP's `FILTER_VALIDATE_INT` rule. If you need to validate the input as being a number please use this rule in combination with [the `numeric` validation rule](#rule-numeric).

<a name="rule-ip"></a>
#### ip

The field under validation must be an IP address.

<a name="ipv4"></a>
#### ipv4

The field under validation must be an IPv4 address.

<a name="ipv6"></a>
#### ipv6

The field under validation must be an IPv6 address.

<a name="rule-mac"></a>
#### mac_address

The field under validation must be a MAC address.

<a name="rule-json"></a>
#### json

The field under validation must be a valid JSON string.

<a name="rule-lt"></a>
#### lt:_field_

The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule.

<a name="rule-lte"></a>
#### lte:_field_

The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule.

<a name="rule-max"></a>
#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

The file under validation must match one of the given MIME types:

    'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'

To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

<a name="basic-usage-of-mime-rule"></a>
#### Basic Usage Of MIME Rule

    'photo' => 'mimes:jpg,bmp,png'

Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

<a name="multiple-of"></a>
#### multiple_of:_value_

The field under validation must be a multiple of _value_.

> {note} The [`bcmath` PHP extension](https://www.php.net/manual/en/book.bc.php) is required in order to use the `multiple_of` rule.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'toppings' => [
            'required',
            Rule::notIn(['sprinkles', 'cherries']),
        ],
    ]);

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

The field under validation must not match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`.

> {note} When using the `regex` / `not_regex` patterns, it may be necessary to specify your validation rules using an array instead of using `|` delimiters, especially if the regular expression contains a `|` character.

<a name="rule-nullable"></a>
#### nullable

The field under validation may be `null`.

<a name="rule-numeric"></a>
#### numeric

The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php).

<a name="rule-password"></a>
#### password

The field under validation must match the authenticated user's password.

> {note} This rule was renamed to `current_password` with the intention of removing it in Laravel 9. Please use the [Current Password](#rule-current-password) rule instead.

<a name="rule-present"></a>
#### present

The field under validation must be present in the input data but can be empty.

<a name="rule-prohibited"></a>
#### prohibited

The field under validation must be empty or not present.

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

The field under validation must be empty or not present if the _anotherfield_ field is equal to any _value_.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

The field under validation must be empty or not present unless the _anotherfield_ field is equal to any _value_.

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

If the field under validation is present, no fields in _anotherfield_ can be present, even if empty.

<a name="rule-regex"></a>
#### regex:_pattern_

The field under validation must match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`.

> {note} When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using `|` delimiters, especially if the regular expression contains a `|` character.

<a name="rule-required"></a>
#### required

The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_.

If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf($request->user()->is_admin),
    ]);

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf(function () use ($request) {
            return $request->user()->is_admin;
        }),
    ]);

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

The field under validation must be an array and must contain at least the specified keys.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.

<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples:

    // Validate that a string is exactly 12 characters long...
    'title' => 'size:12';

    // Validate that a provided integer equals 10...
    'seats' => 'integer|size:10';

    // Validate that an array has exactly 5 elements...
    'tags' => 'array|size:5';

    // Validate that an uploaded file is exactly 512 kilobytes...
    'image' => 'file|size:512';

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

The field under validation must start with one of the given values.

<a name="rule-string"></a>
#### string

The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field.

<a name="rule-timezone"></a>
#### timezone

The field under validation must be a valid timezone identifier according to the `timezone_identifiers_list` PHP function.

<a name="rule-unique"></a>
#### unique:_table_,_column_

The field under validation must not exist within the given database table.

**Specifying A Custom Table / Column Name:**

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

    'email' => 'unique:App\Models\User,email_address'

The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used.

    'email' => 'unique:users,email_address'

**Specifying A Custom Database Connection**

Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name:

    'email' => 'unique:connection.users,email_address'

**Forcing A Unique Rule To Ignore A Given ID:**

Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question.

To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::unique('users')->ignore($user->id),
        ],
    ]);

> {note} You should never pass any user controlled request input into the `ignore` method. Instead, you should only pass a system generated unique ID such as an auto-incrementing ID or UUID from an Eloquent model instance. Otherwise, your application will be vulnerable to an SQL injection attack.

Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model:

    Rule::unique('users')->ignore($user)

If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method:

    Rule::unique('users')->ignore($user->id, 'user_id')

By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method:

    Rule::unique('users', 'email_address')->ignore($user->id),

**Adding Additional Where Clauses:**

You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`:

    'email' => Rule::unique('users')->where(function ($query) {
        return $query->where('account_id', 1);
    })

<a name="rule-url"></a>
#### url

The field under validation must be a valid URL.

<a name="rule-uuid"></a>
#### uuid

The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID).

<a name="conditionally-adding-rules"></a>
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### Skipping Validation When Fields Have Certain Values

You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_if:has_appointment,false|required|date',
        'doctor_name' => 'exclude_if:has_appointment,false|required|string',
    ]);

Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value:

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
        'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
    ]);

<a name="validating-when-present"></a>
#### Validating When Present

In some situations, you may wish to run validation checks against a field **only** if that field is present in the data being validated. To quickly accomplish this, add the `sometimes` rule to your rule list:

    $v = Validator::make($data, [
        'email' => 'sometimes|required|email',
    ]);

In the example above, the `email` field will only be validated if it is present in the `$data` array.

> {tip} If you are attempting to validate a field that should always be present but may be empty, check out [this note on optional fields](#a-note-on-optional-fields).

<a name="complex-conditional-validation"></a>
#### Complex Conditional Validation

Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'email' => 'required|email',
        'games' => 'required|numeric',
    ]);

Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance.

    $validator->sometimes('reason', 'required|max:500', function ($input) {
        return $input->games >= 100;
    });

The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once:

    $validator->sometimes(['reason', 'cost'], 'required', function ($input) {
        return $input->games >= 100;
    });

> {tip} The `$input` parameter passed to your closure will be an instance of `Illuminate\Support\Fluent` and may be used to access your input and files under validation.

<a name="complex-conditional-array-validation"></a>
#### Complex Conditional Array Validation

Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated:

    $input = [
        'channels' => [
            [
                'type' => 'email',
                'address' => 'abigail@example.com',
            ],
            [
                'type' => 'url',
                'address' => 'https://example.com',
            ],
        ],
    ];

    $validator->sometimes('channels.*.address', 'email', function ($input, $item) {
        return $item->type === 'email';
    });

    $validator->sometimes('channels.*.address', 'url', function ($input, $item) {
        return $item->type !== 'email';
    });

Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string.

<a name="validating-arrays"></a>
## Validating Arrays

As discussed in the [`array` validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail:

    use Illuminate\Support\Facades\Validator;

    $input = [
        'user' => [
            'name' => 'Taylor Otwell',
            'username' => 'taylorotwell',
            'admin' => true,
        ],
    ];

    Validator::make($input, [
        'user' => 'array:username,locale',
    ]);

In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules.

<a name="validating-nested-array-input"></a>
### Validating Nested Array Input

Validating nested array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'photos.profile' => 'required|image',
    ]);

You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following:

    $validator = Validator::make($request->all(), [
        'person.*.email' => 'email|unique:users',
        'person.*.first_name' => 'required_with:person.*.last_name',
    ]);

Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array based fields:

    'custom' => [
        'person.*.email' => [
            'unique' => 'Each person must have a unique email address',
        ]
    ],

<a name="accessing-nested-array-data"></a>
#### Accessing Nested Array Data

Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::foreEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element:

    use App\Rules\HasPermission;
    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    $validator = Validator::make($request->all(), [
        'companies.*.id' => Rule::forEach(function ($value, $attribute) {
            return [
                Rule::exists(Company::class, 'id'),
                new HasPermission('manage-company', $value),
            ];
        }),
    ]);

<a name="validating-passwords"></a>
## Validating Passwords

To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rules\Password;

    $validator = Validator::make($request->all(), [
        'password' => ['required', 'confirmed', Password::min(8)],
    ]);

The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing:

    // Require at least 8 characters...
    Password::min(8)

    // Require at least one letter...
    Password::min(8)->letters()

    // Require at least one uppercase and one lowercase letter...
    Password::min(8)->mixedCase()

    // Require at least one number...
    Password::min(8)->numbers()

    // Require at least one symbol...
    Password::min(8)->symbols()

In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method:

    Password::min(8)->uncompromised()

Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security.

By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method:

    // Ensure the password appears less than 3 times in the same data leak...
    Password::min(8)->uncompromised(3);

Of course, you may chain all the methods in the examples above:

    Password::min(8)
        ->letters()
        ->mixedCase()
        ->numbers()
        ->symbols()
        ->uncompromised()

<a name="defining-default-password-rules"></a>
#### Defining Default Password Rules

You may find it convenient to specify the default validation rules for passwords in a single location of your application. You can easily accomplish this using the `Password::defaults` method, which accepts a closure. The closure given to the `defaults` method should return the default configuration of the Password rule. Typically, the `defaults` rule should be called within the `boot` method of one of your application's service providers:

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
                    ? $rule->mixedCase()->uncompromised()
                    : $rule;
    });
}
```

Then, when you would like to apply the default rules to a particular password undergoing validation, you may invoke the `defaults` method with no arguments:

    'password' => ['required', Password::defaults()],

Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this:

    use App\Rules\ZxcvbnRule;

    Password::defaults(function () {
        $rule = Password::min(8)->rules([new ZxcvbnRule]);

        // ...
    });

<a name="custom-validation-rules"></a>
## Custom Validation Rules

<a name="using-rule-objects"></a>
### Using Rule Objects

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory. If this directory does not exist, Laravel will create it when you execute the Artisan command to create your rule:

```shell
php artisan make:rule Uppercase
```

Once the rule has been created, we are ready to define its behavior. A rule object contains two methods: `passes` and `message`. The `passes` method receives the attribute value and name, and should return `true` or `false` depending on whether the attribute value is valid or not. The `message` method should return the validation error message that should be used when validation fails:

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;

    class Uppercase implements Rule
    {
        /**
         * Determine if the validation rule passes.
         *
         * @param  string  $attribute
         * @param  mixed  $value
         * @return bool
         */
        public function passes($attribute, $value)
        {
            return strtoupper($value) === $value;
        }

        /**
         * Get the validation error message.
         *
         * @return string
         */
        public function message()
        {
            return 'The :attribute must be uppercase.';
        }
    }

You may call the `trans` helper from your `message` method if you would like to return an error message from your translation files:

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return trans('validation.uppercase');
    }

Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules:

    use App\Rules\Uppercase;

    $request->validate([
        'name' => ['required', 'string', new Uppercase],
    ]);

#### Accessing Additional Data

If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation:

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;
    use Illuminate\Contracts\Validation\DataAwareRule;

    class Uppercase implements Rule, DataAwareRule
    {
        /**
         * All of the data under validation.
         *
         * @var array
         */
        protected $data = [];

        // ...

        /**
         * Set the data under validation.
         *
         * @param  array  $data
         * @return $this
         */
        public function setData($data)
        {
            $this->data = $data;

            return $this;
        }
    }

Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface:

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;
    use Illuminate\Contracts\Validation\ValidatorAwareRule;

    class Uppercase implements Rule, ValidatorAwareRule
    {
        /**
         * The validator instance.
         *
         * @var \Illuminate\Validation\Validator
         */
        protected $validator;

        // ...

        /**
         * Set the current validator.
         *
         * @param  \Illuminate\Validation\Validator  $validator
         * @return $this
         */
        public function setValidator($validator)
        {
            $this->validator = $validator;

            return $this;
        }
    }

<a name="using-closures"></a>
### Using Closures

If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'title' => [
            'required',
            'max:255',
            function ($attribute, $value, $fail) {
                if ($value === 'foo') {
                    $fail('The '.$attribute.' is invalid.');
                }
            },
        ],
    ]);

<a name="implicit-rules"></a>
### Implicit Rules

By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [`unique`](#rule-unique) rule will not be run against an empty string:

    use Illuminate\Support\Facades\Validator;

    $rules = ['name' => 'unique:users,name'];

    $input = ['name' => ''];

    Validator::make($input, $rules)->passes(); // true

For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To create an "implicit" rule, implement the `Illuminate\Contracts\Validation\ImplicitRule` interface. This interface serves as a "marker interface" for the validator; therefore, it does not contain any additional methods you need to implement beyond the methods required by the typical `Rule` interface.

To generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option :

```shell
php artisan make:rule Uppercase --implicit
```

> {note} An "implicit" rule only _implies_ that the attribute is required. Whether it actually invalidates a missing or empty attribute is up to you.
