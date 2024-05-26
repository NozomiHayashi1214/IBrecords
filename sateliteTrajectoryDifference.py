import json
import decimal
from decimal import Decimal, getcontext
import os

# 有効数字を200桁に設定
getcontext().prec = 200

# 親データのパス
parent_path = "EE/Records/dt0.1d30/satellite_trajectory.json"

# 子データのディレクトリ（ここを変数で変更可能にする）
offset = "+100"  # 例として+100を使用
child_dir = f"EE/Records/dt0.1d30{offset}"
child_path = os.path.join(child_dir, "satellite_trajectory.json")

# 出力するJSONファイルのパス（子データと同じディレクトリに保存）
output_path = os.path.join(child_dir, "difference_trajectory.json")

# JSONファイルを読み込む関数
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# JSONファイルを保存する関数
def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# 親データと子データを読み込み
parent_data = load_json(parent_path)
child_data = load_json(child_path)

# 差を計算して新しいリストを作成
difference_data = []

for parent, child in zip(parent_data, child_data):
    if parent["time"] != child["time"]:
        raise ValueError(f"Time mismatch at time {parent['time']} and {child['time']}")
    
    time = Decimal(parent["time"])
    x_diff = Decimal(parent["x"]) - Decimal(child["x"])
    y_diff = Decimal(parent["y"]) - Decimal(child["y"])
    z_diff = Decimal(parent["z"]) - Decimal(child["z"])
    
    difference_data.append({
        "time": str(time),
        "x": str(x_diff),
        "y": str(y_diff),
        "z": str(z_diff)
    })

# 新しいJSONファイルに保存
save_json(difference_data, output_path)

print(f"Differences calculated and saved to {output_path}")
