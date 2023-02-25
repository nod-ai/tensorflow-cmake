import os
from argparse import ArgumentParser
import subprocess
from typing import Optional
import glob


def install(tf_src: str, install_prefix: str, tf_bin: Optional[str] = None):
    tf_bin = tf_src if tf_bin is None else tf_bin
    libs = []
    libs += glob.glob(os.path.join(tf_bin, "bazel-bin/tensorflow/libtensorflow_cc.so*"))
    libs += glob.glob(
        os.path.join(tf_bin, "bazel-bin/tensorflow/libtensorflow_framework.so*")
    )
    os.makedirs(install_prefix, exist_ok=True)
    subprocess.check_call(
        ["rsync", "-avh"] + libs + [os.path.join(install_prefix, "lib")]
    )
    rsync = ["rsync", "-avh", "--copy-unsafe-links"]
    install_include_dir = os.path.join(install_prefix, "include")
    os.makedirs(install_include_dir, exist_ok=True)
    subprocess.check_call(
        rsync
        + [
            "--prune-empty-dirs",
            '--exclude="_virtual_includes/"',
            os.path.join(tf_bin, "bazel-bin/tensorflow/include/"),
            install_include_dir,
        ]
    )


def parse_args():
    parser = ArgumentParser(description="Build TensorFlow with Bazel.")
    parser.add_argument(
        "--tf_src", type=str, required=True, help="Path to TensorFlow source code."
    )
    parser.add_argument(
        "--tf_bin",
        type=str,
        help="Path to TensorFlow binary directory." " Defaults the source directory.",
    )
    parser.add_argument(
        "--install_prefix",
        type=str,
        help="Installation directory.",
        default="/usr/local",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    install(**vars(args))
