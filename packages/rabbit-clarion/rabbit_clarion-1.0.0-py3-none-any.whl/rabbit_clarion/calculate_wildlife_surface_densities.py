import numpy as np


def calculate_surface_densities_by_group(group, data_transects, transect_lenght=300):
    parameters = Native_Group_Parameters(group, data_transects, transect_lenght)
    animal_group_data = parameters.animal_group_data
    TRANSECT_PARAMETERS = {
        "length": parameters.length,
        "width": parameters.width,
        "point_radius": parameters.point_radius,
    }
    transects = parameters.transects
    species = parameters.species
    results_dic = _init_results()
    for transect in transects:
        vegetal_types = obtain_vegetation_type_by_transect(animal_group_data, transect)
        for i_species in species:
            species_transect_density = Species_Transect_Density(
                transect, i_species, vegetal_types, animal_group_data, TRANSECT_PARAMETERS, group
            )
            species_transect_density._update_results(results_dic)
    return results_dic


class Native_Group_Parameters:
    def __init__(self, group, data_transects, transect_lenght=300):
        self.group = group
        self.length = transect_lenght
        self.animal_group_data = data_transects[data_transects["Grupo"] == group]
        self.width = 10
        self.point_radius = 25
        self.transects = self.animal_group_data["Transecto"].unique()
        self.species = self.animal_group_data["Especie"].dropna().unique()


class Species_Transect_Density:
    def __init__(
        self, transect, species, vegetal_type, animal_group_data, TRANSECT_PARAMETERS, group
    ):
        self.animal_group_data = animal_group_data
        self.transect = transect
        self.species = species
        self.vegetal_type = vegetal_type
        self.TRANSECT_PARAMETERS = TRANSECT_PARAMETERS
        self.group = group
        self.filtered_data = self._filter_data_by_transect_and_specie(transect, species)
        self.density_in_transect_ha = self._calculate_density_in_transect()

    def _filter_data_by_transect_and_specie(self, transect, species):
        return filter_by_transect_and_species(self.animal_group_data, transect, species)

    def _calculate_density_in_transect(self):
        n_individuals = self.filtered_data["Cantidad_individuos"].sum()
        if self.group == "Ave":
            density_in_transect = n_individuals / (
                np.pi * self.TRANSECT_PARAMETERS["point_radius"] ** 2 * 5
            )
        if self.group == "Tecolote":
            density_in_transect = n_individuals / (
                self.TRANSECT_PARAMETERS["length"] * self.get_max_distance() * 2
            )
        if self.group == "Reptil":
            density_in_transect = n_individuals / (
                self.TRANSECT_PARAMETERS["length"] * self.TRANSECT_PARAMETERS["width"] * 2
            )
        density_in_transect_ha = density_in_transect * 10_000
        return density_in_transect_ha

    def get_max_distance(self):
        return self.filtered_data["Distancia"].max()

    def _update_results(self, results_dic):
        maximum_distance = self.get_max_distance()
        results_dic["Especie"].append(self.species)
        results_dic["Transecto"].append(self.transect)
        results_dic["Densidad"].append(self.density_in_transect_ha)
        results_dic["Distancia_max"].append(maximum_distance)
        results_dic["Tipo_vegetacion"].append(check_array(self.vegetal_type))


def obtain_vegetation_type_by_transect(animal_group_data, transect):
    transect_data = animal_group_data[animal_group_data.Transecto == transect]
    vegetal_types = transect_data["Tipo_de_vegetacion"].unique()
    return vegetal_types


def filter_by_transect_and_species(animal_group_data, transect, species):
    mask = (animal_group_data.Transecto == transect) & (animal_group_data.Especie == species)
    filtered_data = animal_group_data[mask]
    return filtered_data


def check_array(array):
    if array.size == 0:
        return "NA"
    return array[0]


def _init_results():
    return {
        "Transecto": [],
        "Especie": [],
        "Densidad": [],
        "Distancia_max": [],
        "Tipo_vegetacion": [],
    }
