# Kustomize
이 문서는 Kustomize 를 통한 배포에 대해 설명하고 있다.

# MariaDB 배포
아래 명령을 통해 MariaDB 를 배포한다.
```bash
kubectl create ns monitoring
kustomize build overlay/mariadb/ | kubectl create -f -
```

## TABLE 생성
아래와 같이 Pod 내 SHELL 을 통해 TABLE 을 생성한다.    

```bash
root@mariadb-7dfb55d496-dr9rl:/# mysql -umariadb -p mariadb
Enter password: *******
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 10.9.2-MariaDB-1:10.9.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mariadb]> CREATE TABLE rss(
    ->     rss_date DATE,
    ->     rss_title VARCHAR(200) NOT NULL,
    ->     rss_url VARCHAR(200) NOT NULL,
    ->     send TINYINT,
    ->     PRIMARY KEY ( rss_date )
    -> );
Query OK, 0 rows affected (0.016 sec)

MariaDB [mariadb]> exit
Bye
```
   
# Rocky Linux Version Checker 배포
아래 명령을 통해 Rlchecker 를 배포한다.   
```bash
kustomize build overlay/rlchecker/ | kubectl create -f - 
```
   
# 환경 변수 설명
Rlchecker 에서 사용되는 환경 변수에는 아래와 같다.     
   
## MariaDB
* `overlay/mariadb/kustomization.yaml`   
MariaDB secret 변경시,   
```console
...
secretGenerator:
- name: mariadb-secrets
  literals:
    - MARIADB_DATABASE=mariadb		<< DATABASE NAME
    - MARIADB_USER=mariadb		<< DATABASE USER
    - MARIADB_PASSWORD=mariadb		<< DATABASE PASSWORD
    - MARIADB_ROOT_PASSWORD=mariadb	<< DATABASE ROOT PASSWORD
...
```
    
* `mariadb/mariadb-patch.json`   
StorageClass 변경시,   
```console
[
    {
        "op": "replace",
        "path": "/spec/storageClassName",
        "value": "local-path"				<< StorageClass
    }
]
```
   
## Rlchecker
* `overlay/rlchecker/kustomization.yml`   
Rlchecker secret 변경시,   
```console
...
secretGenerator:
- name: rlchecker-secrets
  literals:
    - DB_DATABASE=mariadb		<< DATABASE NAME
    - DB_USER=mariadb			<< DATABASE USER
    - DB_PASS=mariadb			<< DATABASE PASSWORD
    - DB_HOST=mariadb			<< DATABASE SERVICE NAME
    - SLACK_WEBHOOK=<slack-webhook>	<< SLACK Webhook URL
    - SLACK_CHANNEL=<slack-channel>	<< SLACK Channel NAME
...
```
   
* `overlay/rlchecker/rlchecker-patch.json`    
Image tag 변경시,   
```console
[
    {
        "op": "replace",
        "path": " /spec/jobTemplate/spec/template/spec/containers/0/image",
        "value": "docker-registry:5001/rockylinux-version-checker"
    }
]
```
