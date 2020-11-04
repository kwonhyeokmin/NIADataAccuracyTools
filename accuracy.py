import yaml
from glob import glob
from pathlib import Path
import numpy as np
import json
import math
from utils.eval_utils import *
import trimesh
import os

class DataAccuracyChecker(object):
    def __init__(self, yaml_file):
        with open(yaml_file) as f:
            self.standard = yaml.load(f, Loader=yaml.FullLoader)
        self.iou_thrs = 0.5
    def _shape_param_count(self, path):
        return len([x for x in Path(path).rglob('*.json')])
    def _template_count(self, path):
        return len([x for x in Path(path).rglob('*.ply')])
    def _sequence_count(self, path):
        return len([x for x in Path(path).rglob('*.json')])
    def _cam_params_count(self, path):
        return len([x for x in Path(path).rglob('*.json')])
    def _images_count(self, path):
        return len([x for x in Path(path).rglob('*.jpg')])
    def _2d_joint_count(self, path):
        return len([x for x in Path(path).rglob('*.json')])
    def _3d_joint_count(self, path):
        return len([x for x in Path(path).rglob('*.json')])
    def _shape_count(self, path):
        return len([x for x in Path(path).rglob('*.obj')])
    def _pointcloud_count(self, path):
        return len([x for x in Path(path).rglob('*.ply')])
    def _check_shape_param(self, path):
        shape_param_paths = [x for x in Path(path).rglob('*.json')]
        count = 0
        for shape_param_path in shape_param_paths:
            with open(shape_param_path, 'r') as f:
                file = json.load(f)
            if len(file['shape_param']) >= 100:
                count += 1
        return count / len(shape_param_paths)
    def _check_3d_joint(self, path):
        info_key = {
            'supercategory': str,
            'action_category_id': int,
            'actor_id': str,
            '3d_pos': int,
            '3d_rot': int,
        }
        annotations_key = {
            'obj_path': int,
            'frame_no': int,
            '3d_pos': list,
            '3d_rot': list
        }
        joint_paths = [x for x in Path(path).rglob('*.json')]
        count = 0
        for joint_path in joint_paths:
            with open(joint_path, 'r') as f:
                file = json.load(f)
                # check info parts
                info = file['info']
                for k,v in info_key.items():
                    if k not in info:
                        continue
                    elif not isinstance(info[k], v):
                        continue
                # check annotations parts
                annotations = file['annotations']
                annotations['3d_pos'] = np.array(annotations['3d_pos'])
                annotations['3d_rot'] = np.array(annotations['3d_rot'])
                for k,v in annotations_key.items():
                    if k in annotations_key.items():
                        continue
                    elif not isinstance(annotations[k], v):
                        continue
                    # check 3d position info
                    if k == '3d_pos' and annotations['3d_pos'].shape != (24, 4, 1):
                        continue
                    # check 3d rotation info
                    if k == '3d_rot' and annotations['3d_rot'].shape != (24, 3, 1):
                        continue
                count += 1
        return count / len(joint_paths)

    def _check_2d_joint(self, path):
        info_key = {
            'supercategory': str,
            'action_category_id': int,
            'actor_id': str,
            'img_width': int,
            'img_height': int,
            'camera_no': int
        }
        annotations_key = {
            'img_no': int,
            'frame_no': int,
            'img_path': str,
            '2d_pos': np.ndarray
        }
        joint_paths = [x for x in Path(path).rglob('*.json')]
        count = 0
        for joint_path in joint_paths:
            with open(joint_path, 'r') as f:
                file = json.load(f)
                # check info parts
                info = file['info']
                for k,v in info_key.items():
                    if k not in info:
                        continue
                    elif not isinstance(info[k], v):
                        continue
                # check annotations parts
                annotations = file['annotations']
                annotations['2d_pos'] = eval('np.array(' + annotations['2d_pos'] + ')')
                for k,v in annotations_key.items():
                    if k in annotations_key.items():
                        continue
                    elif not isinstance(annotations[k], v):
                        continue
                    # check 2d position info
                    if k == '2d_pos' and annotations['2d_pos'].shape != (24, 2):
                        continue
                count += 1

        return count / len(joint_paths)

    def check_1_1(self):
        """
            최종 산출물 및 규모
        :return: (dict) 각 산출물 별 퍼센트
        """
        standard = self.standard['standard']
        filepath = self.standard['filepath']
        result = {}
        # 1-1.2 액터별 Shape 파라미터
        result['2. 액터별 Shape 파라미터'] = self._shape_param_count(filepath['ShapeParam_json'])/standard['shape_params']
        # 1-1.3 액터별 템플릿
        result['3. 액터별 템플릿'] = self._template_count(filepath['Actor'])/standard['templates']
        # 1-1.4 동작종류 메타정보
        result['4. 동작종류 메타정보'] = self._sequence_count(filepath['Sequence_json'])/standard['sequence']
        # 1-1.5 카메라 파라미터 정보
        result['5. 카메라 파라미터 정보'] = self._cam_params_count(filepath['Camera_json'])/standard['cam_params']
        # 1-1.6 2D 이미지
        result['6. 2D 이미지'] = self._images_count(filepath['Image'])/standard['images']
        # 1-1.7 2D 관절정보
        result['7. 2D 관절정보'] = self._2d_joint_count(filepath['2D_json'])/standard['2d_joint']
        # 1-1.8 3D Shape 정보
        result['8. 3D Shape 정보'] = self._shape_count(filepath['3D_shape'])/standard['shape']
        # 1-1.9 3D 관절정보
        result['9. 3D 관절정보'] = self._3d_joint_count(filepath['3D_json'])/standard['3d_joint']
        # 1-1.10 포인트 클라우드
        result['10. 포인트 클라우드'] = self._pointcloud_count(filepath['PointCloud'])/standard['pointcloud'] if standard['pointcloud']!=0 else 1
        # 1-1.11 액터별 Shape 파라미터 - 액터별 템플릿
        result['11. 액터별 Shape 파라미터 - 액터별 템플릿'] = self._check_shape_param(filepath['ShapeParam_json'])
        # 1-1.12 2D 이미지 - 2D 관절정보
        result['12. 2D 이미지 - 2D 관절정보'] = self._check_2d_joint(filepath['2D_json'])
        # 1-1.13 3D Shape 정보 - 3D 관절정보
        result['13. 3D Shape 정보 – 3D 관절정보'] = self._check_3d_joint(filepath['3D_json'])
        for k,v in result.items():
            result[k] *= 100

        return result

    def check_1_4(self):
        """
        2.4 참값(Ground Truth) 정확도
        1-4 구축된 2D 조인트 좌표 정보에 대해 정확도 측정
        :return OKS:
        """
        result = {}
        cam_info = self.standard['cam_info']
        filepath = self.standard['filepath']
        # load 2d joint info
        joint_2d_paths = [x for x in Path(filepath['2D_json']).rglob('*.json')]
        # load 3d joint info
        joint_3d_paths = [x for x in Path(filepath['3D_json']).rglob('*.json')]
        # load cam info
        cam_param_pathes = [x for x in Path(filepath['Camera_json']).rglob('*.json')]
        oks_list = []
        # load 2d joint data
        count = 0
        for joint_2d_path in joint_2d_paths:
            if not os.path.exists(joint_2d_path):
                continue
            with open(joint_2d_path) as f:
                info_2d = json.load(f)
            image_path = info_2d['annotations']['img_path']
            seq_id, actor_id, vid_id, frame_no = os.path.basename(image_path).split('_')
            frame_no = frame_no.replace('.jpg', '')
            folder_id = '_'.join([seq_id, actor_id])
            file_id = os.path.join(folder_id, '3D_{}.json'.format('_'.join([folder_id, frame_no])))
            joint_3d_path = os.path.join(filepath['3D_json'], file_id)
            if not os.path.exists(joint_3d_path):
                continue
            with open(joint_3d_path) as f:
                info_3d = json.load(f)
            # camera info
            cam_param_pathe = os.path.join(filepath['Camera_json'], '{}.json'.format('_'.join([seq_id, actor_id, vid_id])))
            if not os.path.exists(cam_param_pathe):
                continue
            with open(cam_param_pathe, 'r') as f:
                camera_param = json.load(f)
            # cam_date = next((item for item in cam_info if folder_id in item['id']))['date']

            # obj info
            obj_path = os.path.join(filepath['3D_shape'], folder_id, '{}.obj'.format('_'.join([seq_id, actor_id, vid_id])))
            renderer = CustomRenderer()
            camera_no = camera_param['camera_no']
            extrinsics = np.array(camera_param['extrinsics'])
            intrinsics = np.array(camera_param['intrinsics'])
            princpt = intrinsics[:2, 2] * 1920
            focal = np.diag(intrinsics[:2, :2]) * 1920
            # preprocessing extrinsics
            cam_extrinsics = np.vstack((extrinsics, np.array([0, 0, 0, 1])))
            extrinsics_inv = np.linalg.inv(cam_extrinsics)
            extrinsics_inv[:3,3] *= 0.001
            extrinsics_inv[:,1:3] *= -1
            cam_extrinsics = np.linalg.inv(extrinsics_inv)
            cam_param = {'focal':focal, 'princpt':princpt, 'extrinsics':cam_extrinsics, 'cam_no': camera_no}
            renderer.insert_camera(cam_param=cam_param)
            if not os.path.exists(obj_path):
                continue
            mesh = trimesh.load(obj_path)
            vec = trimesh.transformations.scale_and_translate(0.01, np.ones(3))
            mesh.apply_transform(vec)
            renderer.update_mesh(mesh)
            _, valid_mask = renderer.render_mesh(cam_no=camera_no, bg=np.zeros((1080, 1920,3)))
            del renderer
            s = np.count_nonzero(valid_mask)
            dt_2d_pos = eval('np.array(' + info_2d['annotations']['2d_pos'] + ')')
            gt_3d_pos = np.array(info_3d['annotations']['3d_pos'])
            gt_2d_pos = projection(gt_3d_pos, intrinsics, extrinsics)

            # display
            # vis_img = cv2.imread(os.path.join(filepath['Image'], image_path))
            # if vis_img is None:
            #     vis_img = np.zeros(shape=(1080, 1920, 3))
            # vis_img = display(dt_2d_pos, vis_img, color=[255, 0, 0])
            # vis_img = display(gt_2d_pos, vis_img, color=[0, 0, 255])
            # cv2.imwrite('test.jpg', vis_img)
            # calculate oks
            oks = compute_oks(dt_2d_pos, gt_2d_pos, s)
            oks_list.append(oks)
            count += 1
            if count > 50:
                break
        oks_list = np.array(oks_list).reshape(-1, 1)
        result['OKS (AP: {})'.format(self.iou_thrs)] = float(sum(oks_list > self.iou_thrs)) / count * 100
        # load camera paramter data
        return result

