从 bs4.element 导入 *
从 汉化通用 导入 _关键词参数中转英, _反向注入

类 〇页面元素(PageElement):
    """包含页面某一部分(即其在解析树中的当前位置)的导航信息.
    〇可导航字符串 / 〇标签 等都是 〇页面元素 的子类.
    """

    套路 设置(分身, 父元素=None, 上一元素=None, 下一元素=None,
            上一兄弟元素=None, 下一兄弟元素=None):
        """设置此元素与其他元素的初始关系"""
        分身.setup(parent=父元素, previous_element=上一元素, next_element=下一元素,
              previous_sibling=上一兄弟元素, next_sibling=下一兄弟元素)

    @property
    套路 父元素(分身):
        返回 分身.parent
    
    @property
    套路 上一元素(分身):
        返回 分身.previous_element
    
    @property
    套路 下一元素(分身):
        返回 分身.next_element
    
    @property
    套路 下一兄弟元素(分身):
        返回 分身.next_sibling

    @property
    套路 上一兄弟元素(分身):
        返回 分身.previous_sibling

    套路 格式化字符串(分身, 字符串, 格式器):
        "用给定格式化器格式化给定字符串."
        返回 分身.format_string(字符串, 格式器)

    套路 名称格式器(分身, 格式器):
        返回 分身.formatter_for_name(格式器)

    @property
    套路 所有经修剪字符串(分身):
        """生成此元素中的所有字符串, 首先去除这些字符串的首尾空白"""
        取 字符串 于 分身._all_strings(真):
            生成 字符串

    套路 获取文本(分身, 分隔符="", 修剪=假, 类型々=PageElement.default):
        """获取此元素的所有子字符串, 使用指定分隔符拼接"""
        返回 分身.get_text(separator=分隔符, strip=修剪, types=类型々)

    文本 = property(获取文本)

    套路 替换为(分身, *替代元素々):
        "用另外的一个或多个元素替代此元素, 树的其余元素保持不变."
        返回 分身.replace_with(*替代元素々)

    套路 解包(分身):
        "用元素的内容替换当前元素. 返回值为此元素, 它不再是树的一部分."
        返回 分身.unwrap()

    套路 包裹(分身, 目标元素):
        "将此元素包裹在目标元素内部."
        返回 分身.wrap(目标元素)

    套路 拔除(分身, 自身索引=空):
        "将此元素从树中拔除. 返回此元素, 它不再是树的一部分."
        返回 分身.extract(自身索引)

    套路 插入(分身, 位置, 新子元素):
        "在此元素的子元素列表中插入一个新元素."
        分身.insert(位置, 新子元素)

    套路 追加(分身, 标签):
        "在此元素的内容列表中追加给定的元素."
        分身.append(标签)

    套路 扩充(分身, 标签々):
        "在此元素的内容列表中追加给定的元素."
        分身.extend(标签々)

    套路 前插(分身, *参数々):
        "让给定元素成为此元素的直接前驱元素"
        分身.insert_before(*参数々)

    套路 后插(分身, *参数々):
        "让给定元素成为此元素的直接后继元素"
        分身.insert_after(*参数々)

    套路 查找下一元素(分身, 名称=空, 属性々={}, 字符串=空, **关键词参数々):
        """查找文档中此元素之后第一个符合给定条件的元素"""
        返回 分身.find_next(name=名称, attrs=属性々, string=字符串, **关键词参数々)

    套路 查找之后所有元素(分身, 名称=None, 属性々={}, 字符串=None, 限值=None, **关键词参数々):
        """查找文档中此元素之后所有符合给定条件的元素"""
        返回 分身.find_all_next(name=名称, attrs=属性々, string=字符串, 
                            limit=限值, **关键词参数々)

    套路 查找下一兄弟元素(分身, 名称=空, 属性々={}, 字符串=空, **关键词参数々):
        """查找文档中此元素之后第一个符合给定条件的兄弟元素"""
        返回 分身.find_next_sibling(name=名称, attrs=属性々, string=字符串, **关键词参数々)

    套路 查找之后所有兄弟元素(分身, 名称=None, 属性々={}, 字符串=None, 限值=None, **关键词参数々):
        """查找文档中此元素之后所有符合给定条件的兄弟元素"""
        返回 分身.find_next_siblings(name=名称, attrs=属性々, string=字符串, 
                            limit=限值, **关键词参数々)
    
    套路 查找上一元素(分身, 名称=空, 属性々={}, 字符串=空, **关键词参数々):
        """查找文档中此元素之前第一个符合给定条件的元素"""
        返回 分身.find_previous(name=名称, attrs=属性々, string=字符串, **关键词参数々)

    套路 查找之前所有元素(分身, 名称=None, 属性々={}, 字符串=None, 限值=None, **关键词参数々):
        """查找文档中此元素之前所有符合给定条件的元素"""
        返回 分身.find_all_previous(name=名称, attrs=属性々, string=字符串, 
                            limit=限值, **关键词参数々)

    套路 查找上一兄弟元素(分身, 名称=空, 属性々={}, 字符串=空, **关键词参数々):
        """查找文档中此元素之前第一个符合给定条件的兄弟元素"""
        返回 分身.find_previous_sibling(name=名称, attrs=属性々, string=字符串, **关键词参数々)

    套路 查找之前所有兄弟元素(分身, 名称=None, 属性々={}, 字符串=None, 限值=None, **关键词参数々):
        """查找文档中此元素之前所有符合给定条件的兄弟元素"""
        返回 分身.find_previous_siblings(name=名称, attrs=属性々, string=字符串, 
                            limit=限值, **关键词参数々)

    套路 查找父元素(分身, 名称=None, 属性々={}, **关键词参数々):
        """查找此元素的最近的符合给定条件的父元素"""
        返回 分身.find_parent(name=名称, attrs=属性々, **关键词参数々)
    
    套路 查找所有父元素(分身, 名称=None, 属性々={}, 限值=空, **关键词参数々):
        """查找此元素的所有符合给定条件的父元素"""
        返回 分身.find_parents(name=名称, attrs=属性々, limit=限值, **关键词参数々)

    @property
    def 之后所有元素(self):
        """All PageElements that were parsed after this one.

        :yield: A sequence of PageElements.
        """
        i = self.next_element
        while i is not None:
            yield i
            i = i.next_element

    @property
    def 之后所有兄弟元素(self):
        """All PageElements that are siblings of this one but were parsed
        later.

        :yield: A sequence of PageElements.
        """
        i = self.next_sibling
        while i is not None:
            yield i
            i = i.next_sibling

    @property
    def 之前所有元素(self):
        """All PageElements that were parsed before this one.

        :yield: A sequence of PageElements.
        """
        i = self.previous_element
        while i is not None:
            yield i
            i = i.previous_element

    @property
    def 之前所有兄弟元素(self):
        """All PageElements that are siblings of this one but were parsed
        earlier.

        :yield: A sequence of PageElements.
        """
        i = self.previous_sibling
        while i is not None:
            yield i
            i = i.previous_sibling

    @property
    def 所有父元素(self):
        """All PageElements that are parents of this PageElement.

        :yield: A sequence of PageElements.
        """
        i = self.parent
        while i is not None:
            yield i
            i = i.parent

    @property
    def 已销毁(self):
        """Check whether a PageElement has been decomposed.

        :rtype: bool
        """
        return getattr(self, '_decomposed', False) or False

_反向注入(〇页面元素, PageElement)


类 〇可导航字符串(NavigableString):
    """例如, 当解析标记文本 <粗体>静夜思</粗体> 时, 蜘蛛网会为字符串 '静夜思'
    创建一个可导航字符串对象.
    """

    套路 输出就绪(分身, 格式器="minimal"):
        返回 分身.output_ready(格式器)

    @property
    套路 名称(分身):
        返回 空

    @名称.setter
    套路 名称(分身, 名称):
        报 爻属性错误('不能给可导航字符串指定名称.')

    @property
    套路 所有字符串(分身):
        返回 分身.strings

_反向注入(〇可导航字符串, NavigableString)


〇注释 = Comment


类 〇标签(Tag):
    """表示一个 HTML 或 XML 标签(它是解析树的一部分)及其属性和内容.
    """

    套路 __init__(分身, 解析器=空, 构建器=空, 名称=空, 名称空间=空,
                前缀=空, 属性々=空, 父元素=空, 上一元素=空,
                是xml=空, 源行=空, 源位置=空, 可为空元素=空, 
                CDATA属性々=空, 保留空格的标志々=空,
                相关字符串类型々=空, 名称空间々=空):
        """解析器: 一个蜘蛛网对象

        构建器: 解析树构建器

        名称: 标签的名称

        """
        super().__init__(parser=解析器, builder=构建器, name=名称, namespace=名称空间,
                 prefix=前缀, attrs=属性々, parent=父元素, previous=上一元素,
                 is_xml=是xml, sourceline=源行, sourcepos=源位置,
                 can_be_empty_element=可为空元素, cdata_list_attributes=CDATA属性々,
                 preserve_whitespace_tags=保留空格的标志々,
                 interesting_string_types=相关字符串类型々, namespaces=名称空间々)
        # 分身.属性々 = 分身.attrs
        # 分身.内容々 = 分身.contents

    @property
    套路 名称(分身):
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 解析器类(分身):
        返回 分身.parser_class
    
    @property
    套路 名称空间(分身):
        返回 分身.namespace
    
    @property
    套路 前缀(分身):
        返回 分身.prefix

    @property
    套路 源行(分身):
        返回 分身.sourceline

    @property
    套路 源位置(分身):
        返回 分身.sourcepos

    @property
    套路 已知xml(分身):
        返回 分身.known_xml

    @property
    套路 属性々(分身):
        返回 分身.attrs

    @property
    套路 内容々(分身):
        返回 分身.contents
    
    @property
    套路 隐藏(分身):
        返回 分身.hidden

    @property
    套路 可为空元素(分身):
        返回 分身.can_be_empty_element

    @property
    套路 CDATA属性々(分身):
        返回 分身.cdata_list_attributes

    @property
    套路 保留空格的标志々(分身):
        返回 分身.preserve_whitespace_tags
    
    @property
    套路 是空元素(分身):
        返回 分身.is_empty_element

    @property
    套路 字符串(分身):
        返回 分身.string

    @字符串.setter
    套路 字符串(分身, 字符串):
        分身.clear()
        分身.append(字符串.__class__(字符串))

    @property
    套路 所有字符串(分身):
        返回 分身.strings

    套路 销毁(分身):
        "递归销毁当前元素及其所有子节点"
        分身.decompose()

    套路 清空(分身, 销毁=假):
        "清除当前元素的所有子节点"
        分身.clear(销毁)

    套路 平整(分身):
        "整合连续的字符串, 让美化输出更自然."
        分身.smooth()

    套路 索引(分身, 元素):
        "根据标识 (而非值) 查找子节点的索引"
        返回 分身.index(元素)

    套路 获取(分身, 键, 默认值=空):
        "同字典的 '获取' 方法."
        返回 分身.get(键, default=默认值)

    套路 获取属性列表(分身, 键, 默认值=空):
        "同 '获取()', 但返回一个列表, 无论属性是不是多值属性"
        返回 分身.get_attribute_list(键, default=默认值)

    套路 具有属性(分身, 键):
        "判断当前元素是否有给定名称的属性"
        返回 分身.has_attr(键)

    套路 编码(分身, 编码="utf-8", 缩进水平=None, 格式器="minimal",
            错误处理="xmlcharrefreplace"):
        返回 分身.encode(encoding=编码, indent_level=缩进水平,
                        formatter=格式器, errors=错误处理)

    套路 解码(分身, 缩进水平=None, 最终编码="utf-8", 格式器="minimal"):
        返回 分身.decode(indent_level=缩进水平, eventual_encoding=最终编码,
                        formatter=格式器)

    套路 美化(分身, 编码=空, 格式器="minimal"):
        "将当前元素作为字符串美化输出."
        返回 分身.prettify(encoding=编码, formatter=格式器)

    套路 解码内容(分身, 缩进水平=空, 最终编码="utf-8", 格式器="minimal"):
        返回 分身.decode_contents(indent_level=缩进水平, eventual_encoding=最终编码,
                        formatter=格式器)

    套路 编码内容(分身, 缩进水平=空, 编码="utf-8", 格式器="minimal"):
        返回 分身.encode_contents(indent_level=缩进水平, encoding=编码,
                        formatter=格式器)

    套路 查找(分身, 名称=None, 属性々={}, 递归=真, 字符串=None, **关键词参数々):
        "在当前元素的所有子节点中查找第一个符合条件的元素."
        返回 分身.find(name=名称, attrs=属性々, recursive=递归,
                        text=字符串, **关键词参数々)

    套路 查找全部(分身, 名称=None, 属性々={}, 递归=真, 字符串=None, 限值=None, **关键词参数々):
        "在当前元素的所有子节点中查找所有符合条件的元素."
        返回 分身.find_all(name=名称, attrs=属性々, recursive=递归,
                        text=字符串, limit=限值, **关键词参数々)

    @property
    套路 所有子元素(分身):
        返回 iter(分身.contents)  # 可行？
    
    @property
    套路 所有子孙元素(self):
        if not len(self.contents):
            return
        stopNode = self._last_descendant().next_element
        current = self.contents[0]
        while current is not stopNode:
            yield current
            current = current.next_element

    套路 选一个(分身, 选择器, 名称空间々=空, **关键词参数々):
        "对当前元素执行 CSS 选择操作."
        返回 分身.select_one(选择器, namespaces=名称空间々, **关键词参数々)

    套路 选择(分身, 选择器, 名称空间々=空, 限值=空, **关键词参数々):
        "对当前元素执行 CSS 选择操作."
        返回 分身.select(选择器, namespaces=名称空间々, limit=限值, **关键词参数々)

_反向注入(〇标签, Tag)


类 〇树过滤器(SoupStrainer):

    套路 搜索标签(分身, 标记名称=空, 标记属性々={}):
        返回 分身.search_tag(markup_name=标记名称, markup_attrs=标记属性々)

    套路 搜索(分身, 标记文本):
        返回 分身.search(标记文本)

_反向注入(〇树过滤器, SoupStrainer)
