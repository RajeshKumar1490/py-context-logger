# Python Context Logger

A python context logger with thread-local storage and context propagation for Python applications.

## Features

- Thread-local storage for log context.
- Dynamic updating of log context based on function parameters.
- Propagation of log context across threads.
- Decorators to easily integrate the logger into functions and classes.
- Add requestId by default to track the request if not provided. 
- Provides flexibility to configure logger name, log level, log format at the time of ContextLogger initialization.
- Method to get a log property value at any point of the request to pass across services.

## Installation

```bash
pip install py-context-logger
```

## Usage
```python
# Initialization
from context_logger import ContextLogger

from flask import Flask, request
from context_logger import UseContextLogger, ClearLogContext

app = Flask(__name__)
context_logger = ContextLogger()
# Also, we can configure name, log_format, level while instantiating ContextLogger
context_logger.initialize_context_logger()

@app.route('/some-endpoint', methods=['POST'])
@UseContextLogger({
    'resource_name': 'name',
    'resource_id': 'id',
    'headers.requestId': 'requestId',
    'headers.mailId': 'requestedMail'
})
@ClearLogContext()
def some_endpoint(resource_name: str, resource_id: str, headers: dict, logger=None):
    logger.info("Processing request")
    data = request.get_json()
    sample_class = SampleClass()
    user_name, company_name = "Sample user", "Sample company"
    sample_class.method_one(user_name=user_name, user_company=company_name)
    return {"status": "success"}


# Class-Level Logging
from context_logger import UseContextLogger

@UseContextLogger()
class SampleClass:
    def __init__(self, logger=None):
        self.logger = logger

    @UseContextLogger({"user_name": "user_name"})
    def method_one(self, user_name: str, user_company: str, logger=None):
        self.logger.info(f"Processing method_one with user")
        self.method_two(user_company=user_company)

    def method_two(self, user_company: str):
        self.logger.info(f"Processing method_two with company: {user_company}")
    
    # Sample method to fetch the transactionId/requestId to share across services
    def method_three(self, user_company: str):
        self.logger.info(f"Processing method_three with company: {user_company}")
        requestId = self.logger.get_property_value(log_property="requestId")
        # We can pass this requestId while make API calls or pushing to kafka etc.


if __name__ == '__main__':
    app.run(debug=True)

```
## Sample Log Format
```python
2024-07-16 16:20:54,197 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'requestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com'} - Processing request
2024-07-16 16:20:54,198 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'requestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'user_name': 'Sample user'} - Processing method_one with user
2024-07-16 16:20:54,199 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'requestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'user_name': 'Sample user'} - Processing method_two with company: Sample company
2024-07-16 16:20:55,000 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'requestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'user_name': 'Sample user'} - Processing method_three with company: Sample company
```


## Security Considerations
1. Ensure that sensitive information (e.g., personal data, credentials) is not logged unless necessary.<br>
2. Restrict access to log files to authorized personnel only.<br>
3. Implement measures to detect and prevent log manipulation.

## Performance
1. The use of thread-local storage ensures that log context updates are isolated to individual threads, minimizing contention and improving performance in multi-threaded applications.
2. The ContextThread class ensures that log context is propagated efficiently across threads, maintaining consistency without significant performance overhead.
3. The custom logger and decorators are designed to add minimal overhead to logging operations, ensuring that application performance is not adversely affected.

