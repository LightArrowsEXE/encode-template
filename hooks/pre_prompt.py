# TODO: Get this working so we can auto-fill git author and email

# import subprocess
# from cookiecutter.main import cookiecutter  # type:ignore[import]


# def get_git_config_value(key):
#     try:
#         value = subprocess.check_output(['git', 'config', '--get', key]).strip().decode('utf-8')
#         return value
#     except subprocess.CalledProcessError:
#         return None


# git_name = get_git_config_value('user.name')
# git_email = get_git_config_value('user.email')

# context = dict[str, str]()

# if git_name:
#     context['author'] = git_name

# if git_email:
#     context['email'] = git_email

# if context:
#     cookiecutter('encode-template', no_input=True, extra_context=context)
