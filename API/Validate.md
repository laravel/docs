## Route

The `Validate` object contains functions to validate forms.

- [Make](#make)

___

<a name="make"></a>

### Validate::makes()

This method performs a validation.

#### Usage

	$val = Validate::make(VALIDATION_INPUT, VALIDATION_RULES);

VALIDATION_INPUT should an associative array with the items being validated.

VALIDATION_RULES should be an associative array with the validaiton rules.

#### Vaidation rules

`required` - Used to make the item required to pass validation.

#### Examples

Gets the input, sets the rules, validates and attempts `Auth` if successful. Returns "please try again" if not successful.

	$input = Input::all();
	$rules = array('email' => 'required', 'password' => 'required');
	$val = Validate::make($rules, );
	if(val->fails())
		return "Please try again";
	else
		Auth::attempt($input);


___