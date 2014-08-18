# 視圖（ View ）與回應（ Response ）

- [基本回應](#basic-responses)
- [重導](#redirects)
- [視圖](#views)
- [視圖組件](#view-composers)
- [特殊回應](#special-responses)
- [回應巨集](#response-macros)

<a name="basic-responses"></a>
## 基本回應

#### 從路由回傳字串

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### 建立自定回應

`Response` 實例繼承了 `Symfony\Component\HttpFoundation\Response` 類別，其提供了很多方法建立 HTTP 回應。

	$response = Response::make($contents, $statusCode);

	$response->header('Content-Type', $value);

	return $response;

如果想要使用 `Response` 類別的方法，但最終回傳視圖給使用者，你可以使用簡便的 `Response::view` 方法：

	return Response::view('hello')->header('Content-Type', $type);

#### 附加 Cookies 到回應

	$cookie = Cookie::make('name', 'value');

	return Response::make($content)->withCookie($cookie);

<a name="redirects"></a>
## 重導

#### 回傳重導

	return Redirect::to('user/login');

#### 回傳重導並且加上快閃資料（ Flash Data ）

	return Redirect::to('user/login')->with('message', 'Login Failed');

> **提示：** `with` 方法會設定快閃資料到 session，所以可以使用 `Session::get` 取得資料。

#### 回傳根據路由名稱的重導

	return Redirect::route('login');

#### 回傳根據路由名稱的重導，並給予路由參數賦值

	return Redirect::route('profile', array(1));

#### 回傳根據路由名稱的重導，並給予特定名稱路由參數賦值

	return Redirect::route('profile', array('user' => 1));

#### 回傳根據控制器動作的重導

	return Redirect::action('HomeController@index');

#### 回傳根據控制器動作的重導，並給予參數賦值

	return Redirect::action('UserController@profile', array(1));

#### 回傳根據控制器動作的重導，並給予特定名稱參數賦值

	return Redirect::action('UserController@profile', array('user' => 1));

<a name="views"></a>
## Views

視圖通常包含 HTML，並且提供便利的方式分開控制器和表現層的領域邏輯。視圖儲存在 `app/views` 目錄下。

一個簡單的視圖可能看起來如下：

	<!-- View stored in app/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

視圖可以像這樣回傳到使用者瀏覽器：

	Route::get('/', function()
	{
		return View::make('greeting', array('name' => 'Taylor'));
	});

`View::make` 方法傳入的第二個參數是可以在視圖裡使用的陣列資料。

#### 傳遞資料到視圖

	// 使用通用方式
	$view = View::make('greeting')->with('name', 'Steve');

	// 使用魔術方法
	$view = View::make('greeting')->withName('steve');

上面的範例裡，將可以在視圖裡使用變數 `$name` ，其值為 `Steve` 。

如果你想，可以傳入資料陣列作為 `make` 方法第二個參數：

	$view = View::make('greetings', $data);

你也可以設定所有視圖共用資料：

	View::share('name', 'Steve');

#### 傳遞子視圖到視圖

有時候你可能想要傳遞子視圖到另一個視圖。例如，有一個子視圖存在 `app/views/child/view.php`，可以像這樣將它傳遞到另一個視圖：

	$view = View::make('greeting')->nest('child', 'child.view');

	$view = View::make('greeting')->nest('child', 'child.view', $data);

如此可以在視圖裡渲染子視圖：

	<html>
		<body>
			<h1>Hello!</h1>
			<?php echo $child; ?>
		</body>
	</html>

#### 確認視圖是否存在

如果你需要確認視圖是否存在，使用 `View::exists` 方法：

	if (View::exists('emails.customer'))
	{
		//
	}

<a name="view-composers"></a>
## 視圖組件

視圖組件是當渲染視圖時呼叫的回呼函數或類別方法。如果你想在每次渲染某些視圖時綁定資料，視圖組件可以把這樣的邏輯組織在同一個地方。因此，視圖組件的作用可能像是 "view models" 或是 "presenters"。

#### 定義一個組件

	View::composer('profile', function($view)
	{
		$view->with('count', User::count());
	});

之後每當 `profile` 視圖被渲染時， `count` 變數就會被綁定到視圖。

你也可以把一個組件同時附加到很多視圖。

	View::composer(array('profile','dashboard'), function($view)
	{
		$view->with('count', User::count());
	});

如使用類別作為組件，提供了可以從 [IoC 容器](/docs/ioc)自動解析組件的好處，你可以像這樣做：

	View::composer('profile', 'ProfileComposer');

一個視圖組件類別應該像這樣定義：

	class ProfileComposer {

		public function compose($view)
		{
			$view->with('count', User::count());
		}

	}

#### 定義很多組件

你可以使用 `composers` 方法群組視圖組件：

	View::composers(array(
		'AdminComposer' => array('admin.index', 'admin.profile'),
		'UserComposer' => 'user',
	));

> **提示：** 組件類別沒有一定要放在什麼地方，你可以將它們放在任何地方，只要可以使用 `composer.json` 自動載入即可。

### 視圖創建者

視圖 **創建者** 幾乎和組件運作方式一樣；只是他們會在視圖初始化時就立刻建立起來。要註冊一個創建者，只要使用 `creator` 方法：

	View::creator('profile', function($view)
	{
		$view->with('count', User::count());
	});

<a name="special-responses"></a>
## 特殊回應

#### 建立 JSON 回應

	return Response::json(array('name' => 'Steve', 'state' => 'CA'));

#### 建立 JSONP 回應

	return Response::json(array('name' => 'Steve', 'state' => 'CA'))->setCallback(Input::get('callback'));

#### 建立下載檔案回應

	return Response::download($pathToFile);

	return Response::download($pathToFile, $name, $headers);

> **提醒：** 管理檔案下載的套件，Symfony HttpFoundation，要求下載檔名必須為 ASCII 。

<a name="response-macros"></a>
## 回應巨集

如果你想要自定可以在很多路由和控制器重複使用的回應，可以使用 `Response::macro` 方法：

	Response::macro('caps', function($value)
	{
		return Response::make(strtoupper($value));
	});

`macro` 方法第一個參數為巨集名稱，第二個參數為閉合函數。閉合函數會在 `Response` 呼叫巨集名稱的時候被執行：

	return Response::caps('foo');

你可以把定義自己的巨集放在 `app/start` 裡面的文件。又或者，你可以將巨集組織成獨立的文件，並且從其中一個 `start` 文件裡引入。