# DB

This object contains methods to interact with the database.

Set up your database information in the `config/database.php` file, or `config/local/database.php`, or whichever envionment you are using or plan to use. Also set up environment detection in `bootstrap/start.php`. See [Configuration](/doc/configuration.php) for more details.

- [Table](#table)
- [Select](#select)
- [First](#first)
- [Insert](#insert)
- [Update](#update)
- [Delete](#delete)
- [Update](#update)

- [Complete, auto-generated docs](/api/4.2/Illuminate/Database/Connection.html)

___

<a name="table"></a>

### DB::table()

This method specifies which table to perform the database actions in. It's usually used before [Where](#where)or other methods when using Query Builder.

#### Usage

	

#### Examples

___

<a name="select"></a>

### DB::select()

This method selects and returns all results for a query. To return one result, see [selectOne](#selectOne).

#### Usage



#### Examples

___

<a name="first"></a>

### DB::first()

This method executes a query and returns just the first result.

#### Usage

	

#### Examples

___

<a name="selectOne"></a>

### DB::selectOne()

This method selects and returns one result for a query. To return all results, see [select](#select).

#### Usage



#### Examples

___

<a name="insert"></a>

### DB::insert()

This method inserts a new row into a table with the provided values.

#### Query Builder Usage

	DB::table('TABLE_NAME')->insert();

#### SQL Usage

	DB::insert('INSERT_QUERY', PARAMETERS)

`INSERT_QUERY` should be an SQL inert query, with questions marks (`?`) in place of the values, like in a prepared statement.

`PARAMETERS` should be an array containing the values, the the order they are paced in the `INSERT_QUERY`.

#### Examples

	$params = array($input['name'], $input['popularity'], 0, 0, $input['status'], $input['outlook'], $input['notes']);
	DB::insert('INSERT INTO products (name, popularity, launch, closed, status, outlook, notes) VALUES (?, ?, ?, ?, ?, ?, ?)', $params);

___

<a name="update"></a>

### DB::update()

This method updates an existin database row.

#### Query Builder Usage
	


#### Quer Builder Examples

Gets input, finds specified row by `id`, updates row `visible` to `1`.

	$input = Input::all();
	DB::table('products')->where('id', '=', $input['approve'])->update(array('visible' => '1'));

___

<a name="delete"></a>

### DB::delete()

#### Query Builder Usage

	DB::table()->where(COLUMN, VALUE)->delete();

`COLUMN` should be the tables column that you want to search in.

`VALUE` should be the number or string you want to find, then delete the row of. 

#### Examples


___