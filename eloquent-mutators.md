# Eloquent：修改器

- [簡介](#introduction)
- [存取器和修改器](#accessors-and-mutators)
- [日期轉換器](#date-mutators)
- [屬性型別轉換](#attribute-casting)

<a name="introduction"></a>
## 簡介

當你從模型取得 Eloquent 的屬性或是設定它們的值，存取器和修改器可以讓你格式化它們。例如，你可能想要使用 [Laravel 加密器](/docs/{{version}}/encryption)來加密一個被儲存在資料庫中的值，而在你從 Eloquent 模型存取該屬性時可以自動的解密它。

除了自訂的存取器和修改器外，Eloquent 也會自動將日期欄位型別轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 實例或甚至將[文字欄位型別轉換成 JSON](#attribute-casting)。

<a name="accessors-and-mutators"></a>
## 存取器和修改器

#### 定義一個存取器

若要定義一個存取器，必須在你的模型上建立一個 `getFooAttribute` 方法，而且你希望存取的 `Foo` 欄位需使用「駝峰式」的方式命名。在這個範例中，我們將對 `first_name` 屬性定義一個存取器。當 Eloquent 嘗試取得 `first_name` 的值時，將會自動的呼叫存取器：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 取得使用者的名字。
         *
         * @param  string  $value
         * @return string
         */
        public function getFirstNameAttribute($value)
        {
            return ucfirst($value);
        }
    }

如你所見的，欄位原始的值被傳遞到存取器，讓你可以操作並回傳結果。如果要存取被修改的值，你可以簡單的存取 `first_name` 屬性：

    $user = App\User::find(1);

    $firstName = $user->first_name;

#### 定義一個修改器

若要定義一個修改器，必須在你的模型上定義一個 `setFooAttribute` 方法，而且你希望存取的 `Foo` 欄位需使用「駝峰式」的方式命名。所以，讓我們再一次定義 `first_name` 屬性的修改器。當我們嘗試在模型上設定 `first_name` 的值時，將會自動的呼叫修改器：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 設定使用者的名字。
         *
         * @param  string  $value
         * @return string
         */
        public function setFirstNameAttribute($value)
        {
            $this->attributes['first_name'] = strtolower($value);
        }
    }

修改器會取得屬性已經被設定的值，讓你可以操作該值並設定到 Eloquent 模型內部的 `$attributes` 屬性。所以，舉個例子，如果我們嘗試將 `first_name` 屬性設定成 `Sally`：

    $user = App\User::find(1);

    $user->first_name = 'Sally';

在這個範例中，`setFirstNameAttribute` 函式會使用 `Sally` 當參數呼叫。修改器會對該名字使用 `strtolower` 函式並將值設置於內部的 `$attributes` 陣列。

<a name="date-mutators"></a>
## 日期轉換器

預設情況下，Eloquent 將會把 `created_at` 和 `updated_at` 欄位轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 的實例，它提供了各式各樣有用的方法，並繼承了 PHP 原生的 `DateTime` 類別。

你可以在你的模型中自訂哪些欄位要自動地被修改，或甚至完全禁止修改，只要藉由覆寫模型的 `$dates` 屬性：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         *  應該應用日期轉換的屬性。
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

預設來說，時間戳記將會以 `'Y-m-d H:i:s'` 格式化。如果你想要自訂你自己的時間戳記格式，在你的模型中設定 `$dateFormat` 屬性。這個屬性定義了時間屬性該如何被儲存到資料庫，以及模型被序列化成一個陣列或 JSON 時的格式：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 模型的資料欄位的儲存格式。
         *
         * @var string
         */
        protected $dateFormat = 'U';
    }

<a name="attribute-casting"></a>
## 屬性型別轉換

`$casts` 屬性在你的模型中提供了方便的方法將屬性轉換為常見的資料類型。`$casts` 屬性應該是一個陣列，而鍵是那些需要被轉換的屬性名稱，而值則是代表你想要把欄位轉換成什麼類型。支援的型別轉換的類型有：`integer`、`real`、`float`、`double`、`string`、`boolean`、`object` 和 `array`。

例如，`is_admin` 屬性以整數（0 或 1）被儲存在我們的資料庫中，讓我們把它轉換為布林值：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 應該被轉換成原生型別的屬性。
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

現在當你存取 `is_admin` 屬性時，它將會總是被轉換成布林值，即使儲存在資料庫裡面的值是一個整數：

    $user = App\User::find(1);

    if ($user->is_admin) {
        //
    }

#### 陣列型別轉換

如果原本欄位儲存的為被序列化的 JSON 時，那麼 `array` 型別轉換將會特別的有用。例如，如果你的資料庫有一個 `TEXT` 欄位型別包含了被序列化的 JSON，而且對該屬性添加了 `array` 型別轉換，當你在 Eloquent 模型上存取該屬性時，它會自動被反序列化成一個 PHP 的陣列：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 應該被轉換成原生型別的屬性。
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

一旦型別轉換被定義，你可以存取 `options` 屬性而它會自動地從 JSON 反序列化成一個 PHP 陣列。當你設定 `options` 屬性的值，給定的陣列將會自動的被序列化變回成 JSON 以進行儲存：

    $user = App\User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();
