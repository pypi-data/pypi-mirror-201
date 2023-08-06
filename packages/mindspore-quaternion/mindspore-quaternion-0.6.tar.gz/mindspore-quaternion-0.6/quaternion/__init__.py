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


class Quaternion(nn.Cell):
    """ Quaternion object based on MindSpore.
    Args:
        q(Tensor): The input Tensor to construct a quaternion.
    """
    def __init__(self, q):
        super().__init__()
        if q.shape[-1] not in [4, 3, 1]:
            raise ValueError("The defined quaternion at least 4 elements should be given but got {}.".format(
                q.shape[-1]))
        if len(q.shape) == 1:
            q = q[None, :]
        if q.shape[-1] == 4:
            self.s = q[:, 0][:, None]
            self.v = q[:, 1:]
        elif q.shape[-1] == 1:
            self.s = q[:, 0][:, None]
            self.v = msnp.zeros((q.shape[0], 3))
        else:
            self.s = msnp.zeros((q.shape[0], 1))
            self.v = q[:, 0:]
        self.norm = nn.Norm(axis=-1)

    def __str__(self):
        return str(msnp.hstack((self.s, self.v)).asnumpy())

    def __abs__(self):
        q = msnp.hstack((self.s, self.v))
        return q.norm(axis=-1)

    def __len__(self):
        return self.s.shape[0]

    def __add__(self, other):
        q = msnp.hstack((self.s, self.v))
        oq = msnp.hstack((other.s, other.v))
        return Quaternion(q + oq)

    def __radd__(self, other):
        q = msnp.hstack((self.s, self.v))
        oq = msnp.hstack((other.s, other.v))
        return Quaternion(q + oq)

    def __sub__(self, other):
        q = msnp.hstack((self.s, self.v))
        oq = msnp.hstack((other.s, other.v))
        return Quaternion(q - oq)

    def __rsub__(self, other):
        q = msnp.hstack((self.s, self.v))
        oq = msnp.hstack((other.s, other.v))
        return Quaternion(oq - q)

    def _get_mul(self, other):
        s = self.s * other.s
        d = ops.batch_dot(self.v, other.v, axes=-1)
        s -= d
        v = msnp.zeros_like(self.v)
        v += self.s * other.v
        v += self.v * other.s
        v += msnp.cross(self.v, other.v, axisc=-1)
        q = msnp.hstack((s, v))
        return Quaternion(q)

    def __mul__(self, other):
        q = msnp.hstack((self.s, self.v))
        if isinstance(other, int) or isinstance(other, float):
            other = Tensor([other], ms.float32)
        if isinstance(other, Tensor):
            if other.size == 1:
                return Quaternion(q * other)
            elif other.size == q.shape[0]:
                if len(other.shape) == 1:
                    other = other[:, None]
                return Quaternion(q * other)
            elif other.shape[-1] == 3:
                if len(other.shape) == 1:
                    other = other[None, :]
                zeros = msnp.zeros((other.shape[0], 1))
                other = msnp.hstack((zeros, other))
                return self._get_mul(Quaternion(other))
        else:
            try:
                return self._get_mul(other)
            except ValueError:
                import traceback
                traceback.print_exc()

    def _get_rmul(self, other):
        s = self.s * other.s
        d = ops.batch_dot(self.v, other.v, axes=-1)
        s -= d
        v = msnp.zeros_like(self.v)
        v += self.s * other.v
        v += self.v * other.s
        v += msnp.cross(other.v, self.v, axisc=-1)
        q = msnp.hstack((s, v))
        return Quaternion(q)

    def __rmul__(self, other):
        q = msnp.hstack((self.s, self.v))
        if isinstance(other, int) or isinstance(other, float):
            other = Tensor([other], ms.float32)
        if isinstance(other, Tensor):
            if other.size == 1:
                return Quaternion(q * other)
            elif other.size == q.shape[0]:
                if len(other.shape) == 1:
                    other = other[:, None]
                return Quaternion(q * other)
            elif other.shape[-1] == 3:
                if len(other.shape) == 1:
                    other = other[None, :]
                zeros = msnp.zeros((other.shape[0], 1))
                other = msnp.hstack((zeros, other))
                return self._get_rmul(Quaternion(other))
        else:
            try:
                return self._get_rmul(other)
            except ValueError:
                import traceback
                traceback.print_exc()

    def conjugate(self):
        q = msnp.hstack((self.s, -self.v))
        return Quaternion(q)

    def __rtruediv__(self, other):
        inverse = Quaternion(self.to_tensor(quater=self.conjugate()) / (self.__abs__() ** 2))
        return other * inverse

    def __truediv__(self, other):
        inverse = 1 / other
        return self * inverse

    def to_tensor(self, quater=None):
        if quater is not None:
            q = msnp.hstack((quater.s, quater.v))
        else:
            q = msnp.hstack((self.s, self.v))
        return q

    def rotate(self, other):
        return self.to_tensor(self.__mul__(other))[:, 1:]

    def __or__(self, other, return_vector=True):
        op1 = None
        inverse = self.conjugate()
        q = msnp.hstack((inverse.s, inverse.v))
        if isinstance(other, int) or isinstance(other, float):
            other = Tensor([other], ms.float32)
        if isinstance(other, Tensor):
            if other.size == 1:
                op1 = Quaternion(other) * inverse
            elif other.size == q.shape[0]:
                if len(other.shape) == 1:
                    other = other[:, None]
                op1 = Quaternion(other) * inverse
            elif other.shape[-1] == 3:
                if len(other.shape) == 1:
                    other = other[None, :]
                zeros = msnp.zeros((other.shape[0], 1))
                other = msnp.hstack((zeros, other))
                op1 = Quaternion(other) * inverse
            elif other.shape[-1] == 4:
                if len(other.shape) == 1:
                    other = other[None, :]
                op1 = Quaternion(other) * inverse
        else:
            op1 = Quaternion(other) * inverse
        op2 = self.__mul__(op1)
        if return_vector:
            return self.to_tensor(quater=op2)[:, 1:]
        else:
            return op2

    def __rshift__(self, other):
        u = msnp.cross(self.v, other.v, axisc=-1)
        qs = msnp.zeros_like(self.s)
        qv = msnp.zeros_like(self.v)
        qs += self.v.norm(-1, keep_dims=True) * other.v.norm(-1, keep_dims=True) + ops.batch_dot(self.v, other.v, axes=-1)
        qv += u
        q = msnp.hstack((qs, qv))
        q /= q.norm(-1, keep_dims=True)
        return Quaternion(q)
