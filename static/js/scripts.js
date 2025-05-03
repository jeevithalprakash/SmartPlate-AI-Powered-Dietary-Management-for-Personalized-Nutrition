document.getElementById('feedback-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const feedback = document.getElementById('feedback').value;
    fetch('/process_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `feedback=${encodeURIComponent(feedback)}`,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('feedback-result').innerHTML = `
            <p>Satisfaction: ${data.satisfaction}</p>
            <p>Improvement Score: ${data.improvement.toFixed(2)}</p>
        `;
    });
});

document.getElementById('analyze-survey').addEventListener('click', function() {
    fetch('/analyze_survey')
    .then(response => response.json())
    .then(data => {
        document.getElementById('survey-result').innerHTML = `
            <pre>${JSON.stringify(data.report, null, 2)}</pre>
            <p>Accuracy: ${data.accuracy}</p>
        `;
    });
});

document.getElementById('analyze-usage').addEventListener('click', function() {
    fetch('/analyze_usage')
    .then(response => response.json())
    .then(data => {
        document.getElementById('usage-result').innerHTML = `
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
    });
});

document.getElementById('evaluate-taste').addEventListener('click', function() {
    fetch('/evaluate_taste')
    .then(response => response.json())
    .then(data => {
        document.getElementById('taste-result').innerHTML = `
            <p>Mean Squared Error: ${data.mse}</p>
            <p>R^2 Score: ${data.r2}</p>
        `;
    });
});