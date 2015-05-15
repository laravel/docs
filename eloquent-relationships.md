# Eloquent ORM: Relationships

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
	- [One To One](#one-to-one)
	- [One To Many](#one-to-many)
	- [Many To Many](#many-to-many)
	- [Has Many Through](#has-many-through)
- [Querying Relations](#querying-relations)
- [Eager Loading](#eager-loading)
- [Inserting Related Models](#inserting-related-models)
- [Touching Parent Timestamps](#touching-parent-timestamps)
- [Working With Pivot Tables](#working-with-pivot-tables)

<a name="introduction"></a>
## Introduction

Database tables are often related to one another. For example, a blog post may have many comments, or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports several different types of relationships:

- [One To One](#one-to-one)
- [One To Many](#one-to-many)
- [Many To Many](#many-to-many)
- [Has Many Through](#has-many-through)

<a name="defining-relationships"></a>
## Defining Relationships

Eloquent relationships are defined as functions on your Eloquent model classes. Since, like Eloquent models themselves, relationships also serve as powerful [query builders](/docs/{{version}}/queries), defining relationships as functions provides powerful method chaining and querying capabilities. For example:

	$user->posts()->where('active', 1)->get();

But, before diving too deep into using relationships, let's learn how to define each type:

<a name="one-to-one"></a>
### One To One

A one-to-one relationship is a very basic relation. For example, a `User` model might be associated with one `Phone`. To define this relationship, we place a `phone` method on the `User` model. The `phone` method should return the results of the `hasOne` method on the base Eloquent model class:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get the phone record associated with the user.
		 */
		public function phone()
		{
			return $this->hasOne('App\Phone');
		}
	}

The first argument passed to the `hasOne` method is the name of the related model. Once the relationship is defined, we may retrieve the related record using Eloquent's [dynamic properties](#dynamic-properties). Dynamic properties allow you to access relationship functions as if they were properties defined on the model:

	$phone = User::find(1)->phone;

Eloquent assumes the foreign key of the relationship based on the model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method:

	return $this->hasOne('App\Phone', 'foreign_key');

Additionally, Eloquent assumes that the foreign key should have a value matching the `id` column of the parent. In otherwords, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a value other than `id`, you may pass a third argument to the `hasOne` method specifying your custom key:

	return $this->hasOne('App\Phone', 'foreign_key', 'local_key');

#### Defining The Inverse Of The Relation

So, we can access the `Phone` model from our `User`. Now, let's define a relationship on the `Phone` model that will let us access the `User` the owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Phone extends Model
	{
		/**
		 * Get the user that owns the phone.
		 */
		public function user()
		{
			return $this->belongsTo('App\User');
		}
	}

In the example above, Eloquent will try to match the `user_id` from the `Phone` model to an `id` on the `User` model. Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method:

	/**
	 * Get the user that owns the phone.
	 */
	public function user()
	{
		return $this->belongsTo('App\User', 'foreign_key');
	}

If your parent model does not use `id` as its primary key, or you wish to join the child model to a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key:

	/**
	 * Get the user that owns the phone.
	 */
	public function user()
	{
		return $this->belongsTo('App\User', 'foreign_key', 'other_key');
	}

<a name="one-to-many"></a>
### One To Many

A "one-to-many" relationship is used to define relationships where a single model owns any amount of other models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by placing a function on your Eloquent model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Post extends Model
	{
		/**
		 * Get the comments for the blog post.
		 */
		public function comments()
		{
			return $this->hasMany('App\Comment');
		}
	}

Remember, Eloquent will automatically determine the proper foreign key column on the `Comment` model. By convention, Eloquent will take the "snake case" name of the owning model and suffix it with `_id`. So, for this example, Eloquent will assume the foreign key on the `Comment` model is `post_id`.

Once the relationship has been defined, we can access the collection of comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic properties", we can access relationship functions as if they were defined as properties on the model:

	$comments = App\Post::find(1)->comments;

	foreach ($comments as $comment) {
		//
	}

Of course, since all relationships also serve as query builders, you can add further constraints to which comments are retrieved by calling the `comments` method and continuing to chain conditions onto the query:

	$comments = App\Post::find(1)->comments()->where('title', 'foo')->first();

Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method:

	return $this->hasMany('App\Comment', 'foreign_key');

	return $this->hasMany('App\Comment', 'foreign_key', 'local_key');

#### Defining The Inverse Of The Relation

Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship function on the child model which calls the `belongsTo` method:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Comment extends Model
	{
		/**
		 * Get the post that owns the comment.
		 */
		public function post()
		{
			return $this->belongsTo('App\Post');
		}
	}

Once the relationship has been defined, we can retrieve the `Post` model for a `Comment` by accessing the `post` "dynamic property":

	$comment = App\Comment::find(1);

	echo $comment->post->title;

In the example above, Eloquent will try to match the `post_id` from the `Comment` model to an `id` on the `Post` model. Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. However, if the foreign key on the `Comment` model is not `post_id`, you may pass a custom key name as the second argument to the `belongsTo` method:

	/**
	 * Get the post that owns the comment.
	 */
	public function post()
	{
		return $this->belongsTo('App\Post', 'foreign_key');
	}

If your parent model does not use `id` as its primary key, or you wish to join the child model to a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key:

	/**
	 * Get the post that owns the comment.
	 */
	public function post()
	{
		return $this->belongsTo('App\Post', 'foreign_key', 'other_key');
	}

<a name="many-to-many"></a>
### Many To Many

Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of such a relationship is a user with many roles, where the roles are also shared by other users. For example, many users may have the role of "Admin". To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names, and contains the `user_id` and `role_id` columns.

Many-to-many relationships are defined by writing a method that calls the `belongsToMany` method on the base Eloquent class. For example, let's define the `roles` method on our `User` model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The roles that belong to the user.
		 */
		public function roles()
		{
			return $this->belongsToMany('App\Role');
		}
	}

Once the relationship is defined, you may access the user's roles using the `roles` dynamic property:

	$user = App\User::find(1);

	foreach ($user->roles as $role) {
		//
	}

Of course, like all other relationship types, you may call the `roles` method to continue chaining query constraints onto the relationship:

	$roles = App\User::find(1)->roles()->orderBy('name')->get();

As mentioned previously, to determine the table name of the relationship's joining table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method:

	return $this->belongsToMany('App\Role', 'user_roles');

In addition to customizing the name of the joining table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to:

	return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'role_id');

#### Defining The Inverse Of The Relationship

To define the inverse of a many-to-many relationship, you simply place another call to `belongsToMany` on your related model. To continue our user roles example, let's define the `users` method on the `Role` model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Role extends Model
	{
		/**
		 * The users that belong to the role.
		 */
		public function users()
		{
			return $this->belongsToMany('App\User');
		}
	}

As you can see, the relationship is defined exactly the same as its `User` counterpart, with the exception of simply referencing the `App\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the inverse of many-to-many relationships.

<a name="has-many-through"></a>
### Has Many Through

The "has many through" relation provides a convenient short-cut for accessing distant relations via an intermediate relation. For example, a `Country` model might have many `Post` through a `User` model. The tables for this relationship would look like this:

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

Even though the `posts` table does not contain a `country_id` column, the `hasManyThrough` relation will allow us to access a country's posts via `$country->posts`. Let's define the relationship:

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'App\User');
		}

	}

If you would like to manually specify the keys of the relationship, you may pass them as the third and fourth arguments to the method:

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'App\User', 'country_id', 'user_id');
		}

	}

<a name="querying-relations"></a>
## Querying Relations

#### Querying Relations When Selecting

When accessing the records for a model, you may wish to limit your results based on the existence of a relationship. For example, you wish to pull all blog posts that have at least one comment. To do so, you may use the `has` method:

	$posts = Post::has('comments')->get();

You may also specify an operator and a count:

	$posts = Post::has('comments', '>=', 3)->get();

Nested `has` statements may also be constructed using "dot" notation:

	$posts = Post::has('comments.votes')->get();

If you need even more power, you may use the `whereHas` and `orWhereHas` methods to put "where" conditions on your `has` queries:

	$posts = Post::whereHas('comments', function($q)
	{
		$q->where('content', 'like', 'foo%');

	})->get();

<a name="dynamic-properties"></a>
### Dynamic Properties

Eloquent allows you to access your relations via dynamic properties. Eloquent will automatically load the relationship for you, and is even smart enough to know whether to call the `get` (for one-to-many relationships) or `first` (for one-to-one relationships) method.  It will then be accessible via a dynamic property by the same name as the relation. For example, with the following model `$phone`:

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User');
		}

	}

	$phone = Phone::find(1);

Instead of echoing the user's email like this:

	echo $phone->user()->first()->email;

It may be shortened to simply:

	echo $phone->user->email;

> **Note:** Relationships that return many results will return an instance of the `Illuminate\Database\Eloquent\Collection` class.

<a name="eager-loading"></a>
## Eager Loading

Eager loading exists to alleviate the N + 1 query problem. For example, consider a `Book` model that is related to `Author`. The relationship is defined like so:

	class Book extends Model {

		public function author()
		{
			return $this->belongsTo('App\Author');
		}

	}

Now, consider the following code:

	foreach (Book::all() as $book)
	{
		echo $book->author->name;
	}

This loop will execute 1 query to retrieve all of the books on the table, then another query for each book to retrieve the author. So, if we have 25 books, this loop would run 26 queries.

Thankfully, we can use eager loading to drastically reduce the number of queries. The relationships that should be eager loaded may be specified via the `with` method:

	foreach (Book::with('author')->get() as $book)
	{
		echo $book->author->name;
	}

In the loop above, only two queries will be executed:

	select * from books

	select * from authors where id in (1, 2, 3, 4, 5, ...)

Wise use of eager loading can drastically increase the performance of your application.

Of course, you may eager load multiple relationships at one time:

	$books = Book::with('author', 'publisher')->get();

You may even eager load nested relationships:

	$books = Book::with('author.contacts')->get();

In the example above, the `author` relationship will be eager loaded, and the author's `contacts` relation will also be loaded.

### Eager Load Constraints

Sometimes you may wish to eager load a relationship, but also specify a condition for the eager load. Here's an example:

	$users = User::with(['posts' => function($query)
	{
		$query->where('title', 'like', '%first%');

	}])->get();

In this example, we're eager loading the user's posts, but only if the post's title column contains the word "first".

Of course, eager loading Closures aren't limited to "constraints". You may also apply orders:

	$users = User::with(['posts' => function($query)
	{
		$query->orderBy('created_at', 'desc');

	}])->get();

### Lazy Eager Loading

It is also possible to eagerly load related models directly from an already existing model collection. This may be useful when dynamically deciding whether to load related models or not, or in combination with caching.

	$books = Book::all();

	$books->load('author', 'publisher');

You may also pass a Closure to set constraints on the query:

	$books->load(['author' => function($query)
	{
		$query->orderBy('published_date', 'asc');
	}]);

<a name="inserting-related-models"></a>
## Inserting Related Models

#### Attaching A Related Model

You will often need to insert new related models. For example, you may wish to insert a new comment for a post. Instead of manually setting the `post_id` foreign key on the model, you may insert the new comment from its parent `Post` model directly:

	$comment = new Comment(['message' => 'A new comment.']);

	$post = Post::find(1);

	$comment = $post->comments()->save($comment);

In this example, the `post_id` field will automatically be set on the inserted comment.

If you need to save multiple related models:

	$comments = [
		new Comment(['message' => 'A new comment.']),
		new Comment(['message' => 'Another comment.']),
		new Comment(['message' => 'The latest comment.'])
	];

	$post = Post::find(1);

	$post->comments()->saveMany($comments);

### Associating Models (Belongs To)

When updating a `belongsTo` relationship, you may use the `associate` method. This method will set the foreign key on the child model:

	$account = Account::find(10);

	$user->account()->associate($account);

	$user->save();

### Inserting Related Models (Many To Many)

You may also insert related models when working with many-to-many relations. Let's continue using our `User` and `Role` models as examples. We can easily attach new roles to a user using the `attach` method:

#### Attaching Many To Many Models

	$user = User::find(1);

	$user->roles()->attach(1);

You may also pass an array of attributes that should be stored on the pivot table for the relation:

	$user->roles()->attach(1, ['expires' => $expires]);

Of course, the opposite of `attach` is `detach`:

	$user->roles()->detach(1);

Both `attach` and `detach` also take arrays of IDs as input:

	$user = User::find(1);

	$user->roles()->detach([1, 2, 3]);

	$user->roles()->attach([1 => ['attribute1' => 'value1'], 2, 3]);

#### Using Sync To Attach Many To Many Models

You may also use the `sync` method to attach related models. The `sync` method accepts an array of IDs to place on the pivot table. After this operation is complete, only the IDs in the array will be on the intermediate table for the model:

	$user->roles()->sync([1, 2, 3]);

#### Adding Pivot Data When Syncing

You may also associate other pivot table values with the given IDs:

	$user->roles()->sync([1 => ['expires' => true]]);

Sometimes you may wish to create a new related model and attach it in a single command. For this operation, you may use the `save` method:

	$role = new Role(['name' => 'Editor']);

	User::find(1)->roles()->save($role);

In this example, the new `Role` model will be saved and attached to the user model. You may also pass an array of attributes to place on the joining table for this operation:

	User::find(1)->roles()->save($role, ['expires' => $expires]);

<a name="touching-parent-timestamps"></a>
## Touching Parent Timestamps

When a model `belongsTo` another model, such as a `Comment` which belongs to a `Post`, it is often helpful to update the parent's timestamp when the child model is updated. For example, when a `Comment` model is updated, you may want to automatically touch the `updated_at` timestamp of the owning `Post`. Eloquent makes it easy. Just add a `touches` property containing the names of the relationships to the child model:

	class Comment extends Model {

		protected $touches = ['post'];

		public function post()
		{
			return $this->belongsTo('App\Post');
		}

	}

Now, when you update a `Comment`, the owning `Post` will have its `updated_at` column updated:

	$comment = Comment::find(1);

	$comment->text = 'Edit to this comment!';

	$comment->save();

<a name="working-with-pivot-tables"></a>
## Working With Pivot Tables

As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` object has many `Role` objects that it is related to. After accessing this relationship, we may access the `pivot` table on the models:

	$user = User::find(1);

	foreach ($user->roles as $role)
	{
		echo $role->pivot->created_at;
	}

Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table, and may be used as any other Eloquent model.

By default, only the keys will be present on the `pivot` object. If your pivot table contains extra attributes, you must specify them when defining the relationship:

	return $this->belongsToMany('App\Role')->withPivot('foo', 'bar');

Now the `foo` and `bar` attributes will be accessible on our `pivot` object for the `Role` model.

If you want your pivot table to have automatically maintained `created_at` and `updated_at` timestamps, use the `withTimestamps` method on the relationship definition:

	return $this->belongsToMany('App\Role')->withTimestamps();

#### Deleting Records On A Pivot Table

To delete all records on the pivot table for a model, you may use the `detach` method:

	User::find(1)->roles()->detach();

Note that this operation does not delete records from the `roles` table, but only from the pivot table.

#### Updating A Record On A Pivot Table

Sometimes you may need to update your pivot table, but not detach it. If you wish to update your pivot table in place you may use `updateExistingPivot` method like so:

	User::find(1)->roles()->updateExistingPivot($roleId, $attributes);

#### Defining A Custom Pivot Model

Laravel also allows you to define a custom Pivot model. To define a custom model, first create your own "Base" model class that extends `Eloquent`. In your other Eloquent models, extend this custom base model instead of the default `Eloquent` base. In your base model, add the following function that returns an instance of your custom Pivot model:

	public function newPivot(Model $parent, array $attributes, $table, $exists)
	{
		return new YourCustomPivot($parent, $attributes, $table, $exists);
	}
