# 驗證

- [介紹](#introduction)
- [驗證快速上手](#validation-quickstart)
    - [定義路由](#quick-defining-the-routes)
    - [建立控制器](#quick-creating-the-controller)
    - [撰寫驗證邏輯](#quick-writing-the-validation-logic)
    - [顯示驗證錯誤](#quick-displaying-the-validation-errors)
    - [關於可選欄位的說明](#a-note-on-optional-fields)
- [表單請求驗證](#form-request-validation)
    - [建立表單請求](#creating-form-requests)
    - [授權表單請求](#authorizing-form-requests)
    - [自訂錯誤訊息](#customizing-the-error-messages)
    - [自訂驗證參數](#customizing-the-validation-attributes)
- [手動建立驗證器](#manually-creating-validators)
    - [自動重導](#automatic-redirection)
    - [命名錯誤清單](#named-error-bags)
    - [驗證後的掛勾](#after-validation-hook)
- [處理錯誤訊息](#working-with-error-messages)
    - [自訂錯誤訊息](#custom-error-messages)
- [可用的驗證規則](#available-validation-rules)
- [依條件增加規則](#conditionally-adding-rules)
- [驗證陣列](#validating-arrays)
- [自訂驗證規則](#custom-validation-rules)
    - [使用規則物件](#using-rule-objects)
    - [Using Closures](#using-closures)
    - [使用擴充功能](#using-extensions)
    - [Implicit Extensions](#implicit-extensions)

<a name="introduction"></a>
## 介紹

Laravel 提供多種方法來驗證應用程式傳入的資料。預設情況下，Laravel 的基底控制器利用 `ValidatesRequests` trait 提供的一個便利的方法和各種強大的驗證規則來驗證傳入的 HTTP 請求。

<a name="validation-quickstart"></a>
## 驗證快速上手

要了解 Laravel 強大的驗證特性，讓我們來看一個驗證表單並顯示錯誤訊息給使用者的完整範例。

<a name="quick-defining-the-routes"></a>
### 定義路由

首先，假設我們在 `routes/web.php` 檔案中定義了下列的路由：

    Route::get('post/create', 'PostController@create');

    Route::post('post', 'PostController@store');

`GET` 路由會顯示讓使用者新增部落格文章的表單，而 `POST` 路由會儲存部落格新文章到資料庫。

<a name="quick-creating-the-controller"></a>
### 建立控制器

Next, let's take a look at a simple controller that handles these routes. We'll leave the `store` method empty for now:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class PostController extends Controller
    {
        /**
         * 顯示建立部落格新文章的表單。
         *
         * @return Response
         */
        public function create()
        {
            return view('post.create');
        }

        /**
         * 儲存一篇部落格新文章。
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            // 驗證並儲存部落格文章...
        }
    }

<a name="quick-writing-the-validation-logic"></a>
### 撰寫驗證邏輯

現在我們可以把驗證部落格新文章的邏輯寫進 `store` 方法中了。我們會使用 `Illuminate\Http\Request` 物件提供的 `validate` 方法來實現驗證。如果通過驗證規則，程式會繼續正常執行；如果驗證失敗，會拋出一個例外並把適當的錯誤訊息回傳給使用者。在傳統的 HTTP 請求中，會產生一個重導回應，對於 AJAX 請求則發送 JSON 回應。

為了更理解 `validate` 方法，我們先回到 `store` 方法中：

    /**
     * 儲存一篇部落格新文章。
     *
     * @param  Request  $request
     * @return Response
     */
    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        // 部落格文章通過驗證⋯
    }

如你所見，我們單純的把所需的驗證規則傳進 `validate` 方法中。再次提醒，如果驗證失敗，會自動產生適當的回應。如果驗證通過，控制器會繼續正常執行。

另外，驗證規則除了用 `|` 分隔開的字串之外，也可以用陣列傳入：

    $validatedData = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

#### 在首次驗證失敗時停止驗證

有時候你會希望在一個屬性首次驗證失敗時，停止此屬性的其他驗證規則。把 `bail` 規則指派到屬性中來達成目的：

    $request->validate([
        'title' => 'bail|required|unique:posts|max:255',
        'body' => 'required',
    ]);

在這個範例中，如果 `title` 屬性的 `unique` 規則驗證失敗，就不會檢查 `max` 規則。驗證的順序會依照規則指派的順序。

#### 關於巢狀屬性的提醒

如果 HTTP 請求包含了「巢狀」參數，可以在驗證規則中使用「點」語法來指定屬性：

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'author.name' => 'required',
        'author.description' => 'required',
    ]);

<a name="quick-displaying-the-validation-errors"></a>
### 顯示驗證錯誤


那麼當傳入的要求參數沒有通過指定的驗證規則呢？如之前提到，Laravel 會自動把使用者導回先前的位置。另外，所有的驗證錯誤會自動[快閃到 session](/docs/{{version}}/session#flash-data)。

注意到我們在 `GET` 路由中不需要明確地綁定錯誤訊息到視圖。這是因為 Laravel 會自動檢查 session 內的錯誤資料，如果錯誤存在的話，會自動綁定這些錯誤訊息到視圖。`$errors` 變數會是 `Illuminate\Support\MessageBag` 的實例。有關此物件的詳細資訊，[請查閱它的文件](#working-with-error-messages)。

> {tip} `$errors` 變數透過 `web` 中介層群組提供的 `Illuminate\View\Middleware\ShareErrorsFromSession` 中介層綁定到視圖。**當應用這個中介層時，視圖中會永遠存在一個可用的 `$errors` 變數**，你可以方便的假設 `$errors` 變數總是有被定義且可以安全使用。

在我們的範例中，驗證失敗時會將使用者重導到控制器的 `create` 方法，讓我們可以在這個視圖中顯示錯誤訊息：

    <!-- /resources/views/post/create.blade.php -->

    <h1>新增文章</h1>

    @if ($errors->any())
        <div class="alert alert-danger">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <!-- 新增文章表單 -->

#### `@error` 指示

You may also use the `@error` [Blade](/docs/{{version}}/blade) directive to quickly check if validation error messages exist for a given attribute. Within an `@error` 指示，you may echo the `$message` variable to display the error message:

    <!-- /resources/views/post/create.blade.php -->

    <label for="title">Post Title</label>

    <input id="title" type="text" class="@error('title') is-invalid @enderror">

    @error('title')
        <div class="alert alert-danger">{{ $message }}</div>
    @enderror

<a name="a-note-on-optional-fields"></a>
### 關於可選欄位的說明

Laravel 預設會在全域的中介層堆疊中加入 `TrimStrings` 和 `ConvertEmptyStringsToNull` 中介層。`App\Http\Kernel` 類別中列出了堆疊內的中介層。因此，如果你不想讓驗證器認為 `null` 值無效，你通常會需要把「可選」的請求欄位標註為 `nullable`。例如：

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
        'publish_at' => 'nullable|date',
    ]);

在這個範例中，我們指定 `publish_at` 欄位可以為 `null` 或一個有效的日期表示。如果沒有把 `nullable` 修飾字加到規則定義中，驗證器會認為 `null` 是無效的日期。

<a name="quick-ajax-requests-and-validation"></a>
#### AJAX 請求和驗證

在這個範例中，我們使用傳統的表單來發送資料給應用程式。然而，許多應用程式是利用 AJAX 請求。在 AJAX 請求時使用 `validate` 方法，Laravel 不會產生重導回應。而是會產生一個包含所有驗證錯誤的 JSON 回應。此 JSON 回應會包含 422 HTTP 狀態碼。

<a name="form-request-validation"></a>
## 表單請求驗證

<a name="creating-form-requests"></a>
### 建立表單請求

在更複雜的驗證情境中，你可能會想建立一個「表單請求」。表單請求是一種自訂的請求類別，其中包含驗證邏輯。使用 Artisan 命令列指令 `make:request` 來建立一個表單請求類別：

    php artisan make:request StoreBlogPost

新產生的類別檔會放在 `app/Http/Requests` 目錄下。如果目錄不存在，會在執行 `make:request` 時建立。讓我們加入一些驗證規則到 `rules` 方法中：

    /**
     * 取得適用於請求的驗證規則
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

> {tip} You may type-hint any dependencies you need within the `rules` method's signature. They will automatically be resolved via the Laravel [service container](/docs/{{version}}/container).

那驗證的規則會如何執行呢？只需要在控制器方法中，為請求加上型別提示。傳入的表單請求會在控制器方法被呼叫前進行驗證，也就是說不會因為驗證邏輯而把控制器弄得一團亂：

    /**
     * 儲存傳入的部落格文章。
     *
     * @param  StoreBlogPost  $request
     * @return Response
     */
    public function store(StoreBlogPost $request)
    {
        // 有效的傳入請求⋯

        // 取得驗證過的輸入資料⋯
        $validated = $request->validated();
    }

如果驗證失敗，會產生一個重導回應把使用者導回先前的位置。這些錯誤會被快閃至 session，讓錯誤都可以被顯示。如果是 AJAX 請求，則會傳回包含 422 狀態碼及驗證錯誤的 JSON 資料的 HTTP 回應。

#### 為表單請求加上驗證後的掛勾

如果想要為表單請求加上「驗證後」的掛勾，可以利用 `withValidator` 方法。這個方法接收完整建構的驗證器，讓你可以在驗證規則實際被執行前呼叫驗證器的任何方法：

    /**
     * 設定驗證器實例。
     *
     * @param  \Illuminate\Validation\Validator  $validator
     * @return void
     */
    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add('field', 'Something is wrong with this field!');
            }
        });
    }

<a name="authorizing-form-requests"></a>
### 授權表單請求

表單請求類別也包含了 `authorize` 方法。在這個方法中，你可以確認使用者是否真的有權限可以更新特定資料。舉個例子，當一個使用者嘗試更新部落格文章的評論時，可以先判斷這是否是他的評論？例如：

    /**
     * 判斷使用者是否有權限做出此請求。
     *
     * @return bool
     */
    public function authorize()
    {
        $comment = Comment::find($this->route('comment'));

        return $comment && $this->user()->can('update', $comment);
    }

因為所有的表單請求都是繼承 Laravel 基底的請求類別，我們可以利用 `user` 方法來存取當下認證的使用者。同時注意到上面範例中有呼叫 `route` 方法。這個方法讓你可以取得呼叫路由時的 URI 參數，像是如下範例的 `{comment}` 參數：

    Route::post('comment/{comment}');

如果 `authorize` 方法回傳 `false`，會自動回傳一個包含 403 狀態碼的 HTTP 回應，且不會執行控制器方法。

如果你打算在應用程式的其他部分處理授權邏輯，只需讓 `authorize` 方法回傳 `true`：

    /**
     * 判斷使用者是否有權限做出此請求。
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

> {tip} You may type-hint any dependencies you need within the `authorize` method's signature. They will automatically be resolved via the Laravel [service container](/docs/{{version}}/container).

<a name="customizing-the-error-messages"></a>
### 自訂錯誤訊息


你可以透過覆寫表單請求的 `messages` 方法來自定錯誤訊息。此方法必須回傳一個包含成對的屬性與規則及對應錯誤訊息的陣列：

    /**
     * 取得已定義驗證規則的錯誤訊息。
     *
     * @return array
     */
    public function messages()
    {
        return [
            'title.required' => 'A title is required',
            'body.required'  => 'A message is required',
        ];
    }

<a name="customizing-the-validation-attributes"></a>
### Customizing The Validation Attributes

If you would like the `:attribute` portion of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs:

    /**
     * Get custom attributes for validator errors.
     *
     * @return array
     */
    public function attributes()
    {
        return [
            'email' => 'email address',
        ];
    }

<a name="manually-creating-validators"></a>
## 手動建立驗證器

如果你不想要用請求的 `validate` 方法，你可以透過 `Validator` [facade](/docs/{{version}}/facades) 來建立驗證器實例。Facade 中的 `make` 方法會產生一個新的驗證器實例。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Validator;

    class PostController extends Controller
    {
        /**
         * 儲存部落格新文章。
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

            // 儲存部落格文章...
        }
    }

傳給 `make` 方法的第一個參數是需要被驗證的資料。第二個參數是資料使用的驗證規則。

檢查請求是否有驗證通過後，你可以使用 `withErrors` 方法把錯誤訊息快閃到 session。使用這個方法，在重導之後 `$errors` 變數可以自動的在視圖中共用，讓你輕鬆地顯示這些訊息給使用者。`withErrors` 方法接受驗證器、`MessageBag`，或是 PHP `array`。

<a name="automatic-redirection"></a>
### 自動重導

如果在手動建立驗證器的同時，仍然想利用請求的 `validate` 方法所提供的自動重導，你可以呼叫現有的驗證器實體的 `validate` 方法。如果驗證失敗，使用者會被自動重導，或在 AJAX 請求時回傳 JSON 回應：

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validate();

<a name="named-error-bags"></a>
### 命名錯誤清單

假如在一個頁面中有多個表單，你可能希望為每個錯誤的 `MessageBag` 命名，這樣就可以取得特定表單的錯誤訊息。只要在 `withErrors` 的第二個參數傳入名稱即可：

    return redirect('register')
                ->withErrors($validator, 'login');

再來就可以從 `$errors` 變數中取得已命名的 `MessageBag` 實例：

    {{ $errors->login->first('email') }}

<a name="after-validation-hook"></a>
### 驗證後的掛勾

驗證器可以附加回呼以在驗證完成後執行。可以讓你更簡單的做進一步驗證甚至在錯誤訊息集合中增加更多錯誤訊息。在驗證器實例使用 `after` 方法即可：

    $validator = Validator::make(...);

    $validator->after(function ($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add('field', 'Something is wrong with this field!');
        }
    });

    if ($validator->fails()) {
        //
    }

<a name="working-with-error-messages"></a>
## 處理錯誤訊息

呼叫 `Validator` 實例的 `errors` 方法，會得到一個 `Illuminate\Support\MessageBag `的實例，其中有許多方便的方法讓你處理錯誤訊息。在所有視圖中共用的 `$errors` 變數就是 `MessageBag` 類別的實例。

#### 取出特定欄位的第一個錯誤訊息

使用 `first` 方法來取出特定欄位的第一個錯誤訊息：

    $errors = $validator->errors();

    echo $errors->first('email');

#### 取出特定欄位的所有錯誤訊息

使用 `get` 方法來取出特定欄位所有訊息的陣列：

    foreach ($errors->get('email') as $message) {
        //
    }

如果你驗證的表單欄位是個陣列，可以用 `*` 字元來取出每個陣列元素的訊息：

    foreach ($errors->get('attachments.*') as $message) {
        //
    }

#### 取出所有欄位的所有錯誤訊息

使用 `all` 方法來取出所有欄位的所有錯誤訊息：

    foreach ($errors->all() as $message) {
        //
    }

#### 判斷特定欄位是否有錯誤訊息

使用 `has` 方法來判斷特定欄位是否有錯誤訊息：

    if ($errors->has('email')) {
        //
    }

<a name="custom-error-messages"></a>
### 自訂錯誤訊息

如果有需要，你可以自訂驗證的錯誤訊息來取代預設的錯誤訊息。有數種指定自訂訊息的方法。第一種，把自訂的訊息傳到 `Validator::make` 方法的第三個參數：

    $messages = [
        'required' => 'The :attribute field is required.',
    ];

    $validator = Validator::make($input, $rules, $messages);

在這個範例中，`:attribute` 佔位符會被驗證時實際的欄位名稱給取代。也有其他的佔位符可以在驗證訊息中使用。例如：

    $messages = [
        'same'    => 'The :attribute and :other must match.',
        'size'    => 'The :attribute must be exactly :size.',
        'between' => 'The :attribute value :input is not between :min - :max.',
        'in'      => 'The :attribute must be one of the following types: :values',
    ];

#### 指定自訂訊息給特定的屬性

有時候你可能想要對特定的欄位自訂錯誤訊息。在你的屬性名稱後加上「.」符號，並加上指定的驗證規則：

    $messages = [
        'email.required' => 'We need to know your e-mail address!',
    ];

<a name="localization"></a>
#### 在語系檔中指定自訂訊息

在大部分情況下，你可能會希望在語系檔中指定自訂的訊息，而不是被直接傳進 `Validator`。把訊息加到 `resources/lang/xx/validation.php` 語言檔中的 `custom` 陣列來達成目的。

    'custom' => [
        'email' => [
            'required' => 'We need to know your e-mail address!',
        ],
    ],

#### 在語系檔中指定自訂屬性

如果你想把驗證訊息裡的 `:attribute` 取代成自訂的屬性名稱，可以在 `resources/lang/xx/validation.php` 語言檔中的 `attributes` 陣列來指定名稱：

    'attributes' => [
        'email' => 'email address',
    ],

#### Specifying Custom Values In Language Files

Sometimes you may need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`:

    $request->validate([
        'credit_card_number' => 'required_if:payment_type,cc'
    ]);

If this validation rule fails, it will produce the following error message:

    The credit card number field is required when payment type is cc.

Instead of displaying `cc` as the payment type value, you may specify a custom value representation in your `validation` language file by defining a `values` array:

    'values' => [
        'payment_type' => [
            'cc' => 'credit card'
        ],
    ],

Now if the validation rule fails it will produce the following message:

    The credit card number field is required when payment type is credit card.

<a name="available-validation-rules"></a>
## 可用的驗證規則

以下是所有可用的驗證規則與功能：

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Active URL](#rule-active-url)
[After (Date)](#rule-after)
[After Or Equal (Date)](#rule-after-or-equal)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Array](#rule-array)
[Bail](#rule-bail)
[Before (Date)](#rule-before)
[Before Or Equal (Date)](#rule-before-or-equal)
[Between](#rule-between)
[Boolean](#rule-boolean)
[Confirmed](#rule-confirmed)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[E-Mail](#rule-email)
[Ends With](#rule-ends-with)
[Exists (Database)](#rule-exists)
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Image (File)](#rule-image)
[In](#rule-in)
[In Array](#rule-in-array)
[Integer](#rule-integer)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Not In](#rule-not-in)
[Not Regex](#rule-not-regex)
[Nullable](#rule-nullable)
[Numeric](#rule-numeric)
[Present](#rule-present)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#conditionally-adding-rules)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[URL](#rule-url)
[UUID](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted

驗證欄位值是否為 _yes_、_on_、_1_、或 _true_。這在確認是否同意「服務條款」時很有用。

<a name="rule-active-url"></a>
#### active_url

透過 PHP 的 `dns_get_record` 函式來驗證欄位是否為有效的 A 或 AAAA 紀錄。

<a name="rule-after"></a>
#### after:_date_

驗證欄位是否是在指定日期之後的值。這個日期會透過 PHP `strtotime` 函式驗證。

    'start_date' => 'required|date|after:tomorrow'

或者指定另一個用來比較的日期欄位，而不是透過傳給 `strtotime` 的字串：

    'finish_date' => 'required|date|after:start_date'

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

驗證欄位是否在指定日期之後或同一天。更多資訊請參考 [after](#rule-after) 規則。

<a name="rule-alpha"></a>
#### alpha

驗證欄位值是否僅包含字母字元。

<a name="rule-alpha-dash"></a>
#### alpha_dash

驗證欄位值是否僅包含字母、數字、破折號（ - ）以及底線（ _ ）。

<a name="rule-alpha-num"></a>
#### alpha_num

驗證欄位值是否僅包含字母及數字。

<a name="rule-array"></a>
#### array

驗證欄位必須是一個 PHP `array`。

<a name="rule-bail"></a>
#### bail

Stop running validation rules after the first validation failure.

<a name="rule-before"></a>
#### before:_date_

驗證欄位是否是在指定日期之前。這個日期會透過 PHP `strtotime` 函式驗證。 In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

驗證欄位是否在指定日期之前或同一天。這個日期會透過 PHP `strtotime` 函式驗證。 In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

<a name="rule-between"></a>
#### between:_min_,_max_

驗證欄位值的大小是否介於指定的 _min_ 和 _max_ 之間。字串、數值、陣列和檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-boolean"></a>
#### boolean

驗證欄位值必須能夠轉型為布林值。可接受的輸入為 `true`、`false`、`1`、`0`、`"1"` 以及 `"0"`。

<a name="rule-confirmed"></a>
#### confirmed

驗證欄位值必須和對應的 `foo_confirmation` 欄位值相同。例如，如果要驗證 `password` 欄位，必須和輸入資料裡的 `password_confirmation` 欄位值相同。

<a name="rule-date"></a>
#### date

驗證欄位值是有效的日期，會透過 PHP 的 `strtotime` 函式驗證。

<a name="rule-date-equals"></a>
#### date_equals:_date_

驗證欄位是否與指定日期同一天。這個日期會透過 PHP `strtotime` 函式驗證。

<a name="rule-date-format"></a>
#### date_format:_format_

驗證欄位值符合定義的日期格式（ _format_ ）。你應該使用 `date` 或 `date_format` **其一**來驗證欄位，而不是兩者。This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class.

<a name="rule-different"></a>
#### different:_field_

驗證欄位值是否和指定的欄位（ _field_ ）不同。

<a name="rule-digits"></a>
#### digits:_value_

驗證欄位值為長度為 _value_ 的_數字_。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

驗證欄位值的長度必須在 _min_ 和 _max_ 之間。

<a name="rule-dimensions"></a>
#### dimensions

驗證欄位值必須是一張圖片且符合規則參數限制的尺寸：

    'avatar' => 'dimensions:min_width=100,min_height=200'

可用的限制為： _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

_ratio_ 為寬除以高的比例。可以運算式 `3/2` 或浮點數 `1.5` 來表示：

    'avatar' => 'dimensions:ratio=3/2'

由於此規則需要許多參數，你可以用 `Rule::dimensions` 方法來流暢地建構這個規則：

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'avatar' => [
            'required',
            Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
        ],
    ]);

<a name="rule-distinct"></a>
#### distinct

當處理陣列時，驗證欄位中不能有任何重複的值

    'foo.*.id' => 'distinct'

<a name="rule-email"></a>
#### email

驗證欄位必須為一個 e-mail 地址。 Under the hood, this validation rule makes use of the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default the `RFCValidation` validator is applied, but you can apply other validation styles as well:

    'email' => 'email:rfc,dns'

The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply:

<div class="content-list" markdown="1">
- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
</div>

The `filter` validator, which uses PHP's `filter_var` function under the hood, ships with Laravel and is Laravel's pre-5.8 behavior.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

The field under validation must end with one of the given values.

<a name="rule-exists"></a>
#### exists:_table_,_column_

驗證欄位值必須存在一個指定的資料表中。

#### Exists 規則的基本用法

    'state' => 'exists:states'

If the `column` option is not specified, the field name will be used.

#### 指定欄位名稱

    'state' => 'exists:states,abbreviation'

有時候，你可能會指定 `exists` 查詢使用特定的資料庫連線。可以用「點」語法在資料表名稱前加上連線名稱來達成：

    'email' => 'exists:connection.staff,email'

如果想要客制驗證規則執行的查詢，可以用 `Rule` 類別來流暢地定義規則。在這個範例中，我們也會以陣列來表示驗證規則，而不是用 `|` 字元來分割：

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::exists('staff')->where(function ($query) {
                $query->where('account_id', 1);
            }),
        ],
    ]);

<a name="rule-file"></a>
#### file

驗證欄位必須是一個成功上傳的檔案。

<a name="rule-filled"></a>
#### filled

當驗證欄位存在時，不可以為空值。

<a name="rule-gt"></a>
#### gt:_field_

The field under validation must be greater than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-gte"></a>
#### gte:_field_

The field under validation must be greater than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-image"></a>
#### image

驗證欄位檔案必須為圖片格式（ jpeg、png、bmp、gif、svg 或 webp）。

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

驗證欄位必須包含在給定的列表中。由於這個規則經常需要你 `implode` 一個陣列，`Rule::in` 方法可以用來流暢地建構規則：

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'zones' => [
            'required',
            Rule::in(['first-zone', 'second-zone']),
        ],
    ]);

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

驗證欄位的值必須在 _anotherfield_ 陣列中存在。

<a name="rule-integer"></a>
#### integer

驗證欄位必須是一個整數。

> {note} This validation rule does not verify that the input is of the "integer" variable type, only that the input is a string or numeric value that contains an integer.

<a name="rule-ip"></a>
#### ip

驗證欄位必須符合一個 IP 位址的格式。

#### ipv4

驗證欄位必須符合一個 IPv4 位址的格式。

#### ipv6

驗證欄位必須符合一個 IPv6 位址的格式。

<a name="rule-json"></a>
#### json

驗證欄位必須是一個有效的 JSON 字串。

<a name="rule-lt"></a>
#### lt:_field_

The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-lte"></a>
#### lte:_field_

The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-max"></a>
#### max:_value_

驗證欄位值的大小是否小於或等於 _value_。字串、數值和檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

驗證檔案必須符合給定的 MIME 類型之一。

    'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'

為了判斷上傳檔案的 MIME 類型，檔案的內容會被讀取，框架會嘗試猜測 MIME 類型，這可能與客戶端提供的 MIME 類型不同。

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

驗證檔案的 MIME 類型必須符合清單裡的副檔名之一。

#### MIME 規則基本用法

    'photo' => 'mimes:jpeg,bmp,png'

即便只需要指定副檔名，但此規則實際上透過讀取檔案內容，並猜測 MIME 類型來驗證。

完整的 MIME 類型及對應的副檔名清單可以在下方連結找到：[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_

驗證欄位值的大小是否小於或等於 _value_。字串、數值或是檔案大小的計算方式和 [`size`](#rule-size) 規則相同。

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'toppings' => [
            'required',
            Rule::notIn(['sprinkles', 'cherries']),
        ],
    ]);

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

The field under validation must not match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`.

**Note:** When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

<a name="rule-nullable"></a>
#### nullable

驗證欄位值可以為 `null`。在驗證可能含有 `null` 值的基本型別（如字串或整數）時特別有用。

<a name="rule-numeric"></a>
#### numeric

驗證欄位值是否為數值。

<a name="rule-present"></a>
#### present

驗證欄位一定要有值，但可為空值。

<a name="rule-regex"></a>
#### regex:_pattern_

The field under validation must match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`.

**Note:** When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

<a name="rule-required"></a>
#### required

The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_.

If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This methods accepts a boolean or a Closure. When passed a Closure, the Closure should return `true` or `false` to indicate if the field under validation is required:

    use Illuminate\Validation\Rule;

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf($request->user()->is_admin),
    ]);

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf(function () use ($request) {
            return $request->user()->is_admin;
        }),
    ]);

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ any of the other specified fields are present.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ all of the other specified fields are present.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ any of the other specified fields are not present.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ all of the other specified fields are not present.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.

<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value. For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes.

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

The field under validation must start with one of the given values.

<a name="rule-string"></a>
#### string

The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field.

<a name="rule-timezone"></a>
#### timezone

The field under validation must be a valid timezone identifier according to the `timezone_identifiers_list` PHP function.

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

The field under validation must not exist within the given database table.

**Specifying A Custom Column Name:**

The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the field name will be used.

    'email' => 'unique:users,email_address'

**Custom Database Connection**

Occasionally, you may need to set a custom connection for database queries made by the Validator. As seen above, setting `unique:users` as a validation rule will use the default database connection to query the database. To override this, specify the connection and the table name using "dot" syntax:

    'email' => 'unique:connection.users,email_address'

**Forcing A Unique Rule To Ignore A Given ID:**

Sometimes, you may wish to ignore a given ID during the unique check. For example, consider an "update profile" screen that includes the user's name, e-mail address, and location. You will probably want to verify that the e-mail address is unique. However, if the user only changes the name field and not the e-mail field, you do not want a validation error to be thrown because the user is already the owner of the e-mail address.

To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::unique('users')->ignore($user->id),
        ],
    ]);

> {note} You should never pass any user controlled request input into the `ignore` method. Instead, you should only pass a system generated unique ID such as an auto-incrementing ID or UUID from an Eloquent model instance. Otherwise, your application will be vulnerable to an SQL injection attack.

Instead of passing the model key's value to the `ignore` method, you may pass the entire model instance. Laravel will automatically extract the key from the model:

    Rule::unique('users')->ignore($user)

If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method:

    Rule::unique('users')->ignore($user->id, 'user_id')

By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method:

    Rule::unique('users', 'email_address')->ignore($user->id),

**Adding Additional Where Clauses:**

You may also specify additional query constraints by customizing the query using the `where` method. For example, let's add a constraint that verifies the `account_id` is `1`:

    'email' => Rule::unique('users')->where(function ($query) {
        return $query->where('account_id', 1);
    })

<a name="rule-url"></a>
#### url

The field under validation must be a valid URL.

<a name="rule-uuid"></a>
#### uuid

The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID).

<a name="conditionally-adding-rules"></a>
## Conditionally Adding Rules

#### Validating When Present

In some situations, you may wish to run validation checks against a field **only** if that field is present in the input array. To quickly accomplish this, add the `sometimes` rule to your rule list:

    $v = Validator::make($data, [
        'email' => 'sometimes|required|email',
    ]);

In the example above, the `email` field will only be validated if it is present in the `$data` array.

> {tip} If you are attempting to validate a field that should always be present but may be empty, check out [this note on optional fields](#a-note-on-optional-fields)

#### Complex Conditional Validation

Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change:

    $v = Validator::make($data, [
        'email' => 'required|email',
        'games' => 'required|numeric',
    ]);

Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance.

    $v->sometimes('reason', 'required|max:500', function ($input) {
        return $input->games >= 100;
    });

The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is the rules we want to add. If the `Closure` passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once:

    $v->sometimes(['reason', 'cost'], 'required', function ($input) {
        return $input->games >= 100;
    });

> {tip} The `$input` parameter passed to your `Closure` will be an instance of `Illuminate\Support\Fluent` and may be used to access your input and files.

<a name="validating-arrays"></a>
## Validating Arrays

Validating array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so:

    $validator = Validator::make($request->all(), [
        'photos.profile' => 'required|image',
    ]);

You may also validate each element of an array. For example, to validate that each e-mail in a given array input field is unique, you may do the following:

    $validator = Validator::make($request->all(), [
        'person.*.email' => 'email|unique:users',
        'person.*.first_name' => 'required_with:person.*.last_name',
    ]);

Likewise, you may use the `*` character when specifying your validation messages in your language files, making it a breeze to use a single validation message for array based fields:

    'custom' => [
        'person.*.email' => [
            'unique' => 'Each person must have a unique e-mail address',
        ]
    ],

<a name="custom-validation-rules"></a>
## Custom Validation Rules

<a name="using-rule-objects"></a>
### Using Rule Objects

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory:

    php artisan make:rule Uppercase

Once the rule has been created, we are ready to define its behavior. A rule object contains two methods: `passes` and `message`. The `passes` method receives the attribute value and name, and should return `true` or `false` depending on whether the attribute value is valid or not. The `message` method should return the validation error message that should be used when validation fails:

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;

    class Uppercase implements Rule
    {
        /**
         * Determine if the validation rule passes.
         *
         * @param  string  $attribute
         * @param  mixed  $value
         * @return bool
         */
        public function passes($attribute, $value)
        {
            return strtoupper($value) === $value;
        }

        /**
         * Get the validation error message.
         *
         * @return string
         */
        public function message()
        {
            return 'The :attribute must be uppercase.';
        }
    }

You may call the `trans` helper from your `message` method if you would like to return an error message from your translation files:

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return trans('validation.uppercase');
    }

Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules:

    use App\Rules\Uppercase;

    $request->validate([
        'name' => ['required', 'string', new Uppercase],
    ]);

<a name="using-closures"></a>
### Using Closures

If you only need the functionality of a custom rule once throughout your application, you may use a Closure instead of a rule object. The Closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails:

    $validator = Validator::make($request->all(), [
        'title' => [
            'required',
            'max:255',
            function ($attribute, $value, $fail) {
                if ($value === 'foo') {
                    $fail($attribute.' is invalid.');
                }
            },
        ],
    ]);

<a name="using-extensions"></a>
### Using Extensions

Another method of registering custom validation rules is using the `extend` method on the `Validator` [facade](/docs/{{version}}/facades). Let's use this method within a [service provider](/docs/{{version}}/providers) to register a custom validation rule:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Illuminate\Support\Facades\Validator;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Validator::extend('foo', function ($attribute, $value, $parameters, $validator) {
                return $value == 'foo';
            });
        }
    }

The custom validator Closure receives four arguments: the name of the `$attribute` being validated, the `$value` of the attribute, an array of `$parameters` passed to the rule, and the `Validator` instance.

You may also pass a class and method to the `extend` method instead of a Closure:

    Validator::extend('foo', 'FooValidator@validate');

#### Defining The Error Message

You will also need to define an error message for your custom rule. You can do so either using an inline custom message array or by adding an entry in the validation language file. This message should be placed in the first level of the array, not within the `custom` array, which is only for attribute-specific error messages:

    "foo" => "Your input was invalid!",

    "accepted" => "The :attribute must be accepted.",

    // The rest of the validation error messages...

When creating a custom validation rule, you may sometimes need to define custom placeholder replacements for error messages. You may do so by creating a custom Validator as described above then making a call to the `replacer` method on the `Validator` facade. You may do this within the `boot` method of a [service provider](/docs/{{version}}/providers):

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Validator::extend(...);

        Validator::replacer('foo', function ($message, $attribute, $rule, $parameters) {
            return str_replace(...);
        });
    }

<a name="implicit-extensions"></a>
### Implicit Extensions

By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom extensions, are not run. For example, the [`unique`](#rule-unique) rule will not be run against an empty string:

    $rules = ['name' => 'unique:users,name'];

    $input = ['name' => ''];

    Validator::make($input, $rules)->passes(); // true

For a rule to run even when an attribute is empty, the rule must imply that the attribute is required. To create such an "implicit" extension, use the `Validator::extendImplicit()` method:

    Validator::extendImplicit('foo', function ($attribute, $value, $parameters, $validator) {
        return $value == 'foo';
    });

> {note} An "implicit" extension only _implies_ that the attribute is required. Whether it actually invalidates a missing or empty attribute is up to you.

#### Implicit Rule Objects

If you would like a rule object to run when an attribute is empty, you should implement the `Illuminate\Contracts\Validation\ImplicitRule` interface. This interface serves as a "marker interface" for the validator; therefore, it does not contain any methods you need to implement.
