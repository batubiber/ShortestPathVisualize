"""
Version.py

This module contains the Version class, which is used to store the version number of the project.
"""

from dataclasses import dataclass

@dataclass
class Version:
    """
    Version class

    This class is used to store the version number of the project.
    """

    major: int = 1
    minor: int = 2
    patch: int = 0

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

# VERSION HISTORY

#####################################################
# VERSION     : 1.2.0
# DATE        : 2025-06-08
# DESCRIPTION :
# - Added pylint configuration and ran pylint on entire codebase
# - Fixed code style issues and improved code quality
# - Standardized code formatting according to PEP 8
# - Enhanced code readability and maintainability
#
#####################################################

#####################################################
# VERSION     : 1.1.0
# DATE        : 2025-06-08
# DESCRIPTION :
# - Added test suite
# - Added pytest integration
# - Improved documentation
# - Added various test cases
#
#####################################################

#####################################################
# VERSION     : 1.0.0
# DATE        : 2025-06-07
# DESCRIPTION :
# - Initial release
#
#####################################################
