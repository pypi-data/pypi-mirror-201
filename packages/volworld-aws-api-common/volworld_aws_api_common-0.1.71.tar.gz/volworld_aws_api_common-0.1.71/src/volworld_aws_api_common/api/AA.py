from typing import Final
from volworld_common.api.CA import CA


# ====== A: Attribute ======
class AA(CA):

    Token: Final[str] = "tk"


AAList = [AA, CA]
