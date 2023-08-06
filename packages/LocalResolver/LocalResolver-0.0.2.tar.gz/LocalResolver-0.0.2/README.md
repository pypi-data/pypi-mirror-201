![LocalResolver logo](https://mauricelambert.github.io/info/python/code/LocalResolver_small.png "LocalResolver logo")

# LocalResolver

## Description

This package implements local hostname resolver tool with scapy (using netbios and LLMNR query).

## Requirements

This package require: 

 - python3
 - python3 Standard Library
 - Scapy

## Installation

```bash
pip install LocalResolver 
```

## Examples

### Command lines

```bash
HostnameResolver -h
HostnameResolver 192.168.1.2
HostnameResolver 192.168.1.3,192.168.1.2,WIN10,HOMEPC,example.com
```

### Python3

```python
from LocalResolver import LocalResolver

localResolver = LocalResolver("192.168.1.45", timeout=3)
hostname = localResolver.resolve_NBTNS()
hostname = localResolver.resolve_LLMNR()
```

## Links

 - [Github Page](https://github.com/mauricelambert/LocalResolver)
 - [Documentation](https://mauricelambert.github.io/info/python/code/LocalResolver.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/code/LocalResolver.pyz)
 - [Pypi package](https://pypi.org/project/LocalResolver/)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
