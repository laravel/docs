# Pagination

- [Configuration](#configuration)
- [Usage](#usage)
- [Appending to Pagination Links](#appending)

<a name="configuration"></a>
## Configuration

In other frameworks, pagination can be very painful. Laravel makes it a breeze. There is a single configuration option in the `app/config/view.php` file. The `pagination` option specifies which view should be used to create pagination links. By default, Laravel includes two views.

The `pagination::slider` view will show an intelligent "range" of links based on the current page, while the `pagination::simple` view will simply show "previous" and "next" buttons. **Both views are compatible with Twitter Bootstrap out of the box.**

<a name="usage"></a>
## Usage

There are several ways to paginate items. The simplest is by using the `paginate` method on the query builder or an Eloquent model.

**Paginating Database Results**

	$users = DB::table('users')->paginate(15);

You may also paginate [Eloquent](/docs/eloquent) models:

**Paginating An Eloquent Model**

	$users = User::where('votes', '>', 100)->paginate(15);

The argument passed to the `paginate` method is the number of items you wish to display per page. Once you have retrieved the results, you may display them on your view, and create the pagination links using the `links` method:

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->links(); ?>

This is all it takes to create a pagination system! Note that we did not have to inform the framework of the current page. Laravel will determine this for you automatically.

Sometimes you may wish to create a pagination instance manually, passing it an array of items. You may do so using the `Paginator::make` method:

**Creating A Paginator Manually**

	$paginator = Paginator::make($items, $totalItems, $perPage);

## Appending To Pagination Links

You may need to add more items to the pagination links' query strings, such as the column you're sorting by.

Appending to the query string of pagination links:

	<?php echo $users->appends(array('sort' => 'votes'))->links(); ?>

This will generate URLs that look something like this:

	http://example.com/something?page=2&sort=votes
