# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MobileDropdown(Component):
    """A MobileDropdown component.


Keyword arguments:

- id (string; optional)

- className (string; optional)

- clearable (boolean; default True)

- notfoundMsg (string; optional)

- options (list; optional)

- value (string | number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'MobileDropdown'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, options=Component.UNDEFINED, value=Component.UNDEFINED, notfoundMsg=Component.UNDEFINED, clearable=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'clearable', 'notfoundMsg', 'options', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'clearable', 'notfoundMsg', 'options', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MobileDropdown, self).__init__(**args)
