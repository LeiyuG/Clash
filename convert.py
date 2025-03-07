import os
import yaml

# 目标文件夹
input_folder = "Surege/rules"
output_folder = "Clash"

# 确保输出目录存在
os.makedirs(output_folder, exist_ok=True)

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
            else:
                rules.append("  # 未识别规则: " + line)

    # 生成 Clash YAML 规则文件
    yaml_content = {
        "payload": rules
    }
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_content, f, allow_unicode=True, default_flow_style=False)

# 遍历 surge_list 目录中的所有 .list 文件
for filename in os.listdir(input_folder):
    if filename.endswith(".list"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".list", ".yaml"))
        convert_surge_to_clash(input_path, output_path)
        print(f"Converted {filename} -> {output_path}")
