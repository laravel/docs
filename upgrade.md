# Upgrade Guide

- [升级到 5.1.0](#upgrade-5.1.0)
- [升级到 5.0.16](#upgrade-5.0.16)
- [从 4.2 升级到 5.0](#upgrade-5.0)
- [从 4.1 升级到 4.2](#upgrade-4.2)
- [从 4.1.x 升级到 4.1.29](#upgrade-4.1.29)
- [从 4.1.25 升级到 4.1.26](#upgrade-4.1.26)
- [从 4.0 升级到 4.1](#upgrade-4.1)

<a name="upgrade-5.1.0"></a>
## 升级到 5.1.0

#### 估计升级时间, 少于 1 个小时

### 更新 `bootstrap/autoload.php` 文件

修改变量 `$compiledPath` 如下: 

    $compiledPath = __DIR__.'/cache/compiled.php';

### 创建 `bootstrap/cache` 文件夹

在 `bootstrap` 文件夹下, 创建 `cache` 文件夹 (`bootstrap/cache`). 
在 `bootstrap/cache` 文件夹下创建文件 `.gitignore` , 并放置以下代码: 

    *
    !.gitignore

此文件需要可读权限, 是用来放置框架的优化文件的地方, 如 `compiled.php`, `routes.php`, `config.php`, and `services.json`.

### 增加 `BroadcastServiceProvider` Provider

在  `config/app.php` 文件的 `providers` 数组里面, 增加一行 `Illuminate\Broadcasting\BroadcastServiceProvider`.

### 认证

`AuthController` 使用 `AuthenticatesAndRegistersUsers` trait, 如果你是用了 `AuthController` 的话, 你需要做几个修改, 只要是关于用户验证和创建. 

首先, 不再需要 `Guard` 和 `Registrar` 实例了, 可以把他们从控制器的构造器 (constructor) 里面移除. 

其次, 不再需要  `App\Services\Registrar` 类, 把 `validator` 和 `create` 两个方法复制粘帖到 `AuthController` 里面, 并注意在 `AuthController` 文件里引入 `Validator` 和 `User`. 

#### 密码 Controller

`PasswordController` 控制器不在需要任何的依赖, 你可以把他们去除.

### 验证

如果你有重写 `formatValidationErrors`, 或者 `formatErrors` 方法的话, 请使用 `Illuminate\Contracts\Validation\Validator`  而不是 `Illuminate\Validation\Validator` 实例.

### Eloquent

#### `create` 方法

Eloquent 的 `create` 方法, 现在可以在不使用参数的情况下调用, 如果你重写 `create` 方法的话, 请设置 `$attributes` 参数默认为空数组:

    public static function create(array $attributes = [])
    {
        // Your custom implementation
    }

#### `find` 方法

如果你重写 `find` 方法, 并在你的自有模型里面调用 `parent::find()`, 你现在需要修改为使用 `Eloquent 查询语句构造器` 下的 `find`:

    public static function find($id, $columns = ['*'])
    {
        $model = static::query()->find($id, $columns);

        // ...

        return $model;
    }

#### `lists` 方法

Eloquent 请求 `lists` 方法现在修改为返回 `集合`, 如果你想获取数组的话, 请使用 `all` 方法. 


    User::lists('id')->all();

需要注意的是, 在查询语句构造器中使用 `lists` 的话, 依旧是会返回数组. 

#### 时间日期格式化

在之前的版本中, 我们可以在模型中通过修改 `getDateFormat` 来更改数据保存的格式 (created_at, updated_at), 在新版本中, 提供了一个更加便捷的方法, 你可以在模型里面直接修改 `$dateFormat` 属性. 

序列化一个模型到数组或者 JSON 的话, 这个时间格式转换会同样应用到. 如果你想要序列化有自己的单独的格式, 可以在模型里面重写 `serializeDate(DateTime $date)` 方法. 

### Collection (集合) 类

#### `sortBy` 方法

新版本中, 调用 `sortBy` 会返回一个全新的集合, 而不是之前的修改原有的集合. 

    $collection = $collection->sortBy('name');

#### `groupBy` 方法

新版本中, 调用 `groupBy` 方法的话, 会返回 `集合` 实例集合, 如果你想返回的是数组的话, 请使用 `map` 来转换: 

    $collection->groupBy('type')->map(function($item)
    {
        return $item->all();
    });

#### `lists` 方法

`lists` 方法会返回 `集合` 实例, 而不是之前的数组, 你可以利用 `all` 方法来返回数组对象: 

    $collection->lists('id')->all();

### Commands & Handlers

在新版本中, `app/Commands` 已经被重命名为 `app/Jobs`, 然而, 你还是可以使用老的位置用来存放命令类文件, 并且你可以继续使用 `make:command` 和 `handler:command` Artisan 命令来生产命令类文件.

同样的, `app/Handlers` 已经被重命名为 `app/Listeners` 并且只存放命令监听器. 然而, 不要求你重新移动文件到新的目录, 并且你可以继续使用 `handler:event` 来生产事件处理器.

新的版本里提供了对 5.0 版本的向后兼容, 所以你可以按照你的速度慢慢一点点的升级. 

### Blade 模板

`createMatcher`, `createOpenMatcher`, 和 `createPlainMatcher` 已经从 Blade 编译器里面移除了. 请使用新的 `directive` 方法来创建自定义的匹配, 详见 [扩展 blade 模板引擎](/docs/{{version}}/blade#extending-blade).

### 测试

在 `tests/TestCase.php` 文件中添加 `$baseUrl` 属性: 

    protected $baseUrl = 'http://localhost';

### 翻译文件存放地 

默认的扩展库语言包文件存放地已经从原来的  `resources/lang/packages/{locale}/{namespace}` 迁移到 `resources/lang/vendor/{namespace}/{locale}` 文件夹上. 

举个栗子, `Acme/Anvil` 扩展库 `acme/anvil::foo` 英文的语言包从之前的 `resources/lang/packages/en/acme/anvil/foo.php` 迁移到 `resources/lang/vendor/acme/anvil/en/foo.php`.

### Amazon Web Services SDK

如果你使用 AWS 的 SQS 队列驱动器或者 AWS 的 SES 邮件发送驱动器, 你需要升级你的 AWS PHP SDK 到 3.0.

如果你使用 Amazon S3 文件系统驱动器, 你需要更新对应的扩展包版本:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`

### Deprecations

以下 Laravel 功能已经遗弃, 并且会在 5.2 版本发布后完全移除: 

<div class="content-list" markdown="1">
- 路由过滤器会被中间件机制替换 [middleware](/docs/{{version}}/middleware).
- `Illuminate\Contracts\Routing\Middleware` 会被遗弃. 不需要任何 `contract` 来使用中间件. 另外, `TerminableMiddleware` contract 会被遗弃. 不在需要 `implementing` 多余的接口, 只需要在中间件中定义一个 `terminate` 方法即可.
- `Illuminate\Contracts\Queue\ShouldBeQueued` contract 会被 `Illuminate\Contracts\Queue\ShouldQueue` 替代.
- Iron.io "推送队列" 会被 Iron.io 队列和 [队列监听器](/docs/{{version}}/queues#running-the-queue-listener) 替代.
- `Illuminate\Foundation\Bus\DispatchesCommands` trait 遗弃并重命名为 `Illuminate\Foundation\Bus\DispatchesJobs`.
- `Illuminate\Container\BindingResolutionException` 重命名为 `Illuminate\Contracts\Container\BindingResolutionException`.
- 服务容器里的 `bindShared` 方法将会被 `singleton` 替代.
- Eloquent 和 请求构造器里面的 `pluck` 被重命名为 `value`.
- 集合类的 `fetch` 方法会被 `pluck` 替代.
- `array_fetch` 帮助方法会被 `array_pluck` 替代.
</div>

<a name="upgrade-5.0.16"></a>
## 升级到 5.0.16

在 `bootstrap/autoload.php` 文件中, 把 `$compiledPath` 变量更新为：

   $compiledPath = __DIR__.'/../vendor/compiled.php';

<a name="upgrade-5.0"></a>
## 从 4.2 升级到 5.0

### 全新安装，然后迁移

推荐的升级方式是建立一个全新的 Laravel `5.0` 项目，然后复制您在 `4.2` 的文件到此新的应用程序，这将包含控制器、路由、Eloquent 模型、Artisan 命令（Asset）、资源和关于此应用程序的其他特定文件。

最开始，[安装新的 Laravel 5 应用程序](/docs/{{version}}/installation)到新的本地目录下，我们将详细探讨迁移各部分的过程。

### Composer 依赖与组件

别忘了将任何附加于 Composer 的依赖组件加入 5.0 应用程序内，包含第三方代码(例如 SDKs)。

部分组件也许不兼容刚发布的 Laravel 5 版本，请向组件管理者确认该组件支持 Laravel 5 的版本，当您在 Composer 内加入任何组件，请执行 `composer update`。

### 命名空间
默认情况下，Laravel 4 没有在应用程序的源码中使用命名空间，所以，举例来说，所有的 Eloquent 模型和控制器仅存在「全局」的命名空间下，为了更快速的迁移，Laravel 5 也允许您可以将这些类别一样保留在「全局」的命名空间。

### 设置文件

#### 迁移环境变量

复制新的 `.env.example` 文件到 `.env`，在 `5.0` 这相当于原本的 `.env.php`。像是您的 `APP_ENV` 和 `APP_KEY` (您的加密钥匙)、数据库认证和您的缓存驱动与 session 驱动。

此外，复制原先自定义的 `.env.php` 文件，并修改为 `.env` (本机环境的真实设置值) 和 `.env.example` (给其他团队成员的示例)。

更多关于环境设置值，请见[完整文档](/docs/{{version}}/configuration#environment-configuration)。

> **注意:** 在部署 Laravel 5 应用程序之前，您需要在正式主机上放置 `.env` 文件并设置适当的值。

#### 设置文件

Laravel 5.0 不再使用 `app/config/{environmentName}/` 目录结构来提供对应该环境的设置文件，取而代之的是，将环境对应的设置值复制到 `.env`，然后在设置文件使用 `env('key', 'default value')` 来访问，您可以在 `config/database.php` 文件内看到相关范例。

将设置文件放在 `config/` 目录下，来表示所有环境共用的设置文件，或是在文件内使用 `env()` 来取得对应该环境的设置值。

请记住，若您在 `.env` 文件内增加 key 值，同时也要对应增加到 `.env.example` 文件中，这将可以帮助团队成员修改他们的 `.env` 文件。

### 路由

复制原本的 `routes.php` 文件到 `app/Http/routes.php`。

### 控制器

下一步，请将所有的控制器复制到 `app/Http/Controllers` 目录，既然在本指南中我们不打算迁移到完整的命名空间，请将 `app/Http/Controllers` 添加到 `composer.json` 的 `classmap`，接下来，您可以从 `app/Http/Controllers/Controller.php` 基础抽象类中移除命名空间，并确认迁移过来的控制器要继承这个基础类。

在 `app/Providers/RouteServiceProvider.php` 文件中，将 `namespace` 属性设置为 `null`。

### 路由过滤器

将过滤器绑定从原来的 `app/filters.php` 复制到 `app/Providers/RouteServiceProvider.php` 的 `boot()` 方法中，并在 `app/Providers/RouteServiceProvider.php` 加入 `use Illuminate\Support\Facades\Route;` 来继续使用 `Route` Facade。

您不需要移动任何 Laravel 4.0 默认的过滤器，像是 `auth` 和 `csrf` 。他们已经内置，只是换作以中间件形式出现。那些在路由或控制器内有参照到旧有的过滤器 (例如 `['before' => 'auth']`) 请修改参照到新的中间件 (例如 `['middleware' => 'auth'].`)

Laravel 5 并没有将过滤器移除，您一样可以使用 `before` 和 `after` 绑定和使用您自定义的过滤器。

### 全局 CSRF

默认情况下，所有路由都会使用[CSRF 保护](/docs/{{version}}/routing#csrf-protection)。若想关闭他们，或是在指定在特定路由开启，请移除 `App\Http\Kernel` 中 `middleware` 数组内的这一行：

如果您想在其他地方使用它，加入这一行到 `$routeMiddleware`:

    'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

现在，您可于路由内使用 `['middleware' => 'csrf']` 即可个别添加中间件到路由/控制器。了解更多关于中间件，请见[完整文档](/docs/{{version}}/middleware)。

你可以建立新的 `app/Models` 目录来放置所有 Eloquent 模型。并且同样的，在 `composer.json` 将此目录添加到 `classmap` 内。

在模型内加入 `SoftDeletingTrait` 来使用`Illuminate\Database\Eloquent\SoftDeletes`.

#### Eloquent 缓存

Eloquent 不再提供 `remember` 方法来缓存查询。现在你需要手动使用 `Cache::remember` 方法快速缓存。了解更多关于缓存，请见[完整文档](/docs/{{version}}/cache)。

### 会员认证模型

要使用 Laravel 5 的会员认证系统，请遵循以下指引来升级您的 `User` 模型：

**从 `use` 区块删除以下内容：**

```php
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
```

**添加以下内容到 `use` 区块：**

```php
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
```

**移除 UserInterface 和 RemindableInterface 接口。**

**实现以下接口：**

```php
implements AuthenticatableContract, CanResetPasswordContract
```

**在类中声明引入以下 traits：**

```php
use Authenticatable, CanResetPassword;
```

**如果你引入了上面的 traits，从 use 区块和类声明中移除 `Illuminate\Auth\Reminders\RemindableTrait` 和 `Illuminate\Auth\UserTrait`**

### Cashier 的用户需要的修改

[Laravel Cashier](/docs/{{version}}/billing) 的 trait 和接口名称已作修改。trait 请改用 `Laravel\Cashier\Billable` 取代 `BillableTrait`。接口请改用 `Laravel\Cashier\Contracts\Billable` 取代 `Larave\Cashier\BillableInterface` 。不需要修改任何方法。

### Artisan 命令

将所有的命令从旧的 `app/commands` 目录移到新的`app/Console/Commands` 目录。接下来，把 `app/Console/Commands` 目录添加到 `composer.json` 的 `classmap` 中。

然后，复制 Artisan 命令列表从 `start/artisan.php` 到 `app/Console/Kernel.php` 文件的 `command` 数组内。

### 数据库迁移和数据填充

如果在您的数据库内已经有 users 表，请移除 Laravel 5 内置的两个迁移文件。

将所有的迁移文件从旧的 `app/database/migrations` 目录复制到新的 `database/migrations` 。所有的数据填充文件也要从 `app/database/seeds` 复制到 `database/seeds`。

### 全局 IoC 绑定

若您在 `start/global.php` 有绑定任何 [IoC](/docs/{{version}}/container)，请将它们复制到 `app/Providers/AppServiceProvider.php` 内的 `register` 方法，您可能需要引入 `App` facade。

你可以选择将这些绑定，依照类型拆分到不同的服务提供者中。

### 视图

将所有的视图从旧的 `app/views` 复制到新的`resources/views` 目录内。

### Blade 标签修改

从安全的角度考虑，Laravel 5.0 会过滤所有输出，不论您使用 `{{ }}` 或 `{{{ }}}` 标签。您可以使用 `{!! !!}` 新的标签来取消输出过滤。请务必 **确定** 输出内容是安全地才使用 `{!! !!}` 标签。

不过，如果您 **仍然必须** 使用旧的 Blade 语法，请在 `AppServiceProvider@register` 开头加入以下内容：

```php
\Blade::setRawTags('{{', '}}');
\Blade::setContentTags('{{{', '}}}');
\Blade::setEscapedContentTags('{{{', '}}}');
```

但是轻易不要这样做，这可能使您的应用进程更加容易受到 XSS 攻击，并且用 `{{--` 来注释代码将不再起作用。

### 多语言配置文件

将所有的多语言配置文件从旧的 `app/lang` 目录复制到新的`resources/lang` 目录。

### 公开目录

将 `4.2` 版公共目录内的资源复制到新应用程序内的`public` 目录。并确认保留 `5.0` 版的 `index.php` 文件。

### 测试

将所有的测试文件从旧的 `app/tests` 复制到 `tests` 目录。

### 各式各样的文件

复制项目内其他各式各样的文件，例如：`.scrutinizer.yml`, `bower.json` 以及其他类似工具的设置文件。

您可以将 Sass，Less 或 CoffeeScript 移动到任何您想放置的地方。 `resources/assets` 目录是一个不错的默认位置。

### 表单和 HTML 辅助函数

如果您使用表单或 HTML 辅助函数，您将会看到以下错误 `class 'Form' not found` 或 `class 'Html' not found` 。Form 类以及 HTML 辅助函数在 Laravel 5.0 中已经废弃了；不过，这里有一些替代方法，比如基于社区驱动的，由 [Laravel Collective](http://laravelcollective.com/docs/{{version}}/html) 维护。

比如，你可以在 `composer.json` 文件中的 `require` 区块增加 `"laravelcollective/html": "~5.0"`。

您也需要添加表单和 HTML 的 facades 以及服务提供者。 编辑 `config/app.php` 文件，添加此行到 'providers' 数组内：

    'Collective\Html\HtmlServiceProvider',

接着，添加以下到 'aliases' 数组内：

    'Form' => 'Collective\Html\FormFacade',
    'Html' => 'Collective\Html\HtmlFacade',

### 缓存管理员

如果您的程序注入 `Illuminate\Cache\CacheManager` 来取得非 Facade 版本的 Laravel 缓存，请改用 `Illuminate\Contracts\Cache\Repository` 注入。

### 分页

请将所有的 `$paginator->links()` 用 `$paginator->render()` 取代。

Replace any calls to `$paginator->getFrom()` and `$paginator->getTo()` with `$paginator->firstItem()` and `$paginator->lastItem()` respectively.

Remove the "get" prefix from calls to `$paginator->getPerPage()`, `$paginator->getCurrentPage()`, `$paginator->getLastPage()` and `$paginator->getTotal()` (e.g. `$paginator->perPage()`).

### Beanstalk 队列

Laravel 5.0 使用 `"pda/pheanstalk": "~3.0"` 取代原本的 `"pda/pheanstalk": "~2.1"`。

### Remote

Remote 组件已不再使用。

### 工作区

工作区组件已不再使用。

<a name="upgrade-4.2"></a>
## 从 4.1 升级到 4.2

### PHP 5.4+

Laravel 4.2 需要 PHP 5.4.0 以上。

### 默认加密

增加一个新的 `cipher` 选项在你的 `app/config/app.php` 设置文件中。其选项值应为 `MCRYPT_RIJNDAEL_256`。

    'cipher' => MCRYPT_RIJNDAEL_256

该设置可用于设置所使用的 Laravel 加密工具的默认加密方法。

> **附注:** 在 Laravel 4.2，默认加密方法为`MCRYPT_RIJNDAEL_128` (AES)，被认为是最安全的加密。必须将加密改回`MCRYPT_RIJNDAEL_256` 来解密在 Laravel <= 4.1 下加密的 cookies/values

### 软删除模型现在改使用特性

如果你在模型下有使用软删除，现在 `softDeletes` 的属性已经被移除。你现在要使用 `SoftDeletingTrait` 如下：

    use Illuminate\Database\Eloquent\SoftDeletingTrait;

    class User extends Eloquent {
        use SoftDeletingTrait;
    }

你一样必须手动增加 `deleted_at` 字段到你的 `dates` 属性中：

    class User extends Eloquent {
        use SoftDeletingTrait;

        protected $dates = ['deleted_at'];
    }

而所有软删除的 API 使用方式维持相同。

> **附注:** `SoftDeletingTrait` 无法在基本模型下被使用。他只能在一个实际模型类别中使用。

### 视图 / 分页 / 环境 类别改名

如果你直接使用 `Illuminate\View\Environment` 或 `Illuminate\Pagination\Environment` 类别，请更新你的代码将其改为参照 `Illuminate\View\Factory` 和 `Illuminate\Pagination\Factory`。改名后的这两个类别更可以代表他们的功能。

### Additional Parameter On Pagination Presenter

如果你扩展了 `Illuminate\Pagination\Presenter` 类别，抽象方法 `getPageLinkWrapper` 参数表变成要加上 `rel` 参数：

    abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Iron.Io Queue 加密

如果你使用 Iron.io queue 驱动，你将需要增加一个新的 `encrypt` 选项到你的 queue 设置文件中：

    'encrypt' => true

<a name="upgrade-4.1.29"></a>
## 从 4.1.x 升级到 4.1.29

Laravel 4.1.29 对于所有的数据库驱动加强了 column quoting 的部分。当你的模型中**没有**使用 `fillable` 属性，他保护你的应用程序不会受到 mass assignment 漏洞影响。如果你在模型中使用 `fillable` 属性来防范 mass assignment，你的应用程序将不会有漏洞。如果你使用 `guarded` 且在「更新」或「保存」类型的函式中，传递了末端用户控制的数组，那你应该立即升级到 `4.1.29` 以避免 mass assignment 的风险。

升级到 Laravel 4.1.29，只要 `composer update` 即可。在这个发行版本中没有重大的更新。

<a name="upgrade-4.1.26"></a>
## 从 4.1.25 升级到 4.1.26

Laravel 4.1.26 采用了针对「记得我」cookies 的安全性更新。在此更新之前，如果一个记得我的 cookies 被恶意用户劫持，该 cookie 将还可以生存很长一段时间，即使真实用户重设密码或者注销亦同。

此更动需要在你的 `users` (或者类似的) 的数据表中增加一个额外的 `remember_token` 字段。在更新之后，当用户每次登录你的应用程序将会有一个全新的 token 将会被指派。这个 token 也会在用户注销应用程序后被更新。这个更新的影响为：如果一个「记得我」的 cookie 被劫持，只要用户注销应用程序将会废除该 cookie。

### 升级路径

首先，增加一个新的字段，可空值、属性为 VARCHAR(100)、TEXT 或同类型的字段 `remember_token` 到你的 `users` 数据表中。

然后，如果你使用 Eloquent 认证驱动，依照下面更新你的 `User` 类别的三个方法：

    public function getRememberToken()
    {
        return $this->remember_token;
    }

    public function setRememberToken($value)
    {
        $this->remember_token = $value;
    }

    public function getRememberTokenName()
    {
        return 'remember_token';
    }

> **附注:** 所有现存的「记得我」sessions 在此更新后将会失效，所以应用程序的所有用户将会被迫重新登录。

### 组件管理者

两个新的方法被加入到 `Illuminate\Auth\UserProviderInterface` 接口。范例实现方式可以在默认驱动中找到：

    public function retrieveByToken($identifier, $token);

    public function updateRememberToken(UserInterface $user, $token);

`Illuminate\Auth\UserInterface` 也加了三个新方法描述在「升级路径」。

<a name="upgrade-4.1"></a>
## 从 4.0 升级到 4.1

### 升级你的 Composer 依赖性

升级你的应用程序至 Laravel 4.1，将 `composer.json` 里的 `laravel/framework` 版本更改至 `4.1.*`。

### 文件置换

将你的 `public/index.php` 置换成 [这个 repository 的干净版本](https://github.com/laravel/laravel/blob/v4.1.0/public/index.php)。

同样的，将你的 `artisan` 置换成 [这个 repository 的干净版本](https://github.com/laravel/laravel/blob/v4.1.0/artisan)。

### 添加设置文件及选项

更新你在设置文件 `app/config/app.php` 里的 `aliases` 和 `providers` 数组。而更新的选项值可以在 [这个文件](https://github.com/laravel/laravel/blob/v4.1.0/app/config/app.php) 中找到。请确定将你后来加入自定和组件所需的 providers / aliases 加回数组中。

从 [这个 repository](https://github.com/laravel/laravel/blob/v4.1.0/app/config/remote.php) 增加 `app/config/remote.php` 文件。

在你的 `app/config/session.php` 增加新的选项 `expire_on_close`。而默认值为 `false`。

在你的 `app/config/queue.php` 文件里添加 `failed` 设置区块。以下为区块的默认值：

    'failed' => array(
        'database' => 'mysql', 'table' => 'failed_jobs',
    ),

**（非必要）** 在你的 `app/config/view.php` 里，将 `pagination` 设置选项更新为 `pagination::slider-3`。

### 更新控制器（Controllers）

如果 `app/controllers/BaseController.php` 有 `use` 语句在最上面，将 `use Illuminate\Routing\Controllers\Controller;` 改为 `use Illuminate\Routing\Controller;`。

### 更新密码提醒

密码提醒功能已经大幅修正拥有更大的弹性。你可以执行 Artisan 指令 `php artisan auth:reminders-controller` 来检查新的存根控制器。你也可以浏览 [更新文件](/docs/security#password-reminders-and-reset) 然后相应的更新你的应用程序。

更新你的 `app/lang/en/reminders.php` 语系文件来符合 [这个新版文件](https://github.com/laravel/laravel/blob/v4.1.0/app/lang/en/reminders.php)。

### 更新环境侦测

为了安全因素，不再使用网域网址来侦测辨别应用程序的环境。因为这些直很容易被伪造欺骗，继而让攻击者透过请求来达到变更环境。所以你必须改为使用机器的 hostname（在 Mac & Ubuntu 下执行 `hostname` 出来的值）

（译按：的确原有方式有安全性考量，但对于现行 VirtualHost 大量使用下，反而这样改会造成不便）

### 更简单的日志文件

Laravel 目前只会产生单一的日志文件：`app/storage/logs/laravel.log`。然而，你还是可以透过设置你的 `app/start/global.php` 文件来更改他的行为。

### 删除重定向结尾的斜线

在你的 `bootstrap/start.php` 文件中，移除调用 `$app->redirectIfTrailingSlash()`。这个方法已不再需要了，因为之后将会改以框架内的 `.htaccess` 来处理。

然后，用 [新版](https://github.com/laravel/laravel/blob/v4.1.0/public/.htaccess) 替换掉你 Apache 中的 `.htaccess` 文件，来处理结尾的斜线问题。

### 取得目前路由

取得目前路由的方法由 `Route::getCurrentRoute()` 改为 `Route::current()`。

### Composer 更新

一旦你完成以上的更新，你可以执行 `composer update` 来更新应用程序的核心文件。如果有 class load 错误，请在 `update` 之后加上 `--no-scripts`，如：`composer update --no-scripts`。

### 万用字符事件监听者

万用字符事件监听者不再添加事件为参数到你的处理函数。如果你需要寻找你触发的事件你应该用 `Event::firing()`.
