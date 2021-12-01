# django-microservices
> 拆分服務與k8s部署練習，
> 此專案的拓墣圖在docs中

## 部署在 Google Kubernetes Engine

### 先部署MySQL的服務(GCP提供的服務 SQL)
#### 創建以下instance(執行個體)
* 執行個體`users-db`，創建資料庫`users`
* 執行個體`ambassador-db`，創建資料庫`ambassador`
* 執行個體`admin-db`，創建資料庫`admin`
* 執行個體`checkout-db`，創建資料庫`checkout`

### 敏感資訊的處理
#### 敏感資料放在k8s的secret中
* **kafka-secrets**:
  - `BOOTSTRAP_SERVICE`: 
  - `SECURITY_PROTOCOL`:
  - `SASL_USERNAME`: 
  - `SASL_PASSWORD`: 
  - `SASL_MECHANISMS`: 
  - `GROUP_ID`:
* **mail-secrets**: 
  - `EMAIL_HOST`:
  - `EMAIL_PORT`:
  - `EMAIL_USERNAME`:
  - `EMAIL_PASSWORD`:
* **mysql-secrets**:
  - TODO，還沒有做，目前直接寫在環境變數
  - `DB_HOST`:
  - `DB_PASSWORD`:
  - `DB_PORT`:
  - `DB_USERNAME`:
* **STRIPE_KEY**
  - TODO，還沒有做，目前直接寫在環境變數
  - `STRIPE_KEY`:
#### 創建secrets的命令
> Usage:
  kubectl create secret generic NAME [--type=string] [--from-file=[key=]source] [--from-literal=key1=value1]
[--dry-run=server|client|none] [options]
* `kubectl create secret generic kafka-secrets --from-literal=key1=value1`

### 利用k8s部署服務
#### 確認各個yaml配置
#### 在kubernetes資料夾
* `kubectl apply -f .`