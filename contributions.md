# دليل المساهمة

- [تقارير الأخطاء](#bug-reports)
- [أسئلة الدعم](#support-questions)
- [نقاش التطوير الجوهري](#core-development-discussion)
- [ أي فرع؟](#which-branch)
- [الملفات المترجمة (Compiled Assets)](#compiled-assets)
- [الثغرات الأمنية](#security-vulnerabilities)
- [تنسيق الكود](#coding-style)
    - [توثيق PHP](#phpdoc)
    - [أداة StyleCI](#styleci)
- [القواعد السلوكية](#code-of-conduct)

<a name="bug-reports"></a>
## تقارير الأخطاء

لتشجيع التعاون النشط، لارافيل تشجع وبقوة طلبات السحب (pull requests)، بالإضافة لتقارير الأخطاء. ويمكن أيضاً إرسال "تقارير الأخطاء" بشكل طلب سحب (pull request) يحتوي على اختبار فشل. سيتم مراجعة طلبات السحب فقط عندما يتم تعليمها كـ"جاهزة للمراجهة" ("ready for review") وليست في حالة "مسودة" ("draft") وبعد اجتياز جميع الاختبارات للميزات الجديدة المضافة. سيتم إغلاق طلبات السحب العالقة وغير النشطة التي تركت في حالة "المسودة" بعد بضعة أيام.

في كافة الأحوال، اذا قمت بتقديم تقرير خطأ، يجب أن تحتوي مشكلتك على على عنوان وشرح واضح للمشكلة. يجب عليك أيضاً تضمين أكبر قدر ممكن من المعلومات ذات الصلة وعينة من الكود البرمجي الذي يوضح المشكلة. إن الهدف من تقرير الخطأ هو تسهيل استنساخ الخطأ وتطوير حل للمشكلة لك وللمستخدمين الآخرين. 

تذكر، يتم إنشاء تقارير الأخطاء أملاً بأن الآخرين الذين يواجهون نفس المشكلة سيكونون قادرين على التعاون معك في حلها. لا تتوقع بأن تقرير الخطأ سوف يبحث في النشاطات تلقائياً أو أن الآخرين سيهبون لإصلاحه. إنشاء تقرير بالخطأ يأتي في صالحك أنت و الآخرين للبدء في مسار إصلاح المشكلة. إذا كنت تريد المشاركة، يمكنك المساعدة بإصلاح [أي مشكلة مدرحة في أدوات تعقب المشكلات الخاصة بنا](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). يجب عليك أن تكون قد سجلت الدخول بغيت هاب (GitHub) لرؤية جميع مشكلات لارافيل. 

شيفرة المصدر (source code) الخاصة بلارافيل تتم إداراتها على غيت هاب (GitHub)، ومستودعاتهم لكل مشاريع لارافيل هي: 

<div class="content-list" markdown="1">

- [تطبيق لارافيل (Laravel Application)](https://github.com/laravel/laravel)
- [رسومات لارافيل (Laravel Art)](https://github.com/laravel/art)
- [توثيق لارافيل (Laravel Documentation)](https://github.com/laravel/docs)
- [لارافيل داسك (Laravel Dusk)](https://github.com/laravel/dusk)
- [لارافيل كاشيير سترايب (Laravel Cashier Stripe)](https://github.com/laravel/cashier)
- [لارافيل كاشيير بادل (Laravel Cashier Paddle)](https://github.com/laravel/cashier-paddle)
- [لارافيل_ايكو (Laravel Echo)](https://github.com/laravel/echo)
- [لارافيل اينفوي (Laravel Envoy)](https://github.com/laravel/envoy)
- [إطار عمل لارافيل (Laravel Framework)](https://github.com/laravel/framework)
- [لارافيل هومستيد (Laravel Homestead)](https://github.com/laravel/homestead)
- [سكربتات بناء لارافيل هومستيد (Laravel Homestead Build Scripts)](https://github.com/laravel/settler)
- [لارافيل هورايزن (Laravel Horizon)](https://github.com/laravel/horizon)
- [لارافيل جيت ستريم (Laravel Jetstream)](https://github.com/laravel/jetstream)
- [لارافيل باسبورت (Laravel Passport)](https://github.com/laravel/passport)
- [لارافيل سيل (Laravel Sail)](https://github.com/laravel/sail)
- [لارافيل سانكتوم (Laravel Sanctum)](https://github.com/laravel/sanctum)
- [لارافيل سكاوت (Laravel Scout)](https://github.com/laravel/scout)
- [لارافيل سوشيلايت (Laravel Socialite)](https://github.com/laravel/socialite)
- [لارافيل تيليسكوب (Laravel Telescope)](https://github.com/laravel/telescope)
- [موقع لارافيل (Laravel Website)](https://github.com/laravel/laravel.com-next)

</div>

<a name="support-questions"></a>
## أسئلة الدعم

أدوات تتبع أخطاء لارافيل على غيت هاب (GitHub) ليست لتقديم الدعم أو المساعدة بخصوص لارافيل. بدلاً من ذلك، استعمل احدى القنوات التالية لطلب المساعدة:

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## نقاش التطوير الجوهري

يمكنك اقتراح ميزات أو تحسينات لسلوك لارافيل الموجود في مستودع (repository) إطار عمل لارافيل [مجلس المناقشة في غيت هاب (GitHub)](https://github.com/laravel/framework/discussions). اذا كنت تود اقتراح ميزة جديدة، رجاءً كن مستعداً لتنفيذ جزء من الكود البرمجي المطلوب  على الأقل لاتمام الميزة.

المناقشات الغير رسمية بخصوص المشاكل، الميزات الجديدة، وتنفيذ الميزات الحالية يحدث في قناة `#internals` الموجودة في [سيرفر لارافيل على ديسكورد ](https://discord.gg/laravel). تايلور أوتويل، المشرف على لارافيل، عادة ما يكون متواجد على القناة في أيام الأسبوع من الساعة 8 صباحاً - وحتى الـ5 مساءً بتوقيت الولايات المتحدة الأمريكية  (UTC-06:00 or America/Chicago)، ويكون حاضراً بشكل متقطع في القناة في أوقات أخرى. 

<a name="which-branch"></a>
## أي فرع؟


**جميع** الاصلاحات يجب أن ترسل لاخر فرع (branch) مستقر. يجب **ألا** يتم ارسل الأخطاء التي تم اصلاحها للفرع الرئيسي `master` إلا في حال كان إصلاح لميزة موجودة فقط في إصدار قادم.

قد يتم إرسال الميزات **الثانوية والمتوافقة تماماً مع الإصدارات السابقة** للإصدار الحالي إلى أحدث فرع مستقر.

دائماً يجب إرسال الميزات الجديدة **الرئيسية** إلى الفرع الرئيسي `master`، الذي يحتوي على الإصدار القادم.

إذا لم تكن متأكداً بأن ميزتك مؤهلة لتكون ميزة رئيسية أو ميزة ثانوية، رجاءً قم بسؤال تايلور أوتويل في قناة `#internals` الموجودة في [سيرفر لارافيل على ديسكورد ](https://discord.gg/laravel).

<a name="compiled-assets"></a>
## الملفات المترجمة (Compiled Assets)

إذا كنت تقوم بتغيير يؤثر على ملف مترجم (compiled file)، مثل معظم الملفات في `resources/css` أو  `resources/js` في مستودع `laravel/laravel`، لا تقوم بعمل (commit) للملفات المترجمة. لأنه ونظراً لحجمها الكبير، لايمكن مراجعتها بشكل واقعي وجيد من قبل المشرفين، حيث يمكن استغلال هذا الأمر لحقن كود ضار ضمن لارافيل. في إطار الحماية الدفاعية من هذه المشكلة، كل الملفات المترجمة سيتم إنشائها وعمل (commit) لها من قبل مشرفي لارافيل.  

<a name="security-vulnerabilities"></a>
## الثغرات الأمنية

اذا قمت باكتشاف ثغرة أمنية في لارافيل، رجاءً قم بإرسال بريد الكتروني لتايلور أوتويل على البريد التالي <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. سيتم معالجة كل الثغرات الأمنية على الفور. 

<a name="coding-style"></a>
## تنسيق الكود

تتبع لارافيل معيار التكويد [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) ومعيار التحميل التلقائي  [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md). 

<a name="phpdoc"></a>
### توثيق PHP

المثال في الأسفل يعبر عن كتلة توثيق لارافيل سليمة، لاحظ بأن الخاصية `@param` متبوعة بفراغين، من ثم نوع الوسيط، من ثم فراغين، واسم المتحول في النهاية: 

    /**
     * Register a binding with the container.
     *
     * @param  string|array  $abstract
     * @param  \Closure|string|null  $concrete
     * @param  bool  $shared
     * @return void
     *
     * @throws \Exception
     */
    public function bind($abstract, $concrete = null, $shared = false)
    {
        //
    }

<a name="styleci"></a>
### أداة StyleCI

لا تقلق اذا كان تنسيق الكود الخاص بك غير مثالي! [أداة StyleCI](https://styleci.io/) تقوم اتوماتيكياً بإصلاح التنسيقات في مستودع لارافيل بعد دمج (merge) عملية سحب الطلب (pull requests). مما يمكننا من التركيز على محتوى المساهمة بدلاً من تنسيق الكود. 

<a name="code-of-conduct"></a>
## القواعد السلوكية

القواعد السلوكية الخاصة بلارافيل مشتقة من القواعد السلوكية الخاصة بروبي (Ruby). يمكن تبليغ عن أي انتهاكات للقواعد السلوكية لتايلور أوتويل (taylor@laravel.com): 

<div class="content-list" markdown="1">

- يجب على المساهمين أن يكونو متسامحين ويتحملو وجهات النظر المخالفة.
- يجب على المساهمين التأكد من أن لغتهم وأفعالهم خالية من أي تهجم شخصي أو تعليقات شخصية مسيئة. 
- يجب على المساهمين عند تفسير أقوال وأفعال الآخرين افتراض حسن النية دوماً. 
- لن يتم التسامح مع أي سلوك يمكن اعتباره مضايقة.  

</div>