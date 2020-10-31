from flask import Blueprint, render_template, url_for, request
from application import db
from .models import Speeches 
import sys
import csv
import datetime

main_bp = Blueprint("main", __name__)

def _fill_db(data):
    for item in data:
        db.session.add(
            Speeches(
                name = item["name"],
                date_s = datetime.datetime.strptime(item["date"], "%Y-%m-%d"),
                speech = item["speech"],
                url = item["url"],
                len_s = item["len_s"],
                time_s = item["time_s"]
            )
        )
    db.session.commit()

def _read_csv():
    csv.field_size_limit(sys.maxsize)
    with open("all_speeches_20201024.csv") as file:
        csv_reader = csv.reader(file)
        speech_dict = {}
        speech_list = []
        flag = True
        for speech in csv_reader:
            if flag:
                flag = False
            else:
                speech_dict["name"] = speech[1]
                speech_dict["date"] = speech[2]
                speech_dict["speech"] = speech[3]
                speech_dict["url"] = speech[4]
                speech_dict["len_s"] = speech[5]
                speech_dict["time_s"] = speech[6]
                speech_list.append(speech_dict.copy())
    return speech_list


@main_bp.route("/", methods = ["GET"])
def index():
    presidents = Speeches.query.group_by(Speeches.name)
    return render_template("index.html", queries=presidents)


@main_bp.route("/<president>", methods=["GET"])
def analyze(president):
    if president == "all":
        try:
            all_predidents = Speeches.query.all()
        except:
            return "ERROR en la Consulta!"
        q = request.args.get("q")
        result = {}
        all_results = []
        total = 0
        for president in all_predidents:
            match = president.speech.count(q.lower())
            if match > 0:
                result["count"] = int(match)
                result["name"] = president.name
                result["url"] = president.url
                result["date"] = president.date_s.strftime("%b %d, %Y")
                total = total + match
                all_results.append(result.copy())

        temp = {}
        total_by_presi = [] 
        p_list = set([ item["name"] for item in all_results ]) 
        for i in p_list:
            temp["total"] = sum([ item["count"] for item in all_results if i == item["name"] ])
            temp["name"] = i
            total_by_presi.append(temp.copy())

        return render_template("analyze.html", all_results=all_results, total=total, word=q.lower(), total_by_presi=total_by_presi)
