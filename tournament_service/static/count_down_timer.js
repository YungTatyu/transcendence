class CountDownTimer {
	/**
	 * @param {HTMLElement} element タイマーを表示するHTML要素
	 */
	constructor(element) {
		if (!element) {
			throw new Error("Elements are required to create a CountDownTimer");
		}
		this.timerElement = element;
		this.startTime = -1;
		this.intervalId = null;
	}

	start(startTime) {
		this.startTime = startTime;
        this.timerElement.style.display = "block";
		this.updateUI(); // インスタン作成時のUI更新
		const oneSecond = 1000;
		this.intervalId = setInterval(() => this.updateUI(), oneSecond); // 毎秒UIを更新
	}

	clear() {
        this.timerElement.style.display = "none";
		this.startTIme = -1;
		if (this.intervalId) {
			clearInterval(this.intervalId);
			this.intervalId = null;
		}
	}

	updateUI() {
		const remainingTime = this.calcTime();
		if (remainingTime > 0) {
			this.timerElement.textContent = `Tournament is forced to start after ${remainingTime} seconds`;
		} else {
			this.timerElement.textContent = "Tournaments will begin soon!";
		}
	}

	/**
	 * 残り時間を計算
	 * @returns {number} 残り秒数 or 0
	 */
	calcTime() {
		const currentUnixTime = Date.now() / 1000;
		return Math.max(Math.round(this.startTime - currentUnixTime), 0);
	}
}
