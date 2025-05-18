import os
root = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(root, "Raw.proto"), "r", encoding="utf-8") as f:
    proto_content = f.readlines()

with open(os.path.join(root, "NT.txt"), "r", encoding="utf-8") as f:
    nt_content = f.readlines()
    nt_dict = {}
    for line in nt_content:
        line = line.strip().split(" => ")
        nt_dict[line[0]] = line[1]

def main():
    result = []
    for line in proto_content:
        # keep old tab
        indent = ""
        line_rstrip = line.rstrip()
        for c in line_rstrip:
            if c in [' ', '\t']:
                indent += c
            else:
                break

        parts = line_rstrip[len(indent):].split(" ")
        for i, part in enumerate(parts):
            if part in nt_dict:
                parts[i] = nt_dict[part]

        result.append(indent + " ".join(parts) + "\n")

    with open(os.path.join(root, "WutheringWaves.proto"), "w", encoding="utf-8") as f:
        f.writelines(result)

if __name__ == "__main__":
    main()