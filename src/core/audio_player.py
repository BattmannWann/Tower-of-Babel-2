import threading
import sounddevice as sd
import soundfile as sf
import numpy as np


class AudioPlayer: 
    
    def __init__(self):
        
        self.stop_event = threading.Event()
        self.threads = []
        
        
    def play_sound(self, path, devices, volume = 1.0):
        
        """
        Plays a sound file on multiple devices simultaneously 
        """
        #Stop any currently playing sounds first TODO: decide whether or not to keep this
        self.stop()
        
        try:
            data, samplerate = sf.read(path, dtype = "float32")
            
        except Exception as e:
            
            print(f"Error reading audio file {path}, see: {e}")
            return
        
        #Ensure data is 2D for channel manipulation
        if data.ndim == 1:
            data = np.expand_dims(data, axis = 1)
        
        #Apply the volume
        data = np.clip(data * volume, -1.0, 1.0)
        
        # Clear the stop event for the new playback
        self.stop_event.clear()
        self.threads = []
        
        #Start a playback thread for each valid device
        valid_devices = []
        
        for device in set(devices):
            
            if device is not None and device != -1:
                valid_devices.append(device)
                
        #If no valid devices found, try using None, which forces PortAudio
        if not valid_devices:
            
            print("Warning: No valid devices passed. Attempting system default...")
            valid_devices = [None]
            
            
        for device in valid_devices:
            
            thread = threading.Thread(
                target=self._play_on_device,
                args=(data.copy(), samplerate, device),
                daemon=True
            )
            
            thread.start()
            self.threads.append(thread)
                
                
    def _play_on_device(self, data, samplerate, device):
        
        """
        Background task that plays the audio on the speakers and mic
        """
        
        try:
            device_info = sd.query_devices(device, "output")
            max_channels = device_info["max_output_channels"]
            
            if max_channels <= 0:
                
                print(f"Device {device} has no output channels.")
                return
            
            #Match channels such that, for e.g., if MP3 is stereo but mic is mono, then:
            data = self._match_channels(data, max_channels)
            
            with sd.OutputStream(
                device = device,
                samplerate = samplerate,
                channels = data.shape[1],
                dtype = "float32"
            ) as stream:
                
                blocksize = 1024
                idx = 0
                
                while idx < len(data):
                    
                    #If the user presses stop, break the loop
                    if self.stop_event.is_set():
                        break
                    
                    chunk = data[idx:idx + blocksize]
                    stream.write(chunk)
                    
                    idx += blocksize
                    
                    
        except Exception as e:
            print(f"Unable to play sound on device: {device}, see: {e}")
            
            
    def _match_channels(self, data, max_channels):
        
        """
        Downmix or upmix audio to match the device's hardware limits.
        """
        
        num_channels = data.shape[1]
        
        if num_channels == max_channels:
            return data
        
        elif max_channels == 1:
            return data.mean(axis = 1, keepdims = True)
        
        elif max_channels == 2 and num_channels == 1:
            
            mono = data[:, 0]
            return np.column_stack((mono, mono))
        
        else:
            
            #Fallback: truncate or pad channels
            if num_channels > max_channels:
                return data[:, :max_channels]
            
            else:
                pad_width = max_channels - num_channels
                return np.hstack((data, np.zeros((len(data), pad_width), dtype = data.dtype)))
            
               
    def stop(self):
        
        """
        Signals all audio threads to stop immediately
        """
        self.stop_event.set()
        
        for t in self.threads:
            
            if t.is_alive():
                t.join(timeout = 0.2)
        
        
        
        
        
        