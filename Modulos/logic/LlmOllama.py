from typing import ByteString
import requests
from pathlib import Path
from datetime import datetime
from Modulos.Func.valOllama import getListLLM as getLiLlm
class ModelOllama:
    def __init__(self, url:ByteString, context:ByteString, typeCon:ByteString, modelOllama:ByteString):
        self.__url = url
        self.__modelOllama = modelOllama
        print(self.__modelOllama)
        self.context = context
        self.type = typeCon
        self.__res:ByteString
        self.proceOllama()
        return
    def proceOllama(self):
        self.ollamaRequ() if self.type == 'request' else self.ollamaLib()
        return
    def ollamaRequ(self):
        data = {
                "model": self.__modelOllama,
                "prompt": self.context,
                "stream": False
                }

        r = requests.post(self.__url, json=data)
        self.__res = r.json()["response"]
        return
    def ollamaLib(self):
        return
    def promtContext(self):
        return
    def wrArchi(self, dir):
        lv_carpeta = dir / "logs" / datetime.now().strftime("%Y%m%d")
        lv_archivo = lv_carpeta / "ai_summary.md"
        lv_carpeta.mkdir(parents=True, exist_ok=True)
        lv_content = "AI Summary\n" + self.__res

        with lv_archivo.open("a", encoding="utf-8") as f:
            f.write(lv_content + "\n")
        return
    def getResp(self):
        return self.__res
    
    def getListLLM(self):
        lv_response = getLiLlm()
        return lv_response