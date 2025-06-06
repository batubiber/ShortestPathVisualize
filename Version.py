from dataclasses import dataclass

@dataclass
class Version:
    major: int = 1
    minor: int = 0
    patch: int = 0

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"



# VERSION HISTORY

#####################################################
# VERSION     : 1.0.0
# DATE        : 2025-06-07
# DESCRIPTION : 
# - Initial release
#
#####################################################







