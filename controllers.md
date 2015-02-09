# HTTP 控制器

- [簡介](#introduction)
- [基礎控制器](#basic-controllers)
- [控制器中介層](#controller-middleware)
- [內隱控制器](#implicit-controllers)
- [RESTful 資源控制器](#restful-resource-controllers)
- [相依注入和控制器](#dependency-injection-and-controllers)
- [路由快取](#route-caching)

<a name="introduction"></a>
## 簡介

除了在單一的 `routes.php` 檔案中定義所有的請求處理邏輯之外，你可能希望使用控制器類別來組織此行為。控制器可將相關的 HTTP 請求處理邏輯組成一個類別。控制器通常存放在 `app/Http/Controllers` 此目錄中。

<a name="basic-controllers"></a>
## 基礎控制器

這裡是一個基礎控制器類別的例子：

	<?php namespace App\Http\Controllers;

	use App\Http\Controllers\Controller;

	class UserController extends Controller {

		/**
		 * 顯示所給定的使用者個人資料。
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			return view('user.profile', ['user' => User::findOrFail($id)]);
		}

	}

我們可以路由前往控制器動作，就像這樣：

	Route::get('user/{id}', 'UserController@showProfile');

> **注意：** 所有的控制器都應該擴展基礎控制器類別。

#### 控制器和命名空間

有一點非常重要，那就是我們毋需指明完整的控制器命名空間，在類別名稱中 `App\Http\Controllers` 之後的部分即可用於表示「根」命名空間。 `RouteServiceProvider` 預設會在包含根控制器命名空間的路由群組中，載入 `routes.php` 此一檔案。

若你要在 `App\Http\Controllers` 此目錄深層使用 PHP 命名空間以巢狀化或組織你的控制器，只要使用相對於 `App\Http\Controllers` 根命名空間的特定類別名稱即可。因此，若你的控制器類別全名為 `App\Http\Controllers\Photos\AdminController`，你可以像這樣註冊一個路由：

	Route::get('foo', 'Photos\AdminController@method');

#### 命名控制器路由

和封閉路由一樣，你也可以指定控制器路由的名稱。

	Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

#### 指向控制器行為的 URL

要產生一個指向控制器行為的 URL，可使用 `action` 輔助方法。

	$url = action('App\Http\Controllers\FooController@method');

若你想僅使用相對於控制器命名空間的類別名稱中的一部分，來產生指向控制器行為的 URL，可用 URL 產生器註冊控制器的根命名空間。

	URL::setRootControllerNamespace('App\Http\Controllers');

	$url = action('FooController@method');

你可以使用 `currentRouteAction` 方法來存取正在執行的控制器行為名稱：

	$action = Route::currentRouteAction();

<a name="controller-middleware"></a>
## 控制器中介層

[中介層](/docs/5.0/middleware) 可在控制器路由中指定，例如：

	Route::get('profile', [
		'middleware' => 'auth',
		'uses' => 'UserController@showProfile'
	]);

此外，你也可以在控制器建構式中指定中介層 ：

	class UserController extends Controller {

		/**
		 * 建立一個新的 UserController 實例。
		 */
		public function __construct()
		{
			$this->middleware('auth');

			$this->middleware('log', ['only' => ['fooAction', 'barAction']]);

			$this->middleware('subscribed', ['except' => ['fooAction', 'barAction']]);
		}

	}

<a name="implicit-controllers"></a>
## 內隱控制器

Laravel 讓你能輕易地定義單一路由來處理控制器中的每一項行為。首先，用 `Route::controller` 方法定義一個路由：

	Route::controller('users', 'UserController');

`Controller` 方法接受兩個參數。第一個參數是控制器欲處理的 base URI，第二個是控制器的類別名稱。接著只要在你的控制器中加入方法，並在名稱前冠上它們所回應的 HTTP 動詞。

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

`index` 方法會回應控制器處理的根 URI ，在這個例子中是 `users` 。

如果你的控制器行為包含多個字詞，你可以在 URI 中使用「破折號」語法來存取此行為。例如，下面這個在 `UserController` 中的控制器動作會回應 `users/admin-profile` 此一 URI ：

	public function getAdminProfile() {}

<a name="restful-resource-controllers"></a>
## RESTful 資源控制器

資源控制器可讓你無痛建立和資源相關的 RESTful 控制器。例如，你可能希望創建一個控制器，它可用來處理針對你的應用程式所儲存相片的 HTTP 請求。我們可以使用 `make:controller` Artisan 指令，快速創建這樣的控制器：

	php artisan make:controller PhotoController

接著，我們註冊一個指向此控制器的資源路由：

	Route::resource('photo', 'PhotoController');

此單一路由宣告創建了多個路由，用來處理各式各樣和相片資源相關的 RESTful 行為。同樣地，產生的控制器已有各種和這些行為繫結的方法，包含用來通知你它們處理了那些 URI 及動詞。

#### 由資源控制器處理的行為

動詞      | 路徑                        | 行為         | 路由名稱
----------|-----------------------------|--------------|---------------------
GET       | /resource                   | 索引         | resource.index
GET       | /resource/create            | 創建         | resource.create
POST      | /resource                   | 儲存         | resource.store
GET       | /resource/{resource}        | 顯示         | resource.show
GET       | /resource/{resource}/edit   | 編輯         | resource.edit
PUT/PATCH | /resource/{resource}        | 更新         | resource.update
DELETE    | /resource/{resource}        | 消減         | resource.destroy

#### 自定資源路由

除此之外，你也可以指定讓路由僅處理一部分的行為：

	Route::resource('photo', 'PhotoController',
					['only' => ['index', 'show']]);

	Route::resource('photo', 'PhotoController',
					['except' => ['create', 'store', 'update', 'destroy']]);

所有的資源控制器行為預設都有個路由名稱。然而你可在選項中傳遞一個 `names` 陣列來重載這些名稱：

	Route::resource('photo', 'PhotoController',
					['names' => ['create' => 'photo.build']]);

#### 處理巢狀資源控制器

在你的路由宣告中使用「點」號來「巢狀化」資源控制器：

	Route::resource('photos.comments', 'PhotoCommentController');

此路由會註冊一個「巢狀的」資源，可透過像 `photos/{photos}/comments/{comments}` 這樣的 URL 來存取。

	class PhotoCommentController extends Controller {

		/**
		 * 顯示指定照片的評論。
		 *
		 * @param  int  $photoId
		 * @param  int  $commentId
		 * @return Response
		 */
		public function show($photoId, $commentId)
		{
			//
		}

	}

#### 在資源控制器中加入其他的路由

除了預設的資源路由外，若你還需要在資源控制器中加入其他路由，應該在呼叫 `Route::resource` 之前先定義它們：

	Route::get('photos/popular');

	Route::resource('photos', 'PhotoController');

<a name="dependency-injection-and-controllers"></a>
## 相依注入和控制器

#### 建構式注入

Laravel [服務容器](/docs/5.0/container) 用於解析所有的 Laravel 控制器。因此，你可以在控制器所需要的建構式中，對相依作任何的型別限制。

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\UserRepository;

	class UserController extends Controller {

		/**
		 * 使用者儲存庫實例。
		 */
		protected $users;

		/**
		 * 創建新的控制器實例。
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}

	}

當然了，你也可以對任何的 [Laravel contract](/docs/5.0/contracts) 作型別限制。只要容器能解析它，你就可以對它作型別限制。

#### 方法注入

除了建構器注入外，你也可以對控制器方法的相依作型別限制。例如，讓我們對某個方法的 `Request` 實例作型別限制：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * 儲存一個新的使用者。
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}

	}

如果你的控制器方法預期由路由參數取得輸入，只要在其他的相依之後列出路由參數即可：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * 儲存一個新的使用者。
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}

	}

> **注意：** 方法注入和 [模型繫結](/docs/5.0/routing#route-model-binding) 是完全相容的。容器可智慧地判斷那些參數和模型相關以及那些參數應該被注入。	

<a name="route-caching"></a>
## 路由快取

若控制器路由只由你的應用程式專用，你可利用 Laravel 的路由快取。使用路由快取，將大幅降低註冊應用程式所有路由所需要的時間。某些情況下，路由註冊甚至可以快上 100 倍。要產生路由快取，只要執行 `route:cache` Artisan 指令：

	php artisan route:cache

就是這樣！你的快取路由檔案將會被用來代替 `app/Http/routes.php` 此一檔案。記住，若你增加了任何新的路由，你就 必須產生一個新的路由快取。因此在專案部署時，你可能會希望只要執行 `route:cache` 指令：

要移除路由快取檔案，但不希望產生新的快取，可使用 `route:clear` 指令：

	php artisan route:clear
