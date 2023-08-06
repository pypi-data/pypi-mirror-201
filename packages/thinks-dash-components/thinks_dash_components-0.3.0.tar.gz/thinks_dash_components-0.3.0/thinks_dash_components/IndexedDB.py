# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class IndexedDB(Component):
    """An IndexedDB component.


Keyword arguments:

- id (string; required)

- db_name (string; required)

- exe_delete (dict | list; optional)

- exe_delete_all (dict | list; optional)

- exe_get_key_all (dict | list; optional)

- exe_insert (dict | list; optional)

- exe_select (dict | list; optional)

- exe_select_all (dict | list; optional)

- exe_update (dict | list; optional)

- is_delete (boolean; default False)

- result (dict; optional)

- stores (list of dicts; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'IndexedDB'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, is_delete=Component.UNDEFINED, db_name=Component.REQUIRED, stores=Component.REQUIRED, exe_insert=Component.UNDEFINED, exe_update=Component.UNDEFINED, exe_delete=Component.UNDEFINED, exe_delete_all=Component.UNDEFINED, exe_select=Component.UNDEFINED, exe_select_all=Component.UNDEFINED, exe_get_key_all=Component.UNDEFINED, result=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'db_name', 'exe_delete', 'exe_delete_all', 'exe_get_key_all', 'exe_insert', 'exe_select', 'exe_select_all', 'exe_update', 'is_delete', 'result', 'stores']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'db_name', 'exe_delete', 'exe_delete_all', 'exe_get_key_all', 'exe_insert', 'exe_select', 'exe_select_all', 'exe_update', 'is_delete', 'result', 'stores']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'db_name', 'stores']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(IndexedDB, self).__init__(**args)
