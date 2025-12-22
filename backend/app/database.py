# # backend/app/database.py
# from supabase import create_client, Client
# import os

# # 1. رابط المشروع 
# SUPABASE_URL = "https://catkzlbzcjlkngrjrmql.supabase.co" 

# # 2. المفتاح السري 
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNhdGt6bGJ6Y2psa25ncmpybXFsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzE0NDg2MiwiZXhwIjoyMDc4NzIwODYyfQ.7B3zh_2_8W6MyUCzjRk-CpNq8jJ1gf61RVpwwX4vxOk"

# try:
#     supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY )
#     print(" Successfully connected to Supabase!")
# except Exception as e:
#     print(f" Error connecting to Supabase: {e}")
#     supabase = None
