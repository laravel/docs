# Generating urls

- [Introduction](#introduction)
- [URLs To Routes](#urls-to-routes)
- [URLs To Controller Actions](#urls-to-controller-actions)

<a name="introduction"></a>
## Introduction



<a name="urls-to-routes"></a>
## URLs To Controller Actions

**Get the URL for a controller action:

  $url = URL::action('UserController@getProfile');

**Get the URL for a controller action with wildcard values:

$url = URL::to_action('user@profile', [$username]);

<a name="urls-to-controller-actions"></a>
## URLs To Routes

**Get the URL for a named route:
  
  $url = URL::route('profile');

Sometimes you may need to generate a URL to a named route, but also need to specify the values that should be used instead of the route's URI wildcards. It's easy to replace the wildcards with proper values:

**Get the URL for a named route with wildcard values:

  $url = URL::route('profile', [$username]);
