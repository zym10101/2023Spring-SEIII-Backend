import threading

import jpype

init = False
sentistrength = None


def cal_senti(body):
    global init
    global sentistrength
    if(init == False):
        Sentistrength = jpype.JClass("uk.ac.wlv.sentistrength.SentiStrength")
        # 创建对象并调用方法
        sentistrength = Sentistrength()
        init = True
    result = str(sentistrength.initialiseAndRun(['sentidata', "./sentistrength/SentiStrength_Data/", "text", body]))
    print(result)

    # # 释放JVM资源
    # jpype.shutdownJVM()

    return result
