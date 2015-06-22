# 視圖

- [基本用法](#basic-usage)
	- [傳遞資料到視圖](#passing-data-to-views)
	- [把資料共享給所有視圖](#sharing-data-with-all-views)
- [視圖組件](#view-composers)

<a name="basic-usage"></a>
## 基本用法

視圖包含你應用程式所用到的 HTML，它能夠從你的呈現邏輯中分開你的控制器和應用程式邏輯。視圖被存在 `resources/views` 目錄下。

一個簡單的視圖看起來可能像這樣：

	<!-- 視圖被儲存在 resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

因為這個視圖被儲存在 `resources/views/greeting.php`，我們可以像這樣使用全域的輔助方法 `view` 來回傳：

	Route::get('/', function ()	{
		return view('greeting', ['name' => 'James']);
	});

如你所見，`view` 輔助方法的第一個參數會對應到 `resources/views` 目錄內視圖檔案的名稱；傳遞到 `view` 輔助方法的第二個參數是一個能夠在視圖內取用的資料陣列。在這個例子中，我們傳遞 `name` 這個變數，然後在視圖裡面會簡單的用 `echo` 來顯示這個變數。

當然，視圖檔案也可以被存放在 `resources/views` 的子目錄內。`.` （小數點）的表示法可以被用來表示在子目錄內的視圖檔案。舉例來說，如果你的視圖檔案儲存在 `resources/views/admin/profile.php`，你可以用以下的程式碼來回傳：

	return view('admin.profile', $data);

#### 判斷視圖檔案是否存在

如果你需要判斷視圖檔案是否存在，你可以使用 `exists` 方法在一個不傳入任何參數的 `view` 輔助方法之後。這個方法將會在視圖檔案存在時回傳 `true`：

	if (view()->exists('emails.customer')) {
		//
	}

當 `view` 輔助方法在不傳入任何參數呼叫時，將會回傳一個 `Illuminate\Contracts\View\Factory` 的實例，以便你取用這個 Factory 的任何方法。

<a name="view-data"></a>
### 視圖的資料

<a name="passing-data-to-views"></a>
#### 傳遞資料到視圖

就像你在之前的範例所見，你可以間單地傳遞一個陣列的資料給視圖：

	return view('greetings', ['name' => 'Victoria']);

當你用上面這種方式傳遞資料時，`$data` 必須是一個鍵值對的陣列。在視圖中，你可以用相對應的鍵名取用值，如：`<?php echo $key; ?>`；你也可以用另一個替代的語法來傳遞一個資料陣列，在 `view` 輔助方法使用 `with` 來額外傳遞資料給視圖：

	$view = view('greeting')->with('name', 'Victoria');

<a name="sharing-data-with-all-views"></a>
#### 把資料共享給所有視圖

有時候你可能需要共享一些資料給所有你應用程式所渲染的視圖，你可以使用視圖 factory 的 `share` 方法來做到這件事。通常，你會把些呼叫 `share` 方法的程式碼放在一個服務提供者的 `boot` 方法內。你可以選擇直接寫在 `AppServiceProvider` 或是自己產生一個不同的服務提供者來安置這些程式碼：

	<?php namespace App\Providers;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * 啟動任何應用程式的服務。
	     *
	     * @return void
	     */
		public function boot()
		{
			view()->share('key', 'value');
		}

		/**
		 * 註冊服務提供者。
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

<a name="view-composers"></a>
## 視圖組件

視圖組件就是在視圖被渲染前，會呼叫的閉包或類別方法。如果你想在每次渲染某些視圖時綁定資料，視圖組件可以把這樣的程式邏輯組織在同一個地方。

讓我們在[服務提供者](/docs/{{version}}/providers)內註冊我們的視圖組件。底下範例將使用 View 輔助方法來取得底層 `Illuminate\Contracts\View\Factory` contract 實作。請注意，Laravel 沒有預設的目錄來放置視圖組件。你可以自由的把它們放在你想要的地方。舉例來說，你可以建立一個 App\Http\ViewComposers 目錄：

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider
	{
		/**
		 * 在容器內註冊所有綁定。
		 *
		 * @return void
		 */
		public function boot()
		{
			// 使用物件型態的視圖組件
			view()->composer(
				'profile', 'App\Http\ViewComposers\ProfileComposer'
			);

			// 使用閉包型態的視圖組件
			view()->composer('dashboard', function ($view) {

			});
		}

		/**
		 * 註冊服務提供者。
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

記住，如果你建立了一個新的服務提供者包含你註冊的視圖組件，你需要把服務提供者加入在 `config/app.php` 設定檔內的 `providers` 陣列。

現在我們已經註冊了視圖組件，並且在每次 `profile` 視圖渲染的時候，`ProfileComposer@compose` 都將會被執行。接下來我們來看看這個視圖組件類別要如何定義：

	<?php namespace App\Http\ViewComposers;

	use Illuminate\Contracts\View\View;
	use Illuminate\Users\Repository as UserRepository;

	class ProfileComposer
	{
		/**
		 * 使用者物件的實例。
		 *
		 * @var UserRepository
		 */
		protected $users;

		/**
		 * 建立一個新的個人資料視圖組件。
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			// 所有依賴都會自動地被服務容器解析...
			$this->users = $users;
		}

		/**
		 * 將資料綁定到視圖。
		 *
		 * @param  View  $view
		 * @return void
		 */
		public function compose(View $view)
		{
			$view->with('count', $this->users->count());
		}
	}

在視圖被渲染之前，視圖組件的 `compose` 方法就會被呼叫，並且傳入一個 `Illuminate\Contracts\View\View` 實例。你可以使用 `with` 方法來把資料綁定到視圖。

> **備註**：所有的[視圖組件](/docs/{{version}}/container)都會被服務容器 解析，所以你可以在視圖組件的建構子，型別提示注入所需的任何依賴。

#### 在視圖組件內使用萬用字元

你可以在 `composer` 方法的第一個參數傳遞一個視圖陣列，來同時針對多個視圖附加同一個視圖組件：

	view()->composer(
		['profile', 'dashboard'],
		'App\Http\ViewComposers\MyViewComposer'
	);

視圖的 `composer` 方法可以接受 `*` 作為萬用字元，所以你可以對所有視圖附加 composer 如下：

	view()->composer('*', function ($view) {
		//
	});

### 視圖創建者

視圖**創建者**幾乎和視圖組件運作方式一樣；只是視圖創建者會在視圖初始化後就立刻執行，而不是像視圖組件會一直等到視圖即將被渲染時才會執行。要註冊一個創建者，只要使用 `creator` 方法：

	view()->creator('profile', 'App\Http\ViewCreators\ProfileCreator');
