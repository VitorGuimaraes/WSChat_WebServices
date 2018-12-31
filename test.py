y0 = 120
map_chats_click = []
while y0 <= 665:
    y2 = y0 + 77
    map_chats_click.append((y0, y2))
    y0 = y2 + 1

def cell_data(pos_y):
	for index, position in enumerate(map_chats_click):
		if pos_y >= position[0] and pos_y <= position[1]:
			return index

print(cell_data(20))