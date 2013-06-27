# 控制器

- [基础控制器](#basic-controllers)
- [控制器过滤器](#controller-filters)
- [RESTful 控制器](#restful-controllers)
- [资源控制器](#resource-controllers)
- [处理空方法](#handling-missing-methods)

<a name="basic-controllers"></a>
## 基础控制器 （Basic Controllers）

与其把所有路由逻辑写在一个 `routes.php` 文件中，你也许更希望用控制器类来组织它们。控制器可以把相关的路由逻辑组织在一个类中，而且可以使用由框架提供的更为强大的功能，比如自动[依赖注入](/docs/ioc)。

控制器一般储存在 `app/controllers` 目录下，这个目录默认已经被注册在 `app/controllers` 文件的 `classmap` 属性中。

这是一个基础控制器的例子：

	class UserController extends BaseController {

		/**
		 * Show the profile for the given user.
		 */
		public function showProfile($id)
		{
			$user = User::find($id);

			return View::make('user.profile', array('user' => $user));
		}

	}

所有控制器需要继承 `BaseController` 类。 `BaseController` 类也储存在 `app/controllers` 下，通常用来放置公用的控制器逻辑。 `BaseController` 类继承自框架的 `Controller` 类。现在，你可以在路由中像这样调用控制器操作：

	Route::get('user/{id}', 'UserController@showProfile');

如果你需要使用PHP命名空间嵌套组织控制器，你可以在定义路由时使用类名的全称：

	Route::get('foo', 'Namespace\FooController@method');

你也可以在控制器路由中指定名称：

	Route::get('foo', array('uses' => 'FooController@method',
											'as' => 'name'));

你可以使用 `URL::action` 方法获取一个控制器操作的链接：

	$url = URL::action('FooController@method');

你可以使用 `currentRouteAction` 方法获取当前控制器操作的名称：

	$action = Route::currentRouteAction();

<a name="controller-filters"></a>
## 控制器过滤器 （Controller Filters）

[过滤器](/docs/routing#route-filters)可以在控制器路由中指定，就像这样一个"标准的"路由：

	Route::get('profile', array('before' => 'auth',
				'uses' => 'UserController@showProfile'));

不过，你也可以在控制器内部指定过滤器：

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('auth');

			$this->beforeFilter('csrf', array('on' => 'post'));

			$this->afterFilter('log', array('only' =>
								array('fooAction', 'barAction')));
		}

	}

你也可以使用闭包来指定内联的控制器过滤器：

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter(function()
			{
				//
			});
		}

	}

<a name="restful-controllers"></a>
## RESTful 控制器 （RESTful Controllers）

Laravel框架中，你可以使用简单的REST命名规范，轻松定义单个路由去处理控制器的每个操作。首先，使用 `Route::controller` 方法定义路由：

**定义一个 RESTful 控制器**

	Route::controller('users', 'UserController');

`controller` 方法接受两个参数。第一个是基础URI控制器句柄，第二个是控制器的类名。接下来，就可以在控制器中添加带有相应HTTP动词前缀的方法：

	class UserController extends BaseController {

		public function getIndex()
		{
			//
		}

		public function postProfile()
		{
			//
		}

	}

 `index` 方法会应答带有这个控制器句柄的根URI（例如这个例子里的是 `users` ）。

如果你的控制器操作名称包含多个单词，你可以使用 "破折号" 语法来获得URI。例如，下面 `UserController` 控制器中的这个操作会用来应答 `users/admin-profile` URI：

	public function getAdminProfile() {}

<a name="resource-controllers"></a>
## 资源控制器 （Resource Controllers）

资源控制器让围绕资源构建RESTful模式控制器变得更简单。比如，你可能希望创建一个的控制器，用来管理通过你的应用储存的图片（ "photos" ）。通过Artisan命令行输入 `controller:make` 命令以及路由中的 `Route::resource` 方法快速创建一个控制器。

如果要通过命令行创建控制器，使用如下命令：

	php artisan controller:make PhotoController

现在我们可以为这个控制器注册一个资源模式的路由：

	Route::resource('photo', 'PhotoController');

这一个路由声明创建了多个路由规则，用来处理各种图像（photo）资源的RESTful操作。同样地，刚刚创建的控制器中已经包含了许多对应的方法。每个方法都带有注释说明，告诉你分别是用来处理什么URI和HTTP动词的。

**资源控制器中不同操作的用途**

Verb      | Path                  | Action       | Route Name
----------|-----------------------|--------------|---------------------
GET       | /resource             | index        | resource.index
GET       | /resource/create      | create       | resource.create
POST      | /resource             | store        | resource.store
GET       | /resource/{id}        | show         | resource.show
GET       | /resource/{id}/edit   | edit         | resource.edit
PUT/PATCH | /resource/{id}        | update       | resource.update
DELETE    | /resource/{id}        | destroy      | resource.destroy

有时你也许只需要处理其中一部分资源操作：

	php artisan controller:make PhotoController --only=index,show

	php artisan controller:make PhotoController --except=index

同样，你也许需要在路由中制定那一部分要处理的操作：

	Route::resource('photo', 'PhotoController',
					array('only' => array('index', 'show')));

<a name="handling-missing-methods"></a>
## 处理空方法 （Handling Missing Methods）

当控制器中没有任何方法匹配请求时，就会调用一个全局响应的方法。这个方法命名为 `missingMethod` ，它接收请求的参数数组作为方法的唯一参数。

**定义一个空方法**

	public function missingMethod($parameters)
	{
		//
	}