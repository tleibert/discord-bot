#! /bin/env/python3

import json

with open("new_colors.txt") as new_colors:
    new_lines = new_colors.readlines()
with open("colors.json") as color_file:
    color_json = json.load(color_file)


print(int(len(new_lines) / 3))
new_color_dict = {}
for i in range(int(len(new_lines) / 3)):
    color_name = new_lines[3 * i].strip()
    color_value = new_lines[3 * i + 1][1:].strip()
    new_color_dict[color_name] = color_value

color_json.update(new_color_dict)

with open("colors.json", "w") as color_file:
    json.dump(color_json, color_file)
