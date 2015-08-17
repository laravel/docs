# Eloquent：修改器

- [簡介](#introduction)
- [存取器和修改器](#accessors-and-mutators)
- [日期轉換器](#date-mutators)
- [屬性型別轉換](#attribute-casting)

<a name="introduction"></a>
## 簡介

當你從模型取得集合或是設定他們的值，存取器和修改器可以讓你格式化 Eloquent 屬性。例如，你可能想使用 [Laravel 加密](/docs/{{version}}/encryption)來加密一個值而同時儲存在資料庫中，然後當你從一個 Eloquent 模型存取時可以自動的解密該屬性。

除了在自訂的存取器和修改器外，Eloquent 會自動將日期欄位型別轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 實例或甚至可以將 [文字欄位型別轉換成 JSON](#attribute-casting)。

<a name="accessors-and-mutators"></a>
## 存取器和修改器

#### 定義一個存取器

若要定義一個存取器，在你的模型建立一個 `getFooAttribute` 方法，而且你希望存取的 `Foo` 欄位是一個「駝峰式」大小寫的命名。在這個範例中，我們將對 `first_name` 屬性定義一個存取器。當 Eloquent 嘗試取得 `first_name` 的數值時，存取器將會自動的被呼叫：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Get the user's first name.
         *
         * @param  string  $value
         * @return string
         */
        public function getFirstNameAttribute($value)
        {
            return ucfirst($value);
        }
    }

如你所見的，原始欄位的值已經傳送給存取器，讓你可以操作和回傳數值。如果要存取被修改的值，你可以簡單的存取 `first_name` 屬性：

    $user = App\User::find(1);

    $firstName = $user->first_name;

#### 定義一個修改器

若要定義一個修改器，在你的模型上定義一個 `setFooAttribute` 方法，而且你希望存取的 `Foo` 欄位是一個「駝峰式」大小寫的命名。所以，讓我們再一次定義 `first_name` 屬性的修改器。當我們嘗試在模型上設定 `first_name` 的數值時，修改器將會自動的被呼叫：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Set the user's first name.
         *
         * @param  string  $value
         * @return string
         */
        public function setFirstNameAttribute($value)
        {
            $this->attributes['first_name'] = strtolower($value);
        }
    }

修改器會取得已經被設定的屬性數值，讓你可以在 Eloquent 模型內部操作和設定 `$attributes` 的屬性。所以，舉個例子，如果我們嘗試將 `first_name` 屬性設定成 `Sally`：

    $user = App\User::find(1);

    $user->first_name = 'Sally';

在這個範例，`setFirstNameAttribute` 函式將會呼叫的值 `Sally`。修改器將會使用 `strtolower` 函式來命名數值以及設定數值到內部的 `$attributes` 陣列。

<a name="date-mutators"></a>
## 日期轉換器

預設情況下，Eloquent 將會把 `created_at` 和 `updated_at` 欄位轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 的實例，提供了各式各樣的有效方法，和繼承了 PHP 原生 `DateTime` 的類別。

你可以在你的模型中自訂那些欄位可以自動地被修改，和甚至完全禁止被修改，只要覆寫 `$dates` 屬性：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be mutated to dates.
         *
         * @var array
         */
        protected $dates = ['created_at', 'updated_at', 'disabled_at'];
    }

當某個欄位被認為是日期，你可以將數值設定成一個 UNIX 時間戳記、日期字串（`Y-m-d`）、日期時間（ date-time ）字串、當然還有 `DateTime` 或 `Carbon` 實例，然後日期數值會自動正確的儲存到你的資料庫中：

    $user = App\User::find(1);

    $user->disabled_at = Carbon::now();

    $user->save();

如上面所述，在你的 `$dates` 屬性中列出取得的屬性，他們將自動轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 實例，讓你可以在你的屬性上使用任何的 Carbon 方法：

    $user = App\User::find(1);

    return $user->disabled_at->getTimestamp();

如果你想要自訂你自己的時間戳記格式，在你的模型中設定 `$dateFormat` 屬性。這個屬性定義了時間屬性該如何被儲存到資料庫，以及模型被序列化成一個陣列或 JSON 時的格式：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * The storage format of the model's date columns.
         *
         * @var string
         */
        protected $dateFormat = 'U';
    }

<a name="attribute-casting"></a>
## 屬性型別轉換

`$casts` 屬性在你的模型中提供了方便的方法將屬性轉換為常見的資料類型。`$casts` 屬性應該是一個陣列，而且關鍵是在那些名稱需要被轉換，而這些數值類型是你想要轉換的欄位。支援的型別轉換的類型有：`integer`、`real`、`float`、`double`、`string`、`boolean`、`object` 和 `array`。

例如，讓我們轉換 `is_admin` 屬性，這是在我們的資料庫中儲存整數（0 或 1）為布林值：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be casted to native types.
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

現在當你存取 `is_admin` 屬性將會被轉換成布林值，即使儲存在資料庫的底層數值是一個整數：

    $user = App\User::find(1);

    if ($user->is_admin) {
        //
    }

#### 陣列型別轉換

如果原本欄位是被儲存的為序列化的 JSON 時，那麼 `array` 型別轉換將會非常有用。例如，如果你的資料庫有一個 `TEXT` 類型包含了序列化的 JSON，當你存取你的 Eloquent 模型時，通過增加 `array` 型別轉換， 當取得這個屬性的時候會自動反序列化成 PHP 的陣列：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be casted to native types.
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

一旦型別轉換被定義，你可以存取 `options` 屬性而且它會自動地從 JSON 反序列化成一個 PHP 陣列。當你設定 `options` 屬性的值，給定的陣列將會自動的序列化變回成 JSON 再儲存：

    $user = App\User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();
