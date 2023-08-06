from ibrahim_library import event_accuracy_score

# Expected = unser ground-truth (GT) in zeitlicher abfolge als array
expected = [1,2,2,2,2,2,2,3,3,1,1,2,3,4,4,4]
# Predicted = unsere (angenommene) Ausgabe eines klassifizierers
predicted =  [1,1,1,2,2,2,2,3,3,1,1,2,3,3,3,4]

# TODO: Diese sollten auch funktionieren
erre, accf = event_accuracy_score(expected, predicted)
print(f"ERRE: {erre:.2f}, ACCF: {accf:.2f}")  # ERRE: 1.00, ACCF: 0.50

erre, accf = event_accuracy_score(expected, predicted, normalize=False)
print(f"ERRE: {erre:.2f}%, ACCF: {accf:.2f}%")  # ERRE: 100.00%, ACCF: 50.00%
