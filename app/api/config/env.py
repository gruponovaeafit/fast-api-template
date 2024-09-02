import os

# Add here all the environment variables

# Basic configuration
API_NAME = os.getenv('API_NAME')
JWT_SECRET = os.getenv('JWT_SECRET') # The JWT secret string
PRODUCTION_SERVER_URL = os.getenv('PRODUCTION_SERVER_URL')
DEVELOPMENT_SERVER_URL = os.getenv('DEVELOPMENT_SERVER_URL')
LOCALHOST_SERVER_URL = os.getenv('LOCALHOST_SERVER_URL')
IS_PRODUCTION = os.getenv('IS_PRODUCTION') # Boolean to determine if is prod environment or nah