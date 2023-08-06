from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable

from w32py.win import (
    coInitialize,
    coUninitialize,
    dispatch,
    pumpWaitingMessages,
    withEvents,
)


class CALLBACK:
    OnLogin: list[Callable[[str, str], None]] = []
    OnDisconnect: list[Callable[[], None]] = []
    OnReceiveData: list[Callable[[dict[str, Any]], None]] = []
    OnReceiveRealData: list[Callable[[dict[str, Any]], None]] = []


class SESSION_STATUS(Enum):
    DISCONNECT = auto()
    LOGIN_SUCCEEDED = auto()
    LOGIN_FAILED = auto()


class Session:
    def __init__(self) -> None:
        self.com: Any = None
        self.status = SESSION_STATUS.DISCONNECT

    def init(self, com: Any) -> None:
        self.com = com
        self.status = SESSION_STATUS.DISCONNECT

    def OnLogin(self, szCode: str, szMsg: str) -> None:
        if szCode == "0000":
            self.status = SESSION_STATUS.LOGIN_SUCCEEDED
        else:
            self.status = SESSION_STATUS.LOGIN_FAILED
        for OnLogin in CALLBACK.OnLogin:
            OnLogin(szCode, szMsg)

    def OnLogout(self) -> None:
        self.disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()

    def OnDisconnect(self) -> None:
        self.disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()

    def disconnect(self) -> None:
        self.com.DisconnectServer()
        self.status = SESSION_STATUS.DISCONNECT

    def lastError(self, prefix: str) -> str:
        nErrCode = self.com.GetLastError()
        strErrMsg = self.com.GetErrorMessage(nErrCode)
        return f"{prefix}, {nErrCode}, {strErrMsg}"

    def login(
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        nServerType: int,
        szServerIP: str,
        nServerPort: int,
    ) -> str:
        self.disconnect()
        if not self.com.ConnectServer(szServerIP, nServerPort):
            return self.lastError("ConnectServer")
        if not self.com.Login(szID, szPwd, szCertPwd, nServerType, False):
            return self.lastError("Login")

        while self.status == SESSION_STATUS.DISCONNECT:
            pumpWaitingMessages()

        if self.status == SESSION_STATUS.LOGIN_SUCCEEDED:
            return ""
        return "LOGIN_FAILED"


def parse_field(line: str) -> dict[str, Any]:
    cols = [s.strip() for s in line.split(",")]
    return {
        "name": cols[1],
        "desc": cols[0],
        "type": cols[3],
        "size": cols[4],
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
        if line.startswith(".Func,") or line.startswith(".Feed,"):
            parsed["desc"] = line.split(",")[1].strip()
        elif line == "begin":
            latest_begin = i
        elif line == "end":
            block_info = [
                s.strip() for s in lines[latest_begin - 1].split(",")
            ]
            parsed[block_info[2]][block_info[0]] = {
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
        self.com.ResFileName = f"{p}"
        self.meta = parse_res(p)
        self.received = False
        self.tr = p.stem

    def OnReceiveData(self, _szTrCode: str) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.meta["output"].items():
            fields = v["fields"]
            if v["occurs"]:
                block[szBlockName] = [
                    self.getBlock(szBlockName, nRecIdx, fields)
                    for nRecIdx in range(self.com.GetBlockCount(szBlockName))
                ]
            else:
                nRecIdx = 0
                block[szBlockName] = self.getBlock(
                    szBlockName, nRecIdx, fields
                )
        responseQuery = {
            "err": "",
            "tr": self.tr,
            "block": block,
        }
        self.received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def OnReceiveMessage(
        self, bIsSystemError: int, nMessageCode: str, szMessage: str
    ) -> None:
        if bIsSystemError == 0 and nMessageCode[0] == "0":
            return

        responseQuery = {
            "err": f"{bIsSystemError}, {nMessageCode}, {szMessage}",
            "tr": self.tr,
            "block": {},
        }
        self.received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def getBlock(
        self,
        szBlockName: str,
        nRecIdx: int,
        fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        block: dict[str, Any] = {}
        for field in fields:
            szFieldName = field["name"]
            val = self.com.GetFieldData(szBlockName, szFieldName, nRecIdx)
            block[szFieldName] = f"{val}"
        return block

    def setBlock(
        self,
        szBlockName: str,
        nRecIdx: int,
        fields: list[dict[str, Any]],
        block: dict[str, Any],
    ) -> str:
        for field in fields:
            szFieldName = field["name"]
            val = block.get(szFieldName)
            if val is None:
                return (
                    f"InvalidField, {szBlockName}"
                    f", {nRecIdx}, {szFieldName}"
                )
            self.com.SetFieldData(szBlockName, szFieldName, nRecIdx, f"{val}")
        return ""

    def query(self, requestQuery: dict[str, Any]) -> str:
        requestBlock = requestQuery["block"]
        for szBlockName, v in self.meta["input"].items():
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
                    err = self.setBlock(szBlockName, nRecIdx, fields, block)
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
                err = self.setBlock(szBlockName, nRecIdx, fields, block)
                if err:
                    return err

        nErrCode = self.com.Request(requestQuery["cont"])
        if nErrCode < 0:
            strErrMsg = self.com.GetErrorMessage(nErrCode)
            return f"Request, {nErrCode}, {strErrMsg}"

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
        self.com.ResFileName = f"{p}"
        self.meta = parse_res(p)
        self.keys = set()
        self.tr = p.stem

    def OnReceiveRealData(self, _szTrCode: str) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.meta["output"].items():
            fields = v["fields"]
            block[szBlockName] = self.getBlock(szBlockName, fields)
        responseReal = {
            "err": "",
            "tr": self.tr,
            "block": block,
        }
        for OnReceiveRealData in CALLBACK.OnReceiveRealData:
            OnReceiveRealData(responseReal)

    def getBlock(
        self,
        szBlockName: str,
        fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        block: dict[str, Any] = {}
        for field in fields:
            szFieldName = field["name"]
            val = self.com.GetFieldData(szBlockName, szFieldName)
            block[szFieldName] = f"{val}"
        return block

    def advise(self, requestReal: dict[str, Any]) -> str:
        key = requestReal["key"]
        if key in self.keys:
            return ""

        if key:
            self.com.SetFieldData(
                "InBlock",
                self.meta["input"]["InBlock"]["fields"][0]["name"],
                key,
            )
        self.com.AdviseRealData()
        self.keys.add(key)
        return ""

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        key = requestReal["key"]
        if key not in self.keys:
            return ""

        if key:
            self.com.UnadviseRealDataWithKey(key)
        else:
            self.com.UnadviseRealData()
        self.keys.remove(key)
        return ""


class Meta:
    def __init__(self, path: str = "C:/eBEST/xingAPI/Res") -> None:
        self.path = Path(path)
        self.Session: None | Session = None
        self.QueryDict: dict[str, Query] = {}
        self.RealDict: dict[str, Real] = {}

    def __enter__(self) -> Any:
        coInitialize()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        obj = self.getSession()
        obj.disconnect()
        coUninitialize()

    def exists(self, szTrCode: str) -> tuple[bool, Path]:
        p = self.path / f"{szTrCode}.res"
        return p.exists(), p

    def getSession(self) -> Session:
        if self.Session is None:
            com = dispatch("XA_Session.XASession")
            obj = withEvents(com, Session)
            obj.init(com)
            self.Session = obj
        return self.Session

    def getQuery(self, szTrCode: str) -> None | Query:
        obj = self.QueryDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = dispatch("XA_DataSet.XAQuery")
            obj = withEvents(com, Query)
            obj.init(com, p)
            self.QueryDict[szTrCode] = obj
        return obj

    def getReal(self, szTrCode: str) -> None | Real:
        obj = self.RealDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = dispatch("XA_DataSet.XAReal")
            obj = withEvents(com, Real)
            obj.init(com, p)
            self.RealDict[szTrCode] = obj
        return obj

    def login(
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        nServerType: int = 0,
        szServerIP: str = "hts.ebestsec.co.kr",
        nServerPort: int = 20001,
    ) -> str:
        obj = self.getSession()
        return obj.login(
            szID, szPwd, szCertPwd, nServerType, szServerIP, nServerPort
        )

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
