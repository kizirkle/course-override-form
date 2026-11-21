from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import CourseReq
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        student_id = request.form.get('student_id')#Gets the note from the HTML 
        student_name = request.form.get('student_name')
        course_name = request.form.get('course_name')
        course_num = request.form.get('course_id')
        justification = request.form.get('justification')
        if len(justification) < 1 or len(student_id) < 1 or len(student_name) < 1 or len(course_name) < 1 or len(course_num) < 1:
            flash('All sections of the form must be filled out!', category='error') 
        else:
            new_coursereq = CourseReq(justification = justification, student_id = student_id, student_name = student_name,
                                      course_name = course_name, course_num = course_num, user_id = current_user.id)  #providing the schema for the note 
            db.session.add(new_coursereq) #adding the note to the database 
            db.session.commit()
            flash('Request submitted!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-request', methods=['POST'])
def delete_note():  
    coursereq = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    coursereq_id = coursereq['id']
    coursereq = CourseReq.query.get(coursereq_id)
    if coursereq:
        if coursereq.user_id == current_user.id:
            db.session.delete(coursereq)
            db.session.commit()

    return jsonify({})

