import numpy as np
import pyrender
import copy
import cv2

def ndarray2tuple(value: np.ndarray):
    return tuple(value.astype(np.int64).tolist())

def display(p2d_list, visimg, color=(0, 0, 255), size=5):
    visimg = copy.deepcopy(visimg)
    for j, joint in enumerate(p2d_list):
        visimg = cv2.circle(visimg, ndarray2tuple(joint), size, color, -1)
    return visimg

def compute_oks(dts, gts, s):
    tmp = []
    k = np.ones(len(gts))
    for k_i, dt, gt in zip(k, dts, gts):
        d = (dt[0]-gt[0])**2 + (dt[1]-gt[1])**2
        e = -d/(2*(s**2)*(k_i**2))
        tmp.append(np.exp(e))
    return sum(tmp) / sum(k)

def projection(p3d_list, intrinsics, extrinsics, width=1920):
    p2ds = []
    for i, p3d in enumerate(p3d_list):
        projection_matrix = np.matmul(intrinsics, extrinsics)
        projection = np.matmul(projection_matrix, p3d).flatten()
        p2d = projection[:2] / projection[-1]
        p2d *= width
        p2ds.append(p2d.astype(np.int32))
    return np.array(p2ds)

class CustomRenderer(object):
    def __init__(self):
        self.scene = pyrender.Scene(ambient_light=(.3, .3, .3))
        viewport_width, viewport_height = 1920, 1080
        # renderer
        self.renderer = pyrender.OffscreenRenderer(
            viewport_width=viewport_width, viewport_height=viewport_height, point_size=1.0)

    def insert_camera(self, cam_param):
        focal, princpt, cam_no = cam_param['focal'], cam_param['princpt'], cam_param['cam_no']
        camera = pyrender.IntrinsicsCamera(fx=focal[0], fy=focal[1], cx=princpt[0], cy=princpt[1])
        self.scene.add(camera, 'cam_{}'.format(cam_no), np.linalg.inv(cam_param['extrinsics']))
        # light
        light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=.8)
        self.scene.add(light, 'light_{}'.format(cam_no), np.linalg.inv(cam_param['extrinsics']))

    def update_mesh(self, mesh):
        material = pyrender.MetallicRoughnessMaterial(metallicFactor=.0, alphaMode='OPAQUE', baseColorFactor=(1., 1., .9, 1.))
        node = self.scene.get_nodes(name='mesh')
        if len(node) > 1:
            self.scene.remove_node(node.pop())
        mesh = pyrender.Mesh.from_trimesh(mesh, material=material, smooth=False)
        self.scene.add(mesh, 'mesh')

    def render_mesh(self, cam_no, bg):
        # render
        cam_name = 'cam_{}'.format(cam_no)
        cam_node = self.scene.get_nodes(name=cam_name)
        if len(cam_node) < 1:
            raise ValueError('There is any camera named like {}'.format(cam_no))
        self.scene.main_camera_node = cam_node.pop()
        rgb, depth = self.renderer.render(self.scene, flags=pyrender.RenderFlags.RGBA)
        rgb = rgb[:,:,:3].astype(np.float32)
        valid_mask = (depth > 0)[:,:,None]

        # save to image
        img = rgb * valid_mask + bg * (1-valid_mask)
        return img, valid_mask