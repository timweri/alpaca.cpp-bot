import sys
from enum import Enum
import asyncio

class AlpacaCppInterface:
    class State(Enum):
        ACTIVE = 0
        TERMINATED = 1

    def __init__(self, alpaca_exec_path, model_path):
        self.alpaca_exec_path = alpaca_exec_path
        self.model_path = model_path
        self.state = AlpacaCppInterface.State.TERMINATED

    async def restart(self):
        await self.terminate()
        await self.start()

    async def start(self):
        if self.state == AlpacaCppInterface.State.ACTIVE:
            return False

        self.cli_process = await asyncio.create_subprocess_shell(
                ' '.join([self.alpaca_exec_path, '-m', self.model_path]),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=sys.stderr
            )
        # Signal whether the alpaca.cpp process is active
        self.state = AlpacaCppInterface.State.ACTIVE

        # Signal whether alpaca.cpp is ready for another prompt
        self.ready_for_prompt = True
        await self._initial_flush_readline()
        return True
    
    # Flush the initial prints before first user prompt
    async def _initial_flush_readline(self):
        # Shouldn't be reading if process is killed
        if self.state != AlpacaCppInterface.State.ACTIVE:
            return

        # Flush 1 empty line
        await self.cli_process.stdout.readline()

        # Flush "> "
        await self.cli_process.stdout.read(2)
        return True

    # Read the alpaca.cpp generated text
    # Blocks until alpaca.cpp finishes
    async def read(self):
        # Shouldn't be reading if process is killed or alpaca.cpp is waiting for
        # user input
        if self.state != AlpacaCppInterface.State.ACTIVE or self.ready_for_prompt:
            return False

        output = ''

        # Used to detect user input prompt
        prev_new_line = True

        while True:
            # Read output of alpaca.cpp char by char till we see "\n> "
            byte_array = bytearray()
            while True:
                try:
                    byte_array += await self.cli_process.stdout.read(1)
                    new_char = byte_array.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    pass

            # User input prompt detection
            if prev_new_line and new_char == ">":
                # Check if the next char is " "
                next_char = await self.cli_process.stdout.read(1)
                next_char = next_char.decode('utf-8')
                if next_char == " ":
                    break

                output += new_char + next_char
            else:
                output += new_char

            if new_char == '\n':
                prev_new_line = True
            else:
                prev_new_line = False

        # Now we wait for user input
        self.ready_for_prompt = True

        return output

    # Enters thhe next
    async def write(self, prompt):
        # Shouldn't be writing if process is killed or alpaca.cpp is not
        # ready for user input
        if self.state != AlpacaCppInterface.State.ACTIVE or not self.ready_for_prompt:
            return False

        prompt = prompt.strip()
        # print(f"Wrote \"{prompt}\" to chat")
        self.cli_process.stdin.write((prompt+"\n").encode('utf-8'))
        await self.cli_process.stdin.drain()

        # Now we wait for the model to generate text
        self.ready_for_prompt = False

        return True

    async def terminate(self):
        if self.state != AlpacaCppInterface.State.ACTIVE:
            return False

        self.state = AlpacaCppInterface.State.TERMINATED

        await self.cli_process.stdin.close()
        await self.cli_process.terminate()
        await self.cli_process.wait(timeout=0.2)
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.terminate()
