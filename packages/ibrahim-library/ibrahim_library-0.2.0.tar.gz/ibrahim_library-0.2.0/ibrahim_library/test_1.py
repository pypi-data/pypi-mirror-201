from ibrahim_library import event_accuracy_score

y_pred = [0, 2, 1, 3]
y_true = [0, 1, 2, 3]
erre, accf = event_accuracy_score(y_true, y_pred)
print(f"ERRE: {erre:.2f}, ACCF: {accf:.2f}")  # ERRE: 1.00, ACCF: 0.50

erre, accf = event_accuracy_score(y_true, y_pred, normalize=False)
print(f"ERRE: {erre:.2f}%, ACCF: {accf:.2f}%")  # ERRE: 100.00%, ACCF: 50.00%
