def validate_drink_args(
    stand_alone_args: list[str],
    value_args: dict[str, any],
    args_tuple: tuple[str, ...]):
    """
    Validates a tuple of command-line style arguments.
    
    Args:
        valid_args: A list of valid argument flags, e.g., ['-t', '-v', '-o']
        args_tuple: A tuple of arguments, e.g., ('-t', 'test')
        
    Returns: 
        tuple(bool, Optional[str], Optional[str]): A tuple where the first element indicates
    """
    # Check for valid single arguments
    if len(args_tuple) == 1:
        if args_tuple[0] not in stand_alone_args:
            print(f"Arg {args_tuple[0]} not in {stand_alone_args}")
            return False, None, None
        return True, args_tuple[0], None

    # Check for valid value arguments
    if len(args_tuple) > 2:
        print(f"Too many arguments: {args_tuple}")
        return False, None, None
    
    arg, value = args_tuple
    value = value.strip().lower()

    if arg not in value_args or arg in stand_alone_args:
        print(f"Arg {arg} not in {value_args} or is in {stand_alone_args}")
        return False
    
    match arg:
        case "-i":
            if value not in value_args["-i"]:
                print(f"Value {value} not in {value_args['-i']}")
                return False, None, None
        case _:
            print(f"Unhandled arg: {arg}")
            return False, None, None

    return True, arg, value
