from probability4e import BayesNet, T, F, enumeration_ask



class diagnostic:
    def __init__(self):
        self.bn = BayesNet([
            # Priors
            ("Asia", "", 0.01),
            ("Smoking", "", 0.50),

            # Single-parent: {ParentValue: P(Node=True | ParentValue)}
            ("Tuberculosis", "Asia", {T: 0.05, F: 0.01}),
            ("LungCancer", "Smoking", {T: 0.10, F: 0.01}),
            ("Bronchitis", "Smoking", {T: 0.60, F: 0.30}),

            # TBorC = Tuberculosis OR LungCancer
            ("TBorC", "Tuberculosis LungCancer", {
                (T, T): 1.0,
                (T, F): 1.0,
                (F, T): 1.0,
                (F, F): 0.0,
            }),

            # Xray depends on TBorC
            ("Xray", "TBorC", {
                T: 0.99,
                F: 0.05,
            }),

            # Dyspnea depends on TBorC and Bronchitis
            ("Dyspnea", "TBorC Bronchitis", {
                (T, T): 0.90,
                (T, F): 0.70,
                (F, T): 0.80,
                (F, F): 0.10,
            }),
        ])
    
    def diagnose(self, visit_to_asia, smoking, xray_result, dyspnea):
        evidence = {}
        # Visit to Asia
        if visit_to_asia == "Yes":
            evidence["Asia"] = T
        elif visit_to_asia == "No":
            evidence["Asia"] = F

        # Smoking
        if smoking == "Yes":
            evidence["Smoking"] = T
        elif smoking == "No":
            evidence["Smoking"] = F

        # Xray
        if xray_result == "Abnormal":
            evidence["Xray"] = T
        elif xray_result == "Normal":
            evidence["Xray"] = F

        # Dyspnea
        if dyspnea == "Present":
            evidence["Dyspnea"] = T
        elif dyspnea == "Absent":
            evidence["Dyspnea"] = F

        # Query distributions
        tb_dist = enumeration_ask("Tuberculosis", evidence, self.bn)
        ca_dist = enumeration_ask("LungCancer", evidence, self.bn)
        br_dist = enumeration_ask("Bronchitis", evidence, self.bn)

        # Grab P(variable=True | evidence)
        probs = {
            "Tuberculosis": tb_dist[T],
            "Cancer":       ca_dist[T],
            "Bronchitis":   br_dist[T],
        }

        best = max(probs, key=probs.get)
        return best, probs

diag = diagnostic()
