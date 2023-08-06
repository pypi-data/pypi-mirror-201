from qsolve.potentials.components_3d.harmonic_3d import eval_potential_harmonic_3d


class Potential(object):

    def __init__(self, params_solver, params_user):

        x_3d = params_solver["x_3d"]
        y_3d = params_solver["y_3d"]
        z_3d = params_solver["z_3d"]

        m_atom = params_solver["m_atom"]

        unit_frequency = params_solver["unit_frequency"]

        omega_x = params_user["omega_x"] / unit_frequency
        omega_y = params_user["omega_y"] / unit_frequency
        omega_z = params_user["omega_z"] / unit_frequency

        self.V = eval_potential_harmonic_3d(x_3d, y_3d, z_3d, omega_x, omega_y, omega_z, m_atom)

    def eval(self, u):

        return self.V
