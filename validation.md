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
#### Stopping On First Validation Failure Attribute (التوقف عند أول فشل في التحقق من الصحة)
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
## Form Request Validation (التحقق من صحة طلب النموذج)

<a name="creating-form-requests"></a>
### Creating Form Requests (إنشاء نموذج الإتصال)

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
#### Stopping On First Validation Failure Attribute (التوقف عند فشل التحقق باول سمة)

من خلال إضافة خاصية `stopOnFirstFailure` إلى فئة الطلب الخاصة بك ، يمكنك إبلاغ المتحقق بأنه يجب عليه التوقف عن التحقق من صحة جميع السمات (Attributes) بمجرد حدوث فشل واحد في التحقق من الصحة:

    /**
     * Indicates if the validator should stop on the first rule failure.
     *
     * @var bool
     */
    protected $stopOnFirstFailure = true;

<a name="customizing-the-redirect-location"></a>
#### Customizing The Redirect Location (تخصيص موقع إعادة التوجيه)

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
### Authorizing Form Requests (قبول طلبات النماذج)

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

#### Stopping On First Validation Failure (التوقف عند أول فشل في التحقق من الصحة)

سيُعلم التابع `stopOnFirstFailure` المحقق بأنه يجب عليه التوقف عن التحقق من صحة جميع السمات بمجرد حدوث فشل واحد في التحقق من الصحة:

    if ($validator->stopOnFirstFailure()->fails()) {
        // ...
    }

<a name="automatic-redirection"></a>
### Automatic Redirection (إعادة التوجيه التلقائي)

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
## Working With Validated Input (العمل مع المدخلات التي تم التحقق من صحتها)

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
## Working With Error Messages (التعامل مع رسائل الخطأ)

بعد استدعاء التابع `errors` في مثيل `Validator` ، ستتلقى نتيجة من `Illuminate\Support\MessageBag` ، والذي يحتوي على مجموعة متنوعة من التوابع الملائمة للتعامل مع رسائل الخطأ. المتغير `$errors` الذي يتم إتاحته تلقائيًا لجميع طرق العرض هو أيضًا مثيل لفئة `MessageBag`.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### Retrieving The First Error Message For A Field (استرجاع رسالة الخطأ الأولى لحقول الإدخال)

لاسترداد رسالة الخطأ الأولى لحقل معين، استخدم التابع `first`:

    $errors = $validator->errors();

    echo $errors->first('email');

<a name="retrieving-all-error-messages-for-a-field"></a>
#### Retrieving All Error Messages For A Field (استرداد كافة رسائل الخطأ للحقل)

إذا كنت بحاجة إلى استرداد مصفوفة من جميع الرسائل لحقل معين ، فاستخدم التابع `get`:

    foreach ($errors->get('email') as $message) {
        //
    }

إذا كنت تتحقق من صحة حقل نموذج كمصفوفة ، فيمكنك استرداد جميع الرسائل لكل عنصر من عناصر المصفوفة باستخدام الحرف `*`:

    foreach ($errors->get('attachments.*') as $message) {
        //
    }

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### Retrieving All Error Messages For All Fields (استرداد كافة رسائل الخطأ لكافة الحقول)

لاسترداد مصفوفة من جميع الرسائل لجميع الحقول ، استخدم التابع `all`:

    foreach ($errors->all() as $message) {
        //
    }

<a name="determining-if-messages-exist-for-a-field"></a>
#### Determining If Messages Exist For A Field (تحديد ما إذا كانت الرسائل موجودة في أحد الحقول)

يمكن استخدام التابع `has` لتحديد ما إذا كانت هناك أية رسائل خطأ لحقل معين:

    if ($errors->has('email')) {
        //
    }

<a name="specifying-custom-messages-in-language-files"></a>
### Specifying Custom Messages In Language Files (تحديد الرسائل المخصصة في ملفات اللغة)

تحتوي كل قواعد التحقق من الصحة المضمنة في Laravel على رسالة خطأ موجودة في ملف `lang/en/validation.php` الخاص بتطبيقك. في هذا الملف ، ستجد إدخال ترجمة لكل قاعدة تحقق من الصحة. أنت حر في تغيير أو تعديل هذه الرسائل بناءً على احتياجات تطبيقك.

بالإضافة إلى ذلك ، يمكنك نسخ هذا الملف إلى دليل لغة ترجمة آخر لترجمة الرسائل للغة التطبيق الخاص بك. لمعرفة المزيد حول الترجمة في Laravel ، تحقق من [وثائق الترجمة](/docs/{{version}}/localization).

<a name="custom-messages-for-specific-attributes"></a>
#### Custom Messages For Specific Attributes (رسائل مخصصة لسمات محددة)

يمكنك تخصيص رسائل الخطأ المستخدمة في مجموعات القواعد والسمات المحددة ضمن ملفات لغة التحقق من صحة التطبيق الخاص بك. للقيام بذلك ، أضف تخصيصات رسالتك إلى المصفوفة المخصصة `custom` لملف اللغة `lang/xx/validation.php` الخاص بتطبيقك:

    'custom' => [
        'email' => [
            'required' => 'We need to know your email address!',
            'max' => 'Your email address is too long!'
        ],
    ],

<a name="specifying-attribute-in-language-files"></a>
### Specifying Attributes In Language Files (تحديد السمات في ملفات اللغة)

تتضمن العديد من رسائل الخطأ المضمنة في Laravel العنصر النائب `: attribute` الذي تم استبداله باسم الحقل أو السمة تحت التحقق. إذا كنت ترغب في استبدال جزء `: attribute` من رسالة التحقق بقيمة مخصصة ، يمكنك تحديد اسم السمة المخصصة في مصفوفة` attributes` لملف اللغة `lang/xx/validation.php`:

    'attributes' => [
        'email' => 'email address',
    ],

<a name="specifying-values-in-language-files"></a>
### Specifying Values In Language Files (تحديد القيم في ملفات اللغة)

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

يجب أن يكون الحقل تحت التحقق `yes` أو `on` أو `1`, أو `true`. هذا مفيد للتحقق من قبول "شروط الخدمة" (Terms of Service) أو الحقول المماثلة.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,... (قبول شرطي)

يجب أن يكون الحقل تحت التحقق `yes` أو `on` أو `1`, أو `true` إذا كان حقل آخر تحت التحقق مساويًا لقيمة محددة. هذا مفيد للتحقق من قبول "شروط الخدمة" (Terms of Service) أو الحقول المماثلة.

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
#### date (التاريخ)

يجب أن يكون الحقل تحت التحقق تاريخًا صالحًا وغير نسبي وفقًا لتابع PHP `strtotime`.

<a name="rule-date-equals"></a>
#### date_equals:date (التاريخ يساوي)

يجب أن يكون الحقل تحت التحقق مساوياً لتاريخ المحدد. سيتم تمرير التواريخ في تابع PHP `Strtotime` من أجل تحويلها إلى مساوة صالحة `DateTime`.

<a name="rule-date-format"></a>
#### date_format:format (صيغة التاريخ)

يجب أن يتطابق الحقل تحت التحقق مع `_format_` الصيغة المحددة .  يجب عليك استخدام **إما** تاريخ `date` أو تنسيق التاريخ `date_format` عند التحقق من صحة أحد الحقول ، وليس كليهما.  تدعم قاعدة التحقق هذه جميع التنسيقات التي تدعمها فئة الخاصة بـ PHP [DateTime](https://www.php.net/manual/en/class.datetime.php).

<a name="rule-declined"></a>
#### declined (قيمة مرفوضة)

يجب أن يكون الحقل تحت التحقق `no`, `off`, `0`, او `false`.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,... (شرط الرفض)

يجب أن يكون الحقل تحت التحقق `no`, `off`, `0`, او `false` إذا كان حقل آخر تحت التحقق يساوي قيمة محددة.

<a name="rule-different"></a>
#### different:field (الاختلاف)

يجب أن يكون للحقل تحت التحقق قيمة مختلفة عن _field_.

<a name="rule-digits"></a>
#### digits:value(القيمة أرقام)

يجب أن يكون الحقل تحت التحقق _numeric_ ويجب أن يكون بطول _value_ بالضبط.

<a name="rule-digits-between"></a>
####  digits_between:min,max (بين رقمين "أصغري،أغظمي")

يجب أن يكون الحقل تحت التحقق _numeric_ ويجب أن يكون بطول يتراوح بين _min_ الأصغري والحد الأقصى _max_.

<a name="rule-dimensions"></a>
####dimensions (الأبعاد للصور)

يجب أن يكون الملف قيد التحقق صورة تفي بقيود الأبعاد كما هو محدد بواسطة معلمات القاعدة:

    'avatar' => 'dimensions:min_width=100,min_height=200'

القيود المتاحة هي: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

يجب تمثيل القيد _ratio_ بالعرض مقسومًا على الارتفاع. يمكن تحديد ذلك إما بكسر مثل `3/2` أو عدد عشري مثل `1.5`:

    'avatar' => 'dimensions:ratio=3/2'

نظرًا لأن هذه القاعدة تتطلب عدة وسيطات ، يمكنك استخدام التابع `Rule::features` لإنشاء القاعدة بطلاقة:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'avatar' => [
            'required',
            Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
        ],
    ]);

<a name="rule-distinct"></a>
#### distinct (قيمة غير مكررة)

عند التحقق من المصفوفات، يجب ألا يحتوي الحقل تحت التحقق على أي قيم مكررة:

    'foo.*.id' => 'distinct'

يستخدم عامل التميز مقارنات متغيرة فضفاضة بشكل افتراضي. لاستخدام مقارنات صارمة، يمكنك إضافة المعامل `strict` إلى تعريف قاعدة التحقق من الصحة:

    'foo.*.id' => 'distinct:strict'

يمكنك إضافة المعامل `ignore_case` إلى تعريف قاعدة التحقق من الصحة لجعل القاعدة تتجاهل اختلافات الكتابة بالأحرف الكبيرة: 

    'foo.*.id' => 'distinct:ignore_case'

<a name="rule-email"></a>
#### email (تحقق الإيميل)

يجب تنسيق الحقل تحت التحقق كعنوان بريد إلكتروني. تستخدم قاعدة التحقق هذه الحزمة [`egulias/email-validator`](https://github.com/egulias/EmailValidator) للتحقق من صحة البريد الالكتروني. بشكل افتراضي ، يتم تطبيق مدقق `RFCValidation` ، ولكن يمكنك تطبيق أنماط تحقق أخرى أيضًا:

    'email' => 'email:rfc,dns'

سيطبق المثال أعلاه عمليتي التحقق من صحة `RFCValidation` و `DNSCheckValidation`. فيما يلي قائمة كاملة بأنماط التحقق التي يمكنك تطبيقها:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` : `بريد صالح`
- `strict`: `NoRFCWarningsValidation` : `لا يوجد أخطاء بتحقق البريد`
- `dns`: `DNSCheckValidation` : `مجال البريد صالح`
- `spoof`: `SpoofCheckValidation`: `منع انتحال بريد موثوق`
- `filter`: `FilterEmailValidation` : `التحقق بإستخدام تابع Filter`

</div>

مدقق `filter` ، الذي يستخدم دالة`filter_var` في PHP ، يأتي مع Laravel وكان سلوك Laravel الافتراضي للتحقق من البريد الإلكتروني قبل إصدار Laravel 5.8.

> {ملاحظة} تتطلب أدوات التحقق من `dns` و`spoof` امتداد PHP`intl`

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,... (ينتهي في)

يجب أن ينتهي الحقل تحت التحقق بإحدى القيم المقدمة.

<a name="rule-enum"></a>
#### enum (التعداد)

قاعدة `Enum` هي قاعدة قائمة على فئة تتحقق مما إذا كان الحقل تحت التحقق يحتوي على قيمة تعداد صالحة. تقبل قاعدة `Enum` اسم التعداد باعتباره الوسيطة المنشئة الوحيدة:

    use App\Enums\ServerStatus;
    use Illuminate\Validation\Rules\Enum;

    $request->validate([
        'status' => [new Enum(ServerStatus::class)],
    ]);

> {ملاحظة} Enums متاحة فقط في PHP 8.1+.

<a name="rule-exclude"></a>
#### exclude (استبعاد)

سيتم استبعاد الحقل تحت التحقق من بيانات الطلب التي يتم إرجاعها بواسطة طريقتي `validate` و `validated`.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_ (استبعاد شرطي)

سيتم استبعاد الحقل تحت التحقق من بيانات الطلب التي يتم إرجاعها بواسطة طريقتي `validate` و `validated`بشرط ال _anotherfield_ الحقل يساوي _value_.

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_ (استبعاد ما لم)

سيتم استبعاد الحقل تحت التحقق من بيانات الطلب التي يتم إرجاعها بواسطة طريقتي `validate` و `validated`. ما لم يكن حقل _anotherfield_ يساوي _value_.  إذا كانت _value_ `null` (`exclude_unless:name,null`) ، فسيتم استبعاد الحقل تحت التحقق ما لم يكن حقل المقارنة فارغاً `null` أو كان حقل المقارنة مفقودًا من بيانات الطلب.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_ (استبعاد بدون)

سيتم استبعاد الحقل تحت التحقق من بيانات الطلب التي يتم إرجاعها بواسطة طريقتي `validate` و `validated`إذا كان الحقل _anotherfield_ غير موجود.

<a name="rule-exists"></a>
#### exists:_table_,_column_ (موجود بقاعدة البيانات "جدول,عامود")

يجب أن يكون الحقل تحت التحقق موجودًا في جدول قاعدة بيانات محدد.

<a name="basic-usage-of-exists-rule"></a>
#### Basic Usage Of Exists Rule (الاستخدام الأساسي للقاعدة الموجود)

    'state' => 'exists:states'

إذا لم يتم تحديد العمود `column` ، فسيتم استخدام اسم الإدخال. لذلك ، في هذه الحالة ، ستتحقق القاعدة من أن جدول قاعدة بيانات الحالات `states` يحتوي على سجل له قيمة عمود الحالة `state` تطابق قيمة سمة الحالة `state` للطلب.

<a name="specifying-a-custom-column-name"></a>
#### Specifying A Custom Column Name (تحديد اسم عمود مخصص)

يمكنك تحديد اسم عمود قاعدة البيانات بشكل صريح والذي يجب أن تستخدمه قاعدة التحقق من الصحة بوضعه بعد اسم جدول قاعدة البيانات:

    'state' => 'exists:states,abbreviation'

في بعض الأحيان ، قد تحتاج إلى تحديد اتصال قاعدة بيانات معين لاستخدامه في الاستعلام موجود `exists`. يمكنك تحقيق ذلك من خلال إضافة اسم الاتصال مسبقًا إلى اسم الجدول:

    'email' => 'exists:connection.staff,email'

بدلاً من تحديد اسم الجدول مباشرةً ، يمكنك تحديد نموذج Eloquent الذي يجب استخدامه لتحديد اسم الجدول:

    'user_id' => 'exists:App\Models\User,id'

إذا كنت ترغب في تخصيص الاستعلام الذي تم تنفيذه بواسطة قاعدة التحقق ، فيمكنك استخدام فئة `Rule` لتعريف القاعدة بطلاقة. في هذا المثال ، سنحدد أيضًا قواعد التحقق من الصحة كمصفوفة بدلاً من استخدام الحرف `|` لتحديدها:

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
#### file (الملفات)

يجب أن يكون الحقل تحت التحقق ملفًا تم تحميله بنجاح.

<a name="rule-filled"></a>
#### filled (غير فارغ)

يجب ألا يكون الحقل تحت التحقق فارغًا عندما يكون موجودًا.

<a name="rule-gt"></a>
#### gt:_field_ (حجم أكبر من)

يجب أن يكون الحقل تحت التحقق أكبر من _field_ المحدد. يجب أن يكون الحقلين من نفس النوع. يتم تقييم السلاسل والأرقام والمصفوفات والملفات باستخدام نفس الاصطلاحات مثل قاعدة الحجم [`size`](#rule-size).

<a name="rule-gte"></a>
#### gte:_field_ (حجم أكبر أو يساوي)

يجب أن يكون الحقل تحت التحقق أكبر من _field_ المحدد أو مساويًا له. يجب أن يكون الحقلين من نفس النوع. يتم تقييم السلاسل والأرقام والمصفوفات والملفات باستخدام نفس الاصطلاحات مثل قاعدةالحجم [`size`](#rule-size).

<a name="rule-image"></a>
#### image (الصور)

يجب أن يكون الملف قيد التحقق صورة إمتداد (jpg أو jpeg أو png أو bmp أو gif أو svg أو webp).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

يجب تضمين الحقل تحت التحقق في قائمة القيم المحددة. نظرًا لأن هذه القاعدة تتطلب منك دمج `implode` مصفوفة ، يمكن استخدام التابع `Rule::in` لبناء القاعدة بطلاقة:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'zones' => [
            'required',
            Rule::in(['first-zone', 'second-zone']),
        ],
    ]);

عند دمج القاعدة `in` مع قاعدة المصفوفة `array` ، يجب أن تكون كل قيمة في مصفوفة الإدخال موجودة ضمن قائمة القيم المقدمة إلى القاعدة في `in`. في المثال التالي ، رمز المطار `LAS` في مصفوفة الإدخال غير صالح لأنه غير مضمن في قائمة المطارات المقدمة لقاعدة` in`:

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
#### in_array:_anotherfield_.* (تحقق قيمة موجودة في مصفوفة أم لا)

يجب أن يوجد الحقل تحت التحقق في قيم _anotherfield_.

<a name="rule-integer"></a>
#### integer (عدد صحيح)

يجب أن يكون الحقل تحت التحقق عددًا صحيحًا.

> {ملاحظة} لا تتحقق قاعدة التحقق من صحة الإدخال من نوع متغير عدد صحيح `integer` ، فقط أن الإدخال من النوع المقبول بواسطة قاعدة `FILTER_VALIDATE_INT` الخاصة بـ PHP. إذا كنت بحاجة إلى التحقق من صحة الإدخال باعتباره رقمًا ، فيرجى استخدام هذه القاعدة مع قاعدة تحقق الأرقام [the `numeric` validation rule](#rule-numeric).

<a name="rule-ip"></a>
#### ip

يجب أن يكون الحقل تحت التحقق عنوان IP.

<a name="ipv4"></a>
#### ipv4

يجب أن يكون الحقل تحت التحقق عنوان IPv4.

<a name="ipv6"></a>
#### ipv6

يجب أن يكون الحقل تحت التحقق عنوان IPv6.

<a name="rule-mac"></a>
#### mac_address

يجب أن يكون الحقل تحت التحقق عنوان MAC.

<a name="rule-json"></a>
#### json

يجب أن يكون الحقل تحت التحقق سلسلة JSON صالحة.

<a name="rule-lt"></a>
#### lt:_field_ (حجم أقل من المحدد)

يجب أن يكون الحقل تحت التحقق أقل من _field_ المحدد. يجب أن يكون الحقلين من نفس النوع. يتم تقييم السلاسل والأرقام والمصفوفات والملفات باستخدام نفس الاصطلاحات مثل قاعدة الحجم [`size`](#rule-size).

<a name="rule-lte"></a>
#### lte:_field_ (حجم أقل أو يساوي من المحدد)

يجب أن يكون الحقل تحت التحقق أقل من أو يساوي _field_ المحدد. يجب أن يكون الحقلين من نفس النوع. يتم تقييم السلاسل والأرقام والمصفوفات والملفات باستخدام نفس الاصطلاحات مثل قاعدة الحجم [`size`](#rule-size).

<a name="rule-max"></a>
#### max:_value_ (حجم أقل أو يساوي الحد الأقصى)

يجب أن يكون الحقل تحت التحقق أقل أو يساوي الحد الأقصى _value_. يجب أن يكون الحقلين من نفس النوع. يتم تقييم السلاسل والأرقام والمصفوفات والملفات باستخدام نفس الاصطلاحات مثل قاعدة الحجم [`size`](#rule-size).

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,... (تيساوي نوع MINE)

يجب أن يتطابق الملف قيد التحقق مع أحد أنواع MIME المحددة:

    'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'

لتحديد نوع MIME للملف الذي تم تحميله ، ستتم قراءة محتويات الملف وسيحاول إطار العمل تخمين نوع MIME ، والذي قد يكون مختلفًا عن نوع MIME المقدم من العميل.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,... (تيساوي أحد أنواع MINE)

يجب أن يحتوي الملف قيد التحقق من نوع MIME المطابق لإحدى الامتدادات المدرجة.

<a name="basic-usage-of-mime-rule"></a>
#### Basic Usage Of MIME Rule (الاستخدام الأساسي لقاعدة MIME)

    'photo' => 'mimes:jpg,bmp,png'

على الرغم من أنك تحتاج فقط إلى تحديد الامتدادات ، فإن هذه القاعدة تتحقق بالفعل من نوع MIME للملف من خلال قراءة محتويات الملف وتخمين نوع MIME الخاص به. يمكن العثور على قائمة كاملة بأنواع MIME والإضافات المقابلة لها في الموقع التالي:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_ (أقل حجم من)

يجب أن يحتوي الحقل تحت التحقق على _value_ كحد أدنى. يتم تقييم السلاسل والأرقام والمصفوفات والملفات بنفس طريقة تقييم قاعدة الحجم [`size`](#rule-size).

<a name="multiple-of"></a>
#### multiple_of:_value_ (مضاعفات)

يجب أن يكون الحقل تحت التحقق من مضاعفات _value_.

> {ملاحظة} ملحق bcmath PHP [`bcmath` PHP extension](https://www.php.net/manual/en/book.bc.php) مطلوب من أجل استخدام قاعدة `multi_of`.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

يجب عدم تضمين الحقل تحت التحقق في قائمة القيم المحددة. يمكن استخدام التابع `Rule :notIn` لبناء القاعدة بطلاقة:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'toppings' => [
            'required',
            Rule::notIn(['sprinkles', 'cherries']),
        ],
    ]);

<a name="rule-not-regex"></a>
#### not_regex:_pattern_ (الحقل لا يطابق التعبير العادي)

يجب ألا يتطابق الحقل تحت التحقق مع التعبير العادي المحدد.

داخليًا ، تستخدم هذه القاعدة وظيفة PHP `preg_match`. يجب أن يتبع النمط المحدد نفس التنسيق المطلوب بواسطة `preg_match` وبالتالي يتضمن أيضًا محددات صالحة. فمثلا: `'email' => 'not_regex:/^.+$/i'`.

> {ملاحظة} عند استخدام أنماط `regex` / `not_regex` ، قد يكون من الضروري تحديد قواعد التحقق من الصحة باستخدام مصفوفة بدلاً من استخدام محددات `|` ، خاصةً إذا كان التعبير العادي يحتوي على الحرف `|`.

<a name="rule-nullable"></a>
#### nullable (لاغية)

قد يكون الحقل تحت التحقق فارغاً `null`.

<a name="rule-numeric"></a>
#### numeric (أرقام)

يجب أن يكون الحقل تحت التحقق رقميًا [numeric](https://www.php.net/manual/en/function.is-numeric.php).

<a name="rule-password"></a>
#### password (كلمة سر)

يجب أن يتطابق الحقل تحت التحقق مع كلمة مرور المستخدم المصادق عليه.

> {note} تمت إعادة تسمية هذه القاعدة إلى `current_password` بهدف إزالتها في Laravel 9. الرجاء استخدام كلمة المرور الحالية [Current Password](#rule-current-password) قاعدة بدلاً من ذلك.

<a name="rule-present"></a>
#### present (فارغ)

يجب أن يكون الحقل تحت التحقق موجودًا في بيانات الإدخال ولكن يمكن أن يكون فارغًا.

<a name="rule-prohibited"></a>
#### prohibited (غير فارغ)

يجب أن يكون الحقل تحت التحقق فارغًا أو غير موجود.

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

يجب أن يكون الحقل تحت التحقق فارغًا أو غير موجود إذا كان الحقل _anotherfield_ يساوي أي _value_.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

يجب أن يكون الحقل تحت التحقق فارغًا أو غير موجود ما لم يكن الحقل _anotherfield_ يساوي أي _value_.

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

إذا كان الحقل تحت التحقق موجودًا ، فلا يمكن وجود حقول أخرى في _anotherfield_ ، حتى لو كانت فارغة.

<a name="rule-regex"></a>
#### regex:_pattern_

يجب أن يتطابق الحقل تحت التحقق مع التعبير العادي المحدد.

داخليًا ، تستخدم هذه القاعدة وظيفة PHP `preg_match`. يجب أن يتبع النمط المحدد نفس التنسيق المطلوب بواسطة `preg_match` وبالتالي يتضمن أيضًا محددات صالحة. فمثلا: `'email' => 'regex:/^.+@.+$/i'`.

> {ملاحظة} عند استخدام أنماط `regex` / `not_regex` ، قد يكون من الضروري تحديد قواعد التحقق من الصحة باستخدام مصفوفة بدلاً من استخدام محددات `|` ، خاصةً إذا كان التعبير العادي يحتوي على الحرف `|`.

<a name="rule-required"></a>
#### required (مطلوب)

يجب أن يكون الحقل تحت التحقق موجودًا في بيانات الإدخال وألا يكون فارغًا. يعتبر الحقل فارغًا "empty" إذا تحققت إحدى الشروط التالية:

<div class="content-list" markdown="1">

- القيمة خالية `null`.
- القيمة عبارة عن سلسلة فارغة.
- القيمة عبارة عن مصفوفة فارغة أو كائن قابل للعد `Countable` فارغ.
- القيمة عبارة عن ملف تم تحميله بدون مسار.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,... (مطلوب بشرط)

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا إذا كان الحقل _anotherfield_ يساوي أي قيمة _value_.

إذا كنت ترغب في إنشاء شرط أكثر تعقيدًا لقاعدة `required_if` ، فيمكنك استخدام طريقة ` Rule::requiredIf`. تقبل هذه الطريقة منطقية أو إغلاق. عند تمرير الإغلاق ، يجب أن يعرض الإغلاق صواب `true` أو خطأ `false` للإشارة إلى ما إذا كان الحقل تحت التحقق مطلوبًا:

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

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا ما لم يكن الحقل _anotherfield_ يساوي أي _value_. وهذا يعني أيضًا أن _anotherfield_ يجب أن يكون موجودًا في بيانات الطلب ما لم تكن _value_ خالية `خالية`. إذا كانت _value_ خالية `null` (`required_unless:name، null`) ، فسيكون الحقل تحت التحقق مطلوبًا ما لم يكن حقل المقارنة فارغاً `null` أو كان حقل المقارنة مفقودًا من بيانات الطلب.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا _ فقط إذا كان أي من الحقول المحددة الأخرى موجودًا وليس فارغًا.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا _ فقط إذا كانت جميع الحقول المحددة الأخرى موجودة وليست فارغة.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,... (مطلوب بدون)

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا فقط عندما يكون أي من الحقول الأخرى المحددة فارغًا أو غير موجود.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,... (مطلوب بدون الكل)

يجب أن يكون الحقل تحت التحقق موجودًا وألا يكون فارغًا فقط عندما تكون _ جميع الحقول المحددة الأخرى فارغة أو غير موجودة.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,... (مطلوب مفاتيح مصفوفة)

يجب أن يكون الحقل تحت التحقق مصفوفة ويجب أن يحتوي على الأقل على المفاتيح المحددة.

<a name="rule-same"></a>
#### same:_field_ (مساوة قيمة)

يجب أن يتطابق _field_ المقدم مع الحقل قيد التحقق.

<a name="rule-size"></a>
#### size:_value_ (مساوة حجم)

يجب أن يكون للحقل تحت التحقق حجم يطابق _value_ المعطى. بالنسبة لبيانات السلسلة ، تتوافق القيمة _value_ مع عدد الأحرف. بالنسبة إلى البيانات الرقمية ، تتوافق _value_ مع قيمة عدد صحيح معين (يجب أن تحتوي السمة أيضًا على قاعدة عدد ``numeric أو عدد صحيح  `integer`). بالنسبة إلى المصفوفة ، يتوافق _size_ مع عدد `numeric` المصفوفة. بالنسبة للملفات ، يتوافق الحجم _ مع حجم الملف بالكيلو بايت. لنلقِ نظرة على بعض الأمثلة:

    // Validate that a string is exactly 12 characters long...
    'title' => 'size:12';

    // Validate that a provided integer equals 10...
    'seats' => 'integer|size:10';

    // Validate that an array has exactly 5 elements...
    'tags' => 'array|size:5';

    // Validate that an uploaded file is exactly 512 kilobytes...
    'image' => 'file|size:512';

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,... (ابدا ب)

يجب أن يبدأ الحقل تحت التحقق بإحدى القيم المقدمة.

<a name="rule-string"></a>
#### string (ابدء)

يجب أن يكون الحقل تحت التحقق سلسلة. إذا كنت تريد السماح للحقل بأن يكون "فارغًا" ، فيجب عليك تعيين القاعدة "nullable" للحقل.

<a name="rule-timezone"></a>
#### timezone (منطقة زمنية)

يجب أن يكون الحقل تحت التحقق معرّف منطقة زمنية صالحًا وفقًا لوظيفة PHP `timezone_identifiers_list`.

<a name="rule-unique"></a>
#### unique:_table_,_column_ (مطلوب:جدول،عامود)

يجب ألا يكون الحقل تحت التحقق موجودًا في جدول قاعدة البيانات المحدد.

**تحديد اسم عمود / جدول مخصص:**

بدلاً من تحديد اسم الجدول مباشرةً ، يمكنك تحديد نموذج مساوي الذي يجب استخدامه لتحديد اسم الجدول:

    'email' => 'unique:App\Models\User,email_address'

يمكن استخدام خيار العمود `column` لتحديد عمود قاعدة البيانات المقابل للحقل. إذا لم يتم تحديد خيار `column` ، فسيتم استخدام اسم الحقل تحت التحقق كاسم للعامود.

    'email' => 'unique:users,email_address'

**تحديد اتصال قاعدة بيانات مخصص**

من حين لآخر ، قد تحتاج إلى تعيين اتصال مخصص لاستعلامات قاعدة البيانات التي يتم إجراؤها بواسطة Validator. لتحقيق ذلك ، يمكنك إضافة اسم الاتصال إلى اسم الجدول مسبقًا:

    'email' => 'unique:connection.users,email_address'

**فرض قاعدة فريدة لتجاهل معرف معين:**

في بعض الأحيان ، قد ترغب في تجاهل معرف معين أثناء التحقق الفريد من الصحة. على سبيل المثال ، ضع في اعتبارك شاشة "تحديث ملف التعريف" التي تتضمن اسم المستخدم وعنوان البريد الإلكتروني والموقع. ربما تريد التحقق من أن عنوان البريد الإلكتروني فريد. ومع ذلك ، إذا قام المستخدم بتغيير حقل الاسم فقط وليس حقل البريد الإلكتروني ، فلن ترغب في إلقاء خطأ في التحقق من الصحة لأن المستخدم هو بالفعل مالك عنوان البريد الإلكتروني المعني.

لتوجيه المدقق لتجاهل معرف المستخدم ، سنستخدم فئة `Rule` لتعريف القاعدة بطلاقة. في هذا المثال ، سنحدد أيضًا قواعد التحقق من الصحة كمصفوفة بدلاً من استخدام الحرف `|` لتحديد القواعد:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::unique('users')->ignore($user->id),
        ],
    ]);

> {ملاحظة} يجب ألا تمرر أبدًا أي إدخال طلب يتحكم فيه المستخدم إلى طريقة `ignore`. بدلاً من ذلك ، يجب عليك فقط تمرير معرف فريد تم إنشاؤه من قبل النظام مثل معرف التزايد التلقائي أو UUID من مثيل نموذج Eloquent. خلاف ذلك ، سيكون تطبيقك عرضة لهجوم حقن SQL.

بدلاً من تمرير قيمة مفتاح النموذج إلى طريقة `ignore` ، يمكنك أيضًا تمرير مثيل النموذج بالكامل. سيستخرج Laravel المفتاح تلقائيًا من النموذج:

    Rule::unique('users')->ignore($user)

إذا كان الجدول الخاص بك يستخدم اسم عمود مفتاح أساسي بخلاف `id` ، فيمكنك تحديد اسم العمود عند استدعاء طريقة `ignore`:

    Rule::unique('users')->ignore($user->id, 'user_id')

بشكل افتراضي ، ستتحقق القاعدة `unique` من تفرد العمود الذي يطابق اسم السمة التي يتم التحقق من صحتها. ومع ذلك ، يمكنك تمرير اسم عمود مختلف باعتباره الوسيطة الثانية للتابع `unique`:

    Rule::unique('users', 'email_address')->ignore($user->id),

**إضافة بنود مكان إضافية:**

يمكنك تحديد شروط طلب بحث إضافية عن طريق تخصيص الاستعلام باستخدام طريقة `where`. على سبيل المثال ، دعنا نضيف شرط استعلام يحدد نطاق الاستعلام لسجلات البحث التي تحتوي على قيمة عمود معرف_الحساب `account_id` `1`:

    'email' => Rule::unique('users')->where(function ($query) {
        return $query->where('account_id', 1);
    })

<a name="rule-url"></a>
#### url (رابط)

يجب أن يكون الحقل تحت التحقق عنوان URL صالحًا.

<a name="rule-uuid"></a>
#### uuid

يجب أن يكون الحقل تحت التحقق RFC 4122 صالحًا (الإصدار 1 أو 3 أو 4 أو 5) معرّفًا فريدًا عالميًا (UUID).

<a name="conditionally-adding-rules"></a>
## Conditionally Adding Rules (إضافة القواعد بشكل مشروط)

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### Skipping Validation When Fields Have Certain Values (تخطي التحقق من الصحة عندما تحتوي الحقول على قيم معينة)

قد ترغب في بعض الأحيان في عدم التحقق من صحة حقل معين إذا كان حقل آخر له قيمة معينة. يمكنك تحقيق ذلك باستخدام قاعدة التحقق من شرط مستبعد `exclude_if`. في هذا المثال ، لن يتم التحقق من حقلي موعد التاريخ `appointment_date` و اسم الطبيب `doctor_name` إذا كان الحقل موعد المواعيد `has_appointment` يحتوي على قيمة خطأ `false`:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_if:has_appointment,false|required|date',
        'doctor_name' => 'exclude_if:has_appointment,false|required|string',
    ]);

بدلاً من ذلك ، يمكنك استخدام قاعدة استبعاد غير `exclude_unless` لعدم التحقق من صحة حقل معين ما لم يكن هناك حقل آخر له قيمة معينة:

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
        'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
    ]);

<a name="validating-when-present"></a>
#### Validating When Present (التحقق من صحة عند التقديم)

في بعض الحالات ، قد ترغب في إجراء عمليات التحقق من الصحة مقابل حقل **فقط** إذا كان هذا الحقل موجودًا في البيانات التي يتم التحقق من صحتها. لإنجاز ذلك بسرعة ، أضف القاعدة `sometimes` إلى قائمة القواعد الخاصة بك:

    $v = Validator::make($data, [
        'email' => 'sometimes|required|email',
    ]);

في المثال أعلاه ، لن يتم التحقق من صحة حقل `email` إلا إذا كان موجودًا في المصفوفة `$data`.

> {نصيحة} إذا كنت تحاول التحقق من صحة حقل يجب أن يكون دائمًا موجودًا ولكن قد يكون فارغًا ، فقم بإلغاء تحديده (هذه المذكرة في الحقول الاختيارية) [this note on optional fields](#a-note-on-optional-fields).

<a name="complex-conditional-validation"></a>
#### Complex Conditional Validation (المصادقة الشرطية المعقدة)

قد ترغب أحيانًا في إضافة قواعد تحقق تستند إلى منطق شرطي أكثر تعقيدًا. على سبيل المثال ، قد ترغب في طلب حقل معين فقط إذا كانت قيمة حقل آخر أكبر من 100. أو قد تحتاج إلى حقلين للحصول على قيمة معينة فقط عند وجود حقل آخر. لا يجب أن تكون إضافة قواعد التحقق هذه مزعجة. أولاً ، قم بإنشاء مثيل `Validator` بقواعدك الثابة التي لا تتغير أبدًا:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'email' => 'required|email',
        'games' => 'required|numeric',
    ]);

لنفترض أن تطبيق الويب الخاص بنا مخصص لهواة جمع الألعاب. إذا قام أحد جامعي الألعاب بالتسجيل في تطبيقنا وكان لديهم أكثر من 100 لعبة ، فنحن نريدهم توضيح سبب امتلاكهم للعديد من الألعاب. على سبيل المثال ، ربما يديرون متجرًا لإعادة بيع الألعاب ، أو ربما يستمتعون فقط بجمع الألعاب. لإضافة هذا المطلب بشكل مشروط ، يمكننا استخدام طريقة "أحيانًا" في مثيل `Validator`.

    $validator->sometimes('reason', 'required|max:500', function ($input) {
        return $input->games >= 100;
    });

المعامل الأول الذي يتم تمريره إلى الأسلوب `sometimes` هو اسم الحقل الذي نتحقق منه بشروط. الوسيطة الثانية هي قائمة بالقواعد التي نريد إضافتها. إذا تم تمرير الإغلاق لأن الوسيطة الثالثة ترجع `true` ، فستتم إضافة القواعد. تجعل هذه الطريقة إنشاء عمليات تحقق شرطية معقدة أمرًا في غاية السهولة. يمكنك أيضًا إضافة عمليات تحقق شرطية لعدة حقول في وقت واحد:

    $validator->sometimes(['reason', 'cost'], 'required', function ($input) {
        return $input->games >= 100;
    });

> {نصيحة} ستكون المعلمة `$input` التي تم تمريرها إلى الإغلاق الخاص بك نسخة من ` Illuminate\Support\Fluent` ويمكن استخدامها للوصول إلى المدخلات والملفات الخاصة بك تحت التحقق.

<a name="complex-conditional-array-validation"></a>
#### Complex Conditional Array Validation (مصفوفة شرطية معقدة)

قد ترغب أحيانًا في التحقق من صحة حقل استنادًا إلى حقل آخر في نفس المصفوفة المتداخلة التي لا تعرف فهرسها. في هذه الحالات ، قد تسمح لإغلاقك باستلام وسيطة ثانية والتي ستكون العنصر الفردي الحالي في المصفوفة التي يتم التحقق من صحتها:

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

مثل المعلمة `$input` التي تم تمريرها إلى الإغلاق ، فإن المعلمة `$item` هي مثيل لـ `Illuminate\Support\Fluent` عندما تكون بيانات السمة عبارة عن مصفوفة ؛ وإلا فهو عبارة عن سلسلة.

<a name="validating-arrays"></a>
## Validating Arrays (التحقق من صحة المصفوفات)

كما تمت مناقشته في وثائق قاعدة التحقق من صحة المصفوفة [`array` validation rule documentation](#rule-array), تقبل قاعدة المصفوفة `array` قائمة بمفاتيح الصفيف المسموح بها. في حالة وجود أي مفاتيح إضافية داخل المصفوفة ، سيفشل التحقق من الصحة:

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

بشكل عام ، يجب عليك دائمًا تحديد مفاتيح المصفوفة المسموح لها بالتواجد داخل المصفوفة الخاصة بك. وبخلاف ذلك ، ستعيد أساليب `validate` و `validated` الخاصة بالمدقق جميع البيانات التي تم التحقق من صحتها ، بما في ذلك المصفوفة وجميع مفاتيحها ، حتى لو لم يتم التحقق من صحة هذه المفاتيح بواسطة قواعد أخرى للتحقق من صحة المصفوفة المتداخلة.

<a name="validating-nested-array-input"></a>
### Validating Nested Array Input (التحقق من صحة إدخال المصفوفة المتداخلة)

لا يجب أن يكون التحقق من صحة حقول إدخال النموذج القائمة على المصفوفة المتداخلة أمرًا صعبًا. يمكنك استخدام "تدوين النقطة" للتحقق من صحة السمات داخل المصفوفة. على سبيل المثال ، إذا كان طلب HTTP الوارد يحتوي على حقل `photos[profile]` ، فيمكنك التحقق من صحته كما يلي:

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'photos.profile' => 'required|image',
    ]);

يمكنك أيضًا التحقق من صحة كل عنصر من عناصر المصفوفة. على سبيل المثال ، للتحقق من أن كل بريد إلكتروني في حقل إدخال مصفوفة معين فريد ، يمكنك القيام بما يلي:

    $validator = Validator::make($request->all(), [
        'person.*.email' => 'email|unique:users',
        'person.*.first_name' => 'required_with:person.*.last_name',
    ]);

وبالمثل ، يمكنك استخدام الحرف `*` عند تحديد رسائل تحقق مخصصة في ملفات لغتك [custom validation messages in your language files](#custom-messages-for-specific-attributes), مما يجعل من السهل استخدام رسالة تحقق واحدة للحقول القائمة على المصفوفة:

    'custom' => [
        'person.*.email' => [
            'unique' => 'Each person must have a unique email address',
        ]
    ],

<a name="accessing-nested-array-data"></a>
#### Accessing Nested Array Data (الوصول إلى بيانات المصفوفة المتداخلة)

قد تحتاج أحيانًا إلى الوصول إلى قيمة عنصر مصفوفة متداخلة عند تعيين قواعد التحقق من الصحة إلى السمة. يمكنك إنجاز ذلك باستخدام طريقة `Rule::forEach`. يقبل الأسلوب `forEach` إغلاقًا سيتم استدعاؤه لكل تكرار لسمة المصفوفة تحت التحقق من الصحة وسيتلقى قيمة السمة واسم السمة الصريح الموسع بالكامل. يجب أن يعيد الإغلاق مصفوفة من القواعد لتعيينها لعنصر المصفوفة:

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
## Validating Passwords (التحقق من صحة كلمات المرور)

للتأكد من أن كلمات المرور ذات مستوى مناسب من التعقيد ، يمكنك استخدام كائن قاعدة `Password` الخاص بـ Laravel:

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rules\Password;

    $validator = Validator::make($request->all(), [
        'password' => ['required', 'confirmed', Password::min(8)],
    ]);

يسمح لك كائن قاعدة `password` بتخصيص متطلبات تعقيد كلمة المرور لتطبيقك بسهولة ، مثل تحديد أن كلمات المرور تتطلب حرفًا واحدًا أو رقمًا أو رمزًا أو أحرفًا ذات غلاف مختلط:

    // تتطلب 8 أحرف على الأقل ...
    Password::min(8)

    // تتطلب حرفًا كبيرًا واحدًا على الأقل ...
    Password::min(8)->letters()

    // تتطلب حرفًا كبيرًا واحدًا وحرفًا صغيرًا واحدًا على الأقل ...
    Password::min(8)->mixedCase()

    // يتطلب رقمًا واحدًا على الأقل ...
    Password::min(8)->numbers()

    // مطلوب رمز واحد على الأقل ...
    Password::min(8)->symbols()

بالإضافة إلى ذلك ، يمكنك التأكد من أن كلمة المرور لم يتم اختراقها في عملية تسريب لخرق بيانات كلمة المرور العامة باستخدام طريقة `uncompromised`:

    Password::min(8)->uncompromised()

داخليًا ، يستخدم كائن قاعدة `Password` إخفاء الهوية  [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) mأوديل لتحديد ما إذا كان قد تم تسريب كلمة المرور عبر [haveibeenpwned.com](https://haveibeenpwned.com) الخدمة دون التضحية بخصوصية المستخدم أو أمانه.

بشكل افتراضي ، إذا ظهرت كلمة المرور مرة واحدة على الأقل في تسرب البيانات ، فسيتم اعتبارها مخترقة. يمكنك تخصيص هذا الحد باستخدام الوسيطة الأولى للطريقة `uncompromised`:

    // تأكد من ظهور كلمة المرور أقل من 3 مرات في نفس تسريب البيانات ...
    Password::min(8)->uncompromised(3);

بالطبع ، يمكنك ربط جميع التوابع في الأمثلة أعلاه:

    Password::min(8)
        ->letters()
        ->mixedCase()
        ->numbers()
        ->symbols()
        ->uncompromised()

<a name="defining-default-password-rules"></a>
#### تحديد قواعد كلمة المرور الافتراضية

قد تجد أنه من الملائم تحديد قواعد التحقق الافتراضية لكلمات المرور في مكان واحد من تطبيقك. يمكنك إنجاز ذلك بسهولة باستخدام طريقة `Password::defaults` التي تقبل الإغلاق. يجب أن يعيد الإغلاق الممنوح لطريقة `defaults` التكوين الافتراضي لقاعدة كلمة المرور. عادةً ، يجب استدعاء قاعدة `defaults` في طريقة `boot`  لأحد مزودي خدمة التطبيق الخاص بك:

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

بعد ذلك ، عندما ترغب في تطبيق القواعد الافتراضية على كلمة مرور معينة تخضع للتحقق ، يمكنك استدعاء التابع `defaults` بدون وسيطات:

    'password' => ['required', Password::defaults()],

من حين لآخر ، قد ترغب في إرفاق قواعد تحقق إضافية بقواعد التحقق من صحة كلمة المرور الافتراضية. يمكنك استخدام التابع `rules` لإنجاز هذا:

    use App\Rules\ZxcvbnRule;

    Password::defaults(function () {
        $rule = Password::min(8)->rules([new ZxcvbnRule]);

        // ...
    });

<a name="custom-validation-rules"></a>
## Custom Validation Rules (قواعد التحقق من الصحة المخصصة)

<a name="using-rule-objects"></a>
### Using Rule Objects (استخدام كائنات القاعدة)

يوفر Laravel مجموعة متنوعة من قواعد التحقق المفيدة ؛ ومع ذلك ، قد ترغب في تحديد بعض ما يخصك. تتمثل إحدى طرق تسجيل قواعد التحقق المخصصة في استخدام كائنات القاعدة. لإنشاء كائن قاعدة جديدة ، يمكنك استخدام الأمر `make:rule` Artisan. دعنا نستخدم هذا الأمر لإنشاء قاعدة تتحقق من أن السلسلة أحرف كبيرة. سيضع Laravel القاعدة الجديدة في مجلد `app/Rules`. إذا لم يكن هذا المجلد موجودًا ، فسيقوم Laravel بإنشائه عند تنفيذ الأمر Artisan لإنشاء القاعدة الخاصة بك:

```shell
php artisan make:rule Uppercase
```

بمجرد إنشاء القاعدة ، نكون مستعدين لتحديد سلوكها. يحتوي كائن القاعدة على طريقتين: `passes` و` message`. يتلقى الأسلوب `passes` قيمة السمة واسمها ، ويجب أن يعرض `true` أو `false` بناءً على ما إذا كانت قيمة السمة صالحة أم لا. يجب أن تُرجع الطريقة `message` رسالة خطأ التحقق التي يجب استخدامها عند فشل التحقق:

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

يمكنك استدعاء المساعد `trans` من طريقة `message` إذا كنت ترغب في إرجاع رسالة خطأ من ملفات الترجمة الخاصة بك:

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return trans('validation.uppercase');
    }

بمجرد تحديد القاعدة ، يمكنك إرفاقها بمدقق عن طريق تمرير مثيل لكائن القاعدة مع قواعد التحقق الأخرى الخاصة بك:

    use App\Rules\Uppercase;

    $request->validate([
        'name' => ['required', 'string', new Uppercase],
    ]);

#### Accessing Additional Data

إذا كانت فئة قاعدة التحقق المخصصة تحتاج إلى الوصول إلى جميع البيانات الأخرى التي تخضع للتحقق ، فقد تقوم فئة القاعدة الخاصة بك بتنفيذ واجهة `Illuminate\Contracts\Validation\DataAwareRule`. تتطلب هذه الواجهة من فصلك تحديد طريقة `setData`. سيتم استدعاء هذا التابع تلقائيًا بواسطة Laravel (قبل متابعة التحقق) مع جميع البيانات قيد التحقق:

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

أو ، إذا كانت قاعدة التحقق الخاصة بك تتطلب الوصول إلى مثيل المدقق الذي يقوم بعملية التحقق ، فيمكنك تنفيذ واجهة `ValidatorAwareRule`:

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
### Using Closures (استخدام الإغلاق)

إذا كنت تحتاج فقط إلى وظيفة القاعدة المخصصة مرة واحدة في جميع أنحاء التطبيق ، فيمكنك استخدام الإغلاق بدلاً من كائن القاعدة. يتلقى الإغلاق اسم السمة ، وقيمة السمة ، واستدعاء `$fail` الذي يجب استدعاؤه في حالة فشل التحقق:

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
### Implicit Rules (القواعد الضمنية)

بشكل افتراضي ، عندما لا تكون السمة التي يتم التحقق من صحتها موجودة أو تحتوي على سلسلة فارغة ، لا يتم تشغيل قواعد التحقق العادية ، بما في ذلك القواعد المخصصة. على سبيل المثال ، ملف [`unique`](#rule-unique) لن يتم تشغيل القاعدة مقابل سلسلة فارغة:

    use Illuminate\Support\Facades\Validator;

    $rules = ['name' => 'unique:users,name'];

    $input = ['name' => ''];

    Validator::make($input, $rules)->passes(); // true

لكي يتم تشغيل قاعدة مخصصة حتى عندما تكون السمة فارغة ، يجب أن تشير القاعدة ضمنيًا إلى أن السمة مطلوبة. لإنشاء قاعدة "ضمنية" ، قم بتنفيذ واجهة `Illuminate\Contracts\Validation\ImplicitRule`. تعمل هذه الواجهة بمثابة "واجهة علامة" (marker interface) للمدقق ؛ لذلك ، فهو لا يحتوي على أي طرق إضافية تحتاج إلى تنفيذها بخلاف الطرق التي تتطلبها واجهة "القاعدة" النموذجية.

لإنشاء كائن قاعدة ضمنية جديد ، يمكنك استخدام الأمر `make: rule` Artisan مع الخيار `--implicit` :

```shell
php artisan make:rule Uppercase --implicit
```

> {ملاحظة} القاعدة "الضمنية" فقط _ تشير إلى أن السمة مطلوبة. ما إذا كان يؤدي بالفعل إلى إبطال سمة مفقودة أو فارغة ، فهذا أمر متروك لك.
