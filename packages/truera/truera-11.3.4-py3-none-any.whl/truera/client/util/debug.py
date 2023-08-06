"""
# Debugging utilities

- Owners: piotrm
"""

from builtins import print as builtin_print
import inspect
import traceback


def render_exception(exc: Exception):
    """
    Create a representation of an exception that includes minimal frame
    information for exception raise site. This differs in the output of
    str(Exception) especially for assertion exceptions that do not print out the
    raise site.
    """

    tb_info = traceback.extract_tb(exc.__traceback__)
    filename, line_number, function_name, text = tb_info[-1]
    message = f"{str(type(exc).__name__)} {filename}:{line_number}:{function_name}:{text}"
    text = str(exc)
    if text:
        message += "\n" + retab(text, "\t")

    return message


def retab(s, tab: str = "  ", tab_first: bool = True):
    """
    Changes the tab/margin of the given string `s` to the given `tab`. If
    `tab_first` is provided, also adds the marging to the first line of `s`.
    """

    if tab_first:
        return "\n".join([tab + s for s in s.split("\n")])
    else:
        return ("\n" + tab).join(s.split("\n"))


def _get_margin(s):
    if len(s) == 0:
        return ""

    margin = ""

    while s[0] in [" ", "\t"]:
        margin += s[0]
        s = s[1:]

    return margin


def _get_frameinfo(depth=0):
    return inspect.stack()[depth]


def print(
    *objects,
    sep=' ',
    end='\n',
    file=None,
    flush=False,
    max_cols: int = 200
) -> None:
    """
    A print variant that prepends a margin on each line that is retrieved from
    the margin at the site where it was invoked. Other than max_cols, the
    signature is the same as `builtins.print`.
    """

    fi = _get_frameinfo(depth=2)
    line = fi.code_context[0]

    name = fi.function
    margin = list(_get_margin(line))

    if len(name) < len(margin) - 1:
        margin[0:len(name)] = list(name)
    else:
        if len(margin) >= 3:
            margin = list(name[0:len(margin)])
            margin[-3:] = list(".. ")
        else:
            pass

    margin = ''.join(margin)

    content = sep.join(
        map(lambda obj: obj if isinstance(obj, str) else str(obj), objects)
    )

    if max_cols is not None:
        split_lines = []
        for line in content.split("\n"):
            prefix_line = margin + line
            while len(prefix_line) > max_cols:
                split_lines.append(prefix_line[0:max_cols])
                prefix_line = margin + prefix_line[max_cols:]

            split_lines.append(prefix_line)

        content = "\n".join(split_lines)
    else:
        content = "\n".join([margin + line for line in content.split("\n")])

    builtin_print(content, end=end, file=file, flush=flush)
