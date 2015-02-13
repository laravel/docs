# 分页

- [设置](#configuration)
- [使用](#usage)
- [追加分页链接](#appending-to-pagination-links)
- [转换至 JSON](#converting-to-json)

<a name="configuration"></a>
## 设置

在其他的框架中，实作分页是令人感到苦恼的事，但是 Laravel 令它实作起来变得轻松。 Laravel 可以产生基于当前页面的智能「范围」链接，所产生的 HTML 兼容 Bootstrap CSS 框架.

<a name="usage"></a>
## 使用

有几种方法来分页项目。最简单的是在搜索建立器使用 `paginate` 方法或 Eloquent 模型。

#### 对数据库结果分页

	$users = DB::table('users')->paginate(15);

> **注意：** 目前 Laravel 使用 `groupBy` 来做分页操作无法有效率的执行，如果您需要使用 `groupBy` 来分页数据集，建议您手动查找数据库，并使用 `Paginator::make`。

#### 对 Eloquent 模型分页

您也可以对 [Eloquent](/docs/5.0/eloquent) 模型分页:

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

发送给 `paginate` 方法的参数是您希望每页要显示的项目选项数目，只要您取得查找结果后，您可以在视图中显示，并使用 `render` 方法去建立分页链接：

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->render(); ?>

这就是所有建立分页系统的步骤了！您会注意到我们还没有告知 Laravel 我们目前的页面是哪一页，这个信息 Laravel 会自动帮您做好。

您也可以透过以下方法获得额外的分页信息：

- `currentPage`
- `lastPage`
- `perPage`
- `total`
- `count`

#### 「简单分页」

如果您只是要在您的分页视图显示「上一页」和「下一页」链接，您有个选项 `simplePaginate` 方法来执行更高效率的搜索。当您不需要精准的显示页码在视图上时，这个方法在较大的数据集非常有用：

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### 手动建立分页

有的时候您可能会想要从数组中项目手动建立分页实体， 您可以根据您的需要透过 `Illuminate\Pagination\Paginator` 或 `Illuminate\Pagination\LengthAwarePaginator` 实体来建立。

#### 自订分页 URL

您还可以透过 `setPath` 方法自订使用的 URL：

	$users = User::paginate();

	$users->setPath('custom/url');

上面的范例将建立 URL，类似以下内容：
http://example.com/custom/url?page=2

<a name="appending-to-pagination-links"></a>
## 追加分页链接

您可以使用 `appends` 方法增加搜索字串到分页链接中：

	<?php echo $users->appends(['sort' => 'votes'])->render(); ?>

这样会产生类似下列的链接：

	http://example.com/something?page=2&sort=votes

如果您想要将「哈希片段」加到分页的 URL，您可以使用 `fragment` 方法：

	<?php echo $users->fragment('foo')->render(); ?>

此方法调用后将产生 URL，看起来像这样：

	http://example.com/something?page=2#foo

<a name="converting-to-json"></a>
## 转换至 JSON

`Paginator` 类别实作 `Illuminate\Contracts\Support\JsonableInterface` 接口的 `toJson` 方法。由路由返回的值，您可能将 `Paginator` 实体传换成 JSON。JSON 表单的实体会包含一些「后设」信息，例如 `total`、`current_page`、`last_page`。该实体数据将可透过在 JSON 数组中 `data` 的键取得。
