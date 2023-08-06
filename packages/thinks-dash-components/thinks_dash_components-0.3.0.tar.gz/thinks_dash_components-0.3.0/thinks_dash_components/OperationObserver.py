# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class OperationObserver(Component):
    """An OperationObserver component.


Keyword arguments:

- id (string; optional)

- clear (boolean; default False)

- interval (number; default 10000)

- limit (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'OperationObserver'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, limit=Component.REQUIRED, interval=Component.UNDEFINED, clear=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'clear', 'interval', 'limit']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'clear', 'interval', 'limit']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['limit']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(OperationObserver, self).__init__(**args)
