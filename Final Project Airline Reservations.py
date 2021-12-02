#This program will reserve seats on a flight.

#This generates the cost for seat locations on the flight.
def get_cost_matrix():
    cost_matrix = [[500,200,500,200,500] for row in range(10)]
    return cost_matrix

#This function pulls the admin credentials and creates a dictionary from the file for comparison with the entered credentials.
def admin_credentials():
    admin = {}
    with open("passcodes.txt", "r") as file:
        for line in file:
            string = line.split(",")
            admin[string[0].strip()] = string[1].strip()
        return admin

#This function is used to access the admin credentials and compares them to the user input credentials.
def get_admin_login(seating_map):
    print("\nAdmin Login")
    print("-----------\n")
    
    admin_creds = admin_credentials()

    #This while loop checks the input credentials and loops back if the input doesn't match the credentials on file.
    while True:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
      
        if username not in admin_creds.keys():
            print("Invalid username/password combination\n")
        elif admin_creds[username] != password:
            print("Invalid username/password combination\n")
        else:
            print_seating_map(seating_map) #This calls the seating map function.
            print("\nYour Total Sales: ${0}".format(total_sales(seating_map,get_cost_matrix())))
            print("\nYou are logged out now!")
        break

#This function retrieves the stored map of current reservations and open seats on the flight.
def get_initial_map():
    seating_map = [['O']*5 for row in range(10)] #Create the initial matrix of the seating chart.
    #This reads the reservation file and places an X in the reserved seat.
    with open("reservations.txt", "r") as file:
        for line in file:
            string = line.split(",")
            x = int(string[1])
            y = int(string[2])
            seating_map[x][y] = 'X'
        file.close()
        return seating_map

#This function prints the seating map used in multiple functions.
def print_seating_map(seating_map):
    print("\n\nPrinting the Flight Map....\n")
    for x in seating_map:
        print(x)

#This function scans the current seating chart and calculates the total sales based on the cost matrix function.
def total_sales(seating_map, cost_matrix):
    total = 0
    for x in range(10):
        for y in range(5):
            if seating_map[x][y] == 'X':
                total += cost_matrix[x][y]
    return total

#This function is how the user reserves a seat on the flight.
def reserve_seat(seating_map):
    print("\nMake a Reservation")
    print("------------------\n")
    
    firstname = input("Enter First Name: ")
    lastname = input("Enter Last Name: ") #Although this project does not require the last name to be stored, it very easily could be.
    
    print_seating_map(seating_map)
    print()
    
    isValid = False #Setting our boolean for the while loop.
    x = 0 #Creating the local variables for the seating chart matrix.
    y = 0
    
    while not isValid: #This while loop ensures the user is selecting an approved seat range.
        while True:
            x = int(input("Which seat row do you want? (1-10) "))
            if x < 1 or x > 10:
                print("Choose a row in between 1 and 10.")
            else:
                break
        while True:
            y = int(input("Which seat column do you want? (1-5) "))
            if y < 1 or y > 5:
                print("Choose a row in between 1 and 5")
            else:
                break
        #This conditional verifies if the seat entered is already reserved.
        if seating_map[x-1][y-1] == 'X':
            print("Row: {0} Seat: {1} is already assigned. Choose again.\n".format(x,y))
        else:
            print("Your requested seat, Row: {0} Seat: {1} has been assigned.".format(x,y))
            isValid = True
    seating_map[x-1][y-1] = 'X' #This changes the open seat to a reserved one.
    print_seating_map(seating_map)
    print()
    
    e_ticket = "" #Creating the local string for the reservation ticket number.
    code = "INFOTC1040" #This code is used for generating the ticket number.
    
    #This loop takes the first letter from the first name, adds it to the ticket number, then adds the first letter of the code.
    #It then repeats for the second letter of the name and so on until the name is exhausted.
    for index in range(len(firstname)):
        e_ticket += firstname[index]
        e_ticket += code[index]
    e_ticket += code[len(firstname):]
    #This outputs the notification that the seat has been reserved and gives the ticket number.
    print("Congragulations {0} {1}! Your trip is now booked! Enjoy!".format(firstname,lastname))
    print("Your e-ticket number is: {0}".format(e_ticket))

    #This opens the reservations file and appends it with the customer's booking info.
    with open("reservations.txt", 'a') as file:
        file.write('\n')
        file.write(firstname)
        file.write(', ')
        file.write(str(x))
        file.write(', ')
        file.write(str(y))
        file.write(', ')
        file.write(e_ticket)
    file.close()
        
#This function creates the menu options and is accessed by multiple functions.
def menu_get_option():
    print("\n1. Admin Log-In")
    print("2. Reserve a seat")
    print("3. Exit")
    option = int(input("\nChoose an option: "))
    return option


#This is the main function that checks what option the user selects and triggers the correct function correlated to the option. 
def main():
    print("1040 Airways Reservation System")
    print("-------------------------------")
    
    option = 0
    seating_map = get_initial_map() #This access the function that reads the reservation file and stores the matrix.

    #This while loop gets the user option and loops until the user chooses to exit the program.
    while option != 3:
        option = menu_get_option()
        if option not in [1,2,3]:
            print("ERROR: Invalid Option! Select 1 or 2 or 3")
        else:
            if option == 1:
                get_admin_login(seating_map)
            elif option == 2:
                reserve_seat(seating_map)
            else:
                print("\nThank you for choosing 1040 Airways! Goodbye :)")
        
main()
