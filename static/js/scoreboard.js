var get_scores = function() {
	fetch("/scores")
	.then(res => res.json())
	.then(out => out.forEach(
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
						var row = document.getElementById("fullscorestable").insertRow(-1)
						row.insertCell(0).innerHTML = i
						row.insertCell(1).innerHTML = score["name"]
						row.insertCell(2).innerHTML = score["score"]
						row.classList.add("text-light")
						break;
				}
			}
		)
	)
	.catch(err => console.log(err))
}
