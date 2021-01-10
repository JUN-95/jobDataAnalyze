import pandas as pd
import numpy as np
from datetime import datetime

sales_people = {"陈天浩": "上海",
                "孙健": "上海",
                "王梓戎": "广东",
                "刘丹": "上海",
                "刘颖": "上海",
                "刘雪": "天津",
                "章洋": "上海",
                "殷琳": "广东",
                "李辉": "北京",
                "王玉": "吉林",
                "侯宁": "上海",
                "吴中岳": "广东",
                "张林": "广东",
                "庄雷": "上海",
                "王宇": "吉林",
                "利坤": "上海",
                "董丹丹": "广东",
                "蔡建平": "山东",
                "陈杨": "吉林",
                "蔡勇": "广东",
                "李琳": "上海",
                "魏苍生": "天津",
                "刘帆": "天津",
                "戴雪": "上海",
                "许亮": "吉林",
                "李智童": "山东",
                "钱国": "山东",
                "郭华锋": "吉林",
                "阎云": "山东",
                "江敏": "上海"}

products = {"苹果": 10,
            "梨": 8,
            "桃": 6.5,
            "葡萄": 15,
            "椰子": 20,
            "西瓜": 30,
            "百香果": 12,
            "榴莲": 50,
            "桔子": 6,
            "香蕉": 7.5}


def random_dater(start_date, end_date):
    p_start_date = datetime.strptime(start_date, '%Y-%m-%d')
    p_end_date = datetime.strptime(end_date, '%Y-%m-%d')

    days_delta = p_end_date - p_start_date
    days_to_add = np.arange(0, days_delta.days)

    random_date = np.datetime64(
        start_date) + np.random.choice(days_to_add)  # numpy 也可以转换日期

    return random_date


sales0 = pd.DataFrame(
    columns=["交易日期", "客户ID", "售货员", "分公司", "产品", "单价", "数量", "订单金额"])

for i in range(0, 10000):
    date = random_dater('2019-01-01', '2019-12-31')
    customer_id = "C" + str(np.random.randint(1, 1000)).zfill(4)
    sales_person = np.random.choice(list(sales_people))
    region = sales_people[sales_person]
    product = np.random.choice(list(products))
    price = products[product]
    quantity = np.random.randint(1, 10000)
    revenue = price * quantity
    sales0 = sales0.append(pd.Series([date, customer_id, sales_person,
                                      region, product, price, quantity, revenue], index=sales0.columns),
                           ignore_index=True)

print(sales0)
