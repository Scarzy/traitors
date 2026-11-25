var get_scores = function() {
	fetch("/scores")
	.then(res => res.json())
	.then(out => {
			const tbody = document.getElementById("fullscorestable");
			const fragment = document.createDocumentFragment();
			out.forEach(
				function(score, i) {
					switch (i) {
						case 0:
							document.getElementById("firstplacename").textContent = score["name"]
							document.getElementById("firstplacescore").textContent = score["score"]
							break;
						case 1:
							document.getElementById("secondplacename").textContent = score["name"]
							document.getElementById("secondplacescore").textContent = score["score"]
							break;
						case 2:
							document.getElementById("thirdplacename").textContent = score["name"]
							document.getElementById("thirdplacescore").textContent = score["score"]
							break;
						default:
							var row = document.createElement("tr");
							row.insertCell(0).innerHTML = i
							row.insertCell(1).innerHTML = score["name"]
							row.insertCell(2).innerHTML = score["score"]
							row.classList.add("text-light")
							fragment.appendChild(row);
							break;
					}
				}
			)
			tbody.replaceChildren(fragment);
		}
	)
	.catch(err => console.log(err))
}

var start_timers = function() {
	setInterval(get_scores, 1000);
	setInterval(get_thresholds, 1000);
	setInterval(get_voting_valid, 1000);
}

var get_thresholds = function() {
	fetch("/thresholds")
	.then(res => res.json())
	.then(out => {
			document.getElementById("murderthreshold").textContent = out["murderthreshold"]
			document.getElementById("recruitthreshold").textContent = out["recruitthreshold"]
			document.getElementById("banishthreshold").textContent = out["banishthreshold"]
		}
	)
	.catch(err => console.log(err))
}

var get_voting_valid = function() {
	fetch("/votingtime")
	.then(res => res.json())
	.then(out => {
			//document.getElementById("murderthreshold").textContent = out["murderthreshold"]
			//document.getElementById("recruitthreshold").textContent = out["recruitthreshold"]
			//document.getElementById("banishthreshold").textContent = out["banishthreshold"]
		}
	)
	.catch(err => console.log(err))
}
