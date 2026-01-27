# 🔥 AWS BEDROCK SETUP - GET REAL AI WORKING! 🔥

## Current Status

✅ **Backend:** Running on port 8734  
✅ **Frontend:** Running on port 3847  
⚠️  **AI:** Currently in MOCK MODE (needs AWS credentials)  

## Why Mock Mode?

The backend needs AWS Bedrock credentials to make real AI calls. Without valid credentials, it returns mock data so you can still test the UI.

---

## 🚀 OPTION 1: Quick Manual Setup (5 minutes)

### Step 1: Get AWS Credentials

If you already have AWS credentials with Bedrock access:

1. Copy them to `backend/.env`:
```bash
AWS_ACCESS_KEY_ID=your_actual_key
AWS_SECRET_ACCESS_KEY=your_actual_secret
AWS_REGION=us-east-1
```

### Step 2: Enable Bedrock Model Access

1. Go to: https://console.aws.amazon.com/bedrock
2. Click "Model Access" in left sidebar
3. Click "Manage model access"
4. Find and enable **DeepSeek** models (or Claude, Llama, etc.)
5. Click "Save changes"
6. Wait for approval (usually instant)

### Step 3: Restart Backend

```bash
cd backend
kill $(cat backend.pid)
source venv/bin/activate
python -m uvicorn api.app:app --host 0.0.0.0 --port 8734 &
```

**DONE!** Now upload a paper and see REAL AI analysis! 🎉

---

## 🤖 OPTION 2: Automated Terraform Setup (10 minutes)

This creates everything for you: IAM user, permissions, access keys.

### Prerequisites

```bash
# Install Terraform
brew install terraform

# Configure AWS CLI with admin access
aws configure
```

### Run the Setup Script

```bash
cd /Users/jakubbares/Science/New/paper-analyzer
./setup-aws-bedrock.sh
```

This script will:
1. ✅ Initialize Terraform
2. ✅ Create IAM user with Bedrock permissions
3. ✅ Generate access keys
4. ✅ Update `backend/.env` automatically
5. ✅ Show you next steps

### After Terraform

You still need to enable model access in AWS Console:

1. Go to: https://console.aws.amazon.com/bedrock
2. Enable DeepSeek models
3. Restart backend

---

## 🔧 Manual Terraform (if script fails)

```bash
cd terraform

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Get credentials
terraform output bedrock_access_key_id
terraform output -raw bedrock_secret_access_key

# Copy to backend/.env
```

---

## 🧪 Test It's Working

### 1. Check Backend Status

```bash
curl http://localhost:8734/health
```

Should return:
```json
{"status":"healthy","llm":"AWS Bedrock - deepseek-ai.deepseek-v3"}
```

### 2. Upload a Paper

1. Go to: http://localhost:3847
2. Upload a PDF
3. Click "Extract Contributions"
4. Wait 30-60 seconds

### 3. Check for Real Data

If you see:
- ✅ **Real contributions** with actual paper details → **WORKING!**
- ⚠️  **Mock data** with "MOCK" in titles → Still in mock mode

---

## 🐛 Troubleshooting

### Issue: "Access Denied" Error

**Solution:**
1. Enable model access in AWS Console (see Step 2 above)
2. Wait a few minutes after requesting access
3. Restart backend

### Issue: "Model Not Found"

**Solution:** DeepSeek might not be available in your region. Try:

1. Edit `backend/.env`:
```bash
# Try Claude instead
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

2. Or use Llama:
```bash
BEDROCK_MODEL_ID=meta.llama3-70b-instruct-v1:0
```

3. Or check available models:
```bash
aws bedrock list-foundation-models --region us-east-1
```

### Issue: Still Getting Mock Responses

**Check backend log:**
```bash
cd backend
tail -50 backend.log
```

Look for:
- ❌ "Access Denied" → Enable model access
- ❌ "Model not found" → Wrong model ID
- ❌ "Invalid credentials" → Wrong AWS keys

### Issue: "Region not supported"

**Try different region:**
```bash
# In backend/.env
AWS_REGION=us-west-2  # or us-east-1, eu-west-1
```

---

## 💰 Cost

AWS Bedrock pricing (DeepSeek):
- **Input:** ~$0.001 per 1K tokens
- **Output:** ~$0.003 per 1K tokens

**Per paper:** ~$0.02  
**100 papers:** ~$2.00  
**Cached results:** FREE (instant)

---

## 🎯 Quick Commands

```bash
# Check if backend is using real AI
curl http://localhost:8734/health

# View backend logs
tail -f backend/backend.log

# Restart backend
cd backend
kill $(cat backend.pid)
source venv/bin/activate
python -m uvicorn api.app:app --host 0.0.0.0 --port 8734 &

# Check AWS model access
aws bedrock list-foundation-models --region us-east-1

# Run Terraform
cd terraform && terraform apply
```

---

## 📚 Files Created

✅ `terraform/main.tf` - Infrastructure as code  
✅ `terraform/terraform.tfvars` - Variables  
✅ `terraform/README.md` - Terraform docs  
✅ `setup-aws-bedrock.sh` - Automated setup script  
✅ `backend/extractors/llm_client.py` - Fixed with real Bedrock API  
✅ `.cursorrules` - Project configuration  

---

## ✅ Verification Checklist

- [ ] AWS credentials in `backend/.env`
- [ ] Model access enabled in AWS Console
- [ ] Backend restarted
- [ ] Upload test paper
- [ ] Extract contributions
- [ ] Verify REAL data (not "MOCK")

---

## 🎉 Once Working

You'll see:
- ✅ Real technical contributions extracted
- ✅ Actual problem-solution pairs
- ✅ Evidence locations from the paper
- ✅ Proper categorization
- ✅ ~30-60 second processing time
- ✅ Results cached for instant re-access

---

**NOW GO SET IT UP AND GET REAL AI WORKING!** 🚀

Run: `./setup-aws-bedrock.sh` or follow Option 1 for manual setup.


