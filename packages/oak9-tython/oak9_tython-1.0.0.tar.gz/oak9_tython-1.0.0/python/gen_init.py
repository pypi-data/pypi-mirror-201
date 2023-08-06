import os

frmwrk_dir = './oak9'

for comp in os.listdir(frmwrk_dir):
    print(comp)
    init_string = ''
    for comp_file in os.listdir(frmwrk_dir + '/' + comp):
        comp_file = comp_file.split('.')[0]
        if comp_file not in  [comp,'__init__']:
            temp = 'from ' + comp + ' import ' + comp_file + '\n'
            init_string += temp
    with open(frmwrk_dir + '/' + comp + '/__init__.py', 'w') as file:
        file.write(init_string)
        file.close()
