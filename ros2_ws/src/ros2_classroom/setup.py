from setuptools import setup
from pathlib import Path
name = 'ros2_classroom'
data = [('share/ament_index/resource_index/packages', ['resource/' + name]),
        ('share/' + name, ['package.xml'])]
for folder in ['launch', 'config', 'model']:
    for d in sorted({str(f.parent) for f in Path(folder).rglob('*') if f.is_file()}):
        data.append(('share/' + name + '/' + d, [str(f) for f in Path(d).iterdir() if f.is_file()]))
setup(name=name, version='2.0.0', packages=[name], data_files=data,
      entry_points={'console_scripts': [f'{n} = {name}.{n}:main' for n in
        ['basic_publisher', 'basic_subscriber', 'add_server', 'add_client', 'show_model']]})
