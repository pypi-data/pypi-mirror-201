"""


Uilist Operators
****************

:func:`entry_add`

:func:`entry_move`

:func:`entry_remove`

"""

import typing

def entry_add(list_path: str = '', active_index_path: str = '') -> None:

  """

  Add an entry to the list after the current active item

  :file:`startup/bl_ui/generic_ui_list.py\:208 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L208>`_

  """

  ...

def entry_move(list_path: str = '', active_index_path: str = '', direction: str = 'UP') -> None:

  """

  Move an entry in the list up or down

  :file:`startup/bl_ui/generic_ui_list.py\:234 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L234>`_

  """

  ...

def entry_remove(list_path: str = '', active_index_path: str = '') -> None:

  """

  Remove the selected entry from the list

  :file:`startup/bl_ui/generic_ui_list.py\:191 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L191>`_

  """

  ...
