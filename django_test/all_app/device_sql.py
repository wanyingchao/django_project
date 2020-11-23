
def device_sql(agent_phone, business_phone, device_id, device_one, staff_name):
    sql = '''
    SELECT
        ox.`所在仓库`,ox.`仓库状态`,IF(ox.`门店编号` IS NULL,'未部署','已部署') AS '是否部署',
        ox.`设备编号`,ox.`设备状态`,ox.`设备类型`,IF(ox.`BD编号` IS NULL,CONCAT(s.`name`,'(代理)'),CONCAT(ss.staff_name,'(BD)')) AS '当前设备持有人',
        IF(ox.`BD编号` IS NULL,s.phone,ss.phonenum) AS '设备持有人联系方式',
        osi.store_name AS '门店名称',osi.store_address AS '门店地址',osi.store_phone AS '门店联系方式',s1.phone AS '商户登录号码',obi.business_name AS '商户名称'
    FROM
        (SELECT
            bsdr.device_id AS '设备编号',IF(bsdr.del_flag = 0,CASE bsdr.device_type WHEN 6 THEN '6口机' WHEN 12 THEN '12口机' WHEN 'POWER_BANK' THEN '充电宝' END,'未入库或已删除') AS '设备类型',
            odr.bd_id AS 'BD编号',odr.agent_id AS '代理编号',odd.store_id AS '门店编号',CASE box.state WHEN 0 THEN '离线' WHEN 1 THEN '在线' ELSE NULL END AS '设备状态',
            CASE bsdr.storage_state WHEN 0 THEN '未分配' WHEN 1 THEN '分配中' WHEN 2 THEN '已分配' WHEN 3 THEN '已遗失' WHEN 4 THEN '设备异常' END AS '仓库状态',
            IF(bsdr.storage_state = 0,bsi.storage_name,NULL) AS '所在仓库'
    FROM
    ch_box box
    INNER JOIN bms_storage_device_relation bsdr ON box.id = bsdr.device_id AND bsdr.del_flag = 0
    LEFT JOIN ocms_device_relations odr ON odr.device_id = bsdr.device_id AND odr.del_flag = 0
    LEFT JOIN ocms_device_deploy odd ON odd.device_id = odr.device_id AND odd.del_flag = 0
    LEFT JOIN bms_storage_info bsi ON bsi.storage_id = bsdr.storage_id
    GROUP BY
    bsdr.device_id
    )ox
-- 设备持有人
    LEFT JOIN ocms_bd_info obd ON obd.bd_id = ox.`BD编号`
    LEFT JOIN sys_staff ss ON ss.staff_id = obd.staff_id
    LEFT JOIN ocms_agent_info oai ON oai.agent_id = ox.`代理编号`
    LEFT JOIN sys_user s ON s.user_id = oai.user_id
    -- 门店的信息
    LEFT JOIN ocms_store_info osi ON osi.store_id = ox.`门店编号`
    LEFT JOIN ocms_store_business osb ON osb.store_id = osi.store_id AND osb.del_flag = 0
    LEFT JOIN ocms_business_info obi ON obi.business_id = osb.business_id
    LEFT JOIN sys_user s1 ON s1.user_id = obi.user_id
    WHERE
        s.phone = '%s'
        OR s1.phone = '%s'
        OR ox.`设备编号` IN (%s)
        OR ox.`设备编号` = '%s'
        OR ss.staff_name = '%s';
    ''' % (agent_phone, business_phone, device_id, device_one, staff_name)
    return sql


def device_bd_6_sum():
    sql = '''
    SELECT count(odr.device_id) '直营领取6孔设备数量' FROM ocms_device_relations odr
    LEFT JOIN bms_storage_device_relation bsdr on bsdr.device_id = odr.device_id
    WHERE odr.del_flag = 0
    AND bsdr.del_flag = 0
    AND bsdr.device_type = 6
    AND odr.bd_id is not null;
    '''
    return sql


def device_bd_12_sum():
    sql = '''
    SELECT count(odr.device_id) '直营领取12孔设备数量' FROM ocms_device_relations odr
    LEFT JOIN bms_storage_device_relation bsdr on bsdr.device_id = odr.device_id
    WHERE odr.del_flag = 0
    AND bsdr.del_flag = 0
    AND bsdr.device_type = 12
    AND odr.bd_id is not null;
    '''
    return sql


def device_agent_6_sum():
    sql = '''
    SELECT count(odr.device_id) '代理领取6孔设备数量' FROM ocms_device_relations odr
    LEFT JOIN bms_storage_device_relation bsdr on bsdr.device_id = odr.device_id
    WHERE odr.del_flag = 0
    AND bsdr.del_flag = 0
    AND bsdr.device_type = 6
    AND odr.agent_id is not null;
    '''
    return sql


def device_agent_12_sum():
    sql = '''
    SELECT count(odr.device_id) '代理领取12孔设备数量' FROM ocms_device_relations odr
    LEFT JOIN bms_storage_device_relation bsdr on bsdr.device_id = odr.device_id
    WHERE odr.del_flag = 0
    AND bsdr.del_flag = 0
    AND bsdr.device_type = 12
    AND odr.agent_id is not null;
    '''
    return sql


def device_storage_6_sum():
    sql = '''
    SELECT count(bsdr.device_id) '库存6孔设备数量' FROM bms_storage_device_relation bsdr
    INNER JOIN ch_box cb on cb.id = bsdr.device_id
    WHERE bsdr.del_flag = 0
    AND bsdr.device_type = 6
    AND bsdr.storage_state = 0
    AND bsdr.storage_id not in (13,14);
    '''
    return sql


def device_storage_12_sum():
    sql = '''
    SELECT count(bsdr.device_id) '库存12孔设备数量' FROM bms_storage_device_relation bsdr
    INNER JOIN ch_box cb on cb.id = bsdr.device_id
    WHERE bsdr.del_flag = 0
    AND bsdr.device_type = 12
    AND bsdr.storage_state = 0
    AND bsdr.storage_id not in (13,14);
    '''
    return sql


def agent_up(agent_phone):
    sql = '''
    SELECT 
    su.`name`,
    su.account,
    CASE oai.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su1.`name`,
    su1.account,
    CASE oai1.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su2.`name`,
    su2.account,
    CASE oai2.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su3.`name`,
    su3.account,
    CASE oai3.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END
    FROM ocms_agent_info oai
    LEFT JOIN sys_user su on su.user_id = oai.user_id
    LEFT JOIN ocms_agent_info oai1 on oai1.agent_id = oai.parentid
    LEFT JOIN sys_user su1 on su1.user_id = oai1.user_id
    LEFT JOIN ocms_agent_info oai2 on oai2.agent_id = oai1.parentid
    LEFT JOIN sys_user su2 on su2.user_id = oai2.user_id
    LEFT JOIN ocms_agent_info oai3 on oai3.agent_id = oai2.parentid
    LEFT JOIN sys_user su3 on su3.user_id = oai3.user_id
    WHERE su.account = '%s'
    AND su.del_flag = 0;
    ''' % agent_phone
    return sql


def agent_down(agent_phone):
    sql = '''
    SELECT 
    su.`name`,
    su.account,
    CASE oai.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su1.`name`,
    su1.account,
    CASE oai1.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su2.`name`,
    su2.account,
    CASE oai2.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END,
    su3.`name`,
    su3.account,
    CASE oai3.agent_level
        WHEN 1 THEN
            '总代'
        WHEN 2 THEN
          '一代'
        WHEN 3 THEN
            '二代'
        WHEN 4 THEN
            '三代'
    END
    FROM ocms_agent_info oai
    LEFT JOIN sys_user su on su.user_id = oai.user_id
    LEFT JOIN ocms_agent_info oai1 on oai1.parentid = oai.agent_id
    LEFT JOIN sys_user su1 on su1.user_id = oai1.user_id
    LEFT JOIN ocms_agent_info oai2 on oai2.parentid = oai1.agent_id
    LEFT JOIN sys_user su2 on su2.user_id = oai2.user_id
    LEFT JOIN ocms_agent_info oai3 on oai3.parentid = oai2.agent_id
    LEFT JOIN sys_user su3 on su3.user_id = oai3.user_id
    WHERE su.account = '%s'
    AND su.del_flag = 0;
    ''' % agent_phone
    return sql
