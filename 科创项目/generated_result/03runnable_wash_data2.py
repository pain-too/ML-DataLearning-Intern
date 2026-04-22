import pandas as pd
import numpy as np
import os
file_path = '/Users/pc/Desktop/single_comparison/simplified_list.xlsx'
df = pd.read_excel(file_path)

print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print("\n前几行数据:")
print(df.head())

# 根据之前的描述，定义列结构
# 舒尔特测试列：第3列到第11列
# Stroop测试列：第13列到第21列

# 获取所有列名
all_columns = df.columns.tolist()
print(f"\n所有列名: {all_columns}")

# 定义舒尔特测试列（8次测试 + 前测）
schulte_cols = []
for i in range(1, 9):  # 1到8
    col_name = f'schulte_mean_{i}'
    if col_name in df.columns:
        schulte_cols.append(col_name)
    else:
        print(f"警告: 列 '{col_name}' 不存在")

# 添加前测列
if 'schulte_mean_pre' in df.columns:
    schulte_cols.insert(0, 'schulte_mean_pre')
else:
    print("警告: 列 'schulte_mean_pre' 不存在")

print(f"\n舒尔特测试列: {schulte_cols}")

# 定义Stroop测试列（8次测试 + 前测）
stroop_cols = []
for i in range(1, 9):  # 1到8
    col_name = f'stroop_mean_{i}'
    if col_name in df.columns:
        stroop_cols.append(col_name)
    else:
        print(f"警告: 列 '{col_name}' 不存在")

# 添加前测列
if 'stroop_mean_pre' in df.columns:
    stroop_cols.insert(0, 'stroop_mean_pre')
else:
    print("警告: 列 'stroop_mean_pre' 不存在")

print(f"Stroop测试列: {stroop_cols}")

# 检查列是否存在
if len(schulte_cols) < 9 or len(stroop_cols) < 9:
    print("错误: 测试列不完整，无法继续处理")
else:
    # 函数：为每个测试类型找到第一个有效值
    def find_first_valid_value(row, test_cols):
        """
        在给定的测试列中寻找第一个有效值（非0且非None）

        参数:
        row: 数据行
        test_cols: 测试列列表

        返回:
        valid_value: 第一个有效值，如果都无效则返回None
        source_col: 有效值来源的列名
        """
        for col in test_cols:
            value = row[col]
            if pd.notna(value) and value != 0:
                return value, col
        return None, None


    # 函数：检查18次数据是否均互异
    def check_all_values_unique(row, schulte_test_cols, stroop_test_cols):
        """
        检查某个id下的18次数据是否全部互异

        参数:
        row: 数据行
        schulte_test_cols: 舒尔特测试列（包含前测）
        stroop_test_cols: Stroop测试列（包含前测）

        返回:
        is_unique: 是否全部互异
        duplicates: 重复信息列表
        """
        # 收集所有有效值
        all_values = []
        value_sources = []  # 记录每个值的来源

        # 收集舒尔特测试值
        for col in schulte_test_cols:
            value = row[col]
            if pd.notna(value) and value != 0:
                all_values.append(value)
                # 提取测试次数
                if 'pre' in col:
                    source = f"舒尔特前测"
                else:
                    match_num = col.split('_')[-1]
                    source = f"舒尔特第{match_num}次"
                value_sources.append((value, source))

        # 收集Stroop测试值
        for col in stroop_test_cols:
            value = row[col]
            if pd.notna(value) and value != 0:
                all_values.append(value)
                # 提取测试次数
                if 'pre' in col:
                    source = f"Stroop前测"
                else:
                    match_num = col.split('_')[-1]
                    source = f"Stroop第{match_num}次"
                value_sources.append((value, source))

        # 检查是否有重复值
        from collections import Counter
        value_counts = Counter(all_values)

        duplicates = []
        for value, count in value_counts.items():
            if count > 1:
                # 找到这个值出现的所有位置
                sources = [source for val, source in value_sources if val == value]
                duplicates.append({
                    'value': value,
                    'count': count,
                    'sources': sources
                })

        return len(duplicates) == 0, duplicates


    # 创建新数据框
    new_data = []

    print("\n" + "=" * 60)
    print("开始处理数据...")
    print("=" * 60)

    # 处理每一行数据
    for index, row in df.iterrows():
        subject_id = row['id']
        subject_name = row['name']

        # 为舒尔特测试找到第一个有效值
        schulte_valid_value, schulte_source_col = find_first_valid_value(row, schulte_cols[1:])  # 从前测之后开始找

        # 为Stroop测试找到第一个有效值
        stroop_valid_value, stroop_source_col = find_first_valid_value(row, stroop_cols[1:])  # 从前测之后开始找

        # 创建新行数据
        new_row = {
            'id': subject_id,
            'name': subject_name
        }

        # 添加舒尔特的8次结果
        for i in range(1, 9):
            col_name = f'schulte_mean_{i}'
            if col_name in df.columns:
                value = row[col_name]
                if pd.notna(value) and value != 0:
                    new_row[f'schulte_result_{i}'] = value
                else:
                    new_row[f'schulte_result_{i}'] = None

        # 添加Stroop的8次结果
        for i in range(1, 9):
            col_name = f'stroop_mean_{i}'
            if col_name in df.columns:
                value = row[col_name]
                if pd.notna(value) and value != 0:
                    new_row[f'stroop_result_{i}'] = value
                else:
                    new_row[f'stroop_result_{i}'] = None

        new_data.append(new_row)

    # 创建新数据框
    df_new = pd.DataFrame(new_data)

    # 保存新文件
    output_dir = os.path.dirname(file_path)
    output_path = os.path.join(output_dir, 'processed_valid_data.xlsx')
    df_new.to_excel(output_path, index=False)

    print(f"\n新文件已保存到: {output_path}")
    print(f"新文件形状: {df_new.shape}")
    print(f"新文件列名: {df_new.columns.tolist()}")

    # 检查每个id的18次数据是否均互异
    print("\n" + "=" * 60)
    print("检查18次数据是否均互异...")
    print("=" * 60)

    # 定义要检查的测试列（18次数据：9次舒尔特 + 9次Stroop，都包含前测）
    all_test_cols = schulte_cols + stroop_cols

    for index, row in df.iterrows():
        subject_id = row['id']

        # 检查该id下的所有测试数据
        is_unique, duplicates = check_all_values_unique(row, schulte_cols, stroop_cols)

        if not is_unique and duplicates:
            # 构建重复信息字符串
            duplicate_info_parts = []

            for dup in duplicates:
                # 对重复的来源进行分组
                sources = dup['sources']
                if len(sources) > 1:
                    # 将来源按测试类型分组
                    schulte_sources = [s for s in sources if '舒尔特' in s]
                    stroop_sources = [s for s in sources if 'Stroop' in s]

                    # 处理舒尔特重复
                    if len(schulte_sources) > 1:
                        # 提取次数信息
                        times = []
                        for source in schulte_sources:
                            if '前测' in source:
                                times.append('前测')
                            else:
                                # 提取数字
                                import re

                                match = re.search(r'第(\d+)次', source)
                                if match:
                                    times.append(match.group(1))

                        if times:
                            times_str = '、'.join(times)
                            duplicate_info_parts.append(f"舒尔特{times_str}")

                    # 处理Stroop重复
                    if len(stroop_sources) > 1:
                        # 提取次数信息
                        times = []
                        for source in stroop_sources:
                            if '前测' in source:
                                times.append('前测')
                            else:
                                # 提取数字
                                import re

                                match = re.search(r'第(\d+)次', source)
                                if match:
                                    times.append(match.group(1))

                        if times:
                            times_str = '、'.join(times)
                            duplicate_info_parts.append(f"Stroop{times_str}")

                    # 处理跨测试类型重复
                    if schulte_sources and stroop_sources:
                        schulte_times = []
                        for source in schulte_sources:
                            if '前测' in source:
                                schulte_times.append('前测')
                            else:
                                import re

                                match = re.search(r'第(\d+)次', source)
                                if match:
                                    schulte_times.append(match.group(1))

                        stroop_times = []
                        for source in stroop_sources:
                            if '前测' in source:
                                stroop_times.append('前测')
                            else:
                                import re

                                match = re.search(r'第(\d+)次', source)
                                if match:
                                    stroop_times.append(match.group(1))

                        if schulte_times and stroop_times:
                            schulte_str = '、'.join(schulte_times)
                            stroop_str = '、'.join(stroop_times)
                            duplicate_info_parts.append(f"舒尔特{schulte_str}与Stroop{stroop_str}")

            if duplicate_info_parts:
                print(f"{subject_id}: {'，'.join(duplicate_info_parts)}重复")

    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)
