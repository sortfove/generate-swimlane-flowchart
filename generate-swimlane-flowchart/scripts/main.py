import argparse
import json
import os
from pathlib import Path

from drawio_renderer import DrawioRenderer
from layout_engine import LayoutEngine

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / 'flow.json'
DEFAULT_OUTPUT_FILE = BASE_DIR / 'output' / 'flow.drawio'

# 环境变量名，方便在不同项目里复用配置
ENV_OUTPUT_DIR = 'FLOW_OUTPUT_DIR'
ENV_OUTPUT_FILE = 'FLOW_OUTPUT_FILE'


def parse_args():
    parser = argparse.ArgumentParser(description='Generate swimlane flowchart drawio files.')
    parser.add_argument(
        '--project-output-dir',
        type=Path,
        default=None,
        help='Project directory to receive flow.drawio. Also read from FLOW_OUTPUT_DIR env var.'
    )
    parser.add_argument(
        '--project-output-file',
        type=Path,
        default=None,
        help='Complete output file path (overrides --project-output-dir and env vars).'
    )
    return parser.parse_args()


def resolve_project_output(args):
    """确定项目输出路径。优先级（从高到低）：
    1. --project-output-file
    2. FLOW_OUTPUT_FILE 环境变量
    3. --project-output-dir
    4. FLOW_OUTPUT_DIR 环境变量
    """
    if args.project_output_file is not None:
        return args.project_output_file.expanduser().resolve()

    env_file = os.environ.get(ENV_OUTPUT_FILE)
    if env_file:
        return Path(env_file).expanduser().resolve()

    if args.project_output_dir is not None:
        return (args.project_output_dir.expanduser().resolve() / 'flow.drawio')

    env_dir = os.environ.get(ENV_OUTPUT_DIR)
    if env_dir:
        return (Path(env_dir).expanduser().resolve() / 'flow.drawio')

    return None


def main():
    args = parse_args()

    with INPUT_FILE.open(encoding='utf-8') as f:
        data = json.load(f)

    layout = LayoutEngine().calculate(data)

    DEFAULT_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    DrawioRenderer().render(data, layout, str(DEFAULT_OUTPUT_FILE))

    project_output = resolve_project_output(args)
    if project_output is not None:
        project_output.parent.mkdir(parents=True, exist_ok=True)
        if project_output.resolve() != DEFAULT_OUTPUT_FILE.resolve():
            project_output.write_bytes(DEFAULT_OUTPUT_FILE.read_bytes())

    print('生成完成')
    print(f'技能输出: {DEFAULT_OUTPUT_FILE}')
    if project_output is not None:
        print(f'项目输出: {project_output}')
    print(layout)


if __name__ == '__main__':
    main()
