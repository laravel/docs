# Views

- [Views](#views)
  - [Creating & Rendering Views](#creating--rendering-views)
    - [Nested View Directories](#nested-view-directories)
    - [Creating The First Available View](#creating-the-first-available-view)
    - [Determining If A View Exists](#determining-if-a-view-exists)
  - [Passing Data To Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
  - [View Composers](#view-composers)
      - [Attaching A Composer To Multiple Views](#attaching-a-composer-to-multiple-views)
    - [View Creators](#view-creators)
  - [Optimizing Views](#optimizing-views)

<a name="creating-and-rendering-views"></a>
## Creating & Rendering Views



<a name="nested-view-directories"></a>
### Nested View Directories


<a name="creating-the-first-available-view"></a>
### Creating The First Available View


<a name="determining-if-a-view-exists"></a>
### Determining If A View Exists

    }

<a name="passing-data-to-views"></a>
## Passing Data To Views


<a name="sharing-data-with-all-views"></a>
### Sharing Data With All Views


<a name="view-composers"></a>
## View Composers


 

<a name="attaching-a-composer-to-multiple-views"></a>
#### Attaching A Composer To Multiple Views

You may attach a view composer to multiple views at once by passing an array of views as the first argument to the `composer` method:

    use App\Views\Composers\MultiComposer;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

The `composer` method also accepts the `*` character as a wildcard, allowing you to attach a composer to all views:

    View::composer('*', function ($view) {
        //
    });

<a name="view-creators"></a>
### View Creators

View "creators" are very similar to view composers; however, they are executed immediately after the view is instantiated instead of waiting until the view is about to render. To register a view creator, use the `creator` method:

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## Optimizing Views

By default, Blade template views are compiled on demand. When a request is executed that renders a view, Laravel will determine if a compiled version of the view exists. If the file exists, Laravel will then determine if the uncompiled view has been modified more recently than the compiled view. If the compiled view either does not exist, or the uncompiled view has been modified, Laravel will recompile the view.

Compiling views during the request may have a small negative impact on performance, so Laravel provides the `view:cache` Artisan command to precompile all of the views utilized by your application. For increased performance, you may wish to run this command as part of your deployment process:

```shell
php artisan view:cache
```

You may use the `view:clear` command to clear the view cache:

```shell
php artisan view:clear
```

