from flask import Flask, jsonify, render_template
from chart import load_and_process_data

app = Flask(__name__)

age_counts, gender_counts, grade_counts, school_counts, total_track_scores, cluster_scores = load_and_process_data()

@app.route('/chart-data')
def chart_data():
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

if __name__ == '__main__':
    app.run(debug=True)
