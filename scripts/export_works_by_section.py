from export_works import *

# WARNING: requires to be in the same folder as export_works.py


def extract_lines(files):
    """
    parses the files line per line and returns the following structure

    return:
        {toh1: [(vol_id, line1), (vol_id, line2), ...], toh2: ...}
    """
    missing_inc = 1

    works = []
    prev_toh = ''
    current_work = []
    for file in files:
        prefix = file.stem
        lines = [line.strip().strip('\ufeff') for line in file.open().readlines()]
        for line in lines:
            toh = re.findall(r'\{(T[0-9]+)\}', line)
            if toh:
                toh = toh[0]
                if prev_toh != '':
                    current_work.append((prefix, line))

                    if prev_toh == 'T00':
                        prev_toh += str(missing_inc)
                        missing_inc += 1

                    works.append((prev_toh, current_work))

                # initialize new work
                current_work = [(prefix, line)]
                prev_toh = toh
            else:
                current_work.append((prefix, line))
    if not works and prev_toh and current_work:
        works.append((prev_toh, current_work))
    return works


def write_works(works, out_path, linesep='\n'):
    for parent in list(out_path.parents) + [out_path]:
        if not parent.is_dir():
            parent.mkdir(exist_ok=True)

    for work, lines in works:
        if not work.startswith('X'):
            out_file = out_path / str(work + '.txt')
            out_file.write_text(linesep.join(lines))


sections = {
    'འདུལ་བ།':
        [
            "001-tagged.txt",
            "002-tagged.txt",
            "003-tagged.txt",
            "004-tagged.txt",
            "005-tagged.txt",
            "006-tagged.txt",
            "007-tagged.txt",
            "008-tagged.txt",
            "009-tagged.txt",
            "010-tagged.txt",
            "011-tagged.txt",
            "012-tagged.txt",
            "013-tagged.txt"
        ],
    'འབུམ།':
        [
            "014-tagged.txt",
            "015-tagged.txt",
            "016-tagged.txt",
            "017-tagged.txt",
            "018-tagged.txt",
            "019-tagged.txt",
            "020-tagged.txt",
            "021-tagged.txt",
            "022-tagged.txt",
            "023-tagged.txt",
            "024-tagged.txt",
            "025-tagged.txt"
        ],
    'ཉི་ཁྲི།':
        [
            "026-tagged.txt",
            "027-tagged.txt",
            "028-tagged.txt"
        ],
    'ཁྲི་བརྒྱད།':
        [
            "029-tagged.txt",
            "030-tagged.txt",
            "031-tagged.txt",
            "032-tagged.txt"
        ],
    'བརྒྱད་སྟོང་།':
        [
            "033-tagged.txt"
        ],
    'ཤེས་རབ་སྣ་ཚོགས།':
        [
            "034-tagged.txt"
        ],
    'ཕལ་ཆེན།':
        [
            "035-tagged.txt",
            "036-tagged.txt",
            "037-tagged.txt",
            "038-tagged.txt"
        ],
    'དཀོན་བརྩེགས།':
        [
            "039-tagged.txt",
            "040-tagged.txt",
            "041-tagged.txt",
            "042-tagged.txt",
            "043-tagged.txt",
            "044-tagged.txt"
        ],
    'མདོ་སྡེ།':
        [
            "045-tagged.txt",
            "046-tagged.txt",
            "047-tagged.txt",
            "048-tagged.txt",
            "049-tagged.txt",
            "050-tagged.txt",
            "051-tagged.txt",
            "052-tagged.txt",
            "053-tagged.txt",
            "054-tagged.txt",
            "055-tagged.txt",
            "056-tagged.txt",
            "057-tagged.txt",
            "058-tagged.txt",
            "059-tagged.txt",
            "060-tagged.txt",
            "061-tagged.txt",
            "062-tagged.txt",
            "063-tagged.txt",
            "064-tagged.txt",
            "065-tagged.txt",
            "066-tagged.txt",
            "067-tagged.txt",
            "068-tagged.txt",
            "069-tagged.txt",
            "070-tagged.txt",
            "071-tagged.txt",
            "072-tagged.txt",
            "073-tagged.txt",
            "074-tagged.txt",
            "075-tagged.txt",
            "076-tagged.txt"
        ],
    'རྒྱུད་འབུམ།':
        [
            "077-tagged.txt",
            "078-tagged.txt",
            "079-tagged.txt",
            "080-tagged.txt",
            "081-tagged.txt",
            "082-tagged.txt",
            "083-tagged.txt",
            "084-tagged.txt",
            "085-tagged.txt",
            "086-tagged.txt",
            "087-tagged.txt",
            "088-tagged.txt",
            "089-tagged.txt",
            "090-tagged.txt",
            "091-tagged.txt",
            "092-tagged.txt",
            "093-tagged.txt",
            "094-tagged.txt",
            "095-tagged.txt",
            "096-tagged.txt"
        ],
    'རྙིང་རྒྱུད།':
        [
            "097-tagged.txt",
            "098-tagged.txt",
            "099-tagged.txt"
        ],
    'གཟུངས་འདུས།':
        [
            "100-tagged.txt",
            "101-tagged.txt"
        ],
    'དྲི་མེད་འོད།':
        [
            "102-tagged.txt"
        ]
}

if __name__ == '__main__':
    args = parser.parse_args()
    prefix = Path('../derge-kangyur-tags')
    out_path = Path('export/sections')

    for section, filenames in sections.items():
        paths = [prefix / filename for filename in filenames]
        works = extract_lines(paths)
        works = works_in_pages(works)
        works = works_stripped(works)
        flatten_for_output(works)
        # if bool(args.clean_content):
        works = remove_markup(works)
        write_works(works, out_path / section)
