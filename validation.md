# 驗證

- [基本用法](#basic-usage)
- [使用錯誤訊息](#working-with-error-messages)
- [錯誤訊息 & 視圖](#error-messages-and-views)
- [使用驗證規則](#available-validation-rules)
- [有條件新增規則](#conditionally-adding-rules)
- [自訂錯誤訊息](#custom-error-messages)
- [自訂驗證規則](#custom-validation-rules)

<a name="basic-usage"></a>
## 基本用法

Laravel 透過 `Validation` 類別讓你可以簡單、方便的驗證資料正確性及查看驗證的錯誤訊息。

#### 基本驗證範例

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => 'required|min:5')
	);


我們透過 `make` 這個方法來的第一個參數設定該被驗證資料名稱，然後第二個參數我們定義該資料可被接受的規則。

#### 使用陣列來定義規則

多個規則可以使用"|"符號分隔，或是單一陣列作為單獨的元素分隔。

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => array('required', 'min:5'))
	);

#### 驗證多個欄位

    $validator = Validator::make(
        array(
            'name' => 'Dayle',
            'password' => 'lamepassword',
            'email' => 'email@example.com'
        ),
        array(
            'name' => 'required',
            'password' => 'required|min:8',
            'email' => 'required|email|unique:users'
        )
    );


當一個 `Validator` 實例被建立，`fails`（或 `passes`） 這二個方法就可以在驗證時使用，如下：

	if ($validator->fails())
	{
		// The given data did not pass validation
	}


假如驗證失敗，您可以從驗證器中接收錯誤資訊。

	$messages = $validator->messages();


您可能不需要錯誤訊息，只想取得無法通過驗證的規則，您可以使用 'failed' 方法：

	$failed = $validator->failed();

#### 驗證檔案

`Validator` 類別提供了一些規則用來驗證檔案，例如 `size`, `mimes` 等等。當需要驗證檔案時，你僅需將它們和你其他的資料一同送給驗證器即可。

<a name="working-with-error-messages"></a>
## 使用錯誤訊息

當你呼叫一個 `Validator` 實例的 `messages` 方法後，你會得到一個 `MessageBag` 的變數，裡面有許多方便的方法讓你取得錯誤訊息。

#### 查看一個欄位的第一個錯誤訊息

	echo $messages->first('email');

#### 查看一個欄位的所有錯誤訊息

	foreach ($messages->get('email') as $message)
	{
		//
	}

#### 查看所有欄位的所有錯誤訊息

	foreach ($messages->all() as $message)
	{
		//
	}

#### 判斷一個欄位是否有錯誤訊息

	if ($messages->has('email'))
	{
		//
	}

#### 錯誤訊息格式化輸出

	echo $messages->first('email', '<p>:message</p>');

> **注意:** 預設錯誤訊息以 Bootstrap 相容語法輸出。

#### 查看所有錯誤訊息並以格式化輸出

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="error-messages-and-views"></a>
## 錯誤訊息 & 視圖

當你開始進行驗證，你將會需要一個簡易的方法去取得錯誤訊息並回傳到你的視圖中，在 Laravel 你可以很方便的處理這些事，你可以透過下面的路由例子來了解：


	Route::get('register', function()
	{
		return View::make('user.register');
	});

	Route::post('register', function()
	{
		$rules = array(...);

		$validator = Validator::make(Input::all(), $rules);

		if ($validator->fails())
		{
			return Redirect::to('register')->withErrors($validator);
		}
	});

記得當驗證失敗後，我們會使用 `withErrors` 方法來將 `Validator` 實例進行重新導向。這方法會將錯誤訊息存入 session 中，這樣才能在下個請求中被使用。

然而，我們並不需要特別去將錯誤訊息綁定在我們 GET 路由的視圖中。因為 Laravel 會確認在 Session 資料中是否有錯誤訊息，並且自動將它們綁定至視圖中。**所以請注意，`$errors` 變數存在於所有的視圖中，所有的請求裡，**讓你可以直接假設 `$errors` 變數已被定義且可以安全地使用。`$errors` 變數是 `MessageBag` 類別的一個實例。

所以，重新導向之後，你可以自然的在視圖中使用 `$errors` 變數：

	<?php echo $errors->first('email'); ?>

### 命名錯誤清單

假如你在一個頁面中有許多的表單, 你可能希望為錯誤命名一個`MessageBag`. 這將讓你針對特定的表單查看其錯誤訊息, 我們只要簡單的在 `withErrors` 的第二個參數設定名稱即可：

	return Redirect::to('register')->withErrors($validator, 'login');

接著你可以從一個 `$errors` 變數中取得已命名的 `MessageBag` 實例：

	<?php echo $errors->login->first('email'); ?>

<a name="available-validation-rules"></a>
## 既存的驗證規則

以下是既存的驗證規則清單與他們的函式名稱：

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
- [Timezone](#rule-timezone)
- [Unique (Database)](#rule-unique)
- [URL](#rule-url)

<a name="rule-accepted"></a>
#### accepted

欄位值為 _yes_, _on_, 或是 _1_ 時，驗證才會通過。這在確認"服務條款"是否同意時很有用。

<a name="rule-active-url"></a>
#### active_url

欄位值透過 PHP 函式 `checkdnsrr` 來驗證是否為一個有效的網址。

<a name="rule-after"></a>
#### after:_date_

驗證欄位是否是在指定日期之後。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-alpha"></a>
#### alpha

欄位僅全數為字母字元時通過驗證。

<a name="rule-alpha-dash"></a>
#### alpha_dash

欄位值僅允許字母、數字、破折號（-）以及底線（_）

<a name="rule-alpha-num"></a>
#### alpha_num

欄位值僅允許字母、數字

<a name="rule-array"></a>
#### array

欄位值僅允許為陣列

<a name="rule-before"></a>
#### before:_date_

驗證欄位是否是在指定日期之前。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-between"></a>
#### between:_min_,_max_

欄位值需介於指定的 _min_ 和 _max_ 值之間。字串、數值或是檔案都是用同樣的方式來進行驗證。


<a name="rule-confirmed"></a>
#### confirmed

欄位值需與對應的欄位值 `foo_confirmation` 相同。例如，如果驗證的欄位是 `password` ，那對應的欄位 `password_confirmation` 就必須存在且與 `password` 欄位相符。

<a name="rule-date"></a>
#### date

欄位值透過 PHP `strtotime` 函式驗證是否為一個合法的日期。

<a name="rule-date-format"></a>
#### date_format:_format_

欄位值透過 PHP `date_parse_from_format` 函式驗證符合 _format_ 制定格式的日期是否為合法日期。

<a name="rule-different"></a>
#### different:_field_

欄位值需與指定的欄位 _field_ 值不同。


<a name="rule-digits"></a>
#### digits:_value_

欄位值需為數字且長度需為 _value_。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

欄位值需為數字，且長度需介於 _min_ 與 _max_ 之間。

<a name="rule-boolean"></a>
#### boolean

欄位必須可以轉換成布林值，可接受的值為 `true`, `false`, `1`, `0`, `"1"`, `"0"`。

<a name="rule-email"></a>
#### email

欄位值需符合 email 格式。

<a name="rule-exists"></a>
#### exists:_table_,_column_

欄位值需與存在於資料庫 _table_ 中的 _column_ 欄位值其一相同。

#### Exists 規則的基本使用方法

	'state' => 'exists:states'

#### 指定一個自訂的欄位名稱

	'state' => 'exists:states,abbreviation'

你可以指定更多條件且那些條件將會被新增至 "where" 查詢裡：

	'email' => 'exists:staff,email,account_id,1'
	/* 這個驗證規則為 email 需存在於 staff 這個資料表中 email 欄位中且 account_id=1 */

透過`NULL`搭配"where"的縮寫寫法去檢查資料庫的是否為`NULL`

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="rule-image"></a>
#### image

檔案必需為圖片(jpeg, png, bmp 或 gif)

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

欄位值需符合事先給予的清單的其中一個值

<a name="rule-integer"></a>
#### integer

欄位值需為一個整數值

<a name="rule-ip"></a>
#### ip

欄位值需符合 IP 位址格式。

<a name="rule-max"></a>
#### max:_value_

欄位值需小於等於 _value_。字串、數字和檔案則是判斷 `size` 大小。

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

檔案的 MIME 類別需在給定清單中的列表中才能通過驗證。

#### MIME規則基本用法

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

欄位值需大於等於 _value_。字串、數字和檔案則是判斷 `size` 大小。

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

欄位值不得為給定清單中其一。

<a name="rule-numeric"></a>
#### numeric

欄位值需為數字。

<a name="rule-regex"></a>
#### regex:_pattern_

欄位值需符合給定的正規表示式。

**注意:** 當使用`regex`模式時，你必須使用陣列來取代"|"作為分隔，尤其是當正規表示式中含有"|"字元。

<a name="rule-required"></a>
#### required

欄位值為必填。

<a name="rule-required-if"></a>
#### required\_if:_field_,_value_

欄位值在 _field_ 欄位值為 _value_ 時為必填。

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

欄位值 _僅在_ 任一指定欄位有值情況下為必填。

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

欄位值 _僅在_ 所有指定欄位皆有值情況下為必填。

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

欄位值 _僅在_ 任一指定欄位沒有值情況下為必填。

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

欄位值 _僅在_ 所有指定欄位皆沒有值情況下為必填。

<a name="rule-same"></a>
#### same:_field_

欄位值需與指定欄位 _field_ 等值。

<a name="rule-size"></a>
#### size:_value_

欄位值的尺寸需符合給定 _value_ 值。對於字串來說，_value_ 為需符合的字元長度。對於數字來說，_value_ 為需符合的整數值。對於檔案來說，_value_ 為需符合的檔案大小（單位 kb)。

<a name="rule-timezone"></a>
#### timezone

欄位值透過 PHP `timezone_identifiers_list` 函式來驗證是否為有效的時區。

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

欄位值在給定的資料庫中需為唯一值。如果 `column（欄位）` 選項沒有指定，將會使用欄位名稱。

#### 唯一(Unique)規則的基本用法

	'email' => 'unique:users'

#### 指定一個自訂的欄位名稱

	'email' => 'unique:users,email_address'

#### 強制唯一規則忽略指定的 ID

	'email' => 'unique:users,email_address,10'

#### 增加額外的 Where 條件

你也可以指定更多的條件式到 "where" 查詢語句中：

	'email' => 'unique:users,email_address,NULL,id,account_id,1'

上述規則為只有 `account_id` 為 `1` 的資料列會做唯一規則的驗證。

<a name="rule-url"></a>
#### url

欄位值需符合 URL 的格式。

> **注意:** 此函式會使用 PHP `filter_var` 方法驗證。

<a name="conditionally-adding-rules"></a>
## 有條件新增規則

某些情況下，你可能 **只想** 當欄位有值時，才進行驗證。只要增加 `sometimes` 條件進條件列表中，就可以快速達成：

	$v = Validator::make($data, array(
		'email' => 'sometimes|required|email',
	));

在上述範例中，`email` 欄位只會在當其在 `$data` 陣列中有值的情況下才會被驗證。

#### 複雜的條件式驗證

有時，你可以希望給定欄位在其他欄位有超過 100 時為必填。或者你希望兩個欄位，當其一欄位有值時，另一欄位將會有一個給定的值。增加這樣的驗證條件並不痛苦。首先，利用你尚未更動的 _靜態規則_ 創建一個 `Validator` 實例：

	$v = Validator::make($data, array(
		'email' => 'required|email',
		'games' => 'required|numeric',
	));

假設我們的網頁應用程式是專為遊戲收藏家所設計。如果遊戲收藏家收藏超過一百款遊戲，我們希望他們說明為什麼他們擁有這麼多遊戲。像是，可能他們經營一家二手遊戲商店，或是他們可能只是享受收集的樂趣。有條件的加入此需求，我們可以在 `Validator` 實例中使用 `sometimes` 方法。

	$v->sometimes('reason', 'required|max:500', function($input)
	{
		return $input->games >= 100;
	});

傳遞至 `sometimes` 方法的第一個參數是我們要條件式認證的欄位名稱。第二個參數是我們想加入驗證規則。 `閉包（Closure）` 作為第三個參數傳入，如果回傳值為 `true` 那該規則就會被加入。這個方法可以輕而易舉的建立複雜的條件式驗證。你也可以一次對多個欄位增加條件式驗證：

	$v->sometimes(array('reason', 'cost'), 'required', function($input)
	{
		return $input->games >= 100;
	});

> **注意:** 傳遞至你的 `Closure` 的 `$input` 參數為 `Illuminate\Support\Fluent` 的實例且用來作為存取你的輸入及檔案的物件。

<a name="custom-error-messages"></a>
## 自訂錯誤訊息

如果需要，你可以為驗證自訂錯誤訊息取代預設錯誤訊息。這裏有幾個方式可以設定客制訊息。

#### 傳遞客制訊息進驗證器

	$messages = array(
		'required' => 'The :attribute field is required.',
	);

	$validator = Validator::make($input, $rules, $messages);

> **注意:** 在驗證中，`:attribute` 佔位符會被欄位的實際名稱給取代。你也可以在驗證訊息中使用其他的佔位符。

#### 其他的驗證佔位符

	$messages = array(
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	);

#### 為特定屬性給予一個客制化訊息

有時你只想為一個特定欄位指定一個客制錯誤訊息：

	$messages = array(
		'email.required' => 'We need to know your e-mail address!',
	);

<a name="localization"></a>
#### 在語言檔中指定客制訊息

某些狀況下，你可能希望在語言檔中設定你的客制訊息，而非直接將他們傳遞給 `Validator`。要達到目的，將你的訊息增加至 `app/lang/xx/validation.php` 檔案的 `custom` 陣列中。

	'custom' => array(
		'email' => array(
			'required' => 'We need to know your e-mail address!',
		),
	),

<a name="custom-validation-rules"></a>
## 自訂驗證規則

#### 註冊自訂驗證規則

Laravel 提供了各種有用的驗證規則，但是，你可能希望可以設定一些自己專用的。註冊自訂的驗證規則的方法之一就是使用 `Validator::extend` 方法：

	Validator::extend('foo', function($attribute, $value, $parameters)
	{
		return $value == 'foo';
	});

客制驗證器閉包接收三個參數：要被驗證的 `$attribute(屬性)` 的名稱，屬性的值 `$value`，傳遞至驗證規則的 `$parameters` 陣列。

你同樣可以傳遞一個類別和方法到 `extend` 方法中，取代原本的閉包：

	Validator::extend('foo', 'FooValidator@validate');

注意,你同時需要為你的自訂規則訂立一個錯誤訊息。你可以使用行內自訂訊息陣列或是在認證語言檔裡新增。

#### 擴展 Validator 類別

除了使用閉包回呼(Closure callbacks)來擴展 Validator 外，你一樣可以直接擴展 Validator 類別。你可以寫一個擴展自 `Illuminate\Validation\Validator` 的驗證器類別。你也可以增加驗證方法到以 `validate` 為開頭的類別中：


	<?php

	class CustomValidator extends Illuminate\Validation\Validator {

		public function validateFoo($attribute, $value, $parameters)
		{
			return $value == 'foo';
		}

	}

#### Registering A Custom Validator Resolver

接下來，你需要註冊你自訂驗證器擴展：

	Validator::resolver(function($translator, $data, $rules, $messages)
	{
		return new CustomValidator($translator, $data, $rules, $messages);
	});

當創建自訂驗證規則時，你可能有時需要為錯誤訊息定義客制化的佔位符。你可以如上所述創建一個自訂的驗證器，然後增加 `replaceXXX` 函式進驗證器中。

	protected function replaceFoo($message, $attribute, $rule, $parameters)
	{
		return str_replace(':foo', $parameters[0], $message);
	}

如果你想要增加一個自訂訊息 "replacer" 但不擴展 `Validator` 類別，你可以使用 `Validator::replacer` 方法：

	Validator::replacer('rule', function($message, $attribute, $rule, $parameters)
	{
		//
	});
