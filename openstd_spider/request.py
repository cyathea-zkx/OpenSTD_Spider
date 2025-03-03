import random
import time
from typing import IO, Callable, Optional

from httpx import Client

from openstd_spider.schema import StdSearchResult

from .exception import DownloadError
from .parse.gb688 import gb688_parse_page_sheet
from .parse.openstd import openstd_parse_meta, openstd_parse_search_result
from .schema import Gb688Page, StdMeta, StdStatus, StdType

BASE_URL_OPENSTD = "https://openstd.samr.gov.cn/bzgk/gb/"
BASE_URL_GB688 = "http://c.gb688.cn/bzgk/gb/"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"


class OpenstdDto:
    def __init__(self):
        self.client = Client(
            headers={
                "User-Agent": UA,
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            },
            base_url=BASE_URL_OPENSTD,
            follow_redirects=False,
        )

    def get_std_meta(self, std_id: str) -> StdMeta:
        resp = self.client.get(
            "/newGbInfo",
            params={
                "hcno": std_id,
            },
        )
        resp.raise_for_status()
        return openstd_parse_meta(resp.text)

    def search(
        self,
        keyword: str = "",
        std_status: StdStatus = StdStatus.ALL,
        std_type: StdType = StdType.ALL,
        cate="",
        date="",
        ps: int = 10,
        pn: int = 1,
        order_by: str = "",
        order: str = "",
    ) -> StdSearchResult:
        resp = self.client.get(
            "/std_list",
            params={
                "r": random.random(),
                "page": pn,
                "pageSize": ps,
                "p.p1": std_type.value,  # 分类
                "p.p2": keyword,  # 关键字
                "p.p5": std_status.value,  # 状态
                "p.p6": cate,  # 分类
                "p.p7": date,  # 时间
                "p.p90": order_by,  # 排序依据
                "p.p91": order,  # 排序
            },
        )
        resp.raise_for_status()
        return openstd_parse_search_result(resp.text)


class Gb688Dto:
    def __init__(self):
        self.client = Client(
            headers={
                "User-Agent": UA,
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            },
            base_url=BASE_URL_GB688,
            follow_redirects=False,
        )

    def get_pages(self, std_id: str) -> list[Gb688Page]:
        """获取文档页"""
        resp = self.client.get(
            "/showGb",
            params={
                "type": "online",
                "hcno": std_id,
            },
            headers={
                "Referer": f"https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={std_id}"
            },
        )
        resp.raise_for_status()
        return gb688_parse_page_sheet(resp.text)

    def get_pageimg(self, img_id: str):
        """获取页面图片"""
        resp = self.client.get(
            "/viewGbImg",
            params={
                "fileName": img_id,
            },
            headers={
                "Cache-Alive": "chunked",
            },
            follow_redirects=True,
        )
        resp.raise_for_status()
        return resp.content

    def download_pdf(
        self,
        std_id: str,
        fp: IO,
        cb: Optional[Callable[[int, int], None]] = None,
    ):
        """下载pdf文件"""
        with self.client.stream(
            "GET",
            "/viewGb",
            params={
                "hcno": std_id,
            },
        ) as resp:
            resp.raise_for_status()
            total_size = int(resp.headers.get("Content-Length", 0))
            if (
                not resp.headers.get("Content-Disposition", "").endswith(".pdf")
                and total_size != 0
            ):
                # 文件不为pdf
                raise DownloadError
            size = 0
            for chunck in resp.iter_bytes(1024 * 100):
                size += len(chunck)
                fp.write(chunck)
                if cb:
                    cb(total_size, size)

    def get_captcha(self):
        """获取人机验证码"""
        resp = self.client.get(f"/gc?_{int(time.time() * 1000)}")
        resp.raise_for_status()
        return resp.content

    def submit_captcha(self, code: str) -> bool:
        """提交人机验证码"""
        resp = self.client.post(
            "/verifyCode",
            data={
                "verifyCode": code,
            },
        )
        resp.raise_for_status()
        return resp.text == "success"
