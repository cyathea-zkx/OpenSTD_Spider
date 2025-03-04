from datetime import date

from bs4 import BeautifulSoup

from ..exception import NotFoundError
from ..schema import StdListItem, StdMetaFull, StdSearchResult, StdStatus
from ..utils import name2std_status


def openstd_parse_meta(html_text: str) -> StdMetaFull:
    html = BeautifulSoup(html_text, "lxml")
    tag1 = html.select_one("div.bor2")
    tag2 = tag1.select_one("table.tdlist")
    tag3 = tag1.select("div.content")

    std_code = list(tag1.select_one("table.mk1 tr td h1").strings)
    if std_code[0].startswith("您所查询的标准系统尚未收录"):
        raise NotFoundError
    is_ref = std_code[-1] == "采"
    _, std_code = std_code[0].split("标准号：")
    std_code = std_code.strip()

    return StdMetaFull(
        std_code=std_code,
        is_ref=is_ref,
        name_cn=tag2.select_one("tr:nth-of-type(1) td:nth-of-type(1) b").string,
        name_en=tag2.select_one("tr:nth-of-type(2) td:nth-of-type(1)").string.split(
            "英文标准名称："
        )[1],
        status=StdStatus(
            name2std_status(tag2.select_one("tr:nth-of-type(3) td span").string.strip())
        ),
        allow_preview=tag2.select_one("tr:nth-of-type(4) button.ck_btn") is not None,
        allow_download=tag2.select_one("tr:nth-of-type(4) button.xz_btn") is not None,
        pub_date=date.fromisoformat(tag3[2].string.strip()),
        impl_date=date.fromisoformat(tag3[3].string.strip()),
        ccs=tag3[0].string.strip(),
        ics=tag3[1].string.strip(),
        maintenance_depat=tag3[4].string.strip(),
        centralized_depat=tag3[5].string.strip(),
        pub_depat=tag3[6].string.strip(),
        comment=tag3[7].string.strip(),
    )


def openstd_parse_search_result(html_text: str) -> StdSearchResult:
    items = []
    html = BeautifulSoup(html_text, "lxml")
    table = html.select("table.result_list>tbody:nth-of-type(2)>tr")
    for row in table:
        items.append(
            StdListItem(
                id=row.select_one("td:nth-of-type(2)>a")["onclick"][10:-3],
                std_code=row.select_one("td:nth-of-type(2)>a").string.strip(),
                is_ref=row.select_one("td:nth-of-type(3)>span") is not None,
                name_cn=row.select_one("td:nth-of-type(4)>a").string.strip(),
                status=StdStatus(
                    name2std_status(
                        row.select_one("td:nth-of-type(6)>span").string.strip()
                    )
                ),
                pub_date=date.fromisoformat(
                    row.select_one("td:nth-of-type(7)").string.strip()
                ),
                impl_date=date.fromisoformat(
                    row.select_one("td:nth-of-type(8)").string.strip()
                ),
            )
        )
    tag = html.select_one("div.hidden-xs>table>tr>td:nth-of-type(1)>span")
    tag2 = list(tag.strings)

    return StdSearchResult(
        items=items,
        total_item=int(tag2[8].strip()),
        page=int(tag2[11].strip()),
        total_page=int(tag2[12][3:].strip()),
    )
