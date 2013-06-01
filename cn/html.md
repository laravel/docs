# 表单 & HTML

- [创建表单](#opening-a-form)
- [CSRF防御机制](#csrf-protection)
- [表单与模型绑定](#form-model-binding)
- [Label 标签](#labels)
- [单行文本、多行文本、密码和隐藏表单域](#text)
- [多选框和单选框](#checkboxes-and-radio-buttons)
- [文件上传](#file-input)
- [下拉菜单](#drop-down-lists)
- [按钮](#buttons)
- [自定义宏](#custom-macros)

<a name="opening-a-form"></a>
## 创建表单

**创建表单**

	{{ Form::open(array('url' => 'foo/bar')) }}
		//
	{{ Form::close() }}

默认使用 `POST` 方法；当然，你也可以指定使用其他方法提交表单：

	echo Form::open(array('url' => 'foo/bar', 'method' => 'put'))

> **注意：** 因为 HTML 表单只支持 `POST` 方法，在使用 `PUT` 和 `DELETE` 方法时框架会自动通过一个 `_method` 隐藏域来发送伪装的方法信息。

你也可以创建一个表单指向已定义的路由或者控制器操作：

	echo Form::open(array('route' => 'route.name'))

	echo Form::open(array('action' => 'Controller@method'))

如果你需要在表单中上传文件，请添加一个 `files` 参数到数组中：

	echo Form::open(array('url' => 'foo/bar', 'files' => true))

<a name="csrf-protection"></a>
## CSRF防御机制

Laravel框架提供了一种简单的方法帮助你的应用抵御CSRF（跨站请求伪造）式攻击。Laravel框架会自动在用户 session 中存放一个随机令牌（token），并且将这个令牌作为一个隐藏字段包含在表单信息中。当然，你也可以使用表单的 `token` 方法直接调用令牌字段的HTML代码：

**添加CSRF令牌到表单中**

	echo Form::token();
	//译者注，调用结果类似： <input name="_token" type="hidden" value="BndR9iWzoKiseXuADa7gwzG5zf2ZKK3pPiRNvOGE">

**在路由中附加CSRF过滤器**

	Route::post('profile', array('before' => 'csrf', function()
	{
		//
	}));

<a name="form-model-binding"></a>
## 表单与模型绑定

你可以使用 `Form::model` 方法将模型中的内容填充到表单中去：

**创建一个模型表单**

	echo Form::model($user, array('route' => array('user.update', $user->id)))

当你创建一个表单元素（如文本输入字段）时，表单域的值会被自动设置成与之匹配的模型属性的值。例如表单中name属性为 `email` 的文本域的值会被设置为用户模型中 `email` 属性的值。不仅仅这样，当Session数据中有项目与表单域名称相匹配，Session值的填充优先级会高于模型的值。具体的优先级如下：

1. Session 数据 （旧的输入数据）
2. 已传输的数据
3. 模型属性数据

这可以帮助你快速建立与模型绑定的表单，而且当服务器端验证出表单错误时可以轻松回填数据！

> **注意：** 当你使用 `Form::model` 时，别忘了在表单结尾处加上 `Form::close` ！

<a name="labels"></a>
## Label 标签

**获取一个 label 标签元素**

	echo Form::label('email', 'E-Mail Address');
	//译者注，输出结果为： <label for="email">E-Mail Address</label>

**设定其他 HTML 标签属性**

	echo Form::label('email', 'E-Mail Address', array('class' => 'awesome'));
	//译者注，输出结果为： <label for="email" class="awesome">E-Mail Address</label>

> **注意：** 当你创建了一个label标签后，name值与之相匹配的表单元素会被自动加上一个同名的ID属性。

<a name="text"></a>
## 单行文本、多行文本、密码和隐藏表单域

**获取一个单行文本域**

	echo Form::text('username');
	//译者注，输出结果为： <input name="username" type="text">

**设置一个默认的值**

	echo Form::text('email', 'example@gmail.com');
	//译者注，输出结果为： <input name="email" type="text" value="example@gmail.com">

> **注意：** 调用 *hidden* 隐藏域和 *textarea* 多行文本表单域的方法和调用 *text* 单行文本域的方法是一样的。

**获取一个密码域**

	echo Form::password('password');
	//译者注，输出结果为： <input name="password" type="password" value="">

<a name="checkboxes-and-radio-buttons"></a>
## 多选框和单选框

**获取一个多选框和单选框**

	echo Form::checkbox('name', 'value');
	//译者注，输出结果为： <input name="name" type="checkbox" value="value">
	echo Form::radio('name', 'value');
	//译者注，输出结果为： <input name="name" type="radio" value="value">

**获取一个已选中的多选框和单选框**

	echo Form::checkbox('name', 'value', true);
	//译者注，输出结果为： <input checked="checked" name="name" type="checkbox" value="value">
	echo Form::radio('name', 'value', true);
	//译者注，输出结果为： <input checked="checked" name="name" type="radio" value="value">

<a name="file-input"></a>
## 文件上传

**获取一个文件上传域**

	echo Form::file('image');
	//译者注，输出结果为： <input name="image" type="file">

<a name="drop-down-lists"></a>
## 下拉菜单

**获取一个下拉菜单**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'));
	//译者注，输出结果为： <select name="size"><option value="L">Large</option><option value="S">Small</option></select>

**获取一个已选中默认值的下拉菜单**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'), 'S');
	//译者注，输出结果为： <select name="size"><option value="L">Large</option><option value="S" selected="selected">Small</option></select>

**获取一个分组下拉菜单**

	echo Form::select('animal', array(
		'Cats' => array('leopard' => 'Leopard'),
		'Dogs' => array('spaniel' => 'Spaniel'),
	));
	//译者注，输出结果为： <select name="animal"><optgroup label="Cats"><option value="leopard">Leopard</option></optgroup><optgroup label="Dogs"><option value="spaniel">Spaniel</option></optgroup></select>

<a name="buttons"></a>
## 按钮

**获取一个提交按钮**

	echo Form::submit('Click Me!');
	//译者注，输出结果为： <input type="submit" value="Click Me!">

> **注意：** 如果需要创建一个单独的表单元素，可以使用 *button* 方法。它的调用方式和 *submit* 方法一样。

<a name="custom-macros"></a>
## 自定义宏

你可以轻松定义一个表单宏来帮助你创建表单。下面是使用表单宏的方法，注册一个宏名称，然后在闭包函数中定义对应的操作：

**注册一个表单宏**

	Form::macro('myField', function()
	{
		return '<input type="awesome">';
	});

然后你就可以使用刚刚定义的宏名称调用它：

**调用一个自定义表单宏**

	echo Form::myField();
