'''Generate the root Readme file'''
import os
import re
import subprocess

re_md_h1 = re.compile("^#[^#](.*)", re.I)
readme_markdown = '''
# 平时做的一些小实验，小代码，小Tip的收集和分享

平时做的一些如fuzz的小实验，或者写的一些小工具，其内容并不能成为一篇文章或者一个项目，但是又是可以分享的，我就放到这里来。


## 目录

{tree}

'''


def all_markdown():
    md_lst = []
    for dirpath, _, file_list in os.walk("."):
        for filename in [f for f in file_list if f.endswith(".md")]:
            path = os.path.join(dirpath, filename)
            md_lst.append(path)
    return md_lst


def main():
    tree = ""
    md_lst = all_markdown()
    for md_file in md_lst:
        content = open(md_file, "r").read()
        mth = re_md_h1.match(content)
        if mth:
            head1 = mth.group(1)
            li_item = "- [{}]({})\n".format(head1, md_file)
            tree = tree + li_item

    root_readme = readme_markdown.format(tree=tree)
    with open("readme.md", "w") as readme:
        readme.write(root_readme)
    git_commit_lst = ['git', 'commit', '-am', '"update readme.md"']
    subprocess.Popen(git_commit_lst)

if __name__ == '__main__':
    main()
