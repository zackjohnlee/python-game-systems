def add_position(cls):
    class PositionAdded(cls):
        def __init__(self, *args, **kwargs):
            self._position = (0, 0)  # Default position
            super().__init__(*args, **kwargs)

        @property
        def position(self):
            return self._position

        @position.setter
        def position(self, new_position):
            self._position = new_position

    return PositionAdded