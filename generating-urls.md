# Generating urls

- [Introduction](#introduction)
- [URLs To Routes](#urls-to-routes)
- [URLs To Controller Actions](#urls-to-controller-actions)
- [URLs To Assets](#urls-to-assets)
- [Relatvie URLs](#relative-vs-absolute)
- [Secure URLs](#secure-urls)
- [Helpers](#helpers)

<a name="introduction"></a>
## Introduction

<a name="helpers"></a>
## Helpers
For several of the URL generating methods described below there is a shorter helper version. This is convenient to, for instance, make your templates look cleaner. The examples of helpers below will blade oriented, but the helpers are of course also available outside of the blade and template realm as well.

<a name="urls-to-routes"></a>
## URLs To Routes

**Get the URL for a named route**
  
	$url = URL::route('profile');

	{{ route('profile') }}

Sometimes you may need to generate a URL to a named route, but also need to specify the values that should be used instead of the route's URI wildcards. It's easy to replace the wildcards with proper values:

**Get the URL for a named route with wildcard values**

	$url = URL::route('profile', [$username]);

	{{ route('profile', [$username]) }}

The aliases are of course available outside of templates as well. Don't forget to use tripple curly brackets when you don't want the data to be escaped. (read more in the [Templates](/docs/templates#blade-templating-engine) section)

<a name="urls-to-controller-actions"></a>
## URLs To Controller Actions

**Get the URL for a controller action**

	$url = URL::action('UserController@getProfile');

	{{ action('UserController@getProfile') }}

**Get the URL for a controller action with wildcard values**

	$url = URL::action('UserController@profile', [$username]);

	{{ action('UserController@profile', [$username]) }}

**Get the url of a restful controller**

Getting URLs for [resource controllers](/docs/controllers#resource-controllers) work just the same way as other controllers.

	$url = URL::action('PhotoController@index');

	$url = URL::action('PhotoController@show' [$photo_id]);

<a name="urls-to-assets"></a>
## URLs To Assets

**Get the URL for an asset**

	$url = URL::asset('js/jquery.js');

	{{ asset('js/jquery.js') }}

<a name="relative-vs-absolute"></a>
## Relative URLs

By default all generated URLs are absolute. If you would like to generate relative URLs instead, supply a third argument to the URL method with a `false` value.

	$url = URL::action('PhotoController@index', [], false);

Notice the empty array is needed if you don't want to supply a value.

<a name="secure-urls"></a>
## Secure URLs

You can generate secure (https) versions of the URLs by replacing route or action with `secure` or sending `false` as the the second parameter `asset`.

	$url = URL::secure('login');

	$url = URL::secure('profile', [$username]);

	$url = URL::secure('UserController@profile', [$username]);

	$url = URL::asset('js/jquery.js', true);

There is no helper for secure, so you always have to use the full `URL::secure()`
