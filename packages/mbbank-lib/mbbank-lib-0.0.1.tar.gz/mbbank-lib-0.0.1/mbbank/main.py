from PIL import Image
import pytesseract
import re
import datetime
import base64
import hashlib
import typing
import io
import platform
import aiohttp

headers_default = {
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Basic RU1CUkVUQUlMV0VCOlNEMjM0ZGZnMzQlI0BGR0AzNHNmc2RmNDU4NDNm',
    'User-Agent': f'Mozilla/5.0 (X11; {platform.system()} {platform.processor()})',
    "Origin": "https://online.mbbank.com.vn",
    "Referer": "https://online.mbbank.com.vn/"
}


def get_now_time():
    now = datetime.datetime.now()
    microsecond = int(now.strftime("%f")[:2])
    return now.strftime(f"%Y%m%d%H%M{microsecond }")


class MBBank:
    
    deviceIdCommon = f'yeumtmdx-mbib-0000-0000-{get_now_time()}'
    
    def __init__(self, *, username, password, tesseract_path=None):
        self.userid = username
        self.password = password
        if tesseract_path is not None:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.sessionId = None
        self._userinfo = None
        self._temp = {}
        
    
    async def _req(self, url, *, json={}, headers={}):
        while True:
            rid = f"{self.userid}-{get_now_time()}"
            json_data = {
                'sessionId': self.sessionId if self.sessionId is not None else "",
                'refNo': rid,
                'deviceIdCommon': self.deviceIdCommon,
            }
            json_data.update(json)
            headers.update(headers_default)
            headers["X-Request-Id"] = rid
            async with aiohttp.ClientSession() as s:
                async with s.post(url, headers=headers, json=json_data) as r:
                    data_out = await r.json()
            if data_out["result"] is None:
                  await self.getBalance()
            elif data_out["result"]["ok"]:
                data_out.pop("result", None)
                data_out.pop("refNo", None)
                break
            elif data_out["result"]["responseCode"] == "GW200":
                await self.authenticate()
            else:
                err_out = data_out["result"]
                raise Exception(f"{err_out['responseCode']} | {err_out['message']}")
        return data_out
    
    async def authenticate(self):
        while True:
            self._userinfo = None
            self.sessionId = None
            self._temp = {}
            data_out = await self._req("https://online.mbbank.com.vn/retail-web-internetbankingms/getCaptchaImage")
            imgbyte = io.BytesIO(base64.b64decode(data_out["imageString"]))
            img = Image.open(imgbyte)
            img = img.convert('RGBA')
            pix = img.load()
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                        pix[x, y] = (0, 0, 0, 255)
                    else:
                        pix[x, y] = (255, 255, 255, 255)
            text = pytesseract.image_to_string(img)
            text = re.sub(r"\s+", "", text, flags=re.MULTILINE)
            payload = {
                "userId": self.userid,
                "password": hashlib.md5(self.password.encode()).hexdigest(),
                "captcha": text,
                'sessionId': "",
                'refNo': f'{self.userid}-{get_now_time()}',
                'deviceIdCommon': self.deviceIdCommon,
            }

            async with aiohttp.ClientSession() as s:
                async with s.post("https://online.mbbank.com.vn/retail_web/internetbanking/doLogin", headers=headers_default, json=payload) as r:
                    data_out = await r.json()
                    
            if data_out["result"]["ok"]:
                self.sessionId = data_out["sessionId"]
                self._userinfo = data_out
                return
            elif data_out["result"]["responseCode"] == "GW283":
                pass
            else:
                err_out = data_out["result"]
                raise Exception(f"{err_out['responseCode']} | {err_out['message']}")

    async def getTransactionAccountHistory(self, *, from_date: datetime.datetime, to_date: datetime.datetime):
        json_data = {
            'accountNo': self.userid,
            'fromDate': from_date.strftime("%d/%m/%Y"),
            'toDate': to_date.strftime("%d/%m/%Y"), # max 3 months
        }

        data_out = await self._req("https://online.mbbank.com.vn/retail-web-transactionservice/transaction/getTransactionAccountHistory", json=json_data)
        return data_out

    async def getBalance(self):
        data_out = await self._req("https://online.mbbank.com.vn/api/retail-web-accountms/getBalance")
        return data_out
    
    async def getBalanceLoyalty(self):
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/loyalty/getBalanceLoyalty")
        return data_out
    
    async def getInterestRate(self, currency:str ="VND"):
        json_data = {
            "productCode": "TIENGUI.KHN.EMB",
            "currency": currency,
        }
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/saving/getInterestRate", json=json_data)
        return data_out
    
    async def getFavorBeneficiaryList(self, *, transactionType: typing.Literal["TRANSFER", "PAYMENT"], searchType: typing.Literal["MOST", "LATEST"]):
        json_data = {
            "transactionType": transactionType,
            "searchType": searchType
        }
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/internetbanking/getFavorBeneficiaryList", json=json_data)
        return data_out
    
    async def getCardList(self):
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/card/getList")
        return data_out
    
    async def getSavingList(self):
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/saving/getList")
        return data_out
    
    async def getLoanList(self):
        data_out = await self._req("https://online.mbbank.com.vn/api/retail_web/loan/getList")
        return data_out
    
    async def userinfo(self):
        if self._userinfo is None:
            await self.authenticate()
        else:
            await self.getBalance()
        return self._userinfo