# Attributes

- [Introduction](#introduction)
- [Attributes reference](#attributes-reference)
    - [First party](#attributes-reference-first-party)
    - [From depencencies](#attributes-reference-from-dependencies)
    - [Third party packages](#attributes-reference-third-party)

<a name="introduction"></a>
## Introduction

> [!NOTE]
> PHP attributes are not to be confused with [Eloquent model attributes](/docs/{{version}}/eloquent).

[PHP attributes](https://www.php.net/manual/en/language.attributes.overview.php), formerly known as [Annotations](https://www.doctrine-project.org/projects/doctrine-annotations/en/2.0/index.html) in Doctrine as well as Java, and as Decorators in Python, Javascript, are a feature to annotate or decorate a class, function or variable with metadata which might be used to manipulate its behavior.

In PHP, the attributes are not executed. If the developer wants them to do something, they have to use the [Reflection API](https://www.php.net/manual/en/class.reflectionattribute.php). Laravel, however, comes with built-in attributes which can be loaded via the [service container](/docs/{{version}}/container#contextual-attributes). and can use its features.

<a name="attributes-reference"></a>
## Attributes reference

<a name="attributes-reference-first-party"></a>
### First party

<div class="overflow-auto">

| Attribute | Reference |
| --- | --- |
| [`\Illuminate\Database\Eloquent\Attributes\ScopedBy`](https://github.com/illuminate/database/blob/{{version}}/Eloquent/Attributes/ScopedBy.php) | [Applying global scopes to eloquent models](/docs/{{version}}/eloquent#applying-global-scopes) |
| [`\Illuminate\Database\Eloquent\Attributes\ObservedBy`](https://github.com/illuminate/database/blob/{{version}}/Eloquent/Attributes/ObservedBy.php) | [Eloquent model observers](/docs/{{version}}/eloquent#observers) |
| [`\Illuminate\Database\Eloquent\Attributes\CollectedBy`](https://github.com/illuminate/database/blob/{{version}}/Eloquent/Attributes/CollectedBy.php) | [Eloquent collections](/docs/{{version}}/eloquent-collections) |
| [`\Illuminate\Queue\Attributes\WithoutRelations`](https://github.com/illuminate/queue/blob/{{version}}/Attributes/WithoutRelations.php) | [Eloquent model relationships in queued jobs](/docs/{{version}}/queues#handling-relationships) |
| [`\Illuminate\Queue\Attributes\DeleteWhenMissingModels`](https://github.com/illuminate/queue/blob/{{version}}/Attributes/DeleteWhenMissingModels.php) | [Ignoring missing eloquent models in queued jobs](/docs/{{version}}/queues#ignoring-missing-models) |

</div>

<a name="attributes-reference-from-dependencies"></a>
### From dependencies

<div class="overflow-auto">

| Attribute | Reference |
| --- | --- |
| [PHPUnit attributes](https://docs.phpunit.de/en/11.4/attributes.html) (`#[Test]`, `#[TestDox(…)]`, `#[DataProvider(…)]`, etc.) | [Testing](/docs/{{version}}/testing#creating-tests) |
| [Symfony command attribues](https://symfony.com/doc/current/console.html#creating-a-command) (`#[AsCommand(…)]`, etc.) | [Artisan commands](/docs/{{version}}/artisan#writing-commands) |

</div>

<a name="attributes-reference-third-party"></a>
### Third party

<div class="overflow-auto">

| Attribute | Reference |
| --- | --- |
| [`spatie/laravel-route-attributes`](https://github.com/spatie/laravel-route-attributes) | [Routing](/{{version}}/routing)/[Controllers](/docs/{{version}}/controllers) |

</div>
