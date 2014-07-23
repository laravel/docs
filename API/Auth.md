## Auth

The Auth object includes methods related to user authentication (sign-in, logout). 

### Auth::user()

This method finds whether a user is signed in or not. 

#### Blade example

    @if(Auth::user())
    	<h2>You are signed in</h2>



### Auth::logout()

This method logs the user out.

#### Example

    Auth::logout();
    return Redirect::to('/');

