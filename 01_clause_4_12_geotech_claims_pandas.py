import pandas as pd
from datetime import datetime

# 1. 模拟从现场系统导入的数据 (Mock Data)
# 实际工作中，这些数据来自读取现场的 Excel 文件： df = pd.read_excel('site_records.xlsx')
data = {
    'Panel_ID':['D-Wall-01', 'D-Wall-15', 'D-Wall-22', 'D-Wall-35', 'D-Wall-40'],
    'Obstacle_Type':['Soft Clay', 'Huge Boulder', 'Old Piles (旧桩基)', 'Gravel', 'Hard Rock'],
    'Event_Date':['2026-02-01', '2026-03-01', '2026-03-10', '2026-03-15', '2026-01-05'],
    'Notice_Date':['2026-02-05', '2026-04-05', '2026-03-12', '2026-03-16', '2026-03-01'], # 注意部分通知已超期
    'In_Geo_Report':[True, False, False, True, False],
    'Delay_Days': [0, 5, 12, 1, 8]
}

df = pd.DataFrame(data)
df['Event_Date'] = pd.to_datetime(df['Event_Date'])
df['Notice_Date'] = pd.to_datetime(df['Notice_Date'])

# 2. 定义向量化判定函数 (Pandas Vectorized Application)
def evaluate_claims_batch(row):
    days_lapsed = (row['Notice_Date'] - row['Event_Date']).days
    
    if days_lapsed > 28:
        return "Rejected: Time-bar (Clause 20)"
    elif row['In_Geo_Report']:
        return "Rejected: Foreseeable (Clause 4.12)"
    elif row['Delay_Days'] <= 0:
        return "Rejected: No Impact"
    else:
        return "Valid for EOT & Cost"

# 3. 自动执行分析并生成合规动作 (Execute and Generate Actionable Insights)
df['Claim_Status'] = df.apply(evaluate_claims_batch, axis=1)

print("--- 连续墙地质异常索赔自动化评估报告 (D-Wall Claim Automation Report) ---")
print(df[['Panel_ID', 'Obstacle_Type', 'Delay_Days', 'Claim_Status']])
