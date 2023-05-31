import numpy as np
import pyxel

def rotation_matrix(angles):
    roll, pitch, yaw = angles

    roll = np.deg2rad(roll)
    pitch = np.deg2rad(pitch)
    yaw = np.deg2rad(yaw)

    Rx = np.array([
        [1,            0,             0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])

    Ry = np.array([
        [ np.cos(pitch), 0, np.sin(pitch)],
        [             0, 1,             0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw),  0],
        [np.sin(yaw),  np.cos(yaw),  0],
        [          0,            0,  1]
    ])

    R = Rx @ Ry @ Rz

    return R

class App:
    def __init__(self):

        self.fov = 90

        self.screen_width = 64
        self.screen_height = 64

        self.player_mov_speed = 0.1
        self.player_angle_speed = 4

        self.player_angle = np.array([0, 0, 0], 'float64')

        self.player_pos = np.array([0, 0, 0], 'float64')

        pyxel.init(self.screen_width, self.screen_height, title="3D game", capture_scale=4)
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        player_ang_rad = np.deg2rad(self.player_angle)

        if pyxel.btn(pyxel.KEY_W):
            self.player_pos += np.array([
                np.cos(player_ang_rad[2]),
                np.sin(player_ang_rad[2]),
                np.sin(player_ang_rad[1]),
            ]) * self.player_mov_speed

        if pyxel.btn(pyxel.KEY_S):
            self.player_pos -= np.array([
                np.cos(player_ang_rad[2]),
                np.sin(player_ang_rad[2]),
                np.sin(player_ang_rad[1]),
            ]) * self.player_mov_speed

        if pyxel.btn(pyxel.KEY_A):
            self.player_pos += np.array([
                np.cos(player_ang_rad[2] - np.pi/2),
                np.sin(player_ang_rad[2] - np.pi/2),
                0,
            ]) * self.player_mov_speed

        if pyxel.btn(pyxel.KEY_D):
            self.player_pos -= np.array([
                np.cos(player_ang_rad[2] - np.pi/2),
                np.sin(player_ang_rad[2] - np.pi/2),
                0,
            ]) * self.player_mov_speed

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_angle -= np.array([0, 0, self.player_angle_speed])

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_angle += np.array([0, 0, self.player_angle_speed])

        if pyxel.btn(pyxel.KEY_UP):
            self.player_angle += np.array([0, self.player_angle_speed, 0])

        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_angle -= np.array([0, self.player_angle_speed, 0])

        self.player_angle[1] = np.clip(self.player_angle[1], -90, 90)

        # print(self.player_pos, self.player_angle)


    def draw(self):
        pyxel.cls(0)

        yaw_rad = np.deg2rad(self.player_angle[2])

        global_angle = (
            self.player_angle[1] * -np.sin(yaw_rad),
            self.player_angle[1] * np.cos(yaw_rad),
            self.player_angle[2],
        )

        print(global_angle, yaw_rad)

        rotmat = rotation_matrix(global_angle)

        points = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1],
            [0+4, 0, 0],
            [1+4, 0, 0],
            [1+4, 1, 0],
            [0+4, 1, 0],
            [0+4, 0, 1],
            [1+4, 0, 1],
            [1+4, 1, 1],
            [0+4, 1, 1],
            [0, 1+4, 1],
            [0, 0+4, 0],
            [1, 0+4, 0],
            [1, 1+4, 0],
            [0, 1+4, 0],
            [0, 0+4, 1],
            [1, 0+4, 1],
            [1, 1+4, 1],
            [0+4, 1+4, 1],
            [0+4, 0+4, 0],
            [1+4, 0+4, 0],
            [1+4, 1+4, 0],
            [0+4, 1+4, 0],
            [0+4, 0+4, 1],
            [1+4, 0+4, 1],
            [1+4, 1+4, 1],
        ])

        for point in points:
            rel = (point - self.player_pos) @ rotmat

            yaw = np.arctan2(rel[1], rel[0]) / np.pi * 180
            pitch = np.arctan2(rel[2], np.sqrt(rel[1]**2 + rel[0]**2)) / np.pi * 180

            max_yaw = self.fov/2
            max_pitch = max_yaw * self.screen_width/self.screen_height

            screen_x = yaw/self.fov * self.screen_width + self.screen_width/2
            screen_y = pitch/self.fov * self.screen_height + self.screen_height/2

            if np.abs(yaw) < max_yaw and np.abs(pitch) < max_pitch:
                pyxel.pset(screen_x, screen_y, 10)

App()

