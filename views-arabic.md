# الواجهات (Views)

- [مقدمة](#introduction)
- [Creating & Rendering Views](#creating-and-rendering-views)
    - [Nested View Directories](#nested-view-directories)
    - [Creating The First Available View](#creating-the-first-available-view)
    - [Determining If A View Exists](#determining-if-a-view-exists)
- [Passing Data To Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
    - [View Creators](#view-creators)
- [Optimizing Views](#optimizing-views)

<a name="introduction"></a>
## مقدمة

بالطبع ، ليس من العملي إرجاع سلاسل مستندات HTML بالكامل مباشرةً من المسارات (paths) والمتحكمات الخاصة بك (controllers). لحسن الحظ ، توفر الواجهات طريقة مناسبة لوضع كل HTML في ملفات منفصلة. تفصل الواجهات منطق وحدة التحكم / منطق التطبيق عن منطق عرضك التقديمي  (presentation logic) ويتم تخزين الواجهات في المجلد `resources/view`. قد تشبه الواجهة البسيطة المثال التالي:

```blade
<!-- الواجهات المُخزّنة في resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```
نظراً لأن هذه الواجهة مخزنة في `resources/views/greeting.blade.php` ، يمكننا ارجاعها باستخدام المساعد العام `view` مثل:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });


> ملاحظة: هل تبحث عن مزيد من المعلومات حول كيفية كتابة قوالب Blade؟ ألق نظرة على [توثيق Blade](/docs/{{version}}/blade) الكامل للبدء.


