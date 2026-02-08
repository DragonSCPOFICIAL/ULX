#!/usr/bin/env python3
"""
LNX - Universal Hardware Detector

Detecta TUDO em qualquer dispositivo Linux:
- Notebook, Desktop, Celular, Servidor, Raspberry Pi, etc
- Adapta-se automaticamente ao hardware disponível
"""

import os
import subprocess
import json
from pathlib import Path

class UniversalHardwareDetector:
    """Detector universal de hardware para qualquer Linux"""
    
    def __init__(self):
        self.hardware = {
            'device_type': None,
            'cpu': {},
            'gpu': {},
            'ram': {},
            'storage': {},
            'battery': {},
            'thermal': {},
            'network': {},
            'usb': {},
            'pcie': {},
            'sensors': {},
        }
    
    # ===== DETECÇÃO DE TIPO DE DISPOSITIVO =====
    
    def detect_device_type(self):
        """Detecta tipo de dispositivo"""
        
        # Verifica se é notebook (bateria)
        if Path('/sys/class/power_supply/BAT0').exists() or \
           Path('/sys/class/power_supply/BAT1').exists():
            self.hardware['device_type'] = 'notebook'
            return
        
        # Verifica se é celular/Android
        if os.path.exists('/system/build.prop'):
            self.hardware['device_type'] = 'android'
            return
        
        # Verifica se é Raspberry Pi
        try:
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read()
                if 'Raspberry' in model:
                    self.hardware['device_type'] = 'raspberry_pi'
                    return
        except:
            pass
        
        # Verifica se é servidor
        try:
            result = subprocess.run(['dmidecode', '-s', 'system-product-name'],
                                  capture_output=True, text=True, timeout=2)
            if 'Server' in result.stdout or 'Blade' in result.stdout:
                self.hardware['device_type'] = 'server'
                return
        except:
            pass
        
        # Default: Desktop
        self.hardware['device_type'] = 'desktop'
    
    # ===== DETECÇÃO DE CPU =====
    
    def detect_cpu(self):
        """Detecta informações da CPU"""
        cpu = {}
        
        try:
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                
                # Cores
                cpu['cores'] = content.count('processor')
                
                # Modelo
                for line in content.split('\n'):
                    if line.startswith('model name'):
                        cpu['model'] = line.split(':', 1)[1].strip()
                    elif line.startswith('cpu MHz'):
                        cpu['frequency_mhz'] = float(line.split(':', 1)[1].strip())
                
                # Instruções SIMD
                cpu['flags'] = []
                for line in content.split('\n'):
                    if line.startswith('flags'):
                        flags = line.split(':', 1)[1].strip().split()
                        
                        # Detecta instruções importantes
                        if 'avx512f' in flags:
                            cpu['flags'].append('AVX-512')
                        if 'avx2' in flags:
                            cpu['flags'].append('AVX2')
                        if 'avx' in flags:
                            cpu['flags'].append('AVX')
                        if 'sse4_2' in flags:
                            cpu['flags'].append('SSE4.2')
                        if 'neon' in flags:
                            cpu['flags'].append('NEON')  # ARM
                        if 'sve' in flags:
                            cpu['flags'].append('SVE')   # ARM
                        
                        break
        except:
            pass
        
        self.hardware['cpu'] = cpu
    
    # ===== DETECÇÃO DE GPU =====
    
    def detect_gpu(self):
        """Detecta informações de GPU"""
        gpu = {}
        
        # NVIDIA CUDA
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total',
                                   '--format=csv,noheader'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpu['nvidia'] = {
                    'count': len(lines),
                    'devices': lines
                }
        except:
            pass
        
        # AMD GPU
        try:
            result = subprocess.run(['rocm-smi', '--showproductname'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                gpu['amd'] = result.stdout.strip()
        except:
            pass
        
        # Intel GPU
        try:
            result = subprocess.run(['lspci', '-nn'],
                                  capture_output=True, text=True, timeout=2)
            if 'Intel' in result.stdout and 'VGA' in result.stdout:
                gpu['intel'] = 'Integrated Intel GPU'
        except:
            pass
        
        # GPU ARM (Mali, Adreno)
        try:
            with open('/proc/device-tree/gpu@', 'r', errors='ignore') as f:
                gpu['arm'] = f.read()
        except:
            pass
        
        # Vulkan
        try:
            result = subprocess.run(['vulkaninfo', '--summary'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                gpu['vulkan'] = 'Available'
        except:
            pass
        
        # OpenCL
        try:
            result = subprocess.run(['clinfo'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                gpu['opencl'] = 'Available'
        except:
            pass
        
        self.hardware['gpu'] = gpu
    
    # ===== DETECÇÃO DE RAM =====
    
    def detect_ram(self):
        """Detecta informações de RAM"""
        ram = {}
        
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        ram['total_mb'] = kb / 1024
                        ram['total_gb'] = kb / (1024 * 1024)
                    elif line.startswith('MemAvailable:'):
                        kb = int(line.split()[1])
                        ram['available_mb'] = kb / 1024
        except:
            pass
        
        # Tipo de RAM (DDR4, DDR5, etc)
        try:
            result = subprocess.run(['dmidecode', '-t', 'memory'],
                                  capture_output=True, text=True, timeout=2)
            if 'DDR5' in result.stdout:
                ram['type'] = 'DDR5'
            elif 'DDR4' in result.stdout:
                ram['type'] = 'DDR4'
            elif 'DDR3' in result.stdout:
                ram['type'] = 'DDR3'
        except:
            pass
        
        self.hardware['ram'] = ram
    
    # ===== DETECÇÃO DE ARMAZENAMENTO =====
    
    def detect_storage(self):
        """Detecta informações de armazenamento"""
        storage = {}
        
        try:
            result = subprocess.run(['lsblk', '-d', '-o', 'name,rota,size'],
                                  capture_output=True, text=True, timeout=2)
            
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    device = {
                        'name': parts[0],
                        'type': 'SSD' if parts[1] == '0' else 'HDD',
                        'size': parts[2] if len(parts) > 2 else 'Unknown'
                    }
                    devices.append(device)
            
            storage['devices'] = devices
        except:
            pass
        
        # NVMe
        try:
            result = subprocess.run(['nvme', 'list'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                storage['nvme'] = 'Available'
        except:
            pass
        
        self.hardware['storage'] = storage
    
    # ===== DETECÇÃO DE BATERIA =====
    
    def detect_battery(self):
        """Detecta informações de bateria (notebook)"""
        battery = {}
        
        try:
            result = subprocess.run(['acpi', '-b'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                battery['status'] = result.stdout.strip()
        except:
            pass
        
        # Lê diretamente do sysfs
        try:
            bat_path = Path('/sys/class/power_supply/BAT0')
            if bat_path.exists():
                battery['capacity'] = open(bat_path / 'capacity').read().strip()
                battery['status'] = open(bat_path / 'status').read().strip()
        except:
            pass
        
        self.hardware['battery'] = battery
    
    # ===== DETECÇÃO DE THERMAL =====
    
    def detect_thermal(self):
        """Detecta sensores térmicos"""
        thermal = {}
        
        try:
            result = subprocess.run(['sensors'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                thermal['sensors'] = result.stdout.strip()
        except:
            pass
        
        # Lê diretamente do sysfs
        try:
            thermal_path = Path('/sys/class/thermal')
            if thermal_path.exists():
                temps = []
                for zone in thermal_path.glob('thermal_zone*'):
                    try:
                        temp = int(open(zone / 'temp').read()) / 1000
                        temps.append({'zone': zone.name, 'temp_c': temp})
                    except:
                        pass
                thermal['zones'] = temps
        except:
            pass
        
        self.hardware['thermal'] = thermal
    
    # ===== DETECÇÃO DE REDE =====
    
    def detect_network(self):
        """Detecta informações de rede"""
        network = {}
        
        try:
            result = subprocess.run(['ip', 'link', 'show'],
                                  capture_output=True, text=True, timeout=2)
            
            interfaces = []
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith(' '):
                    parts = line.split(':')
                    if len(parts) > 1:
                        interfaces.append(parts[1].strip())
            
            network['interfaces'] = interfaces
        except:
            pass
        
        self.hardware['network'] = network
    
    # ===== DETECÇÃO DE USB =====
    
    def detect_usb(self):
        """Detecta dispositivos USB"""
        usb = {}
        
        try:
            result = subprocess.run(['lsusb'],
                                  capture_output=True, text=True, timeout=2)
            usb['devices'] = len(result.stdout.strip().split('\n'))
        except:
            pass
        
        self.hardware['usb'] = usb
    
    # ===== DETECÇÃO DE PCIE =====
    
    def detect_pcie(self):
        """Detecta dispositivos PCIe"""
        pcie = {}
        
        try:
            result = subprocess.run(['lspci'],
                                  capture_output=True, text=True, timeout=2)
            pcie['devices'] = len(result.stdout.strip().split('\n'))
        except:
            pass
        
        self.hardware['pcie'] = pcie
    
    # ===== DETECÇÃO COMPLETA =====
    
    def detect_all(self):
        """Detecta tudo"""
        print("\n[LNX] Detectando hardware...")
        
        self.detect_device_type()
        self.detect_cpu()
        self.detect_gpu()
        self.detect_ram()
        self.detect_storage()
        self.detect_battery()
        self.detect_thermal()
        self.detect_network()
        self.detect_usb()
        self.detect_pcie()
        
        return self.hardware
    
    # ===== IMPRESSÃO =====
    
    def print_summary(self):
        """Imprime resumo do hardware"""
        print("\n[LNX] ╔════════════════════════════════════════╗")
        print("[LNX] ║   DETECÇÃO UNIVERSAL DE HARDWARE       ║")
        print("[LNX] ╚════════════════════════════════════════╝\n")
        
        print(f"[LNX] Tipo de Dispositivo: {self.hardware['device_type'].upper()}")
        
        if self.hardware['cpu']:
            print(f"\n[LNX] CPU:")
            print(f"[LNX]   Cores: {self.hardware['cpu'].get('cores', 'Unknown')}")
            print(f"[LNX]   Modelo: {self.hardware['cpu'].get('model', 'Unknown')}")
            print(f"[LNX]   Frequência: {self.hardware['cpu'].get('frequency_mhz', 'Unknown')} MHz")
            if self.hardware['cpu'].get('flags'):
                print(f"[LNX]   Instruções: {', '.join(self.hardware['cpu']['flags'])}")
        
        if self.hardware['gpu']:
            print(f"\n[LNX] GPU:")
            for gpu_type, info in self.hardware['gpu'].items():
                print(f"[LNX]   {gpu_type.upper()}: {info}")
        
        if self.hardware['ram']:
            print(f"\n[LNX] RAM:")
            print(f"[LNX]   Total: {self.hardware['ram'].get('total_gb', 'Unknown'):.2f} GB")
            print(f"[LNX]   Tipo: {self.hardware['ram'].get('type', 'Unknown')}")
        
        if self.hardware['storage']['devices']:
            print(f"\n[LNX] Armazenamento:")
            for dev in self.hardware['storage']['devices']:
                print(f"[LNX]   {dev['name']}: {dev['type']} ({dev['size']})")
        
        if self.hardware['battery']:
            print(f"\n[LNX] Bateria:")
            print(f"[LNX]   {self.hardware['battery'].get('status', 'Unknown')}")
        
        if self.hardware['thermal'].get('zones'):
            print(f"\n[LNX] Temperatura:")
            for zone in self.hardware['thermal']['zones']:
                print(f"[LNX]   {zone['zone']}: {zone['temp_c']:.1f}°C")
        
        print("\n")
    
    def to_json(self):
        """Retorna hardware como JSON"""
        return json.dumps(self.hardware, indent=2, default=str)

def main():
    detector = UniversalHardwareDetector()
    hardware = detector.detect_all()
    detector.print_summary()
    
    # Salva em arquivo
    with open('/tmp/hardware_profile.json', 'w') as f:
        f.write(detector.to_json())
    
    print("[LNX] Perfil salvo em: /tmp/hardware_profile.json")

if __name__ == '__main__':
    main()
