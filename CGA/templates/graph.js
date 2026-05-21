document.addEventListener("DOMContentLoaded", function () {
    fetch('/chart-data')
        .then(response => response.json())
        .then(data => {
            // Function to generate random colors dynamically
            function generateColors(numColors) {
                const colors = [];
                for (let i = 0; i < numColors; i++) {
                    const r = Math.floor(Math.random() * 256);
                    const g = Math.floor(Math.random() * 256);
                    const b = Math.floor(Math.random() * 256);
                    colors.push(`rgba(${r}, ${g}, ${b}, 0.6)`);
                }
                return colors;
            }

            // ✅ Age Distribution (Ensures "others" appears)
            const ageLabels = Object.keys(data.age);
            const ageValues = Object.values(data.age);
            new Chart(document.getElementById('ageChart'), {
                type: 'bar',
                data: {
                    labels: ageLabels,
                    datasets: [{
                        label: 'Age Distribution',
                        data: ageValues,
                        backgroundColor: generateColors(ageLabels.length) // Dynamic Colors
                    }]
                }
            });

            // ✅ Gender Distribution
            const genderLabels = Object.keys(data.gender);
            const genderValues = Object.values(data.gender);
            new Chart(document.getElementById('genderChart'), {
                type: 'pie',
                data: {
                    labels: genderLabels,
                    datasets: [{
                        data: genderValues,
                        backgroundColor: generateColors(genderLabels.length) // Dynamic Colors
                    }]
                }
            });

            // ✅ School Distribution
            const schoolLabels = Object.keys(data.school);
            const schoolValues = Object.values(data.school);
            new Chart(document.getElementById('schoolChart'), {
                type: 'bar',
                data: {
                    labels: schoolLabels,
                    datasets: [{
                        label: 'School Distribution',
                        data: schoolValues,
                        backgroundColor: generateColors(schoolLabels.length) // Dynamic Colors
                    }]
                }
            });

            // ✅ Cluster Scores
            const clusterLabels = Object.keys(data.cluster_scores);
            const clusterValues = Object.values(data.cluster_scores);
            new Chart(document.getElementById('clusterChart'), {
                type: 'doughnut',
                data: {
                    labels: clusterLabels,
                    datasets: [{
                        data: clusterValues,
                        backgroundColor: generateColors(clusterLabels.length) // Dynamic Colors
                    }]
                }
            });

            // ✅ Grade Distribution (NEW ADDITION)
            const gradeLabels = Object.keys(data.grade);
            const gradeValues = Object.values(data.grade);
            new Chart(document.getElementById('gradeChart'), {
                type: 'bar',
                data: {
                    labels: gradeLabels,
                    datasets: [{
                        label: 'Grade Distribution',
                        data: gradeValues,
                        backgroundColor: generateColors(gradeLabels.length) // Dynamic Colors
                    }]
                }
            });

        })
        .catch(error => console.error("Error fetching chart data:", error));
});
