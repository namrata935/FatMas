import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import pandas as pd

class CityTransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("City Transport App")
        self.root.geometry("800x400")  # Increased the initial window size
        self.root.configure(bg='#add8e6')  # Set background color to light blue

        self.create_button()

    def create_button(self):
        button = tk.Button(self.root, text="Select Locations", command=self.open_location_page, bg='blue', fg='dark blue', font=('Helvetica', 20))
        button.pack(pady=20)

    def open_location_page(self):
        location_window = tk.Toplevel(self.root)
        location_window.title("Select Locations")
        location_window.geometry("800x400")  # Increased the location window size
        location_window.configure(bg='#add8e6')  # Set background color to light blue

        from_label = tk.Label(location_window, text="From:", bg='#add8e6', fg='black', font=('Helvetica', 20))
        from_label.grid(row=1, column=0, padx=15, pady=15)

        fastag_frame = tk.Frame(location_window, bg='black', pady=20)
        fastag_frame.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="w")

        fastag_label = tk.Label(fastag_frame, text="FASTAG AMOUNT: 1000", bg='black', fg='red', font=('Helvetica', 20))
        fastag_label.pack()

        to_label = tk.Label(location_window, text="To:", bg='#add8e6', fg='black', font=('Helvetica', 20))
        to_label.grid(row=2, column=0, padx=15, pady=15)

        from_var = tk.StringVar()
        to_var = tk.StringVar()

        from_cities = ["Mumbai", "Kolkata", "Delhi", "Chennai", "Bengaluru"]
        to_cities = ["Delhi", "Kolkata", "Bengaluru", "Chennai", "Hyderabad", "Ahmedabad", "Pune", "Surat",
                     "Jaipur", "Lucknow", "Kanpur", "Indore", "Vizag", "Vadodara", "Coimbatore", "Thiruvananthapuram",
                     "Nagpur", "Varanasi", "Patna", "Ghaziabad", "Navi Mumbai", "Noida", "Vijaywada", "Amritsar"]

        from_dropdown = ttk.Combobox(location_window, textvariable=from_var, values=from_cities, state="readonly", background='white', font=('Helvetica', 20))
        from_dropdown.grid(row=1, column=1, padx=15, pady=15)

        to_dropdown = ttk.Combobox(location_window, textvariable=to_var, values=[], state="readonly", background='white', font=('Helvetica', 20))
        to_dropdown.grid(row=2, column=1, padx=15, pady=15)

        route_choice_label = tk.Label(location_window, text="Choose Route:", bg='#add8e6', fg='black', font=('Helvetica', 20))
        route_choice_label.grid(row=3, column=0, padx=15, pady=15, sticky="e")

        route_var = tk.StringVar()
        route_var.set("Fastest")  # Default choice

        fastest_radio = tk.Radiobutton(location_window, text="Fastest", variable=route_var, value="Fastest", font=('Helvetica', 18))
        fastest_radio.grid(row=3, column=1, padx=15, pady=15, sticky="w")

        cheapest_radio = tk.Radiobutton(location_window, text="Cheapest", variable=route_var, value="Cheapest", font=('Helvetica', 18))
        cheapest_radio.grid(row=3, column=2, padx=15, pady=15, sticky="w")

        enter_button = tk.Button(location_window, text="Enter", command=lambda: self.calculate_final_amount(from_var.get(), to_var.get(), route_var.get()), bg='blue', fg='dark blue', font=('Helvetica', 20))
        enter_button.grid(row=4, column=1, pady=20)

        def update_to_dropdown(*args):
            selected_from_city = from_var.get()
            updated_to_cities = [city for city in to_cities if city != selected_from_city]
            to_dropdown['values'] = updated_to_cities
            to_var.set(updated_to_cities[0] if updated_to_cities else "")

        from_var.trace_add("write", update_to_dropdown)

    def calculate_final_amount(self, start_city, end_city, route_type):
        initial_amount = 5000
        toll = self.calculate_toll(start_city, end_city, route_type)

        final_amount = initial_amount - toll

        result_window = tk.Toplevel(self.root)
        result_window.title("Result")
        result_window.geometry("800x400")
        result_window.configure(bg='#add8e6')

        # Results Table
        columns = ["Start City", "End City", "Route Type", "Initial Amount", "Toll Amount", "Final Amount"]
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 'bold', 20), foreground = 'white', background='blue')  # Adjust the font size for column headings
        style.configure("Treeview", font=('Helvetica', 18), background='blue')  # Adjust the font size for table content
        results_table = ttk.Treeview(result_window, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            results_table.heading(col, text=col)
        results_table.pack(pady=10)

        # Inserting data into the table
        results_table.insert("","end", values=["START CITY", 'END CITY', 'ROUTE', 'INITIAL AMOUNT', 'TOLL', 'FINAL AMOUNT'])
        results_table.insert("", "end", values=[start_city, end_city, route_type, initial_amount, toll, final_amount])

        # Display FASTAG information in a black box with red text
        if final_amount > 0:
            fastag_info = f"FASTAG AMOUNT: {final_amount}"
            fastag_label = tk.Label(result_window, text=fastag_info, bg='black', fg='red', font=('Helvetica', 20))
            fastag_label.pack(pady=10)
        elif final_amount < 0:
            recharge_info = f"FASTAG RECHARGE: {-final_amount}"
            recharge_label = tk.Label(result_window, text=recharge_info, bg='black', fg='red', font=('Helvetica', 20))
            recharge_label.pack(pady=10)

    def calculate_toll(self, start_city, end_city, route_type):
        toll_booth_data = pd.read_csv('toll_booth.csv')

        if route_type == "Fastest":
            vehicle_type = simpledialog.askstring("Vehicle Type", "Enter Vehicle Type (Car/Truck/LMC):", parent=self.root)
            toll = toll_booth_data[(toll_booth_data['Start'] == start_city) & (toll_booth_data['End'] == end_city)][f'{vehicle_type.title()}_fastest'].values[0]
        elif route_type == "Cheapest":
            vehicle_type = simpledialog.askstring("Vehicle Type", "Enter Vehicle Type (Car/Truck/LMC):", parent=self.root)
            toll = toll_booth_data[(toll_booth_data['Start'] == start_city) & (toll_booth_data['End'] == end_city)][f'{vehicle_type.title()}_cheapest'].values[0]
        else:
            toll = 0

        return toll

if __name__ == "__main__":
    root = tk.Tk()
    app = CityTransportApp(root)
    root.mainloop()
