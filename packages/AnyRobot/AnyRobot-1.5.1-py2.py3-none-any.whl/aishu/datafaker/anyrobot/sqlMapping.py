from aishu import setting
from aishu.datafaker.profession.entity import ip
def sql(key):
    """
    对应数据服务的sql语句注册
    :param key:
    :return:
    """
    switcher = {
        'OpensearchSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%opensearch服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'HostServiceSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%AR主机服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'ServiceSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%AR服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'MySystemMetric':{
            'sql':"SELECT `groupId` FROM loggroup where groupName LIKE '%mysystemmetric%' order  by createTime desc;",
            'database': 'anyrobot'
        },
        'CPUSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%Linux主机CPU服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'MemorySLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%Linux主机内存服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'LoadSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%Linux主机平均负载服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'IOSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%Linux主机IO利用率服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'DiskSLO': {
            'sql': "SELECT `id` FROM kai_service where name LIKE '%Linux主机磁盘利用率服务SLO%' order  by create_time desc;",
            'database': 'anyrobot'
        },
        'UserID':{'sql':'select userId from User where loginName = "admin";','database':'anyrobot'},
        'MLID': {'sql': "select id from MLJob ;", 'database': 'anyrobotml'},
        'entityID': {'sql': "select id from KAIEntity;", 'database': 'anyrobot'},
        'groupID': {'sql': "select id from KAIEntityGroup;", 'database': 'anyrobot'},
        'AlertRuleID': {'sql': "select id from RuleEngineAlert;", 'database': 'anyrobot'},
        'kpiID': {'sql': "select id from KAIKpi;", 'database': 'anyrobot'},
        'LogTypeID': {'sql': "select dataType from LogWareHouse;", 'database': 'anyrobot'},
        'AddEntityID': {
            'sql': "select entityId from KAIEntityCondition where conditionValues = '192.168.84.26' AND conditionKeys = 'host';",
            'database': 'anyrobot'},
        'KpiTemplateID': {'sql': "select id from KAIKpiTemplate;", 'database': 'anyrobot'},
        'KpiTemplateID1': {'sql': "select id from KAIKpiTemplate;", 'database': 'anyrobot'},
        'KpiTemplateID2': {'sql': "select id from KAIKpiTemplate;", 'database': 'anyrobot'},
        'logWareHouseID': {'sql': "SELECT id From LogWareHouse where LENGTH(id)!=8;", 'database': 'anyrobot'},
        'logWareHouseId': {'sql': "SELECT id From LogWareHouse where LENGTH(id)!=8;", 'database': 'anyrobot'},
        'wareHouseName': {'sql': "SELECT wareHouseName From LogWareHouse;", 'database': 'anyrobot'},
        'dataType': {'sql': "SELECT dataType From LogWareHouse where LENGTH(id)!=8;", 'database': 'anyrobot'},
        'indexID': {'sql': "SELECT id From IndexParams;", 'database': 'anyrobot'},
        'indexName': {'sql': "SELECT indexName From IndexParams;", 'database': 'anyrobot'},
        'StreamId': {'sql': "SELECT id From DataStream;", 'database': 'anyrobot'},
        'LogGroupIdPare': {'sql': 'SELECT groupId From LogGroup where GroupName!="所有日志";', 'database': 'anyrobot'},
        'RoleId': {'sql': 'SELECT roleId From Role where roleName ="admin";', 'database': 'anyrobot'},
        'RoleId_Notadmin': {'sql': 'SELECT roleId From Role where roleName != "admin" AND roleName != "user";', 'database': 'anyrobot'},
        'tagGroupID': {'sql': "SELECT id From TagGroup;", 'database': 'anyrobot'},
        'tagID': {'sql': "SELECT id From Tag;", 'database': 'anyrobot'},
        'HostID': {'sql': "SELECT id From AgentHost;", 'database': 'anyrobot'},
        'HostIp': {'sql': "SELECT ip From AgentHost;", 'database': 'anyrobot'},
        'openapiID': {'sql': "SELECT id From OpenAPIManager;", 'database': 'anyrobotopenLog'},
        'UserID_Notadmin': {'sql': 'select userId from User where loginName != "admin" AND status != 0;', 'database': 'anyrobot'},
        'JDBCCollectorId': {
            'sql': "select collectorId from JDBCCollectorConfig where JDBCCollectorConfig.type='mysqljdbc' AND JDBCCollectorConfig.`sql`='select * from AgentHost';",
            'database': 'anyrobot'},
        'vSphereID': {
            'sql': "SELECT collectorId FROM CollectorConfig WHERE collectorType='vSphere' AND config LIKE '%hlaio.aishu.cn%';",
            'database': 'anyrobot'},
        'vcenterCollectorId': {
            'sql': "SELECT collectorId FROM CollectorConfig WHERE collectorType='vCenter' AND config LIKE '%hlaio.aishu.cn%';",
            'database': 'anyrobot'},
        'MySQLCollectorId': {'sql': "SELECT collectorId FROM CollectorConfig WHERE collectorType='MySQL Performance';",
                             'database': 'anyrobot'},
        'OracleCollectorId': {
            'sql': "SELECT collectorId FROM CollectorConfig WHERE collectorType='Oracle Performance';",
            'database': 'anyrobot'},
        'AIXCollectorId': {'SQL': "SELECT collectorId FROM CollectorConfig WHERE collectorType='AIX Errpt';",
                           'database': 'anyrobot'},
        'CMDCollectorId': {'sql': "SELECT collectorId FROM CollectorConfig WHERE collectorType='Command Result';",
                           'database': 'anyrobot'},
        'CollectorId': {'sql': "SELECT collectorId FROM CollectorConfig;", 'database': 'anyrobot'},
        'DBConnectID': {'sql': "SELECT id FROM DBConnect;", 'database': 'anyrobot'},
        'AuthID': {'sql': "SELECT id FROM AgentHostAuth;", 'database': 'anyrobot'},
        'authName': {'sql': "SELECT `name` FROM AgentHostAuth;", 'database': 'anyrobot'},
        'TemplateID': {'sql': "SELECT id FROM AgentConfigTemplate;", 'database': 'anyrobot'},
        'AgentInputTemplateID': {'sql': "SELECT id FROM AgentConfigTemplate WHERE category='input';",
                                 'database': 'anyrobot'},
        'AgentOutTemplateID': {'sql': "SELECT id FROM AgentConfigTemplate WHERE category='output';",
                               'database': 'anyrobot'},
        'InputTemplateName': {'sql': "SELECT `name` FROM AgentConfigTemplate WHERE category='input';",
                              'database': 'anyrobot'},
        'OutputTemplateName': {'sql': "SELECT `name` FROM AgentConfigTemplate WHERE category='output';",
                               'database': 'anyrobot'},
        'AgentGroupID': {'sql': "SELECT id FROM AgentGroup;", 'database': 'anyrobot'},
        'AgentJobTemplateID': {'sql': "SELECT id FROM AgentJobTemplate", 'database': 'anyrobot'},
        'JobID': {'sql': "SELECT id FROM AgentJobInfo;", 'database': 'anyrobot'},
        'uploadID': {'sql': "SELECT id FROM Upload;", 'database': 'anyrobot'},
        'uninstallHostID': {'sql':"SELECT id From AgentHost WHERE ip='{ip}';".format(ip=ip.date().getAentHostIp()),'database': 'anyrobot'},
        'entitygroupId': {'sql':"SELECT id From KAIEntityGroup ;",'database': 'anyrobot'},
        'serviceKpiId': {'sql':"SELECT id From KAIKpi ;",'database': 'anyrobot'},
        'serviceHeathId': {'sql':"SELECT serviceId From KAIHealth ;",'database': 'anyrobot'},
        'KAIAlertId': {'sql':"SELECT id From KAIAlert ;",'database': 'anyrobot'},
        'KAIBusinessId': {'sql':"SELECT id From KAIBusiness ;",'database': 'anyrobot'},
        'graphName': {'sql':"SELECT graph_name From graph ;",'database': 'anyrobot'},
        'ScheduleTaskId': {'sql':"SELECT id From ScheduleTask ;",'database': 'anyrobot'},
        'ScheduleTaskId1': {'sql':"SELECT id From ScheduleTask ;",'database': 'anyrobot'},
        'UserId': {'sql':"SELECT userId From User ;",'database': 'anyrobot'},
        'UserId2': {'sql':"SELECT userId From User ;",'database': 'anyrobot'},
        'alertLogId': {'sql':"SELECT alert_scenario_rule_id From RuleEngineAlertLog ;",'database': 'anyrobot'},
        'RuleEngineEnableId': {'sql':"SELECT id From RuleEngineAlertScenario Where status = 1;",'database': 'anyrobot'},
        'RuleEngineDisableId': {'sql':"SELECT id From RuleEngineAlertScenario Where status = 0;",'database': 'anyrobot'},
        'KAIAlertEnableId': {'sql':"SELECT id From KAIAlert Where status = 1 ;",'database': 'anyrobot'},
        'KAIAlertDisableId': {'sql':"SELECT id From KAIAlert Where status = 0 ;",'database': 'anyrobot'},
        'ScheduleTaskEnableId': {'sql':"SELECT id From ScheduleTask Where status = 1 ;",'database': 'anyrobot'},
        'ScheduleTaskDisableId': {'sql':"SELECT id From ScheduleTask Where status = 0 ;",'database': 'anyrobot'},
        'ReprotId': {'sql': "SELECT report_id From report WHERE is_share_allowed = 1;", 'database': 'anyrobot'},
        'ReprotIdDisable': {'sql': "SELECT report_id From report WHERE is_share_allowed = 0;", 'database': 'anyrobot'},
        'ReprotName': {'sql': "SELECT `name` From report ;", 'database': 'anyrobot'},
        'ReprotType': {'sql': "SELECT `type` From report ;", 'database': 'anyrobot'},
        'CorrelationSearchesId': {'sql': "SELECT `id` From correlate_search ;", 'database': 'anyrobot'}
    }

    if switcher.get(key) is not None:
        if switcher[key].get('database') is not None:
            if len(switcher[key]['database']) == 0:
                setting.database = 'anyrobot'
            else:
                setting.database = switcher[key]['database']

        return switcher[key]['sql']
    else:
        return False
