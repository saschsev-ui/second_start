name = input("Wie heißt du? ")
alter = int(input("Wie alt bist du? "))
zahl_1 = float(input("Gib die erste Zahl ein: "))
zahl_2 = float(input("Gib die zweite Zahl ein: "))

summe = zahl_1 + zahl_2

print(f"Hallo, {name}!")
print(f"Die Summe der beiden Zahlen ist: {summe}")

if alter < 18:
    print("Du bist noch minderjährig.")
    print(f"Du bist in {18 - alter} Jahren volljährig.")
else:
    print("Du bist volljährig. Tolle Sache!")