# mindspore-quaternion--基于MindSpore深度学习框架的四元数数据结构
![](https://img.shields.io/pypi/l/mindspore-quaternion)

四元数在自动化等领域有非常广泛的应用，其必要性在于解决了使用欧拉角旋转的过程中有可能出现的欧拉角死锁问题。
关于更多的四元数的原理和计算方法，可以阅读本readme末尾的参考博客。

## 安装与更新
本软件支持pip一键安装与更新（这里推荐使用pypi原始的资源，国内的一些镜像源同步的并不是很及时）：
```bash
$ python3 -m pip install mindspore-quaternion --upgrade -i https://pypi.Python.org/simple/
```
也可以使用源码进行安装：
```bash
$ git clone https://gitee.com/dechin/mindspore-quaternion.git
$ cd mindspore-quaternion
$ python3 setup.py install
```

## 定义四元数
详细的代码可以参考[该链接](https://gitee.com/dechin/mindspore-quaternion/tree/master/examples)下的内容，这里我们只作为简单介绍。首先我们需要import一些必要的软件包：
```python
from quaternion import Quaternion
import numpy as np
import mindspore as ms
from mindspore import Tensor
```
接下来我们可以看一下各个不同shape的四元数定义。首先是定义一个常数的四元数，其实也就是`[s, 0, 0, 0]`这样的一个四元数：
```python
element = Tensor([0.], ms.float32)
element_quaternion = Quaternion(element)
print ('The type of element is: {}'.format(type(element_quaternion)))
print ('The value of element is: {}'.format(element_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of element is: <class 'quaternion.Quaternion'>
The value of element is: [[0. 0. 0. 0.]]
```
还可以定义三维矢量所对应的四元数，是如同`[0, vx, vy, vz]`这样的形式：
```python
vector = Tensor(np.arange(3), ms.float32)
vector_quaternion = Quaternion(vector)
print('The type of vector is: {}'.format(type(vector_quaternion)))
print('The value of vector is: {}'.format(vector_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of vector is: <class 'quaternion.Quaternion'>
The value of vector is: [[0. 0. 1. 2.]]
```
当然，如果一开始我们就定义好了一个完整的四维的四元数`[s, vx, vy, vz]`，那么也是可以用来直接构造一个四元数对象的：
```python
quater = Tensor(np.arange(4), ms.float32)
quater_quaternion = Quaternion(quater)
print('The type of quater is: {}'.format(type(quater_quaternion)))
print('The value of quater is: {}'.format(quater_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of quater is: <class 'quaternion.Quaternion'>
The value of quater is: [[0. 1. 2. 3.]]
```
这里必须要提一个最重要的point，那就是当我们使用一个深度学习框架去实现四元数这样的数据结构的时候，我们当然更多的是考虑到GPU加速在多batch的四元数计算
下的性能优势。所以这里我们也可以去定义一个更高维度的，多batch的四元数：
```python
batch_quater = Tensor(np.arange(16).reshape((4, 4)), ms.float32)
batch_quater_quaternion = Quaternion(batch_quater)
print('The type of batch_quater is: {}'.format(type(batch_quater_quaternion)))
print('The value of batch_quater is: {}'.format(batch_quater_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of batch_quater is: <class 'quaternion.Quaternion'>
The value of batch_quater is: [[ 0.  1.  2.  3.]
                               [ 4.  5.  6.  7.]
                               [ 8.  9. 10. 11.]
                               [12. 13. 14. 15.]]
```

## 四元数运算
在mindspore-quaternion中我们支持了一些四元数的基本运算，这里我们仅展示一些最常用的四元数基本运算：
```python
from quaternion import Quaternion
import mindspore as ms
from mindspore import Tensor
q1 = Tensor([1, 2, 3, 4], ms.float32)
q1_quaternion = Quaternion(q1)
q2 = Tensor([3, 1, 0, 5], ms.float32)
q2_quaternion = Quaternion(q2)
print ('The sum of q1 and q2 is: {}'.format(q1_quaternion + q2_quaternion))
print ('The product of q1 and q2 is: {}'.format(q1_quaternion * q2_quaternion))
```
上述代码的运行结果如下：
```bash
The sum of q1 and q2 is: [[4. 3. 3. 9.]]
The product of q1 and q2 is: [[-19.  22.   3.  14.]]
```
除了普通的四元数运算之外，mindspore-quaternion还可用于计算四元数与向量的哈密顿积：
```python
vector = Tensor([1, 2, 3], ms.float32)
hamiltonian = Tensor([0.5, 0.5, 0.5, 0.5], ms.float32)
hamiltonian_quaternion = Quaternion(hamiltonian)
print ('The Hamiltonian product of hamiltonian | vector > is: {}'.format(hamiltonian_quaternion | vector))
```
上述代码的运行结果如下：
```bash
The Hamiltonian product of hamiltonian | vector > is: [[3. 1. 2.]]
```
同时我们也可以使用逆变换：
```python
vector_transform = hamiltonian_quaternion.conjugate() | (hamiltonian_quaternion | vector)
print('The Hamiltonian product of hamiltonian^(-1) | hamiltonian | vector > is: {}'.format(vector_transform))
```
得到的结果如下所示：
```bash
The Hamiltonian product of hamiltonian^(-1) | hamiltonian | vector > is: [[1. 2. 3.]]
```
可用发现，我们经过一重四元数的变换和一重对应的逆变换之后，又得到了跟原来一样的向量。除此之外，我们最经常使用四元数的场景，
是对空间向量之间进行一个变换，比如我们可以获取两个向量之间的旋转四元数。首先我们需要定义一些初始向量和目标向量：
```python
src_vector = Tensor([1, 0, 0], ms.float32)
src_vector_quaternion = Quaternion(src_vector)
dst_vector1 = Tensor([0, 0, 1], ms.float32)
dst_vector1_quaternion = Quaternion(dst_vector1)
dst_vector2 = Tensor([np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3], ms.float32)
dst_vector2_quaternion = Quaternion(dst_vector2)
```
然后可以研究其中从初始向量到目标向量的变换四元数，再使用变换四元数作用到初始向量上：
```python
transform_quaternion = src_vector_quaternion >> dst_vector1_quaternion
print ('The quaternion transform from vector to target_vector is: {}'.format(transform_quaternion))
print ('The transform result is: {}'.format(transform_quaternion | src_vector))
transform_quaternion = src_vector_quaternion >> dst_vector2_quaternion
print('The quaternion transform from vector to target_vector is: {}'.format(transform_quaternion))
print('The transform result is: {}'.format(transform_quaternion | src_vector))
```
运行的结果如下所示：
```bash
The quaternion transform from vector to target_vector is: [[ 0.70710677  0.         -0.7071068   0.        ]]
The transform result is: [[0.         0.         0.99999994]]
The quaternion transform from vector to target_vector is: [[ 0.88807386  0.         -0.32505763  0.32505763]]
The transform result is: [[0.57735026 0.5773504  0.5773504 ]]
```
以上就是一些常用的四元数操作，更多操作可以参考`examples/`路径下的示例。

## 函数式运算
为了更好的支持MindSpore框架中对计算图的编译，这里如果我们使用MindSpore框架去构建一个Quaternion的对象，会引发Jit-FallBack
的报错，因此需要支持一些函数式的操作——保留Tensor的数据结构，仅引入一些四元数的操作。下述代码是一些比较简单的案例：
```python
from quaternion.functions import quaternion_multiply, quaternion_inverse, hamiltonian_product, quaternion_diff
import mindspore as ms
from mindspore import Tensor
import numpy as np

hamiltonian = Tensor([0.5, 0.5, 0.5, 0.5], ms.float32)
q1 = Tensor([1, 2, 3, 4], ms.float32)
q2 = Tensor([3, 1, 0, 5], ms.float32)
vector = Tensor([1, 2, 3], ms.float32)
src_vector = Tensor([1, 0, 0], ms.float32)
dst_vector1 = Tensor([0, 0, 1], ms.float32)
dst_vector2 = Tensor([np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3], ms.float32)

assert np.allclose(quaternion_inverse(hamiltonian).asnumpy(), np.array([[0.5, -0.5, -0.5, -0.5]], np.float32))
assert np.allclose(quaternion_multiply(q1, q2).asnumpy(), np.array([[-19., 22., 3., 14.]], np.float32))
assert np.allclose(quaternion_multiply(q2, q1).asnumpy(), np.array([[-19., -8., 15., 20.]], np.float32))
assert np.allclose(hamiltonian_product(hamiltonian, vector).asnumpy(), np.array([[0., 3., 1., 2.]], np.float32))
assert np.allclose(quaternion_diff(src_vector, dst_vector1).asnumpy(),
                       np.array([[0.70710677,  0.,         -0.7071068,   0.]], np.float32))
assert np.allclose(quaternion_diff(src_vector, dst_vector2).asnumpy(),
                       np.array([[0.88807386,  0.,         -0.32505763,  0.32505763]], np.float32))
```
如果运行正确，上述代码可以正常执行通过，否则会报错。

## 代码贡献
欢迎外部协作者提PR过来，有如下几点PR要求：
1. 先提Issue再提交PR，说清楚特性；
2. 贡献代码部分的flake8需要清空。

## 参考博客
1. https://www.cnblogs.com/dechinphy/p/quaternion-calc.html
