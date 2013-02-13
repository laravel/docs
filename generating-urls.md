# Generating urls

- [Introduction](#introduction)
- [URLs To Routes](#urls-to-routes)
- [URLs To Controller Actions](#urls-to-controller-actions)
- [URLs To Assets](#urls-to-assets)
- [Secure URLs](#secure-urls)
- [Helpers](#helpers)

<a name="introduction"></a>
## Introduction

<a name="urls-to-controller-actions"></a>
## URLs To Routes

**Get the URL for a named route:**
  
	$url = URL::route('profile');

Sometimes you may need to generate a URL to a named route, but also need to specify the values that should be used instead of the route's URI wildcards. It's easy to replace the wildcards with proper values:

**Get the URL for a named route with wildcard values:**

	$url = URL::route('profile', [$username]);
	
<a name="urls-to-routes"></a>
## URLs To Controller Actions

**Get the URL for a controller action:**

	$url = URL::action('UserController@getProfile');

**Get the URL for a controller action with wildcard values:**

	$url = URL::action('UserController@profile', [$username]);

<a name="urls-to-assets"></a>
## URLs To Assets

**Get the URL for an asset:**

	$url = URL::asset('js/jquery.js');

<a name="secure-urls"></a>
## Secure URLs

You can generate secure (https) versions of the URLs by replacing route, action or asset with `secure`

	$url = URL::secure('login');

	$url = URL::secure('profile', [$username]);

	$url = URL::secure('UserController@profile, [$username]');

There is no helper for secure, so you always have to use the full `URL::secure()`

<a name="helpers"></a>	
## Helpers
There are several helper functions for generating URLs designed to make your life easier and your code cleaner:

**Generating a URL relative to the base URL:**

	$url = url('user/profile');
	
**Get the URL for an asset:**

	$url = asset('js/jquery.js');
	
**Get the URL for a named route:**

	$url = route('profile');
	
**Get the URL for a named route with wildcard values:**

	$url = route('profile', [$username]);
	
**Get the URL for a controller action:**

	$url = action('UserController@profile');
	
**Get the URL for a controller action with wildcard values:**

	$url = action('UserController@profile', [$username]);