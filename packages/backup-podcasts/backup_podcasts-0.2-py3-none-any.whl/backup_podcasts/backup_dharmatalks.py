import traceback
from pathlib import Path

from backup_podcasts import backup_feed, log
from joblib import Parallel, delayed
from tqdm import tqdm

if __name__ == "__main__":
	Parallel(n_jobs=8)(delayed(backup_feed)(f"https://dharmaseed.org/feeds/teacher/{i}/?max-entries=all", Path("E:\\Podcasts\\Dharma Seed")) for i in tqdm(range(1600)))