# 表單與 HTML

- [開啟表單](#opening-a-form)
- [CSRF 保護](#csrf-protection)
- [表單模型綁定](#form-model-binding)
- [標籤（Label）](#labels)
- [文字欄位（Text）、多行文字欄位（Text Area）、密碼欄位（Password）和隱藏欄位（Hidden Field）](#text)
- [核取方塊（Checkboxe）和單選按鈕（Radio Button）](#checkboxes-and-radio-buttons)
- [檔案輸入](#file-input)
- [下拉式選單](#drop-down-lists)
- [按鈕](#buttons)
- [自訂巨集（Macro）](#custom-macros)
- [產生 URL](#generating-urls)

<a name="opening-a-form"></a>
## 開啟表單

#### 開啟表單

	{{ Form::open(array('url' => 'foo/bar')) }}
		//
	{{ Form::close() }}

預設表單使用 POST 方法，當然你也可以指定傳送其他表單的方法：

	echo Form::open(array('url' => 'foo/bar', 'method' => 'put'))

> **注意：** 因為 HTML 表單只支援 `POST` 和 `GET` 方法，所以在使用 `PUT` 及 `DELETE` 的方法時，Laravel 將會自動加入隱藏的 `_method` 欄位到表單中，來偽裝表單傳送的方法。

你也可以建立指向命名的路由或控制器至表單：

	echo Form::open(array('route' => 'route.name'))

	echo Form::open(array('action' => 'Controller@method'))

您也可以傳遞路由參數：

	echo Form::open(array('route' => array('route.name', $user->id)))

	echo Form::open(array('action' => array('Controller@method', $user->id)))

如果您的表單允許上傳檔案，可以加入 `files` 選項到參數中:

	echo Form::open(array('url' => 'foo/bar', 'files' => true))

<a name="csrf-protection"></a>
## CSRF 保護

#### 添加 CSRF 標記（Token）到表單

Laravel 提供簡易的方法，讓你可以保護你的應用程式不受到 CSRF (跨網站請求偽造) 攻擊。首先 Laravel 會自動在使用者的 session 中放置隨機的 token，別擔心這些會自動完成。這個 CSRF 參數會用隱藏欄位的方式自動加到你的表單中，你也可以使用 `token` 的方法去產生這個隱藏的 CSRF（token）欄位：

	echo Form::token();

#### 附加 CSRF 過濾器到路由

	Route::post('profile', array('before' => 'csrf', function()
	{
		//
	}));

<a name="form-model-binding"></a>
## 表單模型綁定

#### 開啟模型表單

您經常會想要將模型內容加入至表單中，您可以使用 `Form::model` 方法實現：

	echo Form::model($user, array('route' => array('user.update', $user->id)))

現在當你產生表單元素時，像是 text 欄位，模型的值將會自動比對到欄位名稱，並設定此欄位值，舉例來說，使用者模型的 `email` 屬性，將會設定到名稱為 `email` 的 text 欄位的欄位值，不僅如此，當 Session 中有與欄位名稱相符的名稱， Session 的值將會優先於模型的值，而優先順序如下：

1. Session 的資料 (舊的輸入值)
2. 明確傳遞的資料
3. 模型屬性資料

這樣可以允許您快速地建立表單，不僅是綁定模型資料，也可以在伺服器端資料驗證錯誤時，輕鬆的回填使用者輸入的舊資料！

> **注意：** 當使用 `Form::model` 方法時，必須確保有使用 `Form::close` 方法來關閉表單！

<a name="labels"></a>
## 標籤（Label）

#### 產生標籤（Label）元素

	echo Form::label('email', 'E-Mail Address');

#### 指定額外的 HTML 屬性

	echo Form::label('email', 'E-Mail Address', array('class' => 'awesome'));

> **注意：** 在建立標籤時，任何你建立的表單元素名稱與標籤相符時，將會自動在 ID 屬性建立與標籤名稱相同的 ID。

<a name="text"></a>
## 文字欄位、多行文字欄位、密碼欄位、隱藏欄位

#### 產生文字欄位

	echo Form::text('username');

#### 指定預設值

	echo Form::text('email', 'example@gmail.com');


> **注意：** *hidden* 和 *textarea* 方法和 *text* 方法使用屬性參數是相同的。

#### 產生密碼輸入欄位

	echo Form::password('password');

#### 產生其他輸入欄位

	echo Form::email($name, $value = null, $attributes = array());
	echo Form::file($name, $attributes = array());

<a name="checkboxes-and-radio-buttons"></a>
## 核取方塊和單選項鈕

#### 產生核取方塊或單選按鈕

	echo Form::checkbox('name', 'value');

	echo Form::radio('name', 'value');

#### 產生已選取的核取方塊或單選按鈕

	echo Form::checkbox('name', 'value', true);

	echo Form::radio('name', 'value', true);

<a name="file-input"></a>
## 檔案輸入

#### 產生檔案輸入

	echo Form::file('image');

> **注意：**表單必須已將 `files` 選項設定為 `true`。

<a name="drop-down-lists"></a>
## 下拉式選單

#### 產生下拉式選單

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'));

#### 產生選擇預設值的下拉式選單

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'), 'S');

#### 產生群組清單

	echo Form::select('animal', array(
		'Cats' => array('leopard' => 'Leopard'),
		'Dogs' => array('spaniel' => 'Spaniel'),
	));

#### 產生範圍的下拉式選單

    echo Form::selectRange('number', 10, 20);

#### 產生月份名稱的清單

    echo Form::selectMonth('month');

<a name="buttons"></a>
## 按鈕

#### 產生提交按鈕

	echo Form::submit('Click Me!');

> **注意：** 需要產生按鈕（Button）元素嗎？可以試著使用 *button* 方法去產生按鈕（Button）元素，button 方法與 *submit* 使用屬性參數是相同的。

<a name="custom-macros"></a>
## 自訂巨集

#### 註冊表單巨集

您可以輕鬆的定義你自己的表單類別的輔助方法叫「巨集（macros）」，首先只要註冊巨集（macros），並給預期名稱及封閉函式：

	Form::macro('myField', function()
	{
		return '<input type="awesome">';
	});

現在您可以使用註冊的名稱呼叫您的巨集：

#### 呼叫自訂表單巨集

	echo Form::myField();


<a name="generating-urls"></a>
##產生 URL

更多產生 URL 的資訊，請參閱文件 [輔助方法](/docs/helpers#urls)。
