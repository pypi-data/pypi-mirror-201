
from loguru import logger
import json
from common.common.api_driver import APIDriver
from common.common.constant import Constant
from common.data.handle_common import get_system_key,format_caseName,set_system_key
from common.plat.mysql_platform import MysqlPlatForm
from common.data.data_process import DataProcess



class ATFPlatForm(object):

    @classmethod
    def db_ops(self, _key, _sql, env: str = Constant.ENV):
        """
        执行SQL操作
        :param _key:
        :param _sql:
        :param env:
        :return:
        """
        _sqltemp=_sql.encode("utf-8").decode("latin1")
        if get_system_key(env) is not None:
            env = get_system_key(env)
        sql_type = _sql.strip().split(" ")[0].lower()
        if "select" == sql_type:
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/querySetResult/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sqltemp
                                               )
            logger.info(f"执行sql成功:{_sql}")
            return list(_tempdata.json())
        if "insert" == sql_type or "delete":
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/doExecute/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sqltemp)
            logger.info(f"执行sql成功:{_sql}")
            return _tempdata.text
        else:
            logger.error("不支持其他语句类型执行，请检查sql")


    @classmethod
    def runDeploy(self,jobName, _pramater):
        """
        推送测试结果
        :param jobName:
        :param _pramater:
        :return:
        """
        _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL}/jenkins/runDeploy/{jobName}",
                                               method='get', parametric_key='params', data=_pramater)
        return _tempdata


    @classmethod
    def getProjectData(self, projectName, projectKey):
        """
        获取项目数据
        :param projectName: 项目别名
        :param projectKey: 关键词
        :return:
        """

        try:
            content = APIDriver.http_request(url=f"{Constant.ATF_URL}/api/getProjectData/{projectName}/{projectKey}",
            method='get')
            return (json.loads(content.content)["data"]["projectValue"])
        except Exception as e:
            logger.info(f"{Constant.ATF_URL}/api/getProjectData/{projectName}/{projectKey}" + "获取不到value")
            return None

    @classmethod
    def setProjectData(self, projectKey, value, type = 1):
        """
        设置项目数据
        :param projectName: 项目别名
        :param projectKey: 关键词
        :param value: 值
        :param type: 数据类型[0可以重复使用，1不可以重复使用]
        :return:
        """
        if get_system_key('ProjectAlice') is not None and get_system_key('ProjectAlice').strip() != '':
            projectName = get_system_key('ProjectAlice')
            return APIDriver.http_request(
                url=f"{Constant.ATF_URL}/api/setProjectData/{projectName}/{projectKey}/{value}/{type}",
                method='get'
                )

    @classmethod
    def getCycleByCaseName(self, CaseName:str):
        _list = []
        try:
            _listCase = CaseName.split(";")
            if DataProcess.isNotNull(get_system_key(Constant.ISSUE_KEY)) and DataProcess.isNotNull(get_system_key(Constant.TEST_SRTCYCLE_ID)):
                for _temp in _listCase:
                    _dict =MysqlPlatForm.get_test_case_info(get_system_key(Constant.ISSUE_KEY), get_system_key(Constant.TEST_SRTCYCLE_ID), format_caseName(_temp))
                    if len(_dict) > 0:
                        _list.append(_dict[0])
        except Exception as e:
            logger.info(f'获取周期的用例名称{CaseName}信息异常' + repr(e))
        return _list

    @classmethod
    def syncCaseJiraMysql(self, _caseNameList, result):
        logger.info("初始化需要运行的测试用例并同步到数据库")
        for _case in _caseNameList:
            _caseMete = ATFPlatForm.getCaseInfo(_case['caseid'])
            if _caseMete['type'] == Constant.CASE_TYPE_AUTO and _caseMete['key'] != '00000':
                _runid = _case['caserunid']
                ATFPlatForm.updateByRunid(_runid, result, "")


    @classmethod
    def get_test_autotest_run_byStatus(self, result):
        _list = []
        if DataProcess.isNotNull(get_system_key(Constant.ISSUE_KEY)) and DataProcess.isNotNull(
                get_system_key(Constant.TEST_SRTCYCLE_ID)):
            _list = MysqlPlatForm.get_test_autotest_run(get_system_key(Constant.ISSUE_KEY),
                                                        get_system_key(Constant.TEST_SRTCYCLE_ID), result)
        return _list

    @classmethod
    def getCycleByCaseID(self, caseId: str):
        _list = []
        try:
            _listCase = caseId.split(";")
            if DataProcess.isNotNull(get_system_key(Constant.ISSUE_KEY)) and DataProcess.isNotNull(
                    get_system_key(Constant.TEST_SRTCYCLE_ID)):
                for _temp in _listCase:
                    _dict = MysqlPlatForm.get_test_case_info_ByID(get_system_key(Constant.ISSUE_KEY),
                                                             get_system_key(Constant.TEST_SRTCYCLE_ID),
                                                             _temp)
                    if len(_dict) > 0:
                        _list.append(_dict[0])
        except Exception as e:
            logger.info(f'获取周期的用例编号{caseId}信息异常'+repr(e))
        return _list

    @classmethod
    def getCycleByResult(self,  restult: str = "'通过','未执行','失败','自动化执行'"):
        _list = []
        if DataProcess.isNotNull(get_system_key(Constant.ISSUE_KEY)) and DataProcess.isNotNull(
                get_system_key(Constant.TEST_SRTCYCLE_ID)):
            _list = MysqlPlatForm.get_test_autotest_run(get_system_key(Constant.ISSUE_KEY),
                                                         get_system_key(Constant.TEST_SRTCYCLE_ID),
                                                         restult)
        return _list

    @classmethod
    def runSenceCase(self, _caseList):
        _caseNameList = []
        _caseScriptList = []
        for caseName in _caseNameList:
            caseName = format_caseName(caseName['casename'])
            _caseNameList.append(caseName)
        _caseScriptList = MysqlPlatForm.getScriptyPathByCaseNameList(_caseNameList)
        return _caseNameList, _caseScriptList


    @classmethod
    def sent_result_byCaseName(self, CaseName, CaseID, result, comment, scriptUrl:str = ""):
        try:
            _case = ATFPlatForm.getCycleByCaseName(CaseName)
            if len(_case) == 0 and DataProcess.isNotNull(CaseID):
                _case = ATFPlatForm.getCycleByCaseID(CaseID)
            if len(_case) > 0:
                _runid = _case[0]['caserunid']
                _caseid = _case[0]['caseid']
                _caseTitle = _case[0]['casename']
                if scriptUrl != "":
                    MysqlPlatForm.insert_test_autotest_script(_caseTitle, _caseid, scriptUrl)
                ATFPlatForm.updateByRunid(_runid,result,comment)
                logger.info(f'用例名称:{CaseName} 运行ID：{_runid}  结果:{result} 结果描述:{comment} 推送成功')
            else:
                logger.info(f'用例名称:{CaseName} 用例编号:{CaseID} 结果:{result} 在测试周期中没有找到')
        except Exception as e:
            logger.info(f'用例名称:{CaseName} 用例编号:{CaseID} 结果:{result}  结果描述:{comment} 推送异常:' + repr(e))

    @classmethod
    def syncCycleNameCase(self):
        ATFPlatForm.syncCycleBasic()
        if DataProcess.isNotNull(get_system_key(Constant.TEST_SRTCYCLE_ID)):
            ATFPlatForm.syncCycleCase(get_system_key(Constant.TEST_SRTCYCLE_ID))

    @classmethod
    def syncCycleBasic(self):
        if DataProcess.isNotNull(get_system_key(Constant.TEST_SRTCYCLE_ID)):
            cycleId = get_system_key(Constant.TEST_SRTCYCLE_ID)
            issueKey =""
            try:
                testPlan = ATFPlatForm.getTestPlanInfo(get_system_key(Constant.TEST_SRTCYCLE_ID).strip())
                set_system_key(Constant.TEST_SRTCYCLE_ID, str(testPlan['cycleId']))
                set_system_key(Constant.TEST_SRTCYCLE_NAME, testPlan['cycleName'])
                set_system_key(Constant.TEST_SRTCYCLE_URL, testPlan['cycleUrl'])

                set_system_key(Constant.ISSUE_KEY, testPlan['issueKey'])
                issueKey = testPlan['issueKey']
                set_system_key(Constant.TEST_TestPlan_ID, str(testPlan['testPlanId']))
                set_system_key(Constant.TEST_TestPlan_NAME, testPlan['testPlanName'])
                set_system_key(Constant.TEST_TestPlan_URL, testPlan['testPlanUrl'])
            except Exception as e:
                logger.error(f"获取周期{cycleId}中测试计划:{issueKey}\n 异常:" + repr(e))

        if DataProcess.isNotNull(get_system_key(Constant.PROJECT_NAME)):
            projectId = get_system_key(Constant.PROJECT_NAME).split("（")[-1].split("）")[0]
            set_system_key(Constant.PORJECT_ID, projectId)



    @classmethod
    def getTestPlanInfo(self,cycleId):
        return json.loads(APIDriver.http_request(url=f"{Constant.ATF_PYTHON_URL}/jira/plan/get/{cycleId}", method='get').content)

    @classmethod
    def updateByRunid(self, runid, result, comment:str = "", steps:str = ""):
        _dict = {'result': result, 'comment': comment, 'steps': steps}
        APIDriver.http_request(
            url=f"{Constant.ATF_PYTHON_URL}/jira/run/update/{runid}",
            method='post',
            parametric_key='json',
            data=json.loads(json.dumps(_dict,ensure_ascii=False))
        )

    @classmethod
    def syncCycleCase(self, cycleId):
        if DataProcess.isNotNull(get_system_key('Result')):
            _dict = {'status': get_system_key('Result')}
        else:
            _dict = {'status': ''}
        APIDriver.http_request(
            url=f"{Constant.ATF_PYTHON_URL}/jira/sync/{cycleId}",
            method='post',
            parametric_key='json',
            data=json.loads(json.dumps(_dict, ensure_ascii=False))
        )

    @classmethod
    def updateStausByCycleId(self, cycleId, status):
        _dict = {'status': status}
        APIDriver.http_request(
            url=f"{Constant.ATF_PYTHON_URL}/jira/update/cycle/status/{cycleId}",
            method='post',
            parametric_key='json',
            data=json.loads(json.dumps(_dict, ensure_ascii=False))
        )

    @classmethod
    def getCaseInfoByNameOrID(self, issueKey, caseName:str=""):
        info = ATFPlatForm.getCaseInfo(issueKey)
        if info['key'] == '00000'or caseName != "" :
            info = ATFPlatForm.getCaseInfo(caseName)
        return info

    @classmethod
    def getCaseRunByNameOrID(self, cycleId, name):
        _dict = {'cycleId': cycleId, 'name': name}
        content = APIDriver.http_request(
            url=f"{Constant.ATF_PYTHON_URL}/jira/run/get",
            method='post',
            parametric_key='json',
            data=json.loads(json.dumps(_dict, ensure_ascii=False))
        )
        return json.loads(content.content)



    @classmethod
    def getCaseRun(self,cycleId, issuekey, name):
        run = ATFPlatForm.getCaseRunByNameOrID(cycleId, issuekey)
        if run['caserunid'] == '00000':
            run = ATFPlatForm.getCaseRunByNameOrID(cycleId, name)
        return run

    @classmethod
    def getCaseInfo(self, caseName):
        _dict = {'name': caseName}
        _result = ""
        try:
            if DataProcess.isNotNull(get_system_key(Constant.PORJECT_ID)):
                projectId=get_system_key(Constant.PORJECT_ID)
                _dict = {'name': caseName, 'projectId': projectId}
                content = APIDriver.http_request(
                    url=f"{Constant.ATF_PYTHON_URL}/jira/case/get",
                    method='post',
                    parametric_key='json',
                    data=json.loads(json.dumps(_dict, ensure_ascii=False))
                )
            else:
                content = APIDriver.http_request(
                    url=f"{Constant.ATF_PYTHON_URL}/jira/case/get",
                    method='post',
                    parametric_key='json',
                    data=json.loads(json.dumps(_dict, ensure_ascii=False))
                )
            _result = content.content
            return json.loads(_result)
        except Exception as e:
            logger.error(f"获取用例名称:{_dict}  返回内容:{_result} 异常:" + repr(e))




if __name__ == '__main__':
    print(ATFPlatForm.updateStausByCycleId('21235',Constant.STATUS_PRE))
