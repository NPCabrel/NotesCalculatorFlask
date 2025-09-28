import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

# funtion to calculate mean
def calculate_mean():
    try:
        # read the CSV file
        df = pd.read_csv('notesCalculator.csv')
        
        # rename columns for easier access
        df = df.rename(columns={'students': 'name', 'machine Learning': 'machine_learning'})
        
        # calculate mean for each student
        df['Mean'] = df[['maths', 'physics', 'programming', 'ai', 'machine_learning']].mean(axis=1)
        
        # general mean
        general_mean = df['Mean'].mean()
        
        return df.to_dict('records'), general_mean
    except Exception as e:
        return [], f"Erreur : {str(e)}"

# route to display results  for the web page
@app.route('/')
def index():
    students, general_mean = calculate_mean()
    if isinstance(general_mean, str):  # if there's an error message
        return f"<h1>Erreur</h1><p>{general_mean}</p>"
    
    html = '''
    <html>
        <head>
            <title>Students Notes</title>
        </head>
        <body>
            <h1>Students Notes</h1>
            <table border="1">
                <tr>
                    <th>Name</th>
                    <th>Maths</th>
                    <th>Physics</th>
                    <th>Programming</th>
                    <th>AI</th>
                    <th>Machine Learning</th>
                    <th>Mean</th>
                </tr>
                {% for student in students %}
                <tr>
                    <td>{{ student['name'] }}</td>
                    <td>{{ student['maths'] }}</td>
                    <td>{{ student['physics'] }}</td>
                    <td>{{ student['programming'] }}</td>
                    <td>{{ student['ai'] }}</td>
                    <td>{{ student['machine_learning'] }}</td>
                    <td>{{ student['Mean'] }}</td>
                </tr>
                {% endfor %}
            </table>
            <h2>General Mean: {{ general_mean }}</h2>
        </body>
    </html>
    '''
    return render_template_string(html, students=students, general_mean=general_mean)

if __name__ == '__main__':
    app.run(debug=True)
