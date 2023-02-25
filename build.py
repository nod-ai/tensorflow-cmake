from argparse import ArgumentParser
import subprocess
from typing import List
import shlex


def default_bazel_args() -> List[str]:
    return ["build", "tensorflow:libtensorflow_cc.so", "tensorflow:install_headers"]


def build(
    tf_src: str,
    bazel_command: str,
    bazel_additional_args: str,
    bazel_override_args: str,
):
    bazel_additional_args_list = shlex.split(bazel_additional_args)
    bazel_override_args_list = shlex.split(bazel_override_args)
    if len(bazel_override_args_list) != 0:
        bazel_args = bazel_override_args_list
    else:
        bazel_args = default_bazel_args()
    bazel_args += bazel_additional_args_list
    subprocess.check_call([bazel_command] + bazel_args, cwd=tf_src)


def parse_args():
    parser = ArgumentParser(description="Build TensorFlow with Bazel.")
    parser.add_argument(
        "--tf_src", type=str, required=True, help="Path to TensorFlow source code."
    )
    parser.add_argument("--bazel_command", type=str, default="bazel")
    parser.add_argument(
        "--bazel_additional_args",
        type=str,
        default="",
        help="Additional arguments append to the arguments pass to Bazel.",
    )
    parser.add_argument(
        "--bazel_override_args",
        type=str,
        default="",
        help="Override default Bazel arguments.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(**vars(args))
