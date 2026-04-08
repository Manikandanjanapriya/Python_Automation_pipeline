import subprocess, sys
from datetime import datetime
def run_step(script, label):
 print(f'\n{"="*50}')
 print(f' STEP: {label}')
 print(f'{"="*50}')
 result = subprocess.run([sys.executable, script])
 if result.returncode != 0:
     print(f' ERROR in {script}. Pipeline stopped.')
     sys.exit(1)
     print(f' DONE: {label}')
if __name__ == '__main__':
    start = datetime.now()
    print(f'\nMASTER PIPELINE started: {start:%Y-%m-%d %H:%M:%S}')
    run_step('scraper.py', '1/3 Web Scraping')
    run_step('excel_bot.py', '2/3 Excel Report')
    run_step('email_bot.py', '3/3 Email Distribution')
    elapsed = (datetime.now() - start).seconds
    print(f'\nALL COMPLETE in {elapsed}s')
