# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectableBox(Component):
    """A SelectableBox component.


Keyword arguments:

- id (string; optional)

- className (string; default '')

- optionChildren (list of a list of or a singular dash component, string or numbers; required)

- optionValues (list of string | numbers; required)

- value (string | number; optional)"""
    _children_props = ['optionChildren']
    _base_nodes = ['optionChildren', 'children']
    _namespace = 'thinks_dash_components'
    _type = 'SelectableBox'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, optionChildren=Component.REQUIRED, optionValues=Component.REQUIRED, value=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'optionChildren', 'optionValues', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'optionChildren', 'optionValues', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['optionChildren', 'optionValues']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SelectableBox, self).__init__(**args)
