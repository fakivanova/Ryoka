import os
from flask import current_app, g, _app_ctx_stack as stack
from flask_login import current_user
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

class UdbSessions:
    def __init__(self):
        self._history_handler = None

    def init_app(self, app):
        app.udb_session = self
        app.config.setdefault('UDBSESSIONS_DB_PATH', ':memory:')
        app.teardown_appcontext(self.teardown)
    
    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'udb_sessions'):
            ctx.udb_sessions.teardown()

    def history_handler(self, handler):
        self._history_handler = handler
        return handler

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

    def new_engine(self, index):
        path = 'sqlite:///%s' % os.path.join(current_app.config['UDBSESSIONS_DB_PATH'], str(index) + '.sqlite')
        engine = create_engine(path, echo=False)
        event.listen(engine, 'after_cursor_execute', after_cursor_execute)
        return engine

    def new_session(self, index):
        print('!!! ---- New session!')
        engine = self.new_engine(index)
        Session =  sessionmaker(bind=engine)
        self.sessions[index] = Session()

    def teardown(self):
        print('!!! ---- Tear down appcontex!')
        for session in self.sessions.values():
            session.close()
            #event.remove(session.get_bind(), 'after_cursor_execute', after_cursor_execute)
        del self.sessions

def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not current_app:
        return
    handler = current_app.udb_session._history_handler
    if handler:
        handler(statement + str(parameters))
    print('!!!!!', statement, parameters)
