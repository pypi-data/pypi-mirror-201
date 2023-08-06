'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

import json
import os


class jsonBase:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def save(self, user_id, name, value, list=None, overwrite=True):
        name = name.upper()
        value = float(value)

        file_path = os.path.join(self.folder_path, str(user_id) + ".json")
        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
        if list is not None:
            list = list.upper()
            if list not in data:
                data[list] = []
            updated = False
            for item in data[list]:
                if name in item:
                    item[name] = value
                    updated = True
                    break
            if not updated:
                data[list].append({name: value})
        elif name in data and not overwrite:
            data[name] += value
        else:
            data[name] = value
        with open(file_path, "w") as file:
            json.dump(data, file)

    def load(self, user_id, name):
        file_path = os.path.join(self.folder_path, str(user_id) + ".json")
        name = name.upper()
        if not os.path.exists(file_path):
            return 0

        with open(file_path, "r") as file:
            data = json.load(file)
            value = 0

            def find_value(data, name):
                nonlocal value
                if isinstance(data, dict):
                    for key, val in data.items():
                        if key.upper() == name:
                            value = val
                            break
                        elif isinstance(val, (dict, list)):
                            find_value(val, name)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, (dict, list)):
                            find_value(item, name)

            find_value(data, name)
            return value
