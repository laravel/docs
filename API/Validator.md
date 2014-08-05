## Route

The `Validator` object contains functions to validate forms.

- [Make](#make)

___

<a name="make"></a>

### Validator::makes()

This method performs a validation.

#### Usage

	$val = Validator::make(VALIDATION_INPUT, VALIDATION_RULES);

VALIDATION_INPUT should an associative array with the items being validated.

VALIDATION_RULES should be an associative array with the validaiton rules.

#### Vaidation rules

`required` - Used to make the item required to pass validation.

`unique:TABLE` - Used to require the entry to be unique amongst the defined table. `TABLE` should be a database table. Used for requiring uniue usernames or email addresses.

`email` - Used to require that the value entered is an email address.

`min:NUM` - User to require a minimum number of characters for an input. `NUM` should be the number of characters, eg. `min:8`.

`max:NUM` - Used to require a maximum number of characters.

`confirmed` - Used to require the user input their information twice for verification. Used for passwords or email addresses.

`AlphaNum` - Used to require the input be only alphabatical and numerical characters.

`Integar` - Used to require the input be only numbers.

#### Examples

Gets the input, sets the rules, validates and attempts `Auth` if successful. Returns "please try again" if not successful.

	$input = Input::all();
	$rules = array('email' => 'required', 'password' => 'required');
	$val = Validator::make($input, $rules);
	if(val->fails())
		return "Please try again";
	else
		Auth::attempt($input);


___