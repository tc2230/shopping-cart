
# 購物車功能實做

## 概述

購物車後端功能實做，搭配 docker 及 pytest 做測試及佈署。

## 環境準備

1. **Docker 和 Docker Compose:** 確認系統裡有安裝 Docker 和 Docker Compose。如果沒有，推薦直接安裝 Docker Desktop：
    - macOS： [Docker Desktop on Mac 官方安裝檔下載](https://docs.docker.com/desktop/install/mac-install/)
    - Windows： [Docker Desktop on Windows 官方安裝檔下載](https://docs.docker.com/desktop/install/windows-install/)

2. **安裝完成後，啟動 Docker Desktop，可於介面左下角確認 Docker Engine 正常執行。如下圖：**
    ![image](https://github.com/user-attachments/assets/67ea61fc-8d75-43c9-bab7-3a6ccb0ea3ea)

## 部署

1. **clone這個專案**
   ```bash
   git clone git@github.com:tc2230/shopping-cart.git;
   cd shopping-cart
   ```

2. **建立映像並執行主程式:** 切換到專案目錄，並執行以下命令來建立Image和啟動測試：
   ```bash
   docker compose up
   ```
    Docker compose 會自動建立image、啟動container和執行測試。

3. **確認測試結果:**：
   若無異常應可見測試結果如下圖，包含case_A, case_B, 及其他小功能測試
   ![image]([https://github.com/user-attachments/assets/67ea61fc-8d75-43c9-bab7-3a6ccb0ea3ea](https://github.com/user-attachments/assets/9002ed4d-9dc2-4e10-bd53-6bf4c7f04938))
