# Directory Structure

- [မိတ်ဆက်](#introduction)
- [The Root Directory](#the-root-directory)
    - [The `app` Directory](#the-root-app-directory)
    - [The `bootstrap` Directory](#the-bootstrap-directory)
    - [The `config` Directory](#the-config-directory)
    - [The `database` Directory](#the-database-directory)
    - [The `public` Directory](#the-public-directory)
    - [The `resources` Directory](#the-resources-directory)
    - [The `routes` Directory](#the-routes-directory)
    - [The `storage` Directory](#the-storage-directory)
    - [The `tests` Directory](#the-tests-directory)
    - [The `vendor` Directory](#the-vendor-directory)
- [The App Directory](#the-app-directory)
    - [The `Broadcasting` Directory](#the-broadcasting-directory)
    - [The `Console` Directory](#the-console-directory)
    - [The `Events` Directory](#the-events-directory)
    - [The `Exceptions` Directory](#the-exceptions-directory)
    - [The `Http` Directory](#the-http-directory)
    - [The `Jobs` Directory](#the-jobs-directory)
    - [The `Listeners` Directory](#the-listeners-directory)
    - [The `Mail` Directory](#the-mail-directory)
    - [The `Notifications` Directory](#the-notifications-directory)
    - [The `Policies` Directory](#the-policies-directory)
    - [The `Providers` Directory](#the-providers-directory)
    - [The `Rules` Directory](#the-rules-directory)

<a name="introduction"></a>
## မိတ်ဆတ်

Laravel ရဲ့ application structure က application အကြီးဘဲဖြစ်ဖြစ် အသေးဘဲဖြစ်ဖြစ်လွယ်လွယ်ကူကူစနိုင်ဖို့ရည်ရွယ်ထားတာပါ။ သင့် application ကိုသင့်စိတ်ကြိုက် organize လုပ်ချင်သလိုလုပ်လို့ရပါတယ်။ Composer ကနေ Class တွေကို autoload နိုင်သမျှတော့ Laravel မှာ ဘယ် class တွေကဘယ်မှာဘဲရှိရမယ်ဆိုတာမျို့းသတ်မှတ်မထားပါဘူး။ 

#### Models Directory ကဘယ်မှာလဲ

Laravel ကိုအခုမှစတင်မယ့်သူတွေအတွက် Laravel မှာ `model` directory မရှိတာ နည်းနည်းရှုပ်ထွေးစေနိုင်ပါတယ်။ သို့သော်လည်း အဲ့လို directory မရှိတာကတမင်သက်သက်လုပ်ထားတာပါ။ "models" ဆိုတဲ့စကားလုံရဲ့ အဓိပါယ်အများကြီးရှိတဲ့အတွက် လူတောတော်များများကို စဝေစဝါဖြစ်စေပါတယ်။ တစ်ချို့ developers တွေက application ရဲ့ "models" ကို business logic အကုန်အဲ့မှာရှိရမယ်ဆိုပြီးရည်ညွှန်းကြပြီးတော့ တစ်ချို့ကကျတော့ relational database တွေရဲ့ အပြန်အလှန်ပြု interact လုပ်ပေးတြ့ class တွေလို့ရည်ညွှန်းကြပါတယ်။

အဲ့ဒီအတွက်ကြောင့် Developer တွေကိုကိုယ်ကြိုက်တဲ့နေရာမှာထားထားနိုင်အောင်လို့ Eloquent models တွေကို `app` directory ထဲမှာ default အနေဖြင့်ထားထားတာပါ။

<a name="the-root-directory"></a>
## The Root Directory

<a name="the-root-app-directory"></a>
#### The App Directory

`app` directory ကတော့သင်မျှော်မှန်းထားတဲ့အတိုင်းဘဲ application ရဲ့ core code တွေပါဝင်ပါတယ်။ ကျွန်တော်တို့အဲ့ဒီ့ directory ကိုခဏနေကြလျှင် explore လုပ်မှာပါ သို့သော်လည်း သင့် application ရဲ့ classes တွေအကုန်လုံးကအဲ့ဒီ့ directory ထဲမှာရှိမှာဖြစ်ပါတယ်။

<a name="the-bootstrap-directory"></a>
#### The Bootstrap Directory

`bootstrap` directory ထဲမှာ `app.php` file ရှိနေမှာပါ။ အဲ့ဒီ့ `app.php` file က framework ကို bootstrap လုပ်ပေးထားတာပါ။ bootatrap direcotry ထဲမှာ `cache` directory တစ်ခုလည်းပါဝင်မှာဖြစ်ပြီးတော့ အဲ့ဒီ့ folder ထဲမှာ framework ကနေ performance optimization အတွက် generate လုပ်ပေးထားတဲ့ route နှင့် services cache files တွေရှိမှာဖြစ်ပါတယ်။

<a name="the-config-directory"></a>
#### The Config Directory

`config` directory ကတော့သူ့အဓိပါယ်အတိုင်း သင့် application ရဲ့ configuration files တွေရှိမှာဖြစ်ပါတယ်။ အဲ့ထဲက files တွေကိုဖတ်ကြည့်ပြီးတော့ configuration ကရရှိချင်တဲ့ရွေးချယ်စရာ configuration options တွေနှင့်ရင်းနှီးကျွမ်းဝင်အောင်လုပ်သင့်ပါတယ်။

<a name="the-database-directory"></a>
#### The Database Directory

`database` directory ကတော့သင့် application ရဲ့ database migraation ၊ model factories နှင့် seeds တွေပါဝင်မှာဖြစ်ပါတယ်။ တကယ်လို့သင်က SQLite database သုံးရင်ဒီ folder ထဲမှာ SQLite database ထားနိုင်ပါတယ်။

<a name="the-public-directory"></a>
#### The Public Directory

`public` directory ထဲမှာတော့ application စီလာသမျှ request တွေကိုလက်ခံပြီး autoload configure လုပ်ထားတဲ့ `index.php` file ရှိမှာဖြစ်ပါတယ်။ ဒီ `public` folder ထဲမှာတော့ သင့် application အတွက်လိုအပ်တဲ့ ဓာတ်ပုံထားတဲ့ folder၊ Javascriot နှင့် CSS ထားရှိတဲ့ folder တွေပါဝင်မှာဖြစ်ပါတယ်။

<a name="the-resources-directory"></a>
#### The Resources Directory

`resoruces` directory ထဲမှာတော့ views files တွေနှင့် compile မလုပ်ရသေးတဲ့ LESS၊ SASS နှင့် JavaScript တွေရှိမှာဖြစ်ပါတယ်။ ဒီ directory ထဲမှာသင့်ရဲ့ languages files တွေအတွက် folder လည်းတည်ရှိမှာဖြစ်ပါတယ်။ 

<a name="the-routes-directory"></a>
#### The Routes Directory

`routes` directory ထဲမှာတော့သင့် application အတွက် route definitions တွေရှိမှာဖြစ်ပါတယ်။ Default အနေဖြင့် `web.php`၊ `api.php`၊ `console.php` နှင့် `channels.php` routes တွေရှိမှာဖြစ်ပါတယ်။

`web.php` file မှာတော့ `RouteServiceProvider` မှာထားရှိတဲ့ `web` midddleware group ထဲမှာရှိတဲ့ routes တွေပါဝင်မှာဖြစ်ပါတယ်၊ အဲ့ routes တွေက session state၊ CSRF protection နှင့် cookie encryption တွေထောက်ပံ့ပေးထားပါတယ်။ သင့် application က stateless၊ RESTful API တွေမပါဝင်ဘူးဆိုလျှင်တော့ သင့် route files တွေတော်တော်များများကို `web.php` file မှာသတ်မှတ်ရပါလိမ့်မယ်။

`api.php` file မှာတော့ `RouteServiceProvider` မှာထားရှိတဲ့ `api` middleware group ထဲမှာရှိတဲ့ routes တွေပါဝင်မှာဖြစ်ပါတယ်။ အဲ့ `api` middleware က rate limiting လုပ်လို့ရပါတယ်။ နောက်ဒီထဲမှာရှိတဲ့ rotues တွေက stateless အတွက်ရည်ရွယ်တာဖြစ်တဲ့အတွက် ဒီ routes တွေဆီလာတဲ့ application တွေက token authentication ကိုအသုံးပြုဖို့ရည်ရွယ်တာဖြစ်လို့ session state အသုံးပြုခွင့်ရှိမှာမဟုတ်ပါဘူး။

`console.php` file ကတော့သင့်ရဲ့ Clousre base console commands တွေကိုသတ်မှတ်ဖို့နေရာဘဲဖြစ်ပါတယ်။ Closure တစ်ခုချင်းစီက command instance တစ်ခုချင်းစီရဲ့ IO methods တွေနှင့်လွယ်ကူစွာ interacte လုပ်ဖို့ရာအတွက် bound လုပ်ထားတာပါ။ သို့သော်လည်း ဒီ file မှာ HTTP routes တွေ define မလုပ်ပါဘူး၊ သင့် application ရဲ့ console base entry points (routes) တွေကိုဘဲသတ်မှတ်တာပါ။

`channels.php` file ကတော့သင့် application အထောက်အပံ့ပေးတဲ့ event broadcasting channels တွေကို register လုပ်ဖို့ရာအတွက်ဖြစ်ပါတယ်။

<a name="the-storage-directory"></a>
#### The Storage Directory

`storage` directory မှာတော့ compiled လုပ်ထားတဲ့ Blade tempates တွေ၊ file အခြေခံ sessions တွေ၊ cache fiels တွေနှင့် တစ်ခြား framework ကလို generate လုပ်လိုက်တဲ့ file တွေပါဝင်မှာဖြစ်ပါတယ်။ ဒီ directory ထဲမှာ `app`၊ `framework` နှင့် `logs` ဆိုတဲ့ directory တွေပါဝင်မှာဖြစ်ပါတယ်။ `app` directory ထဲမှာ သင့် application မှ generate လုပ်လိုက်တဲ့ file အားလုံးကို သိမ်းဆည်းဖို့ရာအတွက်အသုံးပြုပါလိမ့်မယ်။ `framework` directory က framework က generate လုပ်လိုက်တဲ့ fiels တွေနှင့် caches တွေကို store ထားမှာဖြစ်ပါတယ်။ နောက်ဆုံး `logs` directory ကတော့ application ရဲ့ log fiels တွေပါဝင်မှာဖြစ်ပါတယ်။

The `storage/app/public` directory may be used to store user-generated files, such as profile avatars, that should be publicly accessible. You should create a symbolic link at `public/storage` which points to this directory. You may create the link using the `php artisan storage:link` command.

<a name="the-tests-directory"></a>
#### The Tests Directory

The `tests` directory contains your automated tests. An example [PHPUnit](https://phpunit.de/) is provided out of the box. Each test class should be suffixed with the word `Test`. You may run your tests using the `phpunit` or `php vendor/bin/phpunit` commands.

<a name="the-vendor-directory"></a>
#### The Vendor Directory

The `vendor` directory contains your [Composer](https://getcomposer.org) dependencies.

<a name="the-app-directory"></a>
## The App Directory

The majority of your application is housed in the `app` directory. By default, this directory is namespaced under `App` and is autoloaded by Composer using the [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/).

The `app` directory contains a variety of additional directories such as `Console`, `Http`, and `Providers`. Think of the `Console` and `Http` directories as providing an API into the core of your application. The HTTP protocol and CLI are both mechanisms to interact with your application, but do not actually contain application logic. In other words, they are two ways of issuing commands to your application. The `Console` directory contains all of your Artisan commands, while the `Http` directory contains your controllers, middleware, and requests.

A variety of other directories will be generated inside the `app` directory as you use the `make` Artisan commands to generate classes. So, for example, the `app/Jobs` directory will not exist until you execute the `make:job` Artisan command to generate a job class.

> {tip} Many of the classes in the `app` directory can be generated by Artisan via commands. To review the available commands, run the `php artisan list make` command in your terminal.

<a name="the-broadcasting-directory"></a>
#### The Broadcasting Directory

The `Broadcasting` directory contains all of the broadcast channel classes for your application. These classes are generated using the `make:channel` command. This directory does not exist by default, but will be created for you when you create your first channel. To learn more about channels, check out the documentation on [event broadcasting](/docs/{{version}}/broadcasting).

<a name="the-console-directory"></a>
#### The Console Directory

The `Console` directory contains all of the custom Artisan commands for your application. These commands may be generated using the `make:command` command. This directory also houses your console kernel, which is where your custom Artisan commands are registered and your [scheduled tasks](/docs/{{version}}/scheduling) are defined.

<a name="the-events-directory"></a>
#### The Events Directory

This directory does not exist by default, but will be created for you by the `event:generate` and `make:event` Artisan commands. The `Events` directory, as you might expect, houses [event classes](/docs/{{version}}/events). Events may be used to alert other parts of your application that a given action has occurred, providing a great deal of flexibility and decoupling.

<a name="the-exceptions-directory"></a>
#### The Exceptions Directory

The `Exceptions` directory contains your application's exception handler and is also a good place to place any exceptions thrown by your application. If you would like to customize how your exceptions are logged or rendered, you should modify the `Handler` class in this directory.

<a name="the-http-directory"></a>
#### The Http Directory

The `Http` directory contains your controllers, middleware, and form requests. Almost all of the logic to handle requests entering your application will be placed in this directory.

<a name="the-jobs-directory"></a>
#### The Jobs Directory

This directory does not exist by default, but will be created for you if you execute the `make:job` Artisan command. The `Jobs` directory houses the [queueable jobs](/docs/{{version}}/queues) for your application. Jobs may be queued by your application or run synchronously within the current request lifecycle. Jobs that run synchronously during the current request are sometimes referred to as "commands" since they are an implementation of the [command pattern](https://en.wikipedia.org/wiki/Command_pattern).

<a name="the-listeners-directory"></a>
#### The Listeners Directory

This directory does not exist by default, but will be created for you if you execute the `event:generate` or `make:listener` Artisan commands. The `Listeners` directory contains the classes that handle your [events](/docs/{{version}}/events). Event listeners receive an event instance and perform logic in response to the event being fired. For example, a `UserRegistered` event might be handled by a `SendWelcomeEmail` listener.

<a name="the-mail-directory"></a>
#### The Mail Directory

This directory does not exist by default, but will be created for you if you execute the `make:mail` Artisan command. The `Mail` directory contains all of your classes that represent emails sent by your application. Mail objects allow you to encapsulate all of the logic of building an email in a single, simple class that may be sent using the `Mail::send` method.

<a name="the-notifications-directory"></a>
#### The Notifications Directory

This directory does not exist by default, but will be created for you if you execute the `make:notification` Artisan command. The `Notifications` directory contains all of the "transactional" notifications that are sent by your application, such as simple notifications about events that happen within your application. Laravel's notification features abstracts sending notifications over a variety of drivers such as email, Slack, SMS, or stored in a database.

<a name="the-policies-directory"></a>
#### The Policies Directory

This directory does not exist by default, but will be created for you if you execute the `make:policy` Artisan command. The `Policies` directory contains the authorization policy classes for your application. Policies are used to determine if a user can perform a given action against a resource. For more information, check out the [authorization documentation](/docs/{{version}}/authorization).

<a name="the-providers-directory"></a>
#### The Providers Directory

The `Providers` directory contains all of the [service providers](/docs/{{version}}/providers) for your application. Service providers bootstrap your application by binding services in the service container, registering events, or performing any other tasks to prepare your application for incoming requests.

In a fresh Laravel application, this directory will already contain several providers. You are free to add your own providers to this directory as needed.

<a name="the-rules-directory"></a>
#### The Rules Directory

This directory does not exist by default, but will be created for you if you execute the `make:rule` Artisan command. The `Rules` directory contains the custom validation rule objects for your application. Rules are used to encapsulate complicated validation logic in a simple object. For more information, check out the [validation documentation](/docs/{{version}}/validation).
