# Poliduckies common packages
[![PyPI version](https://badge.fury.io/py/poliduckie_segmentation.svg)](https://badge.fury.io/py/poliduckie_segmentation)


A package ready to be installed that provides the work made by the Poliduckie team

```
pip install poliduckie-segmentation
```

### Example for segmentation
```python
from poliduckie_segmentation.segmentation import Segmentation

image = [...]
segmentation = Segmentation()

# To predict:
prediction = segmentation.predict(image)

# To get the model:
segmentation.get_model()

# To get the model summary:
segmentation.get_model_summary()

```

### Example for MPC
```python
from poliduckie_segmentation.control import MPC

M = MPC()

# x = state, r = reference (with N=10 be like r=[[0.1, 0.1]]*10)
next_action = M.mpc(x, r)

```

### Example for Model
```python
from poliduckie_segmentation.model import Model

F = Model()

x, y, theta = 0,0,0
action = [1,1] # linear and angular speed
next_state = F.step(x, y, theta, previous_speed, previous_angular_speed, action)

# To use as action left and right wheel speed:
F.step_wheel_speed(x, y, theta, previous_speed, previous_angular_speed, action)

```
