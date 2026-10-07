"""
自定义工具包小练习
"""

import my_utils.str_util
print(my_utils.str_util.str_reverse("abcdefg"))

from my_utils.str_util import str_reverse
print(str_reverse("abcdefg"))

from my_utils.str_util import substr
print(substr("0123456789", 2, 5))