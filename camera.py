

class Camera:

    def __init__(self):
        self.view_scale = 1.0
        self.view_corner = (0, 0)

    def project_coordinate(self, coordinate):
        return (self.view_scale * (coordinate[0] - self.view_corner[0]),
                self.view_scale * (coordinate[1] - self.view_corner[1]))

    def deproject_coordinate(self, coordinate):
        return (int(coordinate[0] / self.view_scale + self.view_corner[0]),
                int(coordinate[1] / self.view_scale + self.view_corner[1]))

    def shift_view(self, delta):
        """
        Shifts the view by a delta measured in screen coordinates.
        """
        self.view_corner = (self.view_corner[0] + delta[0] / self.view_scale,
                            self.view_corner[1] + delta[1] / self.view_scale)

    def set_scale(self, new_scale, zoom_center):
        scale_change_coefficient = 1 / self.view_scale - 1 / new_scale
        self.view_corner = (self.view_corner[0] + zoom_center[0] * scale_change_coefficient,
                            self.view_corner[1] + zoom_center[1] * scale_change_coefficient)
        self.view_scale = new_scale
