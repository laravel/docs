# Eloquent: Serialization

- [簡介](#introduction)
- [基本用法](#basic-usage)
- [隱藏來自 JSON 的屬性](#hiding-attributes-from-json)
- [附加數值到 JSON](#appending-values-to-json)

<a name="introduction"></a>
## 簡介

當建立一個 JSON APIs的時候，你經常需要將模型和關聯轉換成陣列或是 JSON。Eloquent 提供了方便的方法讓我們可以做這些轉換，以及包括在你的序列化中需要控制的屬性。

<a name="basic-usage"></a>
## 基本用法

#### 將模型轉換成一個陣列

如果要將模型還有載入的[關聯](/docs/{{version}}/eloquent-relationships)轉換成一個陣列，你可以使用 `toArray` 方法。這個方法是遞迴的，因此，所有屬性和所有關聯（包含關聯中的關聯）將會被轉換成陣列：

    $user = App\User::with('roles')->first();

    return $user->toArray();

你還可以將[集合](/docs/{{version}}/eloquent-collections)轉換成陣列：

    $users = App\User::all();

    return $users->toArray();

#### 將模型轉換成 JSON

如果要將模型轉換成 JSON，你可以使用 `toJson` 方法。像是 `toArray`、`toJson` 的方法是遞迴的，所以，所有的屬性以及關聯都將被轉換成 JSON：

    $user = App\User::find(1);

    return $user->toJson();

或者，你可以強制把一個模型或集合變成一個字串，他將會自動的呼叫 `toJson` 方法：

    $user = App\User::find(1);

    return (string) $user;

當模型或集合被轉換成字串時，會轉換成 JSON 格式，你可以直接從應用路由或者控制器回傳 Eloquent 物件：

    Route::get('users', function () {
        return App\User::all();
    });

<a name="hiding-attributes-from-json"></a>
## 隱藏來自 JSON 的屬性

有時候你可能會想要限制出現在模型陣列或 JSON 表達式的屬性資料，像是密碼。你可以在模型中增加 `$hidden` 屬性定義：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * hidden 屬性應該是一個陣列。
         *
         * @var array
         */
        protected $hidden = ['password'];
    }

> **注意：** 當你要隱藏關聯的資料，要使用關聯 **方法** 的名稱，而不是動態屬性的名稱。

另外，你也可以使用 `visible` 屬性在你的模型陣列和 JSON 表達式中定義白名單：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * visible 屬性應該是一個陣列。
         *
         * @var array
         */
        protected $visible = ['first_name', 'last_name'];
    }

<a name="appending-values-to-json"></a>
## 附加數值到 JSON

有時候，你可能需要增加不存在的資料庫欄位的陣列屬性。首先定義一個[存取器](/docs/{{version}}/eloquent-mutators)的值：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 為使用者取得管理者的標記。
         *
         * @return bool
         */
        public function getIsAdminAttribute()
        {
            return $this->attributes['admin'] == 'yes';
        }
    }

一旦你建立了存取器，將屬性名稱增加到模型中的 `appends` 屬性：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 存取器被附加到模型的陣列形式。
         *
         * @var array
         */
        protected $appends = ['is_admin'];
    }

一旦屬性被增加到 `appends` 清單，在模型中將會包含陣列和 JSON 兩種形式。在 `appends` 陣列中的屬性也遵循模型中 `visible` 和 `hidden` 的設定。
