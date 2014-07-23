## Auth

The Auth object includes methods related to user authentication (sign-in, logout). 

___

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

### Auth::logout()

This method logs the user out.

#### Usage

There are no arguments needed.

#### Examples

    Auth::logout();
    return Redirect::to('/');

