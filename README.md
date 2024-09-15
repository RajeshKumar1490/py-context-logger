# Python Context Logger

A Python context logger using thread-local storage for log context propagation across threads, designed to simplify logging in multi-threaded applications. The logger dynamically updates log context based on function parameters and provides flexibility for customization at initialization.

## Features

- **Thread-local storage for log context**: Each thread maintains its own isolated log context, ensuring no cross-thread interference.
- **Dynamic log context updating**: Automatically updates log context based on function parameters, enabling detailed logging.
- **Log context propagation across threads**: Ensures log context consistency in multi-threaded environments.
- **Decorators for easy integration**: Integrate logging into functions and classes using decorators for cleaner and more maintainable code.
- **Optional `logRequestId` generation**: Automatically track request IDs unless explicitly disabled.
- **Configurable logger**: Customize the logger name, level, and format during initialization.
- **Constant key-value pairs**: Set log constants to ensure that specific key-value pairs are present in every log entry.
- **Retrieve log property values**: Get specific log property values (e.g., `requestId`) to propagate across services.

## Installation

```bash
pip install py-context-logger
```

---

## Usage

### Basic Initialization

```python
from context_logger import ContextLogger

# Initialize logger
context_logger = ContextLogger()

# Optional: Configure logger name, log format, and log level
context_logger.initialize_context_logger(name="MyLogger", log_format="%(asctime)s - %(message)s", level="INFO")
```

### Flask Example

Integrating the logger into a Flask application to automatically log request context and function parameters.

```python
from flask import Flask, request
from context_logger import UseContextLogger, ClearLogContext

app = Flask(__name__)
context_logger = ContextLogger()

# Initialize context logger
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

    # Class method logging example
    sample_class = SampleClass()
    user_name, company_name = "Sample user", "Sample company"
    sample_class.method_one(user_name=user_name, user_company=company_name)

    return {"status": "success"}

if __name__ == '__main__':
    app.run(debug=True)
```

### Class-Level Logging

Decorate class methods to automatically add context information to logs.

```python
from context_logger import UseContextLogger

@UseContextLogger()
class SampleClass:
    def __init__(self, logger=None):
        self.logger = logger

    @UseContextLogger({"user_name": "username", "log_constants": {"company_city": "New York"}})
    def method_one(self, user_name: str, user_company: str, logger=None):
        self.logger.info(f"Processing method_one with user")
        self.method_two(user_company=user_company)

    def method_two(self, user_company: str):
        self.logger.info(f"Processing method_two with company: {user_company}")
    
    # Fetch log property to pass across services
    def method_three(self, user_company: str):
        requestId = self.logger.get_property_value(log_property="requestId")
        self.logger.info(f"Processing method_three with company: {user_company} and requestId: {requestId}")
```

### Customization of Logger

You can initialize the logger with a custom name, log level, and format.

```python
context_logger.initialize_context_logger(
    name="CustomLogger",
    log_format="%(asctime)s - %(levelname)s - %(message)s",
    level="DEBUG"
)
```

### Retrieve Log Properties

At any point in the application, you can retrieve a log property (e.g., `requestId`) to pass it to other services or systems.

```python
requestId = context_logger.get_property_value("logRequestId")
```

---

## Sample Log Format

```bash
2024-07-16 16:20:54,197 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'logRequestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com'} - Processing request
2024-07-16 16:20:54,198 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'logRequestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'username': 'Sample user', 'company_city': 'New York'} - Processing method_one with user
2024-07-16 16:20:54,199 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'logRequestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'username': 'Sample user', 'company_city': 'New York'} - Processing method_two with company: Sample company
2024-07-16 16:20:55,000 - main.py:79 - INFO - {'name': 'sample_resource', 'id': '123', 'logRequestId': '6239237f-1f96-48c6-93f3-89fd2c63ea6d', 'requestedMail': 'sample-user@gmail.com', 'username': 'Sample user', 'company_city': 'New York'} - Processing method_three with company: Sample company
```

---

## Security Considerations

1. **Sensitive Data**: Ensure sensitive information (e.g., user credentials, personal data) is not logged unless absolutely necessary.
2. **Log Access Control**: Limit access to logs to authorized personnel only.
3. **Log Integrity**: Implement security measures to detect and prevent log manipulation or tampering.

---

## Performance

- **Thread-local storage**: The use of thread-local storage ensures isolated log contexts for each thread, minimizing contention in multi-threaded applications.
- **Efficient context propagation**: Log context is efficiently propagated across threads without introducing significant performance overhead.
- **Minimal overhead**: The custom logger and decorators are designed to introduce minimal performance impact, allowing for high-throughput logging.

---

## License

This project is licensed under the MIT License.

---

## Conclusion

The `py-context-logger` package provides a flexible, powerful logging system designed for multi-threaded Python applications. With easy-to-use decorators, thread-local storage, and support for custom log contexts, this logger simplifies complex logging scenarios while maintaining performance and flexibility.
