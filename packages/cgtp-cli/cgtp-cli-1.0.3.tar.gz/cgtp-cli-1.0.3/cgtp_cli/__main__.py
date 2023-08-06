"""
cgtp.__main__: executed when cgtp directory is called as script.
with python -m cgtp_cli in the cgtp-cli directory (the root of the project)
"""

import sys
sys.path.append('cgtp_cli/cgtp_cli')
from cli import main

main()