# 🚀 Deploy Slang Translator on Render (FREE!)

## 📋 Prerequisites
- GitHub account
- Render account (free at render.com)
- Your code pushed to GitHub

## 🎯 Step-by-Step Deployment

### 1. Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
# Go to github.com → New Repository → Create
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/slang-translator.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

1. **Go to:** https://render.com
2. **Sign up/Login** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repo**
5. **Configure the service:**

   **Basic Settings:**
   - **Name:** `slang-translator` (or any name you like)
   - **Environment:** `Python 3`
   - **Region:** `Oregon (US West)` (closest to you)
   - **Branch:** `main`

   **Build & Deploy:**
   - **Root Directory:** `web_app`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

   **Environment Variables:**
   - **Key:** `HUGGINGFACE_HUB_TOKEN`
   - **Value:** `f_dHMvtQsUlDqCIBaWCSJfpgcsVwnVArbdQw`

6. **Click "Create Web Service"**

### 3. Wait for Deployment
- First deployment takes 10-15 minutes (downloading 13GB model)
- You'll see logs in real-time
- Your app will be live at: `https://your-app-name.onrender.com`

## ⚠️ Important Notes

### Free Tier Limitations:
- **512MB RAM** - May cause issues with Mistral 7B
- **Sleeps after 15 minutes** of inactivity
- **Cold starts** take 30-60 seconds

### If Mistral 7B Fails:
The app will automatically fallback to a smaller model (DialoGPT-medium) which works better on free tier.

## 🔧 Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check that `web_app/` is set as root directory
   - Verify `requirements.txt` exists

2. **Model loading fails:**
   - Check Hugging Face token is set correctly
   - App will use fallback model

3. **Memory issues:**
   - Free tier has limited RAM
   - Consider upgrading to paid plan for better performance

4. **Slow responses:**
   - First request after sleep takes longer
   - This is normal for free tier

## 🚀 Alternative: Use Smaller Model

If you want faster deployment, modify `app.py` to use only the smaller model:

```python
# Replace the model loading with:
model_pipeline = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium",
    device=-1,
    max_length=256,
    do_sample=True,
    temperature=0.7,
)
```

## 📊 Monitoring

- **Render Dashboard:** Monitor logs and performance
- **Health Check:** Visit `https://your-app.onrender.com/health`
- **Logs:** Available in Render dashboard

## 💰 Cost

- **Free Tier:** $0/month
- **Paid Plans:** Start at $7/month for better performance

## 🎉 Success!

Once deployed, your Slang Translator will be live at:
`https://your-app-name.onrender.com`

Share this URL with anyone to use your translation service!

## 🔄 Updates

To update your app:
1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically redeploys

## 📱 Mobile Friendly

The web app is fully responsive and works on:
- Desktop browsers
- Mobile phones
- Tablets

## 🆘 Need Help?

- **Render Docs:** https://render.com/docs
- **Support:** Available in Render dashboard
- **Community:** Render Discord/Forum
