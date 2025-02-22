import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            escaped = mistune.escape(code)
            return f"\n<pre><code>{escaped}</code></pre>\n"

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

    def autolink(self, link, is_email=False):
        text = link = mistune.escape_link(link)
        if is_email:
            link = f"mailto:{link}"
        return f'<a href="{link}" target="_blank">{text}</a>'

    def link(self, link, title, text):
        link = mistune.escape_link(link)
        if not title:
            return f'<a href="{link}" target="_blank">{text}</a>'
        title = mistune.escape(title, quote=True)
        return f'<a href="{link}" title="{title}" target="_blank">{text}</a>'

    def image(self, src, title, text):
        src = mistune.escape_link(src)
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = f'<img class="pure-img" src="{src}" alt="{text}" title="{title}" '
        else:
            html = f'<img class="pure-img" src="{src}" alt="{text}" '

        if self.options.get("use_xhtml"):
            return f"{html} />"
        return f"{html} >"


class PlaintextRenderer(mistune.Renderer):
    def _nothing(*args, **kwargs):
        return " "

    def paragraph(self, text):
        return f"{text}\n"

    block_code = (
        block_quote
    ) = (
        block_html
    ) = header = hrule = list = list_item = table = table_row = table_cell = _nothing

    def autolink(self, link, is_email):
        return link

    # def codespan(self, text):
    #     return f"`{text}`"

    # def double_emphasis(self, text):
    #     return f"**{text}**"

    # def emphasis(self, text):
    #     return f"*{text}*"

    linebreak = newline = image = _nothing

    def link(self, link, title, text):
        return f"[{link}]"

    def strikethrough(self, text):
        return text


highlight_renderer = HighlightRenderer(escape=True)
plaintext_renderer = PlaintextRenderer(escape=True)

highlight_markdown = mistune.Markdown(renderer=highlight_renderer)
plaintext_markdown = mistune.Markdown(renderer=plaintext_renderer)
