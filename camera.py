

class Camera:
    """
    An object that facilitates transformations between screen coordinates and object coordinates,
    for some rectangular object - for example, a world map.
    Works based on a linear scaling projection, where `view_scale` is screen coordinates per object coordinate.
    """
    def __init__(self):
        self.view_scale = 1.0
        self.view_corner = (0, 0)

    def project_coordinate(self, coordinate):
        """
        Given an object coordinate, get the corresponding screen coordinate.
        """
        return (self.view_scale * (coordinate[0] - self.view_corner[0]),
                self.view_scale * (coordinate[1] - self.view_corner[1]))

    def deproject_coordinate(self, coordinate):
        """
        Given a screen coordinate, get the corresponding object coordinate.
        """
        return (int(coordinate[0] / self.view_scale + self.view_corner[0]),
                int(coordinate[1] / self.view_scale + self.view_corner[1]))

    def shift_view(self, delta):
        """
        Shifts the view by a delta measured in screen coordinates.
        """
        self.view_corner = (self.view_corner[0] + delta[0] / self.view_scale,
                            self.view_corner[1] + delta[1] / self.view_scale)

    def set_scale(self, new_scale, zoom_center):
        """
        Sets the view scale, in a way that preserves the screen position of the `zoom_center` coordinate.
        TODO: allow for all projection functions and make setting scale preserve relative screen position
        for an arbitrary projection function.
        """
        scale_change_coefficient = 1 / self.view_scale - 1 / new_scale
        self.view_corner = (self.view_corner[0] + zoom_center[0] * scale_change_coefficient,
                            self.view_corner[1] + zoom_center[1] * scale_change_coefficient)
        self.view_scale = new_scale
