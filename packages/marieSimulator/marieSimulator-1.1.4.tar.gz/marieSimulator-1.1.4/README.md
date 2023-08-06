
# MarieSimulator

Simulator for MARIE (Machine Architecture that is Really Intuitive and Easy)

## Code Format

```Python

from marieSimulator import Marie, MarieReader as mr # import the marie and marie reader modules

marie = Marie(mr('trial')) # trial is the file containing Marie instructions
marie.run() # run the program
marie.show() # show memory in hex after running

```

## Trial File

```Text

        Load        X
        Add         One
        Store       X
        Halt
X,      HEX         0000
One,    HEX         0001

```

## GUI Mode

```Python
from marieSimulator import MarieGUI, app
import sys

window = MarieGUI()
window.show()
sys.exit(app.exec())
```

### Supported Opcodes (Instructions)

1. Load X
2. Store X
3. Add X
4. Subt X
5. Input
6. Output
7. Halt
8. Skipcond X
9. Jump X
10. Clear
11. AddI X
12. JumpI X
13. LoadI X
14. StoreI X
15. JnS X
16. HEX X
