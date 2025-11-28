from flask import Flask,request,render_template,redirect,url_for
import os
import csv


app=Flask(__name__)

@app.route('/')
def index():
    tlist=tasks()
    return render_template("home.html",tlist=tlist)


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle_task(task_id):
    ta = tasks()
    for t in ta:
        if t["Id"] == task_id:
            t["Status"] = "1" if t["Status"] in ["0", "False", "false"] else "0"
            break
    save_tasks(ta)
    return redirect(url_for("index"))


def save_tasks(task_list):
    with open("task.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Id", "Description", "Status"])
        writer.writeheader()
        writer.writerows(task_list)


def tasks():
    tasks = []
    if not os.path.exists("task.csv"):
        with open("task.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Id", "Description", "Status"])
            writer.writeheader()
    with open("task.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return tasks



@app.route("/add", methods=["GET", "POST"])
def add():
    task_id = request.args.get("task_id")  
    ta = tasks()
    
    if request.method == "POST":
        desc = request.form.get("description").strip()  
        task_id_form = request.form.get("task_id")

        if task_id_form:  
            for t in ta:
                if t["Id"] == task_id_form:
                    t["Description"] = desc
                    break
        else:  
            new_id = str(max([int(t["Id"]) for t in ta], default=0) + 1)
            ta.append({"Id": new_id, "Description": desc, "Status": "0"})
        
        save_tasks(ta)
        return redirect(url_for("index"))
    
    
    task_desc = ""
    if task_id:
        for t in ta:
            if t["Id"] == task_id:
                task_desc = t["Description"]
                break
    
    return render_template("add.html", task_id=task_id, task_desc=task_desc)



@app.route("/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    ta = tasks()
    ta = [t for t in ta if t["Id"] != task_id]
    save_tasks(ta)
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)