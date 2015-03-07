# 驗證

- [基本用法](#basic-usage)
- [控制器驗證](#controller-validation)
- [表單請求驗證](#form-request-validation)
- [操作錯誤訊息](#working-with-error-messages)
- [錯誤訊息與視圖](#error-messages-and-views)
- [可用的驗證規則](#available-validation-rules)
- [依條件增加規則](#conditionally-adding-rules)
- [自定錯誤訊息](#custom-error-messages)
- [自定驗證規則](#custom-validation-rules)

<a name="basic-usage"></a>
## 基本用法

Laravel 透過 `Validation` 類別讓你可以簡單、方便的驗證資料正確性及取得驗證的錯誤訊息。

#### 基本驗證範例

	$validator = Validator::make(
		['name' => 'Dayle'],
		['name' => 'required|min:5']
	);

傳入 `make` 方法的第一個參數是待驗證的資料，第二個參數是資料的驗證規則。

#### 使用陣列來定義規則

多個規則之間可以使用「管線（ pipe ）」符號分隔，或是作爲陣列裡的單一元素。

	$validator = Validator::make(
		['name' => 'Dayle'],
		['name' => ['required', 'min:5']]
	);

#### 驗證多個欄位

    $validator = Validator::make(
        [
            'name' => 'Dayle',
            'password' => 'lamepassword',
            'email' => 'email@example.com'
        ],
        [
            'name' => 'required',
            'password' => 'required|min:8',
            'email' => 'required|email|unique:users'
        ]
    );

當一個 `Validator` 實例被建立，`fails`（或 `passes`）這二個方法可以取得驗證結果。

	if ($validator->fails())
	{
		// The given data did not pass validation
	}

假如驗證失敗，可以從 validator 接收錯誤資訊。

	$messages = $validator->messages();

你也可以只取得造成驗證失敗的規則陣列，不包含訊息。使用 `failed` 方法：

	$failed = $validator->failed();

#### 驗證檔案

`Validator` 類別提供了一些規則用來驗證檔案，例如 `size`、`mimes` 等等。當需要驗證檔案時，你僅需將它們和其他的資料一同送給 validator 即可。

### 驗證後掛鉤

Validator 也可以讓你附加回呼函數，並在驗證後執行。這可以讓你作進一步進行驗證，甚至是加入更多錯誤訊息到訊息集合中。在 validator 實例使用 `after` 方法作為開始：

	$validator = Validator::make(...);

	$validator->after(function($validator)
	{
		if ($this->somethingElseIsInvalid())
		{
			$validator->errors()->add('field', 'Something is wrong with this field!');
		}
	});

	if ($validator->fails())
	{
		//
	}

你可以依照需求加入任意個你想要的 `after` 回呼函數。

<a name="controller-validation"></a>
## 控制器驗證

當然，每次都要手動建立 `Validator` 實例和確認驗證結果是很頭痛的事。別擔心，你現在有其他選擇！Laravel 預設的基底 `App\Http\Controllers\Controller` 類別，使用了 `ValidatesRequests` trait。它提供了單一、便利的方式驗證傳入的 HTTP 請求。下面是它看起來的樣子：

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		//
	}

當驗證通過，接下來的程式碼就會正常執行。然而，若驗證失敗，會拋出 `Illuminate\Contracts\Validation\ValidationException` 例外。這個例外會自動被捕捉，並產生重導至使用者之前的位置。甚至驗證的錯誤訊息會被自動閃存至 session！

如果進來的是一個 AJAX 請求，就不會產生重導。而是會傳回一個 HTTP 回應，包含 422 狀態碼，並包含驗證錯誤的 JSON 資料。

例如，下面是手工撰寫的，能發揮相同功能的程式碼：

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$v = Validator::make($request->all(), [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		if ($v->fails())
		{
			return redirect()->back()->withErrors($v->errors());
		}

		//
	}

### 自定閃存的錯誤訊息格式

如果你想要自定驗證失敗時，閃存到 session 的驗證錯誤的格式，在你的基底控制器覆寫 `formatValidationErrors` 方法。別忘了上方要引入 `Illuminate\Validation\Validator`：

	/**
	 * {@inheritdoc}
	 */
	protected function formatValidationErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="form-request-validation"></a>
## 表單請求驗證

在更複雜的驗證情境中，你可能會想建立一個「表單請求（ form request ）」。表單請求是一個自定的請求類別，裡面包含驗證的邏輯。要建立一個表單請求類別，使用 Artisan 命令列指令 `make:request`：

	php artisan make:request StoreBlogPostRequest

新產生的類別檔會放在 `app/Http/Requests` 目錄下。讓我們加入一些驗證規則到 `rules` 方法中：

	/**
	 * Get the validation rules that apply to the request.
	 *
	 * @return array
	 */
	public function rules()
	{
		return [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		];
	}

所以，驗證的規則會如何被執行？你所需要的只有在控制器方法，利用型別提示傳入請求。

	/**
	 * Store the incoming blog post.
	 *
	 * @param  StoreBlogPostRequest  $request
	 * @return Response
	 */
	public function store(StoreBlogPostRequest $request)
	{
		// The incoming request is valid...
	}

進入的請求會在控制器方法被呼叫前進行驗證，意味著你不會因為驗證邏輯把控制器弄的一團糟。因為請求已經被驗證了！

如果驗證失敗，會產生一個重導回應，並將使用者送回先前的頁面。錯誤訊息會被閃存到 session，所以可以將它們顯示出來。如果是個 AJAX 請求，會返回一個 HTTP 回應，包含 422 狀態碼，並包含驗證錯誤的 JSON 資料。

### 授權表單請求

表單請求類別也包含了一個 `authorize` 方法。在這方法裡，你可以確認使用者是否真的通過授權，可以更新特定資料。打個比方，當一個使用者試圖更新部落格文章的評論，他確實是這篇評論的擁有者嗎？例如：

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		$commentId = $this->route('comment');

		return Comment::where('id', $commentId)
                      ->where('user_id', Auth::id())->exists();
	}

注意上面範例呼叫的 `route` 方法。這個方法可以幫助你，取得路由被呼叫時傳入的 URI 參數，像是如下範例的  `{comment}` 參數：

	Route::post('comment/{comment}');

如果 `authorize` 方法回傳 `false`，會自動回傳一個 HTTP 回應，包含 403 狀態碼，而你的控制器方法將不會被執行。

如果你打算在應用程式的其他部分處理授權邏輯，只要從 `authorize` 方法回傳 `true`：

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		return true;
	}

### 自定閃存的錯誤訊息格式

如果你想要自定驗證失敗時，閃存到 session 的驗證錯誤的格式，在你的基底 request（`App\Http\Requests\Request` ）覆寫 `formatValidationErrors` 方法。別忘了上方要引入 `Illuminate\Validation\Validator`：

	/**
	 * {@inheritdoc}
	 */
	protected function formatErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="working-with-error-messages"></a>
## 操作錯誤訊息

呼叫一個 `Validator` 實例的 `messages` 方法，會得到一個 `MessageBag` 的實例，裡面有許多方便的方法讓你操作錯誤訊息。

#### 查看特定欄位的第一個錯誤訊息

	echo $messages->first('email');

#### 查看特定欄位的所有錯誤訊息

	foreach ($messages->get('email') as $message)
	{
		//
	}

#### 查看所有欄位的所有錯誤訊息

	foreach ($messages->all() as $message)
	{
		//
	}

#### 判斷特定欄位是否有錯誤訊息

	if ($messages->has('email'))
	{
		//
	}

#### 取得格式化後的錯誤訊息

	echo $messages->first('email', '<p>:message</p>');

> **注意：**預設上，錯誤訊息會以 Bootstrap 相容語法輸出。

#### 取得所有格式化後的錯誤訊息

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="error-messages-and-views"></a>
## 錯誤訊息與視圖

當驗證過後，你會需要一個簡易的方式取得錯誤訊息並回傳到視圖中。在 Laravel 你可以很方便的處理這些事，瞧瞧下面的路由範例：

	Route::get('register', function()
	{
		return View::make('user.register');
	});

	Route::post('register', function()
	{
		$rules = [...];

		$validator = Validator::make(Input::all(), $rules);

		if ($validator->fails())
		{
			return redirect('register')->withErrors($validator);
		}
	});

可以注意到當驗證失敗，我們將 `Validator` 實例傳入重新導向（ Redirect ）的 `withErrors` 方法。它會在 session 閃存錯誤訊息，這樣就能在下個請求中使用。

然而，注意到我們並沒有特別在 GET 路由的視圖中，綁定錯誤訊息。因為 Laravel 總是會確認在 session 資料中是否有錯誤訊息，若有則自動將它們綁定至視圖。**所以請注意，`$errors` 變數會存在所有的請求回傳的視圖中**，讓你可以直接假設 `$errors` 變數已被定義且可以安全地使用。`$errors` 變數是一個 `MessageBag` 類別的實例。

所以在重新導向之後，你就可以在視圖中使用被自動綁定的 `$errors` 變數：

	<?php echo $errors->first('email'); ?>

### 命名錯誤清單

假如在一個頁面中有許多的表單，你可能希望為 `MessageBag` 的錯誤命名。這可以讓你取得特定表單的所有錯誤訊息，只要在 `withErrors` 的第二個參數設定名稱即可：

	return redirect('register')->withErrors($validator, 'login');

然後你就可以從一個 `$errors` 變數中，取得已命名的 `MessageBag` 實例：

	<?php echo $errors->login->first('email'); ?>

<a name="available-validation-rules"></a>
## 可用的驗證規則

以下是所有可用的驗證規則清單與功能：

- [Accepted](#rule-accepted)
- [Active URL](#rule-active-url)
- [After (Date)](#rule-after)
- [Alpha](#rule-alpha)
- [Alpha Dash](#rule-alpha-dash)
- [Alpha Numeric](#rule-alpha-num)
- [Array](#rule-array)
- [Before (Date)](#rule-before)
- [Between](#rule-between)
- [Boolean](#rule-boolean)
- [Confirmed](#rule-confirmed)
- [Date](#rule-date)
- [Date Format](#rule-date-format)
- [Different](#rule-different)
- [Digits](#rule-digits)
- [Digits Between](#rule-digits-between)
- [E-Mail](#rule-email)
- [Exists (Database)](#rule-exists)
- [Image (File)](#rule-image)
- [In](#rule-in)
- [Integer](#rule-integer)
- [IP Address](#rule-ip)
- [Max](#rule-max)
- [MIME Types](#rule-mimes)
- [Min](#rule-min)
- [Not In](#rule-not-in)
- [Numeric](#rule-numeric)
- [Regular Expression](#rule-regex)
- [Required](#rule-required)
- [Required If](#rule-required-if)
- [Required With](#rule-required-with)
- [Required With All](#rule-required-with-all)
- [Required Without](#rule-required-without)
- [Required Without All](#rule-required-without-all)
- [Same](#rule-same)
- [Size](#rule-size)
- [String](#rule-string)
- [Timezone](#rule-timezone)
- [Unique (Database)](#rule-unique)
- [URL](#rule-url)

<a name="rule-accepted"></a>
#### accepted

驗證欄位值是否為 _yes_ ， _on_ ，或 _1_ 。這在確認「服務條款」是否同意時很有用。

<a name="rule-active-url"></a>
#### active_url

驗證欄位值是否為一個有效的網址，會透過 PHP 的 `checkdnsrr` 函式來驗證。

<a name="rule-after"></a>
#### after:_date_

驗證欄位是否是在指定日期之後。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-alpha"></a>
#### alpha

驗證欄位值是否僅包含字母字元。

<a name="rule-alpha-dash"></a>
#### alpha_dash

驗證欄位值是否僅包含字母、數字、破折號（ - ）以及底線（ _ ）。

<a name="rule-alpha-num"></a>
#### alpha_num

驗證欄位值是否僅包含字母、數字。

<a name="rule-array"></a>
#### array

驗證欄位值是否為陣列。

<a name="rule-before"></a>
#### before:_date_

驗證欄位是否是在指定日期之前。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-between"></a>
#### between:_min_,_max_

驗證欄位值的大小是否介於指定的 _min_ 和 _max_ 之間。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-boolean"></a>
#### boolean

驗證欄位值必須要能夠轉型為布林值。可接受的參數為 `true`、`false`、`1`、`0`、`"1"` 以及 `"0"`。

<a name="rule-confirmed"></a>
#### confirmed

驗證欄位值必須和 `foo_confirmation` 命名型式的欄位其值一致。例如，如果要驗證的欄位是 `password`，就必須和輸入資料裡的 `password_confirmation` 欄為值相同。

<a name="rule-date"></a>
#### date

驗證欄位值是有效的日期，會根據 PHP 的 `strtotime` 函示做驗證。

<a name="rule-date-format"></a>
#### date_format:_format_

驗證欄位值符合定義的日期 _格式_ ，透過 PHP 的 `date_parse_from_format` 函式驗證。

<a name="rule-different"></a>
#### different:_field_

驗證欄位值是否和指定的 _欄位（ field ）_ 不同。

<a name="rule-digits"></a>
#### digits:_value_

驗證欄位值為 _數字_ 且長度為 _value_ 。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

驗證欄位值的長度在 _min_ 和 _max_ 之間。

<a name="rule-email"></a>
#### email

驗證欄位值符合 email 格式。

<a name="rule-exists"></a>
#### exists:_table_,_column_

驗證欄位值存在指定的資料表中。

#### Exists 規則的基本使用方法

	'state' => 'exists:states'

#### 指定一個特定的欄位名稱

	'state' => 'exists:states,abbreviation'

也可以指定更多的條件，它們會被加到 "where" 查詢語句裡：

	'email' => 'exists:staff,email,account_id,1'

如果傳入 "where" 語句的查詢值是 `NULL`，會確認查詢條件的值是否為 `NULL`。

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="rule-image"></a>
#### image

驗證欄位檔案必須為圖片格式（ jpeg、png、bmp、gif、 或 svg ）。

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

驗證欄位值有在給定的清單裡。

<a name="rule-integer"></a>
#### integer

驗證欄位值是整數。

<a name="rule-ip"></a>
#### ip

驗證欄位值符合 IP address 的格式。

<a name="rule-max"></a>
#### max:_value_

驗證欄位值的大小是否小於或等於 _value_ 。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

驗證欄位檔案的 MIME 類型必須符合清單裡。

#### MIME 規則基本用法

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

驗證欄位值的大小是否大於或等於 _value_ 。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

驗證欄位值不在給定的清單裡。

<a name="rule-numeric"></a>
#### numeric

驗證欄位值是否為數值。

<a name="rule-regex"></a>
#### regex:_pattern_

驗證欄位值符合給定的正規表示式。

**注意:**當使用 `regex` pattern 時，你必須使用陣列，而不該用管線分隔規則，尤其是當正規表示式中含有管線字元（ | ）時。

<a name="rule-required"></a>
#### required

驗證輸入資料裏有此欄位。

<a name="rule-required-if"></a>
#### required_if:_field_,_value_,...

如果指定 _欄位（ field ）_ 的欄位值等於任何一個 _value_ ，則此欄位為必填。

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

如果指定的欄位之中， _任一_ 個有值，則此欄位為必填。

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

如果指定的 _所有_ 欄位都有值，則此欄位為必填。

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

如果缺少 _任何一個_ 指定的欄位，則此欄位為必填。

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

如果 _所有_ 指定的欄位都沒有值，則此欄位為必填。

<a name="rule-same"></a>
#### same:_field_

驗證欄位值和指定的 _欄位（ field ）_ 值相同。

<a name="rule-size"></a>
#### size:_value_

驗證欄位值的大小需符合給定 _value_ 值。對於字串來說， _value_ 為字元數。對於數字來說， _value_ 為某個整數值。對於檔案來說， _value_ 是檔案大小（單位 kb ）。

<a name="rule-string"></a>
#### string:_value_

驗證欄位值的型別是否為字串。

<a name="rule-timezone"></a>
#### timezone

驗證欄位值是個有效的時區，會根據 PHP 的 `timezone_identifiers_list` 函式來判斷。

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

驗證欄位值在給定的資料表中唯一。如果沒有指定 `column`，將會使用欄位本身的名稱。

#### Unique 規則的基本用法

	'email' => 'unique:users'

#### 指定一個特定的欄位名稱

	'email' => 'unique:users,email_address'

#### 強迫 Unique 規則忽略特定 ID

	'email' => 'unique:users,email_address,10'

#### 增加額外的 Where 查詢

也可以指定更多的條件到 "where" 查詢語句：

	'email' => 'unique:users,email_address,NULL,id,account_id,1'

上述規則中，只有 `account_id` 為 `1` 的資料列會被包含在 unique 規則的驗證。

<a name="rule-url"></a>
#### url

驗證欄位值需符合 URL 格式。

> **注意:**此函式使用 PHP 的 `filter_var` 函示。

<a name="conditionally-adding-rules"></a>
## 依條件增加規則

某些情況下，你可能**只想**在輸入資料中有此欄位時，才進行驗證。只要增加 `sometimes` 規則到進規則列表，就可以快速達成：

	$v = Validator::make($data, [
		'email' => 'sometimes|required|email',
	]);

在上面的範例中，`email` 欄位的驗證，只會在 `$data` 陣列有此欄位才會進行。

#### 複雜的條件驗證

有時，你可以希望某個指定欄位，在另一個欄位的值有超過 100 時才為必填。
或者你當某個指定欄位有值時，另外兩個欄位要符合特定值。增加這樣的驗證條件並不痛苦。首先，利用你熟悉的 _靜態規則_ 建立一個 `Validator` 實例：

	$v = Validator::make($data, [
		'email' => 'required|email',
		'games' => 'required|numeric',
	]);

假設我們的網頁應用程式是專為遊戲收藏家所設計。如果遊戲收藏家收藏超過一百款遊戲，我們希望他們說明為什麼他們擁有這麼多遊戲。像是，可能他們經營一家二手遊戲商店，或是他們可能只是享受收集的樂趣。為了在特定條件下，加入此驗證需求，我們可以在 `Validator` 實例使用 `sometimes` 方法。

	$v->sometimes('reason', 'required|max:500', function($input)
	{
		return $input->games >= 100;
	});

傳入 `sometimes` 方法的第一個參數，是我們要依條件認證的欄位名稱。第二個參數是我們想加入驗證規則。`閉包（ Closure ）`作為第三個參數傳入，如果其回傳 `true`，額外的規則就會被加入。這個方法可以輕而易舉的建立複雜的條件式驗證。你甚至可以一次對多個欄位增加條件式驗證：

	$v->sometimes(['reason', 'cost'], 'required', function($input)
	{
		return $input->games >= 100;
	});

> **注意：**傳入 `Closure` 的 `$input` 參數為 `Illuminate\Support\Fluent` 的實例，可以用來作為取得你的輸入和檔案的物件。

<a name="custom-error-messages"></a>
## 自定錯誤訊息

如果需要，你可以自定驗證錯誤訊息，取代預設的錯誤訊息。有幾個方式可以自定訊息。

#### 將自定訊息傳入 Validator

	$messages = [
		'required' => 'The :attribute field is required.',
	];

	$validator = Validator::make($input, $rules, $messages);

> **注意：**`:attribute` place-holder 會被驗證欄位的名稱給取代。你也可以在驗證訊息中使用其他的驗證 place-holders。

#### 其他的驗證 Place-Holders

	$messages = [
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	];

#### 為特定屬性指定自定的訊息

有時你可能想為特定欄位指定自定的錯誤訊息：

	$messages = [
		'email.required' => 'We need to know your e-mail address!',
	];

<a name="localization"></a>
#### 在語言檔中指定自定訊息

某些狀況下，你可能希望在語言檔中指定自定訊息，而非直接將他們傳遞給 `Validator`。要達到目的，將你的訊息增加至 `resources/lang/xx/validation.php` 語言檔的 `custom` 陣列中。

	'custom' => [
		'email' => [
			'required' => 'We need to know your e-mail address!',
		],
	],

<a name="custom-validation-rules"></a>
## 自定驗證規則

#### 註冊自定驗證規則

Laravel 提供了很多有用的驗證規則；但是，你可能希望自定一些。註冊自定的驗證規則的方法之一，就是使用 `Validator::extend` 方法：

	Validator::extend('foo', function($attribute, $value, $parameters)
	{
		return $value == 'foo';
	});

自定的驗證閉包接收三個參數：要被驗證的屬性名稱 `$attribute`，屬性的值 `$value`，傳入驗證規則的參數陣列 `$parameters`。

除了使用閉包，你也可以傳入類別和方法到 `extend` 方法中：

	Validator::extend('foo', 'FooValidator@validate');

注意，你同時也需要為自定的規則設定錯誤訊息。你可以使用行內的自定訊息陣列，或是新增在認證語言檔裡。

#### 繼承 Validator 類別

除了使用閉包回呼（ Closure callbacks ）擴展 Validator，你也可以直接繼承 Validator 類別本身。你可以寫一個繼承 `Illuminate\Validation\Validator` 的 Validator 類別。你也可以加入驗證方法到以 `validate` 為前綴的方法到類別中：

	<?php

	class CustomValidator extends Illuminate\Validation\Validator {

		public function validateFoo($attribute, $value, $parameters)
		{
			return $value == 'foo';
		}

	}

#### 註冊自定的 Validator 解析

接下來，你需要註冊自定的 Validator 繼承：

	Validator::resolver(function($translator, $data, $rules, $messages)
	{
		return new CustomValidator($translator, $data, $rules, $messages);
	});

建立自定的驗證規則時，你有時可能想要自訂錯誤訊息的 place-holder。你可以如上所述，建立一個自定的 Validator，並加進 `replaceXXX` 方法。

	protected function replaceFoo($message, $attribute, $rule, $parameters)
	{
		return str_replace(':foo', $parameters[0], $message);
	}

如果你只是想要增加一個自定訊息的 "replacer"，但不繼承 `Validator` 類別，可以使用 `Validator::replacer` 方法：

	Validator::replacer('rule', function($message, $attribute, $rule, $parameters)
	{
		//
	});
