
def Reynolds(velocity, length, kin_viscosity):
	"""Compute the Reynolds number

	Parameters
	----------
	velocity : float
 		velocity of the fluid [m s^-1]
	length : float
  		characteristic length of the system [m]
  	kin_viscosity : float
  		kinetic viscosity of the fluid [m^2 s^-1]
   	
    """
	return (velocity * length)/kin_viscosity
	

def Prandtl(dyn_viscosity, massic_heat_capacity, thermal_conductivity):
	"""Compute the Prandtl number

	Parameters
	----------
	dyn_viscosity : float
		dynamic viscosity of the fluid [kg m^-1 s^-1]
	massic_heat_capacity : float
		isobaric massic heat capacity [J kg^-1 K^-1]
	thermal_conductivity : float
		thermal conductivity [W m^-1 K^-1]
	"""
	return (dyn_viscosity * massic_heat_capacity)/thermal_conductivity


def Nusselt(convective_coeff, length, thermal_conductivity):
	"""Compute the local Nusselt number

	Parameters
	----------
	thermal_conductivity : float
		thermal conductivity of the fluid [W m^-1 K^-1]
	length : float
  		characteristic length of the system [m]
  	convective_coeff : float
  		convective heat transfer coefficient [W m^-2 K^-1]
	"""
	return (convective_coeff * length)/thermal_conductivity


def Grashof(g_acceleration, thermal_expansion_coeff, surf_temp, bulk_temp, length, kin_viscosity):
	"""Compute the Grashof number

	Parameters
	----------
	g_acceleration : float
		gravitationnal acceleration [m s^-2]
	thermal_expansion_coeff : float
		coefficient of thermal expansion
	surf_temp : float
		temperature of the surface [K] or [°C]
	bulk_temp : float
		temperature of the bulk [K] or [°C]
	length : float
		characteristic length of the system [m]
	kin_viscosity : float
		kinetic viscosity of the fluid [m^2 s^-1]
	"""
	return (1/kin_viscosity**2)*(g * thermal_expansion_coeff * length**3)*(surf_temp - bulk_temp)


def Biot(thermal_conductivity, length, convective_coeff):
	"""Compute the Biot number

	Parameters
	----------
	thermal_conductivity : float
		thermal conductivity of the body [W m^-1 K^-1]
	length : float
  		characteristic length of the system [m]
  	convective_coeff : float
  		convective heat transfer coefficient [W m^-2 K^-1]
	"""
	return (convective_coeff * length)/thermal_conductivity