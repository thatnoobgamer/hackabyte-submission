# Import packages

from flask import Flask, render_template, request
import markdown
import openai

def airesponse(injury, severity):   
        f = open("apikey",'r')
        openai.api_key = f.read()
        aicontent = "help! theres a person who is currently/has a" + str(injury) + ". the severity of the injury is " + str(severity) + ".please tell me what to do in a numbered list. please include what to do until help arrives and what to do for any possible injury based on any information provided." 
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "please say what an emt would say. don't say that you are an emt. format your response as: for a <insert severity> <insert injury> do this. also, provide a answer based on injury alone. do not ask for more information. use simple english."},
                {"role": "system", "content": "use english characters and numbers. do not use emojis or other special characters."},
                {"role": "system", "content": "absolutely zero markdown."},
                {"role": "system", "content": "look through places like webmd to find things for the user to help."},
                {"role": "user", "content":   aicontent}
                ],
            max_tokens=1000,
        )
        f.close()
        return response

app = Flask(__name__)

# Homepage router

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/directions', methods=['POST'])
def directions():
    injury = request.form['injury']
    severity = request.form['severity']
    response = airesponse(injury, severity)
    return render_template('directions.html', response=markdown.markdown(response.choices[0].message.content))

if __name__ == '__main__':
    app.run(debug=True)