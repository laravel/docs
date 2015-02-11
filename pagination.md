# Pagination

- [Configuration](#configuration)
- [Usage](#usage)
- [Appending To Pagination Links](#appending-to-pagination-links)
- [Converting To JSON](#converting-to-json)
- [Custom Presenters](#custom-presenters)

<a name="configuration"></a>
## Configuration

In other frameworks, pagination can be very painful. Laravel makes it a breeze. There is a single configuration option in the `app/config/view.php` file. The `pagination` option specifies which view should be used to create pagination links. By default, Laravel includes two views.

The `pagination::slider` view will show an intelligent "range" of links based on the current page, while the `pagination::simple` view will simply show "previous" and "next" buttons. **Both views are compatible with Twitter Bootstrap out of the box.**

<a name="usage"></a>
## Usage

There are several ways to paginate items. The simplest is by using the `paginate` method on the query builder or an Eloquent model.

#### Paginating Database Results

	$users = DB::table('users')->paginate(15);

> **Note:** Currently, pagination operations that use a `groupBy` statement cannot be executed efficiently by Laravel. If you need to use a `groupBy` with a paginated result set, it is recommended that you query the database manually and use `Paginator::make`.

#### Paginating An Eloquent Model

You may also paginate [Eloquent](/docs/4.2/eloquent) models:

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

The argument passed to the `paginate` method is the number of items you wish to display per page. Once you have retrieved the results, you may display them on your view, and create the pagination links using the `links` method:

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->links(); ?>

This is all it takes to create a pagination system! Note that we did not have to inform the framework of the current page. Laravel will determine this for you automatically.

If you would like to specify a custom view to use for pagination, you may pass a view to the `links` method:

	<?php echo $users->links('view.name'); ?>

You may also access additional pagination information via the following methods:

- `getCurrentPage`
- `getLastPage`
- `getPerPage`
- `getTotal`
- `getFrom`
- `getTo`
- `count`


#### "Simple Pagination"

If you are only showing "Next" and "Previous" links in your pagination view, you have the option of using the `simplePaginate` method to perform a more efficient query. This is useful for larger datasets when you do not require the display of exact page numbers on your view:

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### Creating A Paginator Manually

Sometimes you may wish to create a pagination instance manually, passing it an array of items. You may do so using the `Paginator::make` method:

	$paginator = Paginator::make($items, $totalItems, $perPage);

#### Customizing The Paginator URI

You may also customize the URI used by the paginator via the `setBaseUrl` method:

	$users = User::paginate();

	$users->setBaseUrl('custom/url');

The example above will create URLs like the following: http://example.com/custom/url?page=2

<a name="appending-to-pagination-links"></a>
## Appending To Pagination Links

You can add to the query string of pagination links using the `appends` method on the Paginator:

	<?php echo $users->appends(array('sort' => 'votes'))->links(); ?>

This will generate URLs that look something like this:

	http://example.com/something?page=2&sort=votes

If you wish to append a "hash fragment" to the paginator's URLs, you may use the `fragment` method:

	<?php echo $users->fragment('foo')->links(); ?>

This method call will generate URLs that look something like this:

	http://example.com/something?page=2#foo

<a name="converting-to-json"></a>
## Converting To JSON

The `Paginator` class implements the `Illuminate\Support\Contracts\JsonableInterface` contract and exposes the `toJson` method. You may also convert a `Paginator` instance to JSON by returning it from a route. The JSON'd form of the instance will include some "meta" information such as `total`, `current_page`, `last_page`, `from`, and `to`. The instance's data will be available via the `data` key in the JSON array.

<a name="custom-presenters"></a>
## Custom Presenters

The default pagination presenter is Bootstrap compatible out of the box; however, you may customize this with a presenter of your choice.

### Extending The Abstract Presenter

Extend the `Illuminate\Pagination\Presenter` class and implement its abstract methods. An example presenter for Zurb Foundation might look like this:

    class ZurbPresenter extends Illuminate\Pagination\Presenter {

        public function getActivePageWrapper($text)
        {
            return '<li class="current"><a href="">'.$text.'</a></li>';
        }

        public function getDisabledTextWrapper($text)
        {
            return '<li class="unavailable"><a href="">'.$text.'</a></li>';
        }

        public function getPageLinkWrapper($url, $page, $rel = null)
        {
            return '<li><a href="'.$url.'">'.$page.'</a></li>';
        }

    }

### Using The Custom Presenter

First, create a view in your `app/views` directory that will serve as your custom presenter. Then, replace `pagination` option in the `app/config/view.php` configuration file with the new view's name. Finally, the following code would be placed in your custom presenter view:

    <ul class="pagination">
        <?php echo with(new ZurbPresenter($paginator))->render(); ?>
    </ul>
