import modes
import communicate as com
from struct import pack, calcsize


modes.setCurrentMode(modes.allModes()[6])
print(com.sendParams(modes.getCurrentMode()))
