# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Notice(Component):
    """A Notice component.


Keyword arguments:

- id (string; required)

- badge_color (string; default 'red')

- border_color (string; default 'gray')

- color (string; default 'white')

- duration (number; default 300)

- icon_color (string; default 'black')

- max_length (number; default 10)

- notices (list of dicts; optional)

- position (string; default 'right')

- remove_timing (string; default 'check')

- sort (string; default 'desc')

- timeout (string; default '00:30:00')

- value (string | number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'Notice'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, notices=Component.UNDEFINED, remove_timing=Component.UNDEFINED, max_length=Component.UNDEFINED, timeout=Component.UNDEFINED, icon_color=Component.UNDEFINED, color=Component.UNDEFINED, badge_color=Component.UNDEFINED, border_color=Component.UNDEFINED, position=Component.UNDEFINED, value=Component.UNDEFINED, duration=Component.UNDEFINED, sort=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'badge_color', 'border_color', 'color', 'duration', 'icon_color', 'max_length', 'notices', 'position', 'remove_timing', 'sort', 'timeout', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'badge_color', 'border_color', 'color', 'duration', 'icon_color', 'max_length', 'notices', 'position', 'remove_timing', 'sort', 'timeout', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Notice, self).__init__(**args)
