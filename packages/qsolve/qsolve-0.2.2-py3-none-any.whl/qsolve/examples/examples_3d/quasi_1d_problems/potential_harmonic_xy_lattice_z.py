from qsolve.potentials.components_3d.harmonic_x_3d import eval_potential_harmonic_x_3d
from qsolve.potentials.components_3d.harmonic_y_3d import eval_potential_harmonic_y_3d

from qsolve.potentials.components_3d.lattice_z_3d import eval_potential_lattice_z_3d


class Potential(object):

    def __init__(self, params_solver, params_user):

        x_3d = params_solver["x_3d"]
        y_3d = params_solver["y_3d"]
        z_3d = params_solver["z_3d"]

        Lz = params_solver["Lz"]

        m_atom = params_solver["m_atom"]

        unit_frequency = params_solver["unit_frequency"]
        unit_energy = params_solver["unit_energy"]

        omega_x = params_user["omega_x"] / unit_frequency
        omega_y = params_user["omega_y"] / unit_frequency

        V_harmonic_x = eval_potential_harmonic_x_3d(x_3d, omega_x, m_atom)
        V_harmonic_y = eval_potential_harmonic_y_3d(y_3d, omega_y, m_atom)

        self.V_harmonic_xy = V_harmonic_x + V_harmonic_y

        self.V_lattice_z_max = params_user["V_lattice_z_max"] / unit_energy
        m = params_user["V_lattice_z_m"]

        self.V_lattice_z = eval_potential_lattice_z_3d(z_3d, Lz, m)

    def eval(self, u):

        amplitude_V_lattice_z = u * self.V_lattice_z_max

        V = self.V_harmonic_xy + amplitude_V_lattice_z * self.V_lattice_z

        return V
