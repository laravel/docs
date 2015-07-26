# 发布说明

- [关于版本支持的约定](#support-policy)
- [Laravel 5.1.4](#laravel-5.1.4)
- [Laravel 5.1](#laravel-5.1)
- [Laravel 5.0](#laravel-5.0)
- [Laravel 4.2](#laravel-4.2)
- [Laravel 4.1](#laravel-4.1)

<a name="support-policy"></a>
## 关于版本支持的约定

支持 LTS 发布的版本, 如 Laravel 5.1, 自发布起两年的时间支持 Bug 修复, 3 年时间支持安全修复, LTS 版本是此项目能提供的最长时间维护版本. 

一般版本的发布, 只提供 6 个月的 Bug 修复支持, 一年的安全修复支持. 

<a name="laravel-5.1.4"></a>
## Laravel 5.1.4

Laravel 5.1.4 增加了登陆节流功能, 详见: [登录认证文档](/docs/{{version}}/authentication#authentication-throttling)

<a name="laravel-5.1"></a>
## Laravel 5.1

Laravel 5.1 在 5.0 的基础上, 提高了更好的对 PSR-2 的支持, 在功能上新添加了 事件广播, 中间件参数支持, 还有 Artisan 命令行优化等. 

### PHP 5.5.9+

因为 PHP 开发团队已经宣布在 12 月份起, 不再支持 PHP 5.4 的安全更新, 所以, Laravel 5.1 对 PHP 的依赖版本是 5.5.9 或者更高, 5.5.9 也是 Guzzle 和 AWS SDK 最低要求版本. 

### LTS

Laravel 5.1 是 Laravel 社区发布的第一个 LTS 支持项目. 

支持 LTS 发布的版本, 自发布起两年的时间支持 Bug 修复, 3 年时间支持安全修复, LTS 版本的支持周期, 很适合大企业用户. 

### PSR-2

Laravel 框架默认支持 [PSR-2 代码标准指南](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md), 所有的代码产生器也同时支持 PSR-2.

### 文档优化

每一页的 Laravel 框架文档, 都被仔细的审查, 所有的代码示例都被仔细审阅, 并加入注释, 以便更好的说明上下文语境. 

### 事件广播

在现代的 Web 应用程序中, Web Sockets 被用来实现实时更新, 单有数据发生变化的时候, 会把消息广播到所有的连接客户端. 

为了支持此种类型的应用, Laravel 提供了一套更好的机制, 让对事件进行广播, 允许你在服务器和客户端 JS 框架同时使用同一个时间名称. 

详情请见 [事件广播](/docs/{{version}}/events#broadcasting-events).

### 中间件参数支持

中间件现在能支持传参多余的参数, 打个比方, 你需要判断当前登录用户是否是某个角色 (Role) 后, 才能执行某个重要动作, 你可以创建 `RoleMiddleware`, 然后接受一个外加的参数 (只支持 string 类型的传参): 

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class RoleMiddleware
    {
        /**
         * Run the request filter.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @param  string  $role
         * @return mixed
         */
        public function handle($request, Closure $next, $role)
        {
            if (! $request->user()->hasRole($role)) {
                // Redirect...
            }

            return $next($request);
        }

    }

中间件参数的调用, 参数和中间件之间以符号 `:` 分隔开, 多个参数之间使用 `,` 区分:

    Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
        //
    }]);

中间件的介绍详见 [中间件文档](/docs/{{version}}/middleware).

### 测试功能优化

Laravel 自带的测试功能得到了很大的优化, 最新提供了好几个方法, 提供了表达更清晰的接口, 来让你检查返回的内容, 如以下: 

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

详见 [测试文档](/docs/{{version}}/testing).

### 模型工厂

新加入了模型工厂帮助方法, [模型工厂](/docs/{{version}}/testing#model-factories) 可以让你快速创建模型对象, 并且利用了伟大的库 [Faker](https://github.com/fzaninotto/Faker) 来制造假数据: 

    $factory->define('App\User', function ($faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => str_random(10),
            'remember_token' => str_random(10),
        ];
    });

详见 [模型工厂文档](/docs/{{version}}/testing#model-factories).

### Artisan 命令行优化

Artisan 现支持类似于路由一样的 `签名式` 定义方式, 此方式让你使用非常直观的方法来定义命令行参数, 下面是个例子: 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--force}';

详见 [Arsison 命令行稳定](/docs/{{version}}/artisan).

### 文件结构

为了易读性, 把 `app/Commands` 重命名为  `app/Jobs`, 把 `app/Handlers` 改名为 `app/Listeners`. 

这两个修改为非破坏性修改, 不要求强制升级到最新版本. 

### 加密

在之前的 Laravel 版本里面, 我们使用 `mcrypt` PHP 扩展来支持加密, 在 5.1 版本, 所有的加密都由 `openssl` PHP 扩展来处理. 

<a name="laravel-5.0"></a>
## Laravel 5.0

Laravel 5.0 在默认的项目上引进了新的应用程序架构。新的架构提供了更好的功能来构建健壮的 Laravel 应用程序，以及在应用程序中全面采用新的自动加载标准（ PSR-4 ）。首先，来查看一些主要变更：

### 新的目录结构

旧的 `app/models` 目录已经完全被移除。相对的，你所有的代码都放在 `app` 目录下，以及默认使用 `App` 命名空间。这个默认的命名空间可以使用新的 `app:name` Artisan 命令来快速更改。

控制器（ controller ），中间件（ middleware ），以及请求（ requests，Laravel 5.0 中新型态的类别），现在都存放在 `app/Http` 的对应目录下，因为他们都与应用程序的 HTTP 传输层相关。除了一个路由设置的文件外，所有的中间件现在都拆分开成单独的类文件。

新的 `app/Providers` 目录取代了旧版 Laravel 4.x `app/start` 里的文件。这些服务提供者有很多启动应用程序相关的方法，像是错误处理，日志记录，路由加载，以及更多。当然，你可以自由的建立新的服务提供者到应用程序。

应用程序的语言文件和视图都移到 `resources` 目录下。

### Contracts

所有 Laravel 主要组件实现所用的接口都放在 `illuminate/contracts` 项目下。这个项目没有其他的外部依赖。这些方便、集成的接口，可以让你用来让依赖注入变得低耦合，将可以简单作为 Laravel Facades 的替代选项。

更多关于 contracts 的信息，参考[完整文档](/docs/{{version}}/contracts)。

### 路由缓存

如果你的应用程序全部都是使用控制器路由，你可以使用新的 `route:cache` Artisan 命令大幅度地加快路由注册。这对于有 100 个以上路由规则的应用程序很有用，可以**大幅度地**加快应用程序这部分的处理速度。

### 路由中间件（ Middleware ）

除了像 Laravel 4 风格的路由「过滤器（ filters ）」，Laravel 5 现在也支持 HTTP 中间件，而原本的认证和 CSRF 「过滤器」已经改写成中间件。中间件提供了单一、一致的接口取代了各种过滤器，让你在请求进到应用程序前，可以方便地检查甚至拒绝请求。

更多关于中间件的信息，参考[完整文档](/docs/{{version}}/middleware)。

### 控制器方法依赖注入

除了之前有的控制器依赖注入，你现在可以在控制器方法使用类型提示（ type-hint ）进行依赖注入。[服务容器](/docs/{{version}}/container)会自动注入依赖，即使路由包含了其他参数也不成问题：

    public function createPost(Request $request, PostRepository $posts)
    {
        //
    }

### 认证基本架构

用户注册，认证，以及重设密码的控制器现在已经默认含括了，包含相对应的视图，放在 `resources/views/auth`。除此之外， 「users」 数据表迁移也已经默认存在框架中了。这些简单的资源，可以让你快速开发应用程序的业务逻辑，而不用陷在撰写认证模板的泥潭上。认证相关的视图可以经由 `auth/login` 以及 `auth/register` 路由访问。`App\Services\Auth\Registrar` 服务会负责处理用户认证和添加的相关逻辑。

### 事件对象

你现在可以将事件定义成对象，而不是仅使用字串。例如，查看以下的事件：

    class PodcastWasPurchased {

        public $podcast;

        public function __construct(Podcast $podcast)
        {
            $this->podcast = $podcast;
        }

    }

这个事件可以像一般使用那样被派发：

    Event::fire(new PodcastWasPurchased($podcast));

当然，你的事件处理会收到事件的对象而不是数据的列表：

    class ReportPodcastPurchase {

        public function handle(PodcastWasPurchased $event)
        {
            //
        }

    }

更多关于使用事件的信息，参考[完整文档](/docs/{{version}}/events)。

### 命令（ Commands ）、队列（ Queueing ）

除了 Laravel 4 形式的队列任务，Laravel 5 以简单的命令对象作为队列任务。这些命令放在 `app/Commands` 目录下。下面是个简单的命令：

    class PurchasePodcast extends Command implements SelfHandling, ShouldBeQueued {

        use SerializesModels;

        protected $user, $podcast;

        /**
         * Create a new command instance.
         *
         * @return void
         */
        public function __construct(User $user, Podcast $podcast)
        {
            $this->user = $user;
            $this->podcast = $podcast;
        }

        /**
         * Execute the command.
         *
         * @return void
         */
        public function handle()
        {
            // Handle the logic to purchase the podcast...

            event(new PodcastWasPurchased($this->user, $this->podcast));
        }

    }

Laravel 的基底控制器使用了新的 `DispatchesCommands` trait，让你可以简单的派发命令执行。

    $this->dispatch(new PurchasePodcastCommand($user, $podcast));

当然，你也可以将命令视为同步执行（而不会被放到队列里）的任务。事实上，使用命令是个好方式，让你可以封装应用程序需要执行的复杂任务。更多相关的信息，参考 [command bus](/docs/{{version}}/bus) 文档。

### 数据库队列

`database` 队列驱动现在已经包含在 Laravel 中了，提供了简单的本地端队列驱动，让你除了数据库相关软件外不需安装其他套件。

### Laravel 调用（ Scheduler ）

过去，开发者可以产生 Cron 设置，用以调用所有他们想要执行的命令行指令。然而，这是件很头痛的事情，你的命令行调用不再属于版本控制的一部分，而你必须 SSH 到服务器里加入 Cron 设置。

为了让生活变得简单点, 让你可以流畅而且具有表达性的在 Laravel 里面定义你的命令调用，而且服务器只需要单一个 Cron 设置。

它会看起来如下：

    $schedule->command('artisan:command')->dailyAt('15:00');

当然，快参考[完整文档](/docs/{{version}}/artisan#scheduling-artisan-commands)学习所有调用相关知识。

### Tinker、Psysh

`php artisan tinker` 命令现在使用 Justin Hileman 的 [Psysh](https://github.com/bobthecow/psysh)，一个 PHP 更强大的 REPL。如果你喜欢 Laravel 4 的 Boris，你也会喜欢上 Psysh。更好的是，它可以跑在 Windows！要开始使用，只要输入：

    php artisan tinker

### DotEnv

比起一堆令人困惑的、嵌套的环境配置文件目录，Laravel 5 现在使用了 Vance Lucas 的 [DotEnv](https://github.com/vlucas/phpdotenv)。这个套件提供了超级简单的方式管理配置文件，并且让 Laravel 5 环境检测变得轻松。更多的细节，参考完整的[配置文件文档](/docs/{{version}}/configuration#environment-configuration)。

### Laravel Elixir

Jeffrey Way 的 Laravel Elixir 提供了一个流畅、语义化的接口，可以编译以及合并 assets。如果你曾经在学习 Grunt 或 Gulp 被吓到，不必再害怕了。Elixir 让使用 Gulp 编译 Less、Sass 及 CoffeeScript 变得简单。它甚至可以帮你执行测试！

更多关于 Elixir 的信息，参考[完整文档](/docs/{{version}}/elixir)。

### Laravel Socialite

Laravel Socialite 是个可选的，Laravel 5.0 以上兼容的套件，提供了无痛的 OAuth 认证。目前 Socialite 支持 Facebook、Twitter、Google 以及 GitHub。它写起来可能像这样：

    public function redirectForAuth()
    {
        return Socialize::with('twitter')->redirect();
    }

    public function getUserFromProvider()
    {
        $user = Socialize::with('twitter')->user();
    }

不用再花上数小时撰写 OAuth 的认证流程。数分钟就可开始！查看[完整文档](/docs/{{version}}/authentication#social-authentication) 里有所有的细节。

### Flysystem 集成

Laravel 现在包含了强大的 [Flysystem](https://github.com/thephpleague/flysystem)（一个文件系统的抽象类库），提供了无痛的集成，把本地端文件系统、Amazon S3 和 Rackspace 云存储集成在一起，
有统一且优雅的 API！现在要将文件存到 Amazon S3 相当简单：

    Storage::put('file.txt', 'contents');

更多关于 Laravel 文件系统集成，参考[完整文档](/docs/{{version}}/filesystem)。

### Form Requests

Laravel 5.0 使用了 **form requests**，是继承了 `Illuminate\Foundation\Http\FormRequest` 的类。这些 request 对象可以和控制器方法依赖注入结合，提供一个不需样板的方法，可以验证用户输入。让我们深入点，看一个 `FormRequest` 的示例：

    <?php namespace App\Http\Requests;

    class RegisterRequest extends FormRequest {

        public function rules()
        {
            return [
                'email' => 'required|email|unique:users',
                'password' => 'required|confirmed|min:8',
            ];
        }

        public function authorize()
        {
            return true;
        }

    }

定义好类后，我们可以在控制器动作里使用类型提示：

    public function register(RegisterRequest $request)
    {
        var_dump($request->input());
    }

当 Laravel 的服务容器辨别出要注入的类别是个 `FormRequest` 实例，请求会被**自动验证**。意味着，当你的控制器动作被调用了，你可以安全的假设 HTTP 的请求输入己经被验证过，根据你在 form request 类别里自定的规则。甚至，若这个请求验证不通过，一个 HTTP 重定向（可以自定），会自动发出，错误消息可以被闪存到 session 或是转换成 JSON 返回。**表单验证就是如此的简单。**更多关于 `FormRequest` 验证，参考[文档](/docs/{{version}}/validation#form-request-validation)。

### 简易控制器请求验证

Laravel 5 基类控制器包含一个 `ValidatesRequests` trait。这个 trait 包含了一个简单的 `validate` 方法可以验证请求。如果对应用程序来说 `FormRequests` 太复杂了，参考这个：

    public function createPost(Request $request)
    {
        $this->validate($request, [
            'title' => 'required|max:255',
            'body' => 'required',
        ]);
    }

如果验证失败，会抛出异常并且返回对应的 HTTP 回应到浏览器。验证错误信息会被闪存到 session！而如果请求是 AJAX 请求，Laravel 会自动返回 JSON 格式的验证错误信息。

更多关于这个新方法的信息，参考[这个文档](/docs/{{version}}/validation#controller-validation)。

### 新的 Generators

因采用了新的应用程序默认架构，框架也添加了 Artisan generator 命令。使用 `php artisan list` 查看更多细节。

### 配置文件缓存

你现在可以在单一文件里缓存所有配置文件了，使用 `config:cache` 命令。

### Symfony VarDumper

常用的 `dd` 辅助函数，其可以在除错时印出变量信息，已经升级成使用令人惊艳的 Symfony VarDumper。它提供了颜色标记的输出，甚至数组可以自动缩合。在项目中试试下列代码：

    dd([1, 2, 3]);

<a name="laravel-4.2"></a>
## Laravel 4.2

此发行版本的完整变更列表可以从一个 4.2 的完整安装下，执行 `php artisan changes` 命令，或者 [Github 上的变更纪录](https://github.com/laravel/framework/blob/4.2/src/Illuminate/Foundation/changes.json)。此纪录仅含括主要的强化更新和此发行的变更部分。

> **附注:** 在 4.2 发布周期间，许多小的 bug 修正与功能强化被整并至各个 4.1 的子发行版本中。所以最好确认 Laravel 4.1 版本的更新列表。

### PHP 5.4 需求

Laravel 4.2 需要 PHP 5.4 以上的版本。此 PHP 更新版本让我们可以使用 PHP 的新功能：traits 来为像是 [Laravel 收银台](/docs/billing) 来提供更具表达力的接口。PHP 5.4 也比 PHP 5.3 带来显著的速度及性能提升。

### Laravel Forge

Larvel Forge，一个网页应用程序，提供一个简单的接口去建立管理你云端上的 PHP 服务器，像是 Linode、DigitalOcean、Rackspace 和 Amazon EC2。支持自动化 nginx 设置、SSH 密钥管理、Cron job 自动化、透过 NewRelic & Papertrail 服务器监控、「推送部署」、Laravel queue worker 设置等等。Forge 提供最简单且更实惠的方式来部署所有你的 Laravel 应用程序。

默认 Laravel 4.2 的安装里，`app/config/database.php` 配置文件默认已为 Forge 设置完成，让在平台上的全新应用程序更方便部署。

关于 Laravel Forge 的更多信息可以在[官方 Forge 网站](https://forge.laravel.com)上找到。

### Laravel Homestead

Laravel Homestead 是一个为部署健全的 Laravel 和 PHP 应用程序的官方 Vagrant 环境。绝大多数的封装包的相依与软件在发布前已经部署处理完成，让封装包可以极快的被启用。Homestead 包含 Nginx 1.6、PHP 5.5.12、MySQL、Postres、Redis、Memcached、Beanstalk、Node、Gulp、Grunt 和 Bower。Homestead 包含一个简单的 `Homestead.yaml` 配置文件，让你在单一个封装包中管理多个 Laravel 应用程序。

默认的 Laravel 4.2 安装中包含的 `app/config/local/database.php` 配置文件使用 Homestead 的数据库作为默认。让 Laravel 初始化安装与设置更为方便。

官方文档已经更新并包含在 [Homestead 文档](/docs/homestead) 中。

### Laravel 收银台

Laravel 收银台是一个简单、具表达性的资源库，用来管理 Stripe 的订阅帐务。虽然在安装中此组件依然是选用，我们依然将收银台文档包含在主要 Laravel 文档中。此收银台发布版本带来了数个错误修正、多货币支持还有支持最新的 Stripe API。

### Queue Workers 常驻程序

Artisan `queue:work` 命令现在支持 `--daemon` 参数让 worker 可以以「常驻程序」启用。代表 worker 可以持续的处理队列工作不需要重启框架。这让一个复杂的应用程序部署过程中，使得 CPU 的使用有显著的降低。

更多关于 Queue Workers 常驻程序信息请详阅 [queue 文档](/docs/queues#daemon-queue-worker)。

### Mail API Drivers

Laravel 4.2 为 `Mail` 函式采用了新的 Mailgun 和 Mandrill API 驱动。对许多应用程序而言，他提供了比 SMTP 更快也更可靠的方法来递送邮件。新的驱动使用了 Guzzle 4 HTTP 资源库。

### 软删除 Traits

对于软删除和全作用域更简洁的方案
PHP 5.4 的 `traits` 提供了一个更加简洁的软删除架构和全局作用域，这些新架构为框架提供了更有扩展性的功能，并且让框架更加简洁。

更多关于软删除的文档请见: [Eloquent documentation](/docs/eloquent#soft-deleting).

### 更为方便的 认证(auth) & Remindable Traits

得益于 PHP 5.4 traits，我们有了一个更简洁的用户认证和密码提醒接口，这也让 `User` 模型文档更加精简。

### "简易分页"

一个新的 `simplePaginate` 方法已被加入到查找以及 Eloquent 查找器中。让你在分页视图中，使用简单的「上一页」和「下一页」链接查找更为高效。

### 迁移确认

在正式环境中，破坏性的迁移动作将会被再次确认。如果希望取消提示字符确认请使用 `--force` 参数。

<a name="laravel-4.1"></a>
## Laravel 4.1

### 完整变更列表

此发行版本的完整变更列表，可以在版本 4.1 的安装中命令行执行 `php artisan changes` 取得，或者浏览 [Github 变更档](https://github.com/laravel/framework/blob/4.1/src/Illuminate/Foundation/changes.json) 中了解。其中只记录了该版本比较主要的强化功能和变更。

### 新的 SSH 组件

一个全新的 `SSH` 组件在此发行版本中登场。此功能让你可以轻易的 SSH 至远程服务器并执行命令。更多信息，可以参阅 [SSH 组件文档](/docs/ssh)。

新的 `php artisan tail` 指令就是使用这个新的 SSH 组件。更多的信息，请参阅 `tail` [指令集文档](http://laravel.com/docs/ssh#tailing-remote-logs)。

### Boris In Tinker

如果您的系统支持 [Boris REPL](https://github.com/d11wtq/boris)，`php artisan thinker` 指令将会使用到它。系统中也必须先行安装好 `readline` 和 `pcntl` 两个 PHP 套件。如果你没这些套件，从 4.0 之后将会使用到它。

### Eloquent 强化

Eloquent 添加了新的 `hasManyThrough` 关系链。想要了解更多，请参见 [Eloquent 文档](/docs/eloquent#has-many-through)。

一个新的 `whereHas` 方法也同时登场，他将允许[检索基于关系模型的约束](/docs/eloquent#querying-relations)。

### 数据库读写分离

Query Builder 和 Eloquent 目前透过数据库层，已经可以自动做到读写分离。更多的信息，请参考 [文档](/docs/database#read-write-connections)。

### 队列排序

队列排序已经被支持，只要在 `queue:listen` 命令后将队列以逗号分隔送出。

### 失败队列作业处理

现在队列将会自动处理失败的作业，只要在 `queue:listen` 后加上 `--tries` 即可。更多的失败作业处理可以参见 [队列文档](/docs/queues#failed-jobs)。

### 缓存标签

缓存「区块」已经被「标签」取代。缓存标签允许你将多个「标签」指向同一个缓存对象，而且可以清空所有被指定某个标签的所有对象。更多使用缓存标签信息请见 [缓存文档](/docs/cache#cache-tags)。

### 更具弹性的密码提醒

密码提醒引擎已经可以提供更强大的开发弹性，如：认证密码、显示状态消息等等。使用强化的密码提醒引擎，更多的信息 [请参阅文档](/docs/security#password-reminders-and-reset)。

### 强化路由引擎

Laravel 4.1 拥有一个完全重新编写的路由层。API 一样不变。然而与 4.0 相比，速度快上 100%。整个引擎大幅的简化，且对于路由表达式的编译大大减少对 Symfony Routing 的依赖。

### 强化 Session 引擎

此发行版本中，我们亦发布了全新的 Session 引擎。如同路由增进的部分，新的 Session 曾更加简化且更快速。我们不再使用 Symfony 的 Session 处理工具，并且使用更简单、更容易维护的客制化解法。


### Doctrine DBAL

如果你有在你的迁移中使用到 `renameColumn`，之后你必须在 `composer.json` 里加 `doctrine/dbal` 进相依套件中。此套件不再默认包含在 Laravel 之中。
