from html import escape
from pathlib import Path
from yattag import Doc, indent
import argparse

doc, tag, text, line = Doc().ttl()


def main():
    '''Used when calling the converter directly, parses arguments from the
       command line and sends the input filepath to convert_from_file, then
       writes HTML to the output file'''

    parser = argparse.ArgumentParser()
    parser.add_argument("source_file",
                        help="Provide a .paml file used for conversion")
    parser.add_argument("destination_file",
                        help="Provide an .html destination file. It will be"
                        + " appended if it exists and created if it doesn't")
    parser.add_argument("--indent",
                        help="Provide the amount of spaces used for"
                        + " indentation. Indentation is disabled by default",
                        type=int, default=None)
    args = parser.parse_args()
    source_file = Path(args.source_file)
    destination_file = Path(args.destination_file)

    if args.indent is not None:
        indnt = ' ' * args.indent

    convert_from_file(source_file)

    with open(destination_file, 'a+', encoding='utf-8') as f:
        if args.indent is not None:
            f.write(indent(doc.getvalue(), indentation=indnt))
        elif args.indent is None:
            f.write(doc.getvalue())


def convert_from_file(filepath):
    '''Used when the converter is imported, returns a string containing HTML'''

    global doc, tag, text, line
    doc, tag, text, line = Doc().ttl()

    with open(filepath, 'r', encoding='utf-8') as p:
        paml_lines = p.readlines()
        if not paml_lines:
            return ''
        elif paml_lines[-1] != '':
            paml_lines[-1] += '\n'
            paml_lines.append('')

    i = 0
    while i < len(paml_lines):
        i = identify_element(paml_lines, i)

    return doc.getvalue()


def convert_from_text(paml_text):
    '''Used when the converter is imported, returns a string containing HTML'''

    global doc, tag, text, line
    doc, tag, text, line = Doc().ttl()

    paml_lines = paml_text.splitlines(True)

    if not paml_lines:
        return ''
    elif paml_lines[-1] != '':
        paml_lines[-1] += '\n'
        paml_lines.append('')

    i = 0
    while i < len(paml_lines):
        i = identify_element(paml_lines, i)

    return doc.getvalue()


def identify_element(paml_lines: list, i: int) -> int:
    '''Identifies the element on the current line or skips the line. I wanted
       to switch the ifs into something 'smarter' like a dict of identifiers,
       but because of different lengths of identifiers, the best solution I
       could come up with was over 4 times slower. In terms of readability, the
       ifs are probably fine.'''

    paml_line = paml_lines[i].strip()

    if paml_line == '':
        # only spaces and \n on the line
        i += 1
    elif paml_line.startswith('#'):
        i = add_header(paml_lines, i)
    elif paml_line.startswith('>'):
        # '>' by itself does not necessarily mean a collapsible box, but all
        # the other cases nested collapsibles are handled by add_collapsible
        i = add_collapsible_box(paml_lines, i)
    elif paml_line.startswith('/'):
        i = add_command(paml_lines, i)
    elif paml_line.startswith('```'):
        # inline code is handled as part of format_txt
        i = add_code(paml_lines, i)
    elif paml_line.startswith('!['):
        i = add_image(paml_lines, i)
    elif paml_line.startswith('{'):
        i = add_paragraph(paml_lines, i)
    elif paml_line.startswith('-'):
        i = add_unordered_list(paml_lines, i)
    elif paml_line[0] in '0123456789':
        i = add_ordered_list(paml_lines, i)
    elif paml_line.startswith('|'):
        i = add_table(paml_lines, i)
    elif paml_line.startswith('<'):
        i = add_raw_html(paml_lines, i)
    else:
        print('Unsupported line, skipping: ', paml_lines[i])
        i += 1  # fail-safe in case something is not recognized
    return i


def add_header(paml_lines: list, i: int) -> int:
    if paml_lines[i].rstrip().startswith('# '):
        with tag('h1'):
            doc.asis(format_txt(paml_lines[i][2:-1]))
        i += 1
    elif paml_lines[i].rstrip().startswith('## '):
        with tag('h2'):
            doc.asis(format_txt(paml_lines[i][3:-1]))
        i += 1
    elif paml_lines[i].rstrip().startswith('### '):
        with tag('h3'):
            doc.asis(format_txt(paml_lines[i][4:-1]))
        i += 1
    elif paml_lines[i].rstrip().startswith('#### '):
        with tag('h4'):
            doc.asis(format_txt(paml_lines[i][5:-1]))
        i += 1
    elif paml_lines[i].rstrip().startswith('##### '):
        with tag('h5'):
            doc.asis(format_txt(paml_lines[i][6:-1]))
        i += 1
    elif paml_lines[i].rstrip().startswith('###### '):
        with tag('h6'):
            doc.asis(format_txt(paml_lines[i][7:-1]))
        i += 1
    return i


def add_collapsible_box(paml_lines: list, i: int) -> int:
    '''Makes a div that is a box holding together all collapsibles of a single
       type placed one after another.'''

    tag_class = ''
    position = ''
    if paml_lines[i][1] == "l":
        position = "l"
        tag_class = "collapsible-box-half-left"
    elif paml_lines[i][1] == "r":
        position = "r"
        tag_class = "collapsible-box-half-right"
    elif paml_lines[i][1] == "f":
        position = "f"
        tag_class = "collapsible-box-full"

    with tag('div', klass=tag_class):
        while i < len(paml_lines):
            if (not paml_lines[i].lstrip()
               or paml_lines[i].lstrip()[0] != '>'
               or paml_lines[i][0].lstrip() == '>'
               and paml_lines[i].lstrip()[1] != position):
                break
            with tag('details'):
                with tag('summary', klass='header'):
                    if paml_lines[i].lstrip()[2] != " ":
                        with tag('span', klass='icon'):
                            text(paml_lines[i].lstrip()[2])
                    text(paml_lines[i].lstrip()[3:].rstrip())
                    i += 1
                i = add_collapsible(paml_lines, i)
    return i


def add_collapsible(paml_lines: list, i: int, offset=0) -> int:
    '''Starts a loop to add all elements to a collapsible. The amount of
       spaces at the beginning of every line is counted to establish the
       current 'offset' - line's indentation level. With 0 anywhere, the
       collapsible (and the while loop) is terminated; an offset higher than
       current indicates a new indentation level that is then updated; a level
       lower than current but higher than 0 means an ending of a nested
       collapsible.

       Afterwards, there is a check for a special case of a nested collapsible
       (skipping identify_element since that would identify the > as
       a collapsible box that's useless since the collapsible already is in
       a box made for the outmost collapsibles). identify_element is instead
       called for every item that is not a collapsible.'''

    while i < len(paml_lines):
        spaces = 0
        for char in paml_lines[i]:
            if char == ' ':
                spaces += 1
            else:
                break

        if spaces == 0:
            break
        elif spaces > offset:
            offset = spaces
        elif spaces < offset:
            return i

        if paml_lines[i].lstrip()[0] == ">":
            with tag('details'):
                with tag('summary', klass='header'):
                    if paml_lines[i].lstrip()[2] != " ":
                        with tag('span', klass='icon'):
                            text(paml_lines[i].lstrip()[2])
                    text(paml_lines[i].lstrip()[3:].rstrip())
                    i += 1
                i = add_collapsible(paml_lines, i, offset)
        else:
            with tag('div', klass='entry'):
                i = identify_element(paml_lines, i)
    return i


def add_command(paml_lines: list, i: int) -> int:
    with tag('div', klass='command-box'):
        with tag('span', klass='command'):
            doc.asis(format_txt(paml_lines[i].lstrip()
                     [1:paml_lines[i].lstrip().find('/*')]).rstrip())

        if ('/*' in paml_lines[i]
           and paml_lines[i][paml_lines[i].find('/*') + 2] != '*'):
            # making sure '/**' isn't recognized as '/*' when '/*' is not there
            with tag('span', klass='same-line-comment'):
                doc.asis(format_txt(paml_lines[i]
                                    [paml_lines[i].find('/*') + 2:
                                    paml_lines[i].find('*/')]))
        if '/**' in paml_lines[i]:
            with tag('div', klass='small-comment'):
                doc.asis(format_txt(paml_lines[i]
                                    [paml_lines[i].find('/**') + 3:
                                    paml_lines[i].find('**/')]))

    i += 1
    return i


def add_code(paml_lines: list, i: int) -> int:
    if paml_lines[i + 2].rstrip().endswith('```'):
        # code line
        i = add_code_line(paml_lines, i)
    else:
        # code block
        i = add_code_block(paml_lines, i)

    return i


def add_code_line(paml_lines: list, i: int) -> int:
    with tag('div', klass='line-code-box'):
        if ('/*' in paml_lines[i]
           and paml_lines[i][paml_lines[i].find('/*') + 2] != '*'):
            # making sure '/**' isn't recognized as '/*' when '/*' is not there
            with tag('div', klass='line-code-comment'):
                doc.asis(format_txt(paml_lines[i]
                         [paml_lines[i].find('/*') + 2:
                         paml_lines[i].find('*/')].strip()))

        if '/**' in paml_lines[i]:
            with tag('div', klass='line-code-small-comment'):
                doc.asis(format_txt(paml_lines[i]
                         [paml_lines[i].find('/**') + 3:
                         paml_lines[i].find('**/')].strip()))
        i += 1
        with tag('code', klass='line-code'):
            # Removing trailing whitespaces and the new line at the end of line
            text(paml_lines[i].strip())
        i += 2
    return i


def add_code_block(paml_lines: list, i: int) -> int:
    with tag('div', klass='block-code-box'):
        if ('/*' in paml_lines[i]
           and paml_lines[i][paml_lines[i].find('/*') + 2] != '*'):
            # making sure '/**' isn't recognized as '/*' when '/*' is not there
            with tag('div', klass='block-code-comment'):
                doc.asis(format_txt(paml_lines[i]
                         [paml_lines[i].find('/*') + 2:
                         paml_lines[i].find('*/')].strip()))

        if '/**' in paml_lines[i]:
            with tag('div', klass='block-code-small-comment'):
                doc.asis(format_txt(paml_lines[i]
                         [paml_lines[i].find('/**') + 3:
                         paml_lines[i].find('**/')].strip()))
        i += 1
        code_to_add = []
        while i < len(paml_lines):
            if paml_lines[i].strip() == '```':
                # Removing a useless new line at the end of the last line
                code_to_add[-1] = code_to_add[-1].rstrip()
                with tag('code', klass='block-code'):
                    with tag('pre'):
                        text(''.join(code_to_add))
                i += 1
                break
            else:
                code_to_add.append(paml_lines[i])
            i += 1
    return i


def add_image(paml_lines: list, i: int) -> int:
    if paml_lines[i][0] == '{':
        line = paml_lines[i][1:]
    else:
        line = paml_lines[i]

    if line.lstrip().startswith('!l'):
        kls = 'img-half-left'
    elif line.lstrip().startswith('!r'):
        kls = 'img-half-right'
    else:
        kls = None

    if kls is not None:
        doc.stag('img', alt=line[line.find('[') + 1:line.find(']')],
                 src=line[line.find('(') + 1:line.find(')')], klass=kls)
    else:
        doc.stag('img', alt=line[line.find('[') + 1:line.find(']')],
                 src=line[line.find('(') + 1:line.find(')')])
    i += 1
    return i


def add_paragraph(paml_lines: list, i: int) -> int:
    with tag('div', klass='paragraph'):
        if (len(paml_lines[i].lstrip()) > 1
           and paml_lines[i].lstrip()[1] == '!'):
            i = add_image(paml_lines, i)
        else:
            i += 1
        with tag('p'):
            text_to_add = ""
            while i < len(paml_lines):
                if paml_lines[i].strip() == "}":
                    break
                else:
                    text_to_add += paml_lines[i]
                i += 1
            text_to_add = '<br>'.join([line.lstrip()
                                       for line in text_to_add.splitlines()])
            doc.asis(format_txt(text_to_add))
    i += 1
    return i


def add_unordered_list(paml_lines: list, i: int, offset=None) -> int:
    '''Makes use of an offset to determine nested lists and lists inside
       collapsibles.'''

    if offset is None:
        # check where the list is positioned if it's not explicitly stated
        # this helps with e.x. lists inside collapsibles
        offset = 0
        for char in paml_lines[i]:
            if char == ' ':
                offset += 1
            else:
                break

    with tag('ul'):
        while i < len(paml_lines):
            if paml_lines[i].strip() == '':
                break
            elif (paml_lines[i].lstrip()[0] != '-'
                  and not paml_lines[i].lstrip()[0].isnumeric()):
                break

            spaces = 0
            for char in paml_lines[i]:
                if char == ' ':
                    spaces += 1
                else:
                    break
            if offset > 0 and spaces < offset:
                # going back
                offset = spaces
                break
            elif paml_lines[i][offset] == '-':
                # line('li', format_txt(paml_lines[i][offset + 2:-1]))
                with tag('li'):
                    doc.asis(format_txt(paml_lines[i][offset + 2:-1]))
                i += 1
            elif paml_lines[i][offset].isnumeric():
                i = add_ordered_list(paml_lines, i)
            elif paml_lines[i][spaces] == '-':
                i = add_unordered_list(paml_lines, i, spaces)
            elif paml_lines[i][spaces].isnumeric():
                i = add_ordered_list(paml_lines, i, spaces)
    return i


def add_ordered_list(paml_lines: list, i: int, offset=None) -> int:
    '''Makes use of an offset to determine nested lists and lists inside
       collapsibles.'''

    numbers = '0123456789'

    if offset is None:
        # check where the list is positioned if it's not explicitly stated
        # this helps with e.x. lists inside collapsibles
        offset = 0
        for char in paml_lines[i]:
            if char == ' ':
                offset += 1
            else:
                break

    with tag('ol'):
        while i < len(paml_lines):
            if paml_lines[i].strip() == '':
                break
            elif (paml_lines[i].lstrip()[0] not in numbers
                  and paml_lines[i].lstrip()[0] != '-'):
                break

            spaces = 0
            for char in paml_lines[i]:
                if char == ' ':
                    spaces += 1
                else:
                    break

            if offset > 0 and spaces < offset:
                offset = spaces
                break
            elif paml_lines[i][offset] in numbers:
                with tag('li'):
                    doc.asis(format_txt(paml_lines[i][offset + 2:-1]))
                i += 1
            elif paml_lines[i][offset] == '-':
                i = add_unordered_list(paml_lines, i)
            elif paml_lines[i][spaces] in numbers:
                i = add_ordered_list(paml_lines, i, spaces)
            elif paml_lines[i][spaces] == '-':
                i = add_unordered_list(paml_lines, i, spaces)
    return i


def add_table(paml_lines: list, i: int) -> int:
    table_with_headers = True

    for cell in paml_lines[i + 1].split()[1:-1:2]:
        # [1:-1:2] - before first and after last not needed
        # every other to skip the dividers
        for char in cell:
            if char not in [' ', '-']:
                table_with_headers = False
                break
        break

    with tag('table'):
        if table_with_headers:
            with tag('tr'):
                for x in paml_lines[i].split('|')[1:-1]:
                    # [1:-1] - before first and after last not needed
                    with tag('th'):
                        doc.asis(format_txt(x.strip()))
                i += 2

        while i < len(paml_lines):
            if not paml_lines[i].lstrip().startswith('|'):
                break
            else:
                with tag('tr'):
                    for x in paml_lines[i].split('|')[1:-1]:
                        # [1:-1] - before first and after last not needed
                        with tag('td'):
                            doc.asis(format_txt(x.strip()))
                    i += 1
    return i


def add_raw_html(paml_lines: list, i: int) -> int:
    i += 1

    while i < len(paml_lines):
        if paml_lines[i].strip() == '>':
            i += 1
            break
        else:
            doc.asis(paml_lines[i].strip())
            i += 1
    return i


def format_txt(txt: str) -> str:
    '''Using txt in the names to never accidentally mix it with yattag's 'text'
       by accident. All text sent into this function should already be inside
       yattag's doc.asis() function.'''

    # Add inline code, send non-code parts to decorate, check them for links

    txt = txt.strip()
    result = ''

    i = 0
    buffer = ''
    while i < len(txt):
        if txt[i:i+2] == '``':
            decorated = decorate_txt(buffer)
            buffer = ''
            with_links = find_links(decorated)
            decorated = ''
            result += with_links
            with_links = ''

            code = txt[i:i + txt[i+2:].find('``') + 4]
            result += add_inline_code(code)
            i += len(code)
        else:
            buffer += txt[i]
            i += 1

    decorated = decorate_txt(buffer)
    buffer = ''
    with_links = find_links(decorated)
    decorated = ''
    result += with_links
    with_links = ''

    return result


def add_inline_code(txt: str) -> str:
    result = ('<span class="inline-code">' + escape(txt[2:-2]) + "</span>")
    return result


def find_links(txt: str) -> str:
    result = ''
    i = 0
    while i < len(txt):
        if txt[i] == '[' and txt[i:].find('](') != -1:
            # link_start and link_end refer to the actual link inside ()
            link_start = i + txt[i:].find('](')
            link_end = link_start + txt[link_start:].find(')')
            result += add_link(txt[i:link_end + 1])
            i += len(txt[i:link_end + 1])
        else:
            result += txt[i]
            i += 1
    return result


def add_link(txt: str) -> str:
    result = ("<a target=\"_blank\" href="
              + f"\"{txt[txt.find('(') + 1:txt.find(')')]}\">"
              + f"{format_txt(txt[txt.find('[') + 1:txt.find(']')])}</a>")
    return result


def decorate_txt(txt: str) -> str:
    tags = {"**": ("<b>", "</b>"), "__": ("<i>", "</i>"),
            "~~": ("<s>", "</s>")}
    result = txt
    i = 0
    while any((x in result for x in tags.keys())) and i < len(result):
        if result[i:i + 2] == "``":
            # special case for inline code since then any other styling needs
            # to be ignored
            tag_end = result.rfind("``")
            result = (result[:i] + tags[result[i:i + 2]][0]
                      + result[i + 2:tag_end] + tags[result[i:i + 2]][1]
                      + result[tag_end + 2:])
            i += result.rfind("</span>")
            continue
        elif result[i:i + 2] in tags.keys():
            # The end is the first tag of the same type found starting at
            # after the opening tag
            tag_end = i + 2 + result[i + 2:].find(result[i:i + 2])

            result = (result[:i] + tags[result[i:i + 2]][0]
                      # ^ until tag    ^ opening tag from dict
                      + result[i + 2:tag_end] + tags[result[i:i + 2]][1]
                      # ^ inside the tag        ^ closing tag from dict
                      + result[tag_end + 2:])
            #           ^ rest of text

            # i + 2 since all tags have a length of 2 (like **) and it's easier
            # than making a solution for all lengths that's useless for now
            # will need rewriting if longer tags are needed
        i += 1
    return result


if __name__ == '__main__':
    main()
