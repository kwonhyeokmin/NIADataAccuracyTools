import os
import argparse
from accuracy import DataAccuracyChecker

# run with headless mode
os.environ["PYOPENGL_PLATFORM"] = "egl"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_path', help='yaml path for standard')
    parser.add_argument('--output_path', help='result path for accuracy result', default='.')
    args = parser.parse_args()

    yaml_path = args.yaml_path
    output_path = args.output_path

    checker = DataAccuracyChecker(yaml_file=yaml_path)
    with open(os.path.join(output_path, 'result.txt'), 'w+') as f:
        f.write('[최종 산출물 분류 및 규모 ]\n')
        for k, v in checker.check_1_1().items():
            f.write('{}:\t{:,}%\n'.format(k, round(v, 2)))
        f.write('\n')
        f.write('[2D 조인트 좌표 정보 참값 정확도 ]\n')
        for k, v in checker.check_1_4().items():
            f.write('{}:\t{:,}%\n'.format(k, round(v, 2)))