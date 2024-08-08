import numpy
import random
from slider_buttons import slider_window


#global varibles not editable during simualtion
NUMCELL = 30 #variable determining the width and the leght of the grid

#variable determining how much of the vegetob density will be transformed into energy for the erbast
VEGETOB_GAIN = 4/7 

#global varibles editable during simualtion
AGING_ERB = 10
AGING_CAR = 1
MAX_HERD = 20
MAX_PRIDE = 50
MAX_ENERGY_ERB= 125
MAX_ENERGY_CAR = 287
PREDATOR_ADVANTAGE = 9
BOREDOM = 4

#increasing these variable increases the probability for a creature to spawn on a cell (1 means that for every cell a creature will spawn)
POBABILITY_SPAWN_ERB = 0.4
POBABILITY_SPAWN_CAR = 0.3

#set variable dimension to avoid calling the range function to many times
dimension = range(1, NUMCELL-1, 1) #kept NUMCELL only in print_grid and create_grid

#initialize cells list, the main list that will save all the cell objects
cells = []


class Erbast:
    def __init__(self, energy):
        self.MAXLIFE = numpy.random.randint(1, 100) #maxlife attribute is set upon creation of any Erbast or Carviz object
        self.AGE = 0
        self.SOCIALATTITUDE = numpy.random.randint(2) #chooses between 0 and 1
        self.ENERGY = energy

class Carviz:
    def __init__(self, energy):
        self.ENERGY = energy
        self.MAXLIFE = numpy.random.randint(76) 
        self.AGE = 0
        self.SOCIALATTITUDE = numpy.random.randint(2)
        self.bored = 0 #setup an attribute for when a carviz gets bored

class Cell():
    def __init__(self, material, coordinates):
        self.erbast = [] #list containig all erbast objects present in the cell
        self.carviz = [] #list containig all carviz objects present in the cell
        self.moved  = False
        self.value = None #used in graphics file
        
        self.vegetob = 0
        self.coordinates = coordinates

        self.material = material

def neighbors(x, y): #x = col, y = row
    #the function's aim is to create a list with all the cells in range (x-1, x+2) and (y-1, y+2) that have material = 'ground'
    coords = [(x1, y1)
              for x1 in range(x-1, x+2)
              for y1 in range(y-1, y+2)
              if (x1 != x or y1 != y) and
              0 <= x1 < NUMCELL and
              0 <= y1 < NUMCELL]
    #coords = [(1, 1), (1, 2), (1, 3)...]
    #If you don't need to check whether it is ground or water, comment the
    #following lines.
    neighbor_cells = []
    for coord_tuple in coords:
        cell = cells[coord_tuple[1]][coord_tuple[0]]
        if cell.material == "ground":
            neighbor_cells.append(cell)

    return neighbor_cells

def create_grid(cells, NUMCELL):
    #the function's aim is to create a NUMCELLxNUMCELL grid made of Cell classes with a random decision between their materials
    for i in range(NUMCELL):
        row = []
        for j in range(NUMCELL):
            if i == 0 or j == 0 or i == NUMCELL - 1 or j == NUMCELL - 1: #this if statement checks if the current cell is a border cell in which case the material is set to 'water'
                row.append(Cell("water", [i, j]))
                
            else: #meaning we are not at the border
                row.append(Cell(random.choices(["water", "ground"], weights=[0.2, 0.8])[0], [i,j])) #here happens the random decision between materials 
        cells.append(row)

def grow(cells):
    # this function loops through the whole grid adding 1 to the vegetob density, 
    # increasing the erbast and carviz ages, 
    # decreasing the energy by aging if the age is a multiple of 10
    # reducing the erbast and carivz energy by 1
    for row in dimension:
        for col in dimension:
            if cells[row][col].material == "ground" and not cells[row][col].erbast:
                if cells[row][col].vegetob < 100:
                    cells[row][col].vegetob += 1

            if cells[row][col].erbast:
                for i in range(len(cells[row][col].erbast)):

                    if cells[row][col].erbast[i].AGE < cells[row][col].erbast[i].MAXLIFE:
                        cells[row][col].erbast[i].AGE +=1

                    if cells[row][col].erbast[i].AGE % 10 == 0 :
                        if cells[row][col].erbast[i].ENERGY - AGING_ERB >= 0:
                            cells[row][col].erbast[i].ENERGY -= AGING_ERB
                        else: 
                            cells[row][col].erbast[i].ENERGY = 0

                    if cells[row][col].erbast[i].ENERGY > 2:
                        if cells[row][col].erbast[i].ENERGY - 1 >= 0:
                            cells[row][col].erbast[i].ENERGY -= 1
                        else:
                            cells[row][col].erbast[i].ENERGY = 0

            if cells[row][col].carviz:
                for i in range(len(cells[row][col].carviz)):

                    if cells[row][col].carviz[i].AGE < cells[row][col].carviz[i].MAXLIFE:
                        cells[row][col].carviz[i].AGE +=1

                    if cells[row][col].carviz[i].AGE % 10 == 0:
                        if cells[row][col].carviz[i].ENERGY - AGING_CAR >= 0:
                            cells[row][col].carviz[i].ENERGY -= AGING_CAR
                        else:
                            cells[row][col].carviz[i].ENERGY = 0

                    if cells[row][col].carviz[i].ENERGY > 2:
                        if cells[row][col].carviz[i].ENERGY - 1 >=0:
                            cells[row][col].carviz[i].ENERGY -= 1
                        else:
                            cells[row][col].carviz[i].ENERGY = 0

def death_birth(cells):
    # it is the last function that gets called during the 'day cycle' 
    # and is responsible for everything that has to do with eliminating and giving birth to creatures 
    for row in dimension:
        for col in dimension:
            if cells[row][col].erbast:

                #in case a herd with more components than allowed is found its dimension is brought back into the limits stated by the variable MAX_HERD
                if len(cells[row][col].erbast) >= MAX_HERD:
                    slice_index = len(cells[row][col].erbast)//2
                    cells[row][col].erbast = cells[row][col].erbast[slice_index:]

                dead_erbasts = [item for item in cells[row][col].erbast if item.AGE == item.MAXLIFE] #modify dead erbast, remove all items with age != maxlife (list with dead by reaching lifetime)
                neigh_coords_ = neighbors(col, row) #we get the neighbours in order to find the spawn choice
                
                if neigh_coords_: 
                    for erbast in dead_erbasts:
                        spawn_choices = random.choices(neigh_coords_, k=2) # decide 2 random neighbors to spawn the offsprings
                        spawn_choices[0].erbast.append(Erbast(erbast.ENERGY // 2)) # create new Erbasts with energy set to be half of the parent's 
                        spawn_choices[1].erbast.append(Erbast(erbast.ENERGY // 2))
                        cells[row][col].erbast.remove(erbast) #remove the dead erbast 

                    dead_erbasts_energy = [item for item in cells[row][col].erbast if item.ENERGY <= 0] #list with all the erbasts who died because of low energy 
                    for erbast in dead_erbasts_energy:
                        spawn_choices = random.choices(neigh_coords_, k=2)
                        # when a creature dies from low energy it's prole can't of course inherit the enrgy so it is chosen at random 
                        spawn_choices[0].erbast.append(Erbast(energy=numpy.random.randint(0, 42))) 
                        spawn_choices[1].erbast.append(Erbast(energy = numpy.random.randint(0, 42)))
                        cells[row][col].erbast.remove(erbast) #remove the dead erbast 
    
                else: #if there are no neighbors, the children wil spawn in the cell where the parent used to be
                    for erbast in dead_erbasts:
                        cells[row][col].erbast.append(Erbast(erbast.ENERGY // 2)) #energy cannot depend on parent energy
                        cells[row][col].erbast.append(Erbast(erbast.ENERGY // 2))

                neigh = neighbors(col, row)

                vegetob_values = [neighbor.vegetob for neighbor in neigh]
                if are_all_elements_equal(vegetob_values) and vegetob_values[0] == 100: # if an erbast is surrounded by max density vegetob, it gets terminated
                    cells[row][col].erbast.clear()



            if cells[row][col].carviz:
                if len(cells[row][col].carviz) >= MAX_PRIDE:
                    slice_index = len(cells[row][col].carviz)//2
                    cells[row][col].carviz = cells[row][col].carviz[slice_index:]

                dead_carviz = [item for item in cells[row][col].carviz if item.AGE == item.MAXLIFE]
                neigh_coords = neighbors(col, row)

                if neigh_coords:
                    for carviz in dead_carviz:
                        spawn_choices = random.choices(neigh_coords, k=2)
                        spawn_choices[0].carviz.append(Carviz(carviz.ENERGY // 2))
                        spawn_choices[1].carviz.append(Carviz(carviz.ENERGY // 2))
                        cells[row][col].carviz.remove(carviz) #remove the dead carviz 

                    dead_carviz_energy = [item for item in cells[row][col].carviz if item.ENERGY <= 0]
                    for carviz in dead_carviz_energy:
                        spawn_choices = random.choices(neigh_coords, k=2)
                        spawn_choices[0].carviz.append(Carviz(energy = numpy.random.randint(0, 42))) 
                        spawn_choices[1].carviz.append(Carviz(energy = numpy.random.randint(0, 42)))
                        cells[row][col].carviz.remove(carviz) 
                else:
                    for carviz in dead_carviz:
                        cells[row][col].carviz.append(Carviz(carviz.ENERGY // 2)) 
                        cells[row][col].carviz.append(Carviz(carviz.ENERGY // 2))
                
                neigh = neighbors(col, row)
                vegetob_values = [neighbor.vegetob for neighbor in neigh]
                if are_all_elements_equal(vegetob_values) and vegetob_values[0] == 100: # if a carviz is surrounded by max density vegetob, it gets terminated
                    cells[row][col].carviz.clear()

def spawn(cells):
    #the function exploits the random library to spawn living beings on cells with material = 'ground' 
    for i in cells: 
        for j in i:
            if j.material == "ground":
                #the probability of a creature to be spawned are weighted
                if random.choices([0, 1], weights=[POBABILITY_SPAWN_ERB, 1-POBABILITY_SPAWN_ERB])[0] == 0:
                    j.erbast.append(Erbast(energy = numpy.random.randint(0, 76))) #the initial energy of the creature is also set randomly

                if random.choices([0, 1], weights=[POBABILITY_SPAWN_CAR, 1-POBABILITY_SPAWN_CAR])[0] == 0:
                    j.carviz.append(Carviz(energy = numpy.random.randint(0, 76)))
                    
                if random.choices([0, 1], weights=[0.9, 0.1])[0] == 0:
                    j.vegetob += numpy.random.randint(0, 101)

def print_grid(cells, NUMCELL):
    # is not used in the code, but it can be usefull for debugging
    for row in range(0, NUMCELL):
        for col in range(0, NUMCELL):
            if cells[row][col].erbast:
                for i in range (len(cells[row][col].erbast)):
                    print(' ', cells[row][col].erbast[i].SOCIALATTITUDE, end=' ') 
            else:
                print(' ', "[]", end=' ')
        print()
    print()

    print("---------^^^erbast social attitude^^^----------")

    for row in range(0, NUMCELL):
        for col in range(0, NUMCELL):
            if cells[row][col].erbast:
                for i in range(len(cells[row][col].erbast)):
                    print(' ', cells[row][col].erbast[i].ENERGY, end=' ')
            else:
                print(' ', "[]", end=' ')

        print()
    print()

    print("-------------^^^erbast energy^^^--------------")

    for row in range(0, NUMCELL):
        for col in range(0, NUMCELL):
            print(' ', cells[row][col].vegetob, end=' ')
        print()
    print()

    print("-----------^^^vegetob density^^^--------------")

    for row in range(0, NUMCELL):
        for col in range(0, NUMCELL):
            if cells[row][col].carviz:
                for i in range(len(cells[row][col].carviz)):
                    print(' ', cells[row][col].carviz[i].SOCIALATTITUDE, end=' ')
            else:
                print(' ', "[]", end=' ')

        print()
    print()

    print("-----------^^^carviz social attitude^^^----------")

    for row in range(0, NUMCELL):
        for col in range(0, NUMCELL):
            if cells[row][col].carviz:
                for i in range(len(cells[row][col].carviz)):
                    print(' ', cells[row][col].carviz[i].ENERGY, end=' ')
            else:
                print(' ', "[]", end=' ')

        print()
    print()
    print("-----------^^^carviz energy^^^----------")

def get_social(list_creatures): 
    #returns a list of the creatures of a group that have social attitude = 1
    socials = []
    for creature in list_creatures:
        if creature.SOCIALATTITUDE == 1:
            socials.append(creature)
    return socials

def get_not_social(list_creatures): 
    # returns a list of the creatures of a group that have social attitude = 0
    not_socials = []
    for creature in list_creatures:
        if creature.SOCIALATTITUDE == 0:
            not_socials.append(creature)
    return not_socials

def are_all_elements_equal(lst):
    #the function is used to check if all the elements in a list are equal
    if not lst:
        return False
    first_element = lst[0]
    return all(element == first_element for element in lst)
    #returns true if all elements are equal to first_element otherwise it returns false

def tot_group_en(cell, decision):
    #the function, given a particular cell, depending on the value of the decision variable returns the sum of the energy of all the erbast or carviz in the cell 
    total_energy = 0
    if decision == "erbast":
        if cell.erbast:
            total_energy += sum(erbast.ENERGY for erbast in cell.erbast)
    elif decision == "carviz":
        if cell.carviz:
            total_energy += sum(carviz.ENERGY for carviz in cell.carviz)
    return total_energy

def get_energy_group(list_creature):
    #given a list of creatures it returns the sum of all the energies of all the creature in the list 
    #useful for prides and herds where we have to divide social and nonsocial
    tot_energy = 0 
    for creature in list_creature:
        tot_energy += creature.ENERGY
    return tot_energy

def get_max_vegetob_cell(neigh, current_cell): 
    # this function selects the neighbor cell with the maximum vegetob density
    # once is select we check if it is the last cell that was visited, if it is choose another one
    #if there are no suitable neighbors we return the current_cell
    if neigh:
        vegetob_cell = max((cell for cell in neigh), key=lambda x: x.vegetob)

        while vegetob_cell.carviz: 
            neigh.remove(vegetob_cell)

            if neigh:
                vegetob_cell = max((cell for cell in neigh), key = lambda x: x.vegetob)
            else:
                return current_cell
            
        return vegetob_cell
    else:
        return current_cell

def pride_fight(first_pride, second_pride):
    #in case two prides end up being on the same cell this function is called
    #given two carviz lists it returns only the surviving pride

    first_pride = sorted((car for car in first_pride), key=lambda x: x.ENERGY, reverse = True) #sort the list of first pride to be in order of ENERGY
    second_pride = sorted((car for car in second_pride), key=lambda x: x.ENERGY, reverse = True) #sort the list of second pride to be in order of ENERGY

    while first_pride and second_pride: #loops until one of the two lists is empty
        first_champion = first_pride[0]
        second_champion = second_pride[0]

        if first_champion.ENERGY > second_champion.ENERGY: 
            #the champion with the greater energy survives at the cost of half its energy
            second_pride.remove(second_champion)
            first_champion.ENERGY //= 2

        elif first_champion.ENERGY < second_champion.ENERGY:
            first_pride.remove(first_champion)
            second_champion.ENERGY //= 2
        
        # both lists could be sorted again so that at index 0 there will always be the most energetic carviz, 
        # but we decided to let a champion fight till the death before moving on to the next one
            
    if first_pride: #if the first pride is the winnner
        return first_pride
    
    else: #if the second pride is the winner
        return second_pride

def random_cell_choice(neigh, current_cell):
    #returns a randomly selected cells amongst the neighs
    #useful for when creatures get "bored"
    if neigh: 
        move_to = random.choice(neigh)
        
    else: 
        #if there are no neighs return the current_cell
        move_to = current_cell
        
    return move_to

def check_bored_pride(cells, row, col, pride):
    neigh = neighbors(col, row)
    
    if neigh:
        #sort the pride in order to have the most energetic carviz as the first element, which will become the leader
        pride = sorted((car for car in pride), key=lambda x: x.ENERGY, reverse=True) 
        leader_car = pride[0]

        if leader_car.bored >= BOREDOM: #if the leader is bored then the whole social part of the pride is moved to a new randomly chosen location using the random_cell_choice function
            random_cell_choice(neigh, cells[row][col]).carviz.extend(pride)  
            cells[row][col].carviz = [x for x in cells[row][col].carviz if x not in pride] # remove the part that moved from the old cell
            leader_car.bored = 0 #after the leader moves, he is not bored anymore
       
        else:#if it isn't yet bored enough, it gets more bored
            leader_car.bored += 1 
  
    else: # if there are no neighbours to move to then the pride is destined to die
        cells[row][col].carviz.clear()
                                                
def check_neighbours_erbast(cells):

    for row in dimension:
        for col in dimension:
            #this function only concerns itself with lonely erbasts
            if len(cells[row][col].erbast) ==1 and cells[row][col].moved == False:

                oncell_vegetob = 0
                #the value of the vegetob present on the cell is stored in order to confront it later with the vegetob value of the max_vegetob_cell
                if cells[row][col].vegetob > 0:
                    oncell_vegetob = (cells[row][col].vegetob * VEGETOB_GAIN)
                
                # if there is enough energy to move go look for the vegetobs values of the neighbouring cells
                if cells[row][col].erbast[0].ENERGY > 5: 

                    neigh = neighbors(col, row)
                    
                    #get the neighboring cell with the highest vegetob value
                    max_vegetob_cell = get_max_vegetob_cell(neigh, cells[row][col])
                    
                    if max_vegetob_cell.vegetob > 0: #only if the vegetob value is greater than 0 it's worth checking it otherwise the oncell_vegetob would be better 
                        
                        if (max_vegetob_cell.vegetob // 7) * 4 > oncell_vegetob: 
                            #in this case the erbast goes to eat the max neighbour since in the comparison with the oncell-vegetob it turned out to be more remunerative 
 
                            if cells[row][col].erbast[0].ENERGY + (max_vegetob_cell.vegetob * VEGETOB_GAIN) -2 <= MAX_ENERGY_ERB: #check if the new gained energy wouldn't be more than the max allowed
                                cells[row][col].erbast[0].ENERGY += (max_vegetob_cell.vegetob * VEGETOB_GAIN) -2 # gains energy and loses some of it due to movement 
                                
                            else: # if the gained energy would be more than the MAX_ENERGY then, set the energy to the maximum
                                cells[row][col].erbast[0].ENERGY = MAX_ENERGY_ERB 
                            
                            max_vegetob_cell.erbast.append(cells[row][col].erbast[0]) # move the erbast to the cell with greater vegetob density
                            max_vegetob_cell.vegetob = 0 # the vegetob gets eaten
                            cells[row][col].erbast.clear() #remove the erbast from its old cell
                            #set the moved variable to True
                            max_vegetob_cell.moved = True
                            
                        else:  #in this case the erbast eats the oncell vegetob because is more remunerative then the max neighbour cell
                            if cells[row][col].erbast[0].ENERGY + (max_vegetob_cell.vegetob * VEGETOB_GAIN) <= MAX_ENERGY_ERB:
                                cells[row][col].erbast[0].ENERGY += (max_vegetob_cell.vegetob * VEGETOB_GAIN)
                            
                            else:
                                cells[row][col].erbast[0].ENERGY = MAX_ENERGY_ERB

                            cells[row][col].vegetob = 0
                            cells[row][col].moved = True


                    else: #there are no neighbours with vegetob value higher than 0 so the oncell vegetob is eaten
                        if cells[row][col].erbast[0].ENERGY +(cells[row][col].vegetob * VEGETOB_GAIN ) <= MAX_ENERGY_ERB:
                            cells[row][col].erbast[0].ENERGY += (cells[row][col].vegetob * VEGETOB_GAIN)
                            
                        else:
                            cells[row][col].erbast[0].ENERGY = MAX_ENERGY_ERB

                        cells[row][col].vegetob = 0
                        cells[row][col].moved = True

                else: #if the erbast does not have enough energy to move then the oncell vegetob is eaten
                    if cells[row][col].erbast[0].ENERGY + (cells[row][col].vegetob * VEGETOB_GAIN ) >= MAX_ENERGY_ERB:
                        cells[row][col].erbast[0].ENERGY += (cells[row][col].vegetob * VEGETOB_GAIN)
                        
                    else:
                        cells[row][col].erbast[0].ENERGY = MAX_ENERGY_ERB
                        
                    cells[row][col].vegetob = 0
                    cells[row][col].moved = True

    # loops through all the grid to reset the moved state           
    for row in dimension:
        for col in dimension:
            cells[row][col].moved = False

    return cells   

def check_neighbours_carviz(cells):
    for row in dimension:
        for col in dimension:

            #this function only concerns itself with lonely erbasts
            if len(cells[row][col].carviz) == 1 and cells[row][col].moved == False:
                oncell_herd_energy = 0
                 #the value of the total sum of the energies of the erbasts, or erbast, present on the cell is stored in order to confront it later with the the value of the total sum of the energies of the erbasts, or erbast, present on the max_en_cell
                if cells[row][col].erbast: 
                    oncell_herd_energy = tot_group_en(cells[row][col], decision = "erbast")

                # if there is enough energy to move go look for the erbasts energy values of the neighbouring cells
                if cells[row][col].carviz[0].ENERGY > 5:

                    neigh_car = neighbors(col, row)

                    # finds all the cells containing erbasts
                    erbast_cells = [cell for cell in neigh_car if any(e for e in cell.erbast)]
                    # finds all the cells containing carviz
                    carviz_cells = [cell for cell in neigh_car if any(c for c in cell.carviz)]

                    if erbast_cells: 
                        #if there exist erbast_cells we get the one where the sum of the energy of the erbasts hosted is maximum
                        max_en_cell = max(erbast_cells, key=lambda cell: tot_group_en(cell, decision = "erbast")) 
                        #store the value of the sum of the energy of the erbasts hosted in max_en_cell
                        energy_herd = tot_group_en(max_en_cell, decision = "erbast")

                        
                        if energy_herd > oncell_herd_energy: #check which of the two is more remunerative
                            #in this case max_en_cell offered the better option for the carviz so the fight begins
                            if (cells[row][col].carviz[0].ENERGY + PREDATOR_ADVANTAGE) - energy_herd >= 0:
                                #the fight is based on the energy of the two creatures but the carviz, being the predator, has an advantage 
                                if cells[row][col].carviz[0].ENERGY + energy_herd // 2 <= MAX_ENERGY_CAR: #check if the new gained energy wouldn't be more than the max allowed
                                    cells[row][col].carviz[0].ENERGY +=  energy_herd // 2
                                    
                                else:
                                    cells[row][col].carviz[0].ENERGY = MAX_ENERGY_CAR

                                cells[row][col].carviz[0].bored = 0
                                max_en_cell.carviz.append(cells[row][col].carviz[0])
                                cells[row][col].carviz.clear()
                                max_en_cell.erbast.clear()
                                max_en_cell.moved = True
                                
                            else: 
                            #this is the case where the lonely carviz loses gainst the erbast/herd and some energy is detracted from the latter due to defensive efforts
                                for erb in max_en_cell.erbast:
                                    erb.ENERGY  = (erb.ENERGY //3) * 2
                                    
                                cells[row][col].carviz.clear()


                        else: #the oncell erbast/herd is the more remunerating option so it fights with that
                           
                           # the lonely carviz wins
                            if (cells[row][col].carviz[0].ENERGY + PREDATOR_ADVANTAGE) - energy_herd >= 0:
                                
                                if cells[row][col].carviz[0].ENERGY + energy_herd // 2 <= MAX_ENERGY_CAR:
                                    cells[row][col].carviz[0].ENERGY += energy_herd // 2 
                                else:
                                    cells[row][col].carviz[0].ENERGY = MAX_ENERGY_CAR
                                    
                                cells[row][col].erbast.clear()
                                
                            else: #erbast/pride wins
                                for erb in cells[row][col].erbast:
                                    erb.ENERGY  = (erb.ENERGY //3) * 2
                                cells[row][col].carviz.clear()

                    elif cells[row][col].erbast: #if there is a oncell erbast and not a neighbour erbast, then then the carviz begins the fight with the first one
                        
                        if (cells[row][col].carviz[0].ENERGY + PREDATOR_ADVANTAGE) - oncell_herd_energy >= 0:
                           # the lonely carviz wins
                                if cells[row][col].carviz[0].ENERGY + oncell_herd_energy // 2 <= MAX_ENERGY_CAR:
                                    cells[row][col].carviz[0].ENERGY += oncell_herd_energy // 2 
                                else:
                                    cells[row][col].carviz[0].ENERGY = MAX_ENERGY_CAR
                                
                                cells[row][col].erbast.clear()
                                
                        else: #erbast/pride wins
                            for erb in cells[row][col].erbast:
                                erb.ENERGY  = (erb.ENERGY //3) * 2
                            cells[row][col].carviz.clear()

                    elif carviz_cells and cells[row][col].carviz[0].SOCIALATTITUDE == 1: 
                        #if there are neighbour erbast cells and there is no erbast oncell the lonely carviz joins a pride if it is social and if it is bored enough 
                        max_car_cell = max(carviz_cells, key=lambda cell: tot_group_en(cell, decision = "carviz"))
                        
                        cells[row][col].carviz[0].bored = 0
                        max_car_cell.carviz.append(cells[row][col].carviz[0])
                        cells[row][col].carviz.clear()

                    else: #if there are no neighbour erbast cells, no erbast oncell and there are no prides to join then it gets bored
                        if cells[row][col].carviz[0].bored >= BOREDOM: # if the carviz is bored enough, a ranodm cell is choosed and the carviz is moved
                            randoom_cell = random_cell_choice(neigh_car, cells[row][col])
                            cells[row][col].carviz[0].bored = 0
                            randoom_cell.carviz.append(cells[row][col].carviz[0])
                            cells[row][col].carviz.remove(cells[row][col].carviz[0])

                        else:
                            cells[row][col].carviz[0].bored += 1

                
                elif cells[row][col].erbast: #if the carviz does not have enough energy to move then the if there is an erbast on the cell, they fight
                    
                    if (cells[row][col].carviz[0].ENERGY + PREDATOR_ADVANTAGE) - oncell_herd_energy >= 0: #in this case the carviz wins
                        
                        if cells[row][col].carviz[0].ENERGY + oncell_herd_energy // 2 < MAX_ENERGY_CAR: #check if the new gained energy wouldn't be more than the max allowed
                            cells[row][col].carviz[0].ENERGY += oncell_herd_energy // 2 #since is not moving, it is not loosing energy
                            
                        else: # if the gained energy would be more than the MAX_ENERGY then, set the energy to the maximum
                            cells[row][col].carviz[0].ENERGY = MAX_ENERGY_CAR

                        cells[row][col].erbast.clear() #the erbast dies

                    else: #the oncell erbast wins
                        for erb in cells[row][col].erbast:
                            erb.ENERGY  = (erb.ENERGY //3) * 2
                        cells[row][col].carviz.clear()

    # loops through all the grid to reset the moved state   
    for row in dimension:
        for col in dimension:
            cells[row][col].moved = False

    return cells

def move_herd(cells):
    for row in dimension:
        for col in dimension:
            #this function considers only the cells that host a herd
            if len(cells[row][col].erbast) >= 2 and cells[row][col].moved == False:
                #the social stay variable is useful when we want to know if a herd ate the vegetob that is on the cell it is standing on or not
                social_stay = False
                oncell_vegetob = 0
                #save the value of the vegetob of the cell the herd is on
                if cells[row][col].vegetob > 0: 
                    oncell_vegetob = ((cells[row][col].vegetob // len(cells[row][col].erbast)) * VEGETOB_GAIN)
        
                neigh = neighbors(col, row) #find neighbors

                if neigh:
                    max_vegetob_cell = max((cell for cell in neigh), key = lambda x: x.vegetob) #get the neighbour cell with the maximum vegetob density
                else: # if there are no neighbuours,it means it is an island, so the herd dies
                    cells[row][col].erbast.clear()
                
                if max_vegetob_cell.vegetob > 0: #if there are neighbouring cells that contain some vegetob we check those also
                    #because it could be that all the neighbors vegetob are 0

                    social_part_of_the_herd = get_social(cells[row][col].erbast) #create a list with only the social part of the herd
                    nonsocial_part_of_the_herd = get_not_social(cells[row][col].erbast) #creates a list with only the nonsocial part of the herd
                    
                    if social_part_of_the_herd:
                        #if it exists a social part of the herd, we calculate how much energy the latter would gain from eating the vegetob of the max_vegetob_cell and compare it with the energy that would be gained from every erbast by eating the oncell_vegetob
                        if ((max_vegetob_cell.vegetob // len(social_part_of_the_herd)) * VEGETOB_GAIN) > oncell_vegetob + 2: #if there exists a more remunerating neighbour the herd moves there (+2 because of the energy loss due to movement)
                        
                            for erb in social_part_of_the_herd: #every erbasts in the social part of the herd gains energy when a herd moves to eat some vegetob
                                if erb.ENERGY + ((max_vegetob_cell.vegetob // len(cells[row][col].erbast))* VEGETOB_GAIN) - 2 <= MAX_ENERGY_ERB: 
                                    erb.ENERGY += ((max_vegetob_cell.vegetob // len(cells[row][col].erbast)) * VEGETOB_GAIN) - 2
                                    
                                else:
                                    erb.ENERGY += MAX_ENERGY_ERB
                            
                            max_vegetob_cell.erbast.extend(social_part_of_the_herd) # the herd moves to the cell with maximun vegetob density
                            cells[row][col].erbast = [x for x in cells[row][col].erbast if x not in social_part_of_the_herd] #removes only the social part of the herd because is the only one that moved (only nonsocial part remain)
                                
                            max_vegetob_cell.vegetob = 0
                            max_vegetob_cell.moved = True
                            
                        else: #if the vegetob on the cell is more remunerating for the herd than the neighbouring vegetobs, then it gets eaten  
                            for erb in cells[row][col].erbast:
                                if erb.ENERGY + ((cells[row][col].vegetob // len(cells[row][col].erbast))* VEGETOB_GAIN) <= MAX_ENERGY_ERB:
                                    erb.ENERGY += ((cells[row][col].vegetob // len(cells[row][col].erbast)) * VEGETOB_GAIN)
                                else:
                                    erb.ENERGY = MAX_ENERGY_ERB
                            cells[row][col].vegetob = 0
                            #the variable social_stay is set to True because the herd stayed on the original cell, so there is no need to move the nonsocial part of the herd
                            social_stay = True

                    if nonsocial_part_of_the_herd and social_stay == False: #if there is a nonsocial part in the herd and the social part already moved
                        while nonsocial_part_of_the_herd:
                            #we consider every component of the non social part singularly
                            current_erbast = nonsocial_part_of_the_herd.pop()
                            cells[row][col].erbast.remove(current_erbast)
                            
                            neigh_ = neighbors(col, row)
                            max_vegetob_cell = get_max_vegetob_cell(neigh_, cells[row][col])
                           
                            #a possbile improvement is to perform again the comparison between the oncell vegetob and the neighbour vegetob with max density to see which one is the more remunerative option
                            
                            if max_vegetob_cell.vegetob > 0:
                                max_vegetob_cell.erbast.append(current_erbast)
                                max_vegetob_cell.vegetob = 0
                                max_vegetob_cell.moved = True

                            else: #if there are no neighboing cells with vegetob value greater than 0 the non social erbast moves randomly
                                randoom_cell = random_cell_choice(neigh_, cells[row][col])
                                randoom_cell.erbast.append(current_erbast)
                               
        
                elif oncell_vegetob > 0: #if the neighbours vegetob values are all 0 and the vegetob value in the current cell is greater than 0, then it gets eaten
                    for erb in cells[row][col].erbast:
                        if erb.ENERGY + ((cells[row][col].vegetob //len(cells[row][col].erbast))* VEGETOB_GAIN) <= MAX_ENERGY_ERB:
                            erb.ENERGY += ((cells[row][col].vegetob //len(cells[row][col].erbast))* VEGETOB_GAIN)
                        else:
                            erb.ENERGY = MAX_ENERGY_ERB           
                    cells[row][col].vegetob = 0
  
    # loops through all the grid to reset the moved state   
    for row in dimension:
        for col in dimension:
            cells[row][col].moved = False
    return cells

def move_pride(cells):
    for row in dimension:
        for col in dimension:
            #this function considers only the cells that host a pride
            if len(cells[row][col].carviz) >= 2 and cells[row][col].moved == False:
                neigh = neighbors(col, row)  # find neighbors
                #the social stay variable is useful when we want to know if a pride ate the herd/erbast that is on the cell it is standing on or not
                social_stay = False
                #the variable active pride is useful to check if during the current day the pride moved or ate or if it got "bored"
                active_pride = False
                oncell_herd_energy = 0

                social_part_of_the_pride = get_social(cells[row][col].carviz) #create a list with only the social part of the pride
                nonsocial_part_of_the_pride = get_not_social(cells[row][col].carviz) #creates a list with only the nonsocial part of the pride

                if cells[row][col].erbast: #if there is at least one erbast in the current cell, then its energy is saved
                    oncell_herd_energy = tot_group_en(cells[row][col], decision = "erbast")

                if social_part_of_the_pride: #if there exists a social part of the pride
                    energy_pride = get_energy_group(social_part_of_the_pride) #save the energy as the sum of all energies of all the creatures of the pride 
                    
                    #when carviz fight against erbasts: 
                    #if the carviz win the energy of the erbast or herd is halved and divided equally among the members of the pride
                    #if instead the erbast/herd wins then the energy of the erbast or herd is halved and the pride dies
                    
                    #erbast_cells is a list containing all the cells hosting at least one erbasts object
                    erbast_cells = [cell for cell in neigh if any(e for e in cell.erbast)] 
                    if erbast_cells:
                        
                            max_en_cell = max(erbast_cells, key=lambda cell: tot_group_en(cell, decision = "erbast")) #gets the cell containing the most energetic herd/ erbast
                            energy_neighbour_herd = tot_group_en(max_en_cell, decision = "erbast")
                            
                            if energy_neighbour_herd // len(social_part_of_the_pride) > oncell_herd_energy // len(cells[row][col].carviz): #se c'è un vicino che è più cicciottello rispetto a quello sulla cella allora vai la
                                #we set active pride to true so that we know the pride didn't get bored on that day 
                                active_pride = True
                                
                                for car in social_part_of_the_pride:#since the social part is moving, for every member of the part, the bored is set to 0 
                                    car.bored = 0
                                
                                if (energy_pride + PREDATOR_ADVANTAGE * len(social_part_of_the_pride)) - energy_neighbour_herd >= 0:
                                    # carviz pride wins the fight
                                    for car in social_part_of_the_pride:
                                        if car.ENERGY + ((energy_neighbour_herd // len(cells[row][col].carviz)) // 2)-2 < MAX_ENERGY_CAR:
                                            car.ENERGY += ((energy_neighbour_herd // len(cells[row][col].carviz)) // 2)-2
                                        else:
                                            car.ENERGY = MAX_ENERGY_CAR
                                    
                                    max_en_cell.erbast.clear()
                                    
                                    if len(max_en_cell.carviz) >= 2: #before moving the pride we check if were it wants to move there is already another pride
                                        winner = pride_fight(cells[row][col].carviz, max_en_cell.carviz)

                                        max_en_cell.carviz = winner #rimane solo il pride che ha vinto il combat

                                    else: #non c'è un altro pride da combattere quindi semplicemente spostiamo il pride
                                        max_en_cell.carviz.extend(social_part_of_the_pride)

                                    cells[row][col].carviz =[x for x in cells[row][col].carviz if x not in social_part_of_the_pride]
                                    max_en_cell.moved = True
                                    
                                else: #herd/erbast wins the fight 
                                    for erb in max_en_cell.erbast:
                                        erb.ENERGY = (erb.ENERGY // 3) *2
                                        
                                    cells[row][col].carviz = [x for x in cells[row][col].carviz if x not in social_part_of_the_pride] #only the non social part of the pride will survive in the original cell
                            
                            else: #in the comparison between the nearby herd and the herd/erbast on the cell the second of the two turned out to be the better option and therefore the fight begins
                                #the variable social_stay is set to True because the pride stayed on the original cell, so there is no need to move the nonsocial part of the pride
                                social_stay = True
                                #we set active pride to true so that we know the pride didn't get bored on that day 
                                active_pride = True

                                for car in cells[row][col].carviz: #since the pride is eating the oncell herd/erbast, for every member of the part, the bored is set to 0 
                                    car.bored = 0
                                    
                                if (energy_pride + PREDATOR_ADVANTAGE * len(cells[row][col].carviz)) - oncell_herd_energy>= 0:
                                    for car in cells[row][col].carviz:
                                        if car.ENERGY + (len(cells[row][col].erbast) // len(cells[row][col].carviz) // 2) < MAX_ENERGY_CAR:
                                            car.ENERGY += (len(cells[row][col].erbast) // len(cells[row][col].carviz) // 2)
                                        
                                        else:
                                            car.ENERGY = MAX_ENERGY_CAR
                                    
                                    cells[row][col].erbast.clear()
                                else: #the case where the erbasts win the fight, because of defensive action, it loses some energy 
                                    for erb in max_en_cell.erbast: 
                                        erb.ENERGY = (erb.ENERGY // 3) * 2
                                    cells[row][col].carviz.clear()


                    if nonsocial_part_of_the_pride and social_stay == False: 
                        #moving the non social part of the pride, if it exists and the social part moved away, so that on the next day it won't be a pride anymore, because in case the non social part of the pride has len > 2 it would never be considered otherwise 
                        while nonsocial_part_of_the_pride:
                            #we consider every component of the non social part singularly
                            current_carviz = nonsocial_part_of_the_pride.pop()
                            cells[row][col].carviz = nonsocial_part_of_the_pride
                            neigh_ = neighbors(col, row)
                            erbast_cells = [cell for cell in neigh_ if any(e for e in cell.erbast)] #finds all the cells with erbasts
                            if erbast_cells:
                                max_erb = max(erbast_cells, key=lambda cell: tot_group_en(cell, decision = "erbast")) #gets, amongst the erbast cells, the class containing the most energetic list of erbasts

                                energy_max_erb = tot_group_en(max_erb, decision = "erbast")

                                if max_erb: #if there exists at least one erbast amongst the neighbours of the non social part of the pride the fight begins
                                    if current_carviz.ENERGY + PREDATOR_ADVANTAGE - energy_max_erb >= 0: 
                                        #carviz wins the fight and the usual energy check is performed 

                                        if current_carviz.ENERGY + (energy_max_erb // 2) -2 < MAX_ENERGY_CAR:
                                            current_carviz.ENERGY += (energy_max_erb // 2) -2
                                        else:
                                            current_carviz.ENERGY = MAX_ENERGY_CAR
                                        
                                        max_erb.carviz.append(current_carviz) #the carviz is moved
                                        max_erb.moved = True
                                        max_erb.erbast.clear() #the dead erbasts are removed from the cell

                                    else: #the case where the erbasts win the fight, for the defenfing fatique, it loses energy
                                        for erb in max_erb.erbast:
                                            erb.ENERGY = (erb.ENERGY // 3) * 2
                            else: #if there are no erbasts around, leave the nonsocial part of the pride where it is
                                cells[row][col].carviz.append(current_carviz)
                                #we break the while loop 
                                break

                    if active_pride == False and social_part_of_the_pride: #only the social part of the pride is moved if it is bored, and it is bored if the pride wasn't active during the day
                        check_bored_pride(cells, row, col, social_part_of_the_pride)
    
    # loops through all the grid to reset the moved state  
    for row in dimension:
        for col in dimension:
            cells[row][col].moved = False
    return cells

def Movement(cells):
    #the function concrned with calling all the functions that move the creatures 
    check_neighbours_erbast(cells)
    check_neighbours_carviz(cells)
    move_herd(cells)
    move_pride(cells)
    
    return cells

def days(cells):
    #get the value and the text of the slider, from the slider file 
    slider_value = slider_window.get_slider_value()
    slider_text = slider_window.get_slider_text()

    #check the text of slider that is connect with the buttons, to see wich variable should change
    if slider_text == "Predator Advantage":
        global PREDATOR_ADVANTAGE
        PREDATOR_ADVANTAGE = slider_value

    elif slider_text == "Max energy herd":
        global MAX_ENERGY_ERB
        MAX_ENERGY_ERB = slider_value

    elif slider_text == "Max energy pride":
        global MAX_ENERGY_CAR
        MAX_ENERGY_CAR = slider_value

    elif slider_text == "Boredom":
        global BOREDOM
        BOREDOM = slider_value

    elif slider_text == "Aging erbast":
        global AGING_ERB
        AGING_ERB = slider_value

    elif slider_text == "Aging carviz":
        global AGING_CAR
        AGING_CAR = slider_value

    elif slider_text == "Max herd components":
        global MAX_HERD
        MAX_HERD = slider_value

    elif slider_text == "Max pride components":
        global MAX_PRIDE
        MAX_PRIDE = slider_value

    #run the functions in order to give life to the simulation
    grow(cells)
    Movement(cells)
    death_birth(cells)
    
    return cells

def main():
    # the main function creates the grid, sets the initial position and runs the days
    create_grid(cells, NUMCELL)
    spawn(cells)
    days(cells)
    return cells
