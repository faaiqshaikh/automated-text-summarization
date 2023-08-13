from flask import Flask, render_template, request
from transformers import BartForConditionalGeneration, BartTokenizer

app = Flask(__name__)

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = request.form.get("input_text")
        summary = summarize_text(input_text)
        return render_template("index.html", summary=summary, input_text=input_text)
    return render_template("index.html")

def summarize_text(text):
    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(input_ids, max_length=100, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    app.run(debug=True)
