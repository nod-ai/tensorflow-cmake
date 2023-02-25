from os import environ
import os
from argparse import ArgumentParser
import sys
import subprocess
from typing import List
import site


def set_default_env_var(name, default):
    environ[name] = environ[name] if name in environ else default


def set_environment():
    set_default_env_var("CC_OPT_FLAGS", "-march=haswell")
    set_default_env_var("TF_NEED_GCP", "0")
    set_default_env_var("TF_NEED_HDFS", "0")
    set_default_env_var("TF_NEED_OPENCL", "0")
    set_default_env_var("TF_NEED_TENSORRT", "0")
    set_default_env_var("TF_NEED_NGRAPH", "0")
    set_default_env_var("TF_NEED_JEMALLOC", "0")
    set_default_env_var("TF_NEED_VERBS", "0")
    set_default_env_var("TF_NEED_MKL", "0")
    set_default_env_var("TF_DOWNLOAD_MKL", "0")
    set_default_env_var("TF_NEED_MPI", "0")
    set_default_env_var("TF_NEED_AWS", "0")
    set_default_env_var("TF_NEED_GDR", "0")
    set_default_env_var("TF_NEED_CUDA", "0")
    set_default_env_var("TF_CUDA_CLANG", "0")
    set_default_env_var("TF_SET_ANDROID_WORKSPACE", "0")
    set_default_env_var("TF_NEED_KAFKA", "0")
    set_default_env_var("TF_DOWNLOAD_CLANG", "0")
    set_default_env_var("TF_NEED_IGNITE", "0")
    set_default_env_var("TF_NEED_ROCM", "0")
    set_default_env_var("NCCL_INSTALL_PATH", "/usr")
    set_default_env_var("PYTHON_BIN_PATH", sys.executable)
    set_default_env_var("PYTHON_LIB_PATH", site.getsitepackages()[0])


def parse_args():
    parser = ArgumentParser(
        description="Configure TensorFlow for unatended build with default values."
    )
    parser.add_argument(
        "--tf_src", type=str, required=True, help="Path to TensorFlow source code."
    )
    args, remaining_args = parser.parse_known_args()
    return args, remaining_args


def configure(tf_src: str, args: List[str]):
    subprocess.check_call([sys.executable, os.path.join(tf_src, "configure.py")] + args)


if __name__ == "__main__":
    args, remaining_args = parse_args()
    set_environment()
    configure(tf_src=args.tf_src, args=remaining_args)
