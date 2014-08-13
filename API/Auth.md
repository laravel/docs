## Auth

The Auth object includes methods related to user authentication (sign-in, logout). 


- [User](#user)
- [Logout](#logout)
- [Attempt](#attempt)
___

<a name="user"></a>

### Auth::user()

This method finds whether a user is signed in or not. It returns a boolean value. It can return several useful properties.

#### Usage

There are no arguments needed.

#### Properties

`username` The name of the logged-in user.

#### Blade examples

Tell only signed-in users "you are signed in":

    @if(Auth::user())
    	<h2>You are signed in</h2>

Echoes the username of the signed in user.

    {{ Auth::user()->username }}

___

<a name="logout"></a>

### Auth::logout()

This method logs the user out.

#### Usage

There are no arguments needed.

#### Examples

    Auth::logout();
    return Redirect::to('/');

___

<a name="attempt"></a>

### Auth::attempt()

This method attempts to log a user in using their credentials. 

#### Usage

	Auth::attempt(CREDENTIALS_ARRAY);

`CREDENTIALS_ARRAY` should be an associative array with the user's username/email and password.

#### Examples
	
Gets a user's inputs, creates an array, and processes the sign-in.

	$inputs = Inputs::all();
    $credentials = array('email' => $input['email'], 'password' => $input['password']);
	Auth::attempt($credentials)



