from .tenant import db_state


class DBRouter:
    def db_for_read(self, model, **hints):
        account_db = db_state.get()
        # print(f'Database for read {account_db} {model}\n')
        return account_db

    def db_for_write(self, model, **hints):
        account_db = db_state.get()
        # print(f'Database for write {account_db} {model.__module__}\n')
        return account_db

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
