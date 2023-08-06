# MIT License
#
# Copyright (c) 2023 Dechin CHEN
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import mindspore as ms
from mindspore import Tensor, nn, ops
from mindspore import numpy as msnp
from mindspore.ops.functional import vmap


def _quaternion_multiply(tensor_1, tensor_2):
    """ Get the quaternion multiplication of the given tensor.
    Args:
        tensor_1(Tensor): A tensor with shape (B, 4).
        tensor_2(Tensor): A tensor with shape (B, 4).
    Returns:
        q(Tensor): A tensor with shape (B, 4).
    """
    if tensor_1.shape[-1] != 4 or tensor_2.shape[-1] != 4:
        raise ValueError('The input tensor shape for quaternion_multiply should be like (B, 4) or (4, ).')

    s_1 = tensor_1[:, 0]
    s_2 = tensor_2[:, 0]
    v_1 = tensor_1[:, 1:]
    v_2 = tensor_2[:, 1:]
    s = s_1 * s_2
    d = ops.batch_dot(v_1, v_2, axes=-1)
    s -= d
    v = msnp.zeros_like(v_1)
    v += s_1 * v_2
    v += v_1 * s_2
    v += msnp.cross(v_1, v_2, axisc=-1)
    q = msnp.hstack((s, v))

    return q

def _constant_multiply(tensor_1, constant):
    """ Get the quaternion multiplication of the given tensor and constant.
    Args:
        tensor_1(Tensor): A tensor with shape (B, 4).
        constant(Tensor): A tensor with shape (B, 1).
    Returns:
        A tensor with shape (B, 4).
    """
    return tensor_1 * constant

def quaternion_multiply(tensor_1, tensor_2):
    """ Get the quaternion multiplication of the given tensor.
    Args:
        tensor_1(Tensor): A tensor to calculate.
        tensor_2(Tensor): A tensor to calculate
    Returns:
        The multiplication result.
    """
    if tensor_1.ndim == 1:
        tensor_1 = tensor_1[None, :]
    if tensor_2.ndim == 1:
        tensor_2 = tensor_2[None, :]

    if tensor_1.shape[-1] == 1 and tensor_2.shape[-1] == 4:
        return _constant_multiply(tensor_2, tensor_1)
    if tensor_2.shape[-1] == 1 and tensor_1.shape[-1] == 4:
        return _constant_multiply(tensor_1, tensor_2)
    if tensor_1.shape[-1] == 3:
        tensor_1 = msnp.pad(tensor_1, ((0, 0), (1, 0)), mode='constant', constant_value=0)
        return quaternion_multiply(tensor_1, tensor_2)
    if tensor_2.shape[-1] == 3:
        tensor_2 = msnp.pad(tensor_2, ((0, 0), (1, 0)), mode='constant', constant_value=0)
        return quaternion_multiply(tensor_1, tensor_2)
    return _quaternion_multiply(tensor_1, tensor_2)


batch_quaternion_multiply = vmap(quaternion_multiply, in_axes=(0, 0))


def quaternion_inverse(tensor_1):
    """ Get the quaternion conjugate of the given tensor.
    Args:
        tensor_1(Tensor): A tensor to calculate.
    Return:
        tensor_2(Tensor): The multiplication result with shape (B, 4).
    """
    if tensor_1.ndim == 1:
        tensor_1 = tensor_1[None, :]

    if tensor_1.shape[-1] == 1:
        return msnp.pad(tensor_1, ((0, 0), (0, 3)), mode='constant', constant_value=0)

    if tensor_1.shape[-1] == 3:
        return -msnp.pad(tensor_1, ((0, 0), (0, 3)), mode='constant', constant_value=0) / (msnp.norm(
            tensor_1, axis=-1
        )[:, None] ** 2)

    return msnp.hstack((tensor_1[:, 0][:, None], -tensor_1[:, 1:])) / (msnp.norm(
        tensor_1, axis=-1
    )[:, None] ** 2)

def hamiltonian_product(quaternion_1, tensor_2):
    """ Get the Hamiltonian-product of the given quaternion and tensor.
    Args:
        quaternion_1(Tensor): A tensor to calculate.
        tensor_2(Tensor): A tensor to calculate
    Returns:
        The hamiltonian product result.
    """
    if quaternion_1.ndim == 1:
        quaternion_1 = quaternion_1[None, :]
    if tensor_2.ndim == 1:
        tensor_2 = tensor_2[None, :]

    inverse_quaternion = quaternion_inverse(quaternion_1)
    op1 = quaternion_multiply(tensor_2, inverse_quaternion)
    res = quaternion_multiply(quaternion_1, op1)
    return res


batch_hamiltonian_product = vmap(hamiltonian_product, in_axes=(0, 0))


def quaternion_diff(tensor_1, tensor_2):
    """ Get the transform between tensor_1 and tensor_2.
    Args:
        tensor_1(Tensor): A tensor to calculate.
        tensor_2(Tensor): A tensor to calculate
    Returns:
        The transform quaternion result.
    """
    if tensor_1.ndim == 1:
        tensor_1 = tensor_1[None, :]
    if tensor_2.ndim == 1:
        tensor_2 = tensor_2[None, :]

    if tensor_1.shape[-1] == 1:
        tensor_1 = msnp.pad(tensor_1, ((0, 0), (0, 3)), mode='constant', constant_value=0)
        return quaternion_diff(tensor_1, tensor_2)
    if tensor_2.shape[-1] == 1:
        tensor_2 = msnp.pad(tensor_2, ((0, 0), (0, 3)), mode='constant', constant_value=0)
        return quaternion_diff(tensor_1, tensor_2)

    if tensor_1.shape[-1] == 3:
        tensor_1 = msnp.pad(tensor_1, ((0, 0), (1, 0)), mode='constant', constant_value=0)
        return quaternion_diff(tensor_1, tensor_2)
    if tensor_2.shape[-1] == 3:
        tensor_2 = msnp.pad(tensor_2, ((0, 0), (1, 0)), mode='constant', constant_value=0)
        return quaternion_diff(tensor_1, tensor_2)

    s_1 = tensor_1[:, 0]
    v_1 = tensor_1[:, 1:]
    v_2 = tensor_2[:, 1:]
    u = msnp.cross(v_1, v_2, axisc=-1)
    qs = msnp.zeros_like(s_1)
    qv = msnp.zeros_like(v_1)
    qs += v_1.norm(-1, keep_dims=True) * v_2.norm(-1, keep_dims=True) + ops.batch_dot(v_1, v_2, axes=-1)
    qv += u
    q = msnp.hstack((qs, qv))
    q /= q.norm(-1, keep_dims=True)
    return q


batch_quaternion_diff = vmap(quaternion_diff, in_axes=(0, 0))
