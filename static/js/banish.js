var get_scores = function() {
	fetch("/scores")
	.then(res => res.json())
	.then(out => {
			const banishselect = document.getElementById("banish-select");
			out.forEach(
				function(score, i) {
					var option = document.createElement("OPTION");
					option.text = score["name"];
					option.value = score["name"];
					banishselect.add(option);
				}
			)
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
