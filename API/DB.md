# DB

This object contains methods to interact with the database.

Set up your database information in the `config/database.php` file, or `config/local/database.php`, or whichever envionment you are using or plan to use. Also set up environment detection in `bootstrap/start.php`. See [Configuration](/doc/configuration.php) for more details.

___

### DB::select()

#### Usage



#### Examples

___


### DB::insert()

This method inserts a new row into a table with the provided values.

#### Usage

	DB::insert('INSERT_QUERY', PARAMETERS)

`INSERT_QUERY` should be an SQL inert query, with questions marks (`?`) in place of the values, like in a prepared statement.

`PARAMETERS` should be an array containing the values, the the order they are paced in the `INSERT_QUERY`.

#### Examples

	$params = array($input['name'], $input['popularity'], 0, 0, $input['status'], $input['outlook'], $input['notes']);
	DB::insert('INSERT INTO products (name, popularity, launch, closed, status, outlook, notes) VALUES (?, ?, ?, ?, ?, ?, ?)', $params);

___


### DB::update()

#### Usage



#### Examples


___


### DB::delete()

#### Usage



#### Examples


___