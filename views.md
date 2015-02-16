# 視圖（ View ）

- [基本用法](#basic-usage)
- [視圖組件](#view-composers)

<a name="basic-usage"></a>
## 基本用法

視圖通常包含 HTML，並且提供便利的方式分開控制器和表現層的領域邏輯。視圖被儲存在 `resources/views` 目錄下。

一個簡單的視圖看起來可能像這樣：

	<!-- 視圖被儲存在 resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

視圖可以像這樣回傳到使用者瀏覽器：

	Route::get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

如你所見，`view` 輔助方法的第一個參數會對應到 `resources/views` 資料夾內視圖檔案的名稱；傳遞到 `view` 輔助方法的第二個參數是一個能夠在視圖內取用的資料陣列。

當然，視圖檔案也可以被存放在 `resources/views` 的子資料夾內。舉例來說，如果你的視圖檔案儲存在 `resources/views/admin/profile.php`，你可以用以下的程式碼來回傳：

	return view('admin.profile', $data);

#### 傳遞資料到視圖

	// 使用常用的方法
	$view = view('greeting')->with('name', 'Victoria');

	// 使用魔術方法
	$view = view('greeting')->withName('Victoria');

在上面的範例程式碼中，視圖將可以使用 `$name` 來取得資料，其值為 `Victoria`。

如果你想的話，還有一種方式就是直接在 `view` 輔助方法的第二個參數直接傳遞一個陣列：

	$view = view('greetings', $data);

#### 把資料共享給所有視圖

有時候你可能需要共享一些資料給所有視圖，你有很多個選擇：`view` 輔助方法；`Illuminate\Contracts\View\Factory`  [contract](/docs/5.0/contracts)；或是在[視圖組件](#view-composers)內使用萬用字元。

這裡有個 `view` 輔助方法的範例：

	view()->share('data', [1, 2, 3]);

你也可以使用 `view` 的 Facade：

	View::share('data', [1, 2, 3]);

通常你應該在服務提供者的 `boot` 方法內使用 `share` 方法。你可以選擇加在 `AppServiceProvider` 或者是新建一個單獨的服務提供者來放置這些程式碼。

> **備註：**當 `view` 輔助方法被呼叫，而沒有帶入任何參數時，它會回傳一個 `Illuminate\Contracts\View\Factory`  contract 的實作。

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

視圖組件就是在視圖被渲染前，會呼叫的閉包或類別方法。如果你想在每次渲染某些視圖時綁定資料，視圖組件可以把這樣的程式邏輯組織在同一個地方。

#### 定義一個視圖組件

讓我們在[服務提供者](/docs/5.0/providers)內組織我們的視圖組件。底下範例將使用 `View` Facade 來取得底層 `Illuminate\Contracts\View\Factory` contract 實作：

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

> **備註：**Laravel 沒有預設目錄放置視圖組件。你可以自由的把它們放在你想要的地方。舉例來說，你可以放在 `App\Http\Composers` 目錄下。

現在我們已經註冊了視圖組件，並且在每次 `profile` 視圖渲染的時候，`ProfileComposer@compose` 都將會被執行。接下來我們來看看這個類別要如何定義：

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

在視圖被渲染之前，視圖組件的 `compose` 方法就會被呼叫，並且傳入一個 `Illuminate\Contracts\View\View` 實例。你可以使用 `with` 方法來把資料綁定到 `view`。

> **備註：**所有的視圖組件會被[服務容器](/docs/5.0/container) 解析，所以你可以在視圖組件的建構子，型別提示注入所需的任何依賴。

#### 在視圖組件內使用萬用字元

`View` 的 `composer` 方法可以接受 `*` 作為萬用字元，所以你可以對所有視圖附加 `composer` 如下：

	View::composer('*', function()
	{
		//
	});

#### 同時對多個視圖附加視圖組件

你也可以同時針對多個視圖附加同一個視圖組件：

	View::composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### 定義多個視圖組件

你可以使用 `composers` 方法來同時定義一群視圖組件：

	View::composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

### 視圖創建者

視圖**創建者**幾乎和視圖組件運作方式一樣；只是視圖創建者會在視圖初始化後就立刻執行。要註冊一個創建者，只要使用 `creator` 方法：

	View::creator('profile', 'App\Http\ViewCreators\ProfileCreator');
