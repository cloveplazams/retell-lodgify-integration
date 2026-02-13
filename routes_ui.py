from flask import Blueprint, render_template, request, redirect, url_for
from models import Property
from database import db

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/')
def dashboard():
    properties = Property.query.all()
    return render_template('dashboard.html', properties=properties)

@ui_bp.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        name = request.form['name']
        lodgify_id = request.form['lodgify_id']
        capacity = int(request.form['capacity'])
        
        new_prop = Property(name=name, lodgify_id=lodgify_id, capacity=capacity)
        db.session.add(new_prop)
        db.session.commit()
        return redirect(url_for('ui.dashboard'))
    
    return render_template('add_property.html')

@ui_bp.route('/delete/<int:id>')
def delete_property(id):
    prop = Property.query.get_or_404(id)
    db.session.delete(prop)
    db.session.commit()
    return redirect(url_for('ui.dashboard'))
