# jsontodpg


## The Rundown

Build DearPyGui apps using json(ish) objects. It uses python dictionaries more than raw json.

As of dearpygui version 1.7, most ui compoents are working in jsontodpg. Further testing is needed.


## Instalation

```
pip install jsontodpg
```

## Usage
#### Viewports (Required Entry Point)

```python
#.py File

from jsontodpg import JsonToDpg
from dpgkeywords import *

main = {viewport: {width: 800, height: 800}}

JsonToDpg().parse(main)
```

#### Adding Windows

```python
#.py File

from jsontodpg import JsonToDpg
from dpgkeywords import *

main = {
    viewport: {width: 800, height: 800},
    "You can put anything you want as nested object list keys, as long as they are not a dearpygui keyword by them self, e.g window ": [
        {window: {label: "Example Window 1", width: 400, height: 400, pos: [0, 0]}},
        {window: {label: "Example Window 2", width: 400, height: 400}, pos: [400, 0]},
        {window: {label: "Example Window 3", width: 400, height: 400}, pos: [0, 400]},
        {window: {label: "Example Window 4", width: 400, height: 400}, pos: [400, 400]},
    ],
}

JsonToDpg().parse(main)
```

or...

```python
#.py File

from jsontodpg import JsonToDpg
from dpgkeywords import *

window_1 = {window: {label: "Example Window 1", width: 400, height: 400, pos: [0, 0]}}
window_2 = {window: {label: "Example Window 2", width: 400, height: 400}, pos: [400, 0]}
window_3 = {window: {label: "Example Window 3", width: 400, height: 400}, pos: [0, 400]}
window_4 = {
    window: {label: "Example Window 4", width: 400, height: 400},
    pos: [400, 400],
}


main = {
    viewport: {width: 800, height: 800},
    "You can put anything you want as nested object list keys, as long as they are not a dearpygui keyword by them self, e.g window ": [
        window_1,
        window_2,
        window_3,
        window_4,
    ],

}

JsonToDpg().parse(main)
```


