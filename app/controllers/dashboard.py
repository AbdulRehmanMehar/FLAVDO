import os
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, Markup
from flask_login import current_user
from ..models import User, Video, app, db
from ..forms import VideoUploadForm, VideoForm

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def restrict():
    if(not current_user.is_authenticated):
        return abort(401)
    if(not current_user.verified):
        flash('Please verify your email. '+ Markup('<a class="alert-link" href="'+ url_for('auth.send_token', uname=current_user.username) +'">Resend Verification Token?</a>'), 'info')
    if(current_user.photo == None):
        flash(Markup('<a href="'+ url_for('auth.upload_photo') +'">Add a photo?</a>') + ' So others may recognize your channel.', 'info')

@dashboard.route('/')
def home():
    user = User.query.get(current_user.get_id()) 
    videos = Video.query.with_parent(user).limit(6).all()
    
    return render_template('dashboard.html', videos=videos)

@dashboard.route('/upload-video', methods=['GET', 'POST'])
def upload_video():
    form = VideoForm(request.form)
    vform = VideoUploadForm(request.files)
    if request.method == 'POST' and form.validate() and vform.validate():
        vfile = request.files[vform.video.name]
        vfname = form.title.data.replace(' ', '_') + '_by_' + current_user.username + '.' + vform.ext
        print(vfname)
        video = Video(form.title.data, form.description.data, vfname, current_user.get_id())
        vfile.save(os.path.join(app.config['UPLOADS_FOLDER'] + '/videos', vfname))
        db.session.add(video)
        db.session.commit()
        flash('Video has been uploaded.', 'success')
        redir = request.args.get('next') or request.referrer or url_for('auth.login')
        return redirect(redir)
    return render_template('upload-video.html', form=form, vform=vform)

@dashboard.route('/remove-video/<id>')
def remove_video(id):
    video = Video.query.filter(Video.id == id and Video.owner_id == current_user.get_id()).first()
    if video != None:
        db.session.delete(video)
        db.session.commit()
        flash('Video has been removed successfully.', 'success')
    else: 
        flash('Sorry, Something went wrong.', 'danger')
    redir = request.args.get('next') or request.referrer or url_for('auth.login')
    return redirect(redir)
