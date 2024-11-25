import aiohttp
import html2text
from typing import Tuple
from bs4 import BeautifulSoup

class HTMLConverter:
    def __init__(self):
        self.html2text = html2text.HTML2Text()
        self.html2text.ignore_links = False
        self.html2text.ignore_images = False
        self.html2text.body_width = 0  # 不限制行宽
        
    async def fetch_html(self, url: str) -> Tuple[str, str]:
        """
        获取网页HTML内容和标题
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch URL: {url}, status: {response.status}")
                
                html_content = await response.text()
                
                # 使用BeautifulSoup解析HTML获取标题
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.title.string if soup.title else "Untitled"
                
                return html_content, title.strip()
    
    def convert_to_markdown(self, html_content: str) -> str:
        """
        将HTML内容转换为Markdown格式
        """
        return self.html2text.handle(html_content)
