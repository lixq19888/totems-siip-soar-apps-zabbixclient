import os
from SoarAction import SoarAction
from SoarUtils import output_handler
from pyzabbix import ZabbixAPI
import SoarDataModel

LogFile = "zabbixclient.log"
APP_NAME = "ZabbixClient"
ACTION_LIST = ["GET_ALL_HOST","GET_CURRENT_ISSUES"]

class ZabbixClientApp(SoarAction):

    def __init__(self, app_name, action_list, input_data, action_select):
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LogFile)
        super(ZabbixClientApp, self).__init__(app_name, log_path, action_list, input_data, action_select)

    @output_handler
    def GET_ALL_HOST(self):
        try:
            url = self.setting_param_dict["url"]
            user = self.setting_param_dict["user"]
            password = self.setting_param_dict["password"]
            zapi = ZabbixAPI(url)
            zapi.login(user, password)
            self.logger.info("Connected to Zabbix API Version {}".format(zapi.api_version()))
            allhost = zapi.host.get(output="extend")
            return self.get_response_json(allhost)
        except Exception as e:
            errmsg = '获取zabbix主机失败：' + str(e)
            self.logger.warn(errmsg)
            return self.get_error_response(errmsg)

    @output_handler
    def GET_CURRENT_ISSUES(self):
        try:
            url = self.setting_param_dict["url"]
            user = self.setting_param_dict["user"]
            password = self.setting_param_dict["password"]
            zapi = ZabbixAPI(url)
            zapi.login(user, password)
            # 获取所有问题
            triggers = zapi.trigger.get(only_true=1,
                                        skipDependent=1,
                                        monitored=1,
                                        active=1,
                                        output='extend',
                                        expandDescription=1,
                                        selectHosts=['host'],
                                        )
            # 获取未确认问题
            unack_triggers = zapi.trigger.get(only_true=1,
                                              skipDependent=1,
                                              monitored=1,
                                              active=1,
                                              output='extend',
                                              expandDescription=1,
                                              selectHosts=['host'],
                                              withLastEventUnacknowledged=1,
                                              )
            # 未确认问题id
            unack_trigger_ids = [t['triggerid'] for t in unack_triggers]

            for t in triggers:
                t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
                    else False
            return self.get_response_json(triggers)
        except Exception as e:
            errmsg = '获取zabbix主机问题失败：' + str(e)
            self.logger.warn(errmsg)
            return self.get_error_response(errmsg)


    @output_handler
    def PING(self):
        try:
            url = self.setting_param_dict["url"]
            user = self.setting_param_dict["user"]
            password = self.setting_param_dict["password"]
            zapi = ZabbixAPI(url)
            zapi.login(user, password)
            return self.get_response_json(SoarDataModel.ResultStatusEnum.SUCCESS_STATUS)
        except Exception as e:
            self.logger.error(repr(e))
            return self.get_error_response(SoarDataModel.ResultStatusEnum.FAIL_STATUS)

if __name__ == '__main__':
    input_data = None
    action_name = None
    # input_data = r"eyJsYW5ndWFnZVR5cGUiOiJQWVRIT04zIiwicGxheUJvb2tWZXJzaW9uIjoiMS4wLjAiLCJhcHBJZCI6ImZlZDVmNjRmNmNlYjRmMzA5ZGZmYmY3MWJjZDRkYTU5IiwiYXBwTmFtZSI6IlphYmJpeENsaWVudCIsImFwcEFsaWFzIjoiWmFiYml45a6i5oi356uvIiwiYXBwVmVyc2lvbiI6IjEuMC4wIiwiYnJpZWYiOiLkuIDkuKrnlLFweXRob27or63oqIDnvJblhpnnmoR6YWJiaXjov57mjqXlt6XlhbfvvIznlKjmnaXorr/pl656YWJiaXggYXBpIiwiZGVzY3JpcHRpb24iOiJ6YWJiaXjov57mjqXlt6XlhbfvvIznlKjmnaXorr/pl656YWJiaXggYXBpIiwidGFncyI6WyJ6YWJiaXgiXSwiY2F0ZWdvcmllcyI6eyJuYW1lIjoi5pyN5Yqh5Zmo55uR5o6nIiwicGFyZW50Ijoi6buY6K6k5YiG57G7In0sImNvbnRhY3RJbmZvIjp7Im5hbWUiOiJBQlQg5a6J5Y2a6YCaIiwidXJsIjoiaHR0cDovL3d3dy5hYnRuZXR3b3Jrcy5jb20vd2VsY29tZS5odG1sIiwiZW1haWwiOiJYWFhAc2FwbGluZy5jb20uY24iLCJwaG9uZSI6IlhYWFhYIiwiZGVzY3JpcHRpb24iOiJYWFhYWFhYWFhYWFgifSwibGljZW5zZUluZm8iOnsibmFtZSI6IuaOiOadg+S/oeaBryIsInVybCI6Imh0dHBzOi8vWFhYWFgvTElDRU5TRS5tZCJ9LCJpbnN0YW5jZUVuYWJsZWQiOnRydWUsInNldHRpbmciOnsicGFyYW1ldGVycyI6W3sibmFtZSI6InVybCIsInZhbHVlIjoiaHR0cDovLzE5Mi4xNjguMjE1LjE3NDo4MDgwLyIsImV4YW1wbGUiOiJodHRwOi8vMTkyLjE2OC4yMTUuMTc0OjEwMDg2IiwiZGVzY3JpcHRpb24iOiJ6YWJiaXjmnI3liqHlmajlnLDlnYAiLCJzY2hlbWEiOnsidHlwZSI6IlNUUklORyJ9LCJ1aSI6eyJ1aU5hbWUiOiJ6YWJiaXjmnI3liqHlmajlnLDlnYAiLCJ0eXBlIjoidGV4dGFyZWEifSwicmVxdWlyZWQiOnRydWV9LHsibmFtZSI6InVzZXIiLCJ2YWx1ZSI6IkFkbWluIiwiZXhhbXBsZSI6IkFkbWluIiwiZGVzY3JpcHRpb24iOiJ6YWJiaXjnmbvlvZXnlKjmiLflkI0iLCJzY2hlbWEiOnsidHlwZSI6IlNUUklORyJ9LCJ1aSI6eyJ1aU5hbWUiOiJ6YWJiaXjnmbvlvZXnlKjmiLflkI0iLCJ0eXBlIjoidGV4dGFyZWEifSwicmVxdWlyZWQiOnRydWV9LHsibmFtZSI6InBhc3N3b3JkIiwidmFsdWUiOiJ6YWJiaXgiLCJleGFtcGxlIjoiemFiYml4IiwiZGVzY3JpcHRpb24iOiJ6YWJiaXjnmbvlvZXlr4bnoIEiLCJzY2hlbWEiOnsidHlwZSI6IlNUUklORyJ9LCJ1aSI6eyJ1aU5hbWUiOiJ6YWJiaXjnmbvlvZXlr4bnoIEiLCJ0eXBlIjoidGV4dGFyZWEifSwicmVxdWlyZWQiOnRydWV9XX0sImFjdGlvbnMiOlt7Im5hbWUiOiJHRVRfQUxMX0hPU1QiLCJhbGlhcyI6IuiOt+WPluaJgOacieS4u+acuiIsImRlc2NyaXB0aW9uIjoi6I635Y+WemFiYml45omA5pyJ55uR5o6n5Li75py6IiwicGFyYW1ldGVycyI6W3sibmFtZSI6Imhvc3RfaXAiLCJ2YWx1ZSI6IiIsImV4YW1wbGUiOiIxMC4yMTUuNy4xNyIsImRlc2NyaXB0aW9uIjoi5Li75py6aXAiLCJzY2hlbWEiOnsidHlwZSI6IlNUUklORyJ9LCJ1aSI6eyJ1aU5hbWUiOiLkuLvmnLppcCIsInR5cGUiOiJ0ZXh0YXJlYSJ9LCJyZXF1aXJlZCI6dHJ1ZX1dLCJyZXR1cm5zIjp7InNjaGVtYSI6eyJ0eXBlIjoiSlNPTl9BUlJBWSJ9LCJleGFtcGxlIjoiW3tcImhvc3RpZFwiOiBcIjEwMDg0XCIsIFwicHJveHlfaG9zdGlkXCI6IFwiMFwiLCBcImhvc3RcIjogXCJaYWJiaXggc2VydmVyXCIsIFwic3RhdHVzXCI6IFwiMFwiLCBcImRpc2FibGVfdW50aWxcIjogXCIwXCIsIFwiZXJyb3JcIjogXCJcIiwgXCJhdmFpbGFibGVcIjogXCIxXCIsIFwiZXJyb3JzX2Zyb21cIjogXCIwXCIsIFwibGFzdGFjY2Vzc1wiOiBcIjBcIiwgXCJpcG1pX2F1dGh0eXBlXCI6IFwiLTFcIiwgXCJpcG1pX3ByaXZpbGVnZVwiOiBcIjJcIiwgXCJpcG1pX3VzZXJuYW1lXCI6IFwiXCIsIFwiaXBtaV9wYXNzd29yZFwiOiBcIlwiLCBcImlwbWlfZGlzYWJsZV91bnRpbFwiOiBcIjBcIiwgXCJpcG1pX2F2YWlsYWJsZVwiOiBcIjBcIiwgXCJzbm1wX2Rpc2FibGVfdW50aWxcIjogXCIwXCIsIFwic25tcF9hdmFpbGFibGVcIjogXCIwXCIsIFwibWFpbnRlbmFuY2VpZFwiOiBcIjBcIiwgXCJtYWludGVuYW5jZV9zdGF0dXNcIjogXCIwXCIsIFwibWFpbnRlbmFuY2VfdHlwZVwiOiBcIjBcIiwgXCJtYWludGVuYW5jZV9mcm9tXCI6IFwiMFwiLCBcImlwbWlfZXJyb3JzX2Zyb21cIjogXCIwXCIsIFwic25tcF9lcnJvcnNfZnJvbVwiOiBcIjBcIiwgXCJpcG1pX2Vycm9yXCI6IFwiXCIsIFwic25tcF9lcnJvclwiOiBcIlwiLCBcImpteF9kaXNhYmxlX3VudGlsXCI6IFwiMFwiLCBcImpteF9hdmFpbGFibGVcIjogXCIwXCIsIFwiam14X2Vycm9yc19mcm9tXCI6IFwiMFwiLCBcImpteF9lcnJvclwiOiBcIlwiLCBcIm5hbWVcIjogXCJaYWJiaXggc2VydmVyXCIsIFwiZmxhZ3NcIjogXCIwXCIsIFwidGVtcGxhdGVpZFwiOiBcIjBcIiwgXCJkZXNjcmlwdGlvblwiOiBcIlwiLCBcInRsc19jb25uZWN0XCI6IFwiMVwiLCBcInRsc19hY2NlcHRcIjogXCIxXCIsIFwidGxzX2lzc3VlclwiOiBcIlwiLCBcInRsc19zdWJqZWN0XCI6IFwiXCIsIFwidGxzX3Bza19pZGVudGl0eVwiOiBcIlwiLCBcInRsc19wc2tcIjogXCJcIiwgXCJwcm94eV9hZGRyZXNzXCI6IFwiXCIsIFwiYXV0b19jb21wcmVzc1wiOiBcIjFcIiwgXCJpbnZlbnRvcnlfbW9kZVwiOiBcIi0xXCJ9LCB7XCJob3N0aWRcIjogXCIxMDQzMlwiLCBcInByb3h5X2hvc3RpZFwiOiBcIjBcIiwgXCJob3N0XCI6IFwiYWdlbnQxMC4yMTUuNy4xN1wiLCBcInN0YXR1c1wiOiBcIjBcIiwgXCJkaXNhYmxlX3VudGlsXCI6IFwiMFwiLCBcImVycm9yXCI6IFwiXCIsIFwiYXZhaWxhYmxlXCI6IFwiMVwiLCBcImVycm9yc19mcm9tXCI6IFwiMFwiLCBcImxhc3RhY2Nlc3NcIjogXCIwXCIsIFwiaXBtaV9hdXRodHlwZVwiOiBcIi0xXCIsIFwiaXBtaV9wcml2aWxlZ2VcIjogXCIyXCIsIFwiaXBtaV91c2VybmFtZVwiOiBcIlwiLCBcImlwbWlfcGFzc3dvcmRcIjogXCJcIiwgXCJpcG1pX2Rpc2FibGVfdW50aWxcIjogXCIwXCIsIFwiaXBtaV9hdmFpbGFibGVcIjogXCIwXCIsIFwic25tcF9kaXNhYmxlX3VudGlsXCI6IFwiMFwiLCBcInNubXBfYXZhaWxhYmxlXCI6IFwiMFwiLCBcIm1haW50ZW5hbmNlaWRcIjogXCIwXCIsIFwibWFpbnRlbmFuY2Vfc3RhdHVzXCI6IFwiMFwiLCBcIm1haW50ZW5hbmNlX3R5cGVcIjogXCIwXCIsIFwibWFpbnRlbmFuY2VfZnJvbVwiOiBcIjBcIiwgXCJpcG1pX2Vycm9yc19mcm9tXCI6IFwiMFwiLCBcInNubXBfZXJyb3JzX2Zyb21cIjogXCIwXCIsIFwiaXBtaV9lcnJvclwiOiBcIlwiLCBcInNubXBfZXJyb3JcIjogXCJcIiwgXCJqbXhfZGlzYWJsZV91bnRpbFwiOiBcIjBcIiwgXCJqbXhfYXZhaWxhYmxlXCI6IFwiMFwiLCBcImpteF9lcnJvcnNfZnJvbVwiOiBcIjBcIiwgXCJqbXhfZXJyb3JcIjogXCJcIiwgXCJuYW1lXCI6IFwiYWdlbnQxMC4yMTUuNy4xN1wiLCBcImZsYWdzXCI6IFwiMFwiLCBcInRlbXBsYXRlaWRcIjogXCIwXCIsIFwiZGVzY3JpcHRpb25cIjogXCJcIiwgXCJ0bHNfY29ubmVjdFwiOiBcIjFcIiwgXCJ0bHNfYWNjZXB0XCI6IFwiMVwiLCBcInRsc19pc3N1ZXJcIjogXCJcIiwgXCJ0bHNfc3ViamVjdFwiOiBcIlwiLCBcInRsc19wc2tfaWRlbnRpdHlcIjogXCJcIiwgXCJ0bHNfcHNrXCI6IFwiXCIsIFwicHJveHlfYWRkcmVzc1wiOiBcIlwiLCBcImF1dG9fY29tcHJlc3NcIjogXCIxXCIsIFwiaW52ZW50b3J5X21vZGVcIjogXCItMVwifSwge1wiaG9zdGlkXCI6IFwiMTA0MzNcIiwgXCJwcm94eV9ob3N0aWRcIjogXCIwXCIsIFwiaG9zdFwiOiBcImFnZW50MTkyLjE2OC4yMTguMTE1XCIsIFwic3RhdHVzXCI6IFwiMFwiLCBcImRpc2FibGVfdW50aWxcIjogXCIxNjQwODUzOTA3XCIsIFwiZXJyb3JcIjogXCJHZXQgdmFsdWUgZnJvbSBhZ2VudCBmYWlsZWQ6IGNhbm5vdCBjb25uZWN0IHRvIFtbMTkyLjE2OC4yMTguMTE1XToxMDA1MF06IFsxMTFdIENvbm5lY3Rpb24gcmVmdXNlZFwiLCBcImF2YWlsYWJsZVwiOiBcIjJcIiwgXCJlcnJvcnNfZnJvbVwiOiBcIjE2Mzk3Mzc5NzZcIiwgXCJsYXN0YWNjZXNzXCI6IFwiMFwiLCBcImlwbWlfYXV0aHR5cGVcIjogXCItMVwiLCBcImlwbWlfcHJpdmlsZWdlXCI6IFwiMlwiLCBcImlwbWlfdXNlcm5hbWVcIjogXCJcIiwgXCJpcG1pX3Bhc3N3b3JkXCI6IFwiXCIsIFwiaXBtaV9kaXNhYmxlX3VudGlsXCI6IFwiMFwiLCBcImlwbWlfYXZhaWxhYmxlXCI6IFwiMFwiLCBcInNubXBfZGlzYWJsZV91bnRpbFwiOiBcIjBcIiwgXCJzbm1wX2F2YWlsYWJsZVwiOiBcIjBcIiwgXCJtYWludGVuYW5jZWlkXCI6IFwiMFwiLCBcIm1haW50ZW5hbmNlX3N0YXR1c1wiOiBcIjBcIiwgXCJtYWludGVuYW5jZV90eXBlXCI6IFwiMFwiLCBcIm1haW50ZW5hbmNlX2Zyb21cIjogXCIwXCIsIFwiaXBtaV9lcnJvcnNfZnJvbVwiOiBcIjBcIiwgXCJzbm1wX2Vycm9yc19mcm9tXCI6IFwiMFwiLCBcImlwbWlfZXJyb3JcIjogXCJcIiwgXCJzbm1wX2Vycm9yXCI6IFwiXCIsIFwiam14X2Rpc2FibGVfdW50aWxcIjogXCIwXCIsIFwiam14X2F2YWlsYWJsZVwiOiBcIjBcIiwgXCJqbXhfZXJyb3JzX2Zyb21cIjogXCIwXCIsIFwiam14X2Vycm9yXCI6IFwiXCIsIFwibmFtZVwiOiBcImFnZW50MTkyLjE2OC4yMTguMTE1XCIsIFwiZmxhZ3NcIjogXCIwXCIsIFwidGVtcGxhdGVpZFwiOiBcIjBcIiwgXCJkZXNjcmlwdGlvblwiOiBcIlwiLCBcInRsc19jb25uZWN0XCI6IFwiMVwiLCBcInRsc19hY2NlcHRcIjogXCIxXCIsIFwidGxzX2lzc3VlclwiOiBcIlwiLCBcInRsc19zdWJqZWN0XCI6IFwiXCIsIFwidGxzX3Bza19pZGVudGl0eVwiOiBcIlwiLCBcInRsc19wc2tcIjogXCJcIiwgXCJwcm94eV9hZGRyZXNzXCI6IFwiXCIsIFwiYXV0b19jb21wcmVzc1wiOiBcIjFcIiwgXCJpbnZlbnRvcnlfbW9kZVwiOiBcIi0xXCJ9XSIsInVpRXhhbXBsZSI6eyJhcHBzQWN0aW9uUmVzcG9uc2UiOnsic3RhdHVzIjoiU3VjY2VzcyIsInNjaGVtYSI6eyJ0eXBlIjoiSlNPTl9BUlJBWSJ9LCJkYXRhIjpbeyJob3N0aWQiOiIxMDA4NCIsInByb3h5X2hvc3RpZCI6IjAiLCJob3N0IjoiWmFiYml4IHNlcnZlciIsInN0YXR1cyI6IjAiLCJkaXNhYmxlX3VudGlsIjoiMCIsImVycm9yIjoiIiwiYXZhaWxhYmxlIjoiMSIsImVycm9yc19mcm9tIjoiMCIsImxhc3RhY2Nlc3MiOiIwIiwiaXBtaV9hdXRodHlwZSI6Ii0xIiwiaXBtaV9wcml2aWxlZ2UiOiIyIiwiaXBtaV91c2VybmFtZSI6IiIsImlwbWlfcGFzc3dvcmQiOiIiLCJpcG1pX2Rpc2FibGVfdW50aWwiOiIwIiwiaXBtaV9hdmFpbGFibGUiOiIwIiwic25tcF9kaXNhYmxlX3VudGlsIjoiMCIsInNubXBfYXZhaWxhYmxlIjoiMCIsIm1haW50ZW5hbmNlaWQiOiIwIiwibWFpbnRlbmFuY2Vfc3RhdHVzIjoiMCIsIm1haW50ZW5hbmNlX3R5cGUiOiIwIiwibWFpbnRlbmFuY2VfZnJvbSI6IjAiLCJpcG1pX2Vycm9yc19mcm9tIjoiMCIsInNubXBfZXJyb3JzX2Zyb20iOiIwIiwiaXBtaV9lcnJvciI6IiIsInNubXBfZXJyb3IiOiIiLCJqbXhfZGlzYWJsZV91bnRpbCI6IjAiLCJqbXhfYXZhaWxhYmxlIjoiMCIsImpteF9lcnJvcnNfZnJvbSI6IjAiLCJqbXhfZXJyb3IiOiIiLCJuYW1lIjoiWmFiYml4IHNlcnZlciIsImZsYWdzIjoiMCIsInRlbXBsYXRlaWQiOiIwIiwiZGVzY3JpcHRpb24iOiIiLCJ0bHNfY29ubmVjdCI6IjEiLCJ0bHNfYWNjZXB0IjoiMSIsInRsc19pc3N1ZXIiOiIiLCJ0bHNfc3ViamVjdCI6IiIsInRsc19wc2tfaWRlbnRpdHkiOiIiLCJ0bHNfcHNrIjoiIiwicHJveHlfYWRkcmVzcyI6IiIsImF1dG9fY29tcHJlc3MiOiIxIiwiaW52ZW50b3J5X21vZGUiOiItMSJ9LHsiaG9zdGlkIjoiMTA0MzIiLCJwcm94eV9ob3N0aWQiOiIwIiwiaG9zdCI6ImFnZW50MTAuMjE1LjcuMTciLCJzdGF0dXMiOiIwIiwiZGlzYWJsZV91bnRpbCI6IjAiLCJlcnJvciI6IiIsImF2YWlsYWJsZSI6IjEiLCJlcnJvcnNfZnJvbSI6IjAiLCJsYXN0YWNjZXNzIjoiMCIsImlwbWlfYXV0aHR5cGUiOiItMSIsImlwbWlfcHJpdmlsZWdlIjoiMiIsImlwbWlfdXNlcm5hbWUiOiIiLCJpcG1pX3Bhc3N3b3JkIjoiIiwiaXBtaV9kaXNhYmxlX3VudGlsIjoiMCIsImlwbWlfYXZhaWxhYmxlIjoiMCIsInNubXBfZGlzYWJsZV91bnRpbCI6IjAiLCJzbm1wX2F2YWlsYWJsZSI6IjAiLCJtYWludGVuYW5jZWlkIjoiMCIsIm1haW50ZW5hbmNlX3N0YXR1cyI6IjAiLCJtYWludGVuYW5jZV90eXBlIjoiMCIsIm1haW50ZW5hbmNlX2Zyb20iOiIwIiwiaXBtaV9lcnJvcnNfZnJvbSI6IjAiLCJzbm1wX2Vycm9yc19mcm9tIjoiMCIsImlwbWlfZXJyb3IiOiIiLCJzbm1wX2Vycm9yIjoiIiwiam14X2Rpc2FibGVfdW50aWwiOiIwIiwiam14X2F2YWlsYWJsZSI6IjAiLCJqbXhfZXJyb3JzX2Zyb20iOiIwIiwiam14X2Vycm9yIjoiIiwibmFtZSI6ImFnZW50MTAuMjE1LjcuMTciLCJmbGFncyI6IjAiLCJ0ZW1wbGF0ZWlkIjoiMCIsImRlc2NyaXB0aW9uIjoiIiwidGxzX2Nvbm5lY3QiOiIxIiwidGxzX2FjY2VwdCI6IjEiLCJ0bHNfaXNzdWVyIjoiIiwidGxzX3N1YmplY3QiOiIiLCJ0bHNfcHNrX2lkZW50aXR5IjoiIiwidGxzX3BzayI6IiIsInByb3h5X2FkZHJlc3MiOiIiLCJhdXRvX2NvbXByZXNzIjoiMSIsImludmVudG9yeV9tb2RlIjoiLTEifSx7Imhvc3RpZCI6IjEwNDMzIiwicHJveHlfaG9zdGlkIjoiMCIsImhvc3QiOiJhZ2VudDE5Mi4xNjguMjE4LjExNSIsInN0YXR1cyI6IjAiLCJkaXNhYmxlX3VudGlsIjoiMTY0MDg1MzkwNyIsImVycm9yIjoiR2V0IHZhbHVlIGZyb20gYWdlbnQgZmFpbGVkOiBjYW5ub3QgY29ubmVjdCB0byBbWzE5Mi4xNjguMjE4LjExNV06MTAwNTBdOiBbMTExXSBDb25uZWN0aW9uIHJlZnVzZWQiLCJhdmFpbGFibGUiOiIyIiwiZXJyb3JzX2Zyb20iOiIxNjM5NzM3OTc2IiwibGFzdGFjY2VzcyI6IjAiLCJpcG1pX2F1dGh0eXBlIjoiLTEiLCJpcG1pX3ByaXZpbGVnZSI6IjIiLCJpcG1pX3VzZXJuYW1lIjoiIiwiaXBtaV9wYXNzd29yZCI6IiIsImlwbWlfZGlzYWJsZV91bnRpbCI6IjAiLCJpcG1pX2F2YWlsYWJsZSI6IjAiLCJzbm1wX2Rpc2FibGVfdW50aWwiOiIwIiwic25tcF9hdmFpbGFibGUiOiIwIiwibWFpbnRlbmFuY2VpZCI6IjAiLCJtYWludGVuYW5jZV9zdGF0dXMiOiIwIiwibWFpbnRlbmFuY2VfdHlwZSI6IjAiLCJtYWludGVuYW5jZV9mcm9tIjoiMCIsImlwbWlfZXJyb3JzX2Zyb20iOiIwIiwic25tcF9lcnJvcnNfZnJvbSI6IjAiLCJpcG1pX2Vycm9yIjoiIiwic25tcF9lcnJvciI6IiIsImpteF9kaXNhYmxlX3VudGlsIjoiMCIsImpteF9hdmFpbGFibGUiOiIwIiwiam14X2Vycm9yc19mcm9tIjoiMCIsImpteF9lcnJvciI6IiIsIm5hbWUiOiJhZ2VudDE5Mi4xNjguMjE4LjExNSIsImZsYWdzIjoiMCIsInRlbXBsYXRlaWQiOiIwIiwiZGVzY3JpcHRpb24iOiIiLCJ0bHNfY29ubmVjdCI6IjEiLCJ0bHNfYWNjZXB0IjoiMSIsInRsc19pc3N1ZXIiOiIiLCJ0bHNfc3ViamVjdCI6IiIsInRsc19wc2tfaWRlbnRpdHkiOiIiLCJ0bHNfcHNrIjoiIiwicHJveHlfYWRkcmVzcyI6IiIsImF1dG9fY29tcHJlc3MiOiIxIiwiaW52ZW50b3J5X21vZGUiOiItMSJ9XX0sInZpZXdzIjpbeyJ0eXBlIjoiSlNPTiIsImRhdGFTb3VyY2UiOiIke3tkYXRhfX0ifV19LCJkZXNjcmlwdGlvbiI6InphYmJpeCBob3N0IHJlc3VsdCIsInZpZXdzIjpbeyJ0eXBlIjoiSlNPTiIsImRhdGFTb3VyY2UiOiIke3tkYXRhfX0ifV19fSx7Im5hbWUiOiJHRVRfQ1VSUkVOVF9JU1NVRVMiLCJhbGlhcyI6IuiOt+WPluaJgOaciemXrumimCIsImRlc2NyaXB0aW9uIjoi6I635Y+WemFiYml45Li75py66Zeu6aKYIiwicGFyYW1ldGVycyI6W3sibmFtZSI6Imhvc3RfaXAiLCJ2YWx1ZSI6IiIsImV4YW1wbGUiOiIxMC4yMTUuNy4xNyIsImRlc2NyaXB0aW9uIjoi5Li75py6aXAiLCJzY2hlbWEiOnsidHlwZSI6IlNUUklORyJ9LCJ1aSI6eyJ1aU5hbWUiOiLkuLvmnLppcCIsInR5cGUiOiJ0ZXh0YXJlYSJ9LCJyZXF1aXJlZCI6dHJ1ZX1dLCJyZXR1cm5zIjp7InNjaGVtYSI6eyJ0eXBlIjoiSlNPTl9BUlJBWSJ9LCJleGFtcGxlIjoiW3tcInRyaWdnZXJpZFwiOiBcIjE5NzkxXCIsIFwiZXhwcmVzc2lvblwiOiBcInsyMzcwNH0gPiB7JFZGUy5ERVYuUkVBRC5BV0FJVC5XQVJOOlxcXCJzZGFcXFwifSBvciB7MjM3MDV9ID4geyRWRlMuREVWLldSSVRFLkFXQUlULldBUk46XFxcInNkYVxcXCJ9XCIsIFwiZGVzY3JpcHRpb25cIjogXCJzZGE6IERpc2sgcmVhZC93cml0ZSByZXF1ZXN0IHJlc3BvbnNlcyBhcmUgdG9vIGhpZ2ggKHJlYWQgPiAyMCBtcyBmb3IgMTVtIG9yIHdyaXRlID4gMjAgbXMgZm9yIDE1bSlcIiwgXCJ1cmxcIjogXCJcIiwgXCJzdGF0dXNcIjogXCIwXCIsIFwidmFsdWVcIjogXCIxXCIsIFwicHJpb3JpdHlcIjogXCIyXCIsIFwibGFzdGNoYW5nZVwiOiBcIjE2Mzk3MzY2MjdcIiwgXCJjb21tZW50c1wiOiBcIlRoaXMgdHJpZ2dlciBtaWdodCBpbmRpY2F0ZSBkaXNrIHNkYSBzYXR1cmF0aW9uLlwiLCBcImVycm9yXCI6IFwiXCIsIFwidGVtcGxhdGVpZFwiOiBcIjBcIiwgXCJ0eXBlXCI6IFwiMFwiLCBcInN0YXRlXCI6IFwiMFwiLCBcImZsYWdzXCI6IFwiNFwiLCBcInJlY292ZXJ5X21vZGVcIjogXCIwXCIsIFwicmVjb3ZlcnlfZXhwcmVzc2lvblwiOiBcIlwiLCBcImNvcnJlbGF0aW9uX21vZGVcIjogXCIwXCIsIFwiY29ycmVsYXRpb25fdGFnXCI6IFwiXCIsIFwibWFudWFsX2Nsb3NlXCI6IFwiMVwiLCBcIm9wZGF0YVwiOiBcIlwiLCBcImhvc3RzXCI6IFt7XCJob3N0aWRcIjogXCIxMDQzMlwiLCBcImhvc3RcIjogXCJhZ2VudDEwLjIxNS43LjE3XCJ9XSwgXCJ1bmFja25vd2xlZGdlZFwiOiB0cnVlfSwge1widHJpZ2dlcmlkXCI6IFwiMTk3NjFcIiwgXCJleHByZXNzaW9uXCI6IFwiezIzNjIxfT0wXCIsIFwiZGVzY3JpcHRpb25cIjogXCJaYWJiaXggYWdlbnQgaXMgbm90IGF2YWlsYWJsZSAoZm9yIDNtKVwiLCBcInVybFwiOiBcIlwiLCBcInN0YXR1c1wiOiBcIjBcIiwgXCJ2YWx1ZVwiOiBcIjFcIiwgXCJwcmlvcml0eVwiOiBcIjNcIiwgXCJsYXN0Y2hhbmdlXCI6IFwiMTYzOTczODE3NVwiLCBcImNvbW1lbnRzXCI6IFwiRm9yIHBhc3NpdmUgb25seSBhZ2VudHMsIGhvc3QgYXZhaWxhYmlsaXR5IGlzIHVzZWQgd2l0aCB7JEFHRU5ULlRJTUVPVVR9IGFzIHRpbWUgdGhyZXNob2xkLlwiLCBcImVycm9yXCI6IFwiXCIsIFwidGVtcGxhdGVpZFwiOiBcIjE2MjA2XCIsIFwidHlwZVwiOiBcIjBcIiwgXCJzdGF0ZVwiOiBcIjBcIiwgXCJmbGFnc1wiOiBcIjBcIiwgXCJyZWNvdmVyeV9tb2RlXCI6IFwiMFwiLCBcInJlY292ZXJ5X2V4cHJlc3Npb25cIjogXCJcIiwgXCJjb3JyZWxhdGlvbl9tb2RlXCI6IFwiMFwiLCBcImNvcnJlbGF0aW9uX3RhZ1wiOiBcIlwiLCBcIm1hbnVhbF9jbG9zZVwiOiBcIjFcIiwgXCJvcGRhdGFcIjogXCJcIiwgXCJob3N0c1wiOiBbe1wiaG9zdGlkXCI6IFwiMTA0MzNcIiwgXCJob3N0XCI6IFwiYWdlbnQxOTIuMTY4LjIxOC4xMTVcIn1dLCBcInVuYWNrbm93bGVkZ2VkXCI6IHRydWV9LCB7XCJ0cmlnZ2VyaWRcIjogXCIxOTczNFwiLCBcImV4cHJlc3Npb25cIjogXCJ7MjM1NzR9PTBcIiwgXCJkZXNjcmlwdGlvblwiOiBcIlN5c3RlbSB0aW1lIGlzIG91dCBvZiBzeW5jIChkaWZmIHdpdGggWmFiYml4IHNlcnZlciA+IDYwcylcIiwgXCJ1cmxcIjogXCJcIiwgXCJzdGF0dXNcIjogXCIwXCIsIFwidmFsdWVcIjogXCIxXCIsIFwicHJpb3JpdHlcIjogXCIyXCIsIFwibGFzdGNoYW5nZVwiOiBcIjE2NDAxNDk5NDRcIiwgXCJjb21tZW50c1wiOiBcIlRoZSBob3N0IHN5c3RlbSB0aW1lIGlzIGRpZmZlcmVudCBmcm9tIHRoZSBaYWJiaXggc2VydmVyIHRpbWUuXCIsIFwiZXJyb3JcIjogXCJcIiwgXCJ0ZW1wbGF0ZWlkXCI6IFwiMTYwNTVcIiwgXCJ0eXBlXCI6IFwiMFwiLCBcInN0YXRlXCI6IFwiMFwiLCBcImZsYWdzXCI6IFwiMFwiLCBcInJlY292ZXJ5X21vZGVcIjogXCIwXCIsIFwicmVjb3ZlcnlfZXhwcmVzc2lvblwiOiBcIlwiLCBcImNvcnJlbGF0aW9uX21vZGVcIjogXCIwXCIsIFwiY29ycmVsYXRpb25fdGFnXCI6IFwiXCIsIFwibWFudWFsX2Nsb3NlXCI6IFwiMVwiLCBcIm9wZGF0YVwiOiBcIlwiLCBcImhvc3RzXCI6IFt7XCJob3N0aWRcIjogXCIxMDQzMlwiLCBcImhvc3RcIjogXCJhZ2VudDEwLjIxNS43LjE3XCJ9XSwgXCJ1bmFja25vd2xlZGdlZFwiOiB0cnVlfV0iLCJ1aUV4YW1wbGUiOnsiYXBwc0FjdGlvblJlc3BvbnNlIjp7InN0YXR1cyI6IlN1Y2Nlc3MiLCJzY2hlbWEiOnsidHlwZSI6IkpTT05fQVJSQVkifSwiZGF0YSI6W3sidHJpZ2dlcmlkIjoiMTk3OTEiLCJleHByZXNzaW9uIjoiezIzNzA0fSA+IHskVkZTLkRFVi5SRUFELkFXQUlULldBUk46XCJzZGFcIn0gb3IgezIzNzA1fSA+IHskVkZTLkRFVi5XUklURS5BV0FJVC5XQVJOOlwic2RhXCJ9IiwiZGVzY3JpcHRpb24iOiJzZGE6IERpc2sgcmVhZC93cml0ZSByZXF1ZXN0IHJlc3BvbnNlcyBhcmUgdG9vIGhpZ2ggKHJlYWQgPiAyMCBtcyBmb3IgMTVtIG9yIHdyaXRlID4gMjAgbXMgZm9yIDE1bSkiLCJ1cmwiOiIiLCJzdGF0dXMiOiIwIiwidmFsdWUiOiIxIiwicHJpb3JpdHkiOiIyIiwibGFzdGNoYW5nZSI6IjE2Mzk3MzY2MjciLCJjb21tZW50cyI6IlRoaXMgdHJpZ2dlciBtaWdodCBpbmRpY2F0ZSBkaXNrIHNkYSBzYXR1cmF0aW9uLiIsImVycm9yIjoiIiwidGVtcGxhdGVpZCI6IjAiLCJ0eXBlIjoiMCIsInN0YXRlIjoiMCIsImZsYWdzIjoiNCIsInJlY292ZXJ5X21vZGUiOiIwIiwicmVjb3ZlcnlfZXhwcmVzc2lvbiI6IiIsImNvcnJlbGF0aW9uX21vZGUiOiIwIiwiY29ycmVsYXRpb25fdGFnIjoiIiwibWFudWFsX2Nsb3NlIjoiMSIsIm9wZGF0YSI6IiIsImhvc3RzIjpbeyJob3N0aWQiOiIxMDQzMiIsImhvc3QiOiJhZ2VudDEwLjIxNS43LjE3In1dLCJ1bmFja25vd2xlZGdlZCI6dHJ1ZX0seyJ0cmlnZ2VyaWQiOiIxOTc2MSIsImV4cHJlc3Npb24iOiJ7MjM2MjF9PTAiLCJkZXNjcmlwdGlvbiI6IlphYmJpeCBhZ2VudCBpcyBub3QgYXZhaWxhYmxlIChmb3IgM20pIiwidXJsIjoiIiwic3RhdHVzIjoiMCIsInZhbHVlIjoiMSIsInByaW9yaXR5IjoiMyIsImxhc3RjaGFuZ2UiOiIxNjM5NzM4MTc1IiwiY29tbWVudHMiOiJGb3IgcGFzc2l2ZSBvbmx5IGFnZW50cywgaG9zdCBhdmFpbGFiaWxpdHkgaXMgdXNlZCB3aXRoIHskQUdFTlQuVElNRU9VVH0gYXMgdGltZSB0aHJlc2hvbGQuIiwiZXJyb3IiOiIiLCJ0ZW1wbGF0ZWlkIjoiMTYyMDYiLCJ0eXBlIjoiMCIsInN0YXRlIjoiMCIsImZsYWdzIjoiMCIsInJlY292ZXJ5X21vZGUiOiIwIiwicmVjb3ZlcnlfZXhwcmVzc2lvbiI6IiIsImNvcnJlbGF0aW9uX21vZGUiOiIwIiwiY29ycmVsYXRpb25fdGFnIjoiIiwibWFudWFsX2Nsb3NlIjoiMSIsIm9wZGF0YSI6IiIsImhvc3RzIjpbeyJob3N0aWQiOiIxMDQzMyIsImhvc3QiOiJhZ2VudDE5Mi4xNjguMjE4LjExNSJ9XSwidW5hY2tub3dsZWRnZWQiOnRydWV9LHsidHJpZ2dlcmlkIjoiMTk3MzQiLCJleHByZXNzaW9uIjoiezIzNTc0fT0wIiwiZGVzY3JpcHRpb24iOiJTeXN0ZW0gdGltZSBpcyBvdXQgb2Ygc3luYyAoZGlmZiB3aXRoIFphYmJpeCBzZXJ2ZXIgPiA2MHMpIiwidXJsIjoiIiwic3RhdHVzIjoiMCIsInZhbHVlIjoiMSIsInByaW9yaXR5IjoiMiIsImxhc3RjaGFuZ2UiOiIxNjQwMTQ5OTQ0IiwiY29tbWVudHMiOiJUaGUgaG9zdCBzeXN0ZW0gdGltZSBpcyBkaWZmZXJlbnQgZnJvbSB0aGUgWmFiYml4IHNlcnZlciB0aW1lLiIsImVycm9yIjoiIiwidGVtcGxhdGVpZCI6IjE2MDU1IiwidHlwZSI6IjAiLCJzdGF0ZSI6IjAiLCJmbGFncyI6IjAiLCJyZWNvdmVyeV9tb2RlIjoiMCIsInJlY292ZXJ5X2V4cHJlc3Npb24iOiIiLCJjb3JyZWxhdGlvbl9tb2RlIjoiMCIsImNvcnJlbGF0aW9uX3RhZyI6IiIsIm1hbnVhbF9jbG9zZSI6IjEiLCJvcGRhdGEiOiIiLCJob3N0cyI6W3siaG9zdGlkIjoiMTA0MzIiLCJob3N0IjoiYWdlbnQxMC4yMTUuNy4xNyJ9XSwidW5hY2tub3dsZWRnZWQiOnRydWV9XX0sInZpZXdzIjpbeyJ0eXBlIjoiSlNPTiIsImRhdGFTb3VyY2UiOiIke3tkYXRhfX0ifV19LCJkZXNjcmlwdGlvbiI6InphYmJpeCBob3N0IGlzc3VlcyByZXN1bHQiLCJ2aWV3cyI6W3sidHlwZSI6IkpTT04iLCJkYXRhU291cmNlIjoiJHt7ZGF0YX19In1dfX1dLCJpbWFnZSI6e319"
    # action_name = "PING"
    app = ZabbixClientApp(APP_NAME, ACTION_LIST, input_data, action_name)
    app.do_action() 