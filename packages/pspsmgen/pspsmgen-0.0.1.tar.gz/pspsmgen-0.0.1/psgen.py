# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 21:29:25 2022

@author: Ronaldo Herlinger Jr.
"""

import numpy as np 
import math
import scipy.ndimage 

class Psgen():
       
    class Spheres():
        
        """
        Sphere class has functions to built sphere models to reproduce
        microfabrics of Pre-Salt rocks composed of spherulites or particles and other
        components. It has functions to place random touching and untouching 
        spheres in 3d array models. It can populate spheres on previously
        shrubstones models or empty arrays. There are also functions to place
        spheres tangencially to reproduce intraclastic rudstones and grainstones.
        
        """    
       
        def __init__(self, side, n_spheres, radius, radius_std, phi, 
                     phase_number = 2, shrub_number = 3, compaction = False,
                     comp_ratio = 1.1):
            """
            :side: maximum grid value.
            :n_spheres: initial number of spheres.
            :radius: sphere mean radius.
            :radius_std: sphere std radi.
            :phi: minimum porosity.
            :phase_number: the sphere voxels will receive the number 2 by default.
            :compaction: if true, spheres will be dilated to simulate pressure
            solution.
            :comp_ratio: the ratio of compaction
            """
            
            self.phase_number = phase_number
            self.side = side
            self.n_spheres = n_spheres
            self.radius = radius
            self.radius_std = radius_std
            self.phi = phi
            self.shrub_number = shrub_number
            self.compaction = compaction
            self.comp_ratio = comp_ratio
            

        def sphere_generator(self):
            """
            Generates an sphere within limits with aleatory
            coordinate and radius.
        
            :plim_x,lim_y,lim_z: max coordinates.
            :return: coordinates(x,y, and z) and radius.
            """          
           
            x = np.random.randint(0, self.side)
            y = np.random.randint(0, self.side) 
            z = np.random.randint(0, self.side)
            radius = int(np.random.normal(self.radius, self.radius_std))
            
            return [x,y,z,radius]
        
        
        def sphere_generator_tang(self, x, y, z, radius1):
            """
            Generates an sphere within limits with aleatory
            coordinate and radius. The spheres can touch tangentially
            to reproduce reworked particles. The function receives a
            sphere and returns an tangencial sphere.
        
            :x, y, z: input sphere center coordinates.
            :radius1: input sphere radius.
            :return: coordinates(x,y, and z) and radius of a tangential
            sphere.
            """ 
 
            radius2 = int(np.random.normal(self.radius, self.radius_std))
            dist = radius1 + radius2
            n = 0
            tol = 1000
            
            tetha = np.random.randint(-360, 360)
            omega = np.random.randint(-360, 360)
            x2 = int(x + dist * math.cos(math.radians(tetha))
                     * math.sin(math.radians(omega)))
            y2 = int(y + dist * math.sin(math.radians(tetha))
                     * math.sin(math.radians(omega)))
            z2 = int(z + dist * math.cos(math.radians(omega)))
            
            # This looping was implemented to avoid the spheres
            # be placed outside the array.
            while x2 not in range(-radius2, self.side+radius2) or y2 not in range(-radius2, self.side+radius2) or z2 not in range(-radius2, self.side+radius2):
                tetha = np.random.randint(-360, 360)
                omega = np.random.randint(-360, 360)
                x2 = int(x + dist * math.cos(math.radians(tetha))
                         * math.sin(math.radians(omega)))
                y2 = int(y + dist * math.sin(math.radians(tetha))
                     * math.sin(math.radians(omega)))
                z2 = int(z + dist * math.cos(math.radians(omega)))  
                n += 1
                if n == tol:
                    break
            
            return [x2, y2, z2, radius2]
        
        
        
        def dist_test(self, x1, y1, z1, x2, y2, z2, radius1, radius2):   
            """
            
            Measures distance between two spheres returning
            if they are touching each other.
        
            :x1,y1,z1: coordinates of first spheres.
            :x2,y2,z2: coordinates of second spheres.
            :radius1,radius2: radius of two spheres.
            :return: True for not touching.
            """ 

            dist = np.sqrt ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (
                                            z1 - z2) ** 2)
            
            if dist >= radius1 + radius2:
                return True
            
            return False
        
        
        def sphere_list(self):
            """
            
            Generates sphere list containing center coordinates and radius.
            The spheres does not occupy the same space.
        
            :try_number: number of attempties of sphere placement.
            :return: Sphere List.
            """ 
            Spheres = []
            Spheres.append(self.sphere_generator())
            
            for n in range(self.n_spheres):   
                
                Values = []
                sphere = self.sphere_generator()
                
                for Sphere in Spheres:
                    
                    valor = self.dist_test(Sphere[0], Sphere[1], Sphere[2],
                                           sphere[0], sphere[1], sphere[2],
                                           Sphere[3], sphere[3])
                    Values.append(valor)

                if Values == []:
                    Values.append(False)
                                                  
                if all(bool(item) == True for item in Values):
                    
                    if sphere[1] >= 0 and sphere[2] >= 0 and sphere[3] > 0:
        
                        Spheres.append(sphere)
                    
            return Spheres
        

        def sphere_list_tang(self):
            """
            
            Generates sphere list containing center coordinates and radius.
            The spheres does not occupy the same space. All spheres tangent
            at least one sphere.
        
            :return: Sphere List.
            """ 
            
            Spheres = []
            
            Spheres.append([self.side, 0, 0, self.radius])          
            
            for n in range(self.n_spheres):   
    
                
                Values = []
                rand = np.random.randint(0,len(Spheres))
                
                try:
                    
                    sphere_rand = Spheres[rand]
                    sphere = self.sphere_generator_tang(sphere_rand[0], sphere_rand[1],
                                                        sphere_rand[2], sphere_rand[3])
                                    
                    for Sphere in Spheres:
                            
                        valor = self.dist_test(Sphere[0], Sphere[1], Sphere[2],
                                               sphere[0], sphere[1], sphere[2],
                                               Sphere[3], sphere[3])
                        Values.append(valor)
                
                except:
                    pass
                
                if Values == []:
                    Values.append(False)
                
                if all(bool(item) == True for item in Values):
                                       
                    if sphere[1] >= 0 and sphere[2] >= 0 and sphere[3] > 0:
                    
                        Spheres.append(sphere)
                    
            return Spheres        
        
            
        def sphere_list_touching(self):
            """
            
            Generates a list of coordinates and radius of touching spheres.
        
            :try_number: number of attempties of sphere placement.
            :radius: mean sphere radius.
            :radius_std: sphere std radius.
            :side: maximum grid value.
            :return: sphere List.
            """ 
            
            Esferas = []
            
            for n in range(self.n_spheres):
                
                Esferas.append(self.sphere_generator())
        
            return Esferas
        
        def rhomb_sphere_pack(self):  
            """
            
            This function generates an orthorhombic sphere packing.
        

            :return: sphere packing array.
            """ 
            
            coords = []
            coord_x = 0
            coord_y = 0
            coord_z = 0
            
            Spheruls = Psgen.Spheres(self.side, 0, self.radius, 0, 
                                            0, self.phase_number)
            zeros = np.zeros((self.side, self.side, self.side), dtype = int)
            
            for x in range(int((self.side + self.radius * 2) / (self.radius * 2))):
                coord_y = 0
                for y in range(int((self.side + self.radius * 2) / (self.radius*2))):
                    coords.append([coord_x, coord_y, coord_z, self.radius])
                    coord_z = 0
                    for z in range(int((self.side + self.radius*2) / (self.radius*2))):
                        coords.append([coord_x, coord_y, coord_z, self.radius])
                        coord_z = coord_z + self.radius * 2 
                    coord_y = coord_y + self.radius * 2
                coords.append([coord_x, coord_y, coord_z, self.radius])    
                coord_x = coord_x + self.radius * np.sqrt(3) * 1.63

            coord_x = self.radius * np.sqrt(3) / 2 * 1.63
            coord_y = self.radius
            coord_z = self.radius          
            
            for x in range(int((self.side + self.radius*2) / (self.radius * 2))):
                coord_y = self.radius
                for y in range(int((self.side + self.radius*2) / (self.radius * 2))):
                    coords.append([coord_x, coord_y, coord_z, self.radius])
                    coord_z = self.radius
                    for z in range(int((self.side + self.radius*2) / (self.radius * 2))):
                        coords.append([coord_x, coord_y, coord_z, self.radius])
                        coord_z = coord_z + self.radius * 2 
                    coord_y = coord_y + self.radius * 2
                coords.append([coord_x, coord_y, coord_z, self.radius])    
                coord_x = coord_x + self.radius * np.sqrt(3) * 1.63

            return Spheruls.sphere_array(coords,zeros)
        
        
        def sphere_array(self, Sphere_List, array, silent = False):
            """
            
            Generates an array with a sphere list. An array must be provided:
            it can be a zero array or an array with spheres.
        
            :Sphere_List: list of spheres containg coordinates and radius.
            :side: array limits.
            :phi: desirable porosity.
            :array: zeros or previous array.
            :silent: no prints.
            :return: final array.
            """ 
            
            if self.compaction:
                for Sphere in Sphere_List:
                    Sphere[3] = Sphere[3] * self.comp_ratio
                

            x_ = np.linspace(0, self.side, self.side).astype(int)
            y_ = np.linspace(0, self.side, self.side).astype(int)
            z_ = np.linspace(0, self.side, self.side).astype(int)
            u,v,w = np.meshgrid(x_, y_, z_, indexing='ij') 
            d = np.copy(array).astype(np.int8)
            
            if not silent:
                print('')
                print("---------- Progress ----------")
                        
            for center in Sphere_List:
                
                c = np.power(u - center[0], self.phase_number) + np.power(
                    v-center[1], self.phase_number) + np.power(
                        w - center[2], self.phase_number)
                c1 = np.where(c <= center[3] * center[3], self.phase_number, 0)
                mask = (d == 0)
                d[mask] = c1[mask]
                progress = (1 - (np.count_nonzero(d == 0) / self.side ** 3))/(1 - self.phi)
                
                if not silent:
                    if int(progress * 100) % 5 == 0:
                        print(f"\r{str(int(progress*100))}%." , end="")
                if (np.count_nonzero(d == 0)/self.side ** 3) < (self.phi):
                    
                    break
            
            if not silent:
                print('')
                if progress < 1:
                    print('Porosity reached ' + str(
                        round((np.count_nonzero(d == 0)/ self.side ** 3), 2)) + ".")
                    print("If you desire to reach "
                          +str(self.phi)+""", please increase the tries number 
                          on sphere_list function parameter.""")
                else:
                    print("Done!")
                print(" ")
                                
            
            return d.astype(int)
        

        def shrubspherulstone_list(self, Sphere_list, shrubstone_array):
            """
            
            This function receives a list of random spheres and try to insert
            each one in an array with shurbs. If the sphere touch a shrub,
            it is deleted from the list, returning a new list of spheres.
        
            :Sphere_List: list of spheres containg coordinates and radius.
            :shrubstone_array: array with shrubs.
            :return: dictionary with updated sphere list.
            """           
                    
            self.shrubstone_array = shrubstone_array
            sphere_coords = []
            new_sphere_coords = []
            
            # For a single sphere, the function will extract all coordinates
            # and put it on a list.
            for s in range(len(Sphere_list)):
                
                sphere_coord = []
                zeros = np.zeros((self.side, self.side, self.side), dtype = int)
                Sphere = self.sphere_array([Sphere_list[s]], zeros, silent = True)
                
                x = 0
                
                for c in Sphere:
                    y = 0
                    
                    for c1 in c:
                        z = 0
                        
                        for c2 in c1:
                            
                            if c2 == self.phase_number:
                                sphere_coord.append([x,y,z])
                                
                            z += 1
                        y += 1
                    x += 1
                sphere_coords.append(sphere_coord)
            
            n = 0
            new_sphere_coords = {i: sphere_coords[i] for i in range(0, len(sphere_coords))}
            
            # If a single voxel of the sphere touch a shrubstone, the sphere
            # is removed from the list, returning an updated dictionary of
            # spheres.
            for sphere in sphere_coords:
                
                for coord in sphere:
                
                    if shrubstone_array[coord[0],coord[1],coord[2]] == self.shrub_number or shrubstone_array[coord[0],coord[1],coord[2]] == self.phase_number:
                    
                        try:
                            del new_sphere_coords[n]
                            break
                        
                        except:
                            pass          

                n += 1
              
            return new_sphere_coords
        
    
        def shrubspherulstone(self, new_sphere_coords):
            """
            
            Using the list of spheres provided by the function 
            shrubspherulstone_list, this function populates an shrubstone
            array with spheres, creating a shrubspherulstone.
            
            :new_sphere_coords: list of spheres containg coordinates and radius.
            :return: final array.
            """   
            
            print('')
            print("---------- Progress ----------")
            n= 0
            
            for sphere in new_sphere_coords.values():
                
                progress = n / len(new_sphere_coords) * 100
                for coord in sphere:
                    if int(progress) % 5 == 0:
                        print(f"\r{str(int(progress))}%."  , end = "")                    
                    try:
                        self.shrubstone_array[coord[0],coord[1],coord[2]] = self.phase_number
                    except:
                        pass
                n += 1
            
            print('Done!')
            
            return self.shrubstone_array
        

    class Cubes():
        """
        
        This class has several functions to place cubes in 3d array model. The
        cubes represents diverse ways of dolomite replacement or cimentation.
        """

        def __init__(self, side, side_cube, side_cube_std, phi,
                     phase_number = 1, cal_tou = True, sphere_number = 2 , shrub_number = 3):
            """
            
            :side: maximum grid value.
            :side_cube: single cube side.
            :side_cube_std: single cube std side.
            :phi: minimum porosity.
            :phase_number: the cube voxels will receive the number 1 by default.
            :cal_tou: this parameter sets if the spheres or shrubs provided by a
            previous populated array will be touched by cubes.
            :sphere number: in the case of a sphere populated array be used,
            the phase number of spheres should be informed.
            """
            self.phase_number = phase_number
            self.side = side
            self.side_cube = side_cube
            self.side_cube_std = side_cube_std
            self.phi = phi     
            self.cal_tou = cal_tou
            self.sphere_number = sphere_number
            self.shrub_number = shrub_number


        def unit_vector(self, vector):
            """
            
            Returns the unit vector of the vector."""
                        
            return vector / np.linalg.norm(vector)

        
        def angle_between(self, v1, v2):
            """
            
            Finds angle between two vectors."""
            
            v1_u = self.unit_vector(v1)
            v2_u = self.unit_vector(v2)
            
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

        
        def x_rotation(self, vector, theta):
            """
            
            Rotates 3-D vector around x-axis"""
            
            R = np.array([[1, 0, 0],[0, np.cos(theta), -np.sin(theta)],
                          [0, np.sin(theta), np.cos(theta)]])
            
            return np.dot(R, vector)

        
        def y_rotation(self, vector, theta):
            """
            
            Rotates 3-D vector around y-axis"""
            
            R = np.array([[np.cos(theta), 0, np.sin(theta)] ,[0, 1, 0] ,
                          [-np.sin(theta), 0, np.cos(theta)]])
            
            return np.dot(R,vector)

        
        def z_rotation(self, vector, theta):
            """
            
            Rotates 3-D vector around z-axis"""
            
            R = np.array([[np.cos(theta), -np.sin(theta), 0],
                          [np.sin(theta), np.cos(theta), 0],[0, 0, 1]])
            
            return np.dot(R,vector)
        
        def rotation_correction(self,array):
            """
            
            After rotation, cubes tend to develop some holes inside.
            This function fill the holes.
            
            :array: 3d array with cubes.
            :return: 3d array with corrected cubes.
            """ 
            
            array_dilated = scipy.ndimage.binary_dilation(array,iterations=1, border_value = 0).astype(array.dtype)
            Result = scipy.ndimage.binary_erosion(array_dilated,iterations=1, border_value = 0).astype(array_dilated.dtype)
            
            return Result
            
        def cube_generator(self, rotation, max_rotation):
            """
            
            Generates an cube within provided array limits with aleatory
            coordinates and rotation.
            
            :rotation: sets if the cubes will rotate.
            :max_rotation: maximum rotation of cubes.
            :return: radius in which the cube is inscribed, center list 
                    coordinate of cube after random rotation, random 
                    coordinate list before rotation, axis random rotation
                    angle list, and new random side lengh.
            """ 
            
            side_cube = int(np.random.normal(self.side_cube, self.side_cube_std))
            radius_ins = int(self.side_cube * np.sqrt(2) / 2)
        
            random_coord_x = np.random.randint(-self.side_cube,
                                               self.side + self.side_cube)
            random_coord_y = np.random.randint(-self.side_cube,
                                               self.side + self.side_cube)
            random_coord_z = np.random.randint(-self.side_cube,
                                               self.side + self.side_cube)
            if rotation:
                rotation_x = int(np.random.randint(-max_rotation, max_rotation))
                rotation_y = int(np.random.randint(-max_rotation, max_rotation))
                rotation_z = int(np.random.randint(-max_rotation, max_rotation))
                
            else:
                rotation_x = 0
                rotation_y = 0
                rotation_z = 0
                
            center_cube = [int(random_coord_x + self.side_cube/2),
                           int(random_coord_y + self.side_cube/2),
                           int(random_coord_z + self.side_cube/2)]
            
            rotated_center_cube = (self.x_rotation(center_cube, 
                                                   math.radians(rotation_x / math.pi)))
            rotated_center_cube = (self.y_rotation(rotated_center_cube,
                                                   math.radians(rotation_y / math.pi)))
            rotated_center_cube = (self.z_rotation(rotated_center_cube,
                                                   math.radians(rotation_z / math.pi)))
            
            return [radius_ins, rotated_center_cube,
                    [random_coord_x, random_coord_y, random_coord_z],
                    [rotation_x, rotation_y, rotation_z], side_cube]
       
        
        def cube_generator_biased(self):
            """
            
            Generates an cube within provided limits with biased
            coordinates and aleatory rotation. The cube will be placed according
            to a center coordinate, considering a normal probability function and
            the center accouting to the average.
        
            :return: radius in which the cube is inscribed, center list coordinate of 
                    cube after random rotation, random coordinate list before rotation, 
                    axis random rotation angle list, and new random side lengh.
            """ 
            
            side_cube = int(np.random.normal(self.side_cube, self.side_cube_std))
            radius_ins = int(self.side_cube * np.sqrt(2)/2)
            random_coord_x = self.side * self.het * np.random.randn() + self.center[0]
            random_coord_y = self.side * self.het * np.random.randn() + self.center[1]
            random_coord_z = self.side * self.het * np.random.randn() + self.center[2]
            rotation_x = int(np.random.randint(-90, 90))
            rotation_y = int(np.random.randint(-90, 90))
            rotation_z = int(np.random.randint(-90, 90))
            center_cube = [int(random_coord_x + self.side_cube / 2),
                           int(random_coord_y + self.side_cube / 2),
                           int(random_coord_z + self.side_cube / 2)]
            rotated_center_cube = (self.x_rotation(center_cube, 
                                                   math.radians(rotation_x / math.pi)))
            rotated_center_cube = (self.y_rotation(rotated_center_cube,
                                                   math.radians(rotation_y / math.pi)))
            rotated_center_cube = (self.z_rotation(rotated_center_cube,
                                                   math.radians(rotation_z / math.pi)))
            
            return [radius_ins, rotated_center_cube,
                    [random_coord_x, random_coord_y, random_coord_z], 
                    [rotation_x, rotation_y, rotation_z], side_cube]
        
        
        def cube_list(self, try_number, bias = False,
                               het = 1,center = [0,0,0],
                               rotation = True, max_rotation = 90):
            """   
            
            Generates a cube list.
            
            :het: heterogeneity factor.
            :center: center is the coordinate of maximum probability of a
                    cube to be placed.            
            :bias: true will generate heterogeneos cube distribution
            :try_number: number of attempties of cube placement (some of them are placed
                        outside the array grid after rotation).
            :return: a list of cubes with the outputs of cube_generator function.
            """ 
        
            self.het = het
            self.center = center
            Cubes = []
            self.bias = bias
            cube_range = self.side + self.side_cube
            
            for n in range(try_number):   
                
                if self.bias:
                    cube = self.cube_generator_biased()
                else:
                    cube = self.cube_generator(rotation, max_rotation)
                if cube[1][0] < cube_range and cube[1][1] < cube_range and cube[1][2] <cube_range:
                    if cube[1][0] > -self.side_cube / 2 and cube[1][1] > - self.side_cube / 2 and cube[1][2] > -self.side_cube / 2:
                        Cubes.append(cube)
                    
            return Cubes

        
        def cubes_array_untouching(self,center_cube,rotations, new_side_cube, array):
            """
            
            Insert a cube in an 3D array, testing if it doesn´t touch any previous component.
            Inputs are provided by the cube generator in addition to an 3d array.
            
            :center_cube: coordinate of cube vertice provided by the cube list.
                        funcion.
            :rotations: rotations provided by the cube list.
            :new_side_cube: side changed by the random probabilitity set
                            on cube generator function.
            :array: array of zeros or a previous populated array.
            :return: 3d array with a new cube.
            """ 
            
            # The cube will be generated as an xyz grid. After that, the
            # grid coordinate grip will be converted into a list.
            x, y, z= np.meshgrid(np.arange(center_cube[0], center_cube[0] + 
                                           new_side_cube),
                                  np.arange(center_cube[1], center_cube[1] + 
                                            new_side_cube),
                                  np.arange(center_cube[2], center_cube[2] + 
                                            new_side_cube))
            list_coord = list(np.stack([x.flatten(), y.flatten(), z.flatten()], axis = -1))
            
            list_rotated = list(map(lambda value: self.x_rotation(value,math.radians(rotations[0] / math.pi)),list_coord))
            list_rotated = list(map(lambda value: self.y_rotation(value,math.radians(rotations[1] / math.pi)),list_rotated))
            list_rotated = list(map(lambda value: self.z_rotation(value,math.radians(rotations[2] / math.pi)),list_rotated))
            
            n = 0
            for coord in list_rotated:
                list_rotated[n][0] = coord[0] 
                list_rotated[n][1] = coord[1] 
                list_rotated[n][2] = coord[2] 
                n += 1

            list_rotated = [coord for coord in list_rotated if coord[0] <= self.side and coord[1] <= self.side and coord[2] <= self.side]
            list_rotated = [coord for coord in list_rotated if coord[0] >= 0 and coord[1] >= 0 and coord[2] >= 0]
            
            test = True
            
            # The function tests if a cube will touch a previous component.
            for coord in list_rotated:
                if array[int(coord[0])][int(coord[1])][int(coord[2])] == self.sphere_number or array[int(coord[0])][int(coord[1])][int(coord[2])] == self.shrub_number or array[int(coord[0])][int(coord[1])][int(coord[2])] == self.phase_number:
                    test = False
                    break
            
            if test:
                for coord in list_rotated:
        
                    array[int(coord[0])][int(coord[1])][int(coord[2])] = self.phase_number
                    
            return array

        
        def cubes_array_touching(self, center_cube, rotations, new_side_cube, array):
            """
            
            Insert a cube in an 3D array. Inputs are provided by the cube 
            generator in addition to an 3d array.
            
            :center_cube: coordinate of cube vertice provided by the cube list.
                        funcion.
            :rotations: rotations provided by the cube list.
            :new_side_cube: side changed by the random probabilitity set
                            on cube generator function.
            :array: array of zeros or a previous populated array.   
            :return: 3d array with a new cube.
            """ 
            
            x, y, z= np.meshgrid(np.arange(center_cube[0], center_cube[0] + new_side_cube),
                                  np.arange(center_cube[1], center_cube[1] + new_side_cube),
                                  np.arange(center_cube[2], center_cube[2] + new_side_cube))
            list_coord = list(np.stack([x.flatten(), y.flatten(), z.flatten()], axis = -1))
            list_rotated = list(map(lambda value: self.x_rotation(value,math.radians(rotations[0] / math.pi)),list_coord))
            list_rotated = list(map(lambda value: self.y_rotation(value,math.radians(rotations[1] / math.pi)),list_rotated))
            list_rotated = list(map(lambda value: self.z_rotation(value,math.radians(rotations[2] / math.pi)),list_rotated))
            
            n = 0
            for coord in list_rotated:
                list_rotated[n][0] = coord[0] 
                list_rotated[n][1] = coord[1] 
                list_rotated[n][2] = coord[2] 
                n += 1
         
            list_rotated = [coord for coord in list_rotated if coord[0] <= self.side and coord[1] <= self.side and coord[2] <= self.side]
            list_rotated = [coord for coord in list_rotated if coord[0] >= 0 and coord[1] >= 0 and coord[2] >= 0]
            
            # This test is performed if cal_tou is set as False, in other words,
            # if the spheres or shrubs cannot be replaced by dolomite.
            if not self.cal_tou:
                test = True
                for coord in list_rotated:
                    try:
                        if array[int(coord[0])][int(coord[1])][int(coord[2])] == self.sphere_number or array[int(coord[0])][int(coord[1])][int(coord[2])] == self.shrub_number:
                            test = False
                            break
                    except:
                        pass
                
                if test:
                    for coord in list_rotated:
                        try:
                            array[int(coord[0])][int(coord[1])][int(coord[2])] = self.phase_number
                        except:
                            pass
            else:
                for coord in list_rotated:
                    try:
                        array[int(coord[0])][int(coord[1])][int(coord[2])] = self.phase_number
                    except:
                        pass
                    
            return array
        
        def touching_cubes(self, cube_list, array):
            """
            
            Inserts a cube in an 3D array. Inputs are provided by the cube 
            generator in addition to an 3d array.
        
            :cube_list: provided by cube_list_touching function
            :return: 3d array with a new cube.
            """     
            
            array_2 = np.copy(array)
            Cubes_2 = self.cubes_array_touching(cube_list[0][2], cube_list[0][3],
                                                cube_list[0][4], array_2)
            print('')
            print("---------- Progress ----------")
                        
            for cube in cube_list[1:]:
        
                Cubes_2 = self.cubes_array_touching(cube[2], cube[3], cube[4], Cubes_2)
                progress = (1-(np.count_nonzero(Cubes_2==0)/self.side**3))/(1-self.phi)
                
                if int(progress*100)%5 == 0:
                    print(f"\r{str(int(progress*100))}%." , end="")
                if (np.count_nonzero(Cubes_2==0)/self.side**3) < self.phi:
                    
                    break
            
            Cubes_2[Cubes_2 == self.sphere_number] = 0
            Cubes_2[Cubes_2 == self.shrub_number] = 0     
            Result = self.rotation_correction(Cubes_2)
            Result[array == self.sphere_number] = self.sphere_number
            Result[array == self.shrub_number] = self.shrub_number
            print('')
            
            if progress<1:
                print('Porosity reached ' + str(round((np.count_nonzero(Cubes_2==0)/self.side**3),2)) + ".")
                print("""If you desire to reach the input porosity, please 
                      increase the cubes number on cube_list function parameter.
                      """)
                if self.bias:
                    print("Biased models tend to not reach low porosity.")
            else:
                print("Done!")
            print(" ")     
            
            return Result


        def untouching_cubes(self, cube_list,array):
            """
            
            Implements a looping to insert untouching cubes in an 3d array up to
            a porosity limit.
            
            :cube_list: provided by cube_list_touching function
            :array: 3d zeros array or previously populated array.
            :return: the final 3d array
            """     
            
            array_2 = np.copy(array)
            Cubes_2 = self.cubes_array_untouching(cube_list[0][2], cube_list[0][3],
                                                  cube_list[0][4], array_2)

            print('')
            print("---------- Progress ----------")
            for cube in cube_list[1:]:
                
                progress = (1 - (np.count_nonzero(Cubes_2 == 0) / 
                                 self.side ** 3)) / (1-self.phi)
                if int(progress * 100) % 5 == 0:
                    print(f"\r{str(int(progress*100))}%." , end="")
                Cubes_2 = self.cubes_array_untouching(cube[2], cube[3],
                                                      cube[4], Cubes_2)
                if (np.count_nonzero(Cubes_2 == 0) / self.side ** 3) < self.phi:
        
                    break
            
            Cubes_2[Cubes_2 == self.sphere_number] = 0
            Cubes_2[Cubes_2 == self.shrub_number] = 0
            Result = self.rotation_correction(Cubes_2)
            Result[array == self.sphere_number] = self.sphere_number
            Result[array == self.shrub_number] = self.shrub_number
            
            print('')
            if progress<1:
                print('Porosity reached ' + str(
                    round((np.count_nonzero(Result == 0) / self.side ** 3), 2)) + ".")
                print("""If you desire to reach the input porosity, please 
                      increase the cubes number on cube_list function parameter.
                      """)
                if self.bias:
                    print("Biased models tend to not reach low porosity.")
            else:
                print("Done!")
            print(" ")   

            return Result

        
        def cubes_regular_spacing(self, gap, max_rotation = 30, 
                                  rotation = False, shift_position = False, 
                                  shift_value = 10):
            """
            
            Generates an list of regularly spaced cubes. They can touch
            each one.
        
            :gap: gap between cubes.
            :max_rotation: maximum rotation of cubes.
            :rotation: if true, perform rotation of cubes.
            :shift_position: aplies a random shift on cube position.
            :shift_value: maximum shift applied to the cube.
            :return: random coordinate list before rotation,
                axis random rotation angle list,
                and new random side lengh.
            """     
            
            x, y, z= np.meshgrid(np.arange(0, self.side,self.side_cube +
                                           gap),
                                  np.arange(0, self.side,self.side_cube +
                                            gap),
                                  np.arange(0, self.side,self.side_cube +
                                            gap))
      
            list_coord = np.stack([x.flatten(), y.flatten(), z.flatten()], 
                                  axis = -1)
            
            n=0
            result = []
            
            for coord in list_coord:
                
                if shift_position:

                    new_coord_x = int(coord[0] + np.random.randint(-shift_value, shift_value))
                    new_coord_y = int(coord[1] + np.random.randint(-shift_value, shift_value))
                    new_coord_z = int(coord[2] + np.random.randint(-shift_value, shift_value))
                                     
                else:
                    new_coord_x = int(list_coord[n][0])
                    new_coord_y = int(list_coord[n][1])
                    new_coord_z = int(list_coord[n][2])
                    
                if rotation:
                    rotation_x = int(np.random.randint(-max_rotation, max_rotation))
                    rotation_y = int(np.random.randint(-max_rotation, max_rotation))
                    rotation_z = int(np.random.randint(-max_rotation, max_rotation))
                    
                else:
                    rotation_x = 0
                    rotation_y = 0
                    rotation_z = 0

            
                side_cube_single = int(np.random.normal(self.side_cube ,self.side_cube_std))
                result.append([[new_coord_x, new_coord_y, new_coord_z],
                               [rotation_x, rotation_y, rotation_z], 
                               side_cube_single])
                n += 1
            
            return result
        
                
        def touching_regular_cubes(self, cube_regular_list, array):
            """
            
            Insert regularly spaced cubes in an array. The cubes can touch
            each one.
        
            :cube_regular_list: regularly spaced cubes list provided by 
                cubes_regular_spacing function.
            :return: the final 3d array
            """   
           
            print('')
            print("---------- Progress ----------")
            n = 0
            
            array_2 = np.copy(array)
            Cubes_2 = self.cubes_array_touching(cube_regular_list[0][0],
                                                cube_regular_list[0][1],
                                                cube_regular_list[0][2],array_2)
        
            for cube in cube_regular_list[1:]:
                   
                Cubes_2 = self.cubes_array_touching(cube[0],cube[1],cube[2],Cubes_2)
                
                progress = n/len(cube_regular_list)
                if int(progress*100)%5 == 0:
                    print(f"\r{str(int(progress*100))}%." , end="")
                n += 1
            Cubes_2[Cubes_2 == self.sphere_number] = 0
            Cubes_2[Cubes_2 == self.shrub_number] = 0
            Result = self.rotation_correction(Cubes_2)
            Result[array == self.sphere_number] = self.sphere_number
            Result[array == self.shrub_number] = self.shrub_number
            print("")
            print("Done!")            
            return Result


        def untouching_regular_cubes(self, cube_regular_list, array):
            """
            
            Insert regularly spaced cubes in an array. 
        
            :cube_regular_list: regularly spaced cubes list provided by 
                cubes_regular_spacing function.
            :array: 3d zeros array or previously populated array.
            :return: the final 3d array
            """   
            array_2 = np.copy(array)
            Cubes_2 = self.cubes_array_untouching(cube_regular_list[0][0],
                                                cube_regular_list[0][1],
                                                cube_regular_list[0][2],
                                                array_2 )
            print('')
            print("---------- Progress ----------")
            n = 0
            
            for cube in cube_regular_list[1:]:
                   
                Cubes_2 = self.cubes_array_untouching(cube[0], cube[1], 
                                                      cube[2], Cubes_2)
                progress = n / len(cube_regular_list)
                if int(progress * 100) % 5 == 0:
                    print(f"\r{str(int(progress*100))}%." , end="")
                n += 1
            
            Cubes_2[Cubes_2 == self.sphere_number] = 0
            Cubes_2[Cubes_2 == self.shrub_number] = 0
            Result = self.rotation_correction(Cubes_2)
            Result[array == self.sphere_number] = self.sphere_number
            Result[array == self.shrub_number] = self.shrub_number
            
            print("")
            print("Done!")
            
            return Result
          
    
    class Shrubs():
        """
        
        This class built shrubstone models. I provide an initial shape that
        can be stretched or flatened. The shrubs nucleate in a random coordinate.
        They also can nucleate after a datum, wich is usefull to built models
        with spherulites.
        """
        
        def __init__(self, height, height_std, side, ratio = 1, 
                     inclination_min = 80, dat_set = False, datum = 0,
                     phase_number = 3, spherulite_number = 2):
            """
            
            :height: shrub height.
            :height_std: shrub std height.
            :side: side of array.
            :ratio: it defines shape, 0 more elongated, more than 1 will
            generate a flat shrub.
            :inclination: it sets the inclination of shrub.
            :dat_set: it sets if shurbs will nucleate after a defined datum 
            or ramdomly.
            :datum: if dat_set is true, the nucleation datum should be
            provided. The shrubs will nucleate after the datum.
            :spherulite_number: if an array with spherulites is used as input,
            it sets the spherulite on it. The default is 2.
            :phase_number: the shrub number on models.
            """
            
            self.height = height
            self.height_std = height_std
            self.side = side
            self.ratio = ratio
            self.inclination_min = inclination_min    
            self.dat_set = dat_set
            self.datum = datum
            self.phase_number = phase_number
            self.spherulite_number = spherulite_number
            
        def shrub_generator(self):
            """
         
            Generates a shrub list used by other functions.

            :return: the shrub list used by other functions.
            """ 
            

            from scipy.interpolate import interp1d  
            

            # The shape of shrubs was provided according the relative change
            # of their radius.
            Shrub_Shape_radius = [0, 65, 90, 105, 115, 127.5, 135,
                                  137.5, 135, 130, 115, 60, 0]
            Shrub_Shape_height = [0, 50, 100, 150, 200, 250, 300,
                                  350, 400, 450, 500, 550, 570]
           
            height_proportion = self.height / max(Shrub_Shape_height)
         
            if self.dat_set:
                y_factor = np.random.randint(self.datum, self.side)         

            else:
                y_factor = np.random.randint(-self.height ,self.side)           

            Shrub_Shape_radius = [int(x * height_proportion *
                                      self.ratio) for x in Shrub_Shape_radius]
            Shrub_Shape_height = [int(x * height_proportion
                                      ) for x in Shrub_Shape_height]        

            f = interp1d(Shrub_Shape_height, Shrub_Shape_radius,
                         kind= 'quadratic')
            Shrub_Shape_height_new = np.linspace(0, self.height - 1,
                                                 num=self.height,
                                                 endpoint = True)
            Shrub_Shape_radius_new = f(Shrub_Shape_height_new)
          
            x = np.random.randint(-max(Shrub_Shape_radius) / 2,
                                  self.side + max(Shrub_Shape_radius) / 2)
            z = np.random.randint(-max(Shrub_Shape_radius) / 2,
                                  self.side + max(Shrub_Shape_radius) / 2)
          
            n = 0
            list_coord = []
           
            for radius in Shrub_Shape_radius_new:
                list_coord.append((x, Shrub_Shape_height_new[n], z))
                n += 1
               
            inclination_x = np.random.randint(self.inclination_min, 90)
            x_rotated = [math.tan(math.radians(90 - inclination_x)) *
                         (coord[1] - min(Shrub_Shape_height_new)) +
                         coord[0] for coord in list_coord]
            inclination_z = np.random.randint(self.inclination_min, 90)
            z_rotated = [math.tan(math.radians(90 - inclination_z)) *
                         (coord[1] - min(Shrub_Shape_height_new)) +
                         coord[2] for coord in list_coord]
         
            n = 0
            result = []
          
            for y_n in list_coord:
                result.append((int(x_rotated[n]), int(y_n[1]+y_factor),
                               int(z_rotated[n]), Shrub_Shape_radius_new[n]))
                n += 1
          
            return result

        
        def single_shrub(self, Shrub_List, array):
            """

            Inserts a single shrub in a 3d array. The shrubs are allowed
            to replace previous ones.
   
            :Shrub_List: list provided by shrub_generator function.
            :array: an array with zeros or other shrubs.

            :return: an array with a new shrub.
            """ 
        
            x_ = np.linspace(0,self.side, self. side).astype(int)
            y_ = np.linspace(0,self.side, self.side).astype(int)
            u,v = np.meshgrid(x_, y_, indexing='ij')
            d = np.copy(array).astype(np.int8)
            
            # The shrub will be built by print a sphere in each x slice,
            # from bottom to the top.
            for center in Shrub_List:

                if (center[1] >= 0) and (center[1] < self.side):

                    c = np.power(u - center[0], 2) + np.power(v - center[2], 2)
                    c1 = np.where(c <= center[3] ** 2, self.phase_number, 0)           
                    mask = (d[center[1]] == 0)
                    d[center[1]][mask] = c1[mask]
               
            return d.astype(int)
             
        
        def shrubstone(self, array, phi):
            """
            
            Inserts all shrubs provided by the shrub list, invoking shrub_generator 
            and single_shrub functions until the target porosity is reached.
        
            :array: an array with zeros or other shrubs.
            :phi: target porosity.
            :return: an array with final shrubstone model.
            """     

            print('')
            print("---------- Progress ----------")

            n = 0
            
            if self.dat_set:
                phi = phi + (self.datum / self.side)
            
            print(" If datum option is set, the porosity will be approximated")
            print(" only after the datum.")
                
            while np.count_nonzero(array) < (self.side ** 3) * (1 - phi):

                progress = (1 - (np.count_nonzero(array == 0) / 
                                 self.side ** 3)) / (1 - phi)
                if int(progress * 100) % 5 == 0:
                    print(f"\r{str(int(progress*100))}%." , end="")              
                list_coord = self.shrub_generator()
                array = self.single_shrub(list_coord, array)
                n += 1

            print("")
            print("Done!")
            
            return array
        
        
    class Dissolution():
        """
        
        Dissolution class dissolves minerals randomly. The phase, intensity,
        and dissemination can be set. This function can be used to replaces
        a mineral phase with a new mineral, for instance silicification, which 
        is very common on shrubs and spherulites in Pre-salt.
        """     

        def __init__(self, side, phi, mineral_dissolved):
            """
            
            :side: side of array.
            :array: an array with a previous built model.
            :mineral_dissolved: number with mineral phase to be partially
                                dissolved (by default,
                                dolomite = 1, spherulite = 2, and shrub = 3)
            """
            
            self.side = side
            self.phi = phi 
            self.mineral_dissolved = mineral_dissolved  
            
        
        def diss_coord_list(self, array, prob_diss = .5, diss_number = 0):
            """
            
            Function that returns a list of dissolution coordinates.
        
            :prob_diss: value which controls the probability of enlargement 
                        of dissolution pores, the nearest of 1, largest 
                        and less disseminate will be the pore. Lower values
                        will return more disseminated and smaller pores.
                        0.5 means 50% chance of enlargment.
            :diss_number: number to be used in array, default is zero.
            :return: a list with coordinates.
            """  
            
            self.array = array
            self.prob_diss = prob_diss
            self.diss_number = diss_number
            rand_coord_list = []
            rand_coord_list.append(list(np.random.choice(self.side - 1, 3)))

            print('')
            print("---------- Progress ----------")
            
            # The function has a probability of dissolution, which defines
            # if a previous por will be enlarged or if a new nucleous of
            # dissolution will be formed.
            for n in range(100000000):
                random_coord = list(np.random.choice(self.side - 1, 3))
                if self.array[random_coord[0], random_coord[1], random_coord[2]] == self.mineral_dissolved:
                    enlarge_choice = np.random.choice(2, 1, p = [1 - self.prob_diss, self.prob_diss])
            
                    if enlarge_choice == 0:
                         if random_coord not in rand_coord_list:
                                
                            rand_coord_list.append(random_coord)
                    else:
                        idx_list_coord = np.random.choice(len(rand_coord_list))
                        position_choice = np.random.randint(6)
                        if position_choice == 0:
                            random_coord = [rand_coord_list[idx_list_coord][0] - 1,
                                            rand_coord_list[idx_list_coord][1],
                                            rand_coord_list[idx_list_coord][2]]
                        elif position_choice == 1:
                            random_coord = [rand_coord_list[idx_list_coord][0] + 1,
                                            rand_coord_list[idx_list_coord][1],
                                            rand_coord_list[idx_list_coord][2]]
                        elif position_choice == 2:
                            random_coord = [rand_coord_list[idx_list_coord][0], 
                                            rand_coord_list[idx_list_coord][1] - 1,
                                            rand_coord_list[idx_list_coord][2]]
                        elif position_choice == 3:
                            random_coord = [rand_coord_list[idx_list_coord][0], 
                                            rand_coord_list[idx_list_coord][1] + 1,
                                            rand_coord_list[idx_list_coord][2]]
                        elif position_choice == 4:
                            random_coord = [rand_coord_list[idx_list_coord][0],
                                            rand_coord_list[idx_list_coord][1],
                                            rand_coord_list[idx_list_coord][2] - 1]
                        elif position_choice == 5:
                            random_coord = [rand_coord_list[idx_list_coord][0],
                                            rand_coord_list[idx_list_coord][1],
                                            rand_coord_list[idx_list_coord][2] + 1]
                        try:
                            if random_coord not in rand_coord_list and array[random_coord[0], random_coord[1], 
                                  random_coord[2]] == self.mineral_dissolved:
                                rand_coord_list.append(random_coord)
                        except:
                            pass
                
                progress = len(rand_coord_list) / (self.side * self.side * self.side * self.phi) * 100
                
                if int(progress) % 5 == 0:
                    print(f"\r{str(int(progress))}%." , end="")                 
                    
                if len(rand_coord_list) > (self.side * self.side * self.side * self.phi):
                    break
            
            print('Done!')
            
            return rand_coord_list
        
        
        def dissolution_array(self, diss_coord_list):
            """
            
            Function that dissolves a mineral phase, such as dolomite or shrub. The funcion also can
            be used to perform replacement by silica, which is very common in Pre-salt.
        
            :diss_coord_list: coordenate list provided by the diss_coord_list funcition.
            :diss_number: number to be used in array, default is zero.
            :return: a list with coordinates.
            """
            
            for coord in diss_coord_list:
                try:
                    self.array[coord[0],coord[1],coord[2]] = self.diss_number
                except:
                    pass
            return self.array
