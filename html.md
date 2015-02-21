# Forms & HTML

- [開啟表單](#opening-a-form)
- [CSRF 保護](#csrf-protection)
- [表單模型綁定](#form-model-binding)
- [標籤（ Label ）](#labels)
- [文字欄（ Text ）、多行文字欄（ Text Area ）、密碼欄（ Password ）和隱藏欄（ Hidden Field ）](#text)
- [核取方塊（ Checkboxe ）和單選按鈕（ Radio Button ）](#checkboxes-and-radio-buttons)
- [數字欄（ Number ）](#number)
- [檔案輸入](#file-input)
- [下拉式選單](#drop-down-lists)
- [按鈕](#buttons)
- [自定巨集（ Macro ）](#custom-macros)
- [產生 URL](#generating-urls)

<a name="opening-a-form"></a>
## 開啟表單

#### 開啟表單

	{{ Form::open(['url' => 'foo/bar']) }}
		//
	{{ Form::close() }}

預設表單使用 POST 方法，當然你也可以指定其他方法：

	echo Form::open(['url' => 'foo/bar', 'method' => 'put'])

> **注意：**因為 HTML 表單只支援 `POST` 和 `GET` 方法，所以在使用 `PUT` 及 `DELETE` 方法時，Laravel 會自動加入 `_method` 隱藏欄位到表單中，來偽裝表單傳送的方法。

你也可以建立指向命名路由或控制器動作的表單：

	echo Form::open(['route' => 'route.name'])

	echo Form::open(['action' => 'Controller@method'])

也可以傳遞路由參數：

	echo Form::open(['route' => ['route.name', $user->id]])

	echo Form::open(['action' => ['Controller@method', $user->id]])

如果表單允許上傳檔案，在陣列中加上 `files` 選項：

	echo Form::open(['url' => 'foo/bar', 'files' => true])

<a name="csrf-protection"></a>
## CSRF 保護

#### 添加 CSRF Token 到表單

Laravel 提供簡易的方法，讓你可以保護你的應用程式免於跨網站請求偽造（ CSRF ）攻擊。首先 Laravel 會自動在使用者的 session 中存放隨機產生的 token。如果你使用 `Form::open` 方法，並且選擇 `POST`、`PUT` 或是 `DELETE`，CSRF token 會自動加到表單的一個隱藏欄位中。但是，你如果想要替隱藏的 CSRF 欄位產生 HTML，也可以使用 `token` 方法：

	echo Form::token();

#### 附加 CSRF 過濾到路由

	Route::post('profile', ['before' => 'csrf', function()
	{
		//
	}]);

<a name="form-model-binding"></a>
## 表單模型綁定

#### 開啟模型表單

你經常會想要將模型內容加到表單中，可以使用 `Form::model` 方法實現：

	echo Form::model($user, ['route' => ['user.update', $user->id]])

現在當你產生表單元素時，像是 text 欄位，模型屬性和欄位名稱相符的屬性值，會被自動設成欄位值。舉例來說，使用者模型的 `email` 屬性，將會設定到欄位名稱為 `email` 的 text 欄位，不僅如此，當 Session 閃存資料中有與欄位名稱相符的資料，則會優先於模型的值被填入。優先順序如下：

1. Session 閃存資料（舊輸入資料）
2. 自行傳入的資料
3. 模型屬性資料

這讓你可以快速建立表單，不僅是綁定模型資料，也可以在伺服器端資料驗證錯誤時，輕鬆的回填使用者輸入的舊資料！

> **注意：**當使用 `Form::model` 方法時，必須確保有使用 `Form::close` 方法來關閉表單！

<a name="labels"></a>
## 標籤（ Label ）

#### 產生標籤元素

	echo Form::label('email', 'E-Mail Address');

#### 指定額外 HTML 屬性

	echo Form::label('email', 'E-Mail Address', ['class' => 'awesome']);

> **注意：**在建立標籤後，當建立的表單元素名稱與標籤相符時，會自動建立與標籤名稱相同的 ID 屬性。

<a name="text"></a>
## 文字欄（ Text ）、多行文字欄（ Text Area ）、密碼欄（ Password ）和隱藏欄（ Hidden Field ）

#### 產生文字欄位

	echo Form::text('username');

#### 自定預設值

	echo Form::text('email', 'example@gmail.com');

> **注意：** *hidden* 和 *textarea* 方法和 *text* 方法使用屬性參數相同。

#### 產生密碼欄位

	echo Form::password('password');

#### 產生其他欄位

	echo Form::email($name, $value = null, $attributes = []);
	echo Form::file($name, $attributes = []);

<a name="checkboxes-and-radio-buttons"></a>
## 核取方塊（ Checkboxe ）和單選按鈕（ Radio Button ）

#### 產生核取方塊或單選按鈕

	echo Form::checkbox('name', 'value');

	echo Form::radio('name', 'value');

#### 產生已選取的核取方塊或單選按鈕

	echo Form::checkbox('name', 'value', true);

	echo Form::radio('name', 'value', true);

<a name="number"></a>
## 數字欄（ Number ）

#### 產生數字欄位

	echo Form::number('name', 'value');

<a name="file-input"></a>
## 檔案輸入

#### 產生檔案輸入

	echo Form::file('image');

> **注意：**表單必須已將 `files` 選項設定為 `true`。

<a name="drop-down-lists"></a>
## 下拉式選單

#### 產生下拉式選單

	echo Form::select('size', ['L' => 'Large', 'S' => 'Small']);

#### 產生有預設值的下拉式選單

	echo Form::select('size', ['L' => 'Large', 'S' => 'Small'], 'S');

#### 產生群組清單

	echo Form::select('animal', [
		'Cats' => ['leopard' => 'Leopard'],
		'Dogs' => ['spaniel' => 'Spaniel']
	]);

#### 產生數字區間的下拉式選單

    echo Form::selectRange('number', 10, 20);

#### 產生月份名稱的清單

    echo Form::selectMonth('month');

<a name="buttons"></a>
## 按鈕

#### 產生提交按鈕

	echo Form::submit('Click Me!');

> **提示：**需要產生按鈕（ Button ）元素嗎？試試看 *button* 方法。它與 *submit* 使用相同的屬性參數。

<a name="custom-macros"></a>
## 自定巨集

#### 註冊表單巨集（ Macro ）

定義稱為「巨集」的表單類別的輔助方法是很輕鬆的。下面是它的運作方式。首先註冊巨集，給定名稱及閉合函示：

	Form::macro('myField', function()
	{
		return '<input type="awesome">';
	});

現在可以使用註冊名稱呼叫巨集：

#### 呼叫自定表單巨集

	echo Form::myField();

<a name="generating-urls"></a>
## 產生 URL

更多關於產生 URL 的資訊，參考[輔助方法](/docs/5.0/helpers#urls)。
