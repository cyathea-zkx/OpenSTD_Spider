from pathlib import Path

from .captcha import fuck_captcha
from .exception import HandleCaptchaError
from .parse.gb688 import gb688_reorganize_page
from .request import Gb688Dto, OpenstdDto
from .schema import Gb688Page
from typing import Callable, Optional


def fuck_captcha_impl(dto: Gb688Dto):
    "识别验证码"
    for cnt in range(10):
        captcha_img = dto.get_captcha()
        captcha_code = fuck_captcha(captcha_img)
        status = dto.submit_captcha(captcha_code)
        if status is True:
            break
    else:
        raise HandleCaptchaError


def download_preview_img_impl(
    dto: Gb688Dto,
    base_dir: Path,
    img_ids: set[str],
    cb: Optional[Callable[[int], None]] = None,
):
    "下载预览图片"
    for idx, img_id in enumerate(img_ids, 1):
        img_data = dto.get_pageimg(img_id)
        img_file_name = img_id.replace("/", "_")
        raw_file = base_dir / f"{img_file_name}.webp"
        raw_file.write_bytes(img_data)
        if cb:
            cb(idx)


def reorganize_page_impl(
    page_infos: list[Gb688Page],
    base_dir: Path,
    cb: Optional[Callable[[int], None]] = None,
):
    "重组页面图片"
    for idx, page_info in enumerate(page_infos, 1):
        img_file_name = page_info.img_id.replace("/", "_")
        raw_file = base_dir / f"{img_file_name}.webp"
        page_file = base_dir / f"P_{page_info.no}.png"
        gb688_reorganize_page(page_info, raw_file, page_file)
        if cb:
            cb(idx)
