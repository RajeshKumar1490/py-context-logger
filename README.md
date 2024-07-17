# Python Context Logger

A python context logger with thread-local storage and context propagation for Python applications.

## Features

- Thread-local storage for log context.
- Dynamic updating of log context based on function parameters.
- Propagation of log context across threads.
- Decorators to easily integrate the logger into functions and classes.

## Installation

```bash
pip install py-context-logger
```

## Usage
```python
# Initialization
from context_logger import initialize_context_logger

from flask import Flask, request
from context_logger import UseContextLogger, ClearLogContext

app = Flask(__name__)
initialize_context_logger()

@app.route('/some-endpoint', methods=['POST'])
@UseContextLogger({
    'resource_name': 'name',
    'resource_id': 'id',
    'headers.requestId': 'requestId',
    'headers.mailId': 'requestedMail'
})
@ClearLogContext()
def some_endpoint(resource_name: str, resource_id: str, headers: dict, logger=None):
    data = request.get_json()
    logger.info("Processing request")
    return {"status": "success"}

if __name__ == '__main__':
    app.run(debug=True)

    

# Class-Level Logging
from context_logger import UseContextLogger

@UseContextLogger()
class SampleClass:
    def __init__(self, logger=None):
        self.logger = logger

    def method_one(self, param1):
        self.logger.info(f"Processing method_one with param1: {param1}")

    def method_two(self, param2):
        self.logger.info(f"Processing method_two with param2: {param2}")

        
        
# Method-Level Logging will override the class level
from context_logger import UseContextLogger

@UseContextLogger({
    'param1': 'param1_key',
    'param2': 'param2_key'
})
def some_method(param1, param2, logger=None):
    logger.info('Processing some method')
```
## Sample Log Format
```python
2024-07-16 16:20:54,197 - main.py:79 - INFO - {'requestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'id': '123', 'name': 'sample name', 'requestedMail': 'sample-user@gmail.com'} - Request received for fetching resources
```


## Security Considerations
1. Ensure that sensitive information (e.g., personal data, credentials) is not logged unless necessary.<br>
2. Restrict access to log files to authorized personnel only.<br>
3. Implement measures to detect and prevent log manipulation.

## Performance
1. The use of thread-local storage ensures that log context updates are isolated to individual threads, minimizing contention and improving performance in multi-threaded applications.
2. The ContextThread class ensures that log context is propagated efficiently across threads, maintaining consistency without significant performance overhead.
3. The custom logger and decorators are designed to add minimal overhead to logging operations, ensuring that application performance is not adversely affected.

