"""Task routes."""

from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash,
    request,
    jsonify
)

from app import db
from app.models import Tasks


tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    tasks = Tasks.query.all()

    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_tasks():
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first.'
        }), 401

    title = request.form.get('title', '').strip()

    if not title:
        return jsonify({
            'success': False,
            'message': 'Task title cannot be empty.'
        }), 400

    new_task = Tasks(
        title=title,
        status='Pending'
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task added successfully!',
        'task': {
            'id': new_task.id,
            'title': new_task.title,
            'status': new_task.status
        }
    })


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):

    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first.'
        }), 401

    task = Tasks.query.get(task_id)

    if not task:
        return jsonify({
            'success': False,
            'message': 'Task not found!'
        }), 404

    if task.status == 'Pending':
        task.status = 'working'

    elif task.status == 'working':
        task.status = 'done'

    else:
        task.status = 'Pending'

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task status updated!',
        'task': {
            'id': task.id,
            'title': task.title,
            'status': task.status
        }
    })


@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():

    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first.'
        }), 401

    Tasks.query.delete()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'All tasks cleared!'
    })


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):

    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first.'
        }), 401

    task = Tasks.query.get(task_id)

    if not task:
        return jsonify({
            'success': False,
            'message': 'Task not found!'
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task deleted successfully!',
        'task_id': task_id
    })