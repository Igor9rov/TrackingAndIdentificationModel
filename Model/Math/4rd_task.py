count_of_files = int(input())

roots = list(map(lambda str: str.splitlines(), input().split(" ")))
roots = roots[0]


class Tree:
    def __init__(self, roots_list):
        self.count = 0
        self.unreal_name = "My_unreal_folder_name"
        self.dict = {}
        self.previous_dict = {}
        self.current_dict = self.dict
        for root in roots_list:
            slash, *folders, file = root.split("/")
            for folder in folders:
                self.move_to(folder)
            self.current_dict.setdefault(self.unreal_name, [])
            self.current_dict[self.unreal_name].append(file)
            self.move_to_start()

    def move_to(self, folder):
        self.previous_dict = dict(self.current_dict)
        self.current_dict.setdefault(folder, {})
        self.current_dict = self.current_dict[folder]

    def move_back_to_one_folder(self):
        pass

    def calculate_in_one_folder(self, folder=None):
        self.current_dict.setdefault(self.unreal_name, [])
        self.count += len(self.current_dict[self.unreal_name])
        if len(self.current_dict) > 1:
            for folder in self.current_dict:
                if folder != self.unreal_name:
                    self.count += 2
                    self.calculate_in_one_folder(folder)
        else:
            self.move_back_to_one_folder()











