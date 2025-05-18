import os
root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root, "Raw.proto"), "r", encoding="utf-8") as f:
    obf_content = f.readlines()

with open(os.path.join(root, "Contrast.proto"), "r", encoding="utf-8") as f:
    contrast_content = f.readlines()

SYS_LIST = [
    "double",
    "float",
    "int32",
    "int64",
    "uint32",
    "uint64",
    "sint32",
    "sint64",
    "fixed32",
    "fixed64",
    "sfixed32",
    "sfixed64",
    "bool",
    "string",
    "bytes",
    "oneof",
    "map",
    "repeated",
    "optional",
    "required",
    "message",
    "enum"
]

def get_structs(content):
    structs = []
    cur_nest = 0
    flag = False
    cur_struct = []
    for line in content:
        if "//" in line or line.strip() == "":
            continue

        if "{" in line:
            cur_nest += 1
            if cur_nest == 1:
                flag = True

        if flag:
            cur_struct.append(line.strip())

        if "}" in line:
            cur_nest -= 1
            if cur_nest == 0:
                flag = False
                structs.append(cur_struct)
                cur_struct = []

    return structs

def verify_num(list1, list2):
    if len(list1) != len(list2):
        print(str(len(list1)) + " " + str(len(list2)))
        return -1
    return len(list1)

nt_dict = {}
def add_nt(obf_part, contrast_part):
    if obf_part not in nt_dict:
        nt_dict[obf_part] = contrast_part
    else:
        if nt_dict[obf_part] != contrast_part:
            print("conflict at " + obf_part + " : " + nt_dict[obf_part] + " " + contrast_part)

def main():
    # get structs to list
    obf_structs = get_structs(obf_content)
    contrast_structs = get_structs(contrast_content)
    struct_num = verify_num(obf_structs, contrast_structs)
    if struct_num == -1:
        print("struct num not same")
        return

    # for each struct
    for struct_index in range(struct_num):
        obf_struct = obf_structs[struct_index]
        contrast_struct = contrast_structs[struct_index]

        # check line num in struct
        struct_line_num = verify_num(obf_struct, contrast_struct)
        if struct_line_num == -1:
            print(obf_struct)
            print(contrast_struct)
            print("line num in struct not same")
            return

        # for each line in struct
        for line_index in range(struct_line_num):
            obf_parts = obf_struct[line_index].split(" ")
            contrast_parts = contrast_struct[line_index].split(" ")
            part_num = verify_num(obf_parts, contrast_parts)
            if part_num == -1:
                print(obf_struct)
                print(contrast_struct)
                print("part num not same")
                return

            # for each part in line
            for part_index in range(part_num):
                if (obf_parts[part_index] != contrast_parts[part_index]
                and obf_parts[part_index] not in SYS_LIST and obf_parts[part_index] not in SYS_LIST):
                    add_nt(obf_parts[part_index], contrast_parts[part_index])

    with open(os.path.join(root, "NT.txt"), "w", encoding="utf-8") as f:
        for key, value in nt_dict.items():
            f.write(key + " => " + value + "\n")

if __name__ == "__main__":
    main()