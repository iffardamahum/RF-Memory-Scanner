from pymem import Pymem
import time
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve offsets from .env and convert from String to Integer (Hex)
BASE_PTR = int(os.getenv("BASE_PTR"), 16)
OFFSET_NAME = int(os.getenv("OFFSET_NAME"), 16)
OFFSET_DIST = int(os.getenv("OFFSET_DIST"), 16)
OFFSET_IS_DEAD = int(os.getenv("OFFSET_IS_DEAD"), 16)
OFFSET_OBJ_ID = int(os.getenv("OFFSET_OBJ_ID"), 16)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    # Initialize Pymem to RF_Online.bin process
    pm = Pymem("RF_Online.bin")
    base_module = pm.base_address
    print(f"Successfully Connected (Base: {hex(base_module)})")
except Exception as e:
    print(f"Failed to Connect: {e}")
    exit()

def run_radar():
    while True:
        clear_screen()
        print("=== RF Online Radar (Read Only) ===")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Using BASE_PTR from .env
            ptr_manager = pm.read_int(base_module + BASE_PTR)
            list_awal = ptr_manager + 0x0 
            
            detected_count = 0
            
            for i in range(300):
                # Read object address in each slot (4-byte)
                obj_addr = pm.read_int(list_awal + (i * 4))
                
                if obj_addr == 0 or obj_addr == 0xFFFFFFFF:
                    continue
                
                try:
                    # Using offsets from .env
                    name = pm.read_string(obj_addr + OFFSET_NAME, 24).strip()
                    dist = pm.read_float(obj_addr + OFFSET_DIST)
                    is_dead = pm.read_uint(obj_addr + OFFSET_IS_DEAD)
                    obj_id = pm.read_uint(obj_addr + OFFSET_OBJ_ID)

                    if len(name) > 1:
                        status = "ALIVE" if is_dead != 4294967295 else "DEAD"
                        print(f"[{status}] {name: <15} | ID: {obj_id: <8} | Distance: {dist:.2f}")
                        detected_count += 1
                        
                except:
                    continue
            
            if detected_count == 0:
                print("No objects detected in vicinity.")
                
        except Exception as e:
            print(f"Scanning Error: {e}")
        
        # Delay to prevent high CPU usage
        time.sleep(0.5)

if __name__ == "__main__":
    run_radar()