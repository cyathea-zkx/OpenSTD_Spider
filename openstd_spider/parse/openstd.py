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
        try:
            # 提取状态元素
            status_element = row.select_one("td:nth-of-type(6)>span")
            
            # 如果状态元素存在并且有非空内容
            if status_element and status_element.string and status_element.string.strip():
                status = StdStatus(name2std_status(status_element.string.strip()))
            else:
                # 使用默认值
                status = StdStatus.PUBLISHED  # 或者设置为其他合适的默认值
            
            # 尝试获取日期，提供默认值
            try:
                pub_date = date.fromisoformat(row.select_one("td:nth-of-type(7)").string.strip())
            except (AttributeError, ValueError):
                pub_date = date(1900, 1, 1)  # 使用明显的默认日期
                
            try:
                impl_date = date.fromisoformat(row.select_one("td:nth-of-type(8)").string.strip())
            except (AttributeError, ValueError):
                impl_date = date(1900, 1, 1)  # 使用明显的默认日期
            
            # 创建项目并添加到列表
            items.append(
                StdListItem(
                    id=row.select_one("td:nth-of-type(2)>a")["onclick"][10:-3],
                    std_code=row.select_one("td:nth-of-type(2)>a").string.strip(),
                    is_ref=row.select_one("td:nth-of-type(3)>span") is not None,
                    name_cn=row.select_one("td:nth-of-type(4)>a").string.strip(),
                    status=status,
                    pub_date=pub_date,
                    impl_date=impl_date,
                )
            )
        except Exception as e:
            # 记录错误但继续处理其他行
            import sys
            print(f"警告: 解析行时出错: {e}", file=sys.stderr)
            continue
            
    # 获取分页信息，添加错误处理
    try:
        tag = html.select_one("div.hidden-xs>table>tr>td:nth-of-type(1)>span")
        tag2 = list(tag.strings)
        total_item = int(tag2[8].strip())
        page = int(tag2[11].strip())
        total_page = int(tag2[12][3:].strip())
    except (AttributeError, IndexError, ValueError) as e:
        # 分页信息解析失败时使用默认值
        import sys
        print(f"警告: 解析分页信息时出错: {e}", file=sys.stderr)
        total_item = len(items)
        page = 1
        total_page = 1
    
    return StdSearchResult(
        items=items,
        total_item=total_item,
        page=page,
        total_page=total_page,
    )
