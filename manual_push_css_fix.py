import os
import subprocess
import sys

print("🔧 Manual Push for CSS Fix")
print("=" * 40)

# Change to project directory
project_dir = r"C:\Users\yoshitaka\daily-ai-news"
os.chdir(project_dir)
print(f"📁 Working directory: {os.getcwd()}")

# Check if CSS generation is in the file
with open("build_simple_ranking.py", "r", encoding="utf-8") as f:
    content = f.read()
    has_generate_css = "def generate_css():" in content
    has_css_call = "css_content = generate_css()" in content
    
print(f"✅ generate_css function present: {has_generate_css}")
print(f"✅ CSS generation call present: {has_css_call}")

if has_generate_css and has_css_call:
    print("\n📝 CSS generation fix is ready to push!")
    
    # Commands to execute
    commands = [
        "git add build_simple_ranking.py",
        'git commit -m "fix: Add CSS generation to build_simple_ranking.py - resolve styling issues"',
        "git push origin main"
    ]
    
    print("\n🚀 Executing git commands...")
    
    for cmd in commands:
        print(f"\n⚙️ Running: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Success")
                if result.stdout.strip():
                    print(f"   {result.stdout.strip()}")
            else:
                print(f"❌ Failed: {result.stderr.strip()}")
                if "nothing to commit" in result.stderr:
                    print("   (Already committed or no changes)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Push process completed!")
    print("📍 Next step: Manually trigger GitHub Actions workflow")
    print("🔗 https://github.com/awano27/daily-ai-news/actions")
    
else:
    print("❌ CSS generation fix not found in local file!")
    sys.exit(1)