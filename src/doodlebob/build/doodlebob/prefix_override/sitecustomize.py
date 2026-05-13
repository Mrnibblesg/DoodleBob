import sys
if sys.prefix == '/home/Parker/Programming/Robotics/doodlebob_pixi_env_test/.pixi/envs/default':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/Parker/Programming/Robotics/doodlebob_pixi_env_test/src/doodlebob/install/doodlebob'
