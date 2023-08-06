# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Alert(Component):
    """An Alert component.


Keyword arguments:

- id (string; optional)

- buttons (list of dicts; required)

- duration (number; default 150)

- is_open (boolean; default False)

- message (a list of or a singular dash component, string or number; required)

- output_target (boolean | number | string | dict | list; optional)

- title (a list of or a singular dash component, string or number; optional)

- value (string | number; optional)"""
    _children_props = ['message', 'title']
    _base_nodes = ['message', 'title', 'children']
    _namespace = 'thinks_dash_components'
    _type = 'Alert'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, message=Component.REQUIRED, title=Component.UNDEFINED, buttons=Component.REQUIRED, value=Component.UNDEFINED, is_open=Component.UNDEFINED, duration=Component.UNDEFINED, output_target=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttons', 'duration', 'is_open', 'message', 'output_target', 'title', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttons', 'duration', 'is_open', 'message', 'output_target', 'title', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['buttons', 'message']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Alert, self).__init__(**args)
