#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# yogurt_lei@foxmail.com
# 2018-06-23 11:33
# 基于git diff 打增量包(jdk8+maven3)
# --pname=项目工作区路径 --ocid=oldCommitID --ncid=newCommitID

import re
import os
import time
import zipfile
import shutil
import argparse
import xml.etree.ElementTree as ET

COMPLEX_HANDLE_FILE_TYPE = ('.sql', '.properties', 'pom.xml', '.md')
OUT_PUT_LIST = {'vague': [], 'delete': [], 'add': [], "resources": []}


def starter(workPath, oldCommitId, newCommitId):
    """
       :type workPath: string 工作区路径
       :type oldCommitId: string commitId
       :type newCommitId: string commitId
    """
    global ctx, curr_branch, unStash
    unStash = False
    # 未指定 --pname 工作区 默认为当前文件夹
    if not workPath:
        if valider_path(os.path.join(os.getcwd(), '.git')) == _DIR:
            workPath = os.getcwd()
        else:
            raise RuntimeError('未指定--pname参数且当前文件夹非git项目')
    # 定位到项目路径
    try:
        os.chdir(workPath)
    except FileNotFoundError:
        print('项目路径不正确,重新指定 --pname参数')

    if os.system('git --version') != 0:
        raise RuntimeError('git配置有误,检查git配置')
    else:
        if os.system('git show %s %s --name-only' % (oldCommitId, newCommitId)) != 0:
            raise RuntimeError('不正确的commitId参数,检查--ocid和--ncid参数')
        # 保存现场
        for line in os.popen('git branch').readlines():
            if line.startswith('*'):
                curr_branch = line[1:].strip()
                break
        os.system('git stash save "temp_statsh_for_update"')
        os.system('git checkout %s' % newCommitId)

    try:
        basePath = workPath.rstrip(os.sep)
        ctx = basePath[basePath.rfind(os.sep) + 1:]
        compile_workspace()
        os.system('git diff %s %s > diff.patch' % (oldCommitId, newCommitId))

        # 创建补丁包文件夹
        try:
            os.mkdir(ctx)
        except FileExistsError:
            shutil.rmtree(ctx)
            os.mkdir(ctx)

        # 遍历diff action
        with open('diff.patch', errors='ignore') as fr:
            line = fr.readline()
            while line:
                matcher = re.match(r'^diff --git a/(.*) b/(.*)', line)
                if matcher is not None:
                    a = matcher.group(1)
                    if a.endswith(COMPLEX_HANDLE_FILE_TYPE):  # 复杂处理类型
                        fr.seek(handle_complex_file_type(a, fr.tell()))
                    else:
                        try:
                            if a.startswith('src/main/resources'):
                                handle_src_main_resources(a)
                            elif a.startswith('src/main/webapp'):
                                handle_src_main_webapp(a)
                            elif a.startswith('src/main/java'):
                                handle_src_main_java(a)
                        except FileNotFoundError:
                            OUT_PUT_LIST['delete'].append(a)
                line = fr.readline()
    except:
        # 异常恢复现场
        unStash = True
        os.system('git checkout %s' % curr_branch)
        os.system('git stash pop')
        raise RuntimeError('编译工作区发生异常')


def cleaner(ocid, ncid):
    # 压缩更新文件 & 清理工作 & 输出
    with open(os.path.join(ctx, "README.md"), 'w', encoding='utf-8') as fw:
        fw.write('update-Time: %s\n' % time.strftime("%Y-%m-%d %H:%M:%S"))
        fw.write('update-user: %s' % os.popen('git config user.email').readline())
        fw.write('diff commit id: %s...%s\n' % (ocid, ncid))

        if OUT_PUT_LIST['delete']:
            fw.write('\n\nDeleted resource:\n')
            for item in OUT_PUT_LIST['delete']:
                fw.write(item + "\n")

        if OUT_PUT_LIST['resources']:
            fw.write('\n\nUpdate resources:\n')
            for item in OUT_PUT_LIST['resources']:
                fw.write(item + "\n")

        if OUT_PUT_LIST['add']:
            fw.write('\n\nHere is some new update:\n')
            for item in OUT_PUT_LIST['add']:
                fw.write(item + "\n")

        if OUT_PUT_LIST['vague']:
            fw.write('\nPlease identify carefully.\nVague update:')
            for item in OUT_PUT_LIST['vague']:
                if item.endswith(COMPLEX_HANDLE_FILE_TYPE):
                    fw.write("\n%s\n" % item)
                else:
                    fw.write("\t%s\n" % item)

    f = zipfile.ZipFile('%s_hoxfix-%s.zip' % (ctx, time.strftime("%Y%m%d%H%M")), 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(ctx):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()
    os.remove('diff.patch')
    shutil.rmtree(ctx)
    # 正常恢复现场
    if not unStash:
        os.system('git checkout %s' % curr_branch)
        os.system('git stash pop')


def handle_complex_file_type(sourceLine, pos):
    """
        处理复杂类型 COMPLEX_HANDLE_FILE_TYPE = ('.sql', '.properties', 'pom.xml', '.md')
        :param sourceLine: 原始diff处理行
        :param pos: 定位符

        :return pos: 下一次定位符
    """

    if sourceLine == 'pom.xml':
        #  全量复制jar
        if os.system('mvn dependency:copy-dependencies -DincludeScope=compile -DincludeScope=system '
                     '-DoutputDirectory=%s ' % (ctx + '/WEB-INF/lib')) != 0:
            raise RuntimeError('复制依赖失败 检查输出')
    else:
        with open('diff.patch', errors='ignore') as f:
            f.seek(pos)
            line = f.readline()
            if line.startswith('new file mode'):  # 新建文件
                with open(sourceLine, errors='ignore', encoding='utf-8') as nf:
                    OUT_PUT_LIST['add'].append(sourceLine)
                    for nfLine in nf.readlines():
                        OUT_PUT_LIST['add'].append('+' + nfLine)
            elif line.startswith('deleted file mode'):  # 删除文件
                pass
            elif line.startswith('similarity index'):  # 移动路径or更名
                pass
            else:  # 更新
                line = f.readline()
                OUT_PUT_LIST['vague'].append(sourceLine)
                while line:
                    if line.startswith('diff --git'):
                        break
                    if not line.startswith(('---', '+++', '@@')):  # 无效行跳过
                        line = line.strip()
                        if line.startswith('+') and line not in ('+', ''):
                            if sourceLine.endswith(('properties', 'yml')) and not line.startswith(('+#', '-#')):
                                OUT_PUT_LIST['vague'].append(line)
                            elif sourceLine.endswith('sql') and not line.startswith(('+-- ', '--- ')):
                                OUT_PUT_LIST['vague'].append(line)
                    pos = f.tell()
                    line = f.readline()
    return pos


def compile_workspace():
    """
    编译工作区 jdk8+maven3.x,
    针对eclipse项目和idea项目做不同路径查询处理
    """
    try:
        if not valider_path('pom.xml') == _FILE:
            pass
    except FileNotFoundError:
        raise RuntimeError('非MAVEN项目 无法编译工作区')

    # 找寻输出路径
    global CLASSPATH
    try:
        if valider_path('.classpath') == _FILE:
            for child in ET.parse('.classpath').getroot():
                if child.tag == 'classpathentry' and child.attrib['kind'] == 'output':
                    CLASSPATH = os.path.join(os.getcwd(), child.attrib['path'])
            pass
    except FileNotFoundError:
        try:
            if valider_path('%s.iml' % ctx) == _FILE:
                for child in ET.parse('%s.iml' % ctx).getroot():
                    if child.tag == 'component' and child.attrib['name'] == 'NewModuleRootManager':
                        output = child.find('output').attrib['url']
                        CLASSPATH = os.path.join(os.getcwd(),
                                                 output[output.find('/$MODULE_DIR$/') + len('/$MODULE_DIR$/'):])
        except FileNotFoundError:
            raise RuntimeError('非eclipse或IDEA项目 未找到.classpath文件或iml文件')

    if os.system('mvn clean compile -Dfile.encoding=UTF-8 -Dmaven.test.skip=true') != 0:
        raise RuntimeError('项目编译失败 检查配置')


def handle_src_main_resources(line):
    """
       basePath/src/main/resources ==> basePath/projectName/WEB-INF/classes
    :param line: 当前处理diff行
    """
    sourceFile = os.path.join(line)
    if valider_path(sourceFile) == _FILE:
        # e.g. E:\IdeaProjects\kbase-livemgr\kbase-livemgr\WEB-INF\classes
        subDir = 'WEB-INF/classes/' + line[len('src/main/resources/'): line.rfind('/') + 1]
        targetDir = os.path.join(ctx, subDir)
        try:
            os.makedirs(targetDir)
        except FileExistsError:
            pass
        shutil.copy(sourceFile, targetDir)
        OUT_PUT_LIST['resources'].append(subDir + os.path.basename(sourceFile))


def handle_src_main_webapp(line):
    """
       basePath/src/main/webapp ==> basePath/projectName/
    :param line: 当前处理diff行
    """
    sourceFile = os.path.join(line)

    if valider_path(sourceFile) == _FILE:
        # e.g. E:\IdeaProjects\kbase-livemgr\kbase-livemgr\
        subDir = line[len('src/main/webapp/'): line.rfind('/') + 1]
        targetDir = os.path.join(ctx, subDir)
        try:
            os.makedirs(targetDir)
        except FileExistsError:
            pass
        shutil.copy(sourceFile, targetDir)
        OUT_PUT_LIST['resources'].append('src/main/webapp/' + subDir + os.path.basename(sourceFile))


def handle_src_main_java(line):
    """
       basePath/src/main/java ==> basePath/projectName/WEB-INF/classes
    :param line: 当前处理diff行
    """
    # A.class
    baseClassName = line[line.rfind('/') + 1:line.rfind('.')]
    baseClassPath = os.path.join(CLASSPATH, line[len('src/main/java/'):line.rfind('/')])

    flag = False
    if valider_path(baseClassPath) == _DIR:
        for classFileName in os.listdir(baseClassPath):
            # A.class or A$B.class
            if classFileName.startswith(baseClassName):
                sourceFile = os.path.join(baseClassPath, classFileName)
                subDir = 'WEB-INF/classes/' + line[len('src/main/java/'): line.rfind('/') + 1]
                targetDir = os.path.join(ctx, subDir)
                try:
                    os.makedirs(targetDir)
                except FileExistsError:
                    pass
                flag = True
                shutil.copy(sourceFile, targetDir)
                if classFileName == baseClassName + '.class':
                    # 普通类
                    OUT_PUT_LIST['resources'].append(subDir + baseClassName + '.class')
                else:
                    # 内部类
                    OUT_PUT_LIST['resources'].append(subDir + classFileName)
    if not flag:
        raise FileNotFoundError()


def valider_path(sourcePath):
    """
    校验路径: 路径存在并且可读写
    :param sourcePath:
    :return: _FILE 文件 _DIR 文件夹
    """
    global _FILE
    _FILE = 1
    global _DIR
    _DIR = 2

    if os.path.exists(sourcePath):
        if os.access(sourcePath, os.R_OK) and os.access(sourcePath, os.W_OK):
            if os.path.isfile(sourcePath):
                return _FILE
            elif os.path.isdir(sourcePath):
                return _DIR
        else:
            raise RuntimeError('Promission Denied')
    else:
        raise FileNotFoundError


if __name__ == '__main__':
    # 解析参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--pname', type=str, default=None)
    parser.add_argument('--ocid', type=str, default=None)
    parser.add_argument('--ncid', type=str, default=None)
    args = parser.parse_args()

    if not args.ocid or not args.ncid:
        raise RuntimeError('参数指定不完整:--ocid(旧提交) --ncid(新提交) short hash index')

    start = time.process_time()

    try:
        starter(args.pname, args.ocid, args.ncid)
        cleaner(args.ocid, args.ncid)
    except:
        pass

    print('operation is success exit. used time : %ss' % (time.process_time() - start))
