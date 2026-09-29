# Vacuum Cleaner World (2 rooms: A and B)
# Simple reflex agent: if room is dirty -> clean it, else move to the other room

location = "A"                      # starting room
rooms = {"A": "Dirty", "B": "Dirty"}   # "Dirty" or "Clean"

print("Initial state:", rooms, "| Vacuum in room", location)
print()

step = 1
while rooms["A"] == "Dirty" or rooms["B"] == "Dirty":
    if rooms[location] == "Dirty":
        rooms[location] = "Clean"
        action = "Suck (cleaned room " + location + ")"
    else:
        if location == "A":
            location = "B"
            action = "Move Right (to room B)"
        else:
            location = "A"
            action = "Move Left (to room A)"

    print("Step", step, ":", action)
    print("   State:", rooms, "| Vacuum in room", location)
    step = step + 1

print()
print("Both rooms are clean. Done!")
