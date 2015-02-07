# 視圖 (View)

- [基本用法](#basic-usage)
- [視圖組件](#view-composers)

<a name="basic-usage"></a>
## 基本用法

視圖裡面包含了你應用程式所提供的 HTML 程式碼，並且提供一個簡單的方式來區隔控制器和網頁呈現上的邏輯。視圖被儲存在 `resources/views` 資料夾內。

一個簡單的視圖看起來可能像這樣：

	<!-- 視圖被儲存在 resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

這個視圖可以在 `app/Http/routes.php` 內使用以下的程式碼傳遞到使用者的瀏覽器：

	Route::get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

如你所見，`view` 輔助方法的第一個參數是 `greeting`，`view` 輔助方法會用這個參數幫你對應到 `resources/views` 資料夾內的 `greeting.blade.php` 或是 `greeting.php` 視圖檔案；傳遞到 `view` 輔助方法的第二個參數是一個陣列 `['name' => 'James']`，代表你希望視圖檔案使用這個資料來改變呈現的內容。

當然，視圖檔案也可以被存放在 `resources/views` 的子資料夾內。舉例來說，如果你的視圖檔案儲存在 `resources/views/admin/profile.php`，你可以用以下的程式碼來回傳：

	// 譯註：使用小數點取代路徑中的斜線，並且省略 .php 或是 .blade.php 的副檔名
	return view('admin.profile', $data);

#### 傳遞資料到視圖

要傳遞資料到視圖內使用，有很多種方式：

	// 使用 with 方法
	$view = view('greeting')->with('name', 'Victoria');

	// 使用魔術方法
	$view = view('greeting')->withName('Victoria');

> **譯註:** 使用魔術方法時，變數名稱會被使用 `snake_case()` 替換，請參考 [字串輔助方法](/docs/5.0/helpers#strings)。

在上面的範例程式碼中，視圖將可以使用 `$name` 來取得資料，其值為 `Victoria`。

如果你想的話，還有一種方式就是直接在 `view` 輔助方法的第二個參數直接傳遞一個陣列：

	$view = view('greetings', $data);

> **譯註:** 在上面的範例程式碼中，視圖將可以使用 `$name` 來取得資料 `$data['name']` 的資料。

#### 把資料共享給所有視圖

有時候你可能需要共享一些資料給你的所有視圖，你有很多個選擇：

1. `view` 輔助方法
2. `Illuminate\Contracts\View\Factory` [公約 \(contract\)](/docs/5.0/contracts)
3. 在 [視圖組件 \(view composer\)](#view-composers) 內使用萬用字元

這裡有個 `view` 輔助方法的範例：

	view()->share('data', [1, 2, 3]);

你也可以使用 `view` 的 Facade：

	View::share('data', [1, 2, 3]);

通常你應該在服務提供者的 `boot()` 內使用以上的兩種範例。 你可以選擇加在 `AppServiceProvider` 或者是新建一個新的服務提供者來容納這些程式碼。

> **備註:** 當 `view` 輔助方法沒有給予任何參數呼叫時，它將會回傳一個的 `Illuminate\Contracts\View\Factory` 公約 (contract) 的實作 (implementation)。

> **譯註:** 當 `view` 輔助方法沒有給予任何參數呼叫時，`view()->` 會等同於 `View::`

#### 確認視圖是否存在

如果你需要確認視圖是否存在，使用 `exists` 方法：

	if (view()->exists('emails.customer'))
	{
		//
	}

#### 從一個檔案路徑產生視圖

如果你想要的話，你可以從一個完整的檔案路徑來產生一個視圖：

	return view()->file($pathToFile, $data);

<a name="view-composers"></a>
## 視圖組件

視圖組件有兩種形式：**閉包** 及 **類別**。視圖被渲染前，會自動呼叫你所指定的回呼函數或類別的 `compose` 方法。如果你想在每次渲染某些視圖時綁定資料，視圖組件可以把這樣的程式邏輯組織在同一個地方。

#### 定義一個視圖組件

一起在 [服務提供者](/docs/5.0/providers) 內組織視圖組件吧！ 你可以使用閉包或是類別的方式來指定。 底下範例將使用 `View` Facade 來取得底層 `Illuminate\Contracts\View\Factory` 合約的實作：

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
			// 使用類別來指定視圖組件
			View::composer('profile', 'App\Http\ViewComposers\ProfileComposer');

			// 使用閉包來指定視圖組件
			View::composer('dashboard', function()
			{

			});
		}

	}

> **備註:** Laravel 沒有預設的資料夾來放置類別形式的視圖組件。 你可以自由的把它們放在 Composer 能夠自動載入的位置（定義於 `composer.json` 內）。 舉例來說，你可以放在 `App\Http\Composers` 資料夾內。

如果你是使用類別形式來定義視圖組件的話，現在我們已經註冊了視圖組件類別，並且在每次 `profile` 視圖渲染的時候，`ProfileComposer@compose` 都將會被執行。 接下來我們來看看這個類別要如何定義：

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
			// service container 會自動解析所需的參數
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

在視圖被渲染之前，視圖組件類別的 `compose` 方法就會被呼叫，並且傳入一個 `Illuminate\Contracts\View\View` 實例。 你可以使用 `with` 方法來把資料綁訂到 `view`。

> **備註:** 所有的視圖組件類別會自動被 [服務容器 \(service container\)](/docs/5.0/container) 解析，所以你在視圖組件類別 `__construct()` 的參數前面只需要加上型別提示 (type-hint)，即可自動解析所有需要的相依參數。

#### 在視圖組件內使用萬用字元

`View` 所提供的 `composer` 方法可以接受 `*` 作為萬用字元，所以你可以對所有視圖附加 `composer` 如下：

	View::composer('*', function()
	{
		//
	});

#### 同時對多個視圖附加視圖組件

你也可以同時針對多個視圖附加同一個視圖組件：

	View::composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### 定義多個視圖組件

你可以使用 `composers` 方法來同時對多個視圖定義視圖組件類別：

	View::composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

### 視圖創建者

視圖 **創建者** 幾乎和視圖組件運作方式一樣；只是視圖創建者會在視圖初始化後就立刻執行。 要註冊一個創建者，只要使用 `creator` 方法：

	View::creator('profile', 'App\Http\ViewCreators\ProfileCreator');

> **譯註:** 視圖組件與視圖創建者的呼叫順序：<br>
> 1. 視圖初始化<br>
> 2. 呼叫 `creators`<br>
> 3. 視圖被 `view` 輔助方法回傳給 `Controller` 或 `Route`<br>
> 4. 視圖被 `Controller` 或 `Route` 回傳<br>
> 5. 呼叫 `composers`<br>
> 6. 渲染視圖
