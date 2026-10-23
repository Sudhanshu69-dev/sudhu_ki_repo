from abc import ABC, abstractmethod

class Passenger(ABC):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self): return self._name
    @property
    def age(self): return self._age

    @abstractmethod
    def get_discount_percentage(self) -> float:
        pass

    @abstractmethod
    def get_passenger_type(self) -> str:
        pass

class RegularPassenger(Passenger):
    def get_discount_percentage(self) -> float: return 0.0
    def get_passenger_type(self) -> str: return "Regular"

class StudentPassenger(Passenger):
    def get_discount_percentage(self) -> float: return 0.10
    def get_passenger_type(self) -> str: return "Student"

class Flight:
    def __init__(self, flight_code: str, airline: str, source: str, destination: str, available_seats: int, base_fare: float):
        self._flight_code = flight_code
        self._airline = airline
        self._source = source
        self._destination = destination
        self._available_seats = available_seats
        self._base_fare = base_fare

    @property
    def flight_code(self): return self._flight_code
    @property
    def airline(self): return self._airline
    @property
    def source(self): return self._source
    @property
    def destination(self): return self._destination
    @property
    def available_seats(self): return self._available_seats
    @property
    def base_fare(self): return self._base_fare

    def book_seats(self, count: int):
        if count <= self._available_seats:
            self._available_seats -= count

class Booking:
    def __init__(self, booking_id: str, flight: Flight, passenger: Passenger, ticket_count: int, subtotal: float, discount_amount: float, final_total: float):
        self._booking_id = booking_id
        self._flight = flight
        self._passenger = passenger
        self._ticket_count = ticket_count
        self._subtotal = subtotal
        self._discount_amount = discount_amount
        self._final_total = final_total

    def display_booking_summary(self):
        print("\n" + "=" * 40)
        print("          BOOKING CONFIRMED             ")
        print("=" * 40)
        print(f"Booking ID     : {self._booking_id}")
        print(f"Flight Details : {self._flight.flight_code} ({self._flight.airline}) | {self._flight.source} -> {self._flight.destination}")
        print(f"Passenger Name : {self._passenger.name} (Age: {self._passenger.age})")
        print(f"Passenger Type : {self._passenger.get_passenger_type()}")
        print(f"Tickets Booked : {self._ticket_count}")
        print(f"Base Fare      : ₹{self._flight.base_fare:,.2f} per ticket")
        print(f"Subtotal       : ₹{self._subtotal:,.2f}")
        discount_pct = int(self._passenger.get_discount_percentage() * 100)
        print(f"Discount ({self._passenger.get_passenger_type()}) : -₹{self._discount_amount:,.2f} ({discount_pct}%)")
        print("-" * 40)
        print(f"Final Payable  : ₹{self._final_total:,.2f}")
        print("=" * 40 + "\n")

class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 50, 4000.0),
            Flight("MB202", "Kiran Air", "Mumbai", "Bengaluru", 40, 4500.0),
            Flight("PH303", "Kiran Air", "Pune", "Hyderabad", 30, 3500.0)
        ]
        self.booking_history = []
        self.booking_counter = 1001

    def display_flights(self):
        print("\n" + "-" * 75)
        print("                         AVAILABLE FLIGHTS                               ")
        print("-" * 75)
        print(f"{'Code':<8} | {'Airline':<10} | {'Route':<15} | {'Seats':<6} | {'Base Fare':<10}")
        print("-" * 75)
        for f in self.flights:
            print(f"{f.flight_code:<8} | {f.airline:<10} | {f.source + ' -> ' + f.destination:<15} | {f.available_seats:<6} | ₹{f.base_fare:<10,.2f}")
        print("-" * 75)

    def find_flight_by_code(self, code: str):
        for f in self.flights:
            if f.flight_code.lower() == code.lower():
                return f
        return None

    def _prompt_int(self, message: str) -> int:
        while True:
            val = input(message).strip()
            if val.isdigit():
                return int(val)
            print("❌ Invalid input. Please enter a valid positive number.")

    def _prompt_string(self, message: str) -> str:
        while True:
            val = input(message).strip()
            if val:
                return val
            print("❌ Field cannot be blank. Please try again.")

    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("        KIRAN AIR BOOKING SYSTEM        ")
            print("=" * 40)
            print("1. View Available Flights")
            print("2. Book a Flight")
            print("3. View All Bookings")
            print("4. Exit Application")
            print("=" * 40)
            
            choice_str = input("Enter your choice (1-4): ").strip()
            if not choice_str.isdigit():
                print("❌ Invalid choice format. Please enter a number between 1 and 4.")
                continue
            
            choice = int(choice_str)

            if choice == 1:
                self.display_flights()

            elif choice == 2:
                self.display_flights()
                print("\n--- Booking Process ---")
                f_code = self._prompt_string("Enter flight code: ")
                selected_flight = self.find_flight_by_code(f_code)

                if not selected_flight:
                    print("⚠️ Booking failed: Flight code does not exist.")
                    continue

                name = self._prompt_string("Enter passenger name: ")
                age = self._prompt_int("Enter passenger age: ")
                if age <= 0:
                    print("⚠️ Booking failed: Age must be greater than 0.")
                    continue

                passenger = None
                while not passenger:
                    p_type = self._prompt_string("Passenger type (Regular/Student): ")
                    if p_type.lower() == "student":
                        passenger = StudentPassenger(name, age)
                    elif p_type.lower() == "regular":
                        passenger = RegularPassenger(name, age)
                    else:
                        print("❌ Invalid passenger type. Please type 'Regular' or 'Student'.")

                tickets = self._prompt_int("Enter number of tickets: ")
                if tickets <= 0:
                    print("⚠️ Booking failed: Ticket count must be greater than 0.")
                    continue

                if tickets > selected_flight.available_seats:
                    print(f"⚠️ Booking failed: Not enough seats available. Only {selected_flight.available_seats} seats left.")
                    continue

                # Calculations
                subtotal = selected_flight.base_fare * tickets
                discount_amount = subtotal * passenger.get_discount_percentage()
                final_total = subtotal - discount_amount

                # Confirm and save
                selected_flight.book_seats(tickets)
                booking_id = f"BK{self.booking_counter}"
                self.booking_counter += 1
                
                new_booking = Booking(booking_id, selected_flight, passenger, tickets, subtotal, discount_amount, final_total)
                self.booking_history.append(new_booking)
                
                new_booking.display_booking_summary()

            elif choice == 3:
                if not self.booking_history:
                    print("\n📭 No bookings found in the system yet.")
                else:
                    print("\n" + "=" * 40)
                    print("           ALL BOOKING HISTORY          ")
                    print("=" * 40)
                    for b in self.booking_history:
                        b.display_booking_summary()

            elif choice == 4:
                print("\nThank you for choosing Kiran Air. Have a safe flight! ✈️")
                break
            else:
                print("❌ Invalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    app = FlightBookingSystem()
    app.run()