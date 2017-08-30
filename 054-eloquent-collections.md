# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

<a name="introduction"></a>
## Introduction

All multi-result sets returned by Eloquent are instances of the `Illuminate\Database\Eloquent\Collection` object, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends the Laravel [base collection](/docs/{{version}}/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models.

Of course, all collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays:

    $users = App\User::where('active', 1)->get();

    foreach ($users as $user) {
        echo $user->name;
    }

However, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, let's remove all inactive models and gather the first name for each remaining user:

    $users = App\User::where('active', 1)->get();

    $names = $users->reject(function ($user) {
        return $user->active === false;
    })
    ->map(function ($user) {
        return $user->name;
    });

> {note} While most Eloquent collection methods return a new instance of an Eloquent collection, the `pluck`, `keys`, `zip`, `collapse`, `flatten` and `flip` methods return a [base collection](/docs/{{version}}/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be automatically cast to a base collection.

<a name="available-methods"></a>
## Available Methods

### The Base Collection

All Eloquent collections extend the base [Laravel collection](/docs/{{version}}/collections) object; therefore, they inherit all of the powerful methods provided by the base collection class:

<style>
    #collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    #collection-method-list a {
        display: block;
    }
</style>

<div id="collection-method-list" markdown="1">

[all](/docs/{{version}}/collections#method-all)
[average](/docs/{{version}}/collections#method-average)
[avg](/docs/{{version}}/collections#method-avg)
[chunk](/docs/{{version}}/collections#method-chunk)
[collapse](/docs/{{version}}/collections#method-collapse)
[combine](/docs/{{version}}/collections#method-combine)
[contains](/docs/{{version}}/collections#method-contains)
[containsStrict](/docs/{{version}}/collections#method-containsstrict)
[count](/docs/{{version}}/collections#method-count)
[diff](/docs/{{version}}/collections#method-diff)
[diffKeys](/docs/{{version}}/collections#method-diffkeys)
[each](/docs/{{version}}/collections#method-each)
[every](/docs/{{version}}/collections#method-every)
[except](/docs/{{version}}/collections#method-except)
[filter](/docs/{{version}}/collections#method-filter)
[first](/docs/{{version}}/collections#method-first)
[flatMap](/docs/{{version}}/collections#method-flatmap)
[flatten](/docs/{{version}}/collections#method-flatten)
[flip](/docs/{{version}}/collections#method-flip)
[forget](/docs/{{version}}/collections#method-forget)
[forPage](/docs/{{version}}/collections#method-forpage)
[get](/docs/{{version}}/collections#method-get)
[groupBy](/docs/{{version}}/collections#method-groupby)
[has](/docs/{{version}}/collections#method-has)
[implode](/docs/{{version}}/collections#method-implode)
[intersect](/docs/{{version}}/collections#method-intersect)
[isEmpty](/docs/{{version}}/collections#method-isempty)
[isNotEmpty](/docs/{{version}}/collections#method-isnotempty)
[keyBy](/docs/{{version}}/collections#method-keyby)
[keys](/docs/{{version}}/collections#method-keys)
[last](/docs/{{version}}/collections#method-last)
[map](/docs/{{version}}/collections#method-map)
[mapWithKeys](/docs/{{version}}/collections#method-mapwithkeys)
[max](/docs/{{version}}/collections#method-max)
[median](/docs/{{version}}/collections#method-median)
[merge](/docs/{{version}}/collections#method-merge)
[min](/docs/{{version}}/collections#method-min)
[mode](/docs/{{version}}/collections#method-mode)
[nth](/docs/{{version}}/collections#method-nth)
[only](/docs/{{version}}/collections#method-only)
[partition](/docs/{{version}}/collections#method-partition)
[pipe](/docs/{{version}}/collections#method-pipe)
[pluck](/docs/{{version}}/collections#method-pluck)
[pop](/docs/{{version}}/collections#method-pop)
[prepend](/docs/{{version}}/collections#method-prepend)
[pull](/docs/{{version}}/collections#method-pull)
[push](/docs/{{version}}/collections#method-push)
[put](/docs/{{version}}/collections#method-put)
[random](/docs/{{version}}/collections#method-random)
[reduce](/docs/{{version}}/collections#method-reduce)
[reject](/docs/{{version}}/collections#method-reject)
[reverse](/docs/{{version}}/collections#method-reverse)
[search](/docs/{{version}}/collections#method-search)
[shift](/docs/{{version}}/collections#method-shift)
[shuffle](/docs/{{version}}/collections#method-shuffle)
[slice](/docs/{{version}}/collections#method-slice)
[sort](/docs/{{version}}/collections#method-sort)
[sortBy](/docs/{{version}}/collections#method-sortby)
[sortByDesc](/docs/{{version}}/collections#method-sortbydesc)
[splice](/docs/{{version}}/collections#method-splice)
[split](/docs/{{version}}/collections#method-split)
[sum](/docs/{{version}}/collections#method-sum)
[take](/docs/{{version}}/collections#method-take)
[tap](/docs/{{version}}/collections#method-tap)
[toArray](/docs/{{version}}/collections#method-toarray)
[toJson](/docs/{{version}}/collections#method-tojson)
[transform](/docs/{{version}}/collections#method-transform)
[union](/docs/{{version}}/collections#method-union)
[unique](/docs/{{version}}/collections#method-unique)
[uniqueStrict](/docs/{{version}}/collections#method-uniquestrict)
[values](/docs/{{version}}/collections#method-values)
[when](/docs/{{version}}/collections#method-when)
[where](/docs/{{version}}/collections#method-where)
[whereStrict](/docs/{{version}}/collections#method-wherestrict)
[whereIn](/docs/{{version}}/collections#method-wherein)
[whereInStrict](/docs/{{version}}/collections#method-whereinstrict)
[whereNotIn](/docs/{{version}}/collections#method-wherenotin)
[whereNotInStrict](/docs/{{version}}/collections#method-wherenotinstrict)
[zip](/docs/{{version}}/collections#method-zip)

</div>

<a name="custom-collections"></a>
## Custom Collections

If you need to use a custom `Collection` object with your own extension methods, you may override the `newCollection` method on your model:

    <?php

    namespace App;

    use App\CustomCollection;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Create a new Eloquent Collection instance.
         *
         * @param  array  $models
         * @return \Illuminate\Database\Eloquent\Collection
         */
        public function newCollection(array $models = [])
        {
            return new CustomCollection($models);
        }
    }

Once you have defined a `newCollection` method, you will receive an instance of your custom collection anytime Eloquent returns a `Collection` instance of that model. If you would like to use a custom collection for every model in your application, you should override the `newCollection` method on a base model class that is extended by all of your models.
