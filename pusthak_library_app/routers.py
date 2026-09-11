ADMIN_LABELS = {"user", "branch", "role",}
BRANCH_LABELS = {"book","inventory",}
CLIENT_LABELS = {"book_log",}

class DatabaseRouter:

    def db_for_read(self, model, **hints):

        if model._meta.app_label in BRANCH_LABELS:
            return "branch_db"

        if model._meta.app_label in CLIENT_LABELS:
            return "history_db"

        return None


    def db_for_write(self, model, **hints):

        if model._meta.app_label in BRANCH_LABELS:
            return "branch_db"

        if model._meta.app_label in CLIENT_LABELS:
            return "history_db"

        return None


    def allow_relation(self, obj1, obj2, **hints):

        db1 = obj1._state.db
        db2 = obj2._state.db

        if db1 and db2 and db1 == db2:
            return True

        return None


    def allow_migrate(
        self,
        db,
        app_label,
        model_name=None,
        **hints
    ):

        # DEFAULT DATABASE
       

        if db == "default":

            if app_label in ADMIN_LABELS:
                return True

            if app_label in BRANCH_LABELS:
                return False

            if app_label in CLIENT_LABELS:
                return False


        
        # BRANCH DATABASE

        elif db == "branch_db":

            if app_label in BRANCH_LABELS:
                return True

            if app_label in ADMIN_LABELS:
                return False

            if app_label in CLIENT_LABELS:
                return False


        # HISTORY DATABASE

        elif db == "history_db":

            if app_label in CLIENT_LABELS:
                return True

            if app_label in ADMIN_LABELS:
                return False

            if app_label in BRANCH_LABELS:
                return False


        return None