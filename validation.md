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

So, what if the incoming request parameters do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors will automatically be [flashed to the session](/docs/{{version}}/session#flash-data).

Again, notice that we did not have to explicitly bind the error messages to the view in our `GET` route. This is because Laravel will check for errors in the session data, and automatically bind them to the view if they are available. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages).

> {tip} The `$errors` variable is bound to the view by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. **When this middleware is applied an `$errors` variable will always be available in your views**, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used.

So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view:

    <!-- /resources/views/post/create.blade.php -->

    <h1>Create Post</h1>

    @if ($errors->any())
        <div class="alert alert-danger">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <!-- Create Post Form -->

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

If you would like to add an "after" hook to a form request, you may use the `withValidator` method. This method receives the fully constructed validator, allowing you to call any of its methods before the validation rules are actually evaluated:

    /**
     * Configure the validator instance.
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
### Authorizing Form Requests

The form request class also contains an `authorize` method. Within this method, you may check if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update:

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        $comment = Comment::find($this->route('comment'));

        return $comment && $this->user()->can('update', $comment);
    }

Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below:

    Route::post('comment/{comment}');

If the `authorize` method returns `false`, a HTTP response with a 403 status code will automatically be returned and your controller method will not execute.

If you plan to have authorization logic in another part of your application, return `true` from the `authorize` method:

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

> {tip} You may type-hint any dependencies you need within the `authorize` method's signature. They will automatically be resolved via the Laravel [service container](/docs/{{version}}/container).

<a name="customizing-the-error-messages"></a>
### Customizing The Error Messages

You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages:

    /**
     * Get the error messages for the defined validation rules.
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
## Manually Creating Validators

If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/{{version}}/facades). The `make` method on the facade generates a new validator instance:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Validator;

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

The first argument passed to the `make` method is the data under validation. The second argument is the validation rules that should be applied to the data.

After checking if the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`.

<a name="automatic-redirection"></a>
### Automatic Redirection

If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the requests's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an AJAX request, a JSON response will be returned:

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validate();

<a name="named-error-bags"></a>
### Named Error Bags

If you have multiple forms on a single page, you may wish to name the `MessageBag` of errors, allowing you to retrieve the error messages for a specific form. Pass a name as the second argument to `withErrors`:

    return redirect('register')
                ->withErrors($validator, 'login');

You may then access the named `MessageBag` instance from the `$errors` variable:

    {{ $errors->login->first('email') }}

<a name="after-validation-hook"></a>
### After Validation Hook

The validator also allows you to attach callbacks to be run after validation is completed. This allows you to easily perform further validation and even add more error messages to the message collection. To get started, use the `after` method on a validator instance:

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
## Working With Error Messages

After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class.

#### Retrieving The First Error Message For A Field

To retrieve the first error message for a given field, use the `first` method:

    $errors = $validator->errors();

    echo $errors->first('email');

#### Retrieving All Error Messages For A Field

If you need to retrieve an array of all the messages for a given field, use the `get` method:

    foreach ($errors->get('email') as $message) {
        //
    }

If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character:

    foreach ($errors->get('attachments.*') as $message) {
        //
    }

#### Retrieving All Error Messages For All Fields

To retrieve an array of all messages for all fields, use the `all` method:

    foreach ($errors->all() as $message) {
        //
    }

#### Determining If Messages Exist For A Field

The `has` method may be used to determine if any error messages exist for a given field:

    if ($errors->has('email')) {
        //
    }

<a name="custom-error-messages"></a>
### Custom Error Messages

If needed, you may use custom error messages for validation instead of the defaults. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method:

    $messages = [
        'required' => 'The :attribute field is required.',
    ];

    $validator = Validator::make($input, $rules, $messages);

In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example:

    $messages = [
        'same'    => 'The :attribute and :other must match.',
        'size'    => 'The :attribute must be exactly :size.',
        'between' => 'The :attribute value :input is not between :min - :max.',
        'in'      => 'The :attribute must be one of the following types: :values',
    ];

#### Specifying A Custom Message For A Given Attribute

Sometimes you may wish to specify a custom error message only for a specific field. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule:

    $messages = [
        'email.required' => 'We need to know your e-mail address!',
    ];

<a name="localization"></a>
#### Specifying Custom Messages In Language Files

In most cases, you will probably specify your custom messages in a language file instead of passing them directly to the `Validator`. To do so, add your messages to `custom` array in the `resources/lang/xx/validation.php` language file.

    'custom' => [
        'email' => [
            'required' => 'We need to know your e-mail address!',
        ],
    ],

#### Specifying Custom Attributes In Language Files

If you would like the `:attribute` portion of your validation message to be replaced with a custom attribute name, you may specify the custom name in the `attributes` array of your `resources/lang/xx/validation.php` language file:

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
## Available Validation Rules

Below is a list of all available validation rules and their function:

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

The field under validation must be _yes_, _on_, _1_, or _true_. This is useful for validating "Terms of Service" acceptance.

<a name="rule-active-url"></a>
#### active_url

The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function.

<a name="rule-after"></a>
#### after:_date_

The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function:

    'start_date' => 'required|date|after:tomorrow'

Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date:

    'finish_date' => 'required|date|after:start_date'

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule.

<a name="rule-alpha"></a>
#### alpha

The field under validation must be entirely alphabetic characters.

<a name="rule-alpha-dash"></a>
#### alpha_dash

The field under validation may have alpha-numeric characters, as well as dashes and underscores.

<a name="rule-alpha-num"></a>
#### alpha_num

The field under validation must be entirely alpha-numeric characters.

<a name="rule-array"></a>
#### array

The field under validation must be a PHP `array`.

<a name="rule-bail"></a>
#### bail

Stop running validation rules after the first validation failure.

<a name="rule-before"></a>
#### before:_date_

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

<a name="rule-between"></a>
#### between:_min_,_max_

The field under validation must have a size between the given _min_ and _max_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

<a name="rule-boolean"></a>
#### boolean

The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`.

<a name="rule-confirmed"></a>
#### confirmed

The field under validation must have a matching field of `foo_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

<a name="rule-date"></a>
#### date

The field under validation must be a valid, non-relative date according to the `strtotime` PHP function.

<a name="rule-date-equals"></a>
#### date_equals:_date_

The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function.

<a name="rule-date-format"></a>
#### date_format:_format_

The field under validation must match the given _format_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class.

<a name="rule-different"></a>
#### different:_field_

The field under validation must have a different value than _field_.

<a name="rule-digits"></a>
#### digits:_value_

The field under validation must be _numeric_ and must have an exact length of _value_.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

The field under validation must have a length between the given _min_ and _max_.

<a name="rule-dimensions"></a>
#### dimensions

The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters:

    'avatar' => 'dimensions:min_width=100,min_height=200'

Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

A _ratio_ constraint should be represented as width divided by height. This can be specified either by a statement like `3/2` or a float like `1.5`:

    'avatar' => 'dimensions:ratio=3/2'

Since this rule requires several arguments, you may use the `Rule::dimensions` method to fluently construct the rule:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'avatar' => [
            'required',
            Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
        ],
    ]);

<a name="rule-distinct"></a>
#### distinct

When working with arrays, the field under validation must not have any duplicate values.

    'foo.*.id' => 'distinct'

<a name="rule-email"></a>
#### email

The field under validation must be formatted as an e-mail address. Under the hood, this validation rule makes use of the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default the `RFCValidation` validator is applied, but you can apply other validation styles as well:

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

The field under validation must exist on a given database table.

#### Basic Usage Of Exists Rule

    'state' => 'exists:states'

If the `column` option is not specified, the field name will be used.

#### Specifying A Custom Column Name

    'state' => 'exists:states,abbreviation'

Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name using "dot" syntax:

    'email' => 'exists:connection.staff,email'

If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them:

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

The field under validation must be a successfully uploaded file.

<a name="rule-filled"></a>
#### filled

The field under validation must not be empty when it is present.

<a name="rule-gt"></a>
#### gt:_field_

The field under validation must be greater than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-gte"></a>
#### gte:_field_

The field under validation must be greater than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-image"></a>
#### image

The file under validation must be an image (jpeg, png, bmp, gif, svg, or webp)

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule:

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'zones' => [
            'required',
            Rule::in(['first-zone', 'second-zone']),
        ],
    ]);

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

The field under validation must exist in _anotherfield_'s values.

<a name="rule-integer"></a>
#### integer

The field under validation must be an integer.

> {note} This validation rule does not verify that the input is of the "integer" variable type, only that the input is a string or numeric value that contains an integer.

<a name="rule-ip"></a>
#### ip

The field under validation must be an IP address.

#### ipv4

The field under validation must be an IPv4 address.

#### ipv6

The field under validation must be an IPv6 address.

<a name="rule-json"></a>
#### json

The field under validation must be a valid JSON string.

<a name="rule-lt"></a>
#### lt:_field_

The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-lte"></a>
#### lte:_field_

The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the `size` rule.

<a name="rule-max"></a>
#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

The file under validation must match one of the given MIME types:

    'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'

To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client provided MIME type.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

#### Basic Usage Of MIME Rule

    'photo' => 'mimes:jpeg,bmp,png'

Even though you only need to specify the extensions, this rule actually validates against the MIME type of the file by reading the file's contents and guessing its MIME type.

A full listing of MIME types and their corresponding extensions may be found at the following location: [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

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

The field under validation may be `null`. This is particularly useful when validating primitive such as strings and integers that can contain `null` values.

<a name="rule-numeric"></a>
#### numeric

The field under validation must be numeric.

<a name="rule-present"></a>
#### present

The field under validation must be present in the input data but can be empty.

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
