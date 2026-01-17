# Terraform AWS Bedrock Setup

This Terraform configuration sets up AWS Bedrock access with proper IAM roles and permissions.

## Prerequisites

1. **Install Terraform**
   ```bash
   brew install terraform  # macOS
   ```

2. **AWS CLI configured with admin access**
   ```bash
   aws configure
   ```

## Usage

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

### 2. Review the plan
```bash
terraform plan
```

### 3. Apply the configuration
```bash
terraform apply
```

### 4. Get the credentials
```bash
# Get Access Key ID (already shown in output)
terraform output bedrock_access_key_id

# Get Secret Access Key (sensitive)
terraform output -raw bedrock_secret_access_key
```

### 5. Update backend/.env
Copy the credentials to `backend/.env`:
```bash
AWS_ACCESS_KEY_ID=<from terraform output>
AWS_SECRET_ACCESS_KEY=<from terraform output>
AWS_REGION=us-east-1
```

### 6. Enable Bedrock Model Access

1. Go to AWS Console: https://console.aws.amazon.com/bedrock
2. Click "Model Access" in left sidebar
3. Click "Manage model access"
4. Find and enable:
   - DeepSeek models
   - Or other models you want to use
5. Click "Save changes"
6. Wait for approval (usually instant)

### 7. Restart Backend
```bash
cd ../backend
# Kill old backend
kill $(cat backend.pid)
# Start new backend
source venv/bin/activate
python -m uvicorn api.app:app --host 0.0.0.0 --port 8734 &
```

## What This Creates

- **IAM Role**: `paper-analyzer-bedrock-role` with Bedrock permissions
- **IAM User**: `paper-analyzer-bedrock-user` for programmatic access
- **IAM Policy**: Full Bedrock model invocation permissions
- **Access Keys**: Credentials for the backend to use

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

## Troubleshooting

### "Access Denied" errors
- Ensure you've requested model access in AWS Console
- Wait a few minutes after requesting access
- Check IAM user has the correct policy attached

### "Model not found"
- Verify DeepSeek model is available in your region
- Try different region (us-west-2, us-east-1)
- Check model ID matches: `deepseek-ai.deepseek-v3`

## Cost

AWS Bedrock pricing (DeepSeek):
- Input: ~$0.001 per 1K tokens
- Output: ~$0.003 per 1K tokens
- Per paper: ~$0.02
- Monthly (100 papers): ~$2

IAM resources are free.
