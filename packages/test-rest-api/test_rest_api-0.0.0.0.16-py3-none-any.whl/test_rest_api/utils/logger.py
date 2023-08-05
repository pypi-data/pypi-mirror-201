import logging

# Create custom logger for test_rest_api package
test_rest_api_logger = logging.getLogger('test_rest_api')
# Set the logging level
test_rest_api_logger.setLevel(logging.INFO)
# Configure the handler for test_rest_api_logger
test_rest_api_stream_handler = logging.StreamHandler()
# Configure the formatter for test_rest_api_logger
test_rest_api_formatter = logging.Formatter("%(asctime)s: %(message)s")
# Add formatter to the handler
test_rest_api_stream_handler.setFormatter(test_rest_api_formatter)
# Add handler to the logger
test_rest_api_logger.addHandler(test_rest_api_stream_handler)
