"""
Implementation of a Lesanovsky - type potential corresponding to the article: Adiabatic radio - frequency potentials
for the coherent manipulation of matter waves, PHYSICAL REVIEW A 73, 03361 9(2006)
"""

from qsolve.potentials.components_3d.lesanovsky_3d import eval_potential_lesanovsky_3d
from qsolve.potentials.components_3d.tilt_x_3d import eval_potential_tilt_x_3d


class PotentialLesanovskyTiltX(object):

    def __init__(self, params_solver, params_user):

        self.x_3d = params_solver["x_3d"]
        self.y_3d = params_solver["y_3d"]
        self.z_3d = params_solver["z_3d"]

        self.hbar = params_solver["hbar"]
        self.mu_B = params_solver["mu_B"]
        self.m_atom = params_solver["m_atom"]

        unit_length = params_solver["unit_length"]
        unit_energy = params_solver["unit_energy"]
        unit_frequency = params_solver["unit_frequency"]

        self.g_F = params_user["g_F"]
        self.m_F = params_user["m_F"]
        self.m_F_prime = params_user["m_F_prime"]

        self.omega_perp = params_user["omega_perp"] / unit_frequency
        self.omega_para = params_user["omega_para"] / unit_frequency
        self.omega_delta_detuning = params_user["omega_delta_detuning"] / unit_frequency
        self.omega_trap_bottom = params_user["omega_trap_bottom"] / unit_frequency
        self.omega_rabi_ref = params_user["omega_rabi_ref"] / unit_frequency

        self.gamma_tilt_ref = params_user["gamma_tilt_ref"] * unit_length / unit_energy

    def eval(self, u):

        omega_rabi = u[0] * self.omega_rabi_ref

        a_x = -1.0 * u[1] * self.gamma_tilt_ref

        V_lesanovsky = eval_potential_lesanovsky_3d(
            self.x_3d,
            self.y_3d,
            self.z_3d,
            self.g_F,
            self.m_F,
            self.m_F_prime,
            self.omega_perp,
            self.omega_para,
            self.omega_delta_detuning,
            self.omega_trap_bottom,
            omega_rabi,
            self.hbar,
            self.mu_B,
            self.m_atom)

        V_tilt_x = eval_potential_tilt_x_3d(self.x_3d, a_x)

        return V_lesanovsky + V_tilt_x
