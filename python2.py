import random
import time


def print_banner():
  print("=" * 65)
  print("         🚗 KIRAN ACADEMY CAB BOOKING CHATBOT 🛺         ")
  print("=" * 65)


def main():
  # Predefined Cab Rates per km (Task Requirement)
  cab_rates = {1: ("Auto", 12), 2: ("Sedan", 18), 3: ("SUV", 25)}

  # Predefined Routes (Task Requirement)
  routes = {
      1: {"source": "Pune Station", "destination": "Shivajinagar", "distance": 5},
      2: {"source": "Swargate", "destination": "Kothrud", "distance": 8},
      3: {"source": "Hinjawadi", "destination": "Wakad", "distance": 10},
  }

  while True:
    print_banner()
    print("\n--- MAIN MENU ---")
    print("1. Book Ride")
    print("2. Exit")

    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
      print("\n" + "~" * 45)
      print(" STEP 1: CHOOSE CAB TYPE ")
      print("~" * 45)
      print("1. Auto  - ₹12/km")
      print("2. Sedan - ₹18/km")
      print("3. SUV   - ₹25/km")

      cab_choice_input = input("\nSelect cab type (1-3): ").strip()
      if cab_choice_input not in ["1", "2", "3"]:
        print(
            "\n❌ Error: Invalid cab choice! Returning to the main menu.\n"
            + "=" * 65
        )
        continue

      cab_id = int(cab_choice_input)
      cab_name, rate_per_km = cab_rates[cab_id]

      print("\n" + "~" * 45)
      print(" STEP 2: CHOOSE ROUTE ")
      print("~" * 45)
      for r_id, r_info in routes.items():
        print(
            f"{r_id}. {r_info['source']} ➔ {r_info['destination']}"
            f" ({r_info['distance']} km)"
        )

      route_choice_input = input("\nSelect route number (1-3): ").strip()
      if route_choice_input not in ["1", "2", "3"]:
        print(
            "\n❌ Error: Invalid route choice! Returning to the main menu.\n"
            + "=" * 65
        )
        continue

      route_id = int(route_choice_input)
      selected_route = routes[route_id]
      source = selected_route["source"]
      destination = selected_route["destination"]
      distance = selected_route["distance"]

      # Calculate Fare
      total_fare = rate_per_km * distance

      print("\n" + "=" * 45)
      print("          FARE ESTIMATE SUMMARY          ")
      print("=" * 45)
      print(f" Cab Type     : {cab_name} (₹{rate_per_km}/km)")
      print(f" Route        : {source} to {destination}")
      print(f" Distance     : {distance} km")
      print(f" Total Fare   : ₹{total_fare}")
      print("=" * 45)

      # Cancellation / Confirmation Step (Task Requirement)
      print("\n--- BOOKING CONFIRMATION ---")
      print("1. Confirm & Share OTP")
      print("2. Cancel Ride")

      confirm_choice = input("\nEnter your choice (1 or 2): ").strip()

      if confirm_choice == "2":
        print("\n🚫 Ride cancelled successfully before OTP generation.")
        print("Returning to the main menu...\n" + "=" * 65)
        continue
      elif confirm_choice == "1":
        # Generate 4-digit OTP (Task Requirement)
        otp = random.randint(1000, 9999)
        print("\n" + "🔒" * 28)
        print(f"✅ BOOKING CONFIRMED! Your 4-digit OTP is: [ {otp} ]")
        print("ℹ️  RULE: Once the OTP has been shared, cancellation is LOCKED.")
        print("🔒" * 28)

        input("\nPress Enter to return to the main menu...")
        print("=" * 65)
      else:
        print(
            "\n❌ Invalid confirmation choice! Ride cancelled for safety."
            " Returning to main menu.\n"
            + "=" * 65
        )
        continue

    elif choice == "2":
      print("\n" + "=" * 65)
      print("🙏 Thank you for using Kiran Academy Cab Booking Chatbot!")
      print("Have a safe and wonderful day! Goodbye.")
      print("=" * 65)
      break
    else:
      print(
          "\n❌ Invalid choice! Please enter 1 to Book Ride or 2 to Exit.\n"
          + "=" * 65
      )


if __name__ == "__main__":
  main()