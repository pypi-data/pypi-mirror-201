"""
This module inserts prompting magics and allows to turn it on or off.

Examples:
    >>> import prompting
    >>> from .examples.person import Person

    >>> merlin = Person("Myrddin Wyllt", 42, "Caledonia") 


    >>> # Using the default iPython matching engine
    >>> prompting.turn_on(merlin)
    >>> @`merlin.name()`
    Myrddin Wyllt

    >>> @merlin What is your first name?
    Invalid .. .  # TODO add actual error

    >>>
    >>> # Using the default Whoosh sting matching engine
    >>> prompting.turn_on(merlin, magic_type = False)
    >>> @merlin What is your first name?
    Myrddin Wyllt

    >>>
    >>> # Using the intellegence engine
    >>> prompting.turn_on(merlin, magic_type = True)
    
    >>> @`merlin.name()`
    Myrddin Wyllt

    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    It's Merlin. People also call me Merlinus and Myrddin. Please, feel free to call me Merlin. It is easier this way in English.

    >>> prompting.turn_off(merlin)      # By default, this backs up the episode and consolidates the memory
"""


from .magics import load_ipython_extension
from .engine import turn_on, turn_off, on
load_ipython_extension(get_ipython())

