#Yousif Ahmed Jassim 202010375 sec 1
#Hasan Ali Khalil Rajab 202100351 sec 1
import socket
import json
from prettytable import PrettyTable

def send_receive_data(client_socket, type, parameter=""):
#Function to send the request to the server and receive the processed response
    type = type + parameter        #ex: cBAH
    client_socket.send(type.encode("ascii"))
    server_response = client_socket.recv(32768)
    processed_response = json.loads(server_response.decode("ascii"))
    return processed_response

###############################################################################
def print_flight_details():
    # Function to print flight details in a table based on the selected option
    flight_count = len(server_response['flight'])
    table = PrettyTable()
    if option == "a":
        type = "have arrived"
        table.field_names = ["IATA", "Dep Airport", "Arr Time",
                              "Terminal", "Gate"]    #table header
    
    elif option == "b":
        type = "have been delayed"
        table.field_names = ["IATA", "Dep Airport", "Dep Time",
                              "Est Arr Time", "Delay", "Terminal", "Gate"]   
    
    elif option == 'c': 
        if flight_count == 0:
            raise IndexError
        type = f"coming from {city_code}"
        table.field_names = ["IATA", "Dep Airport", "Departure Time",
                              "Est Arr Time", "Departure Gate",
                                "Arrival Gate", "Flight Status"]

    print(f"\n{flight_count} flights {type}.")
    for flight in server_response["flight"]:
        table.add_row(flight)
    print(table)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # configure client socket
        server_ip = "127.0.0.1"
        server_port = 49994
        client_socket.connect((server_ip, server_port))
        client_name = input("Name: ")
        client_socket.send(client_name.encode('ascii'))

        while True:
            print("\nOptions:")
            print("a. Arrived flights")
            print("b. Delayed flights")
            print("c. Incoming Flights from a city")
            print("d. Details of a flight")
            print("e. Quit")
            try:
                option = input(f"{client_name} Select an option (a-e): ").lower()

                if option == 'e':
                    client_socket.send(option.encode("ascii"))
                    server_response = client_socket.recv(1024).decode("ascii")
                    print(server_response)
                    break
                
                elif option in ['a','b']:
                    server_response = send_receive_data(client_socket, option)
                    print_flight_details()
                    
                elif option == 'c':
                    city_code = input("City code (Airport IATA code): ").upper()
                    server_response = send_receive_data(client_socket, option, city_code) 
                    # error message to display it in exceptoin
                    error_msg = "\nNo flights coming from: " + city_code
                    print_flight_details()
                
                elif option == 'd':
                    flight_code = input("IATA: ").upper()
                    server_response = send_receive_data(client_socket, option, flight_code)
                    flight_count = len(server_response['flight'])
                    # error message to display it in exceptoin
                    error_msg = "\nNo flight with this IATA code: " + flight_code
                    if flight_count == 0:
                        raise IndexError
                    
                    table = PrettyTable()
                    #server_response = {"flight":[[iata,..,...,.]
                    #                            ,[iata,...,..,.,],.,.,.]}
                    flight = server_response["flight"][0] 

                    table.field_names = ["IATA", flight[0]]
                    table.add_row(["Departure Airport", flight[1]])
                    table.add_row(["Departure Gate", flight[2]])
                    table.add_row(["Departure Terminal", flight[3]])
                    table.add_row(["Arrival Airport", flight[4]])
                    table.add_row(["Arrival Gate", flight[5]])
                    table.add_row(["Arrival Terminal", flight[6]])
                    table.add_row(["Flight Status", flight[7]])
                    table.add_row(["Scheduled Departure Time", flight[8]])
                    table.add_row(["Scheduled Arrival Time", flight[9]])
                    print(table)
        
                else:
                    print("\nInvalid option choose from (a to e).")  
                   
                
            except KeyboardInterrupt:
                print(f"\n{client_name} forcibly disconnecting.")
                break
            
            except IndexError:
                        print(error_msg)
            
except ConnectionRefusedError:
    print("Make sure to start the server first.")
