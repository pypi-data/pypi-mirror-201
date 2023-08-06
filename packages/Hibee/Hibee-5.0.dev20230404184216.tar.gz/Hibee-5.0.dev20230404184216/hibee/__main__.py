"""
Invokes hibee-admin when the hibee module is run as a script.

Example: python -m hibee check
"""
from hibee.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
