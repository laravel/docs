# Controllers

- [基本 Controller](#basic-controllers)
- [Controller Filter](#controller-filters)
- [RESTful Controller](#restful-controllers)
- [Resource Controller](#resource-controllers)
- [對應遺漏的方法](#handling-missing-methods)

<a name="basic-controllers"></a>
## 基本 Controllers

除了在單一個`routes.php`裡定義所有的邏輯，你可能想要利用 Controller 組織這些邏輯。Controller 可以將相關的邏輯組合到一個類別裡，以及利用更多進階的框架特性如自動的[依賴注入](/docs/ioc)。

Controller 一般存放在`app/controllers`目錄下，而這個目錄註冊在`composer.json`的`classmap`中。然而，技術上 controller 可以放在任何目錄或是子目錄。Route 宣告不需依賴 controller 類別在硬碟中的位置。所以，只要 Composer 知道如何自動載入 controller 類別，你就可以放在任何你想要的地方。

下面是一個基本的 Controlle 類別例子：

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

所有的 controller 都應該繼承`BaseController`類別。`BaseController`也放在`app/controllers`目錄下，`BaseController`可以作為放置共同 controller 邏輯的地方。`BaseController`繼承了框架的`Controller`類別。現在，我們可以像這樣 route 到 controller 的方法：

	Route::get('user/{id}', 'UserController@showProfile');

如果你想要利用巢狀或 PHP namespaces 來組織 controller，只要在定義 route 規則時使用完整的類別名稱：

	Route::get('foo', 'Namespace\FooController@method');

> **注意：**既然我們使用 [Composer](http://getcomposer.org) 自動載入 PHP 類別， controller 可以放在檔案系統的任何地方，只要 Composer 知道如何載入他們。 controller 目錄不強制你應用程式的目錄結構。「如何 route 到 controller 」是完全跟檔案系統去耦合的。

你可以指定 controller route 規則的名稱：

	Route::get('foo', array('uses' => 'FooController@method',
											'as' => 'name'));

為了產生對應 controller 方法的 URL，你可以使用`URL::action`方法或是`action`輔助方法：

	$url = URL::action('FooController@method');

	$url = action('FooController@method');

你可以利用`currentRouteAction`方法取得正在執行的 controller 方法名稱：

	$action = Route::currentRouteAction();

<a name="controller-filters"></a>
## Controller Filters

[Filter](/docs/routing#route-filters) 可以在 controller route 規則宣告中指定，類似于「一般」的宣告

	Route::get('profile', array('before' => 'auth',
				'uses' => 'UserController@showProfile'));

然而，你也可以在 controller 內指定 filter

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

你可以在 controller 裡使用閉合函式定義 filter

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

如果你想使用 controller 裡的方法當作 filter，你可以使用`@`語法定義 filter：

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
## RESTful Controllers

Laravel 讓你可以簡單的經由定義一個 route 規則，就處理 controller 裡的所有遵照 REST 命名規範的方法。首先，使用`Route::controller`方法定義 route 規則：

	Route::controller('users', 'UserController');

`controller`方法可以接收兩個變數，第一個是 controller 對應的基本 URI，第二個是 controller 的類別名稱。接下來，只要把對應的 HTTP 請求動詞前綴加在 controller 方法前：

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

`index`方法會對應到 controller 的根 URI，以上面的例子來說，就是`users`。

若你的 controller 方法包含很多單字，你可以在 URI 使用"dash"語法來對應方法。例如`UserController`中，如下的方法會對應到`users/admin-profile` URI：

	public function getAdminProfile() {}

<a name="resource-controllers"></a>
## Resource Controllers

Resource controller 可以簡單的建立跟 resource 相關的 RESTful controller。例如，你可能想要建立 controller 管理應用程式裡儲存的照片。使用 Artisan 命令列工具裡的`controller:make`以及使用`Route::resource`方法，可以很快的建立 controller。

從命令列執行下列命令建立 controller：

	php artisan controller:make PhotoController

現在我們可以註冊一個 resourceful route 規則到 controller：

	Route::resource('photo', 'PhotoController');

這一行宣告建立了很多 route 規則，對應處理照片 resource 的 RESTful 動作。同樣的，剛才產生的 controller 對這些動作已經有預建的對應方法，以及註解告知對應的 URI 和所處理的請求動作。

#### Resource Controller 對應的動作

Verb      | Path                        | Action       | Route Name
----------|-----------------------------|--------------|---------------------
GET       | /resource                   | index        | resource.index
GET       | /resource/create            | create       | resource.create
POST      | /resource                   | store        | resource.store
GET       | /resource/{resource}        | show         | resource.show
GET       | /resource/{resource}/edit   | edit         | resource.edit
PUT/PATCH | /resource/{resource}        | update       | resource.update
DELETE    | /resource/{resource}        | destroy      | resource.destroy

有時你可能只需要對應部分的 resource 的動作：

	php artisan controller:make PhotoController --only=index,show

	php artisan controller:make PhotoController --except=index

你也可以在 route 宣告時指定需要對應的動作：

	Route::resource('photo', 'PhotoController',
					array('only' => array('index', 'show')));

	Route::resource('photo', 'PhotoController',
					array('except' => array('create', 'store', 'update', 'destroy')));

預設所有的 resource controller 動作都有 route 名稱，然而，你可以在選項傳入`names`陣列，覆寫這些名稱：

	Route::resource('photo', 'PhotoController',
					array('names' => array('create' => 'photo.build')));

#### 處理巢狀 Resource Controller

為了使用巢狀 resource controller，在 route 宣告時使用"點"表示法：

	Route::resource('photos.comments', 'PhotoCommentController');

這個 route 規則會註冊一個巢狀 resource，可以對應如下的 URLs：`photos/{photoResource}/comments/{commentResource}`。

	class PhotoCommentController extends BaseController {

		public function show($photoId, $commentId)
		{
			//
		}

	}

#### 增加額外 route 規則到 Resource Controller

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
