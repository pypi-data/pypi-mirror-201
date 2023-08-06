"""


Rigidbody Operators
*******************

:func:`bake_to_keyframes`

:func:`connect`

:func:`constraint_add`

:func:`constraint_remove`

:func:`mass_calculate`

:func:`object_add`

:func:`object_remove`

:func:`object_settings_copy`

:func:`objects_add`

:func:`objects_remove`

:func:`shape_change`

:func:`world_add`

:func:`world_remove`

"""

import typing

def bake_to_keyframes(frame_start: int = 1, frame_end: int = 250, step: int = 1) -> None:

  """

  Bake rigid body transformations of selected objects to keyframes

  :file:`startup/bl_operators/rigidbody.py\:106 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/rigidbody.py#L106>`_

  """

  ...

def connect(con_type: str = 'FIXED', pivot_type: str = 'CENTER', connection_pattern: str = 'SELECTED_TO_ACTIVE') -> None:

  """

  Create rigid body constraints between selected rigid bodies

  :file:`startup/bl_operators/rigidbody.py\:268 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/rigidbody.py#L268>`_

  """

  ...

def constraint_add(type: str = 'FIXED') -> None:

  """

  Add Rigid Body Constraint to active object

  """

  ...

def constraint_remove() -> None:

  """

  Remove Rigid Body Constraint from Object

  """

  ...

def mass_calculate(material: str = 'DEFAULT', density: float = 1.0) -> None:

  """

  Automatically calculate mass values for Rigid Body Objects based on volume

  """

  ...

def object_add(type: str = 'ACTIVE') -> None:

  """

  Add active object as Rigid Body

  """

  ...

def object_remove() -> None:

  """

  Remove Rigid Body settings from Object

  """

  ...

def object_settings_copy() -> None:

  """

  Copy Rigid Body settings from active object to selected

  :file:`startup/bl_operators/rigidbody.py\:43 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/rigidbody.py#L43>`_

  """

  ...

def objects_add(type: str = 'ACTIVE') -> None:

  """

  Add selected objects as Rigid Bodies

  """

  ...

def objects_remove() -> None:

  """

  Remove selected objects from Rigid Body simulation

  """

  ...

def shape_change(type: str = 'MESH') -> None:

  """

  Change collision shapes for selected Rigid Body Objects

  """

  ...

def world_add() -> None:

  """

  Add Rigid Body simulation world to the current scene

  """

  ...

def world_remove() -> None:

  """

  Remove Rigid Body simulation world from the current scene

  """

  ...
