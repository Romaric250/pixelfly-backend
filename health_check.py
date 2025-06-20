#!/usr/bin/env python3
"""
Health check script for PixelFly Backend
Can be used to verify the deployment is working correctly
"""

import requests
import sys
import json
import time

def check_health(base_url):
    """Check if the service is healthy"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def check_endpoints(base_url):
    """Check if main endpoints are accessible"""
    endpoints = [
        "/",
        "/health",
        "/api/capabilities"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            results[endpoint] = {
                "status_code": response.status_code,
                "accessible": response.status_code < 500
            }
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
            else:
                print(f"⚠️ {endpoint}: {response.status_code}")
        except Exception as e:
            results[endpoint] = {
                "status_code": None,
                "accessible": False,
                "error": str(e)
            }
            print(f"❌ {endpoint}: {e}")
    
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <base_url>")
        print("Example: python health_check.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print(f"🔍 Checking PixelFly Backend at: {base_url}")
    print("-" * 50)
    
    # Basic health check
    if not check_health(base_url):
        print("❌ Basic health check failed")
        sys.exit(1)
    
    print()
    
    # Check all endpoints
    print("🔍 Checking endpoints...")
    results = check_endpoints(base_url)
    
    # Summary
    print("\n" + "=" * 50)
    accessible_count = sum(1 for r in results.values() if r.get('accessible', False))
    total_count = len(results)
    
    if accessible_count == total_count:
        print(f"✅ All {total_count} endpoints are accessible")
        print("🚀 Deployment appears to be successful!")
    else:
        print(f"⚠️ {accessible_count}/{total_count} endpoints are accessible")
        print("🔧 Some endpoints may need attention")
    
    print(f"\n📊 Results summary:")
    for endpoint, result in results.items():
        status = "✅" if result.get('accessible') else "❌"
        print(f"  {status} {endpoint}: {result.get('status_code', 'ERROR')}")

if __name__ == "__main__":
    main()
