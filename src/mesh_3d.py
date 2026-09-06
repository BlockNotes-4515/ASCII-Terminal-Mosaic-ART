import numpy as np
import time
import os

class Cube3D:
    def __init__(self):
        # 3D Cube Vertices
        self.vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
        ], dtype=float)
        
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

    def render_cube(self, angle_x: float, angle_y: float, width: int = 80, height: int = 40) -> str:
        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(angle_x), -np.sin(angle_x)],
            [0, np.sin(angle_x), np.cos(angle_x)]
        ])
        Ry = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y)],
            [0, 1, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y)]
        ])
        
        rotated = self.vertices @ Rx @ Ry
        
        # Projection parameters
        fov, distance = 60, 3.5
        canvas = [[" " for _ in range(width)] for _ in range(height)]
        
        # Project 3D points to 2D Screen
        screen_points = []
        for v in rotated:
            z = v[2] + distance
            x_proj = int(width / 2 + (v[0] * fov) / z)
            y_proj = int(height / 2 + (v[1] * fov * 0.5) / z)
            screen_points.append((x_proj, y_proj))

        # Rasterize wireframe edges
        for edge in self.edges:
            p1, p2 = screen_points[edge[0]], screen_points[edge[1]]
            self._draw_line(p1, p2, canvas, width, height)

        return "\n".join("".join(row) for row in canvas)

    def _draw_line(self, p1, p2, canvas, w, h):
        x0, y0 = p1
        x1, y1 = p2
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            if 0 <= x0 < w and 0 <= y0 < h:
                canvas[y0][x0] = "\033[36m#\033[0m"
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy