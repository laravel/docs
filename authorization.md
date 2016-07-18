# Authorization

- [Introduction](#introduction)
- [Creating Policies](#creating-policies)
    - [Generating Policies](#generating-policies)
	- [Registering Policies](#registering-policies)
- [Writing Policies](#writing-policies)
    - [Policy Methods](#policy-methods)
    - [Methods Without Models](#methods-without-models)
    - [Policy Filters](#policy-filters)
- [Authorizing Actions](#authorizing-actions)
    - [Via The User Model](#via-the-user-model)
    - [Via Blade Templates](#via-blade-templates)
- [Controller Authorization](#controller-authorization)

<a name="introduction"></a>
## Introduction

In addition to providing [authentication](/docs/{{version}}/authentication) services out of the box, Laravel also provides a simple way to authorize user actions against a given resource. Like authentication, Laravel's approach to authorization is simple. By defining small, focused "policy" classes, you can easily determine if a user may perform a given action while using simple and understandable code.

<a name="creating-policies"></a>
## Creating Policies

<a name="generating-policies"></a>
### Generating Policies

Policies are classes that organize authorization logic around on the resource they authorize. For example, if your application is a blog, you will probably have a `Post` model and a corresponding `PostPolicy` to authorize user actions such as creating or updating posts. You may generate a policy using the `make:policy` [artisan command](/docs/{{version}}/artisan). The generated policy will be placed in the `app/Policies` directory:

	php artisan make:policy PostPolicy

The `make:policy` command will generate an empty policy class. If you would like to generate a class with the basic "CRUD" policy methods already included in the class, you may specify a `--model` when executing the command:

    php artisan make:policy PostPolicy --model=Post

> {tip} All policies are resolved via the Laravel [service container](/docs/{{version}}/container), meaning you may type-hint any needed dependencies in the policy's constructor and they will be automatically injected.

<a name="registering-policies"></a>
### Registering Policies

Once the policy exists, it needs to be registered. The `AuthServiceProvider` included with fresh Laravel applications contains a `policies` property which maps your Eloquent models to their corresponding policies. Registering a policy will instruct Laravel which policy to utilize when authorizing actions against a given model:

	<?php

	namespace App\Providers;

	use App\Post;
	use App\Policies\PostPolicy;
    use Illuminate\Support\Facades\Gate;
	use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

	class AuthServiceProvider extends ServiceProvider
	{
	    /**
	     * The policy mappings for the application.
	     *
	     * @var array
	     */
	    protected $policies = [
	        Post::class => PostPolicy::class,
	    ];

	    /**
	     * Register any application authentication / authorization services.
	     *
	     * @return void
	     */
	    public function boot()
	    {
	        $this->registerPolicies();

            //
	    }
	}

<a name="writing-policies"></a>
## Writing Policies

<a name="policy-methods"></a>
### Policy Methods

Once the policy has been registered, you may add methods for each action it authorizes. For example, let's define an `update` method on our `PostPolicy` which determines if the given `User` can update a given `Post` instance.

The `update` method will receive the currently authenticated user and a `Post` instance as its arguments. This method should return `true` or `false` indicating whether the given user is authorized to update the given `Post`. So, for this example, let's verify that the user's `id` matches the `user_id` on the post:

	<?php

	namespace App\Policies;

	use App\User;
	use App\Post;

	class PostPolicy
	{
		/**
		 * Determine if the given post can be updated by the user.
		 *
		 * @param  \App\User  $user
		 * @param  \App\Post  $post
		 * @return bool
		 */
	    public function update(User $user, Post $post)
	    {
	    	return $user->id === $post->user_id;
	    }
	}

You may continue to define additional methods on the policy as needed for the various actions it authorizes. For example, you might define `view` or `delete` methods to authorize various `Post` actions, but remember you are free to give your policy methods any name you like.

> {tip} If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `view`, `create`, `update`, and `delete` actions.

<a name="methods-without-models"></a>
### Methods Without Models

Some policy methods will only receive the currently authenticated user and not an instance of the model they authorize. This situation is most common when authorizing `view` or `create` actions. For example, if you are creating a blog, you may wish to check if a user is authorized to view or create any posts at all.

When defining policy methods that will not receive a model instance, such as a `create` method, you should suffix the methods with `Any`:

    /**
     * Determine if the given user can create posts.
     *
     * @param  \App\User  $user
     * @return bool
     */
    public function createAny(User $user)
    {
        //
    }

When authorizing if a user can `view` a given resource, it's common to have both `view` and `viewAny` methods on your policy. This allows you to authorize that the user can view the resource in general, as well as authorize that they can view particular instances of that resource. It's perfectly acceptable to authorize that a user can view posts but cannot view a *particular* post instance:

    /**
     * Determine whether the user can view posts.
     *
     * @param  App\User  $user
     * @return mixed
     */
    public function viewAny(User $user)
    {
        // Return true if the user can view posts...
    }

    /**
     * Determine whether the user can view the post.
     *
     * @param  App\User  $user
     * @param  App\Post  $post
     * @return mixed
     */
    public function view(User $user, Post $post)
    {
        // Return true if the user can view the given post...
    }

> {tip} If you used the `--model` option when generating your policy, the `viewAny`, `createAny`, and `updateAny` methods will already be defined on the policy.

<a name="policy-filters"></a>
### Policy Filters

For certain users, you may wish to authorize all actions within a given policy. To accomplish this, define a `before` method on the policy. The `before` method will be executed before any other methods on the policy, giving you an opportunity to authorize the action before the intended policy method is actually called. This feature is most commonly used for authorizing application administrators to perform any action:

    public function before($user, $ability)
    {
        if ($user->isSuperAdmin()) {
            return true;
        }
    }

<a name="authorizing-actions"></a>
## Authorizing Actions

<a name="via-the-user-model"></a>
### Via The User Model

Fresh Laravel applications include a `User` model that is located in the `app` directory. The `User` model extends a base class which provides the `can` and `cant` methods. These methods may be used to authorize actions and will automatically utilize the correct policies for the arguments you give them.

To determine if an action is authorized, call the `can` method with the action you wish to authorize and an instance of the model the action is intended for:

	if ($user->can('update', $post)) {
		//
	}

	if ($user->cannot('update', $post)) {
		//
	}

<a name="via-blade-templates"></a>
#### Via Blade Templates

Likewise, the `@can` Blade directive will utilize policies when they are available for the given arguments:

	@can('update', $post)
		<!-- The Current User Can Update The Post -->
	@endcan

#### Via The Policy Helper

The global `policy` helper function may be used to retrieve the `Policy` class for a given class instance. For example, we may pass a `Post` instance to the `policy` helper to get an instance of our corresponding `PostPolicy` class:

	if (policy($post)->update($user, $post)) {
		//
	}

<a name="controller-authorization"></a>
## Controller Authorization

By default, the base `App\Http\Controllers\Controller` class included with Laravel uses the `AuthorizesRequests` trait. This trait provides the `authorize` method, which may be used to quickly authorize a given action and throw a `AuthorizationException` if the action is not authorized.

The `authorize` method shares the same signature as the various other authorization methods such as `Gate::allows` and `$user->can()`. So, let's use the `authorize` method to quickly authorize a request to update a `Post`:

    <?php

    namespace App\Http\Controllers;

    use App\Post;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * Update the given post.
         *
         * @param  int  $id
         * @return Response
         */
        public function update($id)
        {
        	$post = Post::findOrFail($id);

        	$this->authorize('update', $post);

        	// Update Post...
        }
    }

If the action is authorized, the controller will continue executing normally; however, if the `authorize` method determines that the action is not authorized, an `AuthorizationException` will automatically be thrown which generates a HTTP response with a `403 Not Authorized` status code. As you can see, the `authorize` method is a convenient, fast way to authorize an action or throw an exception with a single line of code.

The `AuthorizesRequests` trait also provides the `authorizeForUser` method to authorize an action on a user that is not the currently authenticated user:

	$this->authorizeForUser($user, 'update', $post);

#### Automatically Determining Policy Methods

Frequently, a policy's methods will correspond to the methods on a controller. For example, in the `update` method above, the controller method and the policy method share the same name: `update`.

For this reason, Laravel allows you to simply pass the instance arguments to the `authorize` method, and the ability being authorized will automatically be determined based on the name of the calling function. In this example, since `authorize` is called from the controller's `update` method, the `update` method will also be called on the `PostPolicy`:

    /**
     * Update the given post.
     *
     * @param  int  $id
     * @return Response
     */
    public function update($id)
    {
    	$post = Post::findOrFail($id);

    	$this->authorize($post);

    	// Update Post...
    }

Remember, for resource controller methods that do not relate to a particular model instance, such as `create`, the `Any` version of the policy method would be called. For example:

    /**
     * Show the form to create a new post.
     *
     * @return Response
     */
    public function create()
    {
        $this->authorize();

        // Show Create Post Form...
    }

In this example, the `createAny` method would be called on the policy:

    /**
     * Determine if the given user can create posts.
     *
     * @param  \App\User  $user
     * @return bool
     */
    public function createAny(User $user)
    {
        //
    }
