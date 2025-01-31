# Settings

## Important Configurations to know ##

### Settings Files ###
There are multiple settings files located in the config folder at the root of the project. 

base.py --> Base settings shared by all settings files
local.py --> Local settings for local hosting.
production.py --> Production Settings for deployment.

---

### BASE_DIR ###

Instead of using:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__,)))
```
We are using:
```
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```
Because otherwise our BASE_DIR would start from the config folder where our settings files are located. 
By applying the PATH...parent.parent.parent we specify that the root directory of this project is the BASE_DIR.
See Two Scoops Of Django1.11 for more info