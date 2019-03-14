from pathlib import Path


def check_existence(in_path, string, left=5, right=5):
    vols = Path(in_path).glob('*.*')
    for vol in vols:
        content = vol.read_text().strip().split('\n')
        for num, line in enumerate(content):
            if string in line:
                l = num - left if num - left >= 0 else 0
                r = num + right if num + right < len(content) else len(content) - 1
                report = '\n'.join(content[l:r])
                report = report.replace(string, '***' + string + '***')
                print(vol.name)
                print(report)
                print()


if __name__ == '__main__':

    # Prints to stdout the line where the expression was found surrounded by some context

    expression = 'ལས་བརྒྱ་ཐམ་པ'
    lines_before = 5
    lines_after = 5
    in_dir = '../derge-kangyur-tags'
    check_existence(in_dir, expression, left=lines_before, right=lines_after)
