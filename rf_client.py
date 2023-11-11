import socket


def get_player_info() -> dict:
    """
    prompt player for name and date of birth.
    :return: dictionary of player name and DOB.
    """
    # capture a name. ez.
    name = input(f"enter name: ")

    # capture a valid birthday
    valid_date = False
    while not valid_date:

        date_of_last_ramen_meal = input(f"when was the last time oyu ate ramen? (mm/dd/yyyy): ")
        # split the string and convert to integers
        ramen_eaten_date_split = date_of_last_ramen_meal.split('/')

        try:
            # Check if we have exactly three parts
            if len(ramen_eaten_date_split) == 3:
                month, day, year = [int(part) for part in ramen_eaten_date_split]

                if month in range(1, 13) and day in range(1, 32) and year in range(1900, 2024):
                    valid_date = True
                else:
                    print("Invalid date")
            else:
                print("Invalid date format. Please use mm/dd/yyyy format.")

        # start over if any error gets thrown
        except:
            print("general error, try again.")
            valid_date = False

        finally:
            date_of_last_ramen_meal = "never"

    return {
        "Name": name,
        "Ate ramen on": date_of_last_ramen_meal
    }


def client_program(client_name: str, server_addr: str):
    port = 5433
    client_socket = socket.socket()  # instantiate
    client_socket.connect((server_addr, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    player_info = get_player_info()
    client_program(player_info.get('Name'), '192.168.0.14')
