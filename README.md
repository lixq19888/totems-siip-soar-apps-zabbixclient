## 安博通 http://www.abtnetworks.com/http://www.abtnetworks.com/
## 概述

zabbix连接工具，用来访问zabbix api

## 使用说明

zabbix工具在平台上能正常执行的前置条件如下：  

1、配置zabbix实例，用于连接部署zabbix的服务器地址；

2、配置动作参数，用于设置应用动作的输入；  

## 配置实例
| **参数** |  **参数别名** | **描述** | **必填** | **示例** |
| --- | --- | --- | --- |  --- |
| url | 服务器地址 | 部署了zabbix的服务器地址 | 是 | http://192.168.215.174:10086 |
| user | 用户名 | zabbix登录用户名 | 是 | Admin |
| password | 密码 | zabbix登录密码 | 是 | zabbix |

## 配置动作
### 1.获取所有监控主机

该动作主要用于获取zabbix服务器上监控的所有主机

#### 参数
| **参数** | **参数别名** | **描述** | **必填** | **示例** |
| --- | --- | --- | --- |  --- |
| host_ip | 主机IP | 待查询主机IP | 否 | 192.168.1.2 |


#### 返回示例

```json
{
	"message": "success",
	"data": [
		{
			"hostid": "10084",
			"proxy_hostid": "0",
			"host": "Zabbix server",
			"status": "0",
			"disable_until": "0",
			"error": "",
			"available": "1",
			"errors_from": "0",
			"lastaccess": "0",
			"ipmi_authtype": "-1",
			"ipmi_privilege": "2",
			"ipmi_username": "",
			"ipmi_password": "",
			"ipmi_disable_until": "0",
			"ipmi_available": "0",
			"snmp_disable_until": "0",
			"snmp_available": "0",
			"maintenanceid": "0",
			"maintenance_status": "0",
			"maintenance_type": "0",
			"maintenance_from": "0",
			"ipmi_errors_from": "0",
			"snmp_errors_from": "0",
			"ipmi_error": "",
			"snmp_error": "",
			"jmx_disable_until": "0",
			"jmx_available": "0",
			"jmx_errors_from": "0",
			"jmx_error": "",
			"name": "Zabbix server",
			"flags": "0",
			"templateid": "0",
			"description": "",
			"tls_connect": "1",
			"tls_accept": "1",
			"tls_issuer": "",
			"tls_subject": "",
			"tls_psk_identity": "",
			"tls_psk": "",
			"proxy_address": "",
			"auto_compress": "1",
			"inventory_mode": "-1"
		},
		{
			"hostid": "10432",
			"proxy_hostid": "0",
			"host": "agent10.215.7.17",
			"status": "0",
			"disable_until": "0",
			"error": "",
			"available": "1",
			"errors_from": "0",
			"lastaccess": "0",
			"ipmi_authtype": "-1",
			"ipmi_privilege": "2",
			"ipmi_username": "",
			"ipmi_password": "",
			"ipmi_disable_until": "0",
			"ipmi_available": "0",
			"snmp_disable_until": "0",
			"snmp_available": "0",
			"maintenanceid": "0",
			"maintenance_status": "0",
			"maintenance_type": "0",
			"maintenance_from": "0",
			"ipmi_errors_from": "0",
			"snmp_errors_from": "0",
			"ipmi_error": "",
			"snmp_error": "",
			"jmx_disable_until": "0",
			"jmx_available": "0",
			"jmx_errors_from": "0",
			"jmx_error": "",
			"name": "agent10.215.7.17",
			"flags": "0",
			"templateid": "0",
			"description": "",
			"tls_connect": "1",
			"tls_accept": "1",
			"tls_issuer": "",
			"tls_subject": "",
			"tls_psk_identity": "",
			"tls_psk": "",
			"proxy_address": "",
			"auto_compress": "1",
			"inventory_mode": "-1"
		},
		{
			"hostid": "10433",
			"proxy_hostid": "0",
			"host": "agent192.168.218.115",
			"status": "0",
			"disable_until": "1640853907",
			"error": "Get value from agent failed: cannot connect to [[192.168.218.115]:10050]: [111] Connection refused",
			"available": "2",
			"errors_from": "1639737976",
			"lastaccess": "0",
			"ipmi_authtype": "-1",
			"ipmi_privilege": "2",
			"ipmi_username": "",
			"ipmi_password": "",
			"ipmi_disable_until": "0",
			"ipmi_available": "0",
			"snmp_disable_until": "0",
			"snmp_available": "0",
			"maintenanceid": "0",
			"maintenance_status": "0",
			"maintenance_type": "0",
			"maintenance_from": "0",
			"ipmi_errors_from": "0",
			"snmp_errors_from": "0",
			"ipmi_error": "",
			"snmp_error": "",
			"jmx_disable_until": "0",
			"jmx_available": "0",
			"jmx_errors_from": "0",
			"jmx_error": "",
			"name": "agent192.168.218.115",
			"flags": "0",
			"templateid": "0",
			"description": "",
			"tls_connect": "1",
			"tls_accept": "1",
			"tls_issuer": "",
			"tls_subject": "",
			"tls_psk_identity": "",
			"tls_psk": "",
			"proxy_address": "",
			"auto_compress": "1",
			"inventory_mode": "-1"
		}
	],
	"schema": {
		"type": "JSON_ARRAY"
	},
	"status": "Success"
}
```


### 2.获取zabbix主机异常信息

获取zabbix监管主机的异常信息

#### 参数
| **参数** | **参数别名** | **描述** | **必填** | **示例** |
| --- | --- | --- | --- |  --- |
| host_ip | 主机IP | 待查询主机IP | 否 | 192.168.1.2 |

#### 返回示例
```json
{
	"message": "success",
	"data": [
		{
			"triggerid": "19791",
			"expression": "{23704} > {$VFS.DEV.READ.AWAIT.WARN:\"sda\"} or {23705} > {$VFS.DEV.WRITE.AWAIT.WARN:\"sda\"}",
			"description": "sda: Disk read/write request responses are too high (read > 20 ms for 15m or write > 20 ms for 15m)",
			"url": "",
			"status": "0",
			"value": "1",
			"priority": "2",
			"lastchange": "1639736627",
			"comments": "This trigger might indicate disk sda saturation.",
			"error": "",
			"templateid": "0",
			"type": "0",
			"state": "0",
			"flags": "4",
			"recovery_mode": "0",
			"recovery_expression": "",
			"correlation_mode": "0",
			"correlation_tag": "",
			"manual_close": "1",
			"opdata": "",
			"hosts": [
				{
					"hostid": "10432",
					"host": "agent10.215.7.17"
				}
			],
			"unacknowledged": true
		},
		{
			"triggerid": "19761",
			"expression": "{23621}=0",
			"description": "Zabbix agent is not available (for 3m)",
			"url": "",
			"status": "0",
			"value": "1",
			"priority": "3",
			"lastchange": "1639738175",
			"comments": "For passive only agents, host availability is used with {$AGENT.TIMEOUT} as time threshold.",
			"error": "",
			"templateid": "16206",
			"type": "0",
			"state": "0",
			"flags": "0",
			"recovery_mode": "0",
			"recovery_expression": "",
			"correlation_mode": "0",
			"correlation_tag": "",
			"manual_close": "1",
			"opdata": "",
			"hosts": [
				{
					"hostid": "10433",
					"host": "agent192.168.218.115"
				}
			],
			"unacknowledged": true
		},
		{
			"triggerid": "19734",
			"expression": "{23574}=0",
			"description": "System time is out of sync (diff with Zabbix server > 60s)",
			"url": "",
			"status": "0",
			"value": "1",
			"priority": "2",
			"lastchange": "1640149944",
			"comments": "The host system time is different from the Zabbix server time.",
			"error": "",
			"templateid": "16055",
			"type": "0",
			"state": "0",
			"flags": "0",
			"recovery_mode": "0",
			"recovery_expression": "",
			"correlation_mode": "0",
			"correlation_tag": "",
			"manual_close": "1",
			"opdata": "",
			"hosts": [
				{
					"hostid": "10432",
					"host": "agent10.215.7.17"
				}
			],
			"unacknowledged": true
		}
	],
	"schema": {
		"type": "JSON_ARRAY"
	},
	"debugOutput": "",
	"status": "Success"
}
```

