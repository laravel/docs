# 控制器 (Controllers)

- [基本控制器](#basic-controllers)
- [控制器過濾器(Controller filters)](#controller-filters)
- [RESTful 控制器](#restful-controllers)
- [資源控制器](#resource-controllers)
- [對應遺漏的方法](#handling-missing-methods)

<a name="basic-controllers"></a>
## 基本 Controllers

除了在單一 `routes.php` 檔中定義所有路由層邏輯外，你可能也想利用控制器類別來整合這些行為模式。控制器可以統合相關的路由邏輯到同一個類別中，並且利用更先進的框架特性的優勢，如自動的[依賴注入](/docs/ioc)。


控制器一般存放在 `app/controllers` 目錄下，這個目錄已預設註冊在 `composer.json` 的 `classmap` 中。然而，技術上控制器可以放在任何目錄或是子目錄。路由宣告與控制器類別存放在哪個位址並無關係。所以，只要 Composer 知道如何自動載入控制器類別，你就可以放在任何你想要的地方。

下面是一個基本的控制器類別例子：

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

所有的控制器都應該繼承自 `BaseController` 類別。`BaseController` 也放在 `app/controllers` 目錄下，`BaseController` 可以作為放置共同控制器邏輯的地方。`BaseController` 繼承了框架的 `Controller` 類別。現在，我們可以像這樣將請求從路由導至控制器行為中：

	Route::get('user/{id}', 'UserController@showProfile');

如果你選擇使用 PHP 命名空間來分層或整合你的控制器，只要在定義路由時使用完整的類別名稱：

	Route::get('foo', 'Namespace\FooController@method');

> **注意：**既然我們使用 [Composer](http://getcomposer.org) 自動載入 PHP 類別，控制器可以放在檔案系統的任何地方，只要 Composer 知道如何載入他們。對你的應用程式而言，控制器目錄並沒有強制使用怎樣目錄結構。路由至控制器是完全與檔案系統脫鉤的。

你可以為控制器路由指定名稱：

	Route::get('foo', array('uses' => 'FooController@method',
											'as' => 'name'));

你可以使用 `URL::action` 方法或者是 `action` 輔助方法來產生到控制器行為的 URL：

	$url = URL::action('FooController@method');

	$url = action('FooController@method');

你可以利用 `currentRouteAction` 方法取得正在執行的控制器行為名稱：

	$action = Route::currentRouteAction();

<a name="controller-filters"></a>
## 控制器過濾器

[過濾器(Filter)](/docs/routing#route-filters) 在控制器路由中宣告方式，如同"一般"的路由一樣。

	Route::get('profile', array('before' => 'auth',
				'uses' => 'UserController@showProfile'));

然而，你也可以在控制器中指定過濾器：

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('auth', array('except' => 'getLogin'));

			$this->beforeFilter('csrf', array('on' => 'post'));

			$this->afterFilter('log', array('only' =>
								array('fooAction', 'barAction')));
		}

	}

你可以在控制器裡使用閉合函式定義過濾器：

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

如果你想使用控制器裡的方法當做過濾器，你可以使用`@`語法定義過濾器：

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('@filterRequests');
		}

		/**
		 * Filter the incoming requests.
		 */
		public function filterRequests($route, $request)
		{
			//
		}

	}

<a name="restful-controllers"></a>
## RESTful 控制器

Laravel 讓你可以簡單的經由定義一個路由規則來處理控制器裡的所有遵照 REST 命名規範的行為。首先，使用 `Route::controller` 方法定義路由：

	Route::controller('users', 'UserController');

`controller` 方法可以接收兩個參數，第一個是控制器對應的基本 URI，第二個是控制器的類別名稱。接下來，只要把對應的 HTTP 請求動詞前綴加在控制器方法前：

	class UserController extends BaseController {

		public function getIndex()
		{
			//
		}

		public function postProfile()
		{
			//
		}
		
		public function anyLogin()
		{
			//
		}

	}

`index` 方法會對應到 controller 的根 URI，以上面的例子來說，就是 `users`。

若你的控制器方法包含很多單字，你可以在 URI 使用 "破折號(-)" 來對應方法。例如 `UserController` 中，如下的方法會對應到 `users/admin-profile` URI：

	public function getAdminProfile() {}

<a name="resource-controllers"></a>
## 資源控制器


資源控制器可以簡單的建立跟資源相關的 RESTful 控制器。例如，你可能想要建立控制器管理應用程式裡儲存的照片。透過 Artisan 命令列工具裡的 `controller:make` 以及使用 `Route::resource` 方法，可以很快的建立 控制器。

從命令列執行下列命令建立控制器：

	php artisan controller:make PhotoController

然後我們可以註冊一個資源化路由至控制器上：

	Route::resource('photo', 'PhotoController');

此單一路由宣告創建了處理一系列對圖片資源的 RESTful 行為路由。同樣的，剛才產生的控制器對這些動作已經有預建的對應方法，以及註解告知對應的 URI 和所處理的請求動作。

#### 資源控制器對應的動作

Verb      | Path                        | Action       | Route Name
----------|-----------------------------|--------------|---------------------
GET       | /resource                   | index        | resource.index
GET       | /resource/create            | create       | resource.create
POST      | /resource                   | store        | resource.store
GET       | /resource/{resource}        | show         | resource.show
GET       | /resource/{resource}/edit   | edit         | resource.edit
PUT/PATCH | /resource/{resource}        | update       | resource.update
DELETE    | /resource/{resource}        | destroy      | resource.destroy

有時你可能只需要對應部分的資源的動作：

	php artisan controller:make PhotoController --only=index,show

	php artisan controller:make PhotoController --except=index

你也可以在路由宣告時指定需要對應的動作：

	Route::resource('photo', 'PhotoController',
					array('only' => array('index', 'show')));

	Route::resource('photo', 'PhotoController',
					array('except' => array('create', 'store', 'update', 'destroy')));

預設所有的資源控制器動作都有路由名稱，然而，你可以在選項傳入 `names` 陣列，覆寫這些名稱：

	Route::resource('photo', 'PhotoController',
					array('names' => array('create' => 'photo.build')));

#### 處理巢狀資源控制器

為了使用巢狀資源控制器，在路由宣告時使用"點"表示法：

	Route::resource('photos.comments', 'PhotoCommentController');

這個路由規則會註冊一個"巢狀"資源，可以對應如下的 URLs：`photos/{photoResource}/comments/{commentResource}`。

	class PhotoCommentController extends BaseController {

		public function show($photoId, $commentId)
		{
			//
		}

	}

#### 增加額外路由規則到 Resource Controller

你果你需要增加額外的 route 規則到預設的 resource controller，你應該在宣告`Route::resource`之前宣告這些規則：

	Route::get('photos/popular');
	Route::resource('photos', 'PhotoController');

<a name="handling-missing-methods"></a>
## 對應遺漏的方法

可以定義一個 catch-all 方法，當 controller 找不到對應的方法就會被呼叫，這個方法應該宣告為`missingMethod`, 會傳入請求的方法和參數陣列：

#### 定義一個 Catch-All 方法

	public function missingMethod($parameters = array())
	{
		//
	}
