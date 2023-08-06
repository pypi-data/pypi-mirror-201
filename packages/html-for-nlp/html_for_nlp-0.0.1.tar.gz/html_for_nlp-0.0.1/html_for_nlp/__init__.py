from functools import cached_property
import random

from bs4 import BeautifulSoup, Tag, NavigableString

def stripped_text(text):
    return ' '.join(text.split())

def text_to_html(tag, text, add_new_line=True):
    if not text:
        return ''
    html_text = f'<{tag}>{text}</{tag}>' if tag else text
    if add_new_line:
        html_text = html_text + '\n'
    return html_text

class HTMLObject:
    
    # TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
    # TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']
    TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span']
    MAX_DEPTH = 100
    
    def __init__(self, html, is_soup=False, depth=0):
        
        soup = BeautifulSoup(html, features='lxml') if not is_soup else html

        self.depth = depth
        self.soup = soup
        self.tag = soup.name if soup.name else ''
        self.text = stripped_text(soup.text)
        self.included_in_summary = False
        
    @classmethod
    def _search_tags(cls, soup, tags=TAGS):
    
        elements = []
        if soup.text.strip() and isinstance(soup, Tag):
            for child in soup.children:
                if (child.name in tags or isinstance(child, NavigableString)) and child.text.strip():
                    elements.append(child)
                else:
                    elements.extend(cls._search_tags(child, tags))
                
        return elements
        
    @cached_property
    def elements(self):

        if self.depth > self.MAX_DEPTH:
            return []
        
        elements = []
        
        if self.tag in ['ul', 'ol']:
            list_items = self.soup.find_all('li', recursive=False)
            elements = [HTMLObject(item, is_soup=True, depth=self.depth + 1) for item in list_items if item.text]
        else:
            element_tags = self._search_tags(self.soup)
            elements = [HTMLObject(tag, is_soup=True, depth=self.depth + 1) for tag in element_tags if tag.text]
            
        return elements
    
    @cached_property
    def elements_recursive(self):
        elements = []
        for e in self.elements:
            if e.is_terminal:
                elements.append(e)
            else:
                elements.extend(e.elements_recursive)
        return elements
    
    @cached_property
    def is_terminal(self):
        return len(self.elements) == 0
    
    def _collect_text(self, summarized=True):
        
        text = ''
        
        if summarized and not self.included_in_summary and self.is_terminal:
            return text
        
        if self.is_terminal:
            if self.text:
                text = text_to_html(self.tag, self.text)
        else:
            children_text = ''
            for child in self.elements:
                children_text = children_text + child._collect_text(summarized)
            
            if children_text:
                text = text + f'<{self.tag}>\n'
                text = text + children_text
                text = text + f'</{self.tag}>\n'
                
        return text

class HTMLDocument(HTMLObject):
    def __init__(self, html):
        self.summarized = False
        super().__init__(html, is_soup=False, depth=0)
        
    def unsummarize(self):
        # Undo previous summarization
        for e in self.elements_recursive:
            e.included_in_summary = False
        
    # TODO: return context
    def random_excerpt(self, n_items=5, seed=None):
        self.unsummarize()
        max_start = max(len(self.elements_recursive) - n_items, 0)
        
        start = random.randint(0, max_start)
        
        for e in self.elements_recursive[start:start + n_items]:
            e.included_in_summary = True
            
        self.summarized = True
        return self._collect_text()

    @cached_property
    def full_text(self):
        text = self._collect_text(summarized=False)

        # Replace soft hyphens, see https://stackoverflow.com/questions/51976328/best-way-to-remove-xad-in-python
        text = text.replace('\xad', '') # Soft hyphen
        text = text.replace('\u200b', '') # Zero-width space
        return text

    @classmethod
    def inner_text(cls, text):

        start_index = text.index('<[document]>\n') + len('<[document]>\n')
        end_index = text.index('\n</[document]>')

        return text[start_index:end_index]
