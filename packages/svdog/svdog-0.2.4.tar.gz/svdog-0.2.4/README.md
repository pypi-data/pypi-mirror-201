svdog
=====

supervisor's dog, should deploy with flylog

python2, python3 supported

example:

    [eventlistener:svdog]
    environment=PYTHON_EGG_CACHE=/tmp/.python-eggs/
    command=/usr/local/bin/run_svdog.py
    user=user_00
    events=PROCESS_STATE_EXITED,PROCESS_STATE_FATAL
    autorestart=true

注意:

    redirect_stderr=true should not be used with an eventlistener for any version of Supervisor.
    If redirect_stderr=true and any output is written to stderr, the message will be mixed with stdout and will violate the eventlistener protocol.
    If this happens, supervisord will stop sending events to the eventlistener.
    That is why redirect_stderr=true was disallowed starting in 3.2.0.
