import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

class ObesityPredictor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.encoders = {}
        self.accuracy = 0.0
        self.target_names = []
        
    def _clean_data(self, df):
        """Limpeza de ruídos decimais conforme dicionário"""
        cols_to_fix = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = df[col].round().astype(int)
        return df

    def train(self):
        """Carrega, limpa e treina o modelo"""
        df = pd.read_csv(self.data_path)
        df = self._clean_data(df)
        
        categorical_cols = ['Gender', 'family_history', 'FAVC', 'CAEC', 'SMOKE', 
                            'SCC', 'CALC', 'MTRANS', 'Obesity']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.encoders[col] = le
            
        self.target_names = self.encoders['Obesity'].classes_
        
        X = df.drop('Obesity', axis=1)
        y = df['Obesity']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        return self.accuracy

    def predict(self, user_data):
        """Recebe dados do usuário e retorna predição + probabilidades"""
        input_df = pd.DataFrame([user_data])
        input_df = self._clean_data(input_df)
        
        for col, le in self.encoders.items():
            if col != 'Obesity':
                try:
                    # Tenta transformar usando o encoder aprendido
                    input_df[col] = le.transform(input_df[col])
                except:
                    # Fallback para evitar erro em produção
                    input_df[col] = 0 

        pred_idx = self.model.predict(input_df)[0]
        pred_label = self.target_names[pred_idx]
        
        proba = self.model.predict_proba(input_df)[0]
        confidence = proba[pred_idx]
        
        all_probs = dict(zip(self.target_names, proba))
        
        return pred_label, confidence, all_probs