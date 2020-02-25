import os

ENV = os.getenv("ENV", "local").lower()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
SMS_DB_NAME = os.getenv("SMS_DB_NAME", "sms_dev")
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
