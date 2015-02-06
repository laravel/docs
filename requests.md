# HTTP 請求

- [取得請求實例](#obtaining-a-request-instance)
- [取得輸入資料](#retrieving-input)
- [舊輸入資料](#old-input)
- [Cookies](#cookies)
- [上傳檔案](#files)
- [其他的請求資訊](#other-request-information)

<a name="obtaining-a-request-instance"></a>
## 取得請求實例

### 透過 Facade

`Request` facade 允許你存取當前綁定容器的請求。例如：

	$name = Request::input('name');

切記，如果你在一個命名空間中，你必須導入 `Request` facade，接著在類別的上方宣告 `use Request;`。

### 透過依賴注入

要透過依賴注入的方式取得 HTTP 請求的實例，你必須在控制器中的建構函式或方法對該類別使用型別提示。當前請求的實例將會自動由[服務容器](/docs/5.0/master/container)注入：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
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

如果你的控制器也有從路由參數傳入的輸入資料，只需要將路由參數置於其他依賴之後：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
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

<a name="retrieving-input"></a>
## 取得輸入資料

#### 取得特定輸入資料

你可以透過 `Illuminate\Http\Request` 的實例，經由幾個簡潔的方法取得所有的使用者輸入資料。不需要擔心發出請求時使用的 HTTP 動詞，取得輸入資料的方式都是相同的。

	$name = Request::input('name');

#### 取得特定輸入資料，若沒有則取得預設值

	$name = Request::input('name', 'Sally');

#### 確認是否有輸入資料

	if (Request::has('name'))
	{
		//
	}

#### 取得所有發出請求時傳入的輸入資料

	$input = Request::all();

#### 取得部分發出請求時傳入的輸入資料

	$input = Request::only('username', 'password');

	$input = Request::except('credit_card');

如果是「陣列」形式的輸入資料，可以使用「點」語法取得陣列：

	$input = Request::input('products.0.name');

<a name="old-input"></a>
## 舊輸入資料

Laravel 可以讓你保留這次的輸入資料，直到下一次請求發送前。例如，你可能需要在表單驗證失敗後重新填入表單值。

#### 將輸入資料存成一次性 Session

`flash` 方法會將當前的輸入資料存進 [session](/docs/5.0/session)中，所以下次使用者發出請求時可以使用儲存的資料：

	Request::flash();

#### 將部分輸入資料存成一次性 Session

	Request::flashOnly('username', 'email');

	Request::flashExcept('password');

#### 快閃及重導

你很可能常常需要在重導至前一頁，並將輸入資料存成一次性 Session。只要在重導方法串接的方法中傳入輸入資料，就能簡單地完成。

	return redirect('form')->withInput();

	return redirect('form')->withInput(Request::except('password'));

#### 取得舊輸入資料

若想要取得前一次請求所儲存的一次性 Session，你可以使用 `Request` 實例中的 `old` 方法。

	$username = Request::old('username');

如果你想在 Blade 模板顯示舊輸入資料，可以使用更加方便的輔助方法 `old` ：

	{{ old('username') }}

<a name="cookies"></a>
## Cookies

Laravel 所建立的 cookie 會加密並且加上認證記號，這代表著被使用者擅自更改的 cookie 會失效。

#### 取得 Cookie 值

	$value = Request::cookie('name');

#### 加上新的 Cookie 到回應

輔助方法 `cookie` 提供一個簡易的工廠方法來產生新的 `Symfony\Component\HttpFoundation\Cookie` 實例。可以在 `Response` 實例之後連接 `withCookie` 方法帶入 cookie 至回應：

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

#### 建立永久有效的 Cookie*

_雖然說是「永遠」，但真正的意思是五年。_

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="files"></a>
## 上傳檔案

#### 取得上傳檔案

	$file = Request::file('photo');

#### 確認檔案是否有上傳

	if (Request::hasFile('photo'))
	{
		//
	}

`file` 方法回傳的物件是 `Symfony\Component\HttpFoundation\File\UploadedFile` 的實例，`UploadedFile` 繼承了 PHP 的 `SplFileInfo` 類別並且提供了很多和檔案互動的方法。

#### 確認上傳的檔案是否有效

	if (Request::file('photo')->isValid())
	{
		//
	}

#### 移動上傳的檔案

	Request::file('photo')->move($destinationPath);

	Request::file('photo')->move($destinationPath, $fileName);

### 其他上傳檔案的方法

`UploadedFile` 的實例還有許多可用的方法，可以至[該物件的 API 文件](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/File/UploadedFile.html)瞭解有關這些方法的詳細資訊。

<a name="other-request-information"></a>
## 其他的請求資訊

`Request` 類別提供很多方法檢查 HTTP 請求，它繼承了 `Symfony\Component\HttpFoundation\Request` 類別，下面是一些使用方式。

#### 取得請求 URI

	$uri = Request::path();

#### 取得請求方法

	$method = Request::method();

	if (Request::isMethod('post'))
	{
		//
	}

#### 確認請求路徑是否符合特定格式

	if (Request::is('admin/*'))
	{
		//
	}

#### 取得請求 URL

	$url = Request::url();
