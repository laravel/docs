# Authentication-认证

- [Introduction-介绍](#introduction)
- [Authentication Quickstart-验证快速入门](#authentication-quickstart)
    - [Routing-路由](#included-routing)
    - [Views-视图](#included-views)
    - [Authenticating-认证](#included-authenticating)
    - [Retrieving The Authenticated User-检索验证的用户](#retrieving-the-authenticated-user)
    - [Protecting Routes-保护路由](#protecting-routes)
- [Manually Authenticating Users-手动验证用户](#authenticating-users)
    - [Remembering Users-记住用户](#remembering-users)
    - [Other Authentication Methods-其他身份验证方法](#other-authentication-methods)
- [HTTP Basic Authentication-HTTP基本认证](#http-basic-authentication)
     - [Stateless HTTP Basic Authentication-无状态HTTP基本认证](#stateless-http-basic-authentication)
- [Resetting Passwords-重设密码](#resetting-passwords)
    - [Database Considerations-数据库注意事项](#resetting-database)
    - [Routing-路由](#resetting-routing)
    - [Views-视图](#resetting-views)
    - [After Resetting Passwords-重置密码后](#after-resetting-passwords)
- [Social Authentication-社会认证](#social-authentication)
- [Adding Custom Authentication Drivers-添加自定义的驱动程序认证](#adding-custom-authentication-drivers)

<a name="introduction"></a>
## Introduction-介绍

Laravel makes implementing authentication very simple. In fact, almost everything is configured for you out of the box. The authentication configuration file is located at `config/auth.php`, which contains several well documented options for tweaking the behavior of the authentication services.

Laravel使实现身份验证很简单。事实上，几乎一切都为您配置的开箱。验证配置文件位于config/auth.php`，其中包含几个文档选择调整的认证服务的行为。

### Database Considerations-数据库注意事项

By default, Laravel includes an `App\User` [Eloquent model](/docs/{{version}}/eloquent) in your `app` directory. This model may be used with the default Eloquent authentication driver. If your application is not using Eloquent, you may use the `database` authentication driver which uses the Laravel query builder.

默认情况下，Laravel包括一个`App\User` [Eloquent model](/docs/{{version}}/eloquent)在你的`app`目录中。该模型可用于使用默认口才认证驱动程序。如果您的应用程序没有使用Eloquent，你可以使用`database`，它使用Laravel查询生成器认证的驱动程序。

When building the database schema for the `App\User` model, make sure the password column is at least 60 characters in length.

当构建的数据库架构`App\User`模式，确保密码列长度至少为60个字符。

Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for "remember me" sessions being maintained by your application. This can be done by using `$table->rememberToken();` in a migration.

此外，你应该确认您的用户（或同等学历）表中包含一个可空，字符串 `remember_token`100个字符列。本专栏将被用来存储token“记住我”会通过你的申请被保留。这可以通过使用完成`$table->rememberToken();` 在一个迁移。

<a name="authentication-quickstart"></a>
## Authentication Quickstart-验证快速入门

Laravel ships with two authentication controllers out of the box, which are located in the `App\Http\Controllers\Auth` namespace. The `AuthController` handles new user registration and authentication, while the `PasswordController` contains the logic to help existing users reset their forgotten passwords. Each of these controllers uses a trait to include their necessary methods. For many applications, you will not need to modify these controllers at all.

Laravel附带两种认证控制器开箱，它位于的`App\Http\Controllers\Auth`命名空间。该`AuthController`处理新用户的注册和认证，而`PasswordController`包含的逻辑来帮助现有用户重置其忘记的密码。每个控制器的使用特点，包括他们的必要方法。对于许多应用程序，你不需要在所有修改这些控制器。

<a name="included-routing"></a>
### Routing-路由

By default, no [routes](/docs/{{version}}/routing) are included to point requests to the authentication controllers. You may manually add them to your `app/Http/routes.php` file:

缺省情况下，没有[路由](/docs/{{version}}/routing)被包括以指向请求到认证控制器。您可以手动添加到您的`app/Http/routes.php`文件：

    // Authentication routes...认证路线...
    Route::get('auth/login', 'Auth\AuthController@getLogin');
    Route::post('auth/login', 'Auth\AuthController@postLogin');
    Route::get('auth/logout', 'Auth\AuthController@getLogout');

    // Registration routes...注册路线...
    Route::get('auth/register', 'Auth\AuthController@getRegister');
    Route::post('auth/register', 'Auth\AuthController@postRegister');

<a name="included-views"></a>
### Views-视图

Though the authentication controllers are included with the framework, you will need to provide [views](/docs/{{version}}/views) that these controllers can render. The views should be placed in the `resources/views/auth` directory. You are free to customize these views however you wish. The login view should be placed at `resources/views/auth/login.blade.php`, and the registration view should be placed at `resources/views/auth/register.blade.php`.

虽然认证控制器都包含在框架中，您将需要提供[视图](/docs/{{version}}/views)，这些控制器可以呈现。该视图应放在`resources/views/auth`目录。你可以自由定制这些观点不过你的愿望。登录视图应放在`resources/views/auth/login.blade.php`，注册视图应该被放置在`resources/views/auth/register.blade.php`。

#### Sample Authentication Form-样本验证表单

    <!-- resources/views/auth/login.blade.php -->

    <form method="POST" action="/auth/login">
        {!! csrf_field() !!}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password" id="password">
        </div>

        <div>
            <input type="checkbox" name="remember"> Remember Me
        </div>

        <div>
            <button type="submit">Login</button>
        </div>
    </form>

#### Sample Registration Form-采样登记表

    <!-- resources/views/auth/register.blade.php -->

    <form method="POST" action="/auth/register">
        {!! csrf_field() !!}

        <div class="col-md-6">
            Name
            <input type="text" name="name" value="{{ old('name') }}">
        </div>

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div class="col-md-6">
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">Register</button>
        </div>
    </form>

<a name="included-authenticating"></a>
### Authenticating-认证

Now that you have routes and views setup for the included authentication controllers, you are ready to register and authenticate new users for your application. You may simply access your defined routes in a browser. The authentication controllers already contain the logic (via their traits) to authenticate existing users and store new users in the database.

现在，你有路线和看法设置了包括验证控制器，您就可以注册并为您的应用验证新用户。你可以简单地访问在浏览器中定义的路由。认证控制器已经包含的逻辑（经由他们的性状）来认证现有用户和存储在数据库中的新用户。

When a user is successfully authenticated, they will be redirected to the `/home` URI, which you will need to register a route to handle. You can customize the post-authentication redirect location by defining a `redirectTo` property on the `AuthController`:

当用户身份验证成功，他们将被重定向到`/home` URI，你需要注册一个途径来处理。您可以通过定义一个定制的认证后重定向位置`redirectTo`的property `AuthController`：

    protected $redirectTo = '/dashboard';

#### Customizations-自定义

To modify the form fields that are required when a new user registers with your application, or to customize how new user records are inserted into your database, you may modify the `AuthController` class. This class is responsible for validating and creating new users of your application.

要修改所需的表单字段时，一个新的用户注册与应用程序，或者自定义如何将新用户记录插入到你的数据库，你可以修改`AuthController`类。这个类负责验证和创建应用程序的新用户。

The `validator` method of the `AuthController` contains the validation rules for new users of the application. You are free to modify this method as you wish.

该`validator`的方法`AuthController`包含应用程序的新用户的验证规则。你可以自由的要修改这个方法。

The `create` method of the `AuthController` is responsible for creating new `App\User` records in your database using the [Eloquent ORM](/docs/{{version}}/eloquent). You are free to modify this method according to the needs of your database.

在`create` 的方法`AuthController`负责创建新的`App\User`在使用你的数据库的记录[Eloquent ORM](/docs/{{version}}/eloquent)。你可以自由根据你的数据库的需求来修改这个方法。

<a name="retrieving-the-authenticated-user"></a>
### Retrieving The Authenticated User-检索验证的用户

You may access the authenticated user via the `Auth` facade:

您可以通过访问身份验证的用户`Auth` facade：

    $user = Auth::user();

Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance:

另外，一旦用户通过验证后，您可以通过访问身份验证的`Illuminate\Http\Request`的实例：

    <?php namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class ProfileController extends Controller
    {
        /**
         * Update the user's profile.更新用户的配置文件。
         *
         * @param  Request  $request
         * @return Response
         */
        public function updateProfile(Request $request)
        {
            if ($request->user()) {
                // $request->user() returns an instance of the authenticated user...
            }
        }
    }

#### Determining If The Current User Is Authenticated-确定如果当前用户进行身份验证

To determine if the user is already logged into your application, you may use the `check` method on the `Auth` facade, which will return `true` if the user is authenticated:

要确定是否已经登录到您的应用程序的用户，您可以使用`check`的方法`Auth`facade，这将返回`true`，如果用户进行身份验证：

    if (Auth::check()) {
        // The user is logged in...该用户是在记录...
    }

However, you may use middleware to verify that the user is authenticated before allowing the user access to certain routes / controllers. To learn more about this, check out the documentation on [protecting routes](/docs/{{version}}/authentication#protecting-routes).

但是，您可以使用中间件来验证用户允许某些routes / controllers的用户访问之前进行身份验证。要了解更多关于此，请查看文档的[路由保护（protecting routes）](/docs/{{version}}/authentication#protecting-routes)。

<a name="protecting-routes"></a>
### Protecting Routes-保护路由

[Route middleware](/docs/{{version}}/middleware) can be used to allow only authenticated users to access a given route. Laravel ships with the `auth` middleware, which is defined in `app\Http\Middleware\Authenticate.php`. All you need to do is attach the middleware to a route definition:

[路由中间件](/docs/{{version}}/middleware)可以用来只允许通过认证的用户访问指定的路线。Laravel附带的身份验证的中间件，这是在定义`app\Http\Middleware\Authenticate.php`。所有你需要做的是中间件连接到路由定义：

    // Using A Route Closure...通过路由封...

    Route::get('profile', ['middleware' => 'auth', function() {
        // Only authenticated users may enter...
    }]);

    // Using A Controller...使用控制器...

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'ProfileController@show'
    ]);

Of course, if you are using [controller classes](/docs/{{version}}/controllers), you may call the `middleware` method from the controller's constructor instead of attaching it in the route definition directly:

当然，如果你使用的是[控制器类](/docs/{{version}}/controllers)，您可调用`中间件`直接的路由定义安装它从控制器的构造方法，而不是：

    public function __construct()
    {
        $this->middleware('auth');
    }

<a name="authenticating-users"></a>
## Manually Authenticating Users-手动验证用户

Of course, you are not required to use the authentication controllers included with Laravel. If you choose to remove these controllers, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch!

当然，你不需要使用附带Laravel验证控制器。如果你选择删除这些控制器，则需要直接使用Laravel认证类来管理用户身份验证。不要担心，这是不在话下！

We will access Laravel's authentication services via the `Auth` [facade](/docs/{{version}}/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method:

我们将通过访问Laravel的认证服务验证 的[facade](/docs/{{version}}/facades)，所以我们需要确保导入`Auth` facade,在类的顶部。接下来，让我们看看该尝试的方法：

    <?php namespace App\Http\Controllers;

    use Auth;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Handle an authentication attempt.处理身份验证尝试。
         *
         * @return Response
         */
        public function authenticate()
        {
            if (Auth::attempt(['email' => $email, 'password' => $password])) {
                // Authentication passed...
                return redirect()->intended('dashboard');
            }
        }
    }


The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the hashed `password` value passed to the method via the array. If the two hashed passwords match an authenticated session will be started for the user.

该`attempt` 方法接受 键/值对的数组作为第一个参数。数组中的值将被用来查找数据库中的表中的用户。所以，在上面的例子中，用户将通过的值中检索`email`列。如果用户没有发现存储在数据库中的哈希`password`将与散列进行比较口令传递给经由所述阵列的方法的值。如果这两个散列口令相匹配的认证会话将开始为用户。

The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned.

该  `attempt` 方法将返回真，如果认证`true` 。否则，`false` 将被退回。

The `intended` method on the redirector will redirect the user to the URL they were attempting to access before being caught by the authentication filter. A fallback URI may be given to this method in case the intended destination is not available.

在`intended` 上的重定向方法将被抓住的认证过滤器之前将用户重定向到他们尝试访问的URL。万一备用的URI，可给予该方法的预期目标是不可用。

If you wish, you also may add extra conditions to the authentication query in addition to the user's e-mail and password. For example, we may verify that user is marked as "active":

如果你愿意，你也可以在除了用户的电子邮件和密码添加额外的条件，认证查询。例如，我们可以验证的用户将被标记为“active”：


    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        // The user is active, not suspended, and exists.用户是活跃的，不暂停，并存在。
    }

To log users out of your application, you may use the `logout` method on the `Auth` facade. This will clear the authentication information in the user's session:

以用户身份登录您的应用程序，你可以使用`logout`的方法`Auth` facade。这将清除用户的会话认证信息：
    Auth::logout();

> **Note:** In these examples, `email` is not a required option, it is merely used as an example. You should use whatever column name corresponds to a "username" in your database.

> **注意：**在这些例子中，`email`是不必需的选项，它只是用来作为一个例子。您应该使用什么列名对应于数据库中的一个“username”。

<a name="remembering-users"></a>
## Remembering Users-记住用户

If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method, which will keep the user authenticated indefinitely, or until they manually logout. Of course, your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token.

如果您想提供“记住我”在您的应用程序的功能，你可以把一个布尔值作为第二个参数的`attempt`方法，这将让用户身份验证无限期，或直到手动注销。当然，你的用户表必须包含字符串`remember_token`列，将被用于存储“记住我”的标记。

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // The user is being remembered...用户所记住...
    }

If you are "remembering" users, you may use the `viaRemember` method to determine if the user was authenticated using the "remember me" cookie:

如果你是“记忆”的用户，您可以使用`viaRemember`方法来确定用户是否使用被认证的“记住我”的cookie：

    if (Auth::viaRemember()) {
        //
    }

<a name="other-authentication-methods"></a>
### Other Authentication Methods-其他身份验证方法

#### Authenticate A User Instance-验证用户实例

If you need to log an existing user instance into your application, you may call the `login` method with the user instance. The given object must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/{{version}}/contracts). Of course, the `App\User` model included with Laravel already implements this interface:

如果您需要登录现有的用户实例到你的应用程序，你可以调用`login`方法与用户实例。给定对象必须是一个实现`Illuminate\Contracts\Auth\Authenticatable` 的[合同(contract)](/docs/{{version}}/contracts)。当然，`App\User`包含Laravel模型已经实现了这个接口：

    Auth::login($user);

#### Authenticate A User By ID-验证用户编号查询

To log a user into the application by their ID, you may use the `loginUsingId` method. This method simply accepts the primary key of the user you wish to authenticate:

要通过自己的ID登录用户到应用程序，你可以使用`loginUsingId`方法。这种方法只接受你想验证用户的主键：

    Auth::loginUsingId(1);

#### Authenticate A User Once-验证用户一次

You may use the `once` method to log a user into the application for a single request. No sessions or cookies will be utilized, which may be helpful when building a stateless API. The `once` method has the same signature as the `attempt` method:

您可以使用`once`的方法来记录用户到应用程序的一个请求。没有会议或Cookie会被利用，建立一个无状态的API时，这可能会有帮助。在`once`方法具有相同的签名`attempt`的方法：



    if (Auth::once($credentials)) {
        //
    }

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication-HTTP基本认证

[HTTP Basic Authentication](http://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/{{version}}/middleware) to your route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it:

[HTTP基本身份验证](http://en.wikipedia.org/wiki/Basic_access_authentication)提供了一种快速的方法来验证你的应用程序的用户没有设立专门的“登录”页面。上手，附加`auth.basic`  [中间件](/docs/{{version}}/middleware)到您的路线。该`auth.basic`中间件包含在Laravel框架，所以你不需要去定义它：


    Route::get('profile', ['middleware' => 'auth.basic', function() {
        // Only authenticated users may enter...只有通过认证的用户可以进入...
    }]);

Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will use the `email` column on the user record as the "username".

一旦中间件已附加到路由，你会自动在您的浏览器访问的路由时提示输入凭据。默认情况下，`auth.basic`中间件将使用`电子邮件`栏上的用户记录为“用户名”。

#### A Note On FastCGI-一个注记的FastCGI

If you are using PHP FastCGI, HTTP Basic authentication may not work correctly out of the box. The following lines should be added to your `.htaccess` file:

如果您使用的是PHP的FastCGI，HTTP基本身份验证可能无法正确开箱工作。接下来的几行应该添加到您的的`.htaccess`文件：

    RewriteCond %{HTTP:Authorization} ^(.+)$
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic Authentication-无状态HTTP基本认证

You may also use HTTP Basic Authentication without setting a user identifier cookie in the session, which is particularly useful for API authentication. To do so, [define a middleware](/docs/{{version}}/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application:

您也可以使用HTTP基本身份验证，而不在会议上，这是API认证特别有用设置用户标识符的cookie。要做到这一点，[定义一个中间件](/docs/{{version}}/middleware)调用`onceBasic`方法。如果没有响应被返回`onceBasic`方法，该请求可以被进一步传递到应用程序：

    <?php namespace Illuminate\Auth\Middleware;

    use Auth;
    use Closure;
    use Illuminate\Contracts\Routing\Middleware;

    class AuthenticateOnceWithBasicAuth implements Middleware
    {
        /**
         * Handle an incoming request.处理传入的请求。
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return Auth::onceBasic() ?: $next($request);
        }

    }

Next, [register the route middleware](/docs/{{version}}/middleware#registering-middleware) and attach it to a route:

接下来，[注册路线中间件](/docs/{{version}}/middleware#registering-middleware)和其附加到路由：

    Route::get('api/user', ['middleware' => 'auth.basic.once', function() {
        // Only authenticated users may enter...
    }]);

<a name="resetting-passwords"></a>
## Resetting Passwords-重设密码

<a name="resetting-database"></a>
### Database Considerations-数据库注意事项

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

大多数Web应用程序提供一种方法让用户重置其忘记密码。而不是强迫你重新实现此上的每个应用程序，Laravel提供了方便的方法来发送密码提醒和进行密码重置。

To get started, verify that your `App\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. Of course, the `App\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

要开始使用，验证您的 `App\User`模式实现了`Illuminate\Contracts\Auth\CanResetPassword`合同。当然，`App\User`模型包含在框架已经实现了这个接口，并采用`Illuminate\Auth\Passwords\CanResetPassword`特质，包括实现接口所需的方法。

#### Generating The Reset Token Table Migration-产生复位标记表迁移

Next, a table must be created to store the password reset tokens. The migration for this table is included with Laravel out of the box, and resides in the `database/migrations` directory. So, all you need to do is migrate:

接下来，表必须创建存储密码重置令牌。此表的迁移是包含Laravel开箱，并驻留在`database/migrations`目录。所以，你需要做的是迁移：

    php artisan migrate

<a name="resetting-routing"></a>
### Routing-路由

Laravel includes an `Auth\PasswordController` that contains the logic necessary to reset user passwords. However, you will need to define routes to point requests to this controller:

Laravel包括`Auth\PasswordController`包含需要重置用户密码逻辑。但是，你需要定义的路由指向请求到该控制器：

    // Password reset link request routes...密码重置链接请求的路线......
    Route::get('password/email', 'Auth\PasswordController@getEmail');
    Route::post('password/email', 'Auth\PasswordController@postEmail');

    // Password reset routes...密码重置路线...
    Route::get('password/reset/{token}', 'Auth\PasswordController@getReset');
    Route::post('password/reset', 'Auth\PasswordController@postReset');

<a name="resetting-views"></a>
### Views-视图

In addition to defining the routes for the `PasswordController`, you will need to provide views that can be returned by this controller. Don't worry, we will provide sample views to help you get started. Of course, you are free to style your forms however you wish.

除了 ​​定义的路由`PasswordController`，您将需要提供可以通过该控制器返回意见。不要担心，我们将提供样本的意见，以帮助您开始。当然，你可以自由，但是你希望你的风格形式。

#### Sample Password Reset Link Request Form-样品密码重置链接申请表

You will need to provide an HTML view for the password reset request form. This view should be placed at `resources/views/auth/password.blade.php`. This form provides a single field for the user's e-mail address, allowing them to request a password reset link:

您需要提供密码重置申请表的HTML视图。这种观点应该放在`resources/views/auth/password.blade.php`。这种形式为用户提供的电子邮件地址的单个字段，允许他们请求密码重置链接：

    <!-- resources/views/auth/password.blade.php -->

    <form method="POST" action="/password/email">
        {!! csrf_field() !!}

        <div>
        	Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <button type="submit">
                Send Password Reset Link
            </button>
        </div>
    </form>

When a user submits a request to reset their password, they will receive an e-mail with a link that points to the `getReset` method (typically routed at `/password/reset`) of the `PasswordController`. You will need to create a view for this e-mail at `resources/views/emails/password.blade.php`. The view will receive the `$token` variable which contains the password reset token to match the user to the password reset request. Here is an example e-mail view to get you started:

当用户提交请求重置其密码，他们将收到一封电子邮件与指向一个链接`getReset`方法（通常在路由`/password/reset`的）`PasswordController`。您将需要创建在查看该电子邮件`resources/views/emails/password.blade.php`。该视图将收到`$token`包含密码重置令牌来匹配用户的密码重置请求变量。下面是一个例子电子邮件，以供您参考：

    <!-- resources/views/emails/password.blade.php -->

    Click here to reset your password: {{ url('password/reset/'.$token) }}

#### Sample Password Reset Form-样品密码重置表

When the user clicks the e-mailed link to reset their password, they will be presented with a password reset form. This view should be placed at `resources/views/auth/reset.blade.php`.

当用户点击电子邮件发送链接重置其密码，他们将看到一个密码重置表格。这种观点应该放在`resources/views/auth/reset.blade.php`.

Here is a sample password reset form to get you started:
下面是一个简单的密码重置表单，让你开始：

    <!-- resources/views/auth/reset.blade.php -->

    <form method="POST" action="/password/reset">
        {!! csrf_field() !!}
        <input type="hidden" name="token" value="{{ $token }}">

        <div>
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <input type="password" name="password">
        </div>

        <div>
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">
                Reset Password
            </button>
        </div>
    </form>

<a name="after-resetting-passwords"></a>
### After Resetting Passwords-重置密码后，

Once you have defined the routes and views to reset your user's passwords, you may simply access the routes in your browser. The `PasswordController` included with the framework already includes the logic to send the password reset link e-mails as well as update passwords in the database.

一旦你已经确定的路线和意见重置用户的密码，你可以简单地访问您的浏览器的路由。该`PasswordController`包含在框架已经包括发送密码重置链接的电子邮件，以及更新密码在数据库中的逻辑。

After the password is reset, the user will automatically be logged into the application and redirected to `/home`. You can customize the post password reset redirect location by defining a `redirectTo` property on the `PasswordController`:

密码被复位后，用户将自动登录到应用程序和重定向到`/home`。您可以通过定义一个定制后的密码重置重定向位置`redirectTo`的保护`PasswordController`：

    protected $redirectTo = '/dashboard';

> **Note:** By default, password reset tokens expire after one hour. You may change this via the `reminder.expire` option in your `config/auth.php` file.

> **注意:** 默认情况下，密码重置令牌一小时后到期。你可以通过改变这个`reminder.expire`在您选择的`config/auth.php`文件。

<a name="social-authentication"></a>
## Social Authentication-社会认证

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication with Facebook, Twitter, Google, GitHub and Bitbucket.

除了 ​​典型的，基于表单的认证，Laravel还提供了一个简单，方便的方式与使用OAuth提供者进行身份验证[Laravel Socialite](https://github.com/laravel/socialite)。Socialite目前支持的认证与Facebook，Twitter，谷歌，GitHub,Bitbucket。

To get started with Socialite, add to your `composer.json` file as a dependency:

要开始使用Laravel Socialite，添加到您的`composer.json`文件作为一个依赖：

    composer require laravel/socialite

### Configuration-组态

After installing the Socialite library, register the `Laravel\Socialite\SocialiteServiceProvider` in your `config/app.php` configuration file:

安装Socialite library后，注册`Laravel\Socialite\SocialiteServiceProvider`在你的`config/app.php`配置文件：

    'providers' => [
        // Other service providers... 其他服务供应商...

        'Laravel\Socialite\SocialiteServiceProvider',
    ],

Also, add the `Socialite` facade to the `aliases` array in your `app` configuration file:
此外，添加`Socialite` facade 的`aliases` 在阵列的应用程序配置文件：

    'Socialite' => 'Laravel\Socialite\Facades\Socialite',

You will also need to add credentials for the OAuth services your application utilizes. These credentials should be placed in your `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `google`, or `github`, depending on the providers your application requires. For example:

您还需要添加凭据您的应用程序使用OAuth的服务。这些凭据应放置在你的`config/services.php`配置文件，并应使用钥匙的Facebook，Twitter，谷歌，或github上，根据供应商的应用需要。例如：

    'github' => [
        'client_id' => 'your-github-app-id',
        'client_secret' => 'your-github-app-secret',
        'redirect' => 'http://your-callback-url',
    ],

### Basic Usage-基本用法

Next, you are ready to authenticate users! You will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. We will access Socialite using the `Socialite` [facade](/docs/{{version}}/facades):

接下来，您就可以验证用户！您需要两个路由：对于认证后，从提供商接收回调一个用于将用户重定向到OAuth的提供商，和另一个。我们将利用访问 `Socialite` [facade](/docs/{{version}}/facades)：

    <?php namespace App\Http\Controllers;

    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Redirect the user to the GitHub authentication page.将用户重定向到GitHub的认证页面。
         *
         * @return Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * Obtain the user information from GitHub.从GitHub上的用户信息。
         *
         * @return Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

The `redirect` method takes care of sending the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider. Before redirecting the user, you may also set "scopes" on the request using the `scope` method. This method will overwrite all existing scopes:

该`redirect`方法负责发送用户到OAuth的提供商，而 `user`方法将读取传入的请求并检索来自提供者的用户的信息。在将用户重定向，您还可以设置“作用域”关于使用请求 `scope` 方法。此方法将覆盖所有现有的范围：

    return Socialite::driver('github')
                ->scopes(['scope1', 'scope2'])->redirect();

#### Retrieving User Details-检索用户详细信息

Once you have a user instance, you can grab a few more details about the user:
一旦你有一个用户实例，你可以抓住有关用户更多的一些细节：

    $user = Socialite::driver('github')->user();

    // OAuth Two Providers OAuth的两家供应商
    $token = $user->token;

    // OAuth One Providers  OAuth的供应商之一
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All Providers 所有供应商
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

<a name="adding-custom-authentication-drivers"></a>
## Adding Custom Authentication Drivers-添加自定义的驱动程序认证

If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication driver. We will use the `extend` method on the `Auth` facade to define a custom driver. You should place this call to `extend` within a [service provider](/docs/{{version}}/providers):

如果您使用的不是传统的关系数据库来存储你的用户，你将需要延长Laravel与自己的认证的驱动程序。我们将使用`extend`方法 `Auth` facade 来定义一个定制的驱动程序。你应该把这个调用转给`extend`一个范围内的服务提供商：

    <?php namespace App\Providers;

    use Auth;
    use App\Extensions\RiakUserProvider;
    use Illuminate\Support\ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.执行服务注册后启动。
         *
         * @return void
         */
        public function boot()
        {
            Auth::extend('riak', function($app) {
                // Return an instance of Illuminate\Contracts\Auth\UserProvider...
                return new RiakUserProvider($app['riak.connection']);
            });
        }

        /**
         * Register bindings in the container.注册在容器中的绑定。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

After you have registered the driver with the `extend` method, you may switch to the new driver in your `config/auth.php` configuration file.

当你注册了驱动`extend` 方法，您可以切换到您的新的驱动程序的`config/auth.php`配置文件。

### The User Provider Contract-用户提供合同

The `Illuminate\Contracts\Auth\UserProvider` implementations are only responsible for fetching a `Illuminate\Contracts\Auth\Authenticatable` implementation out of a persistent storage system, such as MySQL, Riak, etc. These two interfaces allow the Laravel authentication mechanisms to continue functioning regardless of how the user data is stored or what type of class is used to represent it.

该 `Illuminate\Contracts\Auth\UserProvider`实现只负责取一个`Illuminate\Contracts\Auth\Authenticatable`实现了持久存储系统，比如MySQL，Riak，等这两个接口允许Laravel认证机制继续发挥作用，无论如何将用户数据 ​​存储或什么类型的类是用来表示它。

Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract:
让我们来看看`Illuminate\Contracts\Auth\UserProvider` 合同：

    <?php namespace Illuminate\Contracts\Auth;

    interface UserProvider {

        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);

    }

The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method.

该`retrieveById`函数通常接收表示用户的一个关键诸如从MySQL数据库自动递增编号。所述`可验证`执行匹配的ID应被检索以及由该方法返回。

The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, stored in a field `remember_token`. As with the previous method, the `Authenticatable` implementation should be returned.

该`retrieveByToken`函数检索用户通过他们独特的标识符$和“记住我” `$identifier`，存放在现场`remember_token`。与前面的方法中，可验证执行应被返回。

The `updateRememberToken` method updates the `$user` field `remember_token` with the new `$token`. The new token can be either a fresh token, assigned on successful "remember me" login attempt, or a null when user is logged out.

该`updateRememberToken`方法更新`$user` 领域`remember_token`新 `$token`。新的令牌可以是一个新的令牌，分配上成功的“记住我”的登录尝试，或者当用户退出空。

The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to sign into an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition on `$credentials['username']`. The method should then return an implementation of `UserInterface`. **This method should not attempt to do any password validation or authentication.**

该`retrieveByCredentials`方法接收传递给凭据阵列`Auth::attempt` 尝试登录到应用程序时的方法。那么该方法应该“查询”底层持久存储匹配那些凭据。通常情况下，这种方法将运行与上一个“，其中”条件的查询`$credentials['username']`。该方法应该然后返回的实现的`UserInterface`。**这种方法不应该试图做任何密码验证或认证**。

The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method might compare the `$user->getAuthPassword()` string to a `Hash::make` of `$credentials['password']`. This method should only validate the user's credentials and return boolean.

该`validateCredentials`方法应该比较给定`$user`的`$credentials`，以验证用户。例如，这种方法可能比较`$user->getAuthPassword()`字符串到`Hash::make`的`$credentials['password']` 。此方法应该只验证用户的凭据，并返回boolean值。

### The Authenticatable Contract-所述可验证合同

Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable`. Remember, the provider should return implementations of this interface from the `retrieveById` and `retrieveByCredentials` methods:

现在，我们已经探索每个上的方法`UserProvider`，让我们一起来看看`可验证`。请记住，提供者应返回从这个接口的实现`retrieveById`和`retrieveByCredentials`方法：

    <?php namespace Illuminate\Contracts\Auth;

    interface Authenticatable {

        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();

    }

This interface is simple. The `getAuthIdentifier` method should return the "primary key" of the user. In a MySQL back-end, again, this would be the auto-incrementing primary key. The `getAuthPassword` should return the user's hashed password. This interface allows the authentication system to work with any User class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes a `User` class in the `app` directory which implements this interface, so you may consult this class for an implementation example.

此接口是简单的。该`getAuthIdentifier`方法应返回用户的“主密钥”。在MySQL后端，再次，这将是自动递增主键。该`getAuthPassword`应返回用户的哈希密码。该接口允许认证系统与任何用户类的工作，无论什么ORM或存储抽象层您正在使用的。默认情况下，Laravel包括`User` 在类的`app`实现此接口，所以您可以咨询这个类实现示例目录。
