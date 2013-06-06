# Helpers

This is a list of available helper functions found in Illuminate\Support

- [Global Functions](#global-functions)
- [Str](#str)

<a name="global-functions"></a>
## Global Functions

A full list of global functions can be found here: http://laravel.com/api/packages/Default.html

*Dump the passed variables and end the script*
    
    dd($value); // Short for die(var_dump($value));

*Escape HTML entities in a strng*
    
    e($value);

<a name="str"></a>
## Str

Str provides some helper functions to easily format strings in a variety of ways.

A full list of `Str` functions can be found here: http://laravel.com/api/classes/Illuminate.Support.Str.html

*Converting a value to camelCase*
    
    $value = 'laravel helper-functions';
    echo Str::camel($value); // Outputs: laravelHelperFunctions

*Limit the number of characters in a string*

    $value = 'This string is 28 characters';
    echo Str::limit($value, 20); // Outputs: This string is 28 ch...

*Limit the number of words in a strng*

    $value = 'There are four words';
    echo Str::word($value, 3); // Outputs: There are four...

*Generate a URL friendly "slug" from a given string*

    $value = 'This is my title';
    echo Str::slug($value); // Outputs: this-is-my-title

*Convert a string to snake case*

    $value = 'Another Fine Example';
    echo Str::snake($value); // Outputs:: another_fine_example

*Convert a string to studly caps case*

    $value = 'Here we go again';
    echo Str::studly($value); // Outputs:: HereWeGoAgain

You can also register your own macro by calling:

    Str::macro($name, $macro);s

