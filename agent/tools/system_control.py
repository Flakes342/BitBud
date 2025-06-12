import os
import sys
import psutil
import platform
import subprocess
import threading
import time
from datetime import datetime, timedelta

def get_system_info():
    """Get comprehensive system information"""
    try:
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": round(psutil.virtual_memory().total / (1024**3), 2),
                "available": round(psutil.virtual_memory().available / (1024**3), 2),
                "percent": psutil.virtual_memory().percent,
                "used": round(psutil.virtual_memory().used / (1024**3), 2)
            },
            "disk": {
                "total": round(psutil.disk_usage('/').total / (1024**3), 2),
                "used": round(psutil.disk_usage('/').used / (1024**3), 2),
                "free": round(psutil.disk_usage('/').free / (1024**3), 2),
                "percent": psutil.disk_usage('/').percent
            }
        }

        output = f""" 
                System Information: \n
                • OS: {info['system']} {info['release']} \n
                • Machine: {info['machine']} | Processor: {info['processor']} \n
                • Node: {info['node']} \n

                ⚡ Performance: \n
                • CPU Cores: {info['cpu_count']} | Usage: {info['cpu_percent']}% \n
                • RAM: {info['memory']['used']}GB / {info['memory']['total']}GB ({info['memory']['percent']}%) \n
                • Disk: {info['disk']['used']}GB / {info['disk']['total']}GB ({info['disk']['percent']}%)
                """.strip()
        
        return output
        
    except Exception as e:
        return f"[ERROR] Failed to get system info: {str(e)}"

def get_running_processes():
    """List running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sorting by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        output = "Top Processes (by CPU usage):\n"
        for i, proc in enumerate(processes[:10]):
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            output += f"{i+1:2d}. {proc['name']:<20} | PID: {proc['pid']:<8} | CPU: {cpu:5.1f}% | MEM: {mem:5.1f}%\n"
        
        return output
        
    except Exception as e:
        return f"[ERROR] Failed to get processes: {str(e)}"

def kill_process(pid):
    """Kill process by PID or name"""
    try:
        killed = []
        
        # Try as PID first
        try:
            pid = int(pid)
            proc = psutil.Process(pid)
            proc_name = proc.name()
            proc.terminate()
            proc.wait(timeout=5)
            killed.append(f"{proc_name} (PID: {pid})")
        except psutil.NoSuchProcess:
            return f"[ERROR] Process with PID {pid} not found"
        except psutil.AccessDenied:
            return f"[ERROR] Access denied to kill process {pid}"
        except ValueError:
            return f"[ERROR] Invalid PID format: {pid}"
        except Exception as e:
            return f"[ERROR] Failed to kill process {pid}: {str(e)}"
        
        if killed:
            return f"Killed processes: {', '.join(killed)}"
        else:
            return f"[ERROR] No processes found matching '{pid}'"
            
    except Exception as e:
        return f"[ERROR] Failed to kill process: {str(e)}"

def system_control(args: dict):
    """Main system control function"""
    cmd_type = args.get("type")
    
    if cmd_type == "get_system_info":
        return get_system_info()
    elif cmd_type == "processes":
        return get_running_processes()
    elif cmd_type == "kill_process":
        pid = args.get("process", "")
        if not pid:
            return "[ERROR] Please specify process PID"
        return kill_process(pid)
    elif cmd_type == "network":
        return get_network_info()
    elif cmd_type == "schedule":
        action = args.get("action", "shutdown")
        try:
            minutes = int(args.get("minutes", 5))
        except ValueError:
            return "[ERROR] Minutes must be a number"
        return scheduled_shutdown(minutes, action)
    elif cmd_type == "cancel_shutdown":
        return cancel_scheduled_shutdown()
    elif cmd_type == "immediate":
        action = args.get("action", "shutdown")
        return immediate_action(action)
    elif cmd_type == "battery":
        return get_battery_info()
    elif cmd_type == "temperature":
        return get_system_temperature()
    elif cmd_type == "cleanup":
        return clean_system()
    elif cmd_type == "volume":
        action = args.get("action", "get")
        value = args.get("value")
        return control_volume(action, value)
    elif cmd_type == "brightness":
        action = args.get("action", "get")
        value = args.get("value")
        return control_brightness(action, value)
    elif cmd_type == "bluetooth":
        action = args.get("action", "status")
        device = args.get("device")
        return control_bluetooth(action, device)
    elif cmd_type == "media":
        action = args.get("action", "status")
        return control_media(action)
    elif cmd_type == "lock":
        return lock_screen()
    else:
        return """[ERROR] Unknown system control command. Please specify a valid type.
        """