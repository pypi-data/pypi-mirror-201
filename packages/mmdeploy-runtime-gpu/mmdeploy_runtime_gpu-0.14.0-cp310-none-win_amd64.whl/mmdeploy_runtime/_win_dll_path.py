# Copyright (c) OpenMMLab. All rights reserved.
import os
import sys

cuda_bin_dir = ""
if "CUDA_PATH" in os.environ:
    cuda_bin_dir = os.path.join(os.environ["CUDA_PATH"], "bin")
else:
    raise ImportError("Can't find environment variable CUDA_PATH")
if sys.version_info >= (3, 8):
    os.add_dll_directory(cuda_bin_dir)
else:
    os.environ["PATH"] = cuda_bin_dir + os.pathsep + os.environ["PATH"]