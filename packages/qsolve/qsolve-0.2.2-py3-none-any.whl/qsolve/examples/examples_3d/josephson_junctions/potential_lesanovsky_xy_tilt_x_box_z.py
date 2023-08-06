from qsolve.potentials.components_3d.lesanovsky_xy_3d import eval_potential_lesanovsky_xy_3d
from qsolve.potentials.components_3d.tilt_x_3d import eval_potential_tilt_x_3d
from qsolve.potentials.components_3d.box_z_3d import eval_potential_box_z_3d


class PotentialLesanovskyXYTiltXBoxZ(object):

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

        V_box_z_max = params_user["V_box_z_max"] / unit_energy
        w_box_z = params_user["w_box_z"] / unit_length
        s_box_z = params_user["s_box_z"] / unit_length

        z1 = w_box_z / 2.0
        z2 = -w_box_z / 2.0

        self.V_box_z = V_box_z_max * eval_potential_box_z_3d(self.z_3d, z1, z2, s_box_z)

    def eval(self, u):

        omega_rabi = u[0] * self.omega_rabi_ref

        V_lesanovsky = eval_potential_lesanovsky_xy_3d(
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

        a_x = -1.0 * u[1] * self.gamma_tilt_ref

        V_tilt_x = eval_potential_tilt_x_3d(self.x_3d, a_x)

        V = V_lesanovsky + V_tilt_x + self.V_box_z

        return V
