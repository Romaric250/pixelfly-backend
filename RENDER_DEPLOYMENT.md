# PixelFly Backend - Render Deployment Guide

This guide will help you deploy the PixelFly Flask backend to Render.

## Prerequisites

1. A Render account (sign up at [render.com](https://render.com))
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Google API key for AI features (optional but recommended)

## Quick Deployment Steps

### 1. Connect Your Repository

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your Git repository containing this code
4. Select the repository and branch

### 2. Configure the Service

Use these settings in the Render dashboard:

- **Name**: `pixelfly-backend` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --config gunicorn.conf.py wsgi:application`
- **Plan**: `Starter` (or higher for production)

### 3. Set Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
- `FLASK_ENV`: `production`
- `PORT`: `10000` (Render will set this automatically)
- `PYTHONPATH`: `.`

**Recommended:**
- `GOOGLE_API_KEY`: Your Google AI API key
- `SECRET_KEY`: A secure random string
- `LOG_LEVEL`: `INFO`

**Optional:**
- `MAX_WORKERS`: `2`
- `WORKER_TIMEOUT`: `60`
- `FRONTEND_URL`: Your frontend domain for CORS

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues

## Configuration Files

This repository includes several files optimized for Render deployment:

- `render.yaml`: Render service configuration
- `gunicorn.conf.py`: Production WSGI server configuration
- `wsgi.py`: Application entry point with fallback imports
- `requirements.txt`: Python dependencies
- `.env.example`: Environment variable template
- `start.sh`: Optional startup script

## Health Check

The application includes a health check endpoint at `/health` that Render will use to monitor your service.

## Scaling and Performance

The configuration is optimized for Render's environment:

- **Workers**: Limited to 2 for memory efficiency
- **Timeout**: 60 seconds for image processing
- **Memory**: Optimized for Starter plan limits
- **Restart**: Workers restart every 300 requests to prevent memory leaks

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies in `requirements.txt` are compatible
   - Verify Python version compatibility

2. **Import Errors**
   - The `wsgi.py` file includes fallback imports for different app structures
   - Check that your main application file is properly structured

3. **Memory Issues**
   - Consider upgrading to a higher Render plan
   - Reduce `MAX_WORKERS` if needed
   - Monitor memory usage in Render dashboard

4. **Timeout Issues**
   - Increase `WORKER_TIMEOUT` for heavy image processing
   - Consider async processing for large batches

### Logs

Monitor your application logs in the Render dashboard:
- Build logs show dependency installation
- Runtime logs show application startup and requests
- Error logs help debug issues

## Environment Variables Reference

See `.env.example` for a complete list of available environment variables.

## Support

For Render-specific issues, check:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)

For application issues, check the application logs and ensure all required environment variables are set.
