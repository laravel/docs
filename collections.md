# 集合

- [介紹](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 介紹

`Illuminate\Support\Collection` 類別提供一個流暢、方便的封裝來操作陣列資料。舉個例子，查看下面的程式碼。我們將會使用 `collect` 輔助方法來用陣列建立一個新的集合實例：

	$collection = collect(['taylor', 'abigail', null])->map(function($name)
	{
		return strtoupper($name);
	})
	->reject(function($name)
	{
		return is_null($value);
	});


就如你所見，`Collection` 類別允許你串接它的方法對背後的陣列執行流暢的映射和歸納。一般說來，每一個 `Collection` 的方法都回傳一個全新的 `Collection` 實例。為了更深一步的了解，請繼續閱讀！

<a name="basic-usage"></a>
## 基本用法

#### 建立集合

如上述，`collect` 輔助方法將會用給定的陣列回傳一個新的 `Illuminate\Support\Collection` 實例。你也可以在 `Collection` 類別上使用 `make` 指令：

	$collection = collect([1, 2, 3]);

	$collection = Collection::make([1, 2, 3]);

當然，[Eloquent](/docs/5.0/eloquent) 的物件集合總是以 `Collection` 實例回傳；然而，你可以在應用程式的任何地方方便的使用 `Collection` 類別。

#### 探索集合

作為列出集合可以用的所有方法 (有很多) 的替代，請查看 [類別的 API 文件](http://laravel.com/api/master/Illuminate/Support/Collection.html)！
