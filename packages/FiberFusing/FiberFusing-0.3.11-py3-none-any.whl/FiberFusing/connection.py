#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
import logging
from scipy.optimize import minimize_scalar
from itertools import combinations

# Local imports
from FiberFusing.buffer import Circle, Point, Polygon, LineString, EmptyPolygon
from FiberFusing import utils


class ConnectionOptimization():
    def iterate_over_connected_fibers(self) -> tuple:
        """
        Just like the name implies, generator that iterate
        over all the connected fibers.

        :returns:   pair of two connected fibers
        :rtype:     tuple
        """
        for fiber0, fiber1 in combinations(self.fiber_list, 2):
            if fiber0.intersection(fiber1).is_empty:
                continue
            else:
                yield fiber0, fiber1

    def shift_connections(self, virtual_shift: float) -> None:
        """
        Set the virtual shift of the virtual circles for each of the
        connections.

        :param      virtual_shift:  The shift of virtual circles
        :type       virtual_shift:  float
        """
        self.virtual_shift = virtual_shift

        topology = self.get_overall_topology()
        for connection in self.connected_fibers:
            connection.set_shift_and_topology(shift=virtual_shift, topology=topology)

    def get_added_section(self) -> Polygon:
        added_section = []
        for n, connection in enumerate(self.connected_fibers):
            Newadded_section = connection.added_section

            added_section.append(Newadded_section)

        _added_section = utils.Union(*added_section) - utils.Union(*self.fiber_list)
        _added_section.remove_non_polygon()

        return _added_section

    def get_removed_section(self) -> Polygon:
        removed_section = []
        for connection in self.connected_fibers:
            removed_section.append(connection.removed_section)

        _removed_section = utils.Union(*removed_section)
        return _removed_section

    def get_removed_area(self):
        return len(self.fiber_list) * self.fiber_list[0].area - utils.Union(*self.fiber_list).area

    def init_connected_fibers_cores(self) -> None:
        """
        Setup the core position for each connections.
        Initial values of the core is the center.
        """
        for connection in self.connected_fibers:
            connection[0]._core = connection[0].center
            connection[1]._core = connection[1].center

    def init_connected_fibers(self) -> None:
        """
        Generate the connections (every pair of connnected fibers).
        """
        self.connected_fibers = []

        for fibers in self.iterate_over_connected_fibers():
            connection = Connection(*fibers)
            self.connected_fibers.append(connection)

        self.init_connected_fibers_cores()

    def get_cost_value(self, virtual_shift: float) -> float:
        """
        Gets the cost value which is the difference between removed section
        and added section for a given virtual circle shift.

        :param      virtual_shift:  The shift of the virtual circles
        :type       virtual_shift:  float

        :returns:   The cost value.
        :rtype:     float
        """

        self.shift_connections(virtual_shift=virtual_shift)

        added_section_area = self.get_added_section().area
        removed_section_area = self.get_removed_area()

        cost = abs(added_section_area - removed_section_area)

        logging.debug(f' Fusing optimization: {virtual_shift = :.2e} \t -> \t{added_section_area = :.2e} \t -> {removed_section_area = :.2e} \t -> {cost = :.2e}')

        return cost

    def optimize_virtual_shift(self, bounds: tuple) -> float:
        """
        Compute the optimized geometry such that mass is conserved.
        Does not compute the core movment.

        :param      bounds:  The virtual shift boundaries
        :type       bounds:  tuple

        :returns:   The optimal virtual shift.
        :rtype:     float
        """
        core_distance = self.connected_fibers[0].distance_between_cores
        bounds = (0, core_distance * 1e3) if bounds is None else bounds

        res = minimize_scalar(
            self.get_cost_value,
            bounds=bounds,
            method='bounded',
            options={'xatol': core_distance * self.tolerance_factor}
        )

        return res.x

    def compute_optimal_structure(self, bounds: tuple = None) -> Polygon:
        """
        Compute the optimized geometry such that mass is conserved and return the optimal geometry.
        Does not compute the core movment.

        :param      bounds:  The virtual shift boundaries
        :type       bounds:  tuple

        :returns:   The optimize geometry.
        :rtype:     buffer.Polygon
        """

        optimal_virtual_shift = self.optimize_virtual_shift(bounds=bounds)

        optimal_geometry = self.get_shifted_geometry(virtual_shift=optimal_virtual_shift)

        self._clad_structure = optimal_geometry

    def get_shifted_geometry(self, virtual_shift: float) -> Polygon:
        """
        Returns the clad geometry for a certain shift value.

        :param      virtual_shift:  The shift value
        :type       virtual_shift:  { type_description }

        :returns:   The optimized geometry.
        :rtype:     { return_type_description }
        """

        added_section = self.get_added_section()

        opt_geometry = utils.Union(*self.fiber_list, added_section)

        return opt_geometry


class Connection():
    def __init__(self, fiber0, fiber1):
        self.fiber_list = [fiber0, fiber1]
        self.added_section = EmptyPolygon()
        self.topology = "not defined"
        self.shift = "not-defined"

    def set_shift_and_topology(self, shift: float, topology: str):
        self.shift = shift
        self.topology = topology
        self.compute_virtual_circles()
        self.compute_mask()
        self.compute_added_section()
        self.compute_removed_section()

    def __getitem__(self, idx):
        return self.fiber_list[idx]

    def __setitem__(self, idx, item):
        self.fiber_list[idx] = item

    @property
    def distance_between_cores(self):
        return self[0].center.distance(self[1].center)

    @property
    def limit_added_area(self):
        return self[0].union(self[1]).convex_hull - self[0] - self[1]

    def compute_removed_section(self) -> None:
        self.removed = utils.Intersection(*self)
        self.removed.Area = self[1].area + self[0].area - utils.Union(*self).area

    def compute_topology(self) -> None:
        if self.removed_section.Area > self.limit_added_area.area:
            self.topology = 'convex'
        else:
            self.topology = 'concave'

    def get_conscripted_circles(self, type='exterior') -> Circle:
        """
        Return the connection two circonscript circles, which can be either of type exterior
        or interior.

        :param      type:  The type of circonscript circle to compute
        :type       type:  str

        :returns:   The conscripted circles.
        :rtype:     Circle
        """
        extended_line = self.get_center_line(extended=True)
        line = self.get_center_line(extended=False)

        perpendicular_vector = extended_line.get_perpendicular().get_vector()

        point = line.mid_point.translate(perpendicular_vector * self.shift)

        if type.lower() in ['exterior', 'concave']:
            radius = numpy.sqrt(self.shift**2 + (line.length / 2)**2) - self[0].radius

        if type.lower() in ['interior', 'convex']:
            radius = numpy.sqrt(self.shift**2 + (line.length / 2)**2) + self[0].radius

        return Circle(position=point, radius=radius)

    def compute_virtual_circles(self) -> None:
        if self.topology == "not defined":
            raise Exception("Trying to compute circonsript virtual circles with a defined topology!")

        line = self.get_center_line(extended=False)

        Circonscript0 = self.get_conscripted_circles(type=self.topology)

        Circonscript1 = Circonscript0.rotate(angle=180, origin=line.mid_point, in_place=False)

        self.virtual_circles = Circonscript0, Circonscript1

    def get_connected_point(self) -> list:
        """
        Return list of contact point from the connected fibers and
        virtual circles.
        """
        P0 = utils.NearestPoints(self.virtual_circles[0], self[0])
        P1 = utils.NearestPoints(self.virtual_circles[1], self[0])
        P2 = utils.NearestPoints(self.virtual_circles[0], self[1])
        P3 = utils.NearestPoints(self.virtual_circles[1], self[1])

        return [Point(position=(p.x, p.y)) for p in [P0, P1, P2, P3]]

    def compute_mask(self) -> None:
        """
        Compute the mask that is connecting the center to the contact point
        with the virtual circles.
        """
        P0, P1, P2, P3 = self.get_connected_point()

        if self.topology.lower() == 'concave':

            mask = Polygon(coordinates=[P0._shapely_object, P1._shapely_object, P3._shapely_object, P2._shapely_object])

            self.mask = (mask - self.virtual_circles[0] - self.virtual_circles[1])

        elif self.topology.lower() == 'convex':
            mid_point = LineString(coordinates=[self[0].center, self[1].center]).mid_point

            mask0 = Polygon(coordinates=[mid_point._shapely_object, P0._shapely_object, P2._shapely_object])
            mask0.scale(
                factor=1000,
                origin=mid_point._shapely_object,
                in_place=True
            )

            mask1 = Polygon(coordinates=[mid_point._shapely_object, P1._shapely_object, P3._shapely_object])
            mask1.scale(
                factor=1000,
                origin=mid_point._shapely_object,
                in_place=True
            )

            self.mask = (utils.Union(mask0, mask1) & utils.Union(*self.virtual_circles))

    def compute_added_section(self) -> None:
        if self.topology == 'convex':
            interesction = self.virtual_circles[0].intersection(self.virtual_circles[1], in_place=False)
            self.added_section = (self.mask - self[0] - self[1]) & interesction

        elif self.topology == 'concave':
            union = self.virtual_circles[0].union(self.virtual_circles[1], in_place=False)
            self.added_section = self.mask - self[0] - self[1] - union

        self.added_section.remove_non_polygon()

    def get_center_line(self, extended: bool = False) -> LineString:
        """
        Returns the line connecting the two centers of the connected fibers.
        If extended is true that line is extended up to the boundary of the two fibers.

        :param      extended:  Indicates if extended
        :type       extended:  bool

        :returns:   The center line.
        :rtype:     LineString
        """
        line = LineString(coordinates=[self[0].center, self[1].center])

        if extended is True:
            line = line.make_length(line.length + self[0].radius + self[1].radius)

        return line

    @property
    def total_area(self) -> Polygon:
        """
        Returns polygone representating the total area of the connected two fibers.

        :returns:   Total area
        :rtype:     Polygon
        """
        output = utils.Union(*self, self.added_section)
        output.remove_non_polygon()

        return output

    def split_geometry(self, geometry, position) -> Polygon:
        """
        Split the connection at a certain position x which is the parametrised
        point covering the full connection.

        :param      geometry:  The geometry
        :type       geometry:  Polygon
        :param      position:  The parametrized position
        :type       position:  float

        :returns:   The splitted geometry
        :rtype:     Polygon
        """
        line = self.get_center_line(extended=False)

        line.centering(center=position).rotate(
            angle=90,
            in_place=True,
            origin=line.mid_point
        )

        line.extend(factor=2)

        external_part = utils.Union(geometry.copy()).remove_non_polygon().keep_largest_polygon()

        return external_part.split_with_line(line=line, return_type='largest')

    def compute_area_mismatch_cost(self, x: float = 0.5) -> float:
        line = self.get_center_line(extended=True)
        position0 = line.get_position_parametrisation(1 - x)
        position1 = line.get_position_parametrisation(x)

        large_section = self.split_geometry(
            geometry=self.total_area,
            position=position0
        )

        small_area = abs(large_section.area - self.total_area.area)

        Cost = abs(small_area - self[0].area / 2.)

        self.core_shift = (position0 - self[0].center), (position1 - self[1].center)

        logging.debug(f'Core positioning optimization: {x = :+.2f} \t -> \t{Cost = :<10.2f} -> \t\t{self.core_shift = }')

        return Cost

    def optimize_core_position(self) -> None:
        minimize_scalar(
            self.compute_area_mismatch_cost,
            bounds=(0.50001, 0.99),
            method='bounded',
            options={'xatol': 1e-10}
        )

        self[0]._core = self[0]._core + self.core_shift[0]

        self[1]._core = self[1]._core + self.core_shift[1]

# -
