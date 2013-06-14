# 分页

- [配置](#configuration)
- [基本用法](#usage)
- [给分页链接添加自定义信息](#appending-to-pagination-links)

<a name="configuration"></a>
## 配置

在其它的框架中，分页有时很痛苦. 但是Laravel让分页简单到不可思议. 默认Laravel包含了两个分页视图, 在`app/config/view.php` 文件中的pagination选项中指定分页链接具体使用哪一个视图.

`pagination::slider`视图 基于当前所在页数给出一个浮动的页数范围,`pagination::simple` 视图只是简单的给出 '上一页' '下一页' 两个链接. **两个视图都能完美的和bootstrap框架结合**

<a name="usage"></a>
## 基本用法

Laravel有多种方式实现分页. 最简单的是在普通查询或Eloquent模型查询中使用 `paginate` 方法.

**从数据库查询中分页**

	$users = DB::table('users')->paginate(15);

也可以从 [Eloquent](/docs/eloquent) 模型中分页:

**从一个 Eloquent 模型中分页**

	$users = User::where('votes', '>', 100)->paginate(15);

你只需要吧每页查询的记录数传给`paginate`方法即可. 在获得包含分页的查询结果集之后, 就可以在视图中展示了, 在视图中输出分页链接使用 `links` 方法:

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->links(); ?>

以上就是创建一个分页链接的所需的所有信息了! 我们还没有提到Laravel做了什么. Laravel会自己吧其它的事情做完.

你也可以通过下面的方法获取关于分页更加详尽的信息:

- `getCurrentPage`
- `getLastPage`
- `getPerPage`
- `getTotal`
- `getFrom`
- `getTo`

有时你可能希望自定义分页, 只需使用 `Paginator::make` 方法,并把 记录集合(array), 总记录数(int), 每页记录数(int) 参数放在数组里:

**自定义分页**

	$paginator = Paginator::make($items, $totalItems, $perPage);

<a name="appending-to-pagination-links"></a>
## 给分页链接添加自定义信息

可以通过分页器的 `appends` 方法为分页链接添加上自定查询字符串:

	<?php echo $users->appends(array('sort' => 'votes'))->links(); ?>

最后产生的url如下:

	http://example.com/something?page=2&sort=votes
