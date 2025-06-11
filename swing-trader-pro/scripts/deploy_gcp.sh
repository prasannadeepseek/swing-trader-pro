#!/bin/bash
# scripts/deploy_gcp.sh

# Set environment variables
export PROJECT_ID="your-project-id"
export SERVICE_ACCOUNT="swing-trader@${PROJECT_ID}.iam.gserviceaccount.com"

# Enable required services
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    scheduler.googleapis.com \
    pubsub.googleapis.com

# Build and deploy container
gcloud builds submit --tag gcr.io/$PROJECT_ID/swing-trader

# Deploy to Cloud Run
gcloud run deploy swing-trader \
    --image gcr.io/$PROJECT_ID/swing-trader \
    --platform managed \
    --region us-central1 \
    --memory 2Gi \
    --service-account $SERVICE_ACCOUNT \
    --set-env-vars "ENVIRONMENT=production"

# Setup scheduled jobs
gcloud scheduler jobs create pubsub market-open \
    --schedule "0 8 * * 1-5" \
    --topic market-events \
    --message-body "market_open" \
    --time-zone "Asia/Kolkata"

gcloud scheduler jobs create pubsub market-close \
    --schedule "0 15 * * 1-5" \
    --topic market-events \
    --message-body "market_close" \
    --time-zone "Asia/Kolkata"