""" util pure functions to validate and format generic fields """

import re

def acc_num_is_valid(acc_num: str) -> bool:
    try:
        if not isinstance(acc_num, str) or not re.match(r"^\d.\d.\d$", acc_num):
            raise ValueError()

    except ValueError:
        return False

    return True
