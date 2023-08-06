#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import itertools
import os

import pandas as pd
import ykenan_log
from pandas import DataFrame

from ykenan_file.util import str_list

logger = ykenan_log.Logger("ykenan_file", is_form_file=False)

'''
 * @Author       : YKenan
 * @Description  : file handler
'''


class Create:
    """
    初始化文件
    """

    def __init__(self, sep='\t',
                 line_terminator="\n",
                 encoding: str = 'utf_8_sig',
                 index: bool = False,
                 header: bool = True,
                 sheet_name='new_sheet'):
        """
        Initialization creation information, public information
        :param sep: File Separator
        :param line_terminator: File Line Break
        :param encoding: Document code
        :param index: Whether there is a row index
        :param header: Whether there is a title
        :param sheet_name: sheet name
        """
        self.sep = sep
        self.line_terminator = line_terminator
        self.encoding = encoding
        self.index = index
        self.header = header
        self.sheet_name = sheet_name

    def to_file(self, df: DataFrame, file: str) -> None:
        """
        :param df: DataFrame
        :param file: File path plus name
        """
        logger.debug(f"create a file: {file}")
        # 导出文件
        if str(file).endswith(".txt"):
            df.to_csv(file, sep=self.sep, lineterminator=self.line_terminator, header=self.header, encoding=self.encoding, index=self.index)
        elif str(file).endswith(".csv"):
            df.to_csv(file, sep=',', lineterminator=self.line_terminator, header=self.header, encoding=self.encoding, index=self.index)
        elif str(file).endswith(".xls") or str(file).endswith(".xlsx"):
            df.to_excel(file, sheet_name=self.sheet_name, header=self.header, index=self.index)
        else:
            with open(file, 'w', encoding='UTF-8') as f:
                df.to_string(f)

    def rename(self, df: DataFrame, columns: list, output_file: str = None) -> None:
        """
        Modify the file column name
        :param df: source document
        :param columns: New column name
        :param output_file: Output file path
        :return:
        """
        # 重新命名
        logger.debug(f"Modify the file column name: {columns}")
        df.columns = columns
        # 保存
        if output_file is not None:
            self.to_file(df, output_file)

    def drop_columns(self, df: DataFrame, columns: list, output_file: str = None) -> None:
        """
        Delete File Column Name
        :param df: source document
        :param columns: 删除的列名
        :param output_file: Output file path
        :return:
        """
        # 删除列
        logger.debug(f"删除文件列名: {columns}")
        df.drop(columns, axis=1, inplace=True)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_content(self, df: DataFrame, list_content: list, columns=None, is_log: bool = False, output_file: str = None) -> None:
        """
        向创建的文件添加内容
        :param df: DataFrame
        :param list_content: 一列的内容信息, 数组形式
        :param columns: 列信息
        :param output_file: Output file path
        :param is_log: 是否打印 log
        :return:
        """
        # 添加内容
        if columns is None:
            columns: list = list(df.columns)
        if is_log:
            logger.debug(f"添加内容 {list_content} ...")
        df.loc[len(df)] = pd.Series(list_content, index=columns)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_difference_column(self, df: DataFrame, column: str, a: str, b: str, output_file: str = None) -> None:
        """
        添加一个减法列 (column = a - b)
        :param df: DataFrame
        :param column: 添加的一个新列名
        :param a: 被减数
        :param b: 减数
        :param output_file: Output file path
        :return:
        """
        logger.debug(f"添加一个减法列: {column}")
        df[column] = df[a] - df[b]
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_rank_by_group(self, df: DataFrame, group: str_list, column: str, output_file: str = None) -> None:
        """
        添加五个 rank 列
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要秩的列
        :param output_file: Output file path
        :return:
        """
        logger.debug(f"添加五个 rank 列: {group}, {column}")
        # 添加排名
        for method in ['average', 'min', 'max', 'dense', 'first']:
            df[f'{method}_rank'] = df.groupby(group)[column].rank(method)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_sum_by_group(self, df: DataFrame, group: str_list, column: str, output_file: str = None) -> DataFrame:
        """
        通过分组计算某列数总和
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要和的列
        :param output_file: Output file path
        :return:
        """
        # 总和
        logger.debug(f"通过分组计算某列数总和: {group}, {column}")
        column_sum = df.groupby(group)[column].sum().reset_index()
        column_sum.columns = [group, f"{column}_sum"]
        # 保存文件
        if output_file is not None:
            self.to_file(column_sum, output_file)
        return column_sum

    def add_count_by_group(self, df: DataFrame, group: str_list, column: str, output_file: str = None) -> DataFrame:
        """
        通过分组计算某列数数量
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要数量的列
        :param output_file: Output file path
        :return:
        """
        # 总和
        logger.debug(f"通过分组计算某列数总和: {group}, {column}")
        column_sum = df.groupby(group)[column].count().reset_index()
        column_sum.columns = [group, f"{column}_count"]
        # 保存文件
        if output_file is not None:
            self.to_file(column_sum, output_file)
        return column_sum

    def add_calculation_by_group(self, df: DataFrame, group: str_list, column: str, output_file: str = None, add_merge_files: list = None):
        """
        通过分组进行一系列数值计算
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要秩的列
        :param output_file: Output file path
        :param add_merge_files: 添加 merge 文件
        :return:
        """
        # 总和
        logger.debug(f"通过分组进行一系列数值计算: {group}, {column}")
        # 个数大小
        column_size = df.groupby(group)[column].size().reset_index()
        column_size.columns = [group, f"{column}_size"]
        # 平均值
        column_mean = df.groupby(group)[column].mean().reset_index()
        column_mean.columns = [group, f"{column}_mean"]
        # 方差 (size == 1 的值为 NaN)
        column_var = df.groupby(group)[column].var().reset_index()
        column_var.columns = [group, f"{column}_var"]
        # 标准误差 (size == 1 的值为 NaN)
        column_sem = df.groupby(group)[column].sem().reset_index()
        column_sem.columns = [group, f"{column}_sem"]
        # 标准偏差 (size == 1 的值为 NaN)
        column_std = df.groupby(group)[column].std().reset_index()
        column_std.columns = [group, f"{column}_std"]
        # 中位数值
        column_median = df.groupby(group)[column].median().reset_index()
        column_median.columns = [group, f"{column}_median"]
        # 最小值
        column_min = df.groupby(group)[column].min().reset_index()
        column_min.columns = [group, f"{column}_min"]
        # 最大值
        column_max = df.groupby(group)[column].max().reset_index()
        column_max.columns = [group, f"{column}_max"]
        # 总和
        column_sum = self.add_sum_by_group(df, group, column)
        # 乘积
        column_prod = df.groupby(group)[column].prod().reset_index()
        column_prod.columns = [group, f"{column}_prod"]
        # 保存文件
        all_merge_files: list = [column_size, column_mean, column_var, column_sem, column_std,
                                 column_median, column_min, column_max, column_sum, column_prod]
        if output_file is not None:
            if add_merge_files is not None:
                all_merge_files.extend(add_merge_files)
                self.merge_files(all_merge_files, on=group, output_file=output_file)
            else:
                self.merge_files(all_merge_files, on=group, output_file=output_file)
        return all_merge_files

    def merge_files(self, files: list, on: str, output_file: str = None) -> None:
        """
        将文件进行合并
        :param files: 多个文件
        :param on: 关键 key
        :param output_file: Output file path
        :return:
        """
        # 总和
        size = len(files)
        logger.debug(f"将文件进行合并: {size}, {on}")
        new_file = files[0]
        i = 1
        while i < size:
            logger.debug(f"将文件进行合并第 {i} 次")
            new_file = pd.merge(new_file, files[i], on=on)
            i += 1
        # 保存文件
        if output_file is not None:
            self.to_file(new_file, output_file)


class Read:
    """
    Read file content
    """

    def __init__(self, sep='\t',
                 line_terminator="\n",
                 encoding: str = "utf-8",
                 orient: str = "records",
                 lines: bool = True,
                 header="infer",
                 sheet_name=0,
                 low_memory: bool = False):
        """
        Read file initialization information, public information
        :param sep: file separator
        :param line_terminator: file line break
        :param encoding: file encoding
        :param orient: Indicates the expected JSON string format, which is valid only when reading a json file
        :param lines: Read the file as a json object per line
        :param header: The first row header situation
        :param sheet_name: Specify the sheet number when reading Excel
        :param low_memory: Process files in internal chunks to reduce memory usage during parsing
        """
        self.sep = sep
        self.line_terminator = line_terminator
        self.encoding = encoding
        self.orient = orient
        self.lines = lines
        self.header = header
        self.sheet_name = sheet_name
        self.low_memory = low_memory

    def get_content(self, file: str):
        """
        Get file content
        :param file: File path information
        :return:
        """
        logger.debug(f"Start reading {file} file...")
        if str(file).endswith(".txt") or str(file).endswith(".bed"):
            return pd.read_table(file, sep=self.sep, header=self.header, encoding=self.encoding, low_memory=self.low_memory)
        elif str(file).endswith(".csv"):
            return pd.read_csv(file, sep=',', header=self.header, encoding=self.encoding, low_memory=self.low_memory)
        elif str(file).endswith(".xls") or str(file).endswith(".xlsx"):
            return pd.read_excel(file, sheet_name=self.sheet_name, header=self.header if isinstance(self.header, int) else 0)
        elif str(file).endswith(".html") or str(file).endswith(".htm"):
            return pd.read_html(file, header=self.header, encoding=self.encoding)
        elif str(file).endswith(".json"):
            return pd.read_json(file, orient=self.orient, lines=self.lines, encoding=self.encoding)

    def read_file(self, *files):
        """
        Read multiple files
        :param files:
        :return:
        """
        files_return = []
        for file in files:
            files_return.append(self.get_content(file))
        return files_return

    def file_concat_output(self, *files, output_file, join="inner", index=False, encoding="utf_8_sig"):
        """
        Merge two files and export the file
        :param files:
        :param output_file:
        :param join: How to merge files
        :param index:
        :param encoding: Encoding of output files
        :return:
        """
        file_content = self.read_file(*files)
        logger.debug(f"Start merging files {files} ...")
        pd_concat = pd.concat(file_content, join=join, ignore_index=True)
        pd.DataFrame(pd_concat).to_csv(output_file, encoding=encoding, sep=self.sep, index=index)


def read_file_line(path: str, mode: str = 'r', encoding: str = "utf-8") -> list:
    """
    Read file by line
    :param path:
    :param mode:
    :param encoding:
    :return:
    """
    content = []
    with open(path, mode, encoding=encoding) as f:
        while True:
            line = f.readline().strip()
            content.append(line)
            if not line:
                break
    return content


def write_file_line(path: str, content: list, line: str = '\n', mode: str = 'a', encoding: str = "utf-8") -> None:
    """
    Write a file (write by line, and it will not be cleared if the original file is called again by default)
    :param path:
    :param content:
    :param line:
    :param mode:
    :param encoding:
    :return:
    """
    with open(path, mode, encoding=encoding) as f:
        for li in content:
            f.write(li + line)


def read_write_line(path: str, output: str, callback, column=None, rm: str = 'r', om: str = 'w',
                    encoding: str = "utf-8", buffering: int = 1, newline: str = "\n") -> None:
    """
    Write one file to another
    :param column: Output column name
    :param path: Enter a path
    :param output: output path
    :param callback: A callback function that returns the input data
    :param rm: Read mode
    :param om: Output mode
    :param encoding: encoding
    :param buffering: Number of loaded lines in the output file
    :param newline: The newline character of the output file
    :return:
    """
    with open(output, om, encoding=encoding, buffering=buffering, newline=newline) as w:
        with open(path, rm, encoding=encoding) as f:
            if column:
                name: str = "\t".join(column)
                logger.debug(f"Add Column Name: {name}")
                w.write(f"{name}\n")
            while True:
                line: str = f.readline().strip()
                if not line:
                    break
                new_line: list = callback(line)
                if new_line and len(new_line) != 0 and new_line != "":
                    content = "\t".join(new_line)
                    w.write(f"{content}\n")


def get_contents(path: str) -> list:
    """
    Obtain all files and folders under the specified path
    :param path: path
    :return: files and folders
    """
    return list(os.listdir(path))


def entry_contents(path: str, type_: int = 0) -> list:
    """
    Obtain all files and (or) folders under the specified path
    :param path: path
    :param type_: judge file or dir
    :return: files and (or) folders
    """
    contents: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if type_ == 0:
                contents.append(entry.name)
            elif type_ == 1 and entry.is_file():
                contents.append(entry.name)
            elif type_ == 2 and entry.is_dir():
                contents.append(entry.name)
            else:
                raise ValueError("type input error, type is 0 or 1 or 2.")
    return contents


def entry_contents_path(path: str, type_: int = 0) -> list:
    """
    Obtain all files and (or) folders under the specified path
    :param path: path
    :param type_: judge file or dir
    :return: files and (or) folders path
    """
    contents: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if type_ == 0:
                contents.append(entry.path)
            elif type_ == 1:
                if entry.is_file():
                    contents.append(entry.path)
            elif type_ == 2:
                if entry.is_dir():
                    contents.append(entry.path)
            else:
                raise ValueError("type input error, type is 0 or 1 or 2.")
    return contents


def get_files(path: str) -> list:
    """
    Obtain all files in the specified path
    :param path:  path
    :return: files
    """
    files: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_file():
                files.append(entry.name)
    return files


def get_files_path(path: str) -> list:
    """
    Obtain all files in the specified path
    :param path:  path
    :return: files
    """
    files: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_file():
                files.append(entry.path)
    return files


def get_dirs(path: str) -> list:
    """
    Obtain all files in the specified path
    :param path:  path
    :return: files
    """
    dirs: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_dir():
                dirs.append(entry.name)
    return dirs


def get_dirs_path(path: str) -> list:
    """
    Obtain all files in the specified path
    :param path:  path
    :return: files
    """
    dirs: list = []
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_dir():
                dirs.append(entry.path)
    return dirs


def entry_contents_dict(path: str, type_: int = 0, suffix: str = None) -> dict:
    """
    Obtain all files in the specified path
    :param path: path
    :param type_: type_
    :param suffix: 筛选的条件
    :return: files and (or) dirs
    """
    files: list = []
    dirs: list = []
    contents: list = []
    dict_: dict = {}
    with os.scandir(path) as it:
        for entry in it:
            entry: os.DirEntry
            # 判断是否满足情况
            if suffix is None or entry.name.endswith(entry.name):
                if type_ == 0:
                    dict_ = dict(itertools.chain(dict_.items(), {
                        entry.name: entry.path
                    }.items()))
                    contents.append(entry.name)
                elif type_ == 1:
                    # 此处判断不能和 type_ == 1 连写，因为需要进行提示 ValueError("type input error, type is 0 or 1 or 2.")
                    if entry.is_file():
                        dict_ = dict(itertools.chain(dict_.items(), {
                            entry.name: entry.path
                        }.items()))
                        files.append(entry.name)
                elif type_ == 2:
                    if entry.is_dir():
                        dict_ = dict(itertools.chain(dict_.items(), {
                            entry.name: entry.path
                        }.items()))
                        dirs.append(entry.name)
                else:
                    raise ValueError("type input error, type is 0 or 1 or 2.")
    dict_ = dict(itertools.chain(dict_.items(), {
        "name": contents if type_ == 0 else files if type_ == 1 else dirs
    }.items()))
    return dict_


def entry_files_dict(path: str) -> dict:
    """
    Obtain all files in the specified path
    :param path: path
    :return: files
    """
    return entry_contents_dict(path, 1)


def entry_dirs_dict(path: str) -> dict:
    """
    Obtain all files in the specified path
    :param path: path
    :return: dirs
    """
    return entry_contents_dict(path, 2)
