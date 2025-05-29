import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def antreneaza_model(cale_fisier, sheet_name):
    df = pd.read_excel(cale_fisier, sheet_name=sheet_name)
    X = df['viteza'].values.reshape(-1, 1)
    y = df['energie totala (Wh)'].values / 1_000_000

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"R2 score: {score:.4f}")

    joblib.dump(model, 'model_turbina_castigatoare.pkl')
    print("Model salvat în model_turbina_castigatoare.pkl")

if __name__ == "__main__":
    # Schimbă aici cu numele fișierului și foaia Excel corespunzătoare turbinei câștigătoare
    antreneaza_model('formule_turbine_complet.xlsx', 'Nordex N100')

