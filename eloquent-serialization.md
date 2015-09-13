# Eloquent: 序列化

- [簡介](#introduction)
- [基本用法](#basic-usage)
- [隱藏來自 JSON 的屬性](#hiding-attributes-from-json)
- [添加一些值到 JSON](#appending-values-to-json)

<a name="introduction"></a>
## 簡介

當你在建立 JSON APIs 的時候，經常需要將模型和關聯轉換成陣列或是 JSON。Eloquent 提供了一些方便的方法讓我們可以做這些轉換，以及控制哪些屬性要包括在你的序列化中。

<a name="basic-usage"></a>
## 基本用法

#### 將模型轉換成一個陣列

如果要將模型還有它載入的[關聯](/docs/{{version}}/eloquent-relationships)轉換成一個陣列，你可以使用 `toArray` 方法。這個方法是遞迴的，因此，所有屬性和所有關聯（包含關聯中的關聯）都會被轉換成陣列：

    $user = App\User::with('roles')->first();

    return $user->toArray();

你也可以將[集合](/docs/{{version}}/eloquent-collections)轉換成陣列：

    $users = App\User::all();

    return $users->toArray();

#### 將模型轉換成 JSON

如果要將模型轉換成 JSON，你可以使用 `toJson` 方法。如同 `toArray`，`toJson` 方法也是遞迴的，所以，所有的屬性以及關聯都將被轉換成 JSON：

    $user = App\User::find(1);

    return $user->toJson();

或者，你可以強制把一個模型或集合轉型成一個字串，它將會自動的呼叫 `toJson` 方法：

    $user = App\User::find(1);

    return (string) $user;

當模型或集合被轉型成字串時，會轉換成 JSON 格式，所以你可以直接從應用程式的路由或者控制器回傳 Eloquent 物件：

    Route::get('users', function () {
        return App\User::all();
    });

<a name="hiding-attributes-from-json"></a>
## 隱藏來自 JSON 的屬性

有時候你可能會想要限制包含在模型陣列或 JSON 表示法的屬性，像是密碼。要達成這個目地，你可以在模型中增加 `$hidden` 屬性定義：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 應該在陣列中隱藏的屬性。
         *
         * @var array
         */
        protected $hidden = ['password'];
    }

> **注意：**當你要隱藏關聯時，要使用關聯的**方法**名稱，而不是它的動態屬性的名稱。

另外，你也可以使用 `visible` 屬性定義應該包含在你的模型陣列和 JSON 表示法中的屬性白名單：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 應該在陣列中可見的屬性。
         *
         * @var array
         */
        protected $visible = ['first_name', 'last_name'];
    }

<a name="appending-values-to-json"></a>
## 添加一些值到 JSON

有時候，你可能需要添加在資料庫沒有對應欄位的陣列屬性。要達成這個目地，首先必須為這個值定義一個[存取器](/docs/{{version}}/eloquent-mutators)：

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

一旦你建立了存取器，就可以把將屬性名稱添加到模型中的 `appends` 屬性：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 存取器被附加到模型陣列的形式。
         *
         * @var array
         */
        protected $appends = ['is_admin'];
    }

一旦屬性被添加到 `appends` 清單，在模型的陣列和 JSON 兩種形式都將會包含進去。在 `appends` 陣列中的屬性也遵循模型中 `visible` 和 `hidden` 的設定。
