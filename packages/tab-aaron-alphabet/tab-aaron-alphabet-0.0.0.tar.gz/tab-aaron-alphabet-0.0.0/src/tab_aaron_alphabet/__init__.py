import argparse as _argparse

parser = _argparse.ArgumentParser(
    fromfile_prefix_chars='@',
    allow_abbrev=False,
)
parser.add_argument('targets', nargs='*')

def main(args=None):
    ns = parser.parse_args(args)
    if len(ns.targets):
        targets = ns.targets
    else:
        targets = ['.']
    files = walk(targets)
    for file in targets:
        with open(file, 'r') as s:
            text = s.read()
        text = text.replace('\t', "    ")
        with open(file, 'w') as s:
            s.write(text) 

def walk(*targets):
    ans = list()
    for target in targets:
        if _os.path.isfile(target):
            if target not in ans:
                ans.append(target)
            continue
        for (root, dirnames, filenames) in _os.walk(target):
            for filename in filenames:
                file = _os.path.join(root, filename)
                if file not in ans:
                    ans.append(file)
    return ans
