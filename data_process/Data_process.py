from sqlalchemy import create_engine
import pandas as pd
import numpy as np


class DataProcess(object):
    __con = create_engine('mysql+pymysql://root:123456@localhost:3306/boss', encoding="UTF-8")
    __sql = "select * from 51table"
    df = pd.read_sql_query(__sql, __con)

    def __init__(self, con, sql, df):
        self.__con = con
        self.__sql = sql
        self.df = df
        pass

    def __del__(self):
        self.__con.close()

    #   元/小时	3
    # 	万/年	313
    # 	万/月	6224
    # 	万以上/年	1
    # 	万以上/月	 2
    # 	千以下/月	3
    # 	元/天	  19
    # 	千/月     895

    # 工资统一换成  万/月
    @staticmethod
    def trans_flag(full_value):
        if "元/天" in full_value:
            full_value = full_value.split("元/天")[0]
            # print(full_value)
            full_value = float(full_value) * 26 / 10000
        elif "万/年" in full_value:
            full_value = float(full_value.split("万/年")[0].split("-")[0]) / 12
        elif "万以上/年" in full_value:
            full_value = float(full_value.split("万以上/年")[0]) / 12
        elif "万以上/月" in full_value:
            full_value = float(full_value.split("万以上/月")[0])
        elif "千以下/月" in full_value:
            full_value = float(full_value.split("千以下/月")[0])
        elif "千/月" in full_value:
            full_value = full_value.split("千/月")[0]
            full_value = (float(full_value.split("-")[0]) + float(full_value.split("-")[1])) / (2 * 10)
        elif "元/小时" in full_value:
            full_value = float(full_value.split("元/小时")[0]) * 4 * 26 / 10000  # 每天工作四个小时，26天
        elif "万/月" in full_value:
            full_value = full_value.split("万/月")[0]
            full_value = (float(full_value.split("-")[0]) + float(full_value.split("-")[1])) / 2
        return full_value

    # 将工资为空替换为平均数
    @classmethod
    def replace_aver_with_null_salary(cls):
        cls.df["format_salary"] = cls.df["salary"].apply(cls.trans_flag)
        # 求平均工资
        aver_value = cls.df.loc[cls.df["format_salary"].apply(lambda x: x != ""), "format_salary"].sum() / \
                     (cls.df["format_salary"].count() - cls.df["format_salary"].apply(
                         lambda x: x == "").sum())  # 计算工资不为空的平均数

        # print(df.loc[df["format_salary"].apply(lambda x:x!=""),"format_salary"].sum())
        # print(aver_value)

        # 将工资为空替换为平均数
        def replace_null(value):
            return aver_value if value == "" else value

        cls.df["format_salary"] = cls.df["format_salary"].apply(replace_null)

    @classmethod
    # 对工资进行区域划分并分组统计
    def group_by_salary(cls):
        fs_data = cls.df["format_salary"]
        # print(fs_data.max())  100万/年
        # print(fs_data.min())   1-1.2万/年	  -->   0.08333333333333333
        # salary_range = list(range(0,int(fs_data.max()+2),1))  # 每月间隔在1万的分组
        salary_range = list(range(0, 12, 1))  # 区间[0,11)每月间隔在1万的分组的数量统计
        salary_group = pd.cut(fs_data.values, salary_range, right=False)
        # print(salary_group.codes)
        # print(salary_group.categories)
        # print(salary_group.value_counts(),type(salary_group))
        # [0, 1)      1119
        # [1, 2)      5162
        # [2, 3)      1004
        # [3, 4)       234
        # [4, 5)        47
        # [5, 6)        10
        # [6, 7)         6
        # [7, 8)         1
        # [8, 9)         2
        # [9, 10)        0
        # [10, 11)       3

        salary_group_df = pd.DataFrame(salary_group.value_counts(), columns=["counts"])
        salary_group_df["range"] = salary_group.categories
        salary_group_df["range"] = salary_group_df["range"].apply(lambda x: str(x))  # 将区间转为str，不然会报格式错误
        salary_group_df = salary_group_df[["range", "counts"]]
        # print(type(salary_group_df))
        salary_group_df.to_sql(name="salary_group_df", con=cls.__con, if_exists="replace", index=False)

    # 公司规模人数分组,统计
    @classmethod
    def group_by_company_size(cls):
        company_size_count = cls.df.groupby("company_size")["company_size"].count()
        company_size = cls.df.groupby("company_size").groups
        # print(company_size)
        company_size_df = pd.DataFrame()
        company_size_df["company_size"] = company_size
        company_size_df["company_size_count"] = company_size_count
        # print(company_size_df)
        company_size_df.to_sql(con=cls.__con, name="company_size_df", if_exists="replace", index=False)

    # 按学历，工作年限进行分组，统计统计招聘岗位的个数，并计算分组后各个组的工资的最小值，最大值，中位数，平均数
    @classmethod
    def company_require_analyze(cls):
        wy_de_sal_count = cls.df.groupby(["degree", "work_year"])["format_salary"].count()
        # print(wy_de_sal_group)
        wy_de_sal_group = cls.df.groupby(["degree", "work_year"]).groups
        wy_de_sal_calculate = cls.df.groupby(["degree", "work_year"])["format_salary"].agg(
            [np.min, np.max, np.median, np.mean])
        # print(wy_de_sal_group)
        wy_de_sal_group_df = pd.DataFrame()
        wy_de_sal_group_df["wy_de_sal_group"] = wy_de_sal_group
        wy_de_sal_group_df["wy_de_sal_count"] = wy_de_sal_count
        # for w in wy_de_sal_group:
        #     print(w)
        wy_de_sal_group_df["wy_de_sal_group"] = wy_de_sal_group_df["wy_de_sal_group"].apply(lambda x: str(x))
        wy_de_sal_group_df = wy_de_sal_group_df.sort_values(by="wy_de_sal_count", ascending=False)
        wy_de_sal_group_df[["salary_min", "salary_max", "salary_median", "salary_mean"]] = wy_de_sal_calculate
        print(wy_de_sal_group_df)
        wy_de_sal_group_df.to_sql(con=cls.__con, name="wy_de_sal_group_df", if_exists="replace", index=False)


if __name__ == "__main__":
    # dataProcess = DataProcess()
    DataProcess.replace_aver_with_null_salary()
    DataProcess.group_by_salary()
    DataProcess.group_by_company_size()
    DataProcess.company_require_analyze()
