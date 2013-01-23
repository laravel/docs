# Security

- [Configuration](#configuration)
- [Storing Passwords](#storing-passwords)
- [Authenticating Users](#authenticating-users)
- [Protecting Routes](#protecting-routes)
- [Encryption](#encryption)

<a name="configuration"></a>
## Configuration

Laravel aims to make implementing authentication very simple. In fact, almost everything is configured for you out of the box. The authentication configuration file is located at `app/config/auth.php`, which contains several well documented options for tweaking the behavior of the authentication facilities.

By default, Laravel includes a `User` model in your `app/models` directory which may be used with the default Eloquent authentication driver. Please remember when building the Schema for this Model to ensure that the password field is a minimum of 60 characters.

If your application is not using Eloquent, you may use the `database` authentication driver which uses the Laravel query builder.

<a name="storing-passwords"></a>
## Storing Passwords

The Laravel `Hash` class provides secure Bcrypt hashing:

**Hashing A Password Using Bcrypt**

	$password = Hash::make('secret');

**Verifying A Password Against A Hash**

	if (Hash::check('secret', $hashedPassword))
	{
		// The passwords match...
	}

<a name="authenticating-users"></a>
## Authenticating Users

To log a user into your application, you may use the `Auth::attempt` method.

	if (Auth::attempt(array('email' => $email, 'password' => $password)))
	{
		// The user's credentials are valid...
	}

Take note that `email` is not a required option, it is merely used for example. You should use whatever column name corresponds to a "username" in your database.

If you would like to provide "remember me" functionality in your application, you may pass `true` as the second argument to the `attempt` method, which will keep the user authenticated indefinitely (or until they manually logout):

**Authenticating A User And "Remembering" Them**

	if (Auth::attempt(array('email' => $email, 'password' => $password), true))
	{
		// The user is being remembered...
	}

**Note:** If the `attempt` method returns `true`, the user is considered logged into the application.

**Authenticating A User with extra conditions**

You may add in extra conditions to ensure that the user is (for example) 'active', or 'not suspended':

    if (Auth::attempt(array('email' => $email, 'password' => $password, 'active' => 1, 'suspended' => 0)))
    {
        // The user is active, not suspended, and exists.
    }

Once a user is authenticated, you may access the User model / record:

**Accessing The Logged In User**

	$email = Auth::user()->email;

**Logging A User Out Of The Application**

	Auth::logout();

<a name="protecting-routes"></a>
## Protecting Routes

Route filters may be used to allow only authenticated users to access a given route. Laravel provides the `auth` filter by default, and it is defined in `app/filters.php`.

**Protecting A Route**

	Route::get('profile', array('before' => 'auth', function()
	{
		// Only authenticated users may enter...
	}));

### CSRF Protection

Laravel provides an easy method of protecting your application from cross-site request forgeries.

**Insert the CSRF token into your form ** using `csrf_token()` or `Session::getToken()`

    <input type="hidden" name="csrf_token" value="<?php echo csrf_token(); ?>">

**Validate the submitted CSRF token**

    Route::post('register', array('before' => 'csrf', function()
    {
        return 'You gave a valid CSRF token!';
    }));

<a name="encryption"></a>
## Encryption

Laravel provides facilities for strong AES-256 encryption via the mcrypt PHP extension:

**Encrypting A Value**

	$encrypted = Crypt::encrypt('secret');

> **Note:** Be sure to set a 32 character, random string in the `key` option of the `app/config/app.php` file. Otherwise, encrypted values will not be secure.

**Decrypting A Value**

	$decrypted = Crypt::decrypt($encryptedValue);
