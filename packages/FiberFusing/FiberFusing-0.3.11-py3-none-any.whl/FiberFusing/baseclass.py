#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import logging
from dataclasses import dataclass

# Third-party imports
import numpy
import shapely.geometry as geo

# Local imports
from MPSPlots.Render2D import Scene2D, Axis
from FiberFusing import utils
from FiberFusing.connection import ConnectionOptimization
from FiberFusing import buffer
from FiberFusing.buffer import Circle
from FiberFusing.rings import FiberRing

logging.basicConfig(level=logging.INFO)


@dataclass
class BaseFused(ConnectionOptimization):
    index: float
    """ Refractive index of the cladding structure. """
    tolerance_factor: float = 1e-2
    """ Tolerance on the optimization problem which aim to minimize the difference between added and removed area of the heuristic algorithm. """
    graded_index_factor: float = 0
    """ If different than zero a refractive index gradient is applied """

    def __post_init__(self):
        self.fiber_list = []
        self.core_list = []
        self._clad_structure = None

    @property
    def is_multi(self):
        return isinstance(self.clad_structure._shapely_object, geo.MultiPolygon)

    @property
    def clad_structure(self):
        if self._clad_structure is None:
            return utils.Union(*self.fiber_list)
        else:
            return self._clad_structure

    @property
    def _shapely_object(self):
        return self.clad_structure._shapely_object

    @property
    def bounds(self):
        """
        Return the boundaries of the structure.
        """
        return self.clad_structure.bounds

    @property
    def center(self):
        return self.clad_structure.center

    @property
    def fiber(self) -> list:
        """
        Return list of all the fiber in the structure

        :returns:   List of the structure fiber components
        :rtype:     list
        """
        return self.fiber_list

    @property
    def removed_section(self) -> buffer.Polygon:
        if self._removed_section is None:
            self.compute_removed_section()
        return self._removed_section

    @property
    def cores(self):
        return [fiber.core for fiber in self.fiber_list]

    def get_overall_topology(self) -> str:
        """
        Compute the overall topology of the structure

        :returns:   The topology ['concave', 'convex'].
        :rtype:     str
        """
        Limit = []
        for connection in self.connected_fibers:
            Limit.append(connection.limit_added_area)

        overall_limit = utils.Union(*Limit) - utils.Union(*self.fiber_list)

        total_removed_area = self.get_removed_area()
        return 'convex' if total_removed_area > overall_limit.area else 'concave'

    def add_fiber_ring(self, number_of_fibers: int,
                             fiber_radius: float,
                             fusion_degree: float = 0.0,
                             scale_position: float = 1.0,
                             angle_shift: float = 0.0) -> None:
        """
        Add a ring of equi-distant and same radius fiber with a given
        radius and degree of fusion

        :param      number_of_fibers:  The number of fibers in the ring
        :type       number_of_fibers:  int
        :param      fusion_degree:     The fusion degree for that ring
        :type       fusion_degree:     float
        :param      fiber_radius:      The fiber radius
        :type       fiber_radius:      float
        """
        ring = FiberRing(
            number_of_fibers=number_of_fibers,
            fiber_radius=fiber_radius,
            angle_shift=angle_shift
        )

        ring.set_fusion_degree(fusion_degree=fusion_degree)
        ring.scale_position(factor=scale_position)

        for fiber in ring.fiber_list:
            self.fiber_list.append(fiber)

    def add_center_fiber(self, fiber_radius: float) -> None:
        """
        Add a single fiber of given radius at the center of the structure.

        :param      fiber_radius:  The fiber radius
        :type       fiber_radius:  float
        """
        fiber = Circle(
            radius=fiber_radius,
            position=(0, 0)
        )

        self.fiber_list.append(fiber)

    def add_custom_fiber(self, *fibers) -> None:
        """
        Add any custom defined fiber

        :param      fibers:  The custom fibers
        :type       fibers:  list
        """
        for fiber in fibers:
            self.fiber_list.append(fiber)

    def compute_core_position(self) -> None:
        """
        Optimize one round for the core positions of each connections.
        """
        for connection in self.connected_fibers:
            connection.optimize_core_position()

    def randomize_core_position(self, randomize_position: float = 0) -> None:
        """
        Shuffle the position of the fiber cores.
        It can be used to add realism to the fusion process.
        """
        if randomize_position != 0:
            for fiber in self.fiber_list:
                random_xy = numpy.random.rand(2) * randomize_position
                fiber.core.translate(random_xy, in_place=True)

    def get_rasterized_mesh(self, coordinate_axis: Axis) -> numpy.ndarray:
        return self.clad_structure.get_rasterized_mesh(coordinate_axis=coordinate_axis)

    def rotate(self, *args, **kwargs):
        """
        Rotates the full structure, including the fiber cores.
        """
        for fiber in self.fiber_list:
            fiber.rotate(*args, **kwargs, in_place=True)
            fiber.core.rotate(*args, **kwargs, in_place=True)

        self.clad_structure = self.clad_structure.rotate(*args, **kwargs)

    def scale_position(self, factor: float):
        """
        Scale down the distance between each cores.

        :param      factor:  The scaling factor
        :type       factor:  float
        """
        for fiber in self.fiber_list:
            fiber.scale_position(factor=factor)

    def plot(self, show_structure: bool = True,
                   show_fibers: bool = False,
                   show_cores: bool = True,
                   show_added: bool = False,
                   show_removed: bool = False) -> Scene2D:

        figure = Scene2D(unit_size=(6, 6))

        ax = Axis(
            row=0,
            col=0,
            x_label=r'x',
            y_label=r'y',
            show_grid=True,
            equal_limits=True,
            equal=True
        )

        figure.add_axes(ax)._generate_axis_()

        if show_structure:
            self.clad_structure._render_(ax)

        if show_added:
            for connection in self.connected_fibers:
                added_section = connection.added_section
                added_section.facecolor = 'green'
                connection.added_section._render_(ax)

        if show_fibers:
            for n, fiber in enumerate(self.fiber_list):
                fiber.name = f'fiber: {n}'
                fiber._render_(ax)

        if show_cores:
            for n, fiber in enumerate(self.fiber_list):
                core = fiber.core
                core.name = f'core: {n}'
                fiber.core._render_(ax)

        return figure


#  -
