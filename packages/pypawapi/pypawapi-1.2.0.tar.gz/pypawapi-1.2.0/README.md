## pawapi
`pawapi` is a Python package providing access to the PythonAnywhere API.

## Install
Use `pip` to install the latest version:

```bash
 $ pip install --upgrade pypawapi --user
```

## Usage
[Get your token](https://www.pythonanywhere.com/account/#api_token)

```python
from pawapi import Pawapi, Python3

TOKEN = "<your_token>"
USER = "<your_username>"

api = Pawapi(USER, TOKEN)
cpu_usage = api.cpu.get_info().content
print(cpu_usage)

domain = f"{USER}.pythonanywhere.com"
api.webapp.create(domain, Python3.PYTHON39)
app = api.webapp.list().content[-1]
print(app["id"])
```

### Available methods
* always_on
    * create
    * delete
    * get_info
    * list
    * restart
    * update
* console
    * create
    * get_info
    * get_output
    * kill
    * list
    * list_shared
    * send_input
* cpu
    * get_info
* file
    * delete
    * get_content
    * get_sharing_status
    * get_tree
    * start_sharing
    * stop_sharing
    * upload
* python
    * get_python3_version
    * set_python3_version
    * get_python_version
    * set_python_version
    * get_sar_version
    * set_sar_version
* scheduled_task
    * create
    * delete
    * get_info
    * list
    * update
* students
    * delete
    * list
* system
    * get_current_image
    * set_image
* webapp
    * list
    * create
    * get_info
    * update
    * delete
    * enable
    * disable
    * reload
    * add_ssl
    * get_ssl_info
    * delete_ssl
    * add_static_file
    * get_static_file_info
    * list_static_files
    * update_static_file
    * delete_static_file
    * add_static_header
    * get_static_header_info
    * update_static_header
    * delete_static_header
    * list_static_headers

## LICENSE
 The MIT License (MIT)    

 Copyright (c) 2019 Maraudeur    

 Permission is hereby granted, free of charge, to any person obtaining    
 a copy of this software and associated documentation files (the    
 "Software"), to deal in the Software without restriction, including    
 without limitation the rights to use, copy, modify, merge, publish,    
 distribute, sublicense, and/or sell copies of the Software, and to    
 permit persons to whom the Software is furnished to do so, subject to    
 the following conditions:    

 The above copyright notice and this permission notice shall be included    
 in all copies or substantial portions of the Software.    

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,    
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.    
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY    
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,    
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE    
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.    
