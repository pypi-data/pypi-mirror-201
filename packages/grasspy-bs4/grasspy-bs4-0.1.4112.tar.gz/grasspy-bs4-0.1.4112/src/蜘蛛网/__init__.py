"""可以从HTML或XML文件中提取数据的库. 

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#

此库的官网有很棒的中文文档.
"""

__all__ = ['〇蜘蛛网']

从 bs4 导入 BeautifulSoup
从 汉化通用 导入 _关键词参数中转英, _反向注入
从 .元素 导入 (
    〇注释,
    〇可导航字符串,
    〇页面元素,
    〇标签
)

BeautifulSoup.NO_PARSER_SPECIFIED_WARNING = "未明确指定解析器, 故将使用此系统提供的最佳 %(markup_type)s 解析器 (\"%(parser)s\"). 这通常不是问题, 但如果你在另一个系统或其他虚拟环境中遇到此提示, 可能是因为它使用不同的解析器, 工作方式有所不同.\n\n引发此警告的代码位于第 %(line_number)s 行, 文件是 %(filename)s. 要消除此警告, 请向蜘蛛网构造函数传递额外的参数 '特性=\"%(parser)s\"'.\n"

类 〇蜘蛛网(BeautifulSoup):
    """代表一个已解析 HTML 或 XML 文档的数据结构."""
    套路 __init__(分身, 标记文本="", 特性=空, 构建器=空, 部分解析=空, 源编码=空, 排除编码々=空,
                 元素类々=空, **关键词参数):
        关键词字典 ={
            '多值属性々' : 'multi_valued_attributes',
            '保留空格的标志々' : 'preserve_whitespace_tags',
            '存储行号' : 'store_line_numbers',
            '字符串容器' : 'string_containers'
        }

        关键词参数 = _关键词参数中转英(关键词参数, 关键词字典)

        super().__init__(markup=标记文本, features=特性, builder=构建器, 
                parse_only=部分解析, from_encoding=源编码, exclude_encodings=排除编码々,
                element_classes=元素类々, **关键词参数)

    套路 重置(分身):
        """将此对象重置为好像从未解析任何标记文本的状态"""
        分身.reset()

    套路 新标签(分身, 名称, 名称空间=空, 名称空间前缀=空, 属性々={}, 源行=空, 源位置=空, **关键词属性):
        """创建一个与此对象相关联的新标签."""
        返回 分身.new_tag(名称, namespace=名称空间, nsprefix=名称空间前缀, attrs=属性々,
                sourceline=源行, sourcepos=源位置, **关键词属性)

    套路 新字符串(分身, 字符串, 子类=空):
        """创建一个与此对象相关联的新可导航字符串对象."""
        返回 分身.new_string(字符串, subclass=子类)

    套路 解码(分身, 美化打印=假, 最终编码='utf-8', 格式器="minimal"):
        """以 HTML 或 XML 文档返回解析树的字符串或 Unicode 表示."""
        返回 分身.decode(pretty_print=美化打印, eventual_encoding=最终编码, 
                        formatter=格式器)

_反向注入(〇蜘蛛网, BeautifulSoup)
