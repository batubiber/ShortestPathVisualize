from dataclasses import dataclass

@dataclass
class Version:
    major: int = 1
    minor: int = 1
    patch: int = 0

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"



# VERSION HISTORY

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







