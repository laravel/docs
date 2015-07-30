# Eloquent：關聯

- [簡介](#introduction)
- [定義關聯](#defining-relationships)
    - [一對一](#one-to-one)
    - [一對多](#one-to-many)
    - [多對多](#many-to-many)
    - [遠層一對多](#has-many-through)
    - [多型關聯](#polymorphic-relations)
    - [多型多對多關聯](#many-to-many-polymorphic-relations)
- [關聯查詢](#querying-relations)
    - [預載入](#eager-loading)
    - [預載入條件限制](#constraining-eager-loads)
    - [延遲預載入](#lazy-eager-loading)
- [寫入關聯模型](#inserting-related-models)
    - [多對多關聯](#inserting-many-to-many-relationships)

<a name="introduction"></a>
## 簡介

資料表通常會互相關聯。例如，一篇部落格文章可能有很多評論，或是一張訂單與下單的客戶相關聯。 Eloquent 讓管理和處理這些關聯變得很容易，並支援多種類型的關聯：
Database tables are often related to one another. For example, a blog post may have many comments, or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports several different types of relationships:

- [一對一](#one-to-one)
- [一對多](#one-to-many)
- [多對多](#many-to-many)
- [遠層一對多](#has-many-through)
- [多型關聯](#polymorphic-relations)
- [多型多對多關聯](#many-to-many-polymorphic-relations)

<a name="defining-relationships"></a>
## 定義關聯

你會在你的 Eloquent 模型類別內將 Eloquent 關聯定義為函式。因為像 Eloquent 模型本身，關聯也可以作為強大的[查詢產生器](/docs/{{version}}/queries)，定義關聯為函式提供了強而有力的方法鏈結及查詢功能。例如：
Eloquent relationships are defined as functions on your Eloquent model classes. Since, like Eloquent models themselves, relationships also serve as powerful [query builders](/docs/{{version}}/queries), defining relationships as functions provides powerful method chaining and querying capabilities. For example:

    $user->posts()->where('active', 1)->get();

不過，在深入了解使用關聯之前，先讓我們學期如何定義每個類型：
But, before diving too deep into using relationships, let's learn how to define each type:

<a name="one-to-one"></a>
### 一對一

一對一關聯是很基本的關聯。例如一個 `User` 模型會對應到一個 `Phone`。要定義這種關聯，我們將 `phone` 方法置於 `User` 模型。`phone` 方法會回傳自身 Eloquent 模型類別上 `hasOne` 方法的結果：
A one-to-one relationship is a very basic relation. For example, a `User` model might be associated with one `Phone`. To define this relationship, we place a `phone` method on the `User` model. The `phone` method should return the results of the `hasOne` method on the base Eloquent model class:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 取得與指定使用者互相關聯的電話紀錄。
         */
        public function phone()
        {
            return $this->hasOne('App\Phone');
        }
    }

傳到 hasOne 方法裡的第一個參數是關聯模型的類別名稱。定義好關聯之後，我們就可以使用 Eloquent 的[動態屬性](#dynamic-properties)取得關聯紀錄。動態屬性能夠讓你存取關聯函式，就像他們是在模型中定義的屬性：
The first argument passed to the `hasOne` method is the name of the related model. Once the relationship is defined, we may retrieve the related record using Eloquent's [dynamic properties](#dynamic-properties). Dynamic properties allow you to access relationship functions as if they were properties defined on the model:

    $phone = User::find(1)->phone;

Eloquent 會假設對應的關聯的外鍵名稱是基於模型名稱。在這個例子裡，預設 `Phone` 模型資料表會以 `user_id` 作為外鍵。如果你想要複寫這個慣例，可以傳入第二個參數到 `hasOne` 方法裡。
Eloquent assumes the foreign key of the relationship based on the model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method:

    return $this->hasOne('App\Phone', 'foreign_key');

此外，Eloquent 預設外鍵會在上層模型的 `id` 欄位有個對應值。換句話說，Eloquent 會尋找使用者的 `id` 欄位與 `Phone` 模型的 `user_id` 欄位的值相同的紀錄。如果你想讓關聯使用 `id` 以外的值，你可以傳遞第三個參數至 `hasOne` 方法來指定你自定的鍵：
Additionally, Eloquent assumes that the foreign key should have a value matching the `id` column of the parent. In other words, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a value other than `id`, you may pass a third argument to the `hasOne` method specifying your custom key:

    return $this->hasOne('App\Phone', 'foreign_key', 'local_key');

#### 定義相對的關聯

所以，我們可以從我們的 `User` 存取 `Phone` 模型。現在，讓我們在 `Phone` 模型定義一個關聯，此關聯能夠讓我們存取擁有此電話的 `User`。我們可以定義與 `hasOne` 關聯相對的 `belongsTo` 方法：
So, we can access the `Phone` model from our `User`. Now, let's define a relationship on the `Phone` model that will let us access the `User` the owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Phone extends Model
    {
        /**
         * 取得擁有此電話的使用者。
         */
        public function user()
        {
            return $this->belongsTo('App\User');
        }
    }

在上述例子中，Eloquent 會嘗試匹配 `Phone` 模型的 `user_id` 至 `User` 模型的 `id`。Eloquent 判斷的預設外鍵名稱參考於關聯模型的方法，並在方法名稱後面加上 `_id`。當然，如果 `Phone` 模型的外鍵不是 `user_id`，你可以傳遞自定的鍵名至 `belongsTo` 方法的第二個參數：
In the example above, Eloquent will try to match the `user_id` from the `Phone` model to an `id` on the `User` model. Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method:

    /**
     * 取得擁有此電話的使用者。
     */
    public function user()
    {
        return $this->belongsTo('App\User', 'foreign_key');
    }

如果你的上層模型不是使用 `id` 作為主鍵，或是你希望以不同的欄位 join 下層模型，你可以傳遞第三參數至 `belongsTo` 方法指定上層資料表的自定鍵：
If your parent model does not use `id` as its primary key, or you wish to join the child model to a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key:

    /**
     * 取得擁有此電話的使用者。
     */
    public function user()
    {
        return $this->belongsTo('App\User', 'foreign_key', 'other_key');
    }

<a name="one-to-many"></a>
### 一對多

一個「一對多」關聯使用於定義單一模型擁有其他模型任意數量的關聯。例如，一篇部落格文章可能有無限多筆評論。就像其他的 Eloquent 關聯，一對多關聯的定義是放置一個函式至你的 Eloquent 模型：
A "one-to-many" relationship is used to define relationships where a single model owns any amount of other models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by placing a function on your Eloquent model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Post extends Model
    {
        /**
         * 取得部落格文章的評論。
         */
        public function comments()
        {
            return $this->hasMany('App\Comment');
        }
    }

切記，Eloquent 會自動判斷 `Comment` 模型上正確的外鍵欄位。以慣例來說，Eloquent 會取用自身模型的「蛇底式命名」後的名稱，並在後方加上 `_id`。所以，以此例來說，Eloquent 會假設 `Comment` 模型的外鍵是 `post_id`。
Remember, Eloquent will automatically determine the proper foreign key column on the `Comment` model. By convention, Eloquent will take the "snake case" name of the owning model and suffix it with `_id`. So, for this example, Eloquent will assume the foreign key on the `Comment` model is `post_id`.

一旦關聯被定義之後，我們可以透過 `comments` 屬性存取評論的集合。切記，因為 Eloquent 提供了「動態屬性」，我們可以存取關聯函式，就像他們是在模型中定義的屬性：
Once the relationship has been defined, we can access the collection of comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic properties", we can access relationship functions as if they were defined as properties on the model:

    $comments = App\Post::find(1)->comments;

    foreach ($comments as $comment) {
        //
    }

當然，因為所有的關聯也提供查詢產生器的服務，你可以對取得的評論進一步增加條件，透過呼叫 `comments` 方法，接著在該查詢的後方鏈結上條件：
Of course, since all relationships also serve as query builders, you can add further constraints to which comments are retrieved by calling the `comments` method and continuing to chain conditions onto the query:

    $comments = App\Post::find(1)->comments()->where('title', 'foo')->first();

就像 `hasOne` 方法，你也可以透過傳遞額外的參數至 `hasMany` 方法複寫外鍵與本地鍵：
Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method:

    return $this->hasMany('App\Comment', 'foreign_key');

    return $this->hasMany('App\Comment', 'foreign_key', 'local_key');

#### 定義相對的關聯

現在我們能存取所有文章的評論，讓我們定義一個透過評論存取上層文章的關聯。若要定義相對於 `hasMany` 的關聯，在下層模型定義一個叫做 `belongsTo` 方法的關聯函式：
Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship function on the child model which calls the `belongsTo` method:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Comment extends Model
    {
        /**
         * 取得擁有此評論的文章。
         */
        public function post()
        {
            return $this->belongsTo('App\Post');
        }
    }

一旦關聯被定義之後，我們可以透過 `post`「動態屬性」取得 `Comment` 的 `Post` 模型：
Once the relationship has been defined, we can retrieve the `Post` model for a `Comment` by accessing the `post` "dynamic property":

    $comment = App\Comment::find(1);

    echo $comment->post->title;

在上述例子中，Eloquent 會嘗試匹配 `Comment` 模型的 `post_id` 至 `Post` 模型的 `id`。
Eloquent 判斷的預設外鍵名稱參考於關聯模型的方法，並在方法名稱後面加上 `_id`。當然，如果 `Comment` 模型的外鍵不是 `post_id`，你可以傳遞自定的鍵名至 `belongsTo` 方法的第二個參數：
In the example above, Eloquent will try to match the `post_id` from the `Comment` model to an `id` on the `Post` model. Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. However, if the foreign key on the `Comment` model is not `post_id`, you may pass a custom key name as the second argument to the `belongsTo` method:

    /**
     * 取得擁有此評論的文章。
     */
    public function post()
    {
        return $this->belongsTo('App\Post', 'foreign_key');
    }

如果你的上層模型不是使用 `id` 作為主鍵，或是你希望以不同的欄位 join 下層模型，你可以傳遞第三參數至 `belongsTo` 方法指定上層資料表的自定鍵：
If your parent model does not use `id` as its primary key, or you wish to join the child model to a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key:

    /**
     * Get the post that owns the comment.
     */
    public function post()
    {
        return $this->belongsTo('App\Post', 'foreign_key', 'other_key');
    }

<a name="many-to-many"></a>
### 多對多

多對多關聯稍微比 `hasOne` 及 `hasMany` 關聯還複雜。這種關聯的例子如，一個使用者可能用有很多身份，而一種身份可能很多使用者都有。舉例來說，很多使用者都擁有「管理者」的身份。要定義這種關聯，需要使用三個資料表：`users`、`roles` 和 `role_user`。`role_user` 表命名是以相關聯的兩個模型資料表，依照字母順序命名，並包含了 `user_id` 和 `role_id` 欄位。
Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of such a relationship is a user with many roles, where the roles are also shared by other users. For example, many users may have the role of "Admin". To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names, and contains the `user_id` and `role_id` columns.

多對多關聯的定義是透過撰寫一個在自身 Eloquent 類別呼叫 `belongsToMany` 的方法。舉個例子，讓我們在 `User` 模型定義 `roles` 方法：
Many-to-many relationships are defined by writing a method that calls the `belongsToMany` method on the base Eloquent class. For example, let's define the `roles` method on our `User` model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 屬於該使用者的身份。
         */
        public function roles()
        {
            return $this->belongsToMany('App\Role');
        }
    }

一旦關聯被定義，你可以使用 `roles` 動態屬性存取使用者的身份：
Once the relationship is defined, you may access the user's roles using the `roles` dynamic property:

    $user = App\User::find(1);

    foreach ($user->roles as $role) {
        //
    }

當然，就像所有的其他關聯類型，你可以呼叫 `roles` 方法，接著在該關聯之後鏈結上查詢的條件：
Of course, like all other relationship types, you may call the `roles` method to continue chaining query constraints onto the relationship:

    $roles = App\User::find(1)->roles()->orderBy('name')->get();

如前文所提，若要判斷關聯合併的資料表名稱，Eloquent 會合併兩個關聯模型的名稱並依照字母順序命名。當然你可以很自由的複寫這個慣例。你可以透過傳遞第二個參數至 `belongsToMany` 方法來達成：
As mentioned previously, to determine the table name of the relationship's joining table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method:

    return $this->belongsToMany('App\Role', 'user_roles');

除了自定合併資料表的名稱，你也可以透過傳遞額外參數至 `belongsToMany` 方法來自定資料表裡鍵的欄位名稱。第三個參數是你定義在關聯中的模型的外鍵名稱，而第四個參數則是你要合併的模型中的外鍵名稱：
In addition to customizing the name of the joining table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to:

    return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'role_id');

#### 定義相對的關聯

要定義相對於多對多的關聯，你只需要簡單的放置另一個名為 `belongsToMany` 至你關聯的模型。繼續我們的使用者身份範例，讓我們在 `Role` 模型定義 `users` 方法：
To define the inverse of a many-to-many relationship, you simply place another call to `belongsToMany` on your related model. To continue our user roles example, let's define the `users` method on the `Role` model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Role extends Model
    {
        /**
         * 屬於該身份的使用者
         */
        public function users()
        {
            return $this->belongsToMany('App\User');
        }
    }

如你所見，此定義除了簡單的參考 `App\User` 模型外，與 `User` 的對應完全相同。因為我們重新使用了 `belongsToMany` 方法，當定義相對於多對多的關聯時，所有常用的自定資料表與鍵的選項都是可用的。
As you can see, the relationship is defined exactly the same as its `User` counterpart, with the exception of simply referencing the `App\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the inverse of many-to-many relationships.

#### 取得中介表欄位

如你所知，要操作多對多關聯需要一個中介的資料表。Eloquent 提供了一些有用的方法和這張表互動。例如，假設 `User` 物件關聯到很多 `Role` 物件。存取這些關聯物件時，我們可以在模型使用 `pivot` 屬性存取中介資料表的資料：
As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` object has many `Role` objects that it is related to. After accessing this relationship, we may access the intermediate table using the `pivot` attribute on the models:

    $user = App\User::find(1);

    foreach ($user->roles as $role) {
        echo $role->pivot->created_at;
    }

注意我們取出的每個 `Role` 模型物件，會自動被賦予 `pivot` 屬性。此屬性是代表中介表的模型，且可以像其它的 Eloquent 模型一樣被使用。
Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table, and may be used like any other Eloquent model.

預設來說，`pivot` 物件只提供模型的鍵。如果你的 pivot 資料表包含了其他的屬性，可以在定義關聯方法時指定那些欄位：
By default, only the model keys will be present on the `pivot` object. If your pivot table contains extra attributes, you must specify them when defining the relationship:

    return $this->belongsToMany('App\Role')->withPivot('column1', 'column2');

如果你想要樞紐表自動維護 `created_at` 和 `updated_at` 時間戳，在定義關聯方法時加上 `withTimestamps` 方法：
If you want your pivot table to have automatically maintained `created_at` and `updated_at` timestamps, use the `withTimestamps` method on the relationship definition:

    return $this->belongsToMany('App\Role')->withTimestamps();

<a name="has-many-through"></a>
### 遠層一對多

「遠層一對多」提供了方便簡短的方法，可以透過中介的關聯取得遠層的關聯。例如，一個 `Country` 模型可能透過中介的 `Users` 模型關聯到多個 `Posts` 模型。讓我們看看定義此種關聯的資料表：
The "has-many-through" relationship provides a convenient short-cut for accessing distant relations via an intermediate relation. For example, a `Country` model might have many `Post` models through an intermediate `User` model. In this example, you could easily gather all blog posts for a given country. Let's look at the tables required to define this relationship:

    countries
        id - integer
        name - string

    users
        id - integer
        country_id - integer
        name - string

    posts
        id - integer
        user_id - integer
        title - string

雖然 `posts` 本身不包含 `country_id` 欄位，但 `hasManyThrough` 關聯透過 `$country->posts` 來提供我們存取一個城市的文章。要執行此查詢，Eloquent 會檢查中介表 `users` 的 `country_id`。在找到匹配的使用者 IDs 後，就會在 `posts` 資料表使用它們來查詢。
Though `posts` does not contain a `country_id` column, the `hasManyThrough` relation provides access to a country's posts via `$country->posts`. To perform this query, Eloquent inspects the `country_id` on the intermediate `users` table. After finding the matching user IDs, they are used to query the `posts` table.

現在我們已經檢查了關聯的資料表結構，讓我們將它定義在 `Country` 模型：
Now that we have examined the table structure for the relationship, let's define it on the `Country` model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Country extends Model
    {
        /**
         * 取得該城市的所有文章。
         */
        public function posts()
        {
            return $this->hasManyThrough('App\Post', 'App\User');
        }
    }

傳遞至 `hasManyThrough` 方法的第一個參數為我們希望最終存取的模型名稱，而第二個參數為中介模型的名稱。
The first argument passed to the `hasManyThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model.

當執行關聯的查詢時，通常將會使用 Eloquent 的外鍵慣例。如果你想要自定關聯的鍵，你可以傳遞它們至 `hasManyThrough` 方法的第三與第四個參數。第三個參數為中介模型的外鍵名稱，而第四個參數為最終模型的外鍵名稱。
Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasManyThrough` method. The third argument is the name of the foreign key on the intermediate model, while the fourth argument is the name of the foreign key on the final model.

    class Country extends Model
    {
        public function posts()
        {
            return $this->hasManyThrough('App\Post', 'App\User', 'country_id', 'user_id');
        }
    }

<a name="polymorphic-relations"></a>
### 多型關聯

#### 資料表結構

多型關聯允許一個模型在單一的關聯從屬一個以上的其他模型。舉個例子，假設你想儲存照片給你的工作人員及你的產品。使用多型關聯，你可以對這兩種情況使用單一的 `photos` 資料表。首先，讓我們查看建立這種關聯所需的資料表結構：
Polymorphic relations allow a model to belong to more than one other model on a single association. For example, imagine you want to store photos for your staff members and for your products. Using polymorphic relationships, you can use a single `photos` table for both of these scenarios. First, let's examine the table structure required to build this relationship:

    staff
        id - integer
        name - string

    products
        id - integer
        price - integer

    photos
        id - integer
        path - string
        imageable_id - integer
        imageable_type - string

要注意的重點是 `photos` 資料表的 `imageable_id` 和 `imageable_type` 欄位。`imageable_id` 欄位會包含所屬的工作人員或產品的 ID 值，而 `imageable_type` 欄位會包含所屬的模型類別名稱。當存取 `imageable` 關聯時，`imageable_type` 欄位會被 ORM 用於判斷所屬的模型是哪個「類型」。
Two important columns to note are the `imageable_id` and `imageable_type` columns on the `photos` table. The `imageable_id` column will contain the ID value of the owning staff or product, while the `imageable_type` column will contain the class name of the owning model. The `imageable_type` column is how the ORM determines which "type" of owning model to return when accessing the `imageable` relation.

#### 模型結構

接著，讓我們查看建立這種關聯所需的模型定義：
Next, let's examine the model definitions needed to build this relationship:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Photo extends Model
    {
        /**
         * 取得所有所屬的可擁有圖片的模型。
         */
        public function imageable()
        {
            return $this->morphTo();
        }
    }

    class Staff extends Model
    {
        /**
         * 取得所有工作人員的照片。
         */
        public function photos()
        {
            return $this->morphMany('App\Photo', 'imageable');
        }
    }

    class Product extends Model
    {
        /**
         * 取得所有產品的照片。
         */
        public function photos()
        {
            return $this->morphMany('App\Photo', 'imageable');
        }
    }

#### 取得多型關聯

一旦你的資料表及模型被定義後，你可以透過你的模型存取關聯。例如，若要存取工作人員的所有照片，我們可以簡單的使用 `photos` 動態屬性：
Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the photos for a staff member, we can simply use the `photos` dynamic property:

    $staff = App\Staff::find(1);

    foreach ($staff->photos as $photo) {
        //
    }

你也可以從多型模型的多型關聯裡，透過存取執行呼叫 `morphTo` 的方法名稱取得擁有者。在我們例子中，就是 `Phone` 模型中的 `imageable` 方法。所以，我們可以存取使用動態屬性存取這個方法：
You may also retrieve the owner of a polymorphic relation from the polymorphic model by accessing the name of the method that performs the call to `morphTo`. In our case, that is the `imageable` method on the `Photo` model. So, we will access that method as a dynamic property:

    $photo = App\Photo::find(1);

    $imageable = $photo->imageable;

`Photo` 模型的 `imageable` 關聯會回傳 `Staff` 或 `Product` 實例，這取決於照片所屬模型的類型。
The `imageable` relation on the `Photo` model will return either a `Staff` or `Product` instance, depending on which type of model owns the photo.

<a name="many-to-many-polymorphic-relations"></a>
### 多型多對多關聯

#### 資料表結構

除了一般的多型關聯，你也可以定義「多對多」的多型關聯。例如，部落格的 `Post` 和 `Video` 模型可以共用多型關聯至 `Tag` 模型。使用多對多的多型關聯能夠讓你的部落格文章及影片共用獨立標籤的單一列表。首先，讓我們查看資料表結構：
In addition to traditional polymorphic relations, you may also define "many-to-many" polymorphic relations. For example, a blog `Post` and `Video` model could share a polymorphic relation to a `Tag` model. Using a many-to-many polymorphic relation allows you to have a single list of unique tags that are shared across blog posts and videos. First, let's examine the table structure:

    posts
        id - integer
        name - string

    videos
        id - integer
        name - string

    tags
        id - integer
        name - string

    taggables
        tag_id - integer
        taggable_id - integer
        taggable_type - string

#### 模型結構

接著，我們已經準備好定義模型的關聯。`Post` 及 `Video` 模型會都擁有 `tags` 方法，並在該方法內呼叫自身 Eloquent 類別的 `morphToMany` 方法：
Next, we're ready to define the relationships on the model. The `Post` and `Video` models will both have a `tags` method that calls the `morphToMany` method on the base Eloquent class:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Post extends Model
    {
        /**
         * 取得該文章的所有標籤。
         */
        public function tags()
        {
            return $this->morphToMany('App\Tag', 'taggable');
        }
    }

#### 定義相對的關聯

然後，在 `Tag` 模型上，你必須對每個要關聯的模型定義一個方法。所以，在這個例子裡，我們需要定義一個 `posts` 方法及一個 `videos` 方法：
Next, on the `Tag` model, you should define a method for each of its related models. So, for this example, we will define a `posts` method and a `videos` method:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Tag extends Model
    {
        /**
         * 取得所有被賦予該標籤的文章。
         */
        public function posts()
        {
            return $this->morphedByMany('App\Post', 'taggable');
        }

        /**
         * 取得所有被賦予該標籤的影片。
         */
        public function videos()
        {
            return $this->morphedByMany('App\Video', 'taggable');
        }
    }

#### 取得關聯

一旦你的資料表及模型被定義後，你可以透過你的模型存取關聯。例如，若要存取文章的所有標籤，你可以簡單的使用 `tags` 動態屬性：
Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the tags for a post, you can simply use the `tags` dynamic property:

    $post = App\Post::find(1);

    foreach ($post->tags as $tag) {
        //
    }

你也可以從多型模型的多型關聯裡，透過存取執行呼叫 `morphedByMany` 的方法名稱取得擁有者。在我們例子中，就是 `Tag` 模型中的 `posts` 或 `videos` 方法。所以，你可以存取使用動態屬性存取這個方法：
You may also retrieve the owner of a polymorphic relation from the polymorphic model by accessing the name of the method that performs the call to `morphedByMany`. In our case, that is the `posts` or `videos` methods on the `Tag` model. So, you will access those methods as dynamic properties:

    $tag = App\Tag::find(1);

    foreach ($tag->videos as $video) {
        //
    }

<a name="querying-relations"></a>
## 查詢關聯

因為所有類型的 Eloquent 關聯都是透過函式定義，你可以呼叫這些函式獲得關聯的一個實例，並不需要實際執行關聯的查詢。此外，所有類型的 Eloquent 關聯也提供了[查詢產生器](/docs/{{version}}/queries)的服務，讓你能夠在你對你的資料庫執行該 SQL 前，在關聯查詢接著鏈結上條件。
Since all types of Eloquent relationships are defined via functions, you may call those functions to obtain an instance of the relationship without actually executing the relationship queries. In addition, all types of Eloquent relationships also serve as [query builders](/docs/{{version}}/queries), allowing you to continue to chain constraints onto the relationship query before finally executing the SQL against your database.

例如，假設有一個部落格系統，其中 `User` 模型擁有許多關聯的 `Post` 模型：
For example, imagine a blog system in which a `User` model has many associated `Post` models:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 取得該使用者的所有文章。
         */
        public function posts()
        {
            return $this->hasMany('App\Post');
        }
    }

你可以查詢 `posts` 關聯並增加額外的條件至關聯，像是：
You may query the `posts` relationship and add additional constraints to the relationship like so:

    $user = App\User::find(1);

    $user->posts()->where('active', 1)->get();

請注意，你可以在關聯使用[查詢產生器](/docs/{{version}}/queries)的任何方法！
Note that you are able to use any of the [query builder](/docs/{{version}}/queries) on the relationship!

#### 關聯方法與動態屬性

如果你不需要增加額外的條件至 Eloquent 的關聯查詢，你可以簡單的存取關聯就如同屬性一樣。例如，延續我們剛剛的 `User` 及 `Post` 範例模型，我們可以存取所有使用者的文章，像是：
If you do not need to add additional constraints to an Eloquent relationship query, you may simply access the relationship as if it were a property. For example, continuing to use our `User` and `Post` example models, we may access all of a user's posts like so:

    $user = App\User::find(1);

    foreach ($user->posts as $post) {
        //
    }

動態屬性是「延遲載入」，意指它們只會在你需要存取它們的時候載入關聯資料。正因為如此，開發者通常使用[預載入](#eager-loading)來預先載入在載入模型後將會被存取的關聯資料。預載入提供了一個明顯減少會被執行於載入模型關聯的 SQL 查詢。
Dynamic properties are "lazy loading", meaning they will only load their relationship data when you actually access them. Because of this, developers often use [eager loading](#eager-loading) to pre-load relationships they know will be accessed after loading the model. Eager loading provides a significant reduction in SQL queries that must be executed to load a model's relations.

#### 查詢關聯是否存在

當存取模型的紀錄時，你可能希望根據關聯的存在限制你的結果。例如，假設你想取得部落格的所有至少有一篇評論的文章。要達成這項功能，你可以傳遞名稱至關聯的 `has` 方法：
When accessing the records for a model, you may wish to limit your results based on the existence of a relationship. For example, imagine you want to retrieve all blog posts that have at least one comment. To do so, you may pass the name of the relationship to the `has` method:

    // 取得所有至少有一篇評論的文章...
    $posts = App\Post::has('comments')->get();

你也可以制定運算子及數量來進一步的自定該查詢：
You may also specify an operator and count to further customize the query:

    // 取得所有至少有三篇評論的文章...
    $posts = Post::has('comments', '>=', 3)->get();

也可以使用「點」符號建構巢狀的 `has` 語句。例如，你可能想取得所有至少有一篇評論被評分的文章：
Nested `has` statements may also be constructed using "dot" notation. For example, you may retrieve all posts that have at least one comment and vote:

    // 取得所有至少有一篇評論被評分的文章...
    $posts = Post::has('comments.votes')->get();

如果你想要更進階的用法，可以使用 `whereHas` 和 `orWhereHas` 方法，在 `has` 查詢裡設定「where」條件。此方法可以讓你增加自訂的條件至關聯條件中，像是檢查評論的內容：
If you need even more power, you may use the `whereHas` and `orWhereHas` methods to put "where" conditions on your `has` queries. These methods allow you to add customized constraints to a relationship constraint, such as checking the content of a comment:

    // 取得所有至少有一篇評論相似於 foo% 的文章Retrieve all posts with at least one comment containing words like foo%
    $posts = Post::whereHas('comments', function ($query) {
        $query->where('content', 'like', 'foo%');
    })->get();

<a name="eager-loading"></a>
### 預載入

當透過屬性存取 Eloquent 關聯時，該關聯資料會被「延遲載入」。意指該關聯資料直到你第一次以屬性存取前，實際上並沒有被載入。不過，Eloquent 可以在你查詢上層模型時「預載入」關聯資料。預載入避免了 N + 1 查詢的問題。要說明 N + 1 查詢的問題，試想一個 `Book` 模型會關聯至 `Author`：
When accessing Eloquent relationships as properties, the relationship data is "lazy loaded". This means the relationship data is not actually loaded until you first access the property. However, Eloquent can "eager load" relationships at the time you query the parent model. Eager loading alleviates the N + 1 query problem. To illustrate the N + 1 query problem, consider a `Book` model that is related to `Author`:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Book extends Model
    {
        /**
         * 取得撰寫該書的作者。
         */
        public function author()
        {
            return $this->belongsTo('App\Author');
        }
    }

現在，讓我們取得所有的書籍及其作者：
Now, let's retrieve all books and their authors:

    $books = App\Book::all();

    foreach ($books as $book) {
        echo $book->author->name;
    }

上方的迴圈會執行一次查詢並取回所有資料表上的書籍，然後每本書都會執行一次查詢取得作者。所以，若有 25 本書，迴圈就會進行 26 次查詢：1 次是原本的書籍，及對每本書查詢並取得作者的額外 25 次。
This loop will execute 1 query to retrieve all of the books on the table, then another query for each book to retrieve the author. So, if we have 25 books, this loop would run 26 queries: 1 for the original book, and 25 additional queries to retrieve the author of each book.

很幸運地，我們可以使用預載入將查詢的操作減少至 2 次。當查詢時，使用 `with` 方法指定想要預載入的關聯資料：
Thankfully, we can use eager loading to reduce this operation to just 2 queries. When querying, you may specify which relationships should be eager loaded using the `with` method:

    $books = App\Book::with('author')->get();

    foreach ($books as $book) {
        echo $book->author->name;
    }

對於該操作，只會執行兩次查詢：
For this operation, only two queries will be executed:

    select * from books

    select * from authors where id in (1, 2, 3, 4, 5, ...)

#### 預載入多種關聯

有時你可能想要在單次操作中預載入多種不同的關聯。要這麼做，只需要傳遞額外的參數至 ` 方法`：
Sometimes you may need to eager load several different relationships in a single operation. To do so, just pass additional arguments to the `with` method:

    $books = App\Book::with('author', 'publisher')->get();

#### 巢狀預載入

若要預載入巢狀關聯，你可以使用「點」語法。例如，讓我們在一個 Eloquent 語法中，預載入所有書籍的作者，及所有作者的個人聯絡方式：
To eager load nested relationships, you may use "dot" syntax. For example, let's eager load all of the book's authors and all of the author's personal contacts in one Eloquent statement:

    $books = App\Book::with('author.contacts')->get();

<a name="constraining-eager-loads"></a>
### 預載入條件限制

有時你可能想要預載入關聯，並且指定預載入額外的查詢條件。下面有一個例子：
Sometimes you may wish to eager load a relationship, but also specify additional query constraints for the eager loading query. Here's an example:

    $users = App\User::with(['posts' => function ($query) {
        $query->where('title', 'like', '%first%');

    }])->get();

在這個例子裡，Eloquent 只會預載入文章標題欄位包含 `first` 的文章。當然，你也可以呼叫其他的[查詢產生器](/docs/{{version}}/queries)來進一步自定預載入的操作：
In this example, Eloquent will only eager load posts that if the post's `title` column contains the word `first`. Of course, you may call other [query builder](/docs/{{version}}/queries) to further customize the eager loading operation:

    $users = App\User::with(['posts' => function ($query) {
        $query->orderBy('created_at', 'desc');

    }])->get();

<a name="lazy-eager-loading"></a>
### 延遲預載入

有時你可能需要在上層模型已經被取得後才預載入關聯。例如，當你需要動態決定是否載入關聯模型時相當有幫助：
Sometimes you may need to eager load a relationship after the parent model has already been retrieved. For example, this may be useful if you need to dynamically decide whether to load related models:

    $books = App\Book::all();

    if ($someCondition) {
        $books->load('author', 'publisher');
    }

如果你想設定預載入查詢的額外條件，你可以傳遞一個 `閉包` 至 `load` 方法：
If you need to set additional query constraints on the eager loading query, you may pass a `Closure` to the `load` method:

    $books->load(['author' => function ($query) {
        $query->orderBy('published_date', 'asc');
    }]);

<a name="inserting-related-models"></a>
## 寫入關聯模型

#### Save 方法

Eloquent 提供了方便的方法來增加新的模型至關聯中。例如，也許你需要寫入新的 `Commnet` 至 `Post` 模型中。除了手動設定 `Commnet` 的 `post_id` 屬性外，你也可以直接使用關聯的 `save` 方法寫入 `Comment`：
Eloquent provides convenient methods for adding new models to relationships. For example, perhaps you need to insert a new `Comment` for a `Post` model. Instead of manually setting the `post_id` attribute on the `Comment`, you may insert the `Comment` directly from the relationship's `save` method:

    $comment = new App\Comment(['message' => 'A new comment.']);

    $post = App\Post::find(1);

    $comment = $post->comments()->save($comment);

注意我們並沒有使用動態屬性存取 `comments` 關聯。相反地，我們呼叫 `comments` 方法取得關聯的實例。`save` 方法會自動在新的 `Comment` 模型增加正確的 `post_id` 值。
Notice that we did not access the `comments` relationship as a dynamic property. Instead, we called the `comments` method to obtain an instance of the relationship. The `save` method will automatically add the appropriate `post_id` value to the new `Comment` model.

如果你需要儲存多筆關聯模型，你可以使用 `saveMany` 方法：
If you need to save multiple related models, you may use the `saveMany` method:

    $post = App\Post::find(1);

    $post->comments()->saveMany([
        new App\Comment(['message' => 'A new comment.']),
        new App\Comment(['message' => 'Another comment.']),
    ]);

#### Save 與多對多關聯

當使用多對多關聯時，`save` 方法允許傳入一個額外的中介表屬性陣列作為第二個參數：
When working with a many-to-many relationship, the `save` method accepts an array of additional intermediate table attributes as its second argument:

    App\User::find(1)->roles()->save($role, ['expires' => $expires]);

#### Create 方法

除了 `save` 與 `saveMany` 方法，你也可以使用 `create` 方法，該方法允許傳入屬性的陣列來立模型，並寫入至資料庫。同樣的，`save` 與 `create` 不同的地方是，`save` 允許傳入一個完整的 Eloquent 模型實例，但 `create` 只允許原始的 PHP `陣列`：
In addition to the `save` and `saveMany` methods, you may also use the `create` method, which accepts an array of attributes, creates a model, and inserts it into the database. Again, the difference between `save` and `create` is that `save` accepts a full Eloquent model instance while `create` accepts a plain PHP `array`:

    $post = App\Post::find(1);

    $comment = $post->comments()->create([
        'message' => 'A new comment.',
    ]);

在使用 `create` 方法前，請確定瀏覽了文件的[批量賦值](/docs/{{version}}/eloquent#mass-assignment)章節。
Before using the `create` method, be sure to review the documentation on attribute [mass assignment](/docs/{{version}}/eloquent#mass-assignment).

<a name="updating-belongs-to-relationships"></a>
#### 更新「從屬」關聯

當更新一個 `belongsTo` 關聯時，你可以使用 `associate` 方法。此方法會設定外鍵至下層模型：
When updating a `belongsTo` relationship, you may use the `associate` method. This method will set the foreign key on the child model:

    $account = App\Account::find(10);

    $user->account()->associate($account);

    $user->save();

當刪除一個 `belongsTo` 關聯時，你可以使用 `dissociate` 方法。此方法會重置關聯至此下層模型的外鍵：
When removing a `belongsTo` relationship, you may use the `dissociate` method. This method will reset the foreign key as well as the relation on the child model:

    $user->account()->dissociate();

    $user->save();

<a name="inserting-many-to-many-relationships"></a>
### 多對多關聯

#### 附加與卸除

當使用多對多關聯時，Eloquent 提供一些額外的輔助方法讓操作關聯模型時更加方便。例如，讓我們假設一個使用者可以擁有多個身份，且每個身份可以被多個使用者擁有。要附加一個規則至一個使用者，並 join 模型及寫入記錄至中介表，可以使用 `attach` 方法：
When working with many-to-many relationships, Eloquent provides a few additional helper methods to make working with related models more convenient. For example, let's imagine a user can have many roles and a role can have many users. To attach a role to a user by inserting a record in the intermediate table that joins the models, use the `attach` method:

    $user = App\User::find(1);

    $user->roles()->attach($roleId);

當附加一個關聯至模型時，你也可以傳遞一個需被寫入至中介表的額外資料陣列：
When attaching a relationship to a model, you may also pass an array of additional data to be inserted into the intermediate table:

    $user->roles()->attach($roleId, ['expires' => $expires]);

當然，有些時候也需要移除使用者的一個身份。要移除一個多對多的紀錄，使用 `detach` 方法。`detach` 方法會從中介表中移除正確的紀錄；當然，兩個模型依然會存在於資料庫中：
Of course, sometimes it may be necessary to remove a role from a user. To remove a many-to-many relationship record, use the `detach` method. The `detach` method will remove the appropriate record out of the intermediate table; however, both models will remain in the database:

    // 從使用者上移除單一身份...
    $user->roles()->detach($roleId);

    // 從使用者上移除所有身份...
    $user->roles()->detach();

為了方便，`attach` 與 `detach` 都允許傳入 IDs 的陣列：
For convenience, `attach` and `detach` also accept arrays of IDs as input:

    $user = App\User::find(1);

    $user->roles()->detach([1, 2, 3]);

    $user->roles()->attach([1 => ['expires' => $expires], 2, 3]);

#### 為了方便的同步

你也可以使用 `sync` 方法建構多對多關聯。`sync` 允許傳入放置於中介表的 IDs 陣列。任何不在給定陣列中的 IDs 將會從中介表中被刪除。所以，在此操作結束後，只會有陣列中的 IDs 存在於中介表中：
You may also use the `sync` method to construct many-to-many associations. The `sync` method accepts an array of IDs to place on the intermediate table. Any IDs that are not in the given array will be removed from the intermediate table. So, after this operation is complete, only the IDs in the array will exist in the intermediate table:

    $user->roles()->sync([1, 2, 3]);

你也可以傳遞中介表上該 IDs 額外的值：
You may also pass additional intermediate table values with the IDs:

    $user->roles()->sync([1 => ['expires' => true], 2, 3]);
