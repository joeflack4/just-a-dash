from flask.ext.login import current_user
from flask.ext.restless import ProcessingException

# - Note: If IDE shows weak warning '**kwargs unused', that is technically untrue. Calling function will use.


class ApiAuth:
    @classmethod
    def logged_in(cls, **kwargs):
        user_logged_in = False
        if not current_user.is_authenticated():
            raise ProcessingException(description='Not Authorized. Please log in first.', code=401)
        elif current_user.is_authenticated():
            user_logged_in = True
        return user_logged_in

    @classmethod
    def basic_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.admin_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic administrative permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.admin_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super administrative permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.admin_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master administrative permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def basic_oms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.oms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic OMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_oms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.oms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super OMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_oms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.oms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master OMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def basic_crm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.crm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic CRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_crm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.crm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super CRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_crm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.crm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master CRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def basic_hrm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.hrm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic HRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_hrm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.hrm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super HRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_hrm_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.hrm_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master HRM admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def basic_ams_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.ams_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic AMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_ams_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.ams_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super AMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_ams_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.ams_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master AMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def basic_mms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('basic', 'super', 'master')
        if user_logged_in:
            if current_user.mms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Basic MMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def super_mms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('super', 'master')
        if user_logged_in:
            if current_user.mms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Super MMS admin permissions or higher '
                                                      'required.', code=401)

    @classmethod
    def master_mms_admin(cls, **kwargs):
        user_logged_in = cls.logged_in()
        allowable_roles = ('master')
        if user_logged_in:
            if current_user.mms_role not in allowable_roles:
                raise ProcessingException(description='Not Authorized. Master MMS admin permissions or higher '
                                                      'required.', code=401)

    def __init__(self):
        self.description = 'API Authorization Object'

    def __repr__(self):
        return 'API Authorization Object'
