# 驗證

- [簡介](#introduction)
- [驗證快速上手](#validation-quickstart)
    - [定義路由](#quick-defining-the-routes)
    - [建立控制器](#quick-creating-the-controller)
    - [撰寫驗證邏輯](#quick-writing-the-validation-logic)
    - [顯示驗證錯誤](#quick-displaying-the-validation-errors)
    - [AJAX 請求和驗證](#quick-ajax-requests-and-validation)
- [其他驗證的處理](#foo)
    - [手動建立驗證程式](#manually-creating-validators)
    - [表單要求驗證](#form-request-validation)
- [處理錯誤訊息](#working-with-error-messages)
    - [自訂錯誤訊息](#custom-error-messages)
- [可用的驗證規則](#available-validation-rules)
- [依條件增加規則](#conditionally-adding-rules)
- [自訂驗證規則](#custom-validation-rules)

<a name="introduction"></a>
## 簡介

Laravel 提供了各種不同的處理方法來驗證應用程式傳入進來的資料。預設情況下，Laravel 的基底控制器類別使用了 `ValidatesRequests` trait，提供了一種方便的方法來驗證傳入的 HTTP 要求和各種強大的驗證規則。

<a name="validation-quickstart"></a>
## 驗證快速上手

要了解有關 Laravel 強大的驗證特色，讓我們來看看一個完整的表單驗證範例以及回傳錯誤訊息給使用者。

<a name="quick-defining-the-routes"></a>
#### 定義路由

首先，讓我們假設我們有下列路由定義在我們的 `app/Http/routes.php` 檔案裡：

    // 顯示一個建立部落格文章的表單...
    Route::get('post/create', 'PostController@create');

    // 儲存一個新的部落格文章...
    Route::post('post', 'PostController@store');

當然，`GET` 路由會顯示使用者用於建立一個新的部落格文章的表單，同時 `POST` 路由會儲存新的部落格文章到資料庫。

<a name="quick-creating-the-controller"></a>
#### 建立控制器

接下來，讓我們看看一個簡單的控制器來操作這些路由。我們現在先讓 `store` 方法為空的：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * 顯示建立部落格文章的表單。
         *
         * @return Response
         */
        public function create()
        {
            return view('post.create');
        }

        /**
         * 儲存一個新的部落格文章。
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            // Validate and store the blog post...
        }
    }

<a name="quick-writing-the-validation-logic"></a>
#### 撰寫驗證邏輯

現在我們準備填寫我們的 `store` 的邏輯方法來驗證我們部落格發佈的新文章。檢查你的應用程式的基底控制器 (`App\Http\Controllers\Controller`) 類別，你會看到這個類別使用了 `ValidatesRequests` trait。這個 trait 在你所有的控制器裡提供了方便的 `validate` 驗證方法。

`validate` 方法接受 HTTP 傳入的請求以及驗證的規則。假設通過驗證規則，你的程式碼可以正常的執行；但是，如果驗證失敗，會拋出異常錯誤訊息自動回傳給使用者。在傳統的 HTTP 請求情況下，會產生一個重導回應，對於 AJAX 請求則發送 JSON 回應。

為了更能夠理解 `validate` 方法，讓我們先回到 `store` 方法：

    /**
     * 儲存一個新的部落格文章。
     *
     * @param  Request  $request
     * @return Response
     */
    public function store(Request $request)
    {
        $this->validate($request, [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        // The blog post is valid, store in database...
    }

正如你所看到的，我們簡單的傳遞當次 HTTP 請求及所需的驗證規則至 `validate` 方法中。再提醒一次，如果驗證失敗，將會自動產生一個對應的回應。如果通過驗證，那我們的控制器會繼續正常的執行。

#### 對於巢狀屬性的提醒

如果你的 HTTP 請求包含了「巢狀」參數，你可以在驗證規則中使用「點」語法指定他們：

    $this->validate($request, [
        'title' => 'required|unique:posts|max:255',
        'author.name' => 'required',
        'author.description' => 'required',
    ]);

<a name="quick-displaying-the-validation-errors"></a>
#### 顯示驗證錯誤

所以，如果當次請求的參數未通過我們給定的驗證規則呢？正如前面所提到的，Laravel 會自動把使用者重導到先前的位置。另外，所有的驗證錯誤會被自動[快閃至 session](/docs/{{version}}/session#flash-data)。

同樣的，注意我們不需要在 `GET ` 路由明確的綁定錯誤訊息至視圖。這是因為 Laravel 會自動檢查 session 內的錯誤資料，如果錯誤存在的話，會自動綁定這些錯誤訊息到視圖。**所以，請注意到 `$errors` 變數在每次請求的所有視圖中都將可以使用**，讓你可以方便假設 `$errors` 變數已被定義且可以安全地使用。`$errors` 變數是 `Illuminate\Support\MessageBag` 的實例。有關此物件的詳細資訊，[請查閱它的文件](#working-with-error-messages)。

所以，在我們的範例中，當驗證失敗，使用者將被重導到我們的控制器 `create` 方法，讓我們在視圖中顯示錯誤的訊息：

    <!-- /resources/views/post/create.blade.php -->

    <h1>建立文章</h1>

    @if (count($errors) > 0)
        <div class="alert alert-danger">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <!-- 建立文章的表單 -->

<a name="quick-customizing-the-flashed-error-format"></a>
#### 自訂快閃的錯誤訊息格式

當驗證失敗時，假設你想要自訂驗證的錯誤格式到你的閃存，覆寫 `formatValidationErrors` 在你的控制器裡。別忘了將 `Illuminate\Contracts\Validation\Validator` 類別引入到檔案的上方：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Foundation\Bus\DispatchesJobs;
    use Illuminate\Contracts\Validation\Validator;
    use Illuminate\Routing\Controller as BaseController;
    use Illuminate\Foundation\Validation\ValidatesRequests;

    abstract class Controller extends BaseController
    {
        use DispatchesJobs, ValidatesRequests;

        /**
         * {@inheritdoc}
         */
        protected function formatValidationErrors(Validator $validator)
        {
            return $validator->errors()->all();
        }
    }

<a name="quick-ajax-requests-and-validation"></a>
### AJAX 請求和驗證

在這個範例中，我們用一種傳統形式將資料發送到應用程式。然而，許多應用程式使用 AJAX 請求。當我們使用 `validate` 方法在 AJAX 的請求中，Laravel 不會產生一個重導的回應。相反的，Laravel 會產生一個包含所有錯誤驗證的 JSON 回應。這個 JSON 回應會傳送一個 422 HTTP 的狀態碼。

<a name="other-validation-approaches"></a>
## 其他驗證的處理

<a name="manually-creating-validators"></a>
### 手動建立驗證程式

如果你不想要使用 `ValidatesRequests` trait 的 `validate` 方法，你可以手動建立一個 validator 實例透過 `Validator::make` 方法在 [facade](/docs/{{version}}/facades) 產生一個新的 validator 實例：

    <?php

    namespace App\Http\Controllers;

    use Validator;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * Store a new blog post.
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $validator = Validator::make($request->all(), [
                'title' => 'required|unique:posts|max:255',
                'body' => 'required',
            ]);

            if ($validator->fails()) {
                return redirect('post/create')
                            ->withErrors($validator)
                            ->withInput();
            }

            // Store the blog post...
        }
    }

第一個參數傳給 `make` 方法是根據資料的驗證。第二個參數應該應用在資料的驗證規則。

在確認之後，假設要求沒有通過驗證， 你可以使用 `withErrors` 方法把錯誤訊息閃存到 session。使用這個方法時，在重導之後，`$errors` 變數可以自動的共用在你的視圖中，讓你輕鬆地顯示這些訊息並回傳給使用者。`withErrors` 方法接受 validator、`MessageBag`，或者是 PHP `array`。

#### 命名錯誤清單

假如在一個頁面中有許多的表單，你可能希望為 `MessageBag` 的錯誤命名。這可以讓你取得特定表單的所有錯誤訊息，只要在 `withErrors` 的第二個參數設定名稱即可：

    return redirect('register')
                ->withErrors($validator, 'login');

然後你就可以從一個 `$errors` 變數中，取得已命名的 `MessageBag` 實例：

    {{ $errors->login->first('email') }}

#### 驗證後的掛勾

在驗證完成之後，validator 可以讓你附加回傳訊息。可以讓你更簡單的做更進一步的驗證以及增加更多的錯誤訊息讓訊息變成一個集合。在 validator 實例使用 `after` 方法作為開始：

    $validator = Validator::make(...);

    $validator->after(function($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add('field', 'Something is wrong with this field!');
        }
    });

    if ($validator->fails()) {
        //
    }

<a name="form-request-validation"></a>
### 表單請求驗證

在更複雜的驗證情境中，你可能會想建立一個「表單請求（ form request ）」。表單請求是一個自訂的請求類別，裡面包含驗證的邏輯。要建立一個表單請求類別，使用 Artisan 命令列指令 `make:request` ：

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
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ];
    }

所以，驗證的規則會如何被執行？你所需要的只有在控制器方法，利用型別提示傳入請求。進入的請求會在控制器方法被呼叫前進行驗證，意思說你不會因為驗證邏輯而把控制器弄得一團糟：

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

假設驗證失敗，會產生一個重導回應把使用者返回到先前的位置。這些錯誤會被閃存到 session，所以這些錯誤都可以被顯示。如果進來的是 AJAX 請求的話，而是會傳回一個 HTTP 回應，包含 422 狀態碼，並包含驗證錯誤的 JSON 資料。

#### 授權表單請求

表單的請求類別內包含了 `authorize` 方法。在這個方法中，你可以確認使用者是否真的通過授權，可以更新特定資料。打個比方，當一個使用者試圖更新部落格文章的評論，他確實是這篇評論的擁有者嗎？例如：

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

注意到上面範例中呼叫 `route` 的方法。這個方法可以幫助你，取得路由被呼叫時傳入的 URI 參數，像是如下範例的 `{comment}` 參數：

    Route::post('comment/{comment}');

如果 `authorize` 方法回傳 `false`，會自動回傳一個 HTTP 回應，包含 403 狀態碼， 而你的控制器方法將不會被執行。

如果你打算在應用程式的其他部分處理授權邏輯，只要從 `authorize` 方法回傳 `true` ：

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

#### 自訂閃存的錯誤訊息格式

如果你想要自訂驗證失敗時，閃存到 session 的驗證錯誤的格式， 在你的基底要求 (`App\Http\Requests\Request`) 覆寫 `formatErrors`。別忘了檔案上方要引入 `Illuminate\Contracts\Validation\Validator` 類別：

    /**
     * {@inheritdoc}
     */
    protected function formatErrors(Validator $validator)
    {
        return $validator->errors()->all();
    }

<a name="working-with-error-messages"></a>
## 處理錯誤訊息

呼叫一個 `Validator` 實例的 `errors` 方法，會得到一個 `Illuminate\Support\MessageBag` 的實例，裡面有許多方便的方法讓你操作錯誤訊息。

#### 查看特定欄位的第一個錯誤訊息

如果要查看特定欄位的第一個錯誤訊息，可以使用 `first` 方法：

    $messages = $validator->errors();

    echo $messages->first('email');

#### 查看特定欄位的所有錯誤訊息

如果你想要簡單得到一個所有的訊息陣列在特定的欄位，可以使用 `get` 方法：

    foreach ($messages->get('email') as $message) {
        //
    }

#### 查看所有欄位的所有錯誤訊息

如果你想要得到所有欄位的訊息陣列，可以使用 `all` 方法：

    foreach ($messages->all() as $message) {
        //
    }

#### 判斷特定欄位是否有錯誤訊息

    if ($messages->has('email')) {
        //
    }

#### 取得格式化後的錯誤訊息

    echo $messages->first('email', '<p>:message</p>');

#### 取得所有格式化後的錯誤訊息

    foreach ($messages->all('<li>:message</li>') as $message) {
        //
    }

<a name="custom-error-messages"></a>
### 自訂錯誤訊息

如果有需要，你可以自訂錯誤的驗證訊息來取代預設的驗證訊息。有幾種方法可以來自訂指定的訊息。首先，你需要先自訂驗證訊息，透過三個參數傳到 `Validator::make` 的方法：

    $messages = [
        'required' => 'The :attribute field is required.',
    ];

    $validator = Validator::make($input, $rules, $messages);

在這個範例中，`:attribute` 透過驗證欄位的的實際名稱，預留的欄位會被取代。你還可以使用其他預設欄位的驗證訊息。例如：

    $messages = [
        'same'    => 'The :attribute and :other must match.',
        'size'    => 'The :attribute must be exactly :size.',
        'between' => 'The :attribute must be between :min - :max.',
        'in'      => 'The :attribute must be one of the following types: :values',
    ];

#### 指定自訂訊息到特定的屬性

有時候你可能想要對特定的欄位自訂錯誤訊息。在你的屬性名稱後，加上「.」符號，並加上指定驗證的規則：

    $messages = [
        'email.required' => 'We need to know your e-mail address!',
    ];

<a name="localization"></a>
#### 在語系檔中自訂指定訊息

在許多情況下，你可能希望在語系檔中，被指定的特定屬性的自訂訊息不是被直接傳到 `Validator `。所以把你的訊息加入到 `resources/lang/xx/validation.php` 語言檔中的 `custom` 陣列。

    'custom' => [
        'email' => [
            'required' => 'We need to know your e-mail address!',
        ],
    ],

<a name="available-validation-rules"></a>
## 可用的驗證規則

以下是所有可用的驗證規則清單與功能：

<style>
    .collection-method-list {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">
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
- [JSON](#rule-json)
- [Max](#rule-max)
- [MIME Types (File)](#rule-mimes)
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
</div>

<a name="rule-accepted"></a>
#### accepted

驗證欄位值是否為 _yes_、_on_、_1_、或 _true_。這在確認「服務條款」是否同意時很有用。

<a name="rule-active-url"></a>
#### active_url

驗證欄位值是否為一個有效的網址，會透過 PHP 的 `checkdnsrr` 函式來驗證。

<a name="rule-after"></a>
#### after:_date_

驗證欄位是否是在指定日期之後。這個日期將會透過 `strtotime` 函式驗證。

    'start_date' => 'required|date|after:tomorrow'

Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date:

    'finish_date' => 'required|date|after:start_date'

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

驗證欄位必須是一個 PHP `array`。

<a name="rule-before"></a>
#### before:_date_

驗證欄位是否是在指定日期之前。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-between"></a>
#### between:_min_,_max_

驗證欄位值的大小是否介於指定的 _min_ 和 _max_之間。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

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

驗證欄位值符合定義的日期 _格式_，透過 PHP 的 `date_parse_from_format` 函式驗證。

<a name="rule-different"></a>
#### different:_field_

驗證欄位值是否和指定的 _欄位（ field ）_ 不同。

<a name="rule-digits"></a>
#### digits:_value_

驗證欄位值為 _數字_ 且長度為 _value_。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

驗證欄位值的長度在 _min_ 和 _max_ 之間。

<a name="rule-email"></a>
#### email

驗證欄位值符合 e-mail 格式。

<a name="rule-exists"></a>
#### exists:_table_,_column_

驗證欄位值存在指定的資料表中。

#### Exists 規則的基本使用方法

    'state' => 'exists:states'

#### 指定一個特定的欄位名稱

    'state' => 'exists:states,abbreviation'

也可以指定更多的條件，它們會被加到 "where" 查詢語句裡：

    'email' => 'exists:staff,email,account_id,1'

如果傳入 "where" 語句的查詢值是 `NULL` ，會確認查詢條件的值是否為 `NULL`：

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

<a name="rule-json"></a>
#### json

The field under validation must a valid JSON string.

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

驗證欄位值的大小是否小於或等於 _value_。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

驗證欄位值不在給定的清單裡。

<a name="rule-numeric"></a>
#### numeric

驗證欄位值是否為數值。

<a name="rule-regex"></a>
#### regex:_pattern_

驗證欄位值符合給定的正規表示式。

**注意：** 當使用 `regex`  pattern 時，你必須使用陣列，而不該用管線分隔規則，especially if the regular expression contains a pipe character.

<a name="rule-required"></a>
#### required

驗證輸入資料裏有此欄位。

<a name="rule-required-if"></a>
#### required_if:_field_,_value_,...

如果指定 _欄位（ field ）_ 的等於任何一個 _value_，則此欄位為必填。

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

如果指定的欄位之中，_任一_ 個有值，則此欄位為必填。

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

驗證欄位值的大小需符合給定 _value_ 值。對於字串來說， _value_ 為字元數。對於數字來說， _value_ 為某個整數值。對檔案來說， _size_ 對應到的是檔案大小（單位 kb ）。

<a name="rule-string"></a>
#### string

驗證欄位值的型別是否為字串。

<a name="rule-timezone"></a>
#### timezone

驗證欄位值是個有效的時區，會根據 PHP 的 `timezone_identifiers_list` 函式來判斷。

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

在給定的資料表，驗證欄位中必須是唯一的。如果沒有指定 `column`，將會使用欄位本身的名稱。

**指定一個特定的欄位名稱：**

    'email' => 'unique:users,email_address'

**自訂資料庫連線**

有時候你可能需要自訂一個連線，透過 Validator 對資料庫進行查詢。如上面所示，設定 `unique:users` 作為驗證規則，透過預設資料庫連線來做資料庫查詢。如果要覆寫驗證規則，將指定的連線後在表單名稱後加上「.」：

    'email' => 'unique:connection.users,email_address'

**強迫 Unique 規則忽略特定 ID：**

有時候，你希望在驗證欄位的時候，忽略給定的 ID。例如，在「更新個人資料」時包含使用者名稱、信箱等等。當然，需要先驗證 e-mail 是否為唯一的。因為使用者只能更改名稱欄位而不是 e-mail 欄位，你不需要去驗證錯誤，因為 e-mail 已經是這個使用者的擁有者。假設使用者提供的 e-mail 已經被不同的使用者使用，你需要拋出驗證錯誤。用特定的規則來忽略使用者 ID，你應該把傳送 ID 當作第三個參數：

    'email' => 'unique:users,email_address,'.$user->id

**增加額外的 Where 查詢：**

也可以指定更多的條件到 "where" 查詢語句：

    'email' => 'unique:users,email_address,NULL,id,account_id,1'

上述規則中，只有 `account_id` 為 `1` 的資料列會被包含在 unique 規則的驗證。

<a name="rule-url"></a>
#### url

驗證欄位值必須符合 URL 格式，根據 PHP 的 `filter_var` 函式。

<a name="conditionally-adding-rules"></a>
## 依條件增加規則

在某些情況下，你可能 **只想** 在輸入資料中有此欄位時，才進行驗證。只要增加 `sometimes` 規則到進規則列表，就可以快速達成：

    $v = Validator::make($data, [
        'email' => 'sometimes|required|email',
    ]);

在上面的範例中，`email` 欄位的驗證，只會在 `$data` 陣列有此欄位才會進行。

#### 複雜的條件驗證

有時候你可能希望增加更複雜的驗證條件，例如，你可以希望某個指定欄位，在另一個欄位的值有超過 100 時才為必填。或者你當某個指定欄位有值時，另外兩個欄位要符合特定值。增加這樣的驗證條件並不痛苦。首先，利用你熟悉的 _static rules_ 建立一個 `Validator` 實例：

    $v = Validator::make($data, [
        'email' => 'required|email',
        'games' => 'required|numeric',
    ]);

假設我們的網頁應用程式是專為遊戲收藏家所設計。如果遊戲收藏家收藏超過一百款遊戲，我們希望他們說明為什麼他們擁有這麼多遊戲。像是，可能他們經營一家二手遊戲商店，或是他們可能只是享受收集的樂趣。為了在特定條件下，加入此驗證需求，我們可以在 `Validator` 實例使用 `sometimes` 方法。

    $v->sometimes('reason', 'required|max:500', function($input) {
        return $input->games >= 100;
    });

傳入 `sometimes` 方法的第一個參數，是我們要依條件認證的欄位名稱。第二個參數是我們想加入驗證規則。`閉包 (Closure)` 作為第三個參數傳入，如果其回傳 `true` 額外的規則就會被加入。這個方法可以輕鬆的建立複雜的條件式驗證。你甚至可以一次對多個欄位增加條件式驗證：

    $v->sometimes(['reason', 'cost'], 'required', function($input) {
        return $input->games >= 100;
    });

> **注意：** 傳入 `Closure` 的 `$input` 參數是 `Illuminate\Support\Fluent` 實例，可以用來作為取得你的輸入和檔案的物件。

<a name="custom-validation-rules"></a>
## 自訂驗證規則

Laravel 提供了很多有用的驗證規則；但是，你可能希望自訂一些規則。註冊自訂的驗證規則的方法之一，就是使用 `Validator::extend` 方法 [facade](/docs/{{version}}/facades) 讓我們使用這個方法在 [服務提供者](/docs/{{version}}/providers) 來自訂註冊的驗證規則：

    <?php

    namespace App\Providers;

    use Validator;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Validator::extend('foo', function($attribute, $value, $parameters) {
                return $value == 'foo';
            });
        }

        /**
         * Register the service provider.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

自訂的驗證閉包接收三個參數：要被驗證的屬性名稱 `$attribute`，屬性的值 `$value`，傳入驗證規則的參數陣列 `$parameters`。

除了使用閉包，你也可以傳入類別和方法到 `extend` 方法中：

    Validator::extend('foo', 'FooValidator@validate');

#### 自訂錯誤訊息

在你的自訂的規則中，需要定義錯誤訊息。你可以自訂訊息陣列或是在驗證語系檔中加入新的規則。這個訊息應該被放在第一個級別的陣列，而不是放在 `custom` 陣列， 這是僅對特定屬性的錯誤訊息:

    "foo" => "Your input was invalid!",

    "accepted" => "The :attribute must be accepted.",

    // The rest of the validation error messages...

當你在建立自訂的驗證規則時，你可能需要定義保留欄位來取代錯誤訊息。你可以建立自訂的 Validator ，像上面所描述的透過 `Validator` facade 來使用 `replacer` 的方法。你可以透過 [服務提供者](/docs/{{version}}/providers) 中的 `boot` 方法這麼做：

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Validator::extend(...);

        Validator::replacer('foo', function($message, $attribute, $rule, $parameters) {
            return str_replace(...);
        });
    }
