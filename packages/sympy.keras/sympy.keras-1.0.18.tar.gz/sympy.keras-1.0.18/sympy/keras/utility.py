from std.file import Text
import inspect
import traceback
import random

def availableGPU():
# pip install nvidia-ml-py3
    try:
        import pynvml  # @UnresolvedImport
        pynvml.nvmlInit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        return -1
#         shutil.copy('C:/Windows/System32/nvml.dll', 'C:/Program Files/NVIDIA Corporation/NVSMI/nvml.dll')
    # fix: copy C:\Windows\System32\nvml.dll and paste to C:\Program Files\NVIDIA Corporation\NVSMI\nvml.dll

    maxFreeMemory = 0
    maxFreeMemoryID = 0
    for i in range(pynvml.nvmlDeviceGetCount()):
        print('the %dth GPU info:' % i)
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print('used memory = ', meminfo.used / (1 << 20))
        print('free memory = ', meminfo.free / (1 << 20))
        print('total memory = ', meminfo.total / (1 << 20))
        if meminfo.free > maxFreeMemory:
            maxFreeMemoryID = i
            maxFreeMemory = meminfo.free

    print('GPU with the maximum Free Memory is %d, with Free Memory of %f MiB' % (maxFreeMemoryID, maxFreeMemory / (1 << 20)))
    
    ids = {maxFreeMemoryID}
    for i in range(pynvml.nvmlDeviceGetCount()):
        if i == maxFreeMemoryID:
            continue
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)        
        print('meminfo.free =', meminfo.free)
        print('maxFreeMemory * 0.9 =', maxFreeMemory * 0.9)
        if meminfo.free > maxFreeMemory * 0.999999:
            ids.add(i)
    
    print('ids =', ids)
    device_id = [*ids][random.randrange(0, len(ids))]
    print('selected device_id =', device_id)
    return device_id


def initialize_vocab(file, start=2):
    index = start
    vocab = {}
    for word in Text(file):
        assert word and word == word.strip()
        assert word not in vocab
        vocab[word] = index
        index += 1
    return vocab


def method_name(func): 
    if inspect.ismethod(func):
        return func.__self__.name + '.' + func.__func__.__name__
    
    if inspect.isfunction(func):
        return func.__qualname__
    
    return func.__qualname__

def print_decimal(avg):
    if abs(avg) > 1e-3:
        return '%.4f' % avg
    else:
        return '%.4e' % avg  
           
def print_time(eta):
    if eta > 3600:
        return '%d:%02d:%02d' % (eta // 3600, (eta % 3600) // 60, eta % 60)
    elif eta > 60:
        return '%d:%02d' % (eta // 60, eta % 60)
    else:
        return '%ds' % eta
