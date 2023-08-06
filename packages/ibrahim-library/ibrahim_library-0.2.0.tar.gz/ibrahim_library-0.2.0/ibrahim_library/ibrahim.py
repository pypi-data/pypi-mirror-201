def event_accuracy_score(expected, predicted, normalize=True):
   # TODO Hier soll die "Event based evaluation" durchgeführt werden gemäß Paper

    # Initialisiere Variablen für Ideale Ereignisse (Ie), Abgewichene Ereignisse (De), Substituierte Ereignisse (Se), Vorhergesagte Ereignisse (Tf) und Erwartete Ereignisse ohne C (Te)
    Ie = 0
    De = 0
    Se = 0
    Te = len([x for x in expected if x != 'C'])
    TP = 0
    TN = 0
    subst = 0
    Tf = len(predicted)

     # Gehe durch die Liste der erwarteten Ausgaben und vergleiche sie mit der Liste der vorhergesagten Ausgaben
    for i in range(len(expected)):
        if expected[i] == predicted[i]:
            # Wenn die Vorhersage und die Erwartung übereinstimmen, erhöhe Ie und TP oder TN entsprechend
            if expected[i] == 'A':
                TP += 1
            else:
                TN += 1
            Ie += 1
        else:
            # Wenn die Vorhersage und die Erwartung nicht übereinstimmen
            if predicted[i] in expected[i+1:] and predicted[i] != 'C':
                # Wenn das vorhergesagte Ereignis später im Ground-Truth vorkommt und nicht C ist, erhöhe De entsprechend
                De += 1
            elif predicted[i] != 'C':
                # Wenn das vorhergesagte Ereignis nicht später im Ground-Truth vorkommt und nicht C ist, erhöhe Se entsprechend
                Se += 1
            if i+1 < len(predicted) and expected[i] == predicted[i+1]:
                # Wenn das nächste Element in der Vorhersage gleich dem erwarteten Element ist, erhöhe subst entsprechend
                subst += 1
    
    # Berechne erre und accf
    erre = (Ie + De + Se) / Te*100
    accf = (TP + TN - subst) / Tf*100
    
    if normalize:
        return erre / 100, accf / 100
    else:
        return erre, accf
