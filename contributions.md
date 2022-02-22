# دليل المساهمة

- [تقارير الأخطاء](#bug-reports)
- [أسئلة الدعم](#support-questions)
- [نقاش التطوير الجوهري](#core-development-discussion)
- [ أي فرع؟](#which-branch)
- [Compiled Assets](#compiled-assets)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Coding Style](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [Code of Conduct](#code-of-conduct)

<a name="bug-reports"></a>
## تقارير الأخطاء

لتشجيع التعاون النشط، لارافيل تشجع وبقوة طلبات السحب (pull requests)، بالإضافة لتقارير الأخطاء. يمكن أيضاً إرسال "تقارير الأخطاء" بشكل طلب سحب (pull request) يحتوي على اختبار فاشل. سيتم مراجعة طلبات السحب فقط عندما يتم تعليمها كـ"جاهزة للمراجهة" ("ready for review") وليست في حالة "مسودة" ("draft") وبعد اجتياز جميع الاختبارات للميزات الجديدة. سيتم إغلاق طلبات السحب العالقة وغير النشطة التي تركت في حالة "المسودة" بعد بضعة أيام.

في كافة الأحوال، اذا قمت بتقديم تقرير خطأ، يجب أن تحتوي مشكلتك على على عنوان وشرح واضح للمشكلة. يجب عليك أيضاً تضمين أكبر قدر ممكن من المعلومات ذات الصلة وعينة من الكود البرمجي الذي يوضح المشكلة. الهدف من تقرير الخطأ هو تسهيل استنساخ الخطأ وتطوير حل بالنسبة لك وللمستخدمين الآخرين. 

تذكر، يتم إنشاء تقارير الأخطاء أملاً بأن الآخرين الذين يواجهون نفس المشكلة سيكونون قادرين على التعاون معك في حلها. لا تتوقع بأن تقرير الخطأ سوف يبحث في النشاطات تلقائياً أو أن الآخرين سيهبون لإصلاحه. إنشاء تقرير بالخطأ يأتي في صالحك أنت و الآخرين للبدء في مسار إصلاح المشكلة. إذا كنت تريد المشاركة، يمكنك المساعدة بإصلاح [أي مشكلة مدرحة في أدوات تعقب المشكلات الخاصة بنا](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). يجب عليك أن تكون قد سجلت الدخول بغيت هاب (GitHub) لرؤية جميع مشكلات لارافيل. 

شيفرة المصدر (source code) الخاصة بلارافيل تتم إداراتها على غيت هاب (GitHub)، ومستودعاتهم لك لكل مشاريع لارافيل: 

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
يمكنك اقتراح ميزات أو تحسينات لسلوك لارافيل موجود في مستودع (repository) إطار عمل لارافيل [مجلس المناقشة في غيت هاب (GitHub)](https://github.com/laravel/framework/discussions). اذا كنت تود اقتراح ميزة جديدة، رجاءً كن مستعداً لتنفيذ جزء من الكود البرمجي المطلوب  على الأقل لاتمام الميزة.

المناقشات الغير رسمية بخصوص المشاكل، الميزات الجديدة، وتنفيذ الميزات الحالية يحدث في قناة `#internals` الموجودة في [سيرفر لارافيل على ديسكورد ](https://discord.gg/laravel). تايلور أوتويل، المشرف على لارافيل، عادة ما يكون متواجد على القناة في أيام الأسبوع من الساعة 8 صباحاً - وحتى الـ5 مساءً بتوقيت الولايات المتحدة الأمريكية  (UTC-06:00 or America/Chicago)، ويكون حاضراً بشكل متقطع في القناة في أوقات أخرى. 

<a name="which-branch"></a>
## أي فرع؟

**جميع** الاصلاحات يجب أن ترسل لاخر فرع (branch) مستقر. يجب **ألا** يتم ارسل الأخطاء التي تم اصلاحها للفرع الرئيسي `master` إلا في حال كان إصلاح لميزة موجودة فقط في إصدار قادم.

قد يتم إرسال الميزات **الثانوية والمتوافقة تماماً مع الإصدارات السابقة** للإصدار الحالي إلى أحدث فرع مستقر.

دائماً يجب إرسال الميزات الجديدة **الرئيسية** إلى الفرع الرئيسي `master`، الذي يحتوي على الإصدار القادم.

إذا لم تكن متأكداً بأن ميزتك مؤهلة لتكون ميزة رئيسية أو ميزة ثانوية، رجاءً اسأل تايلور أوتويل في قناة `#internals` الموجودة في [سيرفر لارافيل على ديسكورد ](https://discord.gg/laravel).

<a name="compiled-assets"></a>
## Compiled Assets

If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers.

<a name="security-vulnerabilities"></a>
## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an email to Taylor Otwell at <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. All security vulnerabilities will be promptly addressed.

<a name="coding-style"></a>
## Coding Style

Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard.

<a name="phpdoc"></a>
### PHPDoc

Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name:

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
### StyleCI

Don't worry if your code styling isn't perfect! [StyleCI](https://styleci.io/) will automatically merge any style fixes into the Laravel repository after pull requests are merged. This allows us to focus on the content of the contribution and not the code style.

<a name="code-of-conduct"></a>
## Code of Conduct

The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com):

<div class="content-list" markdown="1">

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always assume good intentions.
- Behavior that can be reasonably considered harassment will not be tolerated.

</div>
