from typing import Any, Optional
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Account:
    short_name: str
    author_name: str
    author_url: str
    access_token: Optional[str] = None
    auth_url: Optional[str] = None
    page_count: Optional[str] = None

@dataclass
class NodeElement():
    '''
    This object represents a DOM element node.

    Attributes:
        tag (str): Name of the DOM element.  
            Allowed values: ``"a"``, ``"aside"``, ``"b"``, ``"blockquote"``, ``"br"``,  
            ``"code"``, ``"em"``, ``"figcaption"``, ``"figure"``, ``"h3"``, ``"h4"``,  
            ``"hr"``, ``"i"``, ``"iframe"``, ``"img"``, ``"li"``, ``"ol"``, ``"p"``,  
            ``"pre"``, ``"s"``, ``"strong"``, ``"u"``, ``"ul"``, ``"video"``.
        attrs (Dict[str, str] | None): Optional HTML attributes.  
            Allowed keys: ``"href"``, ``"src"``.  
            Example: ``{"href": "https://example.com"}``.
        children (List[Union[str, NodeElement]] | None): Optional list of child nodes.  
            Each child is either a plain text string or another ``NodeElement``.  
            Example: ``["Hello, ", NodeElement(tag="b", children=["world!"])]``.
    '''
    tag: str
    attrs: Optional[Dict[str, Any]] = None
    children: Optional[List['NodeElement']] = None

    def as_dict(self) -> Dict[str, Any]:
        result = {'tag': self.tag}
        if self.attrs:
            result['attrs'] = self.attrs.copy()

        if self.children:
            result['children'] = []
            for child in self.children:
                if isinstance(child, NodeElement):
                    result['children'].append(child.as_dict())
                elif isinstance(child, str):
                    result['children'].append(child)

        return result

@dataclass
class Page():
    path: str
    url: str
    title: str
    description: str
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[List[NodeElement]] = None
    views: Optional[int] = None
    can_edit: Optional[bool] = None

@dataclass
class PageList():
    total_count : str
    pages: List[Page]

@dataclass
class PageViews():
    views: int