# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LoadingWrapper(Component):
    """A LoadingWrapper component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- className (string; optional)

- delay (number; default 500)

- ignores (list of strings; optional)

- interval (number; default 1000)

- is_loading (boolean; optional)

- is_stop (boolean; default False)

- targetClassName (string; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'LoadingWrapper'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, targetClassName=Component.REQUIRED, delay=Component.UNDEFINED, interval=Component.UNDEFINED, ignores=Component.UNDEFINED, is_loading=Component.UNDEFINED, is_stop=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'delay', 'ignores', 'interval', 'is_loading', 'is_stop', 'targetClassName']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'delay', 'ignores', 'interval', 'is_loading', 'is_stop', 'targetClassName']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['targetClassName']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(LoadingWrapper, self).__init__(children=children, **args)
