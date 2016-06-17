# Eloquent: Serialization

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values To JSON](#appending-values-to-json)

<a name="introduction"></a>
## Introduction

When building JSON APIs, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in your serializations.

<a name="basic-usage"></a>
## Basic Usage

#### Converting A Model To An Array

To convert a model and its loaded [relationships](/docs/{{version}}/eloquent-relationships) to an array, you may use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays:

    $user = App\User::with('roles')->first();

    return $user->toArray();

You may also convert [collections](/docs/{{version}}/eloquent-collections) to arrays:

    $users = App\User::all();

    return $users->toArray();

#### Converting A Model To JSON

To convert a model to JSON, you may use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON:

    $user = App\User::find(1);

    return $user->toJson();

Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method:

    $user = App\User::find(1);

    return (string) $user;

Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers:

    Route::get('users', function () {
        return App\User::all();
    });

<a name="hiding-attributes-from-json"></a>
## Hiding Attributes From JSON

Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property definition to your model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be hidden for arrays.
         *
         * @var array
         */
        protected $hidden = ['password'];
    }

> **Note:** When hiding relationships, use the relationship's **method** name, not its dynamic property name.

Alternatively, you may use the `visible` property to define a white-list of attributes that should be included in your model's array and JSON representation:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be visible in arrays.
         *
         * @var array
         */
        protected $visible = ['first_name', 'last_name'];
    }

#### Temporarily Modifying Property Visibility

If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` method. The `makeVisible` method returns the model instance for convenient method chaining:

    return $user->makeVisible('attribute')->toArray();

Likewise, if you would like to make some typically visible attributes hidden on a given model instance, you may use the `makeHidden` method.

    return $user->makeHidden('attribute')->toArray();

<a name="appending-values-to-json"></a>
## Appending Values To JSON

Occasionally, you may need to add array attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/{{version}}/eloquent-mutators) for the value:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Get the administrator flag for the user.
         *
         * @return bool
         */
        public function getIsAdminAttribute()
        {
            return $this->attributes['admin'] == 'yes';
        }
    }

Once you have created the accessor, add the attribute name to the `appends` property on the model:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The accessors to append to the model's array form.
         *
         * @var array
         */
        protected $appends = ['is_admin'];
    }

Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON forms. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model.
