from django.test import TestCase

# Create your tests here.

weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]

print(weapons[2:5])

results = [w for w in weapons if "k" in w.lower()]
print(results)

results2 = []
for w in weapons:
    if "k" in w.lower():
        results2.append(w)

print(results2)
