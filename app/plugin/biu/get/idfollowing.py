# pylint: disable=relative-beyond-top-level
from ....platform import CMDProcessor


@CMDProcessor.plugin_register("api/biu/get/idfollowing")
class getIDFollowing(object):
    def __init__(self, MOD):
        self.MOD = MOD

    def pRun(self, cmd):
        try:
            args = self.MOD.args.getArgs(
                "userFollowing",
                [
                    "userID=%s" % self.MOD.biu.apiAssist.user_id,
                    "restrict=public",
                    "&totalPage=5",
                    "&groupIndex=0",
                ],
            )
        except:
            return {"code": 0, "msg": "missing parameters"}

        return {
            "code": 1,
            "msg": {
                "way": "get",
                "args": args,
                "rst": self.gank(args["ops"].copy(), args["fun"].copy()),
            },
        }

    def gank(self, opsArg, funArg):
        self.MOD.args.argsPurer(funArg, {"userID": "user_id"})
        status_arg = []
        r = []

        grpIdx = int(opsArg["groupIndex"])  # 组序号
        ttlPage = int(opsArg["totalPage"])  # 每组页数

        for p in range(grpIdx * ttlPage, (grpIdx + 1) * ttlPage):
            argg = funArg.copy()
            argg["offset"] = p * 30
            status_arg.append(argg)

        for x in self.MOD.biu.pool_srh.map(self.__thread_gank, status_arg):
            r += x

        return {"api": "app", "data": r}

    def __thread_gank(self, kw):
        try:
            data = self.MOD.biu.apiAssist.user_following(**kw)
        except:
            return []
        if "user_previews" in data and len(data["user_previews"]) != 0:
            return [x["user"] for x in data["user_previews"]]
        return []
