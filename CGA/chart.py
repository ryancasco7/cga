import pandas as pd
import ast

def load_and_process_data(file_path="user_data.xlsx"):
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("Error: File not found. Using an empty DataFrame.")
        df = pd.DataFrame(columns=['User Data', 'Scores', 'Highest Cluster Score', 'Highest Cluster'])

    required_columns = {'User Data', 'Scores', 'Highest Cluster Score', 'Highest Cluster'}
    if not required_columns.issubset(df.columns):
        print("Error: Required columns missing. Returning empty datasets.")
        return {}, {}, {}, {}, {}, {}

    df['User Data'] = df['User Data'].fillna("{}")

    print("Sample 'User Data' before parsing:", df['User Data'].head())

    def safe_parse(x):
        if isinstance(x, dict):
            return x
        try:
            return ast.literal_eval(x) if isinstance(x, str) else {}
        except (ValueError, SyntaxError, TypeError):
            return {}

    df['User Data'] = df['User Data'].apply(safe_parse)

    print("Sample 'User Data' after parsing:", df['User Data'].head())

    def parse_scores(x):
        try:
            parsed = ast.literal_eval(str(x))
            return parsed if isinstance(parsed, dict) else {}
        except (ValueError, SyntaxError):
            return {}

    df['Scores'] = df['Scores'].apply(parse_scores)

    df = df.dropna(subset=['Highest Cluster Score', 'Highest Cluster'])
    df = df[df['Highest Cluster'] != 'Unknown']

    cluster_scores = df.groupby('Highest Cluster')['Highest Cluster Score'].sum().to_dict()

    gender_counts, grade_counts, school_counts, total_track_scores, age_counts = {}, {}, {}, {}, {}

    for _, row in df.iterrows():
        user = row['User Data']  
        scores = row['Scores']

        gender = user.get('gender', 'Not Specified')
        grade = user.get('grade', 'Not Specified')
        school = user.get('school', 'Not Specified')
        age = str(user.get('age', 'Not Specified'))  

        print(f"Processing user - Age: {age}, Gender: {gender}, Grade: {grade}, School: {school}")

        for track, score in scores.items():
            total_track_scores[track] = total_track_scores.get(track, 0) + score

        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
        school_counts[school] = school_counts.get(school, 0) + 1
        age_counts[age] = age_counts.get(age, 0) + 1  

    return age_counts, gender_counts, grade_counts, school_counts, total_track_scores, cluster_scores

