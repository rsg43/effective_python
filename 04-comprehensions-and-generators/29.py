scenes = [1, 2, 3, 4, 5]

scenes_dict = {str(x): x_squared for x in scenes if (x_squared := x * x) > 10}

print(scenes_dict)
