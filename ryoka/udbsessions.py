import os
from flask import current_app, _app_ctx_stack as stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UdbSessions:
    def init_app(self, app):
        app.config.setdefault('UDBSESSIONS_DB_PATH', ':memory:')
        app.teardown_appcontext(self.teardown)
    
    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'udb_sessions'):
            ctx.udb_sessions.teardown()

    def __getitem__(self, index):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'udb_sessions'):
                ctx.udb_sessions = UdbSessionsImpl()
            return ctx.udb_sessions[index]
        return None


class UdbSessionsImpl:
    def __init__(self):
        self.sessions = {}

    def __getitem__(self, index):
        if index not in self.sessions:
            self.new_session(index)
        return self.sessions[index]

    def new_session(self, index):
        print('!!! ---- New session!')
        path = 'sqlite:///%s' % os.path.join(current_app.config['UDBSESSIONS_DB_PATH'], str(index) + '.sqlite')
        engine = create_engine(path, echo=True)
        Session =  sessionmaker(bind=engine)
        self.sessions[index] = Session()

    def teardown(self):
        print('!!! ---- Tear down appcontex!')
        for session in self.sessions.values():
            session.close()
        del self.sessions
