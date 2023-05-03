from trajectoryPlanning import cubic_trajectory_planning
from trajectoryPlanning import plot_joint_trajectoriy
import numpy as np

if __name__ == "__main__":
    q0 = np.array([0, 1, 2])
    qd0 = np.array([0, 0, 0])
    qf = np.array([1, 2, 3])
    qdf = np.array([0, 0, 0])

    q, qd, qdd = cubic_trajectory_planning(q0,qf,qd0,qdf)
    plot_joint_trajectoriy(q,qd,qdd)