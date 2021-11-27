def deduplication(result_obj,sync=None):
    """ 字符串、元组、列表内容去重
    :param result_obj: 待去重序列对象
    :param sync: 分隔符,仅result_obj为str时需要
    :return: 已去重列表
    """
    temp = []
    res = ""
    if sync:
        result_obj = result_obj.split(sync)
        result = [temp.append(i) for i in result_obj if i not in temp]
        for i in temp[:-1]:
            res += (i + ' ')
        return res
    result = [temp.append(i) for i in result_obj if i not in temp]
    # 或使用
    # import numpy as np
    # return np.unique(result_obj)
    return temp
