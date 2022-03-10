# التنصيب

- [قابل لارافل](#meet-laravel)
    - [لماذا لارافل؟](#why-laravel)
- [مشروعك الأول مع لارافل](#your-first-laravel-project)
    - [البدء على macOS](#getting-started-on-macos)
    - [البدء على Windows](#getting-started-on-windows)
    - [البدء على Linux](#getting-started-on-linux)
    - [اختيار خدمات Sail التي تحتاجها](#choosing-your-sail-services)
    - [التنصيب باستخدام مدير الحزم (composer)](#installation-via-composer)
- [الإعدادات الابتدائية](#initial-configuration)
    - [إعدادات المبنية على البيئة](#environment-based-configuration)
    - [إعدادات الدليل (directory)](#directory-configuration)
- [الخطوات التالية](#next-steps)
    - [لارافل إطار عمل المكدس الكامل (Full Stack)](#laravel-the-fullstack-framework)
    - [لارافل واجهة التخاطب الخلفية (Backend API)](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## قابل لارافل

 لارافل هي إطار عمل لتطبيقات الويب بتركيب جمل بليغ وأنيق. يوف إطار عمل تطبيقات الويب بنية (Structure) ونقطة بداية لإنشاء مشروعك، مما يسمح لك بالتركيز على بناء شيء رائع بينما نحن نتعب في التفاصيل.

تسعى لارافل جاهدةً لتقديم تجرِبة مطور رائعة بينما تقدم ميزات قوية كحقن التبعية الشامل (Thorough Dependency Injection)، طبقة تجريد قاعدة البيانات التعبيرية (Expressive Database Abstraction Layer)،الطوابير (Queues) والمهام المجدولة (Scheduled Jobs)، اختبارت الوحدات البرمجية وتكاملها ودمجها مع بعض (Unit & Integration Testing)، والكثير.

سواء كنت جديداً على PHP أو إطر عمل الويب أو لديك سنوات من الخبرة، لارافل هي إطار العمل الذي يمكنه أن يكبر معك. سنساعدك لتأخذ خطواتك الا,لى كمطور ويب أو سنعطيك دفعة بينما تأخذ خبرتك إلى المستوى التالي. لا يسعنا الانتظار لنرى ما تبنيه.

<a name="why-laravel"></a>
### لماذا لارافل؟

هنك تنوع في الأدوات وأطر العمل المتوفرة لك عند بناء تطبيق ويب. ومع ذلك نعتقد أن لارافل هي أفضل خِيار لبناء تطبيقات ويب حديثة كاملة المكدس (Full Stack).

#### إطار عمل تقدمي

نحب أن ندعو لارافل إطار عمل "تقدمي". نعني بذلك أن لارافل تنمو معك. إن كنت تأخذ خطواتك الأولى في تطوير المواقع، مكتبة لارافل الواسع من التوثيق، الأدلة الإرشادية والفيديوهات التعليمية ستساعدك على تعلم إنجاز المهام دون أن ترتبك.

إن كنت مطوراً خبيراً، تعطيك لارافل أدوات قوية [لحقن التبعية](/docs/{{version}}/container) (Dependency Injection)، [اختبار الوحدة البرمجية](/docs/{{version}}/testing) (Unit Testing)، [الطوابير](/docs/{{version}}/queues) (Queues)، [أحداث الوقت الحقيقي](/docs/{{version}}/broadcasting) (Real-time Events)، وأكثر.

#### إطار عمل قابل للتوسيع

إن لارافل قابلة للتوسيع بشكل لا يصدق. بفضل طبيعة PHP الملائمة للتوسع ودعم Laravel المدمج لأنظمة التخزين المؤقت (Cache) السريعة والموزعة مثل Redis، التوسيع الأفقي (Horizontal Scaling) مع لارافل سهل للغاية. في الواقع، وُسِعَت تطبيقات Laravel بسهولة للتعامل مع مئات الملايين من الطلبات شهريًا.

هل تحتاج لتوسيع مهول؟ تسمح منصات مثل [Laravel Vapor](https://vapor.laravel.com) بتشغيل تطبيق لارافل الخاص بك على نطاق غير محدود تقريباً على أحدث تقنيات AWS بدون خادم (Serverless).

#### إطار عمل للمجتمع

تجمع لارافل أفضل الحزم (Packages) في نظام PHP البيئي (PHP Ecosystem) لتقدم أقوى وأسهل إطار عمل للمطورين. بالإضافة لذلك، [ساهم](https://github.com/laravel/framework) آلاف المطورين الموهوبين حول العالم في لارافل

<a name="your-first-laravel-project"></a>
## مشروعك الأول مع لارافل
إن كنت أن تبدأ بأسهل طريقة ممكنة مع لارافل. يوجد العديد من الخيارات لتطوير وتشغيل مشروع لارافل على حاسبك الشخصي. بينما قد ترغب باستكشاف هذه الخيارات في وقت لاحق، لارافل تقدم [خدمة Sail](/docs/{{version}}/sail)، وهي حل مدمج لتشغيل مشروع لارافل باستخدام منصة الحاويات [Docker](https://www.docker.com).

منصة الحاويات (Docker) هي أداة لتشغيل التطبيقات والخدمات في "حاويات" صغيرة وخفيفة والتي لا تتداخل مع البرمجيات المنصبة على حاسبك الشخصي أو عداداته. هذا يعني أنه ليس عليك أن تقلق حول تنصيب أدوات التطوير المعقدة مثل مخدمات الويب وقواعد البيانات على حاسبك الشخصي. لتبدأ، كل ما عليك هو تنصيب برنامج [Docker Desktop](https://www.docker.com/products/docker-desktop).

شراع لارافل (Laravel Sail) هو واجهة خفيفة لموجه الأوامر (command-line) مخصصة للتعامل مع إعدادات لارافل الخاصة بمنصة الحاويات (Docker). تقدم خدمة Sail نقطة بداية رائعة لبناء تطبيق لارافل باستخدام لغة PHP، محركة قواعد البيانات MYSQL، ومخزن البيانات Redis دون الحاجة لأي خبرة مسبقة عن منصة الحاويات Docker.

> {نصيحة}هل انت خبير بمنصة الحاويات Docker؟ لا تقلق! كل شي في واجهة Sail يمكن تخصيصه باستخدام ملف `docker-compose.yml`الموجود مع لارافل

<a name="getting-started-on-macos"></a>
### البدء على MacOS
إنك كنت تستعمل جهاز ماك ولديك برنامج [Docker Desktop](https://www.docker.com/products/docker-desktop) مٌنصب على جهازك. يمكنك استخدام أمر بسيط في موجه الأوامر (terminal) لإنشاء مشروع لارافل جديد. على سبيل المثال، لإنشاء تطبيق لارافل جديد في مجلد اسمه "example-app"، يمكنك تشغيل الأمر الآتي في مشغل الأوامر (terminal):

```shell
curl -s "https://laravel.build/example-app" | bash
```
بالطبع، يمكنك تغيير "example-app" في هذا الرابط لأي شيء تريده. مجلد تطبيق لارافل سيُنشئ داخل المجلد الذي شغلت الأمر فيه.

بعد أن أُنشئ المشروع، يمكنك الانتقال إلى مجلد التطبيق وتشغيل Laravel Sail. تقدم Laravel Sail واجهة بسيطة للتعامل مع إعدادات لارافل لمنصة الحاويات Docker:


```shell
cd example-app

./vendor/bin/sail up
```
 في أول مرة تشغل فيها الأمر `up`، ستُبنى حاويات التطبيق التي في Sail على جهازك. سيستغق هذا الأمر عدة دقائق. **ولكن لا تقلق، المحاولات القادمة لتشغيل Sail ستكون أسرع بكثير.**

بمجرد أن بدأت حاويات Docker الخاصة بمشروعك، يمكنك الوصول إلى مشروعك في متصف الويب على هذا الرابط: http://localhost.

> {نصيحة} لتتعلم المزيد عن Laravel Sail، اقرأ [توثيقها الكامل](/docs/{{version}}/sail).

<a name="getting-started-on-windows"></a>
### البدء على Windows
قبل أن تُنشئ مشروع جديد في باستخدام لارافل على جهازك، تأكد من تنصيب برنامج [Docker Desktop](https://www.docker.com/products/docker-desktop). بعدها، عليك التاكد من أن ميزة الأنظمة الفرعية في Windows لنظام تشغيل Linux بنسختها الثانية (Windows Subsystem for Linux 2) (WSL2) منصبة ومفعلة. خدمة WSL ستمكنك من تشغيل ملفات Linux التنفيذية على Windows 10. مكنك أن تجد معلومات عن كيفية تنصيب وتفعيل WSL2 في [توثيق بيئة التطوير لشركة مايكروسوفت](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> {نصيحة} بعد تنصيب وتفعيل WSL2K ينبغي عليك التأكد من أن برنامج Docker Desktop [معد لاستخدام WSL2(]https://docs.docker.com/docker-for-windows/wsl/)

بعد ذلك، أنت جاهز لإنشاء مشروعك الأول باستخدام لارافل. شغل موجه الأوامر [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) وابدأ جلسة جديدة لنظام تشغيل Linuxالمنصب باستخدام WSL2. ومن ثم، يمكنك استخدام موجه الأوامر لإنشاء مشروع لارافل جديد. على سبيل المثال، لإنشاء تطبيق لارافل جديد في مجلد اسمه "example-app"، يمكنك تشغيل الأمر الآتي في موجه الأوامر Terminal:

```shell
curl -s https://laravel.build/example-app | bash
```
بالطبع، يمكنك تغيير "example-app" في هذا الرابط لأي شيء تريده. سيُنشأ مجلد تطبيق لارافل داخل المجلد الذي شغلت الأمر فيه.

بعد أن أُنشئ المشروع، يمكنك الانتقال إلى مجلد التطبيق وتشغيل Laravel Sail. تقدم Laravel Sail واجهة بسيطة للتعامل مع إعدادات لارافل لمنصة الحاويات Docker:

```shell
cd example-app

./vendor/bin/sail up
```

في أول مرة تشغل فيها الأمر `up`، ستُبنى حاويات التطبيق التي في Sail على جهازك. سيستغق هذا الأمر عدة دقائق. **ولكن لا تقلق، المحاولات القادمة لتشغيل Sail ستكون أسرع بكثير.**

بمجرد أن بدأت حاويات Docker الخاصة بمشروعك، يمكنك الوصول إلى مشروعك في متصف الويب على هذا الرابط: http://localhost.

> {نصيحة} لتتعلم المزيد عن Laravel Sail، اقرأ [توثيقها الكامل](/docs/{{version}}/sail).

#### التطوير داخل WSL2
بالطبع، ستحتاج أن تكون قادراً على تعديل ملفات تطبيق لارافل التي أٌنشأت داخل WSL2. لتتمكن من ذلك، ننصحك باستخدام محرر [Visual Studio Code](https://code.visualstudio.com) المطور لدى شركة مايكروسوفت مع تنصيب إضافة [التطوير البعيد (Remote Development)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

بمجرد أن نُصبت هذه الأدوات، يمكنك فتح أي مشروع لارافل بتشغيل الأمر `code .` داخل المجلد الرئيسي للتطبيق باستخدام موجه الأوامر (Windows Terminal)

<a name="getting-started-on-linux"></a>
### البدء على Linux
إن كنت تطور على نظام Linux ومنصب لديك برنامج [Docker Compose](https://docs.docker.com/compose/install/)، فيمكنك استخدام هذا الأمر على موجه الأوامر لإنشاء مشروع لارافل جديد.  على سبيل المثال، لإنشاء تطبيق لارافل جديد في مجلد اسمه "example-app"، يمكنك تشغيل الأمر الآتي في مشغل الأوامر (terminal):

```shell
curl -s https://laravel.build/example-app | bash
```


بالطبع، يمكنك تغيير "example-app" في هذا الرابط لأي شيء تريده. سيُنشأ مجلد تطبيق لارافل داخل المجلد الذي شغلت الأمر فيه.

بعد أن أُنشئ المشروع، يمكنك الانتقال إلى مجلد التطبيق وتشغيل Laravel Sail. تقدم Laravel Sail واجهة بسيطة للتعامل مع إعدادات لارافل لمنصة الحاويات Docker:

```shell
cd example-app

./vendor/bin/sail up
```

في أول مرة تشغل فيها الأمر `up`، ستُبنى حاويات التطبيق التي في Sail على جهازك. سيستغق هذا الأمر عدة دقائق. **ولكن لا تقلق، المحاولات القادمة لتشغيل Sail ستكون أسرع بكثير.**

بمجرد أن بدأت حاويات Docker الخاصة بمشروعك، يمكنك الوصول إلى مشروعك في متصف الويب على هذا الرابط: http://localhost.

> {نصيحة} لتتعلم المزيد عن Laravel Sail، اقرأ [توثيقها الكامل](/docs/{{version}}/sail).

<a name="choosing-your-sail-services"></a>
### اختيار خدمات Sail التي تحتاجها

عند إنشاء تطبيق لارافل باستخدام Sail، يمكنك استخدام معامل الاستعلام (query string parameter) `with` لاختيار الخدمات التي ستهيئ في ملف `docker-compose.yml` الخاص بمشروعك. الخدمات المتوفرة تتضمن `mysql`، `pgsql`، `mariadb`، `redis`، `memcached`، `meilisearch`، `minio`، `selenium`، و`mailhog`:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

إن لم تحدد الخدمات التي تريد تهيئتها، سيٌهيئ مكدس افتراضي مكون من `mysql`، `redis`، `meilisearch`، `mailhog`، و`selenium`

يمكنك أن تأمر Sail بتنصيب [(Devcontainer) حاوية تطوير افتراضية](/docs/{{version}}/sail#using-devcontainers) بإضافة معامل `devcontainer` إلى الرابط:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="installation-via-composer"></a>
### التنصيب باستخدام مدير الحزم (composer)

إن كان مدير الحزم (composer) و PHP منصَبين على جهازك، يمكنك إنشاء مشروع لارافل جديد باستخدام Composer مباشرة. بعد إنشاء التطبيق، يمكنك بدء مخدم تطوير محل باستخدام أمر `serve` الخاص واجهة الأوامر Artisan:

```shell
composer create-project laravel/laravel example-app

cd example-app

php artisan serve
```

<a name="the-laravel-installer"></a>
#### The Laravel Installer

Or, you may install the Laravel Installer as a global Composer dependency:

```shell
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

Make sure to place Composer's system-wide vendor bin directory in your `$PATH` so the `laravel` executable can be located by your system. This directory exists in different locations based on your operating system; however, some common locations include:

<div class="content-list" markdown="1">

- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux Distributions: `$HOME/.config/composer/vendor/bin` or `$HOME/.composer/vendor/bin`

</div>

For convenience, the Laravel installer can also create a Git repository for your new project. To indicate that you want a Git repository to be created, pass the `--git` flag when creating a new project:

```shell
laravel new example-app --git
```

This command will initialize a new Git repository for your project and automatically commit the base Laravel skeleton. The `git` flag assumes you have properly installed and configured Git. You can also use the `--branch` flag to set the initial branch name:

```shell
laravel new example-app --git --branch="main"
```

Instead of using the `--git` flag, you may also use the `--github` flag to create a Git repository and also create a corresponding private repository on GitHub:

```shell
laravel new example-app --github
```

The created repository will then be available at `https://github.com/<your-account>/example-app`. The `github` flag assumes you have properly installed the [GitHub CLI](https://cli.github.com) and are authenticated with GitHub. Additionally, you should have `git` installed and properly configured. If needed, you can pass additional flags that are supported by the GitHub CLI:

```shell
laravel new example-app --github="--public"
```

You may use the `--organization` flag to create the repository under a specific GitHub organization:

```shell
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
## Initial Configuration

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

<a name="environment-based-configuration"></a>
### Environment Based Configuration

Since many of Laravel's configuration option values may vary depending on whether your application is running on your local computer or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application.

Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed.

> {tip} For more information about the `.env` file and environment based configuration, check out the full [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="directory-configuration"></a>
### Directory Configuration

Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files that exist within your application.

<a name="next-steps"></a>
## Next Steps

Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation:

<div class="content-list" markdown="1">

- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [Directory Structure](/docs/{{version}}/structure)
- [Service Container](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below.

<a name="laravel-the-fullstack-framework"></a>
### Laravel The Full Stack Framework

Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/{{version}}/blade) or using a single-page application hybrid technology like [Inertia.js](https://inertiajs.com). This is the most common way to use the Laravel framework.

If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/{{version}}/routing), [views](/docs/{{version}}/views), or the [Eloquent ORM](/docs/{{version}}/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia.js](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications.

If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Laravel Mix](/docs/{{version}}/mix).

> {tip} If you want to get a head start building your application, check out one of our official [application starter kits](/docs/{{version}}/starter-kits).

<a name="laravel-the-api-backend"></a>
### Laravel The API Backend

Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/{{version}}/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more.

If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), and the [Eloquent ORM](/docs/{{version}}/eloquent).

> {tip} Need a head start scaffolding your Laravel backend and Next.js frontend? Laravel Breeze offers an [API stack](/docs/{{version}}/starter-kits#breeze-and-next) as well as a [Next.js frontend implementation](https://github.com/laravel/breeze-next) so you can get started in minutes.

