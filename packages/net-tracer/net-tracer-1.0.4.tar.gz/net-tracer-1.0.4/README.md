# Net Tracer

Net Tracer is a Python tool for Network Security. Currently, it can:
- `scan.py`: Scan a target IP address or hostname for open ports and generates a CSV report of the scan results. 

## Requirements

- Python 3.7+
- concurrent.futures (https://docs.python.org/3/library/concurrent.futures.html)
- dnspython (https://github.com/rthalley/dnspython)
- json (https://docs.python.org/3/library/json.html)
- nmap (https://xael.org/pages/python-nmap-en.html)
- pyfiglet (https://pypi.org/project/pyfiglet/)

## Installation

You can install `net-tracer` using pip. First, make sure you have Python 3.6 or later installed on your system. Then, open a terminal or command prompt and enter the following command:
```cmd
pip install net-tracer
```

This will download and install the latest version of `net-tracer` and all its dependencies.

Alternatively, you can clone the GitHub repository and install `net-tracer` manually. First, navigate to the directory where you want to clone the repository, then enter the following commands:
```bash
git clone https://github.com/Morbid1134/Net-Tracer.git
cd net-tracer
pip install -r requirements.txt
pip install .
```

This will clone the repository, install the required dependencies, and install `net-tracer` locally on your system.

Once `net-tracer` is installed, you can import it into your Python scripts using the following statement:
```python
import net_tracer
```

That's it! You're ready to use `net-tracer` in your Python projects.

## Usage

You can simply call the imported functions from within your Python script.
```python
import net_tracer

net_tracer.tracer(target=None, ports=None, socket_threads=10000, nmap_threads=8, output=None, printing=False)
```

### Function Parameters
#### tracer(target, ports, socket_threads, nmap_threads, output, printing)
- `target`: The IP address or hostname of the target you want to scan. If no value is provided, the user will be prompted to enter a target at runtime.
- `ports`: A list or range of ports to scan. If no value is provided, all 65,535 ports will be scanned.
- `socket_threads`: The number of threads to use for socket scanning. Default is set to 10,000.
- `nmap_threads`: The number of threads to use for Nmap scanning. Default is set to 8.
- `output`: The name of the output file to write the results to. If no value is provided, the output array will not be written to a file. Output will always be returned and can be set to variable no matter if saving to a file.
- `printing`: If `True` then it will print details as the code is ran. Default is set to `False`.

### Examples

A full Python script is provided to show some ways of using this in [examples.py](examples.py)
  
## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
