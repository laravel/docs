# 請求與輸入

- [基本輸入資料](#basic-input)
- [Cookies](#cookies)
- [舊輸入資料](#old-input)
- [上傳檔案](#files)
- [請求資訊](#request-information)

<a name="basic-input"></a>
## 基本輸入資料

你可以經由幾個簡潔的方法拿到使用者的輸入資料。不需要擔心發出請求時使用的 HTTP 動詞，取得輸入資料的方式都是相同的。

#### 取得特定輸入資料

	$name = Input::get('name');

#### 取得特定輸入資料，若沒有則取得預設值

	$name = Input::get('name', 'Sally');

#### 確認是否有輸入資料

	if (Input::has('name'))
	{
		//
	}

#### 取得所有發出請求時傳入的輸入資料

	$input = Input::all();

#### 取得部分發出請求時傳入的輸入資料

	$input = Input::only('username', 'password');

	$input = Input::except('credit_card');

如果是「陣列」形式的輸入資料，可以使用「點」語法取得陣列：

	$input = Input::get('products.0.name');

> **提醒：** 有些 JavaScript 函式庫如 Backbone 可能會送出 JSON 格式的輸入資料，但是一樣可以使用 `Input::get` 取得資料。

<a name="cookies"></a>
## Cookies

Laravel 建立的 cookie 會加密並且加上認證記號，意味著如果被客戶端擅改，會造成 cookie 失效。

#### 取得 Cookie 值

	$value = Cookie::get('name');

#### 加上新的 Cookie 到回應

	$response = Response::make('Hello World');

	$response->withCookie(Cookie::make('name', 'value', $minutes));

#### 加入 Cookie 隊列到下一個回應

如果你想在回應被建立前設定 cookie ，使用 `Cookie::queue()` 方法。 Cookie 會在最後自動加到回應裡。

	Cookie::queue($name, $value, $minutes);

#### 建立永久有效的 Cookie

	$cookie = Cookie::forever('name', 'value');

<a name="old-input"></a>
## 舊輸入資料

你可能想要在使用者下一次發送請求前，保留這次的輸入資料。例如，你可能需要在表單驗證失敗後重新填入表單值。

#### 將輸入資料存成一次性 Session 

	Input::flash();

#### 將部分輸入資料存成一次性 Session

	Input::flashOnly('username', 'email');

	Input::flashExcept('password');

你很可能常常需要在重導至前一頁，並將輸入資料存成一次性 Session 。只要在重導方法串接的方法中傳入輸入資料，就能簡單地完成。

	return Redirect::to('form')->withInput();

	return Redirect::to('form')->withInput(Input::except('password'));

> **提示：** 你可以使用 [Session](/docs/session) 類別將不同請求資料存成其他一次性 Session。

#### 取得舊輸入資料

	Input::old('username');

<a name="files"></a>
## 上傳檔案

#### 取得上傳檔案

	$file = Input::file('photo');

#### 確認檔案是否有上傳

	if (Input::hasFile('photo'))
	{
		//
	}

`file` 方法回傳的物件是 `Symfony\Component\HttpFoundation\File\UploadedFile` 的實例， `UploadedFile` 繼承了 PHP 的 `SplFileInfo` 類別並且提供了很多方法和檔案互動。

#### 確認上傳的檔案是否有效

	if (Input::file('photo')->isValid())
	{
		//
	}

#### 移動上傳檔案

	Input::file('photo')->move($destinationPath);

	Input::file('photo')->move($destinationPath, $fileName);

#### 取得上傳檔案所在的路徑

	$path = Input::file('photo')->getRealPath();

#### 取得上傳檔案的原始名稱

	$name = Input::file('photo')->getClientOriginalName();

#### 取得上傳檔案的副檔名

	$extension = Input::file('photo')->getClientOriginalExtension();

#### 取得上傳檔案的大小

	$size = Input::file('photo')->getSize();

#### 取得上傳檔案的 MIME 類型

	$mime = Input::file('photo')->getMimeType();

<a name="request-information"></a>
## 請求資訊

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

#### 取得請求 URI 部分片段

	$segment = Request::segment(1);

#### 取得請求標頭

	$value = Request::header('Content-Type');

#### 從 $_SERVER 取得值

	$value = Request::server('PATH_INFO');

#### 確認是否為 HTTPS 請求

	if (Request::secure())
	{
		//
	}

#### 確認是否為 AJAX 請求

	if (Request::ajax())
	{
		//
	}

#### 確認請求是否有 JSON Content Type

	if (Request::isJson())
	{
		//
	}

#### 確認是否要求 JSON 回應

	if (Request::wantsJson())
	{
		//
	}

#### 確認要求的回應格式

`Request::format` 方法會基於 HTTP Accept 標頭回傳請求的回應格式：

	if (Request::format() == 'json')
	{
		//
	}
