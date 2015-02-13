# 视图 (View)

- [基本用法](#basic-usage)
- [视图组件](#view-composers)

<a name="basic-usage"></a>
## 基本用法

视图里面包含了你应用程序所提供的 HTML 代码，并且提供一个简单的方式来区隔控制器和网页呈现上的逻辑。视图被保存在 `resources/views` 文件夹内。

一个简单的视图看起来可能像这样：

	<!-- 视图被保存在 resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

这个视图可以使用以下的代码传递到用户的浏览器：

	Route::get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

如你所见，`view` 辅助方法的第一个参数会对应到 `resources/views` 文件夹内视图文件的名称；传递到 `view` 辅助方法的第二个参数是一个能够在视图内取用的数据数组。

当然，视图文件也可以被存放在 `resources/views` 的子文件夹内。举例来说，如果你的视图文件保存在 `resources/views/admin/profile.php`，你可以用以下的代码来回传：

	return view('admin.profile', $data);

#### 传递数据到视图

	// 使用传统的方法
	$view = view('greeting')->with('name', 'Victoria');

	// 使用魔术方法
	$view = view('greeting')->withName('Victoria');

在上面的范例代码中，视图将可以使用 `$name` 来取得数据，其值为 `Victoria`。

如果你想的话，还有一种方式就是直接在 `view` 辅助方法的第二个参数直接传递一个数组：

	$view = view('greetings', $data);

#### 把数据共享给所有视图

有时候你可能需要共享一些数据给你的所有视图，你有很多个选择：`view` 辅助方法；`Illuminate\Contracts\View\Factory` [公约 \(contract\)](/docs/5.0/contracts)；在 [视图组件 \(view composer\)](#view-composers) 内使用万用字符。

这里有个 `view` 辅助方法的范例：

	view()->share('data', [1, 2, 3]);

你也可以使用 `view` 的 Facade：

	View::share('data', [1, 2, 3]);

通常你应该在服务提供者的 `boot` 方法内使用 `share` 方法。你可以选择加在 `AppServiceProvider` 或者是新建一个单独的服务提供者来容纳这些代码。

> **备注：** 当 `view` 辅助方法没有带入任何参数调用时，它将会回传一个的 `Illuminate\Contracts\View\Factory` 公约 (contract) 的实作 (implementation)。

#### 确认视图是否存在

如果你需要确认视图是否存在，使用 `exists` 方法：

	if (view()->exists('emails.customer'))
	{
		//
	}

#### 从一个文件路径产生视图

如果你想要的话，你可以从一个完整的文件路径来产生一个视图：

	return view()->file($pathToFile, $data);

<a name="view-composers"></a>
## 视图组件

视图组件就是在视图被渲染前，会调用的闭包或类别方法。如果你想在每次渲染某些视图时绑定数据，视图组件可以把这样的程序逻辑组织在同一个地方。

#### 定义一个视图组件

让我们在 [服务提供者](/docs/5.0/providers) 内组织我们的视图组件。底下范例将使用 `View` Facade 来取得底层 `Illuminate\Contracts\View\Factory` 合约的实作：

	<?php namespace App\Providers;

	use View;
	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider {

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot()
		{
			// 使用类别来指定视图组件
			View::composer('profile', 'App\Http\ViewComposers\ProfileComposer');

			// 使用闭包来指定视图组件
			View::composer('dashboard', function()
			{

			});
		}

	}

> **备注：** Laravel 没有默认的文件夹来放置类别形式的视图组件。你可以自由的把它们放在你想要的地方。举例来说，你可以放在 `App\Http\Composers` 文件夹内。

现在我们已经注册了视图组件，并且在每次 `profile` 视图渲染的时候，`ProfileComposer@compose` 都将会被执行。接下来我们来看看这个类别要如何定义：

	<?php namespace App\Http\Composers;

	use Illuminate\Contracts\View\View;
	use Illuminate\Users\Repository as UserRepository;

	class ProfileComposer {

		/**
		 * The user repository implementation.
		 *
		 * @var UserRepository
		 */
		protected $users;

		/**
		 * Create a new profile composer.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			// service container 会自动解析所需的参数
			$this->users = $users;
		}

		/**
		 * Bind data to the view.
		 *
		 * @param  View  $view
		 * @return void
		 */
		public function compose(View $view)
		{
			$view->with('count', $this->users->count());
		}

	}

在视图被渲染之前，视图组件的 `compose` 方法就会被调用，并且传入一个 `Illuminate\Contracts\View\View` 实例。你可以使用 `with` 方法来把数据绑订到 `view`。

> **备注：** 所有的视图组件会被 [服务容器 \(service container\)](/docs/5.0/container) 解析，所以你需要在视图组件的建构子型别限制你所需的任何相依参数。

#### 在视图组件内使用万用字符

`View` 的 `composer` 方法可以接受 `*` 作为万用字符，所以你可以对所有视图附加 `composer` 如下：

	View::composer('*', function()
	{
		//
	});

#### 同时对多个视图附加视图组件

你也可以同时针对多个视图附加同一个视图组件：

	View::composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### 定义多个视图组件

你可以使用 `composers` 方法来同时定义一群视图组件：

	View::composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

### 视图创建者

视图 **创建者** 几乎和视图组件运作方式一样；只是视图创建者会在视图初始化后就立刻执行。要注册一个创建者，只要使用 `creator` 方法：

	View::creator('profile', 'App\Http\ViewCreators\ProfileCreator');
