import socket


def get_player_info() -> dict:
    """
    prompt player for name and date of birth.
    :return: dictionary of player name and DOB.
    """
    # capture a name. ez.
    name = input(f"enter name: ")

    # capture a valid birthday
    valid_birthday = False
    while not valid_birthday:

        birthdate = input(f"enter your birthday (mm/dd/yyyy): ")
        # split the string and convert to integers
        dob_split = birthdate.split('/')

        try:
            # Check if we have exactly three parts
            if len(dob_split) == 3:
                birth_month, birth_day, birth_year = [int(part) for part in dob_split]

                if birth_month in range(1, 13) and birth_day in range(1, 32) and birth_year in range(1900, 2024):
                    valid_birthday = True
                else:
                    print("Invalid date")
            else:
                print("Invalid date format. Please use mm/dd/yyyy format.")

        # start over if any error gets thrown
        except:
            print("general error, try again.")
            valid_birthday = False

    return {
        "Name": name,
        "Date of Birth": birthdate
    }


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    get_player_info()
