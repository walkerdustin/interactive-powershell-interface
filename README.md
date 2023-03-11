# interactive-powershell-interface
This is an interface to use powershell commands from within python
The important thing here is, that all powershell commands are launched strictly
after each other (in serial) within the same context, so that you can
use powershell variables and cli tools, that rely on the current context of the powershell session

limitation: a small (constant) time overhead is added to each command, because I need to detect, when it has finished
You can not use multi line commands, that you would use with shift+enter in powershell.

The problem I had is, that I can not know when a command is finished.
To solve this, I use a trick:
I launch a powershell command, that just prints a random string
When the console output is equal to this string, I know that the command has finished

## Usage
check out the examples.ipynb file to see how to use it
```python
from interactive_powershell import InteractivePowershell
ps = InteractivePowershell()
ps.execute_command_and_wait_for_output("ls")
ps.execute_command_and_wait_for_output("ipconfig")
ps.execute_command_and_wait_for_output("$s = 'hello world'")
ps.execute_command_and_wait_for_output("$s") # 'hello world'
```	