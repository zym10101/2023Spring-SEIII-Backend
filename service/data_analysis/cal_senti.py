import threading

import jpype


def cal_senti(body):
    Sentistrength = jpype.JClass("uk.ac.wlv.sentistrength.SentiStrength")

    # 创建对象并调用方法
    sentistrength = Sentistrength()
    result = str(sentistrength.initialiseAndRun(['sentidata', "./sentistrength/SentiStrength_Data/", "text", body]))
    print(result)

    # # 释放JVM资源
    # jpype.shutdownJVM()

    return result
