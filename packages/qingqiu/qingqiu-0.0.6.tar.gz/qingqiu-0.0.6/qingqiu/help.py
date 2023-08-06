
def help_vscode_config():
    vscodeConfig = '''
    {
"python.testing.pytestArgs": [

    "-s",
    "-q",
    "--log-cli-level=info",
    "--html=report.html",
    "--self-contained-html",
    "--capture=sys",
    "--reruns=1",
    "--reruns-delay=1",
    
],
"python.testing.unittestEnabled": false,
"python.testing.pytestEnabled": true
}
'''
    print(vscodeConfig)

def help_pytest_cmd():

    cmd='''
    pytest --rootdir .  -s -q --log-cli-level=INFO --html=report.html --self-contained-html --capture=sys --reruns=1 --reruns-delay=1 ${{runfile}}
    '''
    print(cmd)