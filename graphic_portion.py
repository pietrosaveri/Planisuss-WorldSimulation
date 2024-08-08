import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from main_code import main, days, NUMCELL
from slider_buttons import slider_window

rows, cols = NUMCELL, NUMCELL 
#the interval between the frames of the animation
speed = 100

#the variable indicating the maximum speed that can be set, this variable must be greater or equal to SPEED_CHANGE
MAX_SPEED = 50

#variable indicating how muche the speed will decrease or increase when the 'speedup_button' or the 'speeddown_button' is pressed
SPEED_CHANGE = 50

#set up a scaling factor to always have the carviz and erbast markers proportioned to the size of the cells
scaling_factor = 1 / max(rows, cols)

#the initial data comes from the main fuction in main_code.py
starting_data = main()

#useful for displaying on the screen the time as it passes by
time_periods = ["day", "month", "year", "decade", "century"]
current_period_index = 0
time_units = [0, 0, 0, 0, 0]

#set a variable for the grey color, we will usse this as background
grey = (211/255, 211/255, 211/255)

#list with all the erbasts of a single day used in the update plot function
LIST_ERB = []

#list with all the carviz of a single day used in the update plot function
LIST_CAR = []

#list with all the vegetob of one day
LIST_VEG = []

#amount of vegetob present in one day relative to the number of ground cells
VEGETOB_NUM = 0

#calculate the number of ground cells in the world
NUM_GROUND_CELLS= 0

#set up list for the passing of time, useful to plot the number of creatures with reletion to the time
time_list = []

def format_time(*time_units):
    # useful for rewriting the time in a formatted manner using a f string 
    return ' '.join(f"{value} {unit if value == 1 else unit + 's'}" for unit, value in time_units if value > 0)

def update_time_units(time_units, current_period_index, time_periods):
    #fucntion to calcultate the passing of time
    #10 days = 1 month
    #10 months = 1 year 
    #10 years = 1 decade
    #10 decades = 1 century
    time_units[0] += 1
    carry = 0
    for j in range(len(time_units) - 1):
        time_units[j] += carry
        carry = time_units[j] // 10
        time_units[j] %= 10

    current_period_index = (current_period_index + 1) % len(time_periods)
    return time_units, current_period_index

def pause_animation(event):
    ani.event_source.stop()

def resume_animation(event):
    ani.event_source.interval = speed #without this line of code the speed would reset to the initial speed value when resuming
    ani.event_source.start()

def speed_up(event):
    #function that will globally affect the variable speed
    global speed
    global label
    if speed == MAX_SPEED:  # if the speed at MAX, do not decrease it because if the interval = 0 the animation stops
        text = "Maximum speed attained"
        label.set_text(text)
    else:
        speed -= SPEED_CHANGE
    #to set the new interval correctly we have to briefly stop the animation 
    ani.event_source.stop()
    ani.event_source.interval = speed
    ani.event_source.start()

def speed_down(event):
    #the speed can be infinitely decreased, there is no limiting value
    global speed
    global label
    text = ""
    label.set_text(text)
    speed += SPEED_CHANGE
    #to set the new interval correctly we have to briefly stop the animation 
    ani.event_source.stop()
    ani.event_source.interval = speed
    ani.event_source.start()

def set_ground_water_values(data_maincode):
    #the function's aim is to loop through the grid and check if a cell is ground or water, then set a value for each
    for row in range(NUMCELL):
        for col in range(NUMCELL):
            if data_maincode[row][col].material == "ground":
                data_maincode[row][col].value = 600 #new randomly chosed value that represent ground
            elif data_maincode[row][col].material == "water":
                data_maincode[row][col].value = 500 #new randomly chosed value that represent water
    return data_maincode

def count_erbast(grid):
    #function that counts the number of erbasts for each cell

    list_erbast = [] #list where each element will be the number of erbasts for each cell of the grid 
    for row in range(NUMCELL):
        for col in range(NUMCELL):
            # initialize a variable for the number of erbasts in the grid[row][col] cell
            number_erb = 0
            if grid[row][col].erbast:
                number_erb = len(grid[row][col].erbast)
                list_erbast.append(number_erb)
            else:
                list_erbast.append(0)

    # reshape the list to be a grid NUMCELLxNUMCELL
    number_erb_grid = np.array(list_erbast).reshape(NUMCELL, NUMCELL)
    return number_erb_grid

def count_carviz(grid):
    #function that counts the number of carviz for each cell
    list_carviz = [] #list where each element will be the number of carviz for each cell of the grid 
    for row in range(NUMCELL):
        for col in range(NUMCELL):
            #initialize a variable for the number of carviz in the grid[row][col] cell
            number_car = 0
            if grid[row][col].carviz:
                number_car = len(grid[row][col].carviz)
                list_carviz.append(number_car)
            else:
                list_carviz.append(0)

    #reshape the list to be a grid NUMCELLxNUMCELL
    number_car_grid = np.array(list_carviz).reshape(NUMCELL, NUMCELL)

    return number_car_grid

def count_creatures(grid):
    #function useful to count the total number of erbasts or carviz in a day, useful to plot the population graph of each creature
    counter = 0
    for row in range(NUMCELL):  
        for col in range(NUMCELL):
            counter += grid[row][col]
    return counter

def update_time(i, time_list):
    #create a list to track the time during the animation, useful for the population graph
    time_list.append(i)
    return time_list

def update_plot(i, time_periods, time_units, current_period_index, time_list, LIST_ERB, LIST_CAR, LIST_VEG, VEGETOB_NUM, NUM_GROUND_CELLS):
    #main function that is recursevly call to update the animation

    #set up the passing of time
    time_units, current_period_index = update_time_units(time_units, current_period_index, time_periods)
    time_list = update_time(i, time_list)
    
    #create a variable that will be call every day, getting the values from main_code.py
    data_days = days(starting_data)

    #set the interval of the aniamtion equal to the speed, so that when the speed is changed, the interval is updated
    ani.interval = speed

    #normalization of the data from main_code.py, to make the code able to represent them in the plot
    grid_ground_water = set_ground_water_values(data_days)
    num_erb_grid = count_erbast(data_days)
    number_car_grid = count_carviz(data_days)

    #set up an array of zeros with dimention row, col, every element has four values, in our case RGBA
    img_array = np.zeros((rows, cols, 4))  # 4 channels (RGBA)
    for row in range(rows):
        for col in range(cols):
            if grid_ground_water[row][col].value == 500: #found a water cell
                img_array[row][col] = [0, 0, 1, 1] #set up the color of the cell, using the RGBA values, Blue, with opaticy at max

            if grid_ground_water[row][col].value == 600: #found a ground cell
                img_array[row][col] = [0.54, 0.27, 0.07, 1] #set up the color of the cell, using the RGBA values, Brown, with opaticy at max

                #increment the number of ground cells found
                NUM_GROUND_CELLS += 1

            if grid_ground_water[row][col].vegetob:

                #if a cell with vegetob is found, use the colormap of greens to rappresent it
                img_array[row][col] = cmap_greens(norm_greens(grid_ground_water[row][col].vegetob)) #the values of the vegetob need to be normalize from 0 to 100
                
                #update he number of vegetob presents in the all grid
                VEGETOB_NUM += grid_ground_water[row][col].vegetob

    #create lists for each creature that save
    #the x and y values as coordinates
    #the number of creature in a cell
    x_values = []
    y_values = []
    numbererb = []

    x_carviz = []
    y_carviz = []
    numbercar = []

    for row in range(rows):
        for col in range(cols):
            if num_erb_grid[row][col] > 0:

                #append the coordinates of the erbast in the lists
                x_values.append(col)
                y_values.append(row)

                #append how many erbasts are in the cell
                numbererb.append(num_erb_grid[row][col] / 10)

            if number_car_grid[row][col] > 0:

                #append the coordinates of the carviz in the lists
                x_carviz.append(col)
                y_carviz.append(row)

                # append how many carivz are in the cell
                numbercar.append(number_car_grid[row][col] / 10)

    #here we update the artists of the terrain using the img_array edited before
    terrain_artist.set_data(img_array)

    # using the set_offsets method, we update the position of the erbast marker
    erbast_artist.set_offsets(np.column_stack((x_values, y_values)))

    #with the set_sezes method, we update the size of the marker, using the scaling factor mentioned before
    erbast_artist.set_sizes(np.array(numbererb) * 300 * scaling_factor)

    #using the set_offsets method, we update the position of the carviz marker, by adding 0.1 we make sure to see both markers even if they are in the same cell
    carviz_artist.set_offsets(np.column_stack((x_carviz, y_carviz))+0.1)

    #with the set_sezes method, we update the size of the marker, using the scaling factor mentioned before
    carviz_artist.set_sizes(np.array(numbercar)* 300 * scaling_factor)

    #update the text of the label to show the passing of time
    tx.set_text(format_time(("century", time_units[4]), ("decade", time_units[3]), ("year", time_units[2]), ("month", time_units[1]), ("day", time_units[0])))
    
    #we count the number of creatures in the all grid, during the day
    tot_erb = count_creatures(num_erb_grid)
    tot_car= count_creatures(number_car_grid)

    #calculate amount of vegetob present in one day relative to the number of ground cells
    VEGETOB_NUM //= NUM_GROUND_CELLS

    #create the three lists useful to plot the data in the population graph
    LIST_ERB.append(tot_erb)
    LIST_CAR.append(tot_car)
    LIST_VEG.append(VEGETOB_NUM)

    #method for clearing the population graph every day
    ax_population.clear()

    #set the population graph labels and title
    ax_population.set_title("Population", style = "normal")
    ax_population.set_xlabel("Days", fontsize = 10)
    ax_population.set_ylabel("Number of Creatures", fontsize = 10)

    #plot the data in the population graph, using the lists of the creatures, vegetob niumber and passing of time
    ax_population.plot(time_list, LIST_ERB, label = "Erbast", color = "yellow")
    ax_population.plot(time_list, LIST_CAR, label = "Carviz", color = "red")
    ax_population.plot(time_list, LIST_VEG, label = "Vegetob", color = "green")
    
    #set up a legent to better unders the graph
    legend = ax_population.legend(loc="upper right")

    # set the backgound color, edgecolor and linewidth of the legend
    legend.get_frame().set_facecolor(grey)
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(0.5)

    ani.event_source.interval = speed

    return erbast_artist, carviz_artist,

#Create the figure, with 2 axis, with window dimention of 10, 5
fig, (ax, ax_population) = plt.subplots(1, 2, figsize = (10, 5))

#set title of main window
fig.canvas.manager.set_window_title("Planisuss")

#set backgound grey color to the population graph
ax_population.set_facecolor(grey)

#set grey background for main figure
fig.patch.set_facecolor(grey)

#remove axis numbers, from simulation graph
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)

#remove axsis ticks, from simulation graph
ax.set_xticks([])
ax.set_yticks([])

#create a colormap for vegetob using the greens colormap
cmap_greens = plt.get_cmap("Greens")
norm_greens = plt.Normalize(0, 100)

#initialize text variable, of label that will show the progression of time
tx = ax.set_title("")

#set title for population graph
tx_population = ax_population.set_title("Population")

#create artists for terrain
terrain_artist = ax.imshow(np.zeros((rows, cols, 4)))

#create artists to plot the markers of carviz and erbast, using the scatter method
erbast_artist = ax.scatter(range(cols), range(rows), marker='o', c= 'yellow', s= 0)  # Initialize with no circles, this will be updated in the update_plot function
carviz_artist = ax.scatter(range(cols), range(rows), marker="o", c = "red", s= 0) # Initialize with no circles, this will be updated in the update_plot function

#create axis for pause and resume buttons
pause_ax = plt.axes([0.135, 0.06, 0.07, 0.05])
resume_ax = plt.axes([0.205, 0.06, 0.07, 0.05])

#create axis for speed up and speed down buttons
speedup_ax = plt.axes([0.375, 0.06, 0.09, 0.05])
speeddown_ax = plt.axes([0.285, 0.06, 0.09, 0.05])

#create the actual speed up, speed down, pause and resume buttons
pause_button = Button(pause_ax, 'Pause', color='white', hovercolor='grey') #set color to white, and hovercolor to grey (when mouse transits over the button it becames grey)
resume_button = Button(resume_ax, 'Resume', color='white', hovercolor='grey')

speedup_button = Button(speedup_ax, "Speed Up", color ='white', hovercolor='grey')
speeddown_button = Button(speeddown_ax, "Slow Down", color ='white', hovercolor='grey')

#connect buttons to their respective functions
pause_button.on_clicked(pause_animation)
resume_button.on_clicked(resume_animation)

speedup_button.on_clicked(speed_up)
speeddown_button.on_clicked(speed_down)

#setup a label for when the maximum speed is reached
text = ""
label = plt.text(-0.75, 17, text, fontsize=10)

#start the slider from slider_buttons.py
slider_window.run()

#reate the animation
ani = animation.FuncAnimation(fig,  update_plot, cache_frame_data=False, fargs=(time_periods, time_units, current_period_index, time_list, LIST_ERB, LIST_CAR, LIST_VEG, VEGETOB_NUM, NUM_GROUND_CELLS), interval=speed)

#show the all plot
plt.show()