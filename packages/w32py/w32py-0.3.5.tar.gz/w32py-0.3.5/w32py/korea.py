from pathlib import Path
from typing import Any, Callable

from w32py.win import pumpWaitingMessages, qApplication, qAxWidget


class CALLBACK:
    OnReceiveData: list[Callable[[dict[str, Any]], None]] = []
    OnReceiveRealData: list[Callable[[dict[str, Any]], None]] = []


def parse_field(line: str) -> dict[str, Any]:
    cols = [s.strip() for s in line.split(",")]
    return {
        "name": cols[1],
        "desc": cols[0],
        "type": cols[2],
        "size": cols[3],
    }


def parse_lines(lines: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {
        "desc": "",
        "input": {},
        "output": {},
    }
    lines = list(
        filter(lambda x: x, map(lambda x: x.replace(";", "").strip(), lines))
    )
    for i, line in enumerate(lines):
        if line.startswith("T,") or line.startswith("R,"):
            parsed["desc"] = line.split(",")[1].strip()
        elif line == "begin":
            latest_begin = i
        elif line == "end":
            block_info = [
                s.strip() for s in lines[latest_begin - 1].split(",")
            ]
            parsed[block_info[1]][block_info[0]] = {
                "occurs": block_info[-1].startswith("occurs"),
                "fields": list(map(parse_field, lines[latest_begin + 1 : i])),
            }
    return parsed


def parse_res(p: Path) -> dict[str, Any]:
    with open(p, "rt", encoding="cp949") as fp:
        return parse_lines(fp.readlines())


class Query:
    def __init__(self) -> None:
        self.com: Any = None
        self.meta: dict[str, Any] = {}
        self.received = False
        self.tr = ""

    def init(self, com: Any, p: Path) -> None:
        self.com = com
        self.com.ReceiveData.connect(self.OnReceiveData)
        self.com.ReceiveErrorData.connect(self.OnReceiveErrorData)
        self.meta = parse_res(p)
        self.received = False
        self.tr = p.stem

    def OnReceiveData(self) -> None:
        RtCode = self.com.dynamicCall("GetRtCode()")
        if RtCode != "0":
            self.OnReceiveErrorData()
            return

        block: dict[str, Any] = {}
        for nBlockIdx, (szBlockName, v) in enumerate(
            self.meta["output"].items()
        ):
            fields = v["fields"]
            if v["occurs"]:
                block[szBlockName] = [
                    self.getBlock(nBlockIdx, nRecIdx, fields)
                    for nRecIdx in range(
                        self.com.dynamicCall(
                            "GetMultiRecrodCount(int)", nBlockIdx
                        )
                    )
                ]
            else:
                nRecIdx = 0
                block[szBlockName] = self.getBlock(nBlockIdx, nRecIdx, fields)
        responseQuery = {
            "err": "",
            "tr": self.tr,
            "block": block,
        }
        self.received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def OnReceiveErrorData(self) -> None:
        RtCode = self.com.dynamicCall("GetRtCode()")
        ReqMsgCode = self.com.dynamicCall("GetReqMsgCode()")
        ReqMessage = self.com.dynamicCall("GetReqMessage()")
        responseQuery = {
            "err": f"{RtCode}, {ReqMsgCode}, {ReqMessage}",
            "tr": self.tr,
            "block": {},
        }
        self.received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def getBlock(
        self,
        nBlockIdx: int,
        nRecIdx: int,
        fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        nAttrType = 0
        block: dict[str, Any] = {}
        for nFieldIdx, field in enumerate(fields):
            szFieldName = field["name"]
            val = self.com.dynamicCall(
                "GetMultiData(int, int, int, int)",
                nBlockIdx,
                nRecIdx,
                nFieldIdx,
                nAttrType,
            )
            block[szFieldName] = f"{val}"
        return block

    def setBlock(
        self,
        szBlockName: str,
        nBlockIdx: int,
        nRecIdx: int,
        fields: list[dict[str, Any]],
        block: dict[str, Any],
    ) -> str:
        for nFieldIdx, field in enumerate(fields):
            szFieldName = field["name"]
            val = block.get(szFieldName)
            if val is None:
                return (
                    f"InvalidField, {szBlockName}"
                    f", {nRecIdx}, {szFieldName}"
                )
            if szFieldName.endswith("PWD"):
                val = self.com.dynamicCall("GetEncryptPassword(QString)", val)
            self.com.dynamicCall(
                "SetMultiBlockData(int, int, int, QString)",
                nBlockIdx,
                nRecIdx,
                nFieldIdx,
                val,
            )
        return ""

    def query(self, requestQuery: dict[str, Any]) -> str:
        requestBlock = requestQuery["block"]
        for nBlockIdx, (szBlockName, v) in enumerate(
            self.meta["input"].items()
        ):
            fields = v["fields"]
            if v["occurs"]:
                blocks = requestBlock.get(szBlockName)
                if blocks is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(blocks, list):
                    return (
                        f"InvalidBlockType, {szBlockName}"
                        f", list, {type(blocks)}"
                    )
                for nRecIdx, block in enumerate(blocks):
                    if not isinstance(block, dict):
                        return (
                            f"InvalidBlockType, {szBlockName}"
                            f", list, {nRecIdx}, dict, {type(block)}"
                        )
                    err = self.setBlock(
                        szBlockName, nBlockIdx, nRecIdx, fields, block
                    )
                    if err:
                        return err
            else:
                nRecIdx = 0
                block = requestBlock.get(szBlockName)
                if block is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(block, dict):
                    return (
                        f"InvalidBlockType, {szBlockName}"
                        f", dict, {type(block)}"
                    )
                err = self.setBlock(
                    szBlockName, nBlockIdx, nRecIdx, fields, block
                )
                if err:
                    return err

        if requestQuery["cont"]:
            self.com.dynamicCall("RequestNextData(QString)", self.tr)
        else:
            self.com.dynamicCall("RequestData(QString)", self.tr)
        while not self.received:
            pumpWaitingMessages()
        return ""


class Real:
    def __init__(self) -> None:
        self.com: Any = None
        self.meta: dict[str, Any] = {}
        self.keys: set[str] = set()
        self.tr = ""

    def init(self, com: Any, p: Path) -> None:
        self.com = com
        self.com.ReceiveRealData.connect(self.OnReceiveRealData)
        self.meta = parse_res(p)
        self.keys = set()
        self.tr = p.stem

    def OnReceiveRealData(self) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.meta["output"].items():
            fields = v["fields"]
            block[szBlockName] = self.getBlock(fields)
        responseReal = {
            "err": "",
            "tr": self.tr,
            "block": block,
        }
        for OnReceiveRealData in CALLBACK.OnReceiveRealData:
            OnReceiveRealData(responseReal)

    def getBlock(
        self,
        fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        nBlockIdx = 0
        nRecIdx = 0
        nAttrType = 0
        block: dict[str, Any] = {}
        for nFieldIdx, field in enumerate(fields):
            szFieldName = field["name"]
            val = self.com.dynamicCall(
                "GetMultiData(int, int, int, int)",
                nBlockIdx,
                nRecIdx,
                nFieldIdx,
                nAttrType,
            )
            block[szFieldName] = f"{val}"
        return block

    def advise(self, requestReal: dict[str, Any]) -> str:
        key = requestReal["key"]
        if key in self.keys:
            return ""

        self.com.dynamicCall("RequestRealData(QString, QString)", self.tr, key)
        self.keys.add(key)
        return ""

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        key = requestReal["key"]
        if key not in self.keys:
            return ""

        self.com.dynamicCall(
            "UnRequestRealData(QString, QString)", self.tr, key
        )
        self.keys.remove(key)
        return ""


class Meta:
    def __init__(
        self, path: str = "C:/eFriend Expert/efriendexpert/qry"
    ) -> None:
        self.path = Path(path)
        self.QueryDict: dict[str, Query] = {}
        self.RealDict: dict[str, Real] = {}
        self.app: Any = None

    def __enter__(self) -> Any:
        self.app = qApplication()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        pass

    def exists(self, szTrCode: str) -> tuple[bool, Path]:
        p = self.path / f"{szTrCode}.qry"
        return p.exists(), p

    def getQuery(self, szTrCode: str) -> None | Query:
        obj = self.QueryDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = qAxWidget("ITGExpertCtl.ITGExpertCtlCtrl.1")
            obj = Query()
            obj.init(com, p)
            self.QueryDict[szTrCode] = obj
        return obj

    def getReal(self, szTrCode: str) -> None | Real:
        obj = self.RealDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = qAxWidget("ITGExpertCtl.ITGExpertCtlCtrl.1")
            obj = Real()
            obj.init(com, p)
            self.RealDict[szTrCode] = obj
        return obj

    def query(self, requestQuery: dict[str, Any]) -> str:
        """
        requestQuery = {
            "tr": str,
            "block": {},
            "cont": bool,
        }
        responseQuery = {
            "err": str,
            "tr": str,
            "block": {},
        }
        """
        tr = requestQuery["tr"]
        obj = self.getQuery(tr)
        if obj is None:
            return f"FileNotFound, {tr}"
        return obj.query(requestQuery)

    def real(self, requestReal: dict[str, Any]) -> str:
        """
        requestReal = {
            "tr": str,
            "key": str,
            "adv": bool,
        }
        responseReal = {
            "err": str,
            "tr": str,
            "block": {},
        }
        """
        tr = requestReal["tr"]
        obj = self.getReal(tr)
        if obj is None:
            return f"FileNotFound, {tr}"
        if requestReal["adv"]:
            return obj.advise(requestReal)
        return obj.unadvise(requestReal)
