import re

import psutil


def cal_page_count(total_count: int, per_page_count: int) -> int:
    """
    根据总条数和每页数量计算页数

    Args:
        total_count: 总条数
        per_page_count: 每页数量

    Returns:
        总页数
    """

    if total_count >= 0 and per_page_count > 0:
        if total_count == 0:
            return 1
        else:
            return total_count // per_page_count if total_count % per_page_count == 0 else total_count // per_page_count + 1
    else:
        raise ValueError("总条数total_count必须>=0，每页数量per_page_count必须>0")


def has_invalid_windows_chars(string: str) -> bool:
    """
    检测windows下，字符串是否包含非法字符
        - <>:"/\|?*：这些字符在Windows中被视为非法字符。
        - \x00-\x1f：这些字符是ASCII控制字符，也被视为非法字符。

    Args:
        string: 需要检测的字符串

    Returns:
        检测结果：包含为True，不包含为False
    """

    pattern = r'[<>:"/\\|?*\x00-\x1f]'
    return bool(re.search(pattern, string))


def get_pids_by_exe_name(exe_name: str) -> list:
    """
    根据exe名称获取所有pid

    Args:
        exe_name: exe名称。示例：

    Returns:
        pid列表
    """

    return [p.pid for p in psutil.process_iter() if p.name() == exe_name]


def get_exe_name_by_pid(pid: int) -> str:
    """
    根据pid获取exe名称

    Args:
        pid: 进程id

    Returns:
        exe名称
    """

    result = ""
    for p in psutil.process_iter():
        if p.pid == pid:
            result = p.name()
    return result


if __name__ == '__main__':
    print(cal_page_count(11, 5))
    print(has_invalid_windows_chars("gg*geg"))
    print(get_pids_by_exe_name("QQBrowser.exe"))
    print(get_exe_name_by_pid(17044))
