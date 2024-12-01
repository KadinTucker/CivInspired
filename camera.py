import worldgen
import math

class Camera:
    """
    An object that facilitates transformations between screen coordinates and object coordinates,
    for some rectangular object - for example, a world map.
    Works based on a linear scaling projection, where `view_scale` is screen coordinates per object coordinate.
    This particular implementation applies the topology as defined in worldgen's wrap_coordinate function
    """
    def __init__(self, object_dimensions, screen_dimensions):
        self.view_scale = 1.0  # screen coordinates per object coordinate
        self.view_corner = (0, 0)  # measured in object coordinates
        self.object_dimensions = object_dimensions
        self.screen_dimensions = screen_dimensions

    def project_coordinate(self, coordinate):
        """
        Given an object coordinate, get the corresponding screen coordinate.
        Only outputs a single coordinate, although multiple may be possible for a wrapped map.
        """
        x = coordinate[0] - self.view_corner[0]
        y = coordinate[1] - self.view_corner[1]
        x = x % self.object_dimensions[0]
        return (self.view_scale * x, self.view_scale * y)

    def deproject_coordinate(self, coordinate):
        """
        Given a screen coordinate, get the corresponding object coordinate.
        Outputs coordinates that would be beyond the domain, but can be wrapped.
        """
        return (int(coordinate[0] / self.view_scale + math.ceil(self.view_corner[0])),
                int(coordinate[1] / self.view_scale + math.ceil(self.view_corner[1])))

    def shift_view(self, delta):
        """
        Shifts the view by a delta measured in screen coordinates.
        """
        self.view_corner = (self.view_corner[0] + delta[0] / self.view_scale,
                            self.view_corner[1] + delta[1] / self.view_scale)

    def bind_vertical(self):
        """
        Given a lower and upper bound for object coordinates, ensures that the view domain fits into those coordinates.
        """
        self.view_corner = (self.view_corner[0], max(min(self.view_corner[1], self.screen_dimensions[1]
                                                     - int(self.screen_dimensions[1] / self.view_scale)), 0))
        self.view_scale = max(self.view_scale, self.screen_dimensions[1] / self.object_dimensions[1])

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
