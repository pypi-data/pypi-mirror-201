"""
config
Utility object for ML project configuration
Hans Buehler 2022
"""

from collections import OrderedDict
from collections.abc import Mapping
from sortedcontainers import SortedDict
from .util import uniqueHashExt
from .prettydict import PrettyDict as pdct
from .logger import Logger
_log = Logger(__file__)

class _ID(object):
    pass

no_default = _ID()    # creates a unique object which can be used to detect if a default value was provided

# ==============================================================================
# New in version 0.1.45
# Support for conditional types, e.g. we can write
#
#  x = config(x, 0.1, Float >= 0., "An 'x' which cannot be negative")
# ==============================================================================

class _Cast(object):

    def __call__( self, value, config_name : str, key_name : str ):
        """ cast 'value' to the proper type """
        raise NotImplementedError("Internal error")

    def __str__(self) -> str:
        """ Returns readable string description of 'self' """
        raise NotImplementedError("Internal error")

def _cast_name( cast : type ) -> str:
    """ Returns the class name of 'cast' """
    if cast is None:
        return ""
    return getattr(cast,"__name__", str(cast))

# ================================
# Simple wrapper
# ================================

class _Simple(_Cast):# NOQA

    def __init__(self, cast : type, config_name : str, key_name : str, none_is_any : bool ):
        """ Simple atomic caster """
        if not cast is None:
            _log.verify( not isinstance(cast, str), "Error in definition for key '%s' in config '%s': 'cast' must be a type. Found a string. Most likely this happened because a help string was defined as position argument, but no 'cast' type. In this case, use 'help=' to specify the help text.", key_name, config_name )
            _log.verify( not isinstance(cast, _Cast), "Internal error in definition for key '%s' in config '%s': 'cast' should not be derived from _Cast. Object is %s", key_name, config_name, str(cast) )
            _log.verify( isinstance( cast, type ), "Error in definition for key '%s' in config '%s': 'cast' must be a type. Found %s", key_name, config_name, str(cast) )
        self.cast        = cast
        self.none_is_any = none_is_any
        _log.verify( not none_is_any is None or not cast is None, "Must set 'none_is_any' to bool value if cast is 'None'.")

    def __call__(self, value, config_name : str, key_name : str ):
        """ Cast 'value' to the proper type """
        if self.cast is None:
            if value is None or self.none_is_any:
                return value
            if not value is None:
                raise TypeError("None expected, found %s", type(value).__name__)
        return self.cast(value)

    def __str__(self) -> str:
        """ Returns readable string """
        if self.cast is None:
            return "any" if self.none_is_any else "None"
        return _cast_name(self.cast)

# ================================
# Conditional types such as Int>0
# ================================

class _Condition(_Cast):
    """ Represents a simple operator condition such as 'Float >= 0.' """

    def __init__(self, cast, op, other):
        """ Initialize the condition for a base type 'cast' and an 'op' with an 'other'  """
        self.cast    = cast
        self.op      = op
        self.other   = other
        self.l_and   = None

    def __and__(self, cond):
        """
        Combines to conditions with logical AND .
        Requires the left hand 'self' to be a > or >=; the right hand must be < or <=
        This means you can write

            x = config("x", 0.5, (Float >= 0.) & (Float < 1.), "Variable x")

        """
        if not self.l_and is None:
            raise NotImplementedError("Cannot combine more than two conditions")
        if not self.op[0] == 'g':
            raise NotImplementedError("The left hand condition when using '&' must be > or >=. Found %s" % self._op_str)
        if not cond.op[0] == 'l':
            raise NotImplementedError("The right hand condition when using '&' must be < or <=. Found %s" % cond._op_str)
        if self.cast != cond.cast:
            raise NotImplementedError("Cannot '&' conditions for types %s and %s" % (self.cast.__name__, cond.cast.__name__))
        op_new = _Condition(self.cast, self.op, self.other)
        op_new.l_and = cond
        return op_new

    def __call__(self, value, config_name : str, key_name : str ):
        """ Test whether 'value' satisfies the condition """
        value = self.cast(value)

        if self.op == "ge":
            ok = value >= self.other
        elif self.op == "gt":
            ok = value > self.other
        elif self.op == "le":
            ok = value <= self.other
        elif self.op == "lt":
            ok = value < self.other
        else:
            raise RuntimeError("Internal error: unknown operator %s" % str(self.op))
        _log.verify( ok, "Config '%s': value for key '%s' %s. Found %s", config_name, key_name, self.err_str, value )
        return self.l_and( value, config_name, key_name) if not self.l_and is None else value

    def __str__(self) -> str:
        """ Returns readable string """
        s = _cast_name(self.cast) + self._op_str + str(self.other)
        if not self.l_and is None:
            s += " and " + str(self.l_and)
        return s

    @property
    def _op_str(self) -> str:
        """ Returns a string for the operator of this conditon """
        if self.op == "ge":
            return ">="
        elif self.op == "gt":
            return ">"
        elif self.op == "le":
            return "<="
        elif self.op == "lt":
            return "<"
        raise RuntimeError("Internal error: unknown operator %s" % str(self.op))

    @property
    def err_str(self) -> str:
        """ Nice error string """
        zero = self.cast(0)
        def mk_txt(cond):
            if cond.op == "ge":
                s = ("not be lower than %s" % cond.other) if cond.other != zero else ("not be negative")
            elif cond.op == "gt":
                s = ("be bigger than %s" % cond.other) if cond.other != zero else ("be positive")
            elif cond.op == "le":
                s = ("not exceed %s" % cond.other) if cond.other != zero else ("not be positive")
            elif cond.op == "lt":
                s = ("be lower than %s" % cond.other) if cond.other != zero else ("be negative")
            else:
                raise RuntimeError("Internal error: unknown operator %s" % str(cond.op))
            return s

        s    = "must " + mk_txt(self)
        if not self.l_and is None:
            s += ", and " + mk_txt(self.l_and)
        return s


class _CastCond(_Cast): # NOQA
    """
    Generates compound _Condition's
    See the two members Float and Int
    """

    def __init__(self, cast):# NOQA
        self.cast = cast
    def __ge__(self, other) -> bool:# NOQA
        return _Condition( self.cast, 'ge', self.cast(other) )
    def __gt__(self, other) -> bool:# NOQA
        return _Condition( self.cast, 'gt', self.cast(other) )
    def __le__(self, other) -> bool:# NOQA
        return _Condition( self.cast, 'le', self.cast(other) )
    def __lt__(self, other) -> bool:# NOQA
        return _Condition( self.cast, 'lt', self.cast(other) )
    def __call__(self, value, config_name : str, key_name : str ):
        """ This gets called if the type was used without operators """
        cast = _Simple(self.cast, config_name, key_name,none_is_any=None )
        return cast(value, config_name, key_name)
    def __str__(self) -> str:
        """ This gets called if the type was used without operators """
        return _cast_name(self.cast)

Float = _CastCond(float)
Int   = _CastCond(int)

# ================================
# Enum type for list 'cast's
# ================================

class _Enum(_Cast):
    """
    Utility class to support enumerator types.
    No need to use this classs directly. It will be automatically instantiated if a list is passed as type, e.g.

        code = config("code", "Python", ['C++', 'Python'], "Which language do we love")

    Note that all list members must be of the same type.
    """

    def __init__(self, enum : list, config_name : str, key_name : str ):
        """ Initializes an enumerator casting type. """
        self.enum = list(enum)
        _log.verify( len(self.enum) > 0, "Error in config '%s': 'cast' for key '%s' is an empty list. Lists are used for enumerator types, hence passing empty list is not defined", config_name, key_name )
        _log.verify( not self.enum[0] is None, "Error in config '%s': 'cast' for key '%s' is an list, with first element 'None'. Lists are used for enumerator types, and the first element defines their underlying type. Hence you cannot use 'None'. (Did you want to use alternative notation with tuples?)", config_name, key_name )
        self.cast = _Simple( type(self.enum[0]), config_name, key_name, none_is_any=None )
        for i in range(1,len(self.enum)):
            try:
                self.enum[i] = self.cast( self.enum[i], config_name, key_name )
            except:
                _log.throw( "Error in config '%s', key '%s': members of the list are not of consistent type. Found %s for the first element which does match the type %s of the %ldth element",\
                        config_name, key_name, self.cast, _cast_name(type(self.enum[i])), i )

    def __call__( self, value, config_name, key_name ):
        """
        Cast 'value' to the proper type and check is one of the list members
        Raises a KeyError if the value was not found in our enum
        """
        value = self.cast(value, config_name, key_name)
        _log.verify( value in self.enum, "Config '%s': value for key '%s' %s. Found %s", config_name, key_name, self.err_str, str(value) )
        return value

    @property
    def err_str(self) -> str:
        """ Nice error string """
        s = "must be one of: '" + str(self.enum[0]) + "'"
        for i in range(1,len(self.enum)-1):
            s += ", '" + str(self.enum[i])
        if len(self.enum) > 1:
            s += " or '" + str(self.enum[-1]) + "'"
        return s

    def __str__(self) -> str:
        """ Returns readable string """
        s     = "[ "
        for i in range(len(self.enum)):
            s += ( ", " + self.enum[i] ) if i > 0 else self.enum[i]
        s += " ]"
        return s

# ================================
# Multiple types
# ================================

class _Alt(_Cast):
    """
    Initialize a casting compund "alternative" type, e.g. it the variable may contain several types, each of which is acceptable.
    None here means that 'None' is an accepted value.
    This is invokved when a tuple is passed, e.g

        config("spread", None, ( None, float ), "Float or None")
        config("spread", 1, ( Int<=-1, Int>=1. ), "A variable which has to be outside (-1,+1)")
    """

    def __init__(self, casts : list, config_name : str, key_name : str ):
        """ Initialize a compound cast """
        _log.verify( len(casts) > 0, "Error in config '%s': 'cast' for key '%s' is an empty tuple. Tupeks are used for aleternative types, hence passing empty tuple is not defined", config_name, key_name )
        self.casts = [ _create_caster(cast, config_name, key_name, none_is_any = False) for cast in casts ]

    def __call__( self, value, config_name : str, key_name : str ):
        """ Cast 'value' to the proper type """
        e0   = None
        done = True
        for cast in self.casts:
            # None means that value == None is acceptable
            try:
                return cast(value, config_name, key_name )
            except Exception as e:
                e0 = e if e0 is None else e0
        _log.throw("Error in config '%s': value for key '%s' %s. Found '%s' of type '%s'", config_name, key_name, self.err_str,str(value), type(value).__name__)

    def test(self, value):
        """ Test whether 'value' satisfies the condition """
        raise self.test

    @property
    def err_str(self):
        """ Returns readable string """
        return "must be one of the following types: " + self.__str__()

    def __str__(self):
        """ Returns readable string """
        s = ""
        for cast in self.casts[:-1]:
            s += str(cast) + " or "
        s += str(self.casts[-1])
        return s

# ================================
# Manage casting
# ================================

def _create_caster( cast : type, name : str, key : str, none_is_any : bool ):
    """
    Implements casting.

    Parameters
    ----------
        value: value, either from the user or the default value if provided
        cast : cast input to call() from the user, or None.
        name : name of the config
        key  : name of the key being access
        none_is_any :If True, then None means that any type is accepted. If False, the None means that only None is accepted.

    Returns
    -------
        value : casted value
        __str__ : casting help text. Empty if 'cast' is None
    """

    if isinstance(cast, list):
        return _Enum( cast, name, key )
    elif isinstance(cast, tuple):
        return _Alt( cast, name, key )
    elif isinstance(cast,_Cast):
        return cast
    return _Simple( cast, name, key, none_is_any=none_is_any )

# ==============================================================================
#
# Actual Config class
#
# ==============================================================================

class Config(OrderedDict):
    """
    A simple Config class.
    Main features

    Write
        Set data as usual:

            config = Config()
            config['features']  = [ 'time', 'spot' ]
            config['weights']   = [ 1, 2, 3 ]

        Use member notation

            config.network.samples    = 10000
            config.network.activation = 'relu'

    Read
        def read_config( confg ):

            features = config("features", [], list )          # reads features and returns a list
            weights  = config("weights", [], np.ndarray )     # reads features and returns a nump array

            network  = config.network
            samples  = network('samples', 10000)              # networks samples
            config.done()                                     # returns an error as we haven't read 'network.activitation'

    Detaching child configs
    You can also detach a child config, which allows you to store it for later
    use without triggering done() errors for its parent.

        def read_config( confg ):

            features = config("features", [], list )          # reads features and returns a list
            weights  = config("weights", [], np.ndarray )     # reads features and returns a nump array

            network  = config.network.detach()
            samples  = network('samples', 10000)              # networks samples
            config.done()                                     # no error as 'network' was detached
            network.done()                                    # error as network.activation was not read

    Self-recording "help"
    When reading a value, specify an optional help text:

        def read_config( confg ):

            features = config("features", [], list, help="Defines the features" )
            weights  = config("weights", [], np.ndarray, help="Network weights" )

            network  = config.network
            samples  = network('samples', 10000, int, help="Number of samples")
            activt   = network('activation', "relu", str, help="Activation function")
            config.done()

            config.usage_report()   # prints help

    Attributes
    ----------
        config_name : str
            Qualified name of the config, useful for error messages
        children : dict
            Children of this config
        as_dict : dict
            Converts object into a dict of dict's'
        recorder : dict
            Records usage of the object and its children.

    Methods
    -------
        done()
            Checks that all arguments passed to the config, and its children have been read.
            If not, a warning will be produced. This helps catching typos.
            The function will the call mark_done() on itself and all children
            such that subsequent calls to done() to not produce error messages

        mark_done()
            Marks all elements of this config and all children as 'read' (done).
            Any elements not read explicitly will not be recorded for usage_report

        reset_done()
            Removes all usage information for all members of this config and its children.
            Note: this does not affected recorded previous usage.

        detach()
            Create a copy of the current object; set it as 'done'; and return it.
            The copy keeps the reference to the usage recorder.
            This is used to defer using children of configs to a later stage.
            See examples above

        copy()
            Returns a blank copy of the current config, with a new recorder.
    """

    def __init__(self, *args, config_name : str = None, **kwargs):
        """
        See help(Config) for a description of this class.

        Parameters
        ----------
            *args : list
                List of dictionaries to update() for.
                If the first element is a config, and no other parameters
                are passed, then this object will be copy of that config
            config_name : str, optional
                Name of the configuration for report_usage. Default is 'config'
            **kwargs : dict
                Used to initialize the config, e.g.
                Config(a=1, b=2)
        """
        if len(args) == 1 and isinstance(args[0], Config) and config_name is None and len(kwargs) == 0:
            source               = args[0]
            self._done           = source._done
            self._name           = source._name
            self._children       = source._children
            self._recorder       = source._recorder
            OrderedDict.__init__(self, source)
            return

        OrderedDict.__init__(self)
        self._done           = set()
        self._name           = config_name if not config_name is None else "config"
        self._children       = OrderedDict()
        self._recorder       = SortedDict()
        self._recorder._name = self._name
        for k in args:
            self.update(k)
        self.update(kwargs)

    @property
    def config_name(self) -> str:
        """ Returns the fully qualified name of this config """
        return self._name

    @property
    def children(self) -> OrderedDict:
        """ Returns dictionary of children """
        return self._children

    def __str__(self) -> str:
        """ Print myself as dictionary """
        return str(self.as_dict)

    def __repr__(self) -> str:
        """ Print myself as reconstructable object """
        return "Config( **" + self.__str__() + " )"

    @property
    def as_dict(self) -> dict:
        """
        Convert into dictionary of dictionaries
        This operation will turn all members to 'read'
        """
        d = dict(self)
        for n in self._children:
            c = self._children[n].as_dict
            _log.verify( not n in d, "Cannot convert config to dictionary: found both a regular value, and a child with name '%s'", n)
            d[n] = c
        return d

    @property
    def is_empty(self) -> bool:
        """ Checks whether any variables have been set """
        return len(self) + len(self._children) == 0

    def done(self, include_children : bool = True, mark_done : bool = True ):
        """
        Closes the config and checks that no unread parameters remain.
        By default this function also validates that all child configs were done".

        If you want to make a copy of a child config for later processing use detach() first
            config = Config()
            config.a = 1
            config.child.b = 2

            _ = config.a # read a
            config.done()   # error because confg.child.b has not been read yet

        Instead use:
            config = Config()
            config.a = 1
            config.child.b = 2

            _ = config.a # read a
            child = config.child.detach()
            config.done()   # no error, even though confg.child.b has not been read yet
        """
        inputs = set(self)
        rest   = inputs - self._done
        if len(rest) > 0:
            _log.verify( False, "Error closing '%s': the following config arguments were not read: %s\n\n"\
                                "Summary of all variables read from this object:\n%s", \
                                        self._name, list(rest), \
                                        self.usage_report(filter_path=self._name ) )
        if include_children:
            for config in self._children:
                self._children[config].done(include_children=include_children,mark_done=False)
        if mark_done:
            self.mark_done(include_children=include_children)
        return

    def reset_done(self):
        """ Undo done """
        self._done = set()

    def mark_done(self, include_children : bool = True ):
        """ Mark all members as being read. Once called calling done() will no longer trigger an error """
        self._done = set( self )
        if include_children:
            for c in self._childen:
                c.mark_done(include_children=include_children)

    def __getattr__(self, key : str):
        """
        Returns either the value for 'key', if it exists, or creates on-the-fly a child config
        with the name 'key' and retruns it
        """
        _log.verify( key.find('.') == -1 , "Error in config '%s': key name cannot contain '.'. Found %s", self._name, key )
        if key in self._children:
            return self._children[key]
        _log.verify( key.find(" ") == -1, "Error in config '%s': sub-config names cannot contain spaces. Found %s", self._name, key )
        config = Config()
        config._name              = self._name + "." + key
        config._recorder          = self._recorder
        self._children[key]       = config
        return config

    def detach(self,  mark_self_done : bool = True, new_recorder = False ):
        """
        Creates a copy of the current config, and marks the current config as "done" unless 'mark_self_done' is used.
        The use case for this function is storing sub config's for deferred processing.

        Example:

            Creates

                config = Config()
                config['x']        = 1
                config.child['y']  =2

            Using detach

                def g_done_y( config ):
                    y = config("y")
                    config.done()

                def f_done_x( config ):
                    x = config("x")
                    child = config.child.detach()
                    config.done()   # <-- checks that all members of 'config'
                                    # except 'child' are done
                    g_done_y( child )

                f_done_x( config )

        Consistency
        -----------
        By default, the copy will have the same shared recorder as 'self' which means that usage detection
        is shared between the copied and the original config.
        This is to catch mistakes of the following type:

            config = Config()
            config.sub.a = 1

            _ = config.sub("a", 2)   # read 'a' with default value 2

            def f(sub_config):
                _ = sub_config("a",3) # read 'a' with default value 3
            f(config.sub)

        The below will fail with an error message as 'a' is read twice, but with different default values.

        Use new_recorder = True to create a new, clean recorder.
        This is the default when copy() is used.

        Parameters
        ----------
            mark_self_done : bool, optional
                If True mark 'self' as 'read'.
                This allows storing (a copy of) 'self' for deferred processing without triggering a warning when done() is called on a parent object.
            new_recorder : optional
                False: use recorder of 'self'. That means any usage inconsistencies are detected between the new and old config.
                True: create new recorder
                <recorder> if a recorder is specified, use it.
        """
        config = Config()
        config.update(self)
        config._done             = set( self._done )
        config._name             = self._name
        if isinstance( new_recorder, SortedDict ):
            config._recorder     = new_recorder
        elif new_recorder:
            new_recorder         = config._recorder
        else:
            config._recorder     = self._recorder

        config._children         = { _: self._children[_].detach(mark_self_done=mark_self_done, new_recorder=new_recorder) for _ in self._children }
        config._children         = OrderedDict( config._children )

        if mark_self_done:
            self.mark_done()
        return config

    def copy( self ):
        """
        Return a copy of 'self'.
        Do not flag the original config as 'done' but create a new recorder.
        That means that the copied config can be used independently of the 'self'.

        As an example, this allows using different default values for
        config members of the same name:

            base = Config()
            base.a = 1
            copy = base.copy()

            _ = base("x", 1)
            _ = copy("x", 2)

        This call is equivalent to detach(mark_self_done=False, new_recorder=True)
        """
        return self.detach( mark_self_done=False, new_recorder=True )

    def update( self, other=None, **kwargs ):
        """
        Overwrite values of 'self' new values.
        Accepts the two main formats

            update( dictionary )
            update( config )
            update( a=1, b=2 )

        Parameters
        ----------
            other : dict, Config, optional
                Copy all content of 'other' into 'self'.
                If 'other' is a config: elements of other will /not/ be marked as used, or recorded.
                Use mark_used() if this is desired
            **kwargs
                Allows assigning specific values.
        """
        if not other is None:
            if isinstance( other, Config ):
                # copy() children
                # and reset recorder to ours.
                def set_recorder(config, recorder):
                    config._recorder = recorder
                    for c in config._children:
                        set_recorder( config._children[c], recorder )
                for sub in other._children:
                    child = other._children[sub]
                    child = child.copy()
                    set_recorder(child, self._recorder)
                    self._children[sub]= child
                # copy elements from other.
                # we do not mark elements from another config as 'used'
                for key in other:
                    self[key] = OrderedDict.get(other,key)
            else:
                _log.verify( isinstance(other, Mapping), "Cannot update config with an object of type '%s'. Expected 'Mapping' type.", type(other).__name__ )
                for key in other:
                    self[key] = other[key]

        OrderedDict.update( self, kwargs )

    # Read
    # -----

    def __call__(self, key          : str,
                       default      = no_default,
                       cast         : type = None,
                       help         : str = None,
                       help_default : str = None,
                       help_cast    : str = None,
                       mark_done    : bool = True,
                       record       : bool = True ):
        """
        Reads 'key' from the config. If not found, return 'default' if specified.

            config("key")                      - returns the value for 'key' or if not found raises an exception
            config("key", 1)                   - returns the value for 'key' or if not found returns 1
            config("key", 1, int)              - if 'key' is not found, return 1. If it is found cast the result with int().
            config("key", 1, int, "A number"   - also stores an optional help text.
                                                 Call usage_report() after the config has been read to a get a full
                                                 summary of all data requested from this config.

        Parameters
        ----------
            key : string
                Keyword to read
            default : optional
                Default value. Set to 'no_default' to avoid defaulting. In this case the argument is mandatory.
            cast : object, optional
                If None, any value will be acceptable.
                If not None, the function will attempt to cast the value provided with the provided value.
                E.g. if cast = int, then it will run int(x)
                This function now also allows passing the following complex arguemts:
                    * A list, in which case it is assumed that the 'key' must be from this list. The type of the first element of the list will be used to cast values
                    * Int or Float which allow defining constrained integers and floating numbers.
                    * A tuple of types, in which case any of the types is acceptable. A None here means that the value 'None' is acceptable (it does not mean that any value is acceptable)
            help : str, optional
                If provied adds a help text when self documentation is used.
            help_default : str, optional
                If provided, specifies the default value in plain text. In this case the actual
                default value is ignored. Use this for complex default values which are hard to read.
            help_cast : str, optional
                If provided, specifies a description of the cast type.
                Use this for complex cast types which are hard to read.
            mark_done : bool, optional
                If true, marks the respective element as read.
            record : bool, optional
                If True, records usage of the key and validates that previous usage of the key is consistent with
                the current usage, e.g. that the default values are consistent and that if help was provided it is the same.

        Returns
        -------
            Value.
        """
        _log.verify( isinstance(key, str), "'key' must be a string. Found type %s. Details: %s", type(key), key)
        _log.verify( key.find('.') == -1 , "Error in config '%s': key name cannot contain '.'. Found %s", self._name, key )

        # determine raw value
        if not key in self:
            if default == no_default:
                raise KeyError(key, "Error in config '%s': key '%s' not found " % (self._name, key))
            value = default
        else:
            value = OrderedDict.get(self,key)

        # casting
        caster = _create_caster( cast, self._name, key, none_is_any = True )
        value  = caster( value, self._name, key )

        # mark key as read, and record call
        if mark_done:
            self._done.add(key)

        # avoid recording
        if not record:
            return value

        # record?
        record_key    = self._name + "['" + key + "']"    # using a fully qualified keys allows 'recorders' to be shared accross copy()'d configs.
        help          = str(help) if not help is None and len(help) > 0 else ""
        help          = help[:-1] if help[-1:] == "." else help
        help_default  = str(help_default) if not help_default is None else ""
        help_default  = str(default) if default != no_default and len(help_default) == 0 else help_default
        help_cast     = help_cast if not help_cast is None else str(caster)
        _log.verify( default != no_default or help_default == "", "Config %s setup error for key %s: cannot specify 'help_default' if no default is given", self._name, key )

        raw_use       = help == "" and help_cast == "" and help_default == "" # raw_use, e.g. simply get() or []. Including internal use
        record        = SortedDict( value=value,
                                    raw_use=raw_use,
                                    help=help,
                                    help_default=help_default,
                                    help_cast=help_cast )
        if default != no_default:
            record['default'] = default

        exst_value    = self._recorder.get(record_key, None)

        if exst_value is None:
            # no previous use --> use this one.
            self._recorder[record_key] = record
        else:
            if not raw_use:
                if exst_value['raw_use']:
                    # previous usesage was 'raw'. Record this as qualified use.
                    self._recorder[record_key] = record
                else:
                    # Both current and past were bona fide uses. Ensure that their usage is consistent.
                    if default != no_default and 'default' in exst_value:
                        _log.verify( exst_value['default'] == default,  "Config %s was read twice for key %s (%s) with different default values '%s' and '%s'", self._name, key, record_key, exst_value['default'], default )

                    _log.verify( exst_value['help_default'] == help_default, "Config %s was read twice for key %s (%s) with different 'help_default' values '%s' and '%s'", self._name, key, record_key, exst_value['help_default'], help_default )
                    _log.verify( exst_value['help'] == help, "Config %s was read twice for key %s (%s) with different 'help' values '%s' and '%s'", self._name, key, record_key, exst_value['help'], help )
                    _log.verify( exst_value['help_cast'] == help_cast, "Config %s was read twice for key %s (%s) with different 'help_cast' values '%s' and '%s'", self._name, key, record_key, exst_value['help_cast'], help_cast )
        # done
        return value

    def __getitem__(self, key : str):
        """ Returns self(key) """
        return self(key)
    def get(self, key : str, default = None ):
        """
        Returns self(key, default)
        Note that if a default is provided, then this function will fail if a previous call has provided help texts, or a different default.
        If no default is provided, then this function operates silently and will not trigger an error if previous use provided additional, inconsistent information.
        """
        return self(key, default)
    def get_default(self, key : str, default):
        """
        Returns self(key,default)
        Note that if a default is provided, then this function will fail if a previous call has provided help texts, or a different default.
        If no default is provided, then this function operates silently and will not trigger an error if previous use provided additional, inconsistent information.
        """
        return self(key,default)
    def get_raw(self, key : str, default = None ):
        """
        Returns self(key, default, mark_done=False, record=False )
        Reads the respectitve element without marking the element as read; and without recording access to the element.
        """
        return self(key, default, mark_done=False, record=False)
    def get_recorded(self, key : str ):
        """
        Returns the recorded used value of key, e.g. the value returned when the config was used:
            If key is part of the input data, return that value
            If key is not part of the input data, and a default was provided when the config was read, return the default.
        This function:
            Throws a KeyError if the key was never read successfully from the config (e.g. it is not used in the calling stack)
        """
        _log.verify( key.find('.') == -1 , "Error in config '%s': key name cannot contain '.'. Found %s", self._name, key )
        record_key    = self._name + "['" + key + "']"    # using a fully qualified keys allows 'recorders' to be shared accross copy()'d configs.
        record        = self._recorder.get(record_key, None)
        if record is None:
            raise KeyError(key)
        return record['value']

    # Write
    # -----

    def __setattr__(self, key, value):
        """
        Assign value like self[key] = value
        If 'value' is a config, then the config will be assigned as child.
        Its recorder and name will be overwritten.
        """
        if key[0] == "_" or key in self.__dict__:
            OrderedDict.__setattr__(self, key, value )
        elif isinstance( value, Config ):
            value._name              = self._name + "." + key
            value._recorder          = self._recorder
            self._children[key]      = value
        else:
            self[key] = value

    # Recorder
    # --------

    @property
    def recorder(self) -> SortedDict:
        """ Returns the top level recorder """
        return self._recorder

    def usage_report(self,    with_values  : bool = True,
                              with_help    : bool = True,
                              with_defaults: bool = True,
                              with_cast    : bool = False,
                              filter_path  : str  = None ) -> str:
        """
        Generate a human readable report of all variables read from this config.

        Parameters
        ----------
            with_values : bool, optional
                Whether to also print values. This can be hard to read
                if values are complex objects

            with_help: bool, optional
                Whether to print help

            with_defaults: bool, optional
                Whether to print default values

            with_cast: bool, optional
                Whether to print types

            filter_path : str, optional
                If provided, will match all children names vs this string.
                Most useful with filter_path = self._name

        Returns
        -------
            str
                Report.
        """
        with_values   = bool(with_values)
        with_help     = bool(with_help)
        with_defaults = bool(with_defaults)
        with_cast     = bool(with_cast)
        l             = len(filter_path) if not filter_path is None else 0
        rep_here      = ""
        reported      = ""

        for key in self._recorder:
            record       =  self._recorder[key]
            value        =  record['value']
            help         =  record['help']
            help_default =  record['help_default']
            help_cast    =  record['help_cast']
            report       =  key + " = " + str(value) if with_values else key

            do_help      =  with_help and help != ""
            do_cast      =  with_cast and help_cast != ""
            do_defaults  =  with_defaults and help_default != ""

            if do_help or do_cast or do_defaults:
                report += " # "
                if do_cast:
                    report += "(" + help_cast + ") "
                if do_help:
                    report += help
                    if do_defaults:
                        report += "; default: " + help_default
                elif do_defaults:
                    report += " Default: " + help_default

            if l > 0 and key[:l] == filter_path:
                rep_here += report + "\n"
            else:
                reported += report + "\n"

        if len(reported) == 0:
            return rep_here
        if len(rep_here) == 0:
            return reported
        return rep_here + "# \n" + reported

    def usage_reproducer(self) -> str:
        """
        Returns a string expression which will reproduce the current
        configuration tree as long as each 'value' handles
        repr() correctly.
        """
        report = ""
        for key in self._recorder:
            record       =  self._recorder[key]
            value        =  record['value']
            report       += key + " = " + repr(value) + "\n"
        return report

    def input_report(self) -> str:
        """
        Returns a report of all inputs in a readable format, as long as all values
        are as such.
        """
        inputs = []
        def ireport(self, inputs):
            for key in self:
                value      = self.get_raw(key)
                report_key = self._name + "['" + key + "'] = %s" % str(value)
                inputs.append( report_key )
            for c in self._children:
                ireport(self._children[c], inputs)
        ireport(self, inputs)

        inputs = sorted(inputs)
        report = ""
        for i in inputs:
            report += i + "\n"
        return report

    def input_dict(self, ignore_underscore = True ) -> dict:
        """ Returns a (pretty) dictionary of all inputs into this config. """
        inputs = pdct()
        for key in self:
            if ignore_underscore and key[:1] == "_":
                continue
            inputs[key] = self.get_raw(key)
        for c in self._children:
            if ignore_underscore and c[:1] == "_":
                continue
            inputs[c] = self._children[c].input_dict()
        return inputs

    def unique_id(self, length : int = None, parse_functions : bool = False, parse_underscore : str = "none" ) -> str:
        """
        Returns an MDH5 hash key for this object, based on its provided inputs /not/ based on its usage
        ** WARNING **
        By default function ignores
         1) Config keys or children with leading '_'s unless 'parse_underscore' is set to 'protected' or 'private'.
         2) Functions and properties unless parse_functions is True
            In the latter case function code will be used to distinguish
            functions assigned to the config.
        See util.unqiueHashExt() for further information.

        Parameters
        -----------
            length : int
                Desired length of the ID to be returned. Default is default hash size.
            parse_functions : bool
                If True, then function code will be parsed to hash functions. False means functions are not hashed
            parse_underscore : str
                If 'none' then any keys or sub-configs with leading '_' will be ignored.
                If 'protected' then any keys or sub-configs with leading '__' will be ignored.
                If 'private' then no keys or sub-configs will be ignored based on leading '_'s

        Returbs
        -------
            String ID
        """
        inputs = {}
        for key in self:
            if key[:1] == "_":
                continue
            inputs[key] = self.get_raw(key)
        for c in self._children:
            if c[:1] == "_":
                continue
            # collect ID for the child
            child_data = self._children[c].unique_id()
            # we only register children if they have keys.
            # this way we do not trigger a change in ID simply due to a failed read access.
            if child_data != "":
                inputs[c]  = child_data
        return uniqueHashExt(length=length,parse_functions=parse_functions)(inputs) if len(inputs) > 0 else ""

    # magic
    # -----

    def __iter__(self):
        """
        Iterate. For some odd reason, adding this override will make
        using f(**self) call our __getitem__() function.
        """
        return OrderedDict.__iter__(self)

    # pickling
    # --------

    def __reduce__(self):
        """
        Pickling this object explicitly
        See https://docs.python.org/3/library/pickle.html#object.__reduce__
        """
        keys = [ k for k in self ]
        data = [ self.get_raw(k) for k in keys ]
        state = dict(done = self._done,
                     name = self._name,
                     children = self._children,
                     recorder = self._recorder,
                     keys = keys,
                     data = data )
        return (Config, (), state)

    def __setstate__(self, state):
        """ Supports unpickling """
        self._name = state['name']
        self._done = state['done']
        self._children = state['children']
        self._recorder = state['recorder']
        data = state['data']
        keys = state['keys']
        for (k,d) in zip(keys,data):
            self[k] = d

empty = Config()       # empty config as default value for function arguments
Config.empty = empty

def to_config( kwargs, config_name = "kwargs"):
    """
    Makes sure an object is a config, and otherwise tries to convert it into one
    Classic use case is to transform 'kwargs' to a Config
    """
    return kwargs if isinstance(kwargs,Config) else Config( kwargs,config_name=config_name )


def __test_pickle():
    import pickle

    config = Config()
    # world
    config.world.samples = 10000
    config.world.steps = 20
    config.world.black_scholes = True
    config.world.rvol = 0.2    # 20% volatility
    config.world.drift = 0.    # real life drift
    config.world.cost_s = 0.
    # gym
    config.gym.objective.utility = "cvar"
    config.gym.objective.lmbda = 1.
    config.gym.agent.network.depth = 5   # <====== changed this
    config.gym.agent.network.width = 40
    config.gym.agent.network.activation = "softplus"
    # trainer
    config.trainer.train.optimizer = "adam"
    config.trainer.train.batch_size = None
    config.trainer.train.epochs = 400
    config.trainer.caching.epoch_freq = 10
    config.trainer.caching.mode = "on"
    config.trainer.visual.epoch_refresh = 1
    config.trainer.visual.time_refresh = 10
    config.trainer.visual.confidence_pcnt_lo = 0.25
    config.trainer.visual.confidence_pcnt_hi = 0.75

    id2 = config.unique_id()

    # pickle test

    binary   = pickle.dumps(config)
    restored = pickle.loads(binary)
    idrest   = restored.unique_id()
    assert idrest == id2, (idrest, id2)



