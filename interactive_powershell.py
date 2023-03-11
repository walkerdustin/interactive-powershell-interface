from subprocess import Popen, PIPE
from typing import List

class InteractivePowershell:
    """This is an interface to use powershell commands from within python
    The important thing here is, that all powershell commands are launched strictly
    after each other (in serial) within the same context, so that you can
    use powershell variables and cli tools, that rely on the current context of the powershell session

    limitation: a small (constant) time overhead is added to each command, because I need to detect, when it has finished
    You can not use multi line commands, that you would use with shift+enter in powershell.

    The problem I had is, that I can not know when a command is finished.
    so after each command I launch another command, that just prints some random string
    if my the console output is then equal to this string, I know that both commands have finished
    """

    def __init__(self) -> None:
        print("InteractivePowershell.__init__(): Object Initialized")
        # this string is used to detect, when a command has finished
        # it can be any random characters, that are not output by a regular command
        self.done_string = (
            "siugvabheoishduvzigbahewosfughsedzifgvhoasugguhdfgu"
        )

        # start powershell process
        self.process = Popen("powershell", stdin=PIPE, stdout=PIPE, stderr=PIPE)

        # do the trick were I write another command and wait for it to finish
        self.process.stdin.write(f"Write-Output {self.done_string}\n".encode("cp850"))
        self.process.stdin.flush()
        s = self.__decode(self.process.stdout.readline()).strip()

        while s != self.done_string:
            s = self.__decode(self.process.stdout.readline()).strip()
        # now i know, that both commands have finished and stdout is empty
        print("InteractivePowershell.__init__():: powershell session started")

    def execute_command_and_wait_for_output(self, cmd: str) -> List[str]:
        """execute a powershell command in the same powershell context

        Args:
            cmd (str): a powershell command (just one line (without\\n))
                        else this might fail
        Returns:
            List[str]: the output of the powershell command as a list of strings
        """
        self.process.stdin.write(f"{cmd.strip()}\n".encode("cp850"))
        print(f"InteractivePowershell: PS command: {cmd} called")
        self.process.stdin.flush()
        self.process.stdin.write(f"Write-Output {self.done_string}\n".encode("cp850"))
        self.process.stdin.flush()
        output_lines: List[str] = []
        s = self.__decode(self.process.stdout.readline()).strip()
        # the first line is the prompt (PS C:\\user\\folder\\subfolder> ipconfig)
        # so we dont add this to output_lines
        
        # now we read lines until we find the done_string
        while s != self.done_string:
            s = self.__decode(self.process.stdout.readline()).strip()
            output_lines.append(s)
        # now we know. that both commands have finished
        print(f"InteractivePowershell: PS command: {cmd} finished")
        # the last two lines are therefor the prompt of the second command
        # and the done_string, so we remove them again
        return output_lines[0:-2]

    def terminate(self):
        print(f"InteractivePowershell.terminate(): PS Session terminated")
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=0.2)
        
    def __decode(self, b: bytes) -> str:
        selected_encoding = "cp850"
        other_possible_encodings = ["utf-8", "cp850", "cp1252", "cp437"] 
        try: 
            s = b.decode(selected_encoding)
        except UnicodeDecodeError as e:
            print(f"InteractivePowershell: UnicodeDecodeError: {e}")
            print(f"InteractivePowershell: trying other encodings")
            print(f"InteractivePowershell: selected_encoding: {selected_encoding}")
            print(f"InteractivePowershell: other_possible_encodings: {other_possible_encodings}")
            
        return s
