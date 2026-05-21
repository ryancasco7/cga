import pandas as pd
import ast 

file_path = "user_data.xlsx"


if file_path.endswith(".csv"):
    df = pd.read_csv(file_path, encoding="utf-8")
elif file_path.endswith(".xlsx"):
    df = pd.read_excel(file_path, engine="openpyxl")
else:
    raise ValueError("Unsupported file format. Use CSV or Excel.")


df.columns = df.columns.str.strip()


if "Scores" in df.columns:
    print("'Scores' column found!")


    df["Scores"] = df["Scores"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    def get_highest_score(scores_dict):
        if isinstance(scores_dict, dict):  
            return max(scores_dict, key=scores_dict.get) 
        return None

    df["Top Track"] = df["Scores"].apply(get_highest_score)

    print("🔹 First 5 rows with highest-scoring track:")
    print(df[["Scores", "Top Track"]].head())

else:
    print(" 'Scores' column is missing! Available columns:", df.columns.tolist())
    
df.to_csv("processed_user_data.csv", index=False)
