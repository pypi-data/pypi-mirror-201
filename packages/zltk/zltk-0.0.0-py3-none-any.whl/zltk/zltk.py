import json
from typing import Callable, List, Literal
import yaml
import numpy as np


def load_lines(file, remove_empty=True, strip_space=False):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if strip_space:
        lines = [line.strip() for line in lines]
    else:
        lines = [line.strip('\n') for line in lines]
    if remove_empty:
        lines = list(filter(None, lines))
    return lines


def store_lines(lines, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def store_json(obj, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    return obj


def store_yaml(obj, file):
    with open(file, 'w') as f:
        yaml.safe_dump(dict(obj), f)


"""简易的并行处理"""

pbars = []  # 并行处理的进度条


def equal_split(all_items, all_ids, n, split_manner):
    """将all_items, all_ids均分成块，每块的形式都是[(id,item),...]"""
    total = len(all_items)
    if all_ids == None:
        all_ids = list(range(total))
    assert split_manner in ['chunk', 'turn']
    if split_manner == 'chunk':
        indices = np.array_split(range(total), n)
    elif split_manner == 'turn':
        indices = [list(range(total)[i::n]) for i in range(n)]
    items = [[(all_ids[i], all_items[i]) for i in inds] for inds in indices]  # (id, doc)
    return items


def single_run_cpu(func, num_proc, docs):
    """用func逐一处理docs"""
    docs, pos = docs
    # pos = multiprocessing.current_process()._identity[0] - 1  # 0,1,2..., 但每次运行的Pool都会累加
    res = []
    if pos == 0 or pos == num_proc-1:
        pbar = pbars[0 if pos == 0 else 1]  # 只显示第一个和最后一个进程的进度条
        for id, doc in docs:
            res.append(func(doc))
            pbar.update()
    else:
        for id, doc in docs:
            res.append(func(doc))
    return res


def parallel_run(func: Callable, all_docs: List, num_proc: int, split_manner: Literal['chunk', 'turn']):  # all_doc是一个list, func对一个doc做处理
    """并行处理

    Args:
        func: 对一个doc做处理的函数
        all_docs: 所有需要被处理的doc
        num_proc: 进程数量
        split_manner: chunk/turn 分块分配/轮流分配

    Return:
        当func不是模型批量处理时，返回结果等价于 [func(doc) for doc in all_docs]
        当func是模型批量处理时，返回结果类似，只不过func是批量处理的
    """
    import functools
    from tqdm import tqdm
    import multiprocessing
    global pbars
    num_proc = min(num_proc, len(all_docs))
    split_docs = equal_split(all_docs, None, num_proc, split_manner)

    single_run = single_run_cpu
    pbars = [tqdm(total=len(docs), desc=str(docs[0][0]).rjust(5, '0'), position=pos) for pos, docs in enumerate(split_docs[:1]+split_docs[-1:])]

    results = []
    with multiprocessing.Pool(num_proc) as p:
        pids = list(range(num_proc))
        assert len(pids) == len(split_docs)
        for single_res in p.imap(functools.partial(single_run, func, num_proc), list(zip(split_docs, pids))):
            results.extend(single_res)
    print('\n'*4)
    return results
