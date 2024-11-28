import threading
import pynput.keyboard as keyboard # cannot use keyboard module as it is not supported in macOS :-)
import time

class InputManager:
    def __init__(self, key_states_queue, Timing, PRINT_WARNINGS):
        
        self.key_states = {}
        self.Timing = Timing
        self.key_states_queue = key_states_queue
        self.input_event = threading.Event()
        self.PRINT_WARNINGS = PRINT_WARNINGS
        self.max_poll_ticks_per_iteration = 1000
        
    def start_keyboard_hook(self):
        self.keyboard_listener = keyboard.Listener(
            on_press = self.on_key_press,
            on_release = self.on_key_release
        )
        self.keyboard_listener.start()
    
    def stop_keyboard_hook(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_hook = None
    
    def exit(self):
        """
        Stops the InputManager and cleans up resources.
        """
        self.Timing.exited = True
        self.stop_keyboard_hook()
        
    def queue_key_states(self):
        self.key_states_queue.put(self.key_states)

    def on_key_press(self, key):
        keyinfo = self.__get_key_info(key)
        try:
            KeyEntry = self.key_states[keyinfo]
            if KeyEntry:
                KeyEntry['previous'] = KeyEntry['current']
                KeyEntry['current'] = True
                
        except KeyError:
            KeyEntry = self.key_states.setdefault(keyinfo, {'current': False, 'previous': False})
            KeyEntry['previous'] = KeyEntry['current']
            KeyEntry['current'] = True
        
        self.queue_key_states()
        self.input_event.set()
         
    def on_key_release(self, key):
        keyinfo = self.__get_key_info(key)
        
        try:
            KeyEntry = self.key_states[keyinfo]
            if KeyEntry:
                KeyEntry['previous'] = KeyEntry['current']
                KeyEntry['current'] = False
                
        except KeyError:
            KeyEntry = self.key_states.setdefault(keyinfo, {'current': False, 'previous': False})
            KeyEntry['previous'] = KeyEntry['current']
            KeyEntry['current'] = False
        
        self.queue_key_states()
        self.input_event.set()
         
    def __get_key_info(self, key):
        try:
            return key.name
        except AttributeError:
            return key

    def wait_for_input_event(self, timeout = None):
        if self.input_event.wait(timeout = timeout):
            self.input_event.clear()  
            return True
        return False
     
    def input_loop(self):
        
        try:
            while not self.Timing.exited:
                
                ticks_this_iteration = 0
                iteration_start_time = time.perf_counter()
            
                self.Timing.current_input_tick_time = time.perf_counter() - self.Timing.start_times['input_loop']
                self.Timing.elapsed_times['input_loop'] = self.Timing.current_input_tick_time
                
                self.Timing.input_tick_delta_time += (self.Timing.current_input_tick_time - self.Timing.last_input_tick_time) / self.Timing.poll_interval
                self.Timing.last_input_tick_time = self.Timing.current_input_tick_time
                
                if self.Timing.do_first_input_tick:
                    self.do_input_tick()
                    self.Timing.do_first_input_tick = False
                    ticks_this_iteration += 1
                
                while self.Timing.input_tick_delta_time >= 1 and ticks_this_iteration < self.max_poll_ticks_per_iteration:
                    self.do_input_tick()
                    self.Timing.input_tick_delta_time -= 1
                    ticks_this_iteration += 1
                    
                if ticks_this_iteration > self.max_poll_ticks_per_iteration:
                    if self.PRINT_WARNINGS:
                        print("\033[93mWARNING: Too many ticks processed in one iteration of Input Loop, recalibrating...\033[0m")
                        
                    self.Timing.input_tick_delta_time = 1
                
                if self.Timing.current_input_tick_time > self.Timing.input_tick_counter_last_cleared + 1:
                    self.get_poll_rate()
                    self.Timing.input_tick_counter = 0
                    self.Timing.input_tick_counter_last_cleared += 1

                iteration_end_time = time.perf_counter()
                elapsed_time = iteration_end_time - iteration_start_time
                
                if elapsed_time > self.Timing.poll_interval and self.PRINT_WARNINGS:
                    print(f"\033[93mWARNING: Input loop iteration took too long! [{elapsed_time:.6f} s]\033[0m")
                
                time.sleep(max(0, self.Timing.poll_interval - elapsed_time))
                   
        except Exception as e:
            print(f"\033[91mError in {threading.current_thread().name}: {e}\033[0m")
            return
        
        finally:
            if self.PRINT_WARNINGS:
                print(f"\033[92mInput loop Timing.exited in {threading.current_thread().name}\033[0m")
            self.Timing.exited = True
            return
        
    def do_input_tick(self):
        
        if self.Timing.exited:
            return
        
        if self.wait_for_input_event():
           
            self.key_states = self.key_states_queue.get()
            print(self.key_states)
            
        self.Timing.input_tick_counter += 1
        
    def get_poll_rate(self):
        self.Timing.POLLING_RATE = self.Timing.input_tick_counter