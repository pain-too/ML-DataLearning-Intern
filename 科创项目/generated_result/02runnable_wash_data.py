#=================================把simplified_list变成processed1，剔除全None并报错前测和第一次重复的=========================
'''import pandas as pd
import numpy as np
import os

# 读取数据
file_path = '/Users/pc/Documents/GitHub/LLM-study-notes/科创项目/simplified_list.xlsx'
df = pd.read_excel(file_path)

# 定义列集合
schulte_cols = ['schulte_mean_pre', 'schulte_mean_1', 'schulte_mean_2',
                'schulte_mean_3', 'schulte_mean_4', 'schulte_mean_5',
                'schulte_mean_6', 'schulte_mean_7', 'schulte_mean_8']

stroop_cols = ['stroop_mean_pre', 'stroop_mean_1', 'stroop_mean_2',
               'stroop_mean_3', 'stroop_mean_4', 'stroop_mean_5',
               'stroop_mean_6', 'stroop_mean_7', 'stroop_mean_8']

# 检查列是否存在
print("检查列是否存在...")
for col in schulte_cols + stroop_cols:
    if col not in df.columns:
        print(f"警告: 列 '{col}' 不存在于数据中")


# 函数：从列名中提取时间点数字
def extract_time_point(col_name):
    """从列名中提取时间点数字，pre返回0，其他返回数字"""
    if 'pre' in col_name:
        return 0
    else:
        # 提取_mean_后面的数字
        import re
        match = re.search(r'_mean_(\d+)', col_name)
        if match:
            return int(match.group(1))
        else:
            return None


# 函数：检查重复数据并按照指定格式报错
def check_duplicates_with_format(df, test_cols, test_name):
    """
    检查同一受试者在不同时间点的数据是否重复，并按照指定格式报错

    参数:
    df: 数据框
    test_cols: 要检查的列列表
    test_name: 测试名称（用于输出信息）

    返回:
    duplicate_info: 重复数据的详细信息
    has_duplicates: 是否有重复数据
    """
    duplicate_info = []
    has_duplicates = False

    for index, row in df.iterrows():
        subject_id = row['id']
        subject_name = row['name']

        # 获取该受试者的测试数据
        test_data = row[test_cols].values

        # 创建一个字典来存储每个值对应的时间点
        value_to_timepoints = {}

        # 遍历所有时间点，建立值到时间点的映射
        for i, (col, val) in enumerate(zip(test_cols, test_data)):
            if pd.notna(val) and val != 0:
                time_point = extract_time_point(col)
                if time_point is not None:
                    if val not in value_to_timepoints:
                        value_to_timepoints[val] = []
                    value_to_timepoints[val].append(time_point)

        # 检查哪些值有重复的时间点
        for value, timepoints in value_to_timepoints.items():
            if len(timepoints) > 1:
                # 找到重复的时间点
                duplicate_times = sorted(timepoints)

                # 格式化时间点：0显示为"前测"，其他显示为数字
                formatted_times = []
                for t in duplicate_times:
                    if t == 0:
                        formatted_times.append("前测")
                    else:
                        formatted_times.append(str(t))

                # 按照要求格式报错
                if test_name == 'stroop':
                    print(f"id:{subject_id}，name:{subject_name}，第{','.join(formatted_times)}次数据重复，请检查")
                    has_duplicates = True
                elif test_name == 'schulte':
                    print(f"id:{subject_id}，name:{subject_name}，第{','.join(formatted_times)}次数据重复，请检查")

                duplicate_info.append({
                    'id': subject_id,
                    'name': subject_name,
                    'test_type': test_name,
                    'duplicate_value': value,
                    'duplicate_timepoints': duplicate_times,
                    'formatted_timepoints': formatted_times
                })

    return duplicate_info, has_duplicates


# 函数：检查并剔除无效数据
def remove_invalid_data(df, stroop_cols):
    """
    剔除stroop集所有数据都是0或None的id

    参数:
    df: 原始数据框
    stroop_cols: stroop测试的列名列表

    返回:
    filtered_df: 过滤后的数据框
    removed_ids: 被剔除的id列表
    """
    removed_ids = []
    valid_indices = []

    print("\n检查无效数据...")

    for index, row in df.iterrows():
        subject_id = row['id']
        subject_name = row['name']

        # 获取该受试者的stroop数据
        stroop_data = row[stroop_cols].values

        # 检查是否所有数据都是0或None
        all_invalid = True
        for val in stroop_data:
            if pd.notna(val) and val != 0:
                all_invalid = False
                break

        if all_invalid:
            removed_ids.append({
                'id': subject_id,
                'name': subject_name,
                'reason': 'stroop集所有数据都是0或None'
            })
            print(f"剔除无效数据: id:{subject_id}，name:{subject_name} - stroop集所有数据都是0或None")
        else:
            valid_indices.append(index)

    # 创建过滤后的数据框
    filtered_df = df.loc[valid_indices].copy().reset_index(drop=True)

    return filtered_df, removed_ids


print("=" * 60)
print("开始处理数据...")
print("=" * 60)

# 第一步：剔除无效数据
filtered_df, removed_ids = remove_invalid_data(df, stroop_cols)

print(f"\n共剔除了 {len(removed_ids)} 个无效数据记录")
print(f"剩余有效数据记录: {len(filtered_df)} 个")

# 第二步：检查重复数据
print("\n" + "=" * 60)
print("开始检查重复数据...")
print("=" * 60)

# 检查stroop集的重复数据
print("\n检查stroop集的重复数据:")
stroop_duplicates, stroop_has_duplicates = check_duplicates_with_format(filtered_df, stroop_cols, 'stroop')

if not stroop_has_duplicates:
    print("stroop集中未发现重复数据。")

# 检查schulte集的重复数据
print("\n检查schulte集的重复数据:")
schulte_duplicates, schulte_has_duplicates = check_duplicates_with_format(filtered_df, schulte_cols, 'schulte')

if not schulte_has_duplicates:
    print("schulte集中未发现重复数据。")

# 创建新文件（包含重复数据信息）
output_dir = os.path.dirname(file_path)
output_path = os.path.join(output_dir, 'processed_data.xlsx')

# 创建新的数据框，包含原始数据和重复标记
df_new = filtered_df.copy()

# 添加重复标记列
df_new['has_stroop_duplicates'] = False
df_new['has_schulte_duplicates'] = False
df_new['stroop_duplicate_info'] = ''
df_new['schulte_duplicate_info'] = ''

# 标记stroop重复
for dup in stroop_duplicates:
    idx = df_new[df_new['id'] == dup['id']].index
    if len(idx) > 0:
        df_new.loc[idx, 'has_stroop_duplicates'] = True
        current_info = df_new.loc[idx, 'stroop_duplicate_info'].values[0]
        new_info = f"值{dup['duplicate_value']}在时间点{dup['formatted_timepoints']}重复"
        if current_info:
            df_new.loc[idx, 'stroop_duplicate_info'] = current_info + "; " + new_info
        else:
            df_new.loc[idx, 'stroop_duplicate_info'] = new_info

# 标记schulte重复
for dup in schulte_duplicates:
    idx = df_new[df_new['id'] == dup['id']].index
    if len(idx) > 0:
        df_new.loc[idx, 'has_schulte_duplicates'] = True
        current_info = df_new.loc[idx, 'schulte_duplicate_info'].values[0]
        new_info = f"值{dup['duplicate_value']}在时间点{dup['formatted_timepoints']}重复"
        if current_info:
            df_new.loc[idx, 'schulte_duplicate_info'] = current_info + "; " + new_info
        else:
            df_new.loc[idx, 'schulte_duplicate_info'] = new_info

# 保存到新文件
df_new.to_excel(output_path, index=False)
print(f"\n处理后的数据已保存到: {output_path}")

# 创建处理报告
report_path = os.path.join(output_dir, 'data_processing_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("数据处理报告\n")
    f.write("=" * 50 + "\n\n")

    # 无效数据剔除报告
    f.write("1. 无效数据剔除情况:\n")
    f.write("-" * 30 + "\n")
    f.write(f"原始数据记录数: {len(df)}\n")
    f.write(f"剔除无效数据记录数: {len(removed_ids)}\n")
    f.write(f"剩余有效数据记录数: {len(filtered_df)}\n\n")

    if removed_ids:
        f.write("被剔除的ID列表:\n")
        for removed in removed_ids:
            f.write(f"  id:{removed['id']}，name:{removed['name']} - {removed['reason']}\n")
    else:
        f.write("未发现无效数据需要剔除。\n")

    f.write("\n" + "=" * 50 + "\n\n")

    # 重复数据检查报告
    f.write("2. 重复数据检查情况:\n")
    f.write("-" * 30 + "\n")

    if stroop_duplicates:
        f.write("STROOP测试重复数据汇总:\n")
        f.write(f"共发现 {len(stroop_duplicates)} 处重复数据\n\n")
        for dup in stroop_duplicates:
            f.write(f"id:{dup['id']}，name:{dup['name']}，第{','.join(dup['formatted_timepoints'])}次数据重复\n")
    else:
        f.write("STROOP测试: 未发现重复数据\n")

    f.write("\n")

    if schulte_duplicates:
        f.write("SCHULTE测试重复数据汇总:\n")
        f.write(f"共发现 {len(schulte_duplicates)} 处重复数据\n\n")
        for dup in schulte_duplicates:
            f.write(f"id:{dup['id']}，name:{dup['name']}，第{','.join(dup['formatted_timepoints'])}次数据重复\n")
    else:
        f.write("SCHULTE测试: 未发现重复数据\n")

    f.write("\n" + "=" * 50 + "\n\n")

    # 数据质量总结
    f.write("3. 数据质量总结:\n")
    f.write("-" * 30 + "\n")
    f.write(f"最终有效数据记录数: {len(df_new)}\n")
    f.write(f"有stroop重复数据的记录数: {df_new['has_stroop_duplicates'].sum()}\n")
    f.write(f"有schulte重复数据的记录数: {df_new['has_schulte_duplicates'].sum()}\n")

print(f"数据处理报告已保存到: {report_path}")

print("\n" + "=" * 60)
print("处理完成！")
print("=" * 60)
print(f"原始数据记录数: {len(df)}")
print(f"剔除无效数据后记录数: {len(filtered_df)}")
print(f"最终保存记录数: {len(df_new)}")
print("=" * 60)'''

#==========================把processed1变成processed2，检查四项数据是否有任意两个重复=================================
import pandas as pd
import numpy as np
import os

# 读取数据
file_path = '/Users/pc/Documents/GitHub/LLM-study-notes/科创项目/processed2_data.xlsx'
df = pd.read_excel(file_path)

print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print("\n前几行数据:")
print(df.head())

# 根据您的描述，确定要检查的列
# 第三列：schulte_mean_pre
# 第四列：schulte_mean_1
# 第八列：stroop_mean_pre
# 第九列：stroop_mean_1

# 获取列名
column_names = df.columns.tolist()
print(f"\n所有列名: {column_names}")

# 根据位置获取列名
if len(column_names) >= 9:
    schulte_pre_col = column_names[2]  # 第三列
    schulte_1_col = column_names[3]  # 第四列
    stroop_pre_col = column_names[7]  # 第八列
    stroop_1_col = column_names[8]  # 第九列

    print(f"\n要检查的列:")
    print(f"舒尔特前测: {schulte_pre_col}")
    print(f"舒尔特第1次: {schulte_1_col}")
    print(f"Stroop前测: {stroop_pre_col}")
    print(f"Stroop第1次: {stroop_1_col}")

    # 要检查的列列表
    check_cols = [schulte_pre_col, schulte_1_col, stroop_pre_col, stroop_1_col]

    # 检查这些列是否存在
    missing_cols = [col for col in check_cols if col not in df.columns]
    if missing_cols:
        print(f"\n错误: 以下列不存在: {missing_cols}")
    else:
        # 函数：检查同一行内四个数据是否有重复
        def check_same_row_duplicates(df, check_cols):
            """
            检查同一行内指定列的数据是否有任意两项重复

            参数:
            df: 数据框
            check_cols: 要检查的列列表

            返回:
            duplicate_rows: 有重复数据的行信息列表
            """
            duplicate_rows = []

            for index, row in df.iterrows():
                subject_id = row['id']
                subject_name = row['name']

                # 获取要检查的数据
                check_data = []
                for col in check_cols:
                    val = row[col]
                    # 只检查有效数据（非空且不为0）
                    if pd.notna(val) and val != 0:
                        check_data.append({
                            'column': col,
                            'value': val
                        })

                # 如果有至少2个有效数据，检查是否有重复
                if len(check_data) >= 2:
                    # 使用字典记录每个值出现的列
                    value_to_columns = {}

                    for item in check_data:
                        value = item['value']
                        column = item['column']

                        if value not in value_to_columns:
                            value_to_columns[value] = []
                        value_to_columns[value].append(column)

                    # 检查哪些值有重复
                    duplicate_values = {}
                    for value, columns in value_to_columns.items():
                        if len(columns) > 1:
                            duplicate_values[value] = columns

                    # 如果有重复值，记录信息
                    if duplicate_values:
                        # 提取列名中的测试类型和时间点
                        duplicate_details = []
                        for value, columns in duplicate_values.items():
                            # 格式化列名，使其更易读
                            formatted_cols = []
                            for col in columns:
                                # 简化列名显示
                                if 'schulte' in col:
                                    if 'pre' in col:
                                        formatted_cols.append('舒尔特前测')
                                    else:
                                        formatted_cols.append('舒尔特第1次')
                                elif 'stroop' in col:
                                    if 'pre' in col:
                                        formatted_cols.append('Stroop前测')
                                    else:
                                        formatted_cols.append('Stroop第1次')
                                else:
                                    formatted_cols.append(col)

                            duplicate_details.append({
                                'value': value,
                                'columns': columns,
                                'formatted_columns': formatted_cols
                            })

                        duplicate_rows.append({
                            'id': subject_id,
                            'name': subject_name,
                            'row_index': index,
                            'duplicate_details': duplicate_details,
                            'has_duplicates': True
                        })

            return duplicate_rows


        # 检查重复数据
        print("\n" + "=" * 60)
        print("开始检查同一行内的重复数据...")
        print("=" * 60)

        duplicate_rows = check_same_row_duplicates(df, check_cols)

        if duplicate_rows:
            print(f"发现 {len(duplicate_rows)} 个受试者有行内重复数据:\n")

            for dup in duplicate_rows:
                print(f"id:{dup['id']}，name:{dup['name']}")

                for detail in dup['duplicate_details']:
                    columns_str = "、".join(detail['formatted_columns'])
                    print(f"  值 {detail['value']} 在 {columns_str} 中重复")
                print()
        else:
            print("未发现同一行内的重复数据。")

        # 创建新文件，添加重复标记
        output_dir = os.path.dirname(file_path)
        output_path = os.path.join(output_dir, 'processed2_wash.xlsx')

        # 创建新数据框
        df_new = df.copy()

        # 添加重复标记列
        df_new['has_same_row_duplicates'] = False
        df_new['same_row_duplicate_info'] = ''

        # 标记有重复数据的行
        for dup in duplicate_rows:
            idx = dup['row_index']
            df_new.loc[idx, 'has_same_row_duplicates'] = True

            # 构建重复信息字符串
            dup_info_parts = []
            for detail in dup['duplicate_details']:
                columns_str = "、".join(detail['formatted_columns'])
                dup_info_parts.append(f"值{detail['value']}在{columns_str}重复")

            df_new.loc[idx, 'same_row_duplicate_info'] = "; ".join(dup_info_parts)

        # 保存到新文件
        df_new.to_excel(output_path, index=False)
        print(f"\n处理后的数据已保存到: {output_path}")

        # 创建详细报告
        report_path = os.path.join(output_dir, 'same_row_duplicate_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("同一行内重复数据检查报告\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"检查的列: {', '.join(check_cols)}\n")
            f.write(f"总数据行数: {len(df)}\n")
            f.write(f"发现重复数据的行数: {len(duplicate_rows)}\n\n")

            if duplicate_rows:
                f.write("重复数据详情:\n")
                f.write("-" * 30 + "\n")

                for dup in duplicate_rows:
                    f.write(f"id: {dup['id']}, name: {dup['name']}\n")

                    for detail in dup['duplicate_details']:
                        columns_str = "、".join(detail['formatted_columns'])
                        f.write(f"  值 {detail['value']} 在 {columns_str} 中重复\n")
                    f.write("\n")
            else:
                f.write("未发现同一行内的重复数据。\n")

        print(f"详细报告已保存到: {report_path}")

        # 统计信息
        print("\n" + "=" * 60)
        print("统计信息:")
        print(f"总数据行数: {len(df)}")
        print(f"有行内重复数据的行数: {len(duplicate_rows)}")
        print(f"无重复数据的行数: {len(df) - len(duplicate_rows)}")
        print("=" * 60)

else:
    print(f"错误: 数据列数不足，只有 {len(column_names)} 列，但需要至少9列")

print("\n处理完成！")