from fabric.api import lcd, local

def prepare_deployment(master):
    local('python manage.py test tki')
    local('git add -p && git commit') # or local('hg add && hg commit')


def deploy():
    with lcd('/path/to/my/prod/area/'):

        # With git...
        local('git pull /my/path/to/dev/area/')


        # With both
        local('python manage.py migrate taekwondo')
        local('python manage.py test taekwondo')
        local('python manage.py runserver')