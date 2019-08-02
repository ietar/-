__author__ = 'ietar'

import random


def distribution(total=200, n=10, deviation=2, **kw):
    """Divide the total amount into n parts(return a generator).
Small probability event probability is reduced (controlled by deviation).
"""
    for _ in kw:
        pass
    if deviation <= 1:
        raise ValueError('deviation must be greater than 1')
    
    while n > 1:
        base = total/n
        res = base
        temp = 1
        while random.random() < temp:
            base /= deviation
            alter = random.choice((-1, 1)) * base * random.random() 
            if res + alter < 0:
                break
            res += alter
            temp /= deviation
        n -= 1
        total -= res
        yield round(res, 2)
        
    if n == 1:
        yield round(total, 2)


def ldistribution(**kw):
    """return list of distribution()"""
    return list(distribution(**kw))


def test_over_twice(total=200, n=10, deviation=2, rate=2):
    """测试小概率事件"""
    overmax = rate * total / n
    overmin = total/n/2/rate
    count = 1
    while 1:
        index = 1
        for i in distribution(total=total, n=n, deviation=deviation):
            if i > overmax or i < overmin:
                # print('出现了越界值{},在第{}次的第{}个'.format(i, count, index))
                return i, count, index
            index += 1
        count += 1


def test2():
    collect_i = []
    collect_count = []
    collect_index = dict.fromkeys(range(1, 11))
    for i in collect_index:
        collect_index[i] = 0
    for _ in range(1000):
        res = test_over_twice()
        collect_i.append(res[0])
        collect_count.append(res[1])
        collect_index[res[2]] += 1
    assert len(collect_i) == 1000
    assert len(collect_count) == 1000
    assert sum(list(collect_index.values())) == 1000
    
    return collect_i, collect_count, collect_index


if __name__ == '__main__':
    test_res = test2()
