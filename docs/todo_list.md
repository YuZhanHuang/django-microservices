## 待辦事項
- 目前各微服務對於資料的初始化尚未完善，寫在`core/management/commands`，最好可以不相之前monolith專案的初始化資料
- 可以考慮環境變數的管理方法e.g. `django-envron`
- 關於套件版版的管理方式目前是用傳統的`pip install`，可以考慮以`poetry`的管理
- 錯誤處理與日誌
- 還需要有搭配的`ELK`計畫