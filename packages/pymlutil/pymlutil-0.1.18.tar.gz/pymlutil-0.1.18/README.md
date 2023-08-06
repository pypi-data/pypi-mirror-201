# pymlutil
Python Machine Learning utilities:

## functions
### GaussianBasis
Computes a unit height gaussian bell curve function  \
$ GaussianBasis(x, zero, sigma) = e^{-\frac{(x-zero)^2}{2*sigma^2}} $ \
- x : function input
- zero : location of the peak center
- sigma: curve with or standard deviation

```python
def GaussianBasis(x, zero=0.0, sigma=0.33)
```

Example:
```python
x = np.arange(-2.0, 2.0, 0.01) 
y = GaussianBasis(torch.tensor(x))
plt.plot(x, y)
plt.show()
```
![gaussian_bias](./img/gaussian_bias.png)


### imutial

### jsonutil

- cmd(command, check=True, timeout=None): execute subprocess.call prining the execution time and results

### metrics

### s3
```
python3 -clone 

### torch_util

### version

### workflow


[Packaging Python Projects](https://www.freecodecamp.org/news/build-your-first-python-package/)
[How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

- Install twine:
    ```cmd
    pip3 install twine
    ```

- Build whl:
    ```cmd
    py setup.py sdist bdist_wheel
    ```

- Upload package to pipy
    ```cmd
    twine upload dist/*
    ```

[pymlutil](https://pypi.org/project/pymlutil)

- Load package into project
    ```cmd
    pip3 install --upgrade pymlutil
    ```

- Include pymlutil into project
```cmd
from pymlutil import *
```

## Notes
[Packaging and Distributing Python Projects](https://indico.in2p3.fr/event/20306/contributions/96819/attachments/64768/89975/packaging.pdf)
[Package Discovery](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)