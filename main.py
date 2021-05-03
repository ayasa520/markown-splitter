import os
import re
import sys


def split_md(filename):
    # , prefix, date
    prefix = input("输入命名前缀\n")
    usefm = input("是否使用 Front Matter? y/n\n")
    fm = []

    if usefm == 'y':
        print("输入 Front Matter 属性 (每行一个, 输入为空完成输入)")
        while True:
            attibute = input()
            if attibute.strip() == '':
                break
            else:
                fm.append(attibute)

    fm = '\n'.join(fm)
    folder = os.path.abspath(os.path.dirname(filename))

    with open(filename, 'r', encoding='utf-8')as f:
        index = 1
        md_content = []
        for line in f.readlines():
            # 匹配一级标题
            if re.match(r"^#{1,1} ", line):
                title = re.findall(r"# (.+)", line)[0]
                if md_content and ''.join(md_content).strip() != '':
                    new_file_name = folder + '\\' + prefix + "_" + '{:02d}'.format(index) + ".md"
                    with open(new_file_name, 'w', encoding='utf-8') as newf:
                        newf.write(''.join(md_content))
                        index += 1
                md_content = []

                # 若不使用 front matter, 直接添加一级标题
                if usefm == 'y':
                    md_content.append('---\ntitle: ' + '"' + title + '"\n' + fm + '\n---\n')
                else:
                    md_content.append('# ' + title)

            else:
                # 其他内容直接添加
                md_content.append(line)

        # 最后一部分内容没有下一个一级标题
        new_file_name = folder + '\\' + prefix + "_" + '{:02d}'.format(index) + ".md"
        with open(new_file_name, 'w', encoding='utf-8') as newf:
            newf.write(''.join(md_content))


def level_up(filename):
    new_content = []
    with open(filename, encoding='utf-8')as f:
        for line in f.readlines():
            if re.match(r"^#+", line):
                new_content.append(line[1:])
            else:
                new_content.append(line)
    with open(filename, 'w', encoding='utf-8')as f:
        f.write(''.join(new_content))


def level_down(filename):
    new_content = []
    with open(filename, encoding='utf-8')as f:
        for line in f.readlines():
            if re.match(r"^#+", line):
                new_content.append('#' + line)
            else:
                new_content.append(line)
    with open(filename, 'w', encoding='utf-8')as f:
        f.write(''.join(new_content))


if __name__ == '__main__':
    filename = sys.argv[1]
    func = [level_up, level_down, split_md, ]
    print(filename)
    if filename[-3:] != '.md':
        cont = input("非 md 文档, 是否继续? y/n\n")
        if cont == 'n':
            exit()
    op = input("输入要完成的操作\n1: 所有标题等级提升 1 级\n2: 所有标题等级降低 1 级\n3: 将文档按一级标题拆分开\n")
    try:
        func[int(op) - 1](filename)
    except:
        exit()
