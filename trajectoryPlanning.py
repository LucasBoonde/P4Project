import numpy as np
from matplotlib import pyplot as plt


def cubic_trajectory_planning(q0, qf, qd0, qdf, m = 100):
    """
    Point to Point Cubic Trajectory Planning

    ...


    :param q0: The Initial Position (Dof x 1)
    :param qf: The Final Position (Dof x 1)
    :param qd0: The Initial Velocity (Dof x 1)
    :param qdf: The Final Velocity (Dof x 1)
    :param m(Optional): The Discrete Time Steps

    :returns

    ---

    q, qd, qdd : Position, Velocity and Acceleration (Dof x m)
    """
    n = q0.shape[0]

    # Polynomial Parameters
    a0 = np.copy(q0)
    a1 = np.copy(qd0)
    a2 = 3 * (qf - q0)
    a3 = -2 * (qf - q0)

    timesteps = np.linspace(0,1, num=m)

    q = np.zeros((n, m))
    qd = np.zeros((n, m))
    qdd = np.zeros((n, m))

    for i in range(len(timesteps)):
        t = timesteps[i]
        t_2 = t * t
        t_3 = t * t * t
        q[:, i] = (a0) + (a1 * t) + (a2 * t_2) + (a3 * t_3)
        qd[:, i] = (a1) + (2 * a2 * t) + (3 * a3 * t_2)
        qdd[:, i] = (2* a2) + (6 * a3 * t)

    return q, qd, qdd


def plot_joint_trajectoriy(q, qd, qdd):
    """
    Function to plot joint trajectories

    ...

    parameters

    :param q: Joint Position (Dof x m)
    :param qd: Joint Velocity (Dof x m)
    :param qdd: joint Accelerration (Dof x m)

    :returns
    """
    m = q.shape[1]
    timesteps = np.linspace(0, 1, num = m)

    n = q.shape[0]

    fig, axis = plt.subplots(3)
    fig.suptitle("Joint Trajectories")


    #Joint Positions
    axis[0].set_title("Position")
    axis[0].set(xlabel = "Time", ylabel = "Position")
    for i in range(n):
        axis[0].plot(timesteps, q[i])


    #Joint Velocities
    axis[0].set_title("Velocity")
    axis[0].set(xlabel="Time", ylabel="Velocity")
    for i in range(n):
        axis[1].plot(timesteps, qd[i])

    #Joint Accelerations
    axis[2].set_title("Acceleration")
    axis[0].set(xlabel="Time", ylabel="Acceleration")
    for i in range(n):
        axis[2].plot(timesteps, qdd[i])

    #Legends
    legends = [f"Joints_{i+1}" for i in range(n)]
    axis[0].legend(legends)
    axis[1].legend(legends)
    axis[2].legend(legends)


    fig.tight_layout()
    plt.show()