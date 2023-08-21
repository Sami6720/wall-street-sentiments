# Wall Street Sentiments Backend
This repository contains the backend for [Wall Street Sentiments](https://wall-street-sentiments-front-end.vercel.app/dashboard). It's a web app designed to predict the price direction of today's most discussed stocks on Reddit. This prediction is powered by a combination of fundamental stock information and data from Reddit on those stocks. This also includes sentiment data.

## 🛠 Tech stack
The backend is built in Python with AWS providing the cloud infrastructure.
#### More details
- Data Lake: S3
- ETL Components: AWS Lambda
- Orchestration: AWS Step Functions
- Database: MongoDB
- Continuous Deployment: GitHub Actions
- REST API: API Gateway
- Image Repository: AWS ECR

## ETL Architecture
![image](https://github.com/Sami6720/wall-street-sentiments/assets/78088136/8b5276e6-c467-44af-9484-b0942967d4f6)
