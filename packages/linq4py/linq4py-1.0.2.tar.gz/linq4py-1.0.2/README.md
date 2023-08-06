# Linq for Python

像C#或JavaScript一样链式写python

## 1 代码说明
代码Fork `https://pypi.org/project/py-linq/`

## 2 新增功能
- 新增：`filter`,`map`,`find`等类似于JavaScript`filter`,`map`,`find`
- 使用函数式入口来初始化列表`linq4py.array()`

## 3 举例

```
import linq4py as lp

origin_items = [
    {'id': '1', 'parent_id': '', 'name': 'indicator 1', 'weight': 1, 'has_child': True},
    {'id': '2', 'parent_id': '1', 'name': 'indicator 2', 'weight': 0.6, 'has_child': True},
    {'id': '3', 'parent_id': '1', 'name': 'indicator 3', 'weight': 0.4, 'has_child': True},
    {'id': '4', 'parent_id': '2', 'name': 'indicator 4', 'weight': 0.5, 'has_child': False},
    {'id': '5', 'parent_id': '2', 'name': 'indicator 5', 'weight': 0.8, 'has_child': False},
    {'id': '6', 'parent_id': '3', 'name': 'indicator 6', 'weight': 0.8, 'has_child': False},
    {'id': '7', 'parent_id': '3', 'name': 'indicator 7', 'weight': 0.8, 'has_child': False},
]


# count demo
count = lp.array(origin_items).count(lambda item: item['has_child'])
print(count)

# filter,order_by_descending map demo
items = lp.array(origin_items).filter(lambda item: item["has_child"]).order_by_descending(
    lambda item: item['weight']).map(lambda item: (item['id'], item['name']))
print(items)

# find demo
result = lp.array(origin_items).find(lambda item: item['weight'] > 0.3)
print(result)

```

## 4 修改日志

- 2023-04-08 重新打包
- 2023-04-08 Fork项目并新增相关功能