import os
import yaml

# 获取当前脚本（convert.py）所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# Surge 规则目录（根目录的 Surge/rules/）
input_folder = os.path.abspath(os.path.join(script_dir, "../Surge/rules"))

# Clash 规则目录（直接存放到 Clash/ 目录）
output_folder = script_dir  # 直接存放到 Clash 根目录

def convert_surge_to_clash(input_file, output_file):
    rules = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # 跳过空行和注释
            
            # 规则转换
            if line.startswith("DOMAIN-SUFFIX,"):
                rules.append("  - DOMAIN-SUFFIX," + line.split(",")[1])
            elif line.startswith("DOMAIN,"):
                rules.append("  - DOMAIN," + line.split(",")[1])
            elif line.startswith("IP-CIDR,"):
                rules.append("  - IP-CIDR," + line.split(",")[1])
            elif line.startswith("GEOIP,"):
                rules.append("  - GEOIP," + line.split(",")[1])
            elif line.startswith("MATCH"):
                rules.append("  - MATCH")
            else:
                rules.append("  # 未识别规则: " + line)

    # 生成 Clash YAML 规则文件
    yaml_content = {
        "payload": rules
    }
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_content, f, allow_unicode=True, default_flow_style=False)

# 遍历 Surge/rules 目录中的所有 .list 文件
for filename in os.listdir(input_folder):
    if filename.endswith(".list"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".list", ".yaml"))  # 直接存到 Clash 目录
        convert_surge_to_clash(input_path, output_path)
        print(f"Converted {filename} -> {output_path}")
