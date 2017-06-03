from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)
projects = os.listdir('/afs/cern.ch/user/d/dbiswas/www/projects/')


@app.route('/')
def index():
    return render_template('index.html', projects=projects)


@app.route('/project/<name>')
def project(name):
    projectdir = os.path.join('/afs/cern.ch/user/d/dbiswas/www/projects/', name)
    if os.path.exists(projectdir):
        projectinfo = {'name': name, 'folders': []}
        for d in os.listdir(projectdir):
            if os.path.isdir(os.path.join(projectdir, d)):
                folder_dict = {'name': d, 'images': []}
                projectinfo['folders'].append(folder_dict)
                for f in os.listdir(os.path.join(projectdir, d)):
                    if f.endswith('.png') or f.endswith('jpg'):
                        img_dict = {'path': os.path.join('https://dbiswas.web.cern.ch/dbiswas/projects/', name, d, f),
                                    'title': f[0:-4]}
                        if os.path.exists(os.path.join(projectdir, d, f + ".info")):
                            info = open(os.path.join(projectdir, d, f + ".info")).read().split('\n', 2)
                            img_dict['title'] = info[0]
                            if (len(info) > 1):
                                img_dict['des'] = info[1]
                        folder_dict['images'].append(img_dict)
        return render_template('project.html', projects=projects, projectinfo=projectinfo)
    else:
        abort(404)
