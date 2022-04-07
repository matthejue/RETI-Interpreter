from colormanager import ColorManager as CM
import re


def colorize_help_page(cinput):
    cinput = colorize(r"(\[|\])", cinput, CM().MAGENTA, CM().BLUE)
    cinput = colorize("`[^`]+`", cinput, CM().RED, CM().BLUE)
    cinput = colorize("<.+>`", cinput, CM().RED, CM().BLUE)
    cinput = colorize(
        "(=+[^`][^`])|(~+[^`][^`])",
        cinput,
        CM().BRIGHT + CM().WHITE,
        CM().NORMAL + CM().BLUE,
    )
    cinput = colorize(
        r"[A-Z_]{2,}", cinput, CM().YELLOW, CM().BLUE, r"-{1,2}\w+ [A-Z_]{2,}"
    )
    cinput = colorize(r"-{1,2}\w+", cinput, CM().GREEN, CM().BLUE)
    return CM().BLUE + cinput + CM().RESET_ALL


def colorize(pattern, cinput, ansi, default_ansi, condition=None):
    p = re.compile(condition if condition else pattern)
    num_extra_letters = 0
    itertr = p.finditer(cinput)
    for span in map(lambda i: i.span(), itertr):
        if condition:
            match_pre = re.search(
                pattern,
                cinput[span[0] + num_extra_letters : span[1] + num_extra_letters],
            )
            if match_pre:
                sub_span_pre = match_pre.span()
                sub_span = (span[0] + sub_span_pre[0], span[0] + sub_span_pre[1])
                cinput = (
                    cinput[: sub_span[0] + num_extra_letters]
                    + ansi
                    + cinput[
                        sub_span[0]
                        + num_extra_letters : sub_span[1]
                        + num_extra_letters
                    ]
                    + default_ansi
                    + cinput[sub_span[1] + num_extra_letters :]
                )
        else:
            cinput = (
                cinput[: span[0] + num_extra_letters]
                + ansi
                + cinput[span[0] + num_extra_letters : span[1] + num_extra_letters]
                + default_ansi
                + cinput[span[1] + num_extra_letters :]
            )
        num_extra_letters += len(ansi) + len(default_ansi)
    return cinput
