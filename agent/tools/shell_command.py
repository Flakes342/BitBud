import subprocess
from agent.llm import text_to_shell_command

def run_shell_command(command: str) -> str:
    try:
        output = subprocess.check_output(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=10,
            text=True  # returns output as string
        )
        return f"Output:\n{output.strip()}"
    
    except subprocess.CalledProcessError as e:
        return f"Error (code {e.returncode}):\n{e.output.strip()}"
    
    except subprocess.TimeoutExpired:
        return "Command timed out."
    
    except Exception as e:
        return f"Failed to run command: {e}"

        
def linux_commands(message: str):
    shell_cmd = text_to_shell_command(message)
    print(f"[Shell Command]: {shell_cmd}")

    # Ask for confirmation if risky
    if any(x in shell_cmd for x in ["rm", "reboot", "shutdown", "mkfs", "dd"]):
        return f"Dangerous command detected!: `{shell_cmd}`. I won’t run this without confirmation."

    result = run_shell_command(shell_cmd)
    return result

