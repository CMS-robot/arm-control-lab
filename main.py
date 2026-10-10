from src.robot_config import load_dh

print(load_dh())

from src.robot_config import load_joint_limits

print(load_joint_limits())

from src.robot_config import count_joints
print(count_joints(load_dh()))