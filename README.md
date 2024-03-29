# Wall Street Sentiments Backend
This repository contains the backend for [Wall Street Sentiments](https://wall-street-sentiments-front-end.vercel.app/dashboard). It's a web app designed to predict the price direction of today's most discussed stocks on Reddit. This prediction is powered by a combination of fundamental stock information and data from Reddit on those stocks. This also includes sentiment data.

## 🛠️ Tech stack
The backend is built in Python with AWS providing the cloud infrastructure.

#### More details
- Data Lake: S3
- ETL Components: AWS Lambda
- Orchestration: AWS Step Functions
- Database: MongoDB
- Continuous Deployment: GitHub Actions
- REST API: API Gateway
- Image Repository: AWS ECR

## 📁 Folders and Branches
- The `workflows` folder contains code for the ETL components.
- The `api_lambdas` folder contains code for the REST API lambdas.
- The [`dev-experiments-data-science`](https://github.com/Sami6720/wall-street-sentiments/tree/dev-experiments-data-science) branch contains all the experimentation and exploratory notebooks.

## 📐 ETL Architecture
![image](https://github.com/Sami6720/wall-street-sentiments/assets/78088136/8b5276e6-c467-44af-9484-b0942967d4f6)


## ☁️ Cloud Architecture
![wss-backend-architecture (5)](https://github.com/Sami6720/wall-street-sentiments/assets/78088136/6846d182-2a83-4215-90f7-8beab10069be)
