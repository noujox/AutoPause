#this app will focus on one proccess listening windows focus, if the proccess lost focus must sent key esc to the proccess
import time
import win32process
import pyautogui
import win32gui
import threading
import psutil

# Process name or PID to monitor
class ProcessToMonitoring:
    def __init__(self, name, key_to_press):
        self.name = name
        self.key_to_press = key_to_press
        self.process_id = None
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def key_to_press(self):
        return self._key_to_press
    
    @key_to_press.setter
    def key_to_press(self, value):
        self._key_to_press = value
    
    @property
    def process_id(self):
        return self._process_id
    
    @process_id.setter
    def process_id(self, value):
        self._process_id = value

    @property
    def is_process_running(self):
        # Verificar si el proceso existe
        if self.process_id is not None:
            print(f"Monitoreando el proceso '{self.name}' con el ID: {self.process_id}")
            return True
        
        return False

    @property
    def has_process_focus(self):
        foreground_hwnd = win32gui.GetForegroundWindow()    # Obtener el identificador de la ventana en foco
        process_onFocus_id = win32process.GetWindowThreadProcessId(foreground_hwnd)     # Obtener el identificador del proceso asociado a la ventana con el foco
        # Verificar si el nombre del proceso coincide con el nombre especificado
        if process_onFocus_id == self.process_id:
            return True

        return False

def get_process_id_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def simulate_key_press(proc):
    hwnd = win32gui.GetWindow(proc.pid, 0)
    if hwnd:
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key_to_press), 0)

def monitor_process_focus(process):
    while True:
        # Verificar si el proceso actualmente en foco es el proceso que deseamos monitorear
        time.sleep(2)
        if process.has_process_focus:
            # El proceso tiene el foco, seguir monitoreando
            pass
        else:
            # El proceso no tiene el foco, enviar la tecla Esc
            simulate_key_press(process)
        time.sleep(1)

def main():
    # Crear un hilo para monitorear el foco del proceso
    proccess = ProcessToMonitoring("MiniAirways.exe", "esc")
    proccess.process_id = get_process_id_by_name(proccess.name)

    thread = threading.Thread(target=monitor_process_focus, args=(proccess,))
    thread.start()
    try:
        while proccess.is_process_running & thread.is_alive() :
            thread.join(timeout=3)
            print("Motinorizando...")
    except KeyboardInterrupt:
        print("Cerrando el hilo de monitoreo")
        thread.join()



if __name__ == "__main__":
    main()

