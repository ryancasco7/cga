from flask import Flask, render_template, request, jsonify
import joblib  
import pandas as pd

import random
import requests
import os

import matplotlib.pyplot as plt
import io
import base64

import ast

from chart import load_and_process_data

app = Flask(__name__)
clf = joblib.load("mix/track_classifier.pkl")



@app.route('/save_file', methods=['POST'])
def save_file():
    if request.method == 'POST':
        user_data = request.form.get('user_data', 'N/A')
        scores = request.form.get('scores', 'N/A')
        recommended_tracks = request.form.get('recommended_tracks', 'N/A')
        name = request.form.get('name', 'Anonymous')
        setting1 = request.form.get('setting1', 'N/A')
        setting2 = request.form.get('setting2', 'N/A')
        work_type = request.form.get('work_type', 'N/A')
        work_env = request.form.get('work_env', 'N/A')
        business_type = request.form.get('business_type', 'N/A')
        immediate_goals = request.form.get('immediate_goals', 'N/A')
        long_term_goal = request.form.get('long_term_goal', 'N/A')
        highest_cluster_score = request.form.get('highest_cluster_score', 'N/A')
        highest_cluster = request.form.get('highest_cluster', 'N/A')
        highly_skilled = request.form.get('highly_skilled', 'N/A')
        skilled = request.form.get('skilled', 'N/A')
        moderately_skilled = request.form.get('moderately_skilled', 'N/A')
        unskilled = request.form.get('unskilled', 'N/A')

        data_to_save = {
            'User Data': [user_data],
            'Scores': [scores],
            'Recommended Tracks': [recommended_tracks],
            'Name': [name],
            'Setting 1': [setting1],
            'Setting 2': [setting2],
            'Work Type': [work_type],
            'Work Environment': [work_env],
            'Business Type': [business_type],
            'Immediate Goals': [immediate_goals],
            'Long-Term Goal': [long_term_goal],
            'Highest Cluster Score': [highest_cluster_score],
            'Highest Cluster': [highest_cluster],
            'Highly Skilled': [highly_skilled],
            'Skilled': [skilled],
            'Moderately Skilled': [moderately_skilled],
            'Unskilled': [unskilled]
        }

        file_path = 'user_data.xlsx'

        if os.path.exists(file_path):
            existing_data = pd.read_excel(file_path)

            new_data = pd.DataFrame(data_to_save)

            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            
            updated_data.to_excel(file_path, index=False)
        else:

            new_data = pd.DataFrame(data_to_save)
            new_data.to_excel(file_path, index=False)

    return render_template('result.html', saved_conf=True)


@app.route('/history_log')
def history_log():
    file_path = 'user_data.xlsx'

    try:
        data = pd.read_excel(file_path)
    except FileNotFoundError:
        data = pd.DataFrame()  
        
    data_list = data.to_dict(orient='records')
    
    return render_template('history_log.html', data=data_list)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():

    scores = {
        "HOME_ECO": 0,
        "HUMSS": 0,
        "ICT": 0,
        "STEM": 0,
        "ARTS_DESIGN": 0,
        "INDUSTRIAL_ARTS": 0,
        "GENERAL": 0,
        "AGRI_FISHERIES": 0,
        "ABM": 0,
        "SPORTS": 0
    }
    
    Cluster_score = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
    }

    user_data = {
        "name": request.form.get('name', 'Anonymous'),
        "age": request.form.get('age', 'N/A'),
        "gender": request.form.get('gender', 'N/A'),
        "grade": request.form.get('grade', 'N/A'),
        "school": request.form.get('school', 'N/A')
    }


    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    grade = request.form.get('grade')
    school = request.form.get('school')


    setting1 = request.form.get('setting1')
    setting2 = request.form.get('setting2')

    work_type = request.form.get('work_type')
    work_env = request.form.get('work_env')
    business_type = request.form.get('business_type')

    immediate_goals = request.form.getlist('immediate_goals')
    long_term_goal = request.form.get('long_term_goal')


    work_type = request.form.get('work_type')
    work_env = request.form.get('work_env')
    immediate_goals = request.form.get('immediate_goals')

    work_type_scores = {
        "teaching, healthcare, or social work": ["HOME_ECO", "HUMSS"],
        "computers, IT, or engineering": ["ICT", "STEM"],
        "writing, design, or photography": ["ICT", "ARTS_DESIGN"],
        "construction, cooking, or crafting": ["INDUSTRIAL_ARTS", "GENERAL"],
        "project management or planning": ["AGRI_FISHERIES", "ABM"]
    }

    for key in work_type_scores.get(work_type, []):
        scores[key] += 1

    work_env_scores = {
        "Working in an office": ["HOME_ECO", "HUMSS", "ICT", "STEM"],
        "Working from home or anywhere": ["SPORTS", "ARTS_DESIGN", "AGRI_FISHERIES"],
        "Working outside in nature or travel": ["HUMSS", "SPORTS", "GENERAL"],
        "Working with a team or group": ["SPORTS", "GENERAL"],
        "Working mostly on your own": ["AGRI_FISHERIES", "ABM", "ICT", "STEM"]
    }

    for key in work_env_scores.get(work_env, []):
        scores[key] += 1

    immediate_goals_scores = {
        "Finish schooling": ["HOME_ECO", "HUMSS", "ICT", "STEM"],
        "Explore different careers": ["SPORTS", "ARTS_DESIGN", "AGRI_FISHERIES", "STEM"],
        "Join clubs or activities": ["HUMSS", "SPORTS", "GENERAL", "ARTS_DESIGN"],
        "Improve my grades": ["STEM", "GENERAL"],
        "Take extra classes": ["AGRI_FISHERIES", "ABM", "ICT", "STEM"],
        "Learn a new skill": ["HUMSS", "SPORTS", "GENERAL", "ICT"],
        "Save money": ["HUMSS", "GENERAL", "AGRI_FISHERIES"],
        "Volunteer": ["AGRI_FISHERIES", "ABM", "SPORTS", "STEM"]
    }

    def safe_int(value, default=0):
        try:
            return int(value.strip()) if value and value.strip().isdigit() else default
        except ValueError:
            return default

    skills = {
        "written_comm": safe_int(request.form.get('written_comm', '0')),
        "verbal_comm": safe_int(request.form.get('verbal_comm', '0')),
        "problem_solving": safe_int(request.form.get('problem_solving', '0')),
        "teamwork": safe_int(request.form.get('teamwork', '0')),
        "analytical": safe_int(request.form.get('analytical', '0')),
        "reactive": safe_int(request.form.get('reactive', '0')),
        "creative": safe_int(request.form.get('creative', '0')),
        "numeracy": safe_int(request.form.get('numeracy', '0')),
        "leadership": safe_int(request.form.get('leadership', '0')),
        "commercial": safe_int(request.form.get('commercial', '0')),
        "decision": safe_int(request.form.get('decision', '0')),
    }

    if skills["written_comm"] <= 4:
        for strand in ["ICT", "STEM", "HUMSS"]:
            scores[strand] += 1
    if skills["verbal_comm"] <= 3:
        for strand in ["HUMSS", "ABM", "ARTS_DESIGN", "GENERAL"]:
            scores[strand] += 1
    if skills["problem_solving"] <= 4:
        for strand in ["STEM", "ICT", "INDUSTRIAL_ARTS", "AGRI_FISHERIES"]:
            scores[strand] += 1
    if skills["teamwork"] <= 2:
        for strand in ["SPORTS", "ABM", "HUMSS", "ARTS_DESIGN", "GENERAL"]:
            scores[strand] += 1
    if skills["analytical"] <= 5:
        for strand in ["STEM", "ICT", "HUMSS", "GENERAL"]:
            scores[strand] += 1
    if skills["reactive"] <= 3:
        for strand in ["SPORTS", "INDUSTRIAL_ARTS", "AGRI_FISHERIES", "HOME_ECO"]:
            scores[strand] += 1
    if skills["creative"] <= 4:
        for strand in ["ARTS_DESIGN", "HUMSS", "ABM", "HOME_ECO"]:
            scores[strand] += 1
    if skills["numeracy"] <= 3:
        for strand in ["STEM", "ABM", "ICT"]:
            scores[strand] += 1
    if skills["leadership"] <= 4:
        for strand in ["ABM", "HUMSS", "SPORTS", "GENERAL"]:
            scores[strand] += 1
    if skills["commercial"] <= 2:
        for strand in ["ABM", "HOME_ECO", "ICT"]:
            scores[strand] += 1
    if skills["decision"] <= 4:
        for strand in ["STEM", "HUMSS", "ABM", "SPORTS"]:
            scores[strand] += 1


    # cluster a
    Aliketo = request.form.getlist('AlikeTo') 
    Aam = request.form.getlist('Aam') 
    AinterestedIn = request.form.getlist('interestedIn')  

    ART_DESIGN = 0
    
    Aliketo_matches = [item for item in Aliketo if item in ["pictureThings", "workHands", "perform", "playInstrument", "artsCrafts", "recordAudioVideo", "designDisplays", "decoratePlaces", "creativeProjects"]]
    ART_DESIGN += len(Aliketo_matches)  
    
    Aam_matches = [item for item in Aam if item in ["goodHands", "creative", "attentiveDetails", "versatile", "planner", "patientPersistent"]]
    ART_DESIGN += len(Aam_matches)  
    
    AinterestedIn_matches = [item for item in AinterestedIn if item in ["artGraphic", "music", "speechDrama", "audioVideo", "cultureArts"]]
    ART_DESIGN += len(AinterestedIn_matches)  

    scores["ARTS_DESIGN"] += ART_DESIGN
    Cluster_score["A"] += ART_DESIGN
    
    # cluster B
    Bliketo = request.form.getlist('BlikeTo') 
    Bam = request.form.getlist('Bam') 
    BinterestedIn = request.form.getlist('BinterestedIn')  

    SPORTS = 0
    Bliketo_matches = [item for item in Bliketo if item in ["outdoorActivities", "athleteSomeday", "sportsActivities", "coachSports", "artsCrafts", "readSportsMagazines", "watchSportsEvents", "representCountrySports", "strenuousActivities", "organizeSportsClinics"]]
    SPORTS += len(Bliketo_matches)  
    
    Bam_matches = [item for item in Bam if item in ["physicallyActive", "sportsInclined", "persistentDedicated", "competitive", "truthful", "attentive"]]
    SPORTS += len(Bam_matches)  
    
    BinterestedIn_matches = [item for item in BinterestedIn if item in ["sportsActivities", "coachingTasks", "athletics", "physicalActivities", "outdoorEvents"]]
    SPORTS += len(BinterestedIn_matches)  

    scores["SPORTS"] += SPORTS
    Cluster_score["B"] += SPORTS
    
    # cluster C
    Cliketo = request.form.getlist('ClikeTo') 
    Cam = request.form.getlist('Cam') 
    CinterestedIn = request.form.getlist('CinterestedIn')  

    HOME_ECO = 0
    ICT = 0
    INDUSTRIAL_ARTS = 0
    AGRI_FISHERIES = 0
    
    Cliketo_matches = [item for item in Cliketo if item in ["cookKitchenActivities", "makeHandicrafts", "workWithHands", "repairToolsMachines", "planBreedAnimals", "entertainGuests", "manualTasksActivities", "assembleThings", "produceHandsOnResults"]]
    HOME_ECO += len(Cliketo_matches)
    ICT += len(Cliketo_matches) 
    INDUSTRIAL_ARTS += len(Cliketo_matches) 
    AGRI_FISHERIES += len(Cliketo_matches) 
    
    Cam_matches = [item for item in Cam if item in ["practical", "dependable", "streetSmart", "techSavy", "entrepreneurial", "mechanical"]]
    HOME_ECO += len(Cam_matches)
    ICT += len(Cam_matches) 
    INDUSTRIAL_ARTS += len(Cam_matches) 
    AGRI_FISHERIES += len(Cam_matches)  
    
    CinterestedIn_matches = [item for item in CinterestedIn if item in ["technicalSkills", "civilTechnology", "drafting", "computerHardware", "servicing", "culinaryArts", "foodBeverageServices"]]
    HOME_ECO += len(CinterestedIn_matches)
    ICT += len(CinterestedIn_matches) 
    INDUSTRIAL_ARTS += len(CinterestedIn_matches) 
    AGRI_FISHERIES += len(CinterestedIn_matches)  

    scores["HOME_ECO"] += HOME_ECO
    scores["ICT"] += ICT
    scores["INDUSTRIAL_ARTS"] += INDUSTRIAL_ARTS
    scores["AGRI_FISHERIES"] += AGRI_FISHERIES
    
    Cluster_score["C"] += HOME_ECO + ICT + INDUSTRIAL_ARTS + AGRI_FISHERIES
    
    # cluster D
    Dliketo = request.form.getlist('DlikeTo') 
    Dam = request.form.getlist('Dam') 
    DinterestedIn = request.form.getlist('DinterestedIn')  

    HUMSS = 0
    STEM = 0
    GENERAL = 0
    AMB = 0
    
    Dliketo_matches = [item for item in Dliketo if item in ["workWithNumbersDetails", "useFactsPredictions", "analyzeFinancialInformation", "handleMoney", "keepAccurateRecords", "browseNewProducts", "followTrends", "communicateIdeas", "persuadePeople"]]
    HUMSS += len(Dliketo_matches)
    STEM += len(Dliketo_matches) 
    GENERAL += len(Dliketo_matches) 
    AMB += len(Dliketo_matches) 
    
    Dam_matches = [item for item in Dam if item in ["logical", "entrepreneurial", "precise", "inquisitive", "detailOriented", "selfConfident"]]
    HUMSS += len(Dam_matches)
    STEM += len(Dam_matches) 
    GENERAL += len(Dam_matches) 
    AMB += len(Dam_matches) 
    
    DinterestedIn_matches = [item for item in DinterestedIn if item in ["accounting", "mathematics", "economics", "bankingFinance", "businessMarketing"]]
    HUMSS += len(DinterestedIn_matches)
    STEM += len(DinterestedIn_matches) 
    GENERAL += len(DinterestedIn_matches) 
    AMB += len(DinterestedIn_matches)  

    scores["HUMSS"] += HUMSS
    scores["STEM"] += STEM
    scores["GENERAL"] += GENERAL
    scores["ABM"] += AMB
    
    Cluster_score["D"] += HUMSS + STEM + GENERAL + AMB
    
        # cluster E
    Eliketo = request.form.getlist('ElikeTo') 
    Eam = request.form.getlist('Eam') 
    EinterestedIn = request.form.getlist('EinterestedIn')  

    ICT = 0
    STEM = 0
    GENERAL = 0
   
    
    Eliketo_matches = [item for item in Eliketo if item in ["workWithNumbersDetails", "useFactsPredictions", "analyzeFinancialInformation", "handleMoney", "keepAccurateRecords", "browseNewProducts", "followTrends", "communicateIdeas", "persuadePeople"]]
    ICT += len(Eliketo_matches)
    STEM += len(Eliketo_matches) 
    GENERAL += len(Eliketo_matches) 
  
    Eam_matches = [item for item in Eam if item in ["logical", "entrepreneurial", "precise", "inquisitive", "detailOriented", "selfConfident"]]
    ICT += len(Eam_matches)
    STEM += len(Eam_matches) 
    GENERAL += len(Eam_matches) 
    
    EinterestedIn_matches = [item for item in EinterestedIn if item in ["accounting", "mathematics", "economics", "bankingFinance", "businessMarketing"]]
    HUMSS += len(EinterestedIn_matches)
    STEM += len(EinterestedIn_matches) 
    GENERAL += len(EinterestedIn_matches)  

    scores["ICT"] += ICT
    scores["STEM"] += STEM
    scores["GENERAL"] += GENERAL
    Cluster_score["E"] += ICT + STEM + GENERAL
    
    #cluster f
    Fliketo = request.form.getlist('FlikeTo') 
    Fam = request.form.getlist('Fam') 
    FinterestedIn = request.form.getlist('FinterestedIn')  
    
    HUMSS  = 0
    AMB = 0
    INDUSTRIAL_ARTS = 0
   
    Fliketo_matches = [item for item in Fliketo if item in ["workWithNumbersDetails", "useFactsPredictions", "analyzeFinancialInformation", "handleMoney", "keepAccurateRecords", "browseNewProducts", "followTrends", "communicateIdeas", "persuadePeople"]]
    HUMSS += len(Fliketo_matches)
    AMB += len(Fliketo_matches) 
    INDUSTRIAL_ARTS += len(Fliketo_matches) 
  
    Fam_matches = [item for item in Fam if item in ["logical", "entrepreneurial", "precise", "inquisitive", "detailOriented", "selfConfident"]]
    HUMSS += len(Fam_matches)
    AMB += len(Fam_matches) 
    INDUSTRIAL_ARTS += len(Fam_matches) 
    
    FinterestedIn_matches = [item for item in FinterestedIn if item in ["accounting", "mathematics", "economics", "bankingFinance", "businessMarketing"]]
    HUMSS += len(FinterestedIn_matches)
    AMB += len(FinterestedIn_matches) 
    INDUSTRIAL_ARTS += len(FinterestedIn_matches)  

    scores["HUMSS"] += HUMSS
    scores["ABM"] += AMB
    scores["INDUSTRIAL_ARTS"] += INDUSTRIAL_ARTS
    Cluster_score["F"] += HUMSS + AMB + INDUSTRIAL_ARTS

    highest_cluster = max(Cluster_score, key=Cluster_score.get)
    highest_cluster_score = Cluster_score[highest_cluster]

    highest_score = max(scores.values())
    recommended_tracks = [track for track, score in scores.items() if score == highest_score]
    
    # debug
    # print(f"Cluster scores: {Cluster_score}")
    # print(f"Track scores: {scores}")
    # print(f"Highest cluster: {highest_cluster} with score {highest_cluster_score}")
    # print(f"Recommended tracks: {recommended_tracks}")


    def get_skill_value(skill_name):
        value = request.form.get(skill_name, '')
        try:
            return int(value) if value else 0  
        except ValueError:
            return 0  

    skills = {
        "Written Communication": get_skill_value('written_comm'),
        "Verbal Communication": get_skill_value('verbal_comm'),
        "Problem Solving": get_skill_value('problem_solving'),
        "Teamwork": get_skill_value('teamwork'),
        "Analytical Ability": get_skill_value('analytical'),
        "Reactive Ability": get_skill_value('reactive'),
        "Creative Thinking": get_skill_value('creative'),
        "Numeracy": get_skill_value('numeracy'),
        "Leadership": get_skill_value('leadership'),
        "Decision Making": get_skill_value('decision'),
    }
    
    highly_skilled = [skill for skill, rating in skills.items() if rating == 5]
    skilled = [skill for skill, rating in skills.items() if 3 <= rating <= 4]
    moderately_skilled = [skill for skill, rating in skills.items() if 2 <= rating <= 2]
    unskilled = [skill for skill, rating in skills.items() if rating < 2]

    return render_template(
    'result.html',
        user_data=user_data,
        scores=scores,
        recommended_tracks=recommended_tracks,
        name=name,
        setting1=setting1,
        setting2=setting2,
        work_type=work_type,
        work_env=work_env,
        business_type=business_type,
        immediate_goals=immediate_goals,
        long_term_goal=long_term_goal,
        highest_cluster_score=highest_cluster_score,
        highest_cluster=highest_cluster,
        highly_skilled=highly_skilled,
        skilled=skilled,
        moderately_skilled=moderately_skilled,
        unskilled=unskilled,
    )




@app.route('/careers')
def careers():
    API_KEY = "bf80b42ce4msh395ac8583ec140bp11c26ajsnfdbf75019027"
    API_HOST = "linkedin-jobs-api2.p.rapidapi.com"

    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY,
    }

    url = f"https://{API_HOST}/active-jb-24h"
    params = {
        "title_filter": "Data Engineer",
        "location_filter": "United States",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        jobs = response.json()  
    else:
        jobs = []  

    return render_template('careers.html', jobs=jobs)


file_path = "user_data.xlsx"

def load_data():
    """Load data from the Excel file and process it"""
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        return {}, {}, {}, {}, {}

    if not {'User Data', 'Scores', 'Highest Cluster Score', 'Highest Cluster'}.issubset(df.columns):
        return {}, {}, {}, {}, {}

    def safe_parse(x):
        try:
            return ast.literal_eval(x) if isinstance(x, str) else {}
        except (ValueError, SyntaxError):
            return {}

    user_data_list = df['User Data'].apply(safe_parse)
    scores_list = df['Scores'].astype(str).tolist()

    df = df.dropna(subset=['Highest Cluster Score', 'Highest Cluster'])
    df = df[df['Highest Cluster'] != 'Unknown']

    cluster_scores = {}
    for _, row in df.iterrows():
        cluster = row['Highest Cluster']
        score = row['Highest Cluster Score']
        cluster_scores[cluster] = cluster_scores.get(cluster, 0) + score

    gender_counts, grade_counts, school_counts, total_track_scores = {}, {}, {}, {}


    for index, user in enumerate(user_data_list):
        gender = user.get('gender', 'Unknown')
        grade = user.get('grade', 'Unknown')
        school = user.get('school', 'Unknown')

        try:
            scores = ast.literal_eval(scores_list[index])
            if not isinstance(scores, dict):
                scores = {}
        except (ValueError, SyntaxError):
            scores = {}

        for track, score in scores.items():
            total_track_scores[track] = total_track_scores.get(track, 0) + score

        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
        school_counts[school] = school_counts.get(school, 0) + 1

    return gender_counts, grade_counts, school_counts, total_track_scores, cluster_scores



@app.route('/chart-data')
def chart_data():
    
    age_counts, gender_counts, grade_counts, school_counts, total_track_scores, cluster_scores = load_and_process_data()

    return jsonify({
        "age": age_counts, 
        "gender": gender_counts,
        "grade": grade_counts,
        "school": school_counts,
        "scores": total_track_scores,
        "cluster_scores": cluster_scores
    })

@app.route('/graphs')
def graphs():
    return render_template("graph.html")




@app.route('/tracks')
def tracks():
    return render_template('tracks.html')

@app.route('/opportunity')
def opportunity():
    return render_template('opportunity.html')

@app.route('/guidance')
def guidance():
    return render_template('guidance.html')

if __name__ == '__main__':
    app.run(debug=True)