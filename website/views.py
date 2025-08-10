from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, Note


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note_data = request.form.get('note')
        if not note_data or note_data.strip() == '':
            flash("Can't save an empty note!", category='error')
        else:
            new_note = Note(data=note_data.strip(), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note saved! You’re crushing it!", category='success')
        return redirect(url_for('views.notes'))

    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_created.desc()).all()
    return render_template('notes.html', notes=user_notes)
@views.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You can't delete this note, That’s not yours.", category='error')
        return redirect(url_for('views.notes'))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted. Clean slate!", category='success')
    return redirect(url_for('views.notes'))